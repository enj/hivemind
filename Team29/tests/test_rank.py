import unittest

import hivemind.pipeline.rank as ranker
from datagenerator import DataGenerator


class TestRank(unittest.TestCase):

    def setUp(self):
        self.dag = DataGenerator()

    def test_rank_by_total_successors_linear(self):
        p = self.dag.get_linear_pipeline()
        ranker.rank_by_total_successors(p)
        ranks = {task._uid: task._rank for task in p.dag.node}
        expected = {'A': 2, 'B': 1, 'C': 0}
        self.assertEqual(ranks, expected)

    def test_rank_by_total_successors_tree(self):
        p = self.dag.get_tree_pipeline()
        ranker.rank_by_total_successors(p)
        ranks = {task._uid: task._rank for task in p.dag.node}
        expected = {'A': 6, 'B': 2, 'C': 2, 'D': 0, 'E': 0, 'F': 0, 'G': 0}
        self.assertEqual(ranks, expected)

    def test_rank_by_total_successors_dag(self):
        p = self.dag.get_dag_pipeline()
        ranker.rank_by_total_successors(p)
        ranks = {task._uid: task._rank for task in p.dag.node}
        expected = {'A': 6, 'B': 2, 'C': 5, 'D': 1, 'E': 0, 'F': 1, 'G': 0}
        self.assertEqual(ranks, expected)

    def test_rank_by_total_successors_dag_disconected(self):
        p = self.dag.get_disconnected_pipeline()
        ranker.rank_by_total_successors(p)
        ranks = {task._uid: task._rank for task in p.dag.node}
        expected = {'A': 1, 'B': 0, 'C': 2, 'D': 0, 'E': 0}
        self.assertEqual(ranks, expected)

    def test_rank_by_total_successors_single_node(self):
        p = self.dag.get_single_node_pipeline()
        ranker.rank_by_total_successors(p)
        ranks = {task._uid: task._rank for task in p.dag.node}
        expected = {'A': 0}
        self.assertEqual(ranks, expected)

    def test_rank_by_total_successors_unbalanced_pipeline(self):
        p = self.dag.get_unbalanced_pipeline()
        ranker.rank_by_total_successors(p)
        ranks = {task._uid: task._rank for task in p.dag.node}
        expected = {'A': 6, 'B': 4, 'C': 0, 'D': 3, 'E': 0, 'F': 0, 'G': 0}
        self.assertEqual(ranks, expected)

    def test_rank_by_total_successors_ranktree_pipeline(self):
        p = self.dag.get_ranktree_pipeline()
        ranker.rank_by_total_successors(p)
        ranks = {task._uid: task._rank for task in p.dag.node}
        expected = {'A': 13, 'B': 6, 'C': 5, 'D': 2, 'E': 2, 'F': 0, 'G': 0,
                    'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0}
        self.assertEqual(ranks, expected)

    def test_rank_by_total_successors_loose_pipeline(self):
        p = self.dag.get_loose_pipeline()
        ranker.rank_by_total_successors(p)
        ranks = {task._uid: task._rank for task in p.dag.node}
        expected = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}
        self.assertEqual(ranks, expected)

    def test_rank_by_successors_linear(self):
        p = self.dag.get_linear_pipeline()
        ranker.rank_by_successors(p)
        ranks = {task._uid: task._rank for task in p.dag.node}
        expected = {'A': 1, 'B': 1, 'C': 0}
        self.assertEqual(ranks, expected)

    def test_rank_by_successors_tree(self):
        p = self.dag.get_tree_pipeline()
        ranker.rank_by_successors(p)
        ranks = {task._uid: task._rank for task in p.dag.node}
        expected = {'A': 2, 'B': 2, 'C': 2, 'D': 0, 'E': 0, 'F': 0, 'G': 0}
        self.assertEqual(ranks, expected)

    def test_rank_by_successors_dag(self):
        p = self.dag.get_dag_pipeline()
        ranker.rank_by_successors(p)
        ranks = {task._uid: task._rank for task in p.dag.node}
        expected = {'A': 1, 'B': 1, 'C': 3, 'D': 1, 'E': 0, 'F': 1, 'G': 0}
        self.assertEqual(ranks, expected)

    def test_rank_by_successors_dag_disconected(self):
        p = self.dag.get_disconnected_pipeline()
        ranker.rank_by_successors(p)
        ranks = {task._uid: task._rank for task in p.dag.node}
        expected = {'A': 1, 'B': 0, 'C': 2, 'D': 0, 'E': 0}
        self.assertEqual(ranks, expected)

    def test_rank_by_successors_single_node(self):
        p = self.dag.get_single_node_pipeline()
        ranker.rank_by_total_successors(p)
        ranks = {task._uid: task._rank for task in p.dag.node}
        expected = {'A': 0}
        self.assertEqual(ranks, expected)

    def test_rank_by_successors_unbalanced_pipeline(self):
        p = self.dag.get_unbalanced_pipeline()
        ranker.rank_by_successors(p)
        ranks = {task._uid: task._rank for task in p.dag.node}
        expected = {'A': 2, 'B': 1, 'C': 0, 'D': 3, 'E': 0, 'F': 0, 'G': 0}
        self.assertEqual(ranks, expected)

    def test_rank_by_successors_ranktree_pipeline(self):
        p = self.dag.get_ranktree_pipeline()
        ranker.rank_by_successors(p)
        ranks = {task._uid: task._rank for task in p.dag.node}
        expected = {'A': 2, 'B': 2, 'C': 5, 'D': 2, 'E': 2, 'F': 0, 'G': 0,
                    'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0}
        self.assertEqual(ranks, expected)

    def test_rank_by_successors_loose_pipeline(self):
        p = self.dag.get_loose_pipeline()
        ranker.rank_by_successors(p)
        ranks = {task._uid: task._rank for task in p.dag.node}
        expected = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}
        self.assertEqual(ranks, expected)

    def test_rank_by_fifo_tree(self):
        p = self.dag.get_tree_pipeline()
        ranks = {task._uid: task._rank for task in p.dag.node}
        expected = {'A': None, 'B': None, 'C': None, 'D': None, 'E': None, 'F': None, 'G': None}
        self.assertEqual(ranks, expected)

    def test_rank_by_fifo_unbalanced_pipeline(self):
        p = self.dag.get_unbalanced_pipeline()
        ranks = {task._uid: task._rank for task in p.dag.node}
        expected = {'A': None, 'B': None, 'C': None, 'D': None, 'E': None, 'F': None, 'G': None}
        self.assertEqual(ranks, expected)

    def test_rank_by_fifo_ranktree_pipeline(self):
        p = self.dag.get_ranktree_pipeline()
        ranks = {task._uid: task._rank for task in p.dag.node}
        expected = {'A': None, 'B': None, 'C': None, 'D': None, 'E': None, 'F': None, 'G': None,
                    'H': None, 'I': None, 'J': None, 'K': None, 'L': None, 'M': None, 'N': None}
        self.assertEqual(ranks, expected)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRank)
    unittest.TextTestRunner(verbosity=2).run(suite)
