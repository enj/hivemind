import unittest
import networkx as nx

from hivemind.pipeline import PipelineFramework, ConcretePipeline
from datagenerator import DataGenerator


class TestPipeline(unittest.TestCase):

    def setUp(self):
        self.dg = DataGenerator()

    def test_create_empty_framework(self):
        with self.assertRaises(Exception):
            self.dg.get_empty_pipeline()

    def test_single_node_framework(self):
        p = self.dg.get_single_node_pipeline()
        self.assertTrue(type(p) is PipelineFramework)
        self.assertEquals(len(p), 1)
        self.assertTrue(nx.is_tree(p.dag))

    def test_linear_framework(self):
        p = self.dg.get_linear_pipeline()
        self.assertTrue(type(p) is PipelineFramework)
        self.assertEquals(len(p), 3)
        self.assertTrue(nx.is_tree(p.dag))

    def test_tree_framework(self):
        p = self.dg.get_tree_pipeline()
        self.assertTrue(type(p) is PipelineFramework)
        self.assertEquals(len(p), 7)
        self.assertTrue(nx.is_tree(p.dag))

    def test_dag_framework(self):
        p = self.dg.get_dag_pipeline()
        self.assertTrue(type(p) is PipelineFramework)
        self.assertEquals(len(p), 7)
        self.assertTrue(nx.is_directed_acyclic_graph(p.dag))

    def test_cyclic_framework(self):
        with self.assertRaises(Exception):
            self.dg.get_cyclic_pipeline()

    def test_disconnected_framework(self):
        p = self.dg.get_disconnected_pipeline()
        self.assertTrue(type(p) is PipelineFramework)
        self.assertEquals(len(p), 5)
        self.assertTrue(nx.is_directed_acyclic_graph(p.dag))

    def test_unbalanced_framework(self):
        p = self.dg.get_unbalanced_pipeline()
        self.assertTrue(type(p) is PipelineFramework)
        self.assertEquals(len(p), 7)
        self.assertTrue(nx.is_tree(p.dag))

    def test_ranktree_framework(self):
        p = self.dg.get_ranktree_pipeline()
        self.assertTrue(type(p) is PipelineFramework)
        self.assertEquals(len(p), 14)
        self.assertTrue(nx.is_tree(p.dag))

    def test_loose_framework(self):
        p = self.dg.get_loose_pipeline()
        self.assertTrue(type(p) is PipelineFramework)
        self.assertEquals(len(p), 6)
        self.assertTrue(nx.is_directed_acyclic_graph(p.dag))

    def test_self_ref_framework(self):
        with self.assertRaises(Exception):
            self.dg.get_self_ref_pipeline()

    def test_duplicate_node_framework(self):
        with self.assertRaises(Exception):
            self.dg.get_duplicate_node_pipeline()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPipeline)
    unittest.TextTestRunner(verbosity=2).run(suite)
    #unittest.main()
