#!/usr/bin/env python
# encoding: utf-8

from util import tags

class Master(object):

	def __init__(self, mpi, queue):
		self.queue = queue
		self.sent_tasks = 0
		self.completed_tasks = 0
		self.mpi = mpi
        self.name = mpi.Get_processor_name()
        self.comm = mpi.COMM_WORLD
        self.status = mpi.Status()
        self.receive()

   	def send(self, target, task, tag):
   		self.comm.send(task, dest=target, tag=tag)

   	def receive(self):
   		task = self.comm.recv(source=self.mpi.ANY_SOURCE, tag=self.mpi.ANY_TAG, status=self.status)
   		self.queue.push(task)
   		source = self.status.Get_source()
        tag = self.status.Get_tag()
        if tag == tags.DONE:
   			self.completed_tasks += 1
        elif tag == tags.READY:
        	if self.queue:
        		self.send(source, self.queue.pop(), tags.START)
        		self.sent_tasks += 1
        	elif self.sent_tasks == self.queue.num_tasks:
        		self.send(source, None, tags.EXIT)
            else:
                self.send(source, None, tags.WAIT)
