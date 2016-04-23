#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents a Pipeline of Tasks."""

from re import escape, match as re_match, sub as re_sub, findall
from os.path import isfile

from networkx import DiGraph, is_directed_acyclic_graph as is_dag, maximal_independent_set, transitive_closure

from ..util import to_bool, join

# MIS only works for standard graphs because of how 'neighbors' is implemented
# It is better to copy a method pointer instead of the whole graph
DiGraph.neighbors = lambda graph, task: graph.successors(task) + graph.predecessors(task)


class PipelineFramework(object):
    """A PipelineFramework is a set Tasks that may have data dependencies."""

    def __init__(self, tasks_reqs):
        """Construct a PipelineFramework based on the given Tasks and their requirements.

        A PipelineFramework is the structure of the pipeline, it contains no patient data.

        :param tasks_reqs: the Tasks and their requirements
        :type tasks_reqs: iterable of tuples, each with a Task and its list of required UIDs
        :raises: ValueError
        """
        self.dag = DiGraph()
        task_dict = {}
        for task, _ in tasks_reqs:
            if self.dag.has_node(task):
                raise ValueError("Pipeline contains duplicate Task {}".format(task))
            self.dag.add_node(task, done=False)
            task_dict[task._uid] = task

        for task, reqs in tasks_reqs:
            for req_uid in reqs:
                uid = task_dict.get(req_uid)
                if uid is None:
                    raise ValueError("Unknown UID {} set as requirement for {}".format(req_uid, task))
                self.dag.add_edge(uid, task)

        if not is_dag(self.dag):
            raise ValueError("Pipeline contains a cycle.")

    def __len__(self):
        """Determine the length of the Pipeline.

        :returns: the number of Tasks in this Pipeline
        :rtype: {int}
        """
        return self.dag.__len__()


