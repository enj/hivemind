#!/usr/bin/env python
# encoding: utf-8

from util import tags, MASTER


class Worker(object):
    def __init__(self, mpi):
        self.mpi = mpi
        self.name = mpi.Get_processor_name()
        self.comm = mpi.COMM_WORLD
        self.rank = self.comm.rank
        self.status = mpi.Status()
        self.tag = tags.READY
        self.send(None)
        self.receive()

    def send(self, message):
        self.comm.send(message, dest=MASTER, tag=self.tag)

    def receive(self):
        self.task = self.comm.recv(source=MASTER, tag=self.mpi.ANY_TAG, status=self.status)
        self.tag = self.status.Get_tag()
        if self.tag == tags.START:
            self.run()
        elif self.tag == tags.EXIT:
            self.send(None)

    def run(self):
        self.task.run()
        self.tag = tags.DONE
        self.send(self.task.next)
        self.tag = tags.READY
        #self.receive() #Move this to the master in a loop
