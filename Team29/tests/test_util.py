import unittest

import hivemind.util as utl
import os.path as path
import shutil as rm


class TestUtil(unittest.TestCase):

    def test_json_to_tasks_uid_task(self):
        tasks = utl.json_to_tasks("utilTest.json")
        ts = {task._uid: task.cmd for task, _ in tasks}
        expected = {'A': ['/bin/task-1', "arg-1", "/$$arg$$"],
                    'B': ['/bin/task-2', "arg-1", "arg-2", "/$$arg$$"],
                    'C': ['/bin/task-3'],
                    'D': ['/bin/task-4', "arg-1", "arg-2", "/$$arg$$"]}
        self.assertEqual(ts, expected)

    def test_json_to_tasks_uid_wd(self):
        tasks = utl.json_to_tasks("utilTest.json")
        wds = {task._uid: task.wd for task, _ in tasks}
        expected = {'A': '/wd-A', 'B': '/wd-B', 'C': '/wd-C', 'D': '/wd-D'}
        self.assertEqual(wds, expected)

    def test_json_to_tasks_uid_require(self):
        tasks = utl.json_to_tasks("utilTest.json")
        reqs = {task._uid: req for task, req in tasks}
        expected = {'A': [], 'B': ['A'], 'C': ['B'], 'D': ['C']}
        self.assertEqual(reqs, expected)

    def test_read_csv(self):
        p = utl.read_csv("csvTest1.csv")
        pats = {pat['$$name$$']: pat['$$file$$'] for pat in p}
        expected = {'Hussein': 'hussein.txt', 'Mo': 'mo.txt', 'Sarah': 'sarah.txt'}
        self.assertEqual(pats, expected)

    def test_read_csv_single_col(self):
        p = utl.read_csv("csvTest2.csv")
        pats = [pat['$$name$$'] for pat in p]
        expected = ['Hussein', 'Mo', 'Sarah']
        self.assertEqual(pats, expected)

    def test_make_path(self):
        utl.make_path("./temp/temp2/temp3/")
        expected = "./temp/temp2/temp3"
        self.assertTrue(path.exists(expected))
        rm.rmtree("./temp")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtil)
    unittest.TextTestRunner(verbosity=2).run(suite)
