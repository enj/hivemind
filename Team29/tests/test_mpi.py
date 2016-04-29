#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""MPI Master and Worker tests."""

import unittest
from threading import Thread

from hivemind.util import json_to_tasks, read_csv, tags, join
from hivemind.mpi import Master, Worker
from hivemind.pipeline import rank_by_successors

from fake_mpi import FakeMPIWorld


def get_file(checkpoint_dir, pid, uid):
    """Get contents of stdout file."""
    out = join(checkpoint_dir, str(pid), str(uid), "out.log")
    with open(out, "rb") as f:
        return f.read()


class TestMPISingleWorker(unittest.TestCase):
    """Sequential tests with single Master and Worker."""

    def setUp(self):
        """Create Master, Worker and load data."""
        self.tasks = json_to_tasks("mpi.json")  # 6 linear tasks
        patients = read_csv("mpi.csv")  # 7 patients
        self.world = FakeMPIWorld(2)
        self.master = Master(self.world[0], self.tasks, patients, rank_by_successors)
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
        """Test loop and end state using multiple threads / single Worker."""
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

        for pid in xrange(7):
            for task, _ in self.tasks:
                if task._uid == "A6":
                    with self.assertRaisesRegexp(IOError, "^\[Errno 2\] No such file or directory"):
                        get_file(self.master.checkpoint_dir, pid, task._uid)
                else:
                    self.assertEqual(get_file(self.master.checkpoint_dir, pid, task._uid), task._uid + "\n")


class TestMPIMultipleWorker(unittest.TestCase):
    """Sequential tests with single Master and multiple Workers."""

    def setUp(self):
        """Create Master, all Workers and load data."""
        self.tasks = json_to_tasks("mpi.json")  # 6 linear tasks
        patients = read_csv("mpi.csv")  # 7 patients
        self.world = FakeMPIWorld(4)
        self.master = Master(self.world[0], self.tasks, patients, rank_by_successors)
        self.worker1 = Worker(self.world[1])
        self.worker2 = Worker(self.world[2])
        self.worker3 = Worker(self.world[3])

    def test_start_state(self):
        """Test Master / all Workers' initial state."""
        self.assertEqual(len(self.master.concrete_pipelines), 7)
        self.assertEqual(self.master.concrete_pipelines[0].pid, 0)
        self.assertEqual(self.master.concrete_pipelines[-1].pid, 6)
        self.assertEqual(self.master.sent_tasks, 0)
        self.assertEqual(self.master.closed_workers, 0)
        self.assertEqual(self.master.total_workers, 3)
        self.assertEqual(self.master.workers.qsize(), 3)
        self.assertEqual(self.master.num_tasks, 42)
        self.assertEqual(self.master.queue.qsize(), 7)
        self.assertEqual(self.master.out_tasks, {})

        for p in self.master.concrete_pipelines:
            for task in p.dag.nodes_iter():
                self.assertFalse(p.is_done(task))

        self.assertEqual(self.worker1.tag, tags.WORK)
        self.assertEqual(self.worker2.tag, tags.WORK)
        self.assertEqual(self.worker3.tag, tags.WORK)

    def test_loop(self):
        """Test loop and end state using multiple threads / multiple Workers."""
        master_loop = Thread(target=self.master.loop)
        worker_loop1 = Thread(target=self.worker1.loop)
        worker_loop2 = Thread(target=self.worker2.loop)
        worker_loop3 = Thread(target=self.worker3.loop)
        master_loop.start()
        worker_loop1.start()
        worker_loop2.start()
        worker_loop3.start()
        worker_loop1.join()
        worker_loop2.join()
        worker_loop3.join()
        master_loop.join()

        self.assertEqual(len(self.master.concrete_pipelines), 7)
        self.assertEqual(self.master.concrete_pipelines[0].pid, 0)
        self.assertEqual(self.master.concrete_pipelines[-1].pid, 6)
        self.assertEqual(self.master.sent_tasks, 42)
        self.assertEqual(self.master.closed_workers, 3)
        self.assertEqual(self.master.total_workers, 3)
        self.assertEqual(self.master.workers.qsize(), 0)
        self.assertEqual(self.master.num_tasks, 42)
        self.assertEqual(self.master.queue.qsize(), 0)
        self.assertEqual(self.master.out_tasks, {})

        for p in self.master.concrete_pipelines:
            for task in p.dag.nodes_iter():
                self.assertTrue(p.is_done(task))

        self.assertEqual(self.worker1.tag, tags.EXIT)
        self.assertEqual(self.worker2.tag, tags.EXIT)
        self.assertEqual(self.worker3.tag, tags.EXIT)

        for pid in xrange(7):
            for task, _ in self.tasks:
                if task._uid == "A6":
                    with self.assertRaisesRegexp(IOError, "^\[Errno 2\] No such file or directory"):
                        get_file(self.master.checkpoint_dir, pid, task._uid)
                else:
                    self.assertEqual(get_file(self.master.checkpoint_dir, pid, task._uid), task._uid + "\n")


class TestMPIDryRun(unittest.TestCase):
    """Dry run tests using MPI."""

    def setUp(self):
        """Create Master, Worker and load data for dry run."""
        self.tasks = json_to_tasks("mpi.json")  # 6 linear tasks
        for t, _ in self.tasks:
            t._dry_run = True
        patients = read_csv("mpi.csv")  # 7 patients
        self.world = FakeMPIWorld(2)
        self.master = Master(self.world[0], self.tasks, patients, rank_by_successors, dry_run=True)
        self.worker = Worker(self.world[1])

    def test_loop_dry(self):
        """Test loop with dry run."""
        master_loop = Thread(target=self.master.loop)
        worker_loop = Thread(target=self.worker.loop)
        master_loop.start()
        worker_loop.start()
        worker_loop.join()
        master_loop.join()

        for pid in xrange(7):
            for task, _ in self.tasks:
                with self.assertRaisesRegexp(IOError, "^\[Errno 2\] No such file or directory"):
                    get_file(self.master.checkpoint_dir, pid, task._uid)


if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestMPISingleWorker)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(TestMPIMultipleWorker)
    suite3 = unittest.TestLoader().loadTestsFromTestCase(TestMPIDryRun)
    suite = unittest.TestSuite([suite1, suite2, suite3])
    unittest.TextTestRunner(verbosity=2).run(suite)
