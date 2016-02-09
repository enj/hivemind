#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents a Pipeline of Tasks."""

from networkx import DiGraph


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
            task_dict[task.uid] = task

        for task, reqs in tasks_reqs:
            for req_uid in reqs:
                self.dag.add_edge(task_dict[req_uid], task)

class ConcretePipeline(object):

    def __init__(self):
        pass

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
            for predecessor in self.dag.predecessors(successor):
                if not self.is_done(predecessor):
                    break
            else:
                ready_successors.append(successor)

        return ready_successors
