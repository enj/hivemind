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
        return PipelineFramework([(Task("A", False, False, "", None, ""), [])])

    def get_linear_pipeline(self):
        return PipelineFramework([
            (Task("A", False, False, "", None, ""), []),
            (Task("B", False, False, "", None, ""), ["A"]),
            (Task("C", False, False, "", None, ""), ["B"])
        ])

    def get_tree_pipeline(self):
        return PipelineFramework([
            (Task("A", False, False, "", None, ""), []),
            (Task("B", False, False, "", None, ""), ["A"]),
            (Task("C", False, False, "", None, ""), ["A"]),
            (Task("D", False, False, "", None, ""), ["B"]),
            (Task("E", False, False, "", None, ""), ["B"]),
            (Task("F", False, False, "", None, ""), ["C"]),
            (Task("G", False, False, "", None, ""), ["C"])
        ])

    def get_dag_pipeline(self):
        return PipelineFramework([
            (Task("A", False, False, "", None, ""), []),
            (Task("B", False, False, "", None, ""), []),
            (Task("C", False, False, "", None, ""), ["A"]),
            (Task("D", False, False, "", None, ""), ["C"]),
            (Task("E", False, False, "", None, ""), ["C"]),
            (Task("F", False, False, "", None, ""), ["B", "C"]),
            (Task("G", False, False, "", None, ""), ["D", "F"])
        ])

    def get_cyclic_pipeline(self):
        return PipelineFramework([
            (Task("A", False, False, "", None, ""), ["C"]),
            (Task("B", False, False, "", None, ""), ["A"]),
            (Task("C", False, False, "", None, ""), ["B"])
        ])

    def get_disconnected_pipeline(self):
        return PipelineFramework([
            (Task("A", False, False, "", None, ""), []),
            (Task("B", False, False, "", None, ""), ["A"]),
            (Task("C", False, False, "", None, ""), []),
            (Task("D", False, False, "", None, ""), ["C"]),
            (Task("E", False, False, "", None, ""), ["C"])
        ])

    def get_unbalanced_pipeline(self):
        return PipelineFramework([
            (Task("A", False, False, "", None, ""), []),
            (Task("B", False, False, "", None, ""), ["A"]),
            (Task("C", False, False, "", None, ""), ["A"]),
            (Task("D", False, False, "", None, ""), ["B"]),
            (Task("E", False, False, "", None, ""), ["D"]),
            (Task("F", False, False, "", None, ""), ["D"]),
            (Task("G", False, False, "", None, ""), ["D"])
        ])

    def get_ranktree_pipeline(self):
        """Differently unbalanced depending on ranking method"""
        return PipelineFramework([
            (Task("A", False, False, "", None, ""), []),
            (Task("B", False, False, "", None, ""), ["A"]),
            (Task("C", False, False, "", None, ""), ["A"]),
            (Task("D", False, False, "", None, ""), ["B"]),
            (Task("E", False, False, "", None, ""), ["B"]),
            (Task("F", False, False, "", None, ""), ["D"]),
            (Task("G", False, False, "", None, ""), ["D"]),
            (Task("H", False, False, "", None, ""), ["E"]),
            (Task("I", False, False, "", None, ""), ["E"]),
            (Task("J", False, False, "", None, ""), ["C"]),
            (Task("K", False, False, "", None, ""), ["C"]),
            (Task("L", False, False, "", None, ""), ["C"]),
            (Task("M", False, False, "", None, ""), ["C"]),
            (Task("N", False, False, "", None, ""), ["C"])
        ])

    def get_self_ref_pipeline(self):
        return PipelineFramework([
            (Task("A", False, False, "", None, ""), ["A"])
        ])

    def get_duplicate_node_pipeline(self):
        return PipelineFramework([
            (Task("A", False, False, "", None, ""), []),
            (Task("A", False, False, "", None, ""), [])
        ])

    def get_loose_pipeline(self):
        return PipelineFramework([
            (Task("A", False, False, "", None, ""), []),
            (Task("B", False, False, "", None, ""), []),
            (Task("C", False, False, "", None, ""), []),
            (Task("D", False, False, "", None, ""), []),
            (Task("E", False, False, "", None, ""), []),
            (Task("F", False, False, "", None, ""), [])
        ])

    def get_args(self):
        return {
            "$$a1$$": "val_for_a1",
            "$$a2$$": "secondParameter",
            "$$a3$$": "a_3rd_one",
            "$$a4$$": "4",
            "$$skip1$$": "t",
            "$$skip2$$": "TRUE",
            "$$skip3$$": "1",
            "$$skip4$$": 1,
            "$$skip5$$": "f",
            "$$skip6$$": "False"
        }
