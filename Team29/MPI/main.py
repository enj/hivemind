#!/usr/bin/env python
# encoding: utf-8

from task import Task
from pipeline import Pipeline

a = Task("/Users/srbaucom/Documents1", "a.out")
b = Task("/Users/srbaucom/Documents2", "a.out")
c = Task("/Users/srbaucom/Documents3", "a.out")
p = Pipeline(a, b, c)
