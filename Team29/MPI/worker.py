#!/usr/bin/env python
# encoding: utf-8

from time import sleep

from util import tags, MASTER


class Worker(object):

    SLEEP_TIME = 10

    def __init__(self, mpi):
        self.mpi = mpi
        self.name = mpi.Get_processor_name()
        self.comm = mpi.COMM_WORLD
        self.rank = self.comm.rank
        self.status = mpi.Status()
        self.tag = tags.READY
        print "I am worker", self.rank
        self.send(None)
        self.receive()

    def send(self, task):
        self.comm.send(task, dest=MASTER, tag=self.tag)

    def receive(self):
        self.task = self.comm.recv(source=MASTER, tag=self.mpi.ANY_TAG, status=self.status)
        self.tag = self.status.Get_tag()
        if self.tag == tags.START:
            print "STARTing"
            self.run()
        #elif self.tag == tags.EXIT:
        #    self.send(None)
        elif self.tag == tags.WAIT:
            print "WAITing"
            sleep(self.SLEEP_TIME)
            self.tag = tags.READY

    def run(self):
        self.task.run()
        self.tag = tags.DONE
        self.send(self.task.next)
        self.tag = tags.READY
