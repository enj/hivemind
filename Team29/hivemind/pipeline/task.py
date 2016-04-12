#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents a Task in a pipeline."""

from subprocess import check_call
from functools import total_ordering

from ..util import make_path, join


@total_ordering
class Task(object):
    """A Task is the smallest unit of work in a pipeline."""

    def __init__(self, uid, skip, shell, exe, verify_exe, wd, *args):
        """Construct a task based on the given path, executable, and arguments.

        :param exe_path: The file system location of the executable
        :type exe_path: string
        :param exe: The name of the executable
        :type exe: string
        :param *args: The list of parameters needed to the run the executable
        :type *args: iterable of strings
        """
        self.skip = skip
        self.shell = shell
        self.cmd = [exe]
        self.cmd.extend(args)
        self.verify_exe = verify_exe
        self.wd = wd
        self.dryrun = False

        self._uid = uid
        self._pid = None
        self._rank = None
        self._checkpoint_dir = None

    def run(self):
        """Run the executable associated with this Task."""

        if self.dryrun:
            print ' '.join(self.cmd)
            return

        out = join(self._checkpoint_dir, str(self._pid), str(self._uid), "out.log")
        err = join(self._checkpoint_dir, str(self._pid), str(self._uid), "err.log")
        make_path(out)

        # Leaving this here in case we realize it was needed after all
        # for i, s in enumerate(self.cmd):
        #     self.cmd[i] = s.encode('iso-8859-1')

        with open(out, 'a') as stdout, open(err, 'a') as stderr:
            if self.shell:
                check_call(' '.join(self.cmd), shell=True, cwd=self.wd, stdout=stdout, stderr=stderr)
            else:
                check_call(self.cmd, cwd=self.wd, stdout=stdout, stderr=stderr)

            if self.verify_exe:
                if self.shell:
                    check_call(' '.join([self.verify_exe] + self.cmd), shell=True, cwd=self.wd, stdout=stdout, stderr=stderr)
                else:
                    check_call([self.verify_exe] + self.cmd, cwd=self.wd, stdout=stdout, stderr=stderr)

    def __str__(self):
        return ' '.join(self.cmd)

    def __repr__(self):
        return "{} {} {}".format(self._uid, self._pid, self._rank)

    def __hash__(self):
        return hash(self._uid)

    def __eq__(self, other):
        return self._uid == other._uid and \
            self._pid == other._pid and \
            self._rank == other._rank and \
            self.skip == other.skip and \
            self.shell == other.shell and \
            self.verify_exe == other.verify_exe and \
            self.wd == other.wd and \
            self._checkpoint_dir == other._checkpoint_dir and \
            self.cmd == other.cmd

    def __lt__(self, other):
        return self._rank > other._rank
