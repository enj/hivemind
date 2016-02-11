#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents a Pipeline of Tasks."""

from networkx import DiGraph
from re import compile

from util import to_bool


class PipelineFramework(object):
    """A Pipeline is a series of sequential Tasks."""

    def __init__(self, *tasks_reqs):
        """Construct a Pipeline based on the given Tasks by linking them together.

        :param *tasks: A list of Tasks from which to create the Pipeline
        :type *tasks: iterable of Tasks
        """

        self.dag = DiGraph()
        task_dict = {}
        for task, _ in tasks_reqs:
            self.dag.add_node(task, done=False)
            task_dict[task._uid] = task

        for task, reqs in tasks_reqs:
            for req_uid in reqs:
                self.dag.add_edge(task_dict[req_uid], task)


class ConcretePipeline(object):

    def __init__(self, pid, framework, data):
        self.dag = framework.dag.copy()
        self.framework_to_concrete(pid, data)

    def framework_to_concrete(self, pid, data):
        for task in self.dag.nodes():
            task._pid = pid
            all_fields = vars(task)
            public_fields = {field: value for field, value in all_fields.iteritems() if not field.startswith('_')}
            for field, value in public_fields.iteritems():
                all_fields[field] = self.replace_values(value, data)
                self.validate_field(all_fields[field])
            task.skip = to_bool(task.skip)

    def replace_values(self, value, data):
        if isinstance(value, str):
            return self.replace_variable(value, data)
        elif isinstance(value, list):
            return [self.replace_variable(v, data) for v in value]
        elif isinstance(value, bool):
            return value
        elif isinstance(value, unicode):
            return self.replace_values(value.encode('ascii', 'ignore'), data)
        else:
            raise Exception

    def replace_variable(self, string, data):
        if not data.get(string):
            return string
        pattern = compile('|'.join(data.keys()))
        return pattern.sub(lambda x: data[x.group()], data[string])

    def validate_field(self, field):
        if isinstance(field, bool):
            return
        if field is None:
            return
        if isinstance(field, list):
            for a in field:
                self.validate_field(a)
            return

        pattern = compile('\$\$.*\$\$')
        if pattern.match(field):
            raise Exception

    def __len__(self):
        """Determine the length of the Pipeline.

        :returns: the number of Tasks in this Pipeline
        :rtype: {int}
        """
        return self.dag.__len__()

    def set_done(self, task):
        self.dag.node[task]['done'] = True

    def is_done(self, task):
        return self.dag.node[task]['done']

    def get_ready_successors(self, task):
        ready_successors = []
        for successor in self.dag.successors(task):
            predecessors = self.dag.predecessors_iter(successor)
            predecessor_state = (self.is_done(predecessor) for predecessor in predecessors)
            if all(predecessor_state):
                ready_successors.append(successor)
        return ready_successors
