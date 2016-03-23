#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Code for faking MPI's interface (adapter pattern)."""


class FakeMPIWorld(object):

    def __init__(self, size):

        class FakeMPI(object):

            ANY_TAG = -1
            ANY_SOURCE = -2

            def __init__(self, rank, network):

                class FakeCOMM(object):

                    def __init__(self, rank, network):

                        class FakeStatus(object):

                            def __init__(self, source=None, tag=None):
                                self.source = source
                                self.tag = tag

                            def Get_source(self):
                                return self.source

                            def Get_tag(self):
                                return self.tag

                        self.network = network
                        self.rank = rank
                        self.fake_status = FakeStatus

                    def Get_size(self):
                        return len(self.network.data)

                    def Get_rank(self):
                        return self.rank

                    def send(self, obj, dest, tag=0):
                        q = self.network.data[dest]
                        q.put((obj, self.fake_status(self.rank, tag)))

                    def recv(self, buf=None, source=0, tag=0, status=None):
                        q = self.network.data[self.rank]
                        m, s = q.get()
                        if status:
                            status.source = s.source
                            status.tag = s.tag
                        return m

                self.COMM_WORLD = FakeCOMM(rank, network)
                self.name = "{} {}".format(__name__, rank)

            def Status(self):
                return self.COMM_WORLD.fake_status()

            def Get_processor_name(self):
                return self.name

        class FakeNetwork(object):

            def __init__(self, size):
                from Queue import Queue
                self.data = tuple(Queue(maxsize=1) for _ in xrange(size))

        network = FakeNetwork(size)
        self.array = [FakeMPI(rank, network) for rank in xrange(size)]

    def __getitem__(self, rank):
        return self.array[rank]
