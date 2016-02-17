#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents a Pipeline of Tasks."""

from re import compile as re_compile
from os.path import isfile

from networkx import DiGraph

from ..util import to_bool


class PipelineFramework(object):
    """A Pipeline is a series of sequential Tasks."""

    def __init__(self, tasks_reqs):
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

    def __init__(self, pid, framework, data, checkpoint_dir):
        self.pid = pid
        self.checkpoint_dir = checkpoint_dir
        self.dag = framework.dag.copy()
        self.framework_to_concrete(data)

    def framework_to_concrete(self, data):
        for task in self.dag.nodes_iter():
            task._pid = self.pid
            all_fields = vars(task)
            for field, value in all_fields.iteritems():
                if not field.startswith('_'):
                    all_fields[field] = self.replace_values(value, data)
                    self.validate_field(all_fields[field])
            task.skip = to_bool(task.skip)

    def replace_values(self, value, data):
        if isinstance(value, str):
            return self.replace_variable(value, data)
        elif isinstance(value, list):
            return [self.replace_values(v, data) for v in value]
        elif isinstance(value, bool):
            return value
        elif isinstance(value, unicode):
            return self.replace_variable(value.encode('ascii', 'ignore'), data)
        else:
            raise Exception

    def replace_variable(self, string, data):
        if data.get(string) is None:
            return string
        pattern = re_compile('|'.join(data.keys()))
        return pattern.sub(lambda x: data[x.group()], data[string])

    def validate_field(self, field):
        if field is None or isinstance(field, bool):
            return

        if isinstance(field, list):
            for a in field:
                self.validate_field(a)
            return

        pattern = re_compile('\$\$.*\$\$')
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

    def is_done_by_file(self, task):
        f = "%s/%d/%s/_.done" % (self.checkpoint_dir, self.pid, task._uid)
        if isfile(f):
            self.set_done(task)
        return self.is_done(task)

    def get_ready_successors(self, task):
        for successor in self.dag.successors_iter(task):
            predecessors = self.dag.predecessors_iter(successor)
            predecessor_state = (self.is_done(predecessor) for predecessor in predecessors)
            if all(predecessor_state):
                yield successor

    def get_ready_tasks(self):
        for task in self.dag.nodes_iter():
            predecessors = self.dag.predecessors_iter(task)
            predecessor_state = (self.is_done(predecessor) for predecessor in predecessors)
            if not self.is_done(task) and all(predecessor_state):
                yield task
