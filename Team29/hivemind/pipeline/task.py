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
        """Construct a task.

        :param uid: The unique identifier for this Task
        :type uid: string
        :param skip: Whether this Task should be skipped or not
        :type skip: bool
        :param shell: Does this Task need to be run using the shell
        :type shell: bool
        :param exe: The name of the executable
        :type exe: string
        :param verify_exe: The name of the verification executable
        :type verify_exe: string
        :param wd: The working directory to run the executable in
        :type wd: string
        :param *args: The list of parameters needed to the run the executable
        :type *args: iterable of strings
        """
        self.skip = skip
        self.shell = shell
        self.cmd = [exe]
        self.cmd.extend(args)
        self.verify_exe = verify_exe
        self.wd = wd

        self._uid = uid
        self._dry_run = False
        self._pid = None
        self._rank = None
        self._checkpoint_dir = None

    def run(self):
        """Run the executable associated with this Task."""
        if self._dry_run:
            print self
            return

        out = join(self._checkpoint_dir, str(self._pid), str(self._uid), "out.log")
        err = join(self._checkpoint_dir, str(self._pid), str(self._uid), "err.log")
        make_path(out)

        # Leaving this here in case we realize it was needed after all
        # for i, s in enumerate(self.cmd):
        #     self.cmd[i] = s.encode("iso-8859-1")

        with open(out, "ab") as stdout, open(err, "ab") as stderr:
            if self.shell:
                check_call(" ".join(self.cmd), shell=True, cwd=self.wd, stdout=stdout, stderr=stderr)
            else:
                check_call(self.cmd, cwd=self.wd, stdout=stdout, stderr=stderr)

            if self.verify_exe:
                if self.shell:
                    check_call(" ".join([self.verify_exe] + self.cmd), shell=True, cwd=self.wd, stdout=stdout, stderr=stderr)
                else:
                    check_call([self.verify_exe] + self.cmd, cwd=self.wd, stdout=stdout, stderr=stderr)

    def __str__(self):
        """Helps with printing.

        :returns: The string representation of this Task
        :rtype: {string}
        """
        return " ".join(self.cmd)

    def __repr__(self):
        """Also helps with printing.

        :returns: Another string representation of this Task
        :rtype: {string}
        """
        return "{} {} {}".format(self._uid, self._pid, self._rank)

    def __hash__(self):
        """Hash this Task based on it's UID.

        The UID field should never be changed otherwise it will break how the pipelines work.

        :returns: the hash of this Task
        :rtype: {int}
        """
        return hash(self._uid)

    def __eq__(self, other):
        """Determine if this Task is equal to the other Task based on all fields in the Task.

        :param other: The other Task to compare this Task to
        :type other: Task
        :returns: Whether the two Tasks are equal to each other
        :rtype: {bool}
        """
        return self._uid == other._uid and \
            self._pid == other._pid and \
            self._rank == other._rank and \
            self.skip == other.skip and \
            self.shell == other.shell and \
            self.verify_exe == other.verify_exe and \
            self.wd == other.wd and \
            self._checkpoint_dir == other._checkpoint_dir and \
            self._dry_run == other._dry_run and \
            self.cmd == other.cmd

    def __lt__(self, other):
        """Determine if this Task is less than another Task.

        Tasks that are less than another Task are considered to be of higher priority.
        Thus the Task with the greater rank is considered smaller.

        :param other: The other Task to compare this Task to
        :type other: Task
        :returns: Whether this Task is smaller than the other one
        :rtype: {bool}
        """
        return self._rank > other._rank  # This is not a mistake
