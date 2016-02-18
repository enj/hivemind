#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents a Pipeline of Tasks."""

from hivemind.pipeline import PipelineFramework
from hivemind.pipeline import Task


class DataGenerator(object):
    def __init__(self):
        pass

    def get_empty_pipeline(self):
        return PipelineFramework([()])

    def get_single_node_pipeline(self):
        return PipelineFramework([(Task("A", False, "", "", []), [])])

    def get_linear_pipeline(self):
        return PipelineFramework([
            (Task("A", False, "", "", []), []),
            (Task("B", False, "", "", []), ["A"]),
            (Task("C", False, "", "", []), ["B"])
        ])

    def get_tree_pipeline(self):
        return PipelineFramework([
            (Task("A", False, "", "", []), []),
            (Task("B", False, "", "", []), ["A"]),
            (Task("C", False, "", "", []), ["A"]),
            (Task("D", False, "", "", []), ["B"]),
            (Task("E", False, "", "", []), ["B"]),
            (Task("F", False, "", "", []), ["C"]),
            (Task("G", False, "", "", []), ["C"])
        ])

    def get_dag_pipeline(self):
        return PipelineFramework([
            (Task("A", False, "", "", []), []),
            (Task("B", False, "", "", []), []),
            (Task("C", False, "", "", []), ["A"]),
            (Task("D", False, "", "", []), ["C"]),
            (Task("E", False, "", "", []), ["C"]),
            (Task("F", False, "", "", []), ["B", "C"]),
            (Task("G", False, "", "", []), ["D", "F"])
        ])

    def get_cyclic_pipeline(self):
        return PipelineFramework([
            (Task("A", False, "", "", []), ["C"]),
            (Task("B", False, "", "", []), ["A"]),
            (Task("C", False, "", "", []), ["B"])
        ])

    def get_disconnected_pipeline(self):
        return PipelineFramework([
            (Task("A", False, "", "", []), []),
            (Task("B", False, "", "", []), ["A"]),
            (Task("C", False, "", "", []), []),
            (Task("D", False, "", "", []), ["C"]),
            (Task("E", False, "", "", []), ["C"])
        ])
