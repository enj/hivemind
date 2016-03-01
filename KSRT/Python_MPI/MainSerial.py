
#!/usr/bin/env python
import os
import datetime
import string
import subprocess
import sys
import shutil
import time
import csv
import numpy
import foobar as msmpi4py
if len(sys.argv)>1:
	arg1 = sys.argv[1]
else:
	arg1 = 'NAUGHT_Y_MATH_EXPR_LOL'


today = datetime.date.today()
t = datetime.time(1, 2, 3)
list_time = [str(today.year), str(today.month), str(today.day), str(t.hour), str(t.minute), str(t.second)]
string_time = '_' + '_'.join(list_time)
subprocess.call(['~/.ksrt_profile'], shell=True)
SetSubmitPreprocessTasks = set()
list_row = msmpi4py.ksrtLoadTrainerData(os.environ['trainingFILE'])
for row in list_row[1:4]:
	SetSubmitPreprocessTasks.add( \
		msmpi4py.ksrtSubmitPreprocessSerialTask(row[0], row[1]))
SubmitPreprocessParallelJob = \
	msmpi4py.ParallelJob(SetSubmitPreprocessTasks)
while SetSubmitPreprocessTasks:
	SerialTask = SetSubmitPreprocessTasks.pop()
	SerialTask.ExecuteSerialTask()
	# SubmitPreprocessParallelJob.CompletedSerialTasksMPI4PY.add(RecvCurrentJob)
