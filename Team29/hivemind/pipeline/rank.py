#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Custom rank functions."""


def rank_by_total_successors(framework):

    def rank(task):
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
    for task in framework.dag.nodes_iter():
        task._rank = framework.dag.out_degree(task)


def zero_in_degree(dag):
    for task, in_degree in dag.in_degree_iter():
        if in_degree == 0:
            yield task
