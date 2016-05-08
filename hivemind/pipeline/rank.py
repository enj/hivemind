#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Custom rank functions."""


def rank_by_total_successors(framework):
    """Rank the input framework by the total successors of each Task.

    :param framework: the input PipelineFramework
    :type framework: PipelineFramework
    """
    def rank(task):
        """Determine the rank based on total successors of this Task.

        :param task: The input Task
        :type task: Task
        :returns: The total successors of this Task + 1
        :rtype: {int}
        """
        if task._rank is not None:
            return task._rank

        r = 0
        for successor in framework.dag.successors_iter(task):
            r += rank(successor)
            r += 1
        task._rank = r
        return r

    for task in zero_in_degree(framework.dag):
        rank(task)


def rank_by_successors(framework):
    """Rank the input framework by the immediate successors of each Task.

    :param framework: the input PipelineFramework
    :type framework: PipelineFramework
    """
    for task in framework.dag.nodes_iter():
        task._rank = framework.dag.out_degree(task)


def zero_in_degree(dag):
    """Get all Tasks from the input DAG that have no predecessors.

    :param dag: the input DAG
    :type dag: DiGraph
    :returns: A generator of Tasks that have no predecessors
    :rtype: {generator}
    """
    for task, in_degree in dag.in_degree_iter():
        if in_degree == 0:
            yield task
