import unittest
import networkx as nx

from hivemind.pipeline import PipelineFramework, ConcretePipeline, Task, rank_by_fifo as rank
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

    def test_replace_none(self):
        data = self.dg.get_args()
        p = PipelineFramework([(Task("A", False, "path", "exe", "none", "are", "replaced"), [])])
        cp = ConcretePipeline(0, p, data, "blah")
        rank(cp)
        task = cp.dag.nodes()[0]
        self.assertEquals(str(task), "./exe none are replaced")
        self.assertEquals(task.exe_path, "path")
        self.assertFalse(task.skip)

    def test_replace_simple(self):
        data = self.dg.get_args()
        p = PipelineFramework([(Task("B", "$$skip1$$", "path", "exe", "-blah", "$$a1$$"), [])])
        cp = ConcretePipeline(0, p, data, "blah")
        rank(cp)
        task = cp.dag.nodes()[0]
        self.assertEquals(str(task), "./exe -blah val_for_a1")
        self.assertEquals(task.exe_path, "path")
        self.assertTrue(task.skip)

    def test_replace_multiple(self):
        data = self.dg.get_args()
        p = PipelineFramework([(Task("C", "$$skip2$$", "$$a1$$", "$$a2$$", "$$a3$$", "$$a4$$"), [])])
        cp = ConcretePipeline(0, p, data, "blah")
        rank(cp)
        task = cp.dag.nodes()[0]
        self.assertEquals(str(task), "./secondParameter a_3rd_one 4")
        self.assertEquals(task.exe_path, "val_for_a1")
        self.assertTrue(task.skip)

    def test_replace_repeated(self):
        data = self.dg.get_args()
        p = PipelineFramework([(Task("D", "$$skip3$$", "$$a1$$", "$$a1$$", "$$a1$$", "$$a1$$"), [])])
        cp = ConcretePipeline(0, p, data, "blah")
        rank(cp)
        task = cp.dag.nodes()[0]
        self.assertEquals(str(task), "./val_for_a1 val_for_a1 val_for_a1")
        self.assertEquals(task.exe_path, "val_for_a1")
        self.assertTrue(task.skip)

    def test_replace_partial(self):
        data = self.dg.get_args()
        p = PipelineFramework([(Task("E", "$$skip4$$", "$$a4$$a4$$", "$$a1$$"), [])])
        with self.assertRaises(Exception):
            ConcretePipeline(0, p, data, "blah")

    def test_replace_back_to_back(self):
        data = self.dg.get_args()
        p = PipelineFramework([(Task("F", "$$skip5$$", "$$a2$$", "$$a4$$$$a4$$"), [])])
        cp = ConcretePipeline(0, p, data, "blah")
        rank(cp)
        task = cp.dag.nodes()[0]
        self.assertEquals(str(task), "./44")
        self.assertEquals(task.exe_path, "secondParameter")
        self.assertFalse(task.skip)

    def test_replace_substring(self):
        data = self.dg.get_args()
        p = PipelineFramework([(Task("G", "$$skip6$$", "/path/$$a2$$/more", "exe", "-$$a3$$", "\"$$a4$$\""), [])])
        cp = ConcretePipeline(0, p, data, "blah")
        rank(cp)
        task = cp.dag.nodes()[0]
        self.assertEquals(str(task), "./exe -a_3rd_one \"4\"")
        self.assertEquals(task.exe_path, "/path/secondParameter/more")
        self.assertFalse(task.skip)

    def test_replace_unicode(self):
        data = self.dg.get_args()
        p = PipelineFramework([(Task("G", False, u"/path/$$a2$$/more", u"exe", u"-$$a3$$", u"\"$$a4$$\""), [])])
        cp = ConcretePipeline(0, p, data, "blah")
        rank(cp)
        task = cp.dag.nodes()[0]
        self.assertEquals(str(task), "./exe -a_3rd_one \"4\"")
        self.assertEquals(task.exe_path, "/path/secondParameter/more")
        self.assertFalse(task.skip)

    def test_replace_invalid_var(self):
        data = self.dg.get_args()
        p = PipelineFramework([(Task("G", "$$skip6$$", "/path/$$a2$$/more", "exe", "-$$a3$$", "$$a5$$"), [])])
        with self.assertRaises(Exception):
            ConcretePipeline(0, p, data, "blah")

    def test_replace_invalid_type(self):
        data = self.dg.get_args()
        p = PipelineFramework([(Task("G", "$$skip6$$", None, "exe", "-$$a3$$", "$$a4$$"), [])])
        with self.assertRaises(Exception):
            ConcretePipeline(0, p, data, "blah")

    def test_done(self):
        data = self.dg.get_args()
        p = self.dg.get_dag_pipeline()
        cp = ConcretePipeline(0, p, data, "blah")
        ready = list(cp.get_ready_tasks())
        self.assertEquals(len(ready), 2)
        task = [t for t in ready if t._uid is "A"][0]

        self.assertFalse(list(cp.get_ready_successors(task)))
        self.assertFalse(cp.is_done(task))
        cp.set_done(task)
        self.assertTrue(cp.is_done(task))
        self.assertEquals(list(cp.get_ready_successors(task))[0]._uid, "C")
        self.assertEquals(cp.get_completed_tasks(), 1)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPipeline)
    unittest.TextTestRunner(verbosity=2).run(suite)
    #unittest.main()