class ConcretePipeline(object):
    """A ConcretePipeline represents a single patient's pipeline."""

    # Number of times to run maximal_independent_set during max concurrency calculation
    MAX_ROUNDS = 64

    def __init__(self, pid, framework, data, checkpoint_dir):
        """Build a ConcretePipeline using a PipelineFramework and the CSV data.

        :param pid: the PID for this patient
        :type pid: int
        :param framework: the framework to build this ConcretePipeline from
        :type framework: PipelineFramework
        :param data: key/value mapping for all variables
        :type data: dictionary
        :param checkpoint_dir: the checkpoint directory
        :type checkpoint_dir: string
        """
        self.pid = pid
        self.checkpoint_dir = checkpoint_dir
        self.dag = framework.dag.copy()
        self.framework_to_concrete(data)
        self.tc = transitive_closure(self.dag)
        self.update_max_concurrency()

    def framework_to_concrete(self, data):
        """Replace all $$ variables for every Task in the pipeline.

        Sets the PID and checkpoint directory for all Tasks.
        Fields are validated after variable replacement.

        :param data: key/value mapping for all variables
        :type data: dictionary
        """
        for task in self.dag.nodes_iter():
            task._pid = self.pid
            task._checkpoint_dir = self.checkpoint_dir
            all_fields = vars(task)
            for field, value in all_fields.iteritems():
                # The only field where None is valid
                if field == "verify_exe" and value is None:
                    continue
                if not field.startswith("_"):
                    all_fields[field] = self.replace_values(value, data)
                    self.validate_field(all_fields[field])
            task.skip = to_bool(task.skip)
            task.shell = to_bool(task.shell)

    def replace_values(self, value, data):
        """Replace any $$ variables in the given input using the associated values in data.

        If value is a list, all items in the list are replaced, recursively.

        :param value: the input value, can be a variety of types
        :param data: key/value mapping for all variables
        :type data: dictionary
        :returns: the value with all $$ variables replaced
        :raises: TypeError
        """
        if isinstance(value, str):
            return self.replace_variable(value, data)
        elif isinstance(value, list):
            return [self.replace_values(v, data) for v in value]
        elif isinstance(value, bool):
            return value
        elif isinstance(value, unicode):
            return self.replace_variable(value.encode("ascii", "ignore"), data)
        else:
            raise TypeError("Invalid type specified for value {}".format(value))

    def replace_variable(self, string, data):
        """Replace any $$ variables in the given string using the associated values in data.

        :param string: the input string
        :type string: string
        :param data: key/value mapping for all variables
        :type data: dictionary
        :returns: the string with variables replaced
        :rtype: {string}
        """
        matches = findall(r"(\$\$.*?\$\$)", string)
        if not matches:
            return string

        for match in matches:
            if not data.get(match):
                continue
            string = re_sub(ur"(.*){0}(.*)".format(escape(match)), ur"\g<1>{0}\g<2>".format(data[match]), string)
        return string

    def validate_field(self, field):
        """Test to make sure that all $$ variables have been replaced in the given field.

        :param field: the field to validate
        :raises: ValueError
        """
        if field is None or isinstance(field, bool):
            return

        if isinstance(field, list):
            for a in field:
                self.validate_field(a)
            return

        if re_match(r"\$\$", field):
            raise ValueError("Not all $$ variables replaced in {}".format(field))

    def __len__(self):
        """Determine the length of the Pipeline.

        :returns: the number of Tasks in this Pipeline
        :rtype: {int}
        """
        return self.dag.__len__()

    def set_done(self, task):
        """Set the given Task as done.

        :param task: the input Task
        :type task: Task
        """
        self.dag.node[task]["done"] = True

    def is_done(self, task):
        """Determine if the given Task is done.  Does NOT take checkpointing into account.

        :param task: the input Task
        :type task: Task
        :returns: if the Task is done
        :rtype: {bool}
        """
        return self.dag.node[task]["done"]

    def is_done_by_file(self, task):
        """Determine if the given Task is done.  Takes checkpointing into account.

        :param task: the input Task
        :type task: Task
        :returns: if the Task is done
        :rtype: {bool}
        """
        f = join(self.checkpoint_dir, str(self.pid), str(task._uid), "_.done")
        if isfile(f):
            self.set_done(task)
        return self.is_done(task)

    def get_ready_successors(self, task):
        """Get the ready successors of the given Task.

        :param task: the input Task
        :type task: Task
        :returns: generator of successor Tasks that are ready to run
        :rtype: {generator}
        """
        for successor in self.dag.successors_iter(task):
            predecessors = self.dag.predecessors_iter(successor)
            predecessor_state = (self.is_done(predecessor) for predecessor in predecessors)
            if all(predecessor_state):
                yield successor

    def get_ready_tasks(self):
        """Get all Tasks that can be run.

        :returns: generator of Tasks that are ready to run
        :rtype: {generator}
        """
        for task in self.dag.nodes_iter():
            predecessors = self.dag.predecessors_iter(task)
            predecessor_state = (self.is_done(predecessor) for predecessor in predecessors)
            if not self.is_done(task) and all(predecessor_state):
                yield task

    def get_completed_tasks(self):
        """Get number of completed tasks.  Takes checkpointing into account.

        :returns: number of completed tasks
        :rtype: {int}
        """
        completed_tasks = 0
        for task in self.dag.nodes_iter():
            if self.is_done_by_file(task):
                completed_tasks += 1
        return completed_tasks

    def update_max_concurrency(self):
        """
        Determine the maximum number of concurrent Tasks that can still run.

        This is based on the maximal independent set of the subgraph
        of the transitive closure of the Tasks that are not done.

        The maximal_independent_set based on a random algorithm and thus must
        be run multiple times to have a high chance of getting the max value.

        The calculation for sg is highly optimized.  The more straightforward implementation is:
        sg = transitive_closure(self.dag.subgraph(n for n in self.dag.nodes_iter() if not self.is_done(n))).to_undirected()

        This will work even without modifying the neighbors method of DiGraph
        and does not require storing of the transitive closure.  However,
        it makes many unnecessary copies of the DAG and thus should be avoided.

        This method is called quite often by the Master, and thus needs to be as
        fast as possible.  Setting a higher MAX_ROUNDS is not recommended.
        """
        # Get the subgraph of the transitive closure based on the uncompleted tasks
        sg = self.tc.subgraph(n for n in self.dag.nodes_iter() if not self.is_done(n))

        # Cannot get the independent set of an empty graph
        if len(sg) == 0:
            self.mc = 0
            return

        # There are many independent sets. Loop through MAX_ROUNDS times to get longest
        # With 64 rounds it has 99.9999% chance of getting the correct value
        self.mc = max(len(maximal_independent_set(sg)) for _ in xrange(self.MAX_ROUNDS))
