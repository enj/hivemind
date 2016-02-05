#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents a Task in a pipeline."""

from subprocess import call


class Task(object):
    """A Task is the smallest unit of work in a pipeline."""

    def __init__(self, uid, skip, requires, exe_path, exe, *args):
        """Construct a task based on the given path, executable, and arguments.

        :param exe_path: The file system location of the executable
        :type exe_path: string
        :param exe: The name of the executable
        :type exe: string
        :param *args: The list of parameters needed to the run the executable
        :type *args: iterable of strings
        """
        self.uid = uid
        self.skip = skip
        self.requires = requires
        self.exe_path = exe_path
        self.cmd = ["./" + exe]
        self.cmd.extend(args)
        self.pid = None

    def run(self):
        """Run the executable associated with this Task."""
        call(self.cmd, cwd=self.exe_path)

    def __str__(self):
        return ' '.join(self.cmd)

    def __hash__(self):
        return hash((
                    self.uid,
                    self.skip,
                    tuple(self.requires),
                    self.exe_path,
                    tuple(self.cmd),
                    self.pid
                    ))

    def __eq__(self, other):
        return self.uid == other.uid and self.pid == other.pid and hash(self) == hash(other)

    def __ne__(self, other):
        return not self.__eq__(other)
