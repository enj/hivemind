#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents a Task in a pipeline."""

from subprocess import call


class Task(object):
    """A Task is the smallest unit of work in a pipeline."""

    def __init__(self, exe_path, exe, *args):
        """Construct a task based on the given path, executable, and arguments.

        :param exe_path: The file system location of the executable
        :type exe_path: string
        :param exe: The name of the executable
        :type exe: string
        :param args: The list of parameters needed to the run the executable
        :type args: iterable of strings
        """
        self.exe_path = exe_path
        self.exe = "./" + exe
        self.args = list(args)
        self.next = None

    def run(self):
        """TODO."""
        call([self.exe] + self.args, cwd=self.exe_path)

    def link(self, next):
        """TODO."""
        self.next = next
