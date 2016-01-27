#!/usr/bin/env python
# encoding: utf-8

from subprocess import call


class Task(object):
    def __init__(self, exe_path, exe, *args):
        self.exe_path = exe_path
        self.exe = "./" + exe
        self.args = list(args)
        self.next = None

    def run(self):
        call([self.exe] + self.args, cwd=self.exe_path)
        return self.next

    def link(self, next):
        self.next = next
