#!/usr/bin/env python
# -*- coding: utf-8 -*-


from argparse import ArgumentParser
import os.path
from subprocess import check_call

parser = ArgumentParser(description="Wrapper for DNA Merge Lanes")

parser.add_argument('-e', '--exe', action='append', help="Path to exe", required=True)
parser.add_argument('-T', help="Tool", required=True)
parser.add_argument('-R', help="-R file", required=True)
parser.add_argument('-I', action='append', help="Input BAM file", required=True)
parser.add_argument('--read_filter', help="Read Filter", required=True)
parser.add_argument('-o', help="Output file", required=True)
args = parser.parse_args()

cmd = args.exe
cmd.extend(['-T', args.T])
cmd.extend(['-R', args.R])

for i in xrange(len(args.I)):
    if os.path.isfile(args.I[i]):
        cmd.extend(['-I', args.I[i]])

cmd.extend(['--read_filter', args.read_filter])
cmd.extend(['-o', args.o])

#print ' '.join(cmd)
check_call(' '.join(cmd), shell=True)
