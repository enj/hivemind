#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""MPI Master and Worker tests."""

import unittest

from hivemind.util import json_to_tasks, read_csv
from hivemind.mpi import Master, Worker

from fake_mpi import FakeMPIWorld


class TestMPISingleWorker(unittest.TestCase):
    """Sequential tests with single Master and Worker."""

    def setUp(self):
        """Create Master, Worker and load data."""
        tasks = json_to_tasks("mpi.json")  # 6 linear tasks
        patients = read_csv("mpi.csv")  # 7 patients
        self.world = FakeMPIWorld(2)
        self.master = Master(self.world[0], tasks, patients)
        self.worker = Worker(self.world[1])

    def test_start_state(self):
        """Test Master's initial state."""
        self.assertEqual(len(self.master.concrete_pipelines), 7)
        self.assertEqual(self.master.concrete_pipelines[0].pid, 0)
        self.assertEqual(self.master.concrete_pipelines[-1].pid, 6)
        self.assertEqual(self.master.sent_tasks, 0)
        self.assertEqual(self.master.closed_workers, 0)
        self.assertEqual(self.master.total_workers, 1)
        self.assertEqual(self.master.workers.qsize(), 1)
        self.assertEqual(self.master.num_tasks, 42)
        self.assertEqual(self.master.queue.qsize(), 7)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMPISingleWorker)
    unittest.TextTestRunner(verbosity=2).run(suite)
