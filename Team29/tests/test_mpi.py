#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""MPI Master and Worker tests."""

import unittest
from threading import Thread

from hivemind.util import json_to_tasks, read_csv, tags
from hivemind.mpi import Master, Worker
from hivemind.pipeline import rank_by_successors

from fake_mpi import FakeMPIWorld


class TestMPISingleWorker(unittest.TestCase):
    """Sequential tests with single Master and Worker."""

    def setUp(self):
        """Create Master, Worker and load data."""
        tasks = json_to_tasks("mpi.json")  # 6 linear tasks
        patients = read_csv("mpi.csv")  # 7 patients
        self.world = FakeMPIWorld(2)
        self.master = Master(self.world[0], tasks, patients, rank_by_successors)
        self.worker = Worker(self.world[1])

    def test_start_state(self):
        """Test Master/Worker's initial state."""
        self.assertEqual(len(self.master.concrete_pipelines), 7)
        self.assertEqual(self.master.concrete_pipelines[0].pid, 0)
        self.assertEqual(self.master.concrete_pipelines[-1].pid, 6)
        self.assertEqual(self.master.sent_tasks, 0)
        self.assertEqual(self.master.closed_workers, 0)
        self.assertEqual(self.master.total_workers, 1)
        self.assertEqual(self.master.workers.qsize(), 1)
        self.assertEqual(self.master.num_tasks, 42)
        self.assertEqual(self.master.queue.qsize(), 7)
        self.assertEqual(self.master.out_tasks, {})

        for p in self.master.concrete_pipelines:
            for task in p.dag.nodes_iter():
                self.assertFalse(p.is_done(task))

        self.assertEqual(self.worker.tag, tags.WORK)

    def test_loop(self):
        """Test loop and end state using multiple threads."""
        master_loop = Thread(target=self.master.loop)
        worker_loop = Thread(target=self.worker.loop)
        master_loop.start()
        worker_loop.start()
        worker_loop.join()
        master_loop.join()

        self.assertEqual(len(self.master.concrete_pipelines), 7)
        self.assertEqual(self.master.concrete_pipelines[0].pid, 0)
        self.assertEqual(self.master.concrete_pipelines[-1].pid, 6)
        self.assertEqual(self.master.sent_tasks, 42)
        self.assertEqual(self.master.closed_workers, 1)
        self.assertEqual(self.master.total_workers, 1)
        self.assertEqual(self.master.workers.qsize(), 0)
        self.assertEqual(self.master.num_tasks, 42)
        self.assertEqual(self.master.queue.qsize(), 0)
        self.assertEqual(self.master.out_tasks, {})

        for p in self.master.concrete_pipelines:
            for task in p.dag.nodes_iter():
                self.assertTrue(p.is_done(task))

        self.assertEqual(self.worker.tag, tags.EXIT)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMPISingleWorker)
    unittest.TextTestRunner(verbosity=2).run(suite)
