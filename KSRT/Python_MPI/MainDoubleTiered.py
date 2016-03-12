
#!/usr/bin/env python
from mpi4py import MPI
import os
import datetime
import string
import subprocess
import sys
import shutil
import time
import csv
import numpy
import copy
# import ksrtSubmitPreprocssPipeline as msmpi4py

def ksrtLoadTrainerData(filename):
	list_row = []
	list_row_TEMP = []
	with open(filename, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ')
		for row in spamreader:
			list_row.append(row)
	return list_row

class SerialTask:
	def __init__(self, InputString):
		# SerialTask.__init__(self)
		StringListTemp = InputString.split(' ')
		self.env_dict = {}
		self.env_dict['ID'] = StringListTemp[0]
		self.env_dict['FLIP'] = StringListTemp[1]
	def Execute(self):
		print "hallo there ID=%s of FLIP=%s!" % (self.env_dict['ID'], self.env_dict['FLIP'])
		return True
if len(sys.argv)>1:
	arg1 = sys.argv[1]
else:
	arg1 = 'NAUGHT_Y_MATH_EXPR_LOL'
# Define weighted average methodology
def CurrentTimeStamp():
	return time.time()
def ExpMovingAverage(CurrentValue, PrevAverage = 0, Alpha = 0.3):
	if PrevAverage==0:
		CurrentAverage = CurrentValue
	else:
		CurrentAverage = CurrentValue*Alpha + PrevAverage*(1 - Alpha)
	return CurrentAverage

# Define MPI message tags
# {'READY' : 0, 'DONE' : 1, 'EXIT' : 2, 'START' : 3, 'ERROR' : 4}
IntJobMultiplier = 3
list_MPI_TAG = [ \
	'READY', 'DONE', 'EXIT', 'START', 'ERROR', \
	'CONTINUE', 'MORE', 'STARTUP', 'SHUTDOWN', 'CLOSE', 'REPORT' ]
dict_MPI_TAG = {}
IndexCurrent = 0
for current_MPI_TAG in list_MPI_TAG:
	dict_MPI_TAG[current_MPI_TAG] = IndexCurrent
	IndexCurrent += 1
reverse_dict_MPI_TAG = {}
for current_MPI_TAG in list_MPI_TAG:
	reverse_dict_MPI_TAG[dict_MPI_TAG[current_MPI_TAG]] = current_MPI_TAG
# Initializations and preliminaries
comm = MPI.COMM_WORLD   # get MPI communicator object
size = comm.size        # total number of processes
rank = comm.rank        # rank of this process
status = MPI.Status()   # get MPI status object
Head_status = MPI.Status()   # get MPI status object
name = MPI.Get_processor_name()
SubMasterCount = 4
# class ConstantTierCommand(RankingList=[[0],range[1,4],range[5,size]]):
	# def __init__(self, InputString):
		# self.CommandStructureRecursive = []
		
		# self.env_dict = {}
		# self.env_dict['ID'] = StringListTemp[0]
		# self.env_dict['FLIP'] = StringListTemp[1]

	# def RecursiveSetUp(InputRankingList, CommandStructureRecursive):
		# []
		# RecursiveSetUp()
# Establish local master ID
# Establish dict for starting subset workers
SubMasterRange = range(1, SubMasterCount + 1)
WorkerRange = range(SubMasterCount + 1, size)
ListFlatTree = [[0], SubMasterRange, WorkerRange]
# This should be fine if I make it recursive but I am going for simple at the moment
def ReturnSubList(InputListBranchedTree, InputValue):
	for Index in InputListBranchedTree[1]:
		if Index[0] == InputValue:
			return Index[1]
	return []
# def static_num() :
   # global x
   # x=x+1
   # return x
# for i in range(0,10) :
     # print static_num
var_OUTPUT_CALLS = 0
def RecvLog(FileLogFstreamInput, InputRank, InputComm, RecvSource=MPI.ANY_SOURCE):
	LocalStatus = MPI.Status()
	RecvValue = InputComm.recv(source=RecvSource, tag=MPI.ANY_TAG, status=LocalStatus)
	RecvSource = LocalStatus.Get_source()
	RecvTag = LocalStatus.Get_tag()
	global var_OUTPUT_CALLS
	var_OUTPUT_CALLS = var_OUTPUT_CALLS + 1
	if var_OUTPUT_CALLS<1000:
		FileLogFstreamInput.write('\nTIME=%.17f\tRECV: rank=%s tag=%s source=%s' % (CurrentTimeStamp(), str(InputRank), reverse_dict_MPI_TAG[RecvTag], str(RecvSource)))
		FileLogFstreamInput.write('\n\tDATA_RECV=%s' % str(RecvValue))
	if rank in WorkerRange:
		print '\nTIME=%.17f\tRECV: rank=%s tag=%s source=%s' % (CurrentTimeStamp(), str(InputRank), reverse_dict_MPI_TAG[RecvTag], str(RecvSource))
	return (RecvValue, RecvSource, RecvTag)
def SendLog(FileLogFstreamInput, InputComm, InputRank, DataToSend, InputTagString, InputDestination):
	InputComm.send(DataToSend, dest=InputDestination, tag=dict_MPI_TAG[InputTagString])
	global var_OUTPUT_CALLS
	var_OUTPUT_CALLS = var_OUTPUT_CALLS + 1
	if var_OUTPUT_CALLS<1000:
		FileLogFstreamInput.write('\nTIME=%.17f\tSEND: rank=%s tag=%s to dest=%s' % (CurrentTimeStamp(), str(rank), InputTagString, str(InputDestination)))
		FileLogFstreamInput.write('\n\tDATA_SENT=%s' % str(DataToSend))
	if rank in WorkerRange:
		print '\nTIME=%.17f\tSEND: rank=%s tag=%s to dest=%s' % (CurrentTimeStamp(), str(rank), InputTagString, str(InputDestination))
	return True
if rank == 0:
	role = 'HEADMASTER'
	LocalMaster = 0
	print 'rank=%s as master' % str(rank)
elif rank in ListFlatTree[1]:
	role = 'SUBMASTER'
	LocalMaster = rank
	print 'rank=%s as submaster with master=0' % str(rank)
elif rank in ListFlatTree[2]:
	role = 'WORKER'
	LocalMaster = ListFlatTree[1][rank%len(ListFlatTree[1])]
	print 'rank=%s worker for submaster=%s ' % (str(rank), str(LocalMaster))
DebugFlag = False
FileLogName = '_'.join(['LOG', role, str(rank), name])
FileLogFstream = open(FileLogName, 'w')
ListBranchedTree = [0,[]]
for Index in ListFlatTree[1]:
	ListBranchedTree[1].append([Index,[]])		
for Index in WorkerRange:
	IndexForLocalMaster = ListFlatTree[1][Index%len(ListFlatTree[1])]
	for SubIndex in ListBranchedTree[1]:
		if SubIndex[0] == IndexForLocalMaster:
			SubIndex[1].append(Index)
# START CODE FOR STATIC HEADMASTER
if rank == 0:
	SubMasterNodeList = []
	SubMasterNodeList.extend(ListFlatTree[1])
	WorkerNodeList = []
	WorkerNodeList.extend(ListFlatTree[2])
	DictActiveJobs = {}
	subprocess.call(['~/.ksrt_profile'], shell=True)
	list_row = ksrtLoadTrainerData(os.environ['trainingFILE'])
	ListSerialTaskStrings = []
	ListDoneSerialTasks = []
	ListErrorSerialTasks = []
	for Index in range(100):
		for row in list_row:
			InputString = (' ' + str(Index)).join(row)
			ListSerialTaskStrings.append(InputString)
	# for row in list_row:
		# InputString = ' '.join(row)
		# ListSerialTaskStrings.append(InputString)
	StartCountSerialTasks = len(ListSerialTaskStrings)
	StartCountSerialTasks = len(ListSerialTaskStrings)
	StartTime = CurrentTimeStamp()
	ActiveJobs = []
	ClosedSubMaster = 0
	FinishedSerialTaskCount = 0
	while ClosedSubMaster<len(ListFlatTree[1]):
		(RecvValue, source, tag_recv) = RecvLog(FileLogFstream, rank, comm, MPI.ANY_SOURCE)
		#RecvValue = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
		#source = status.Get_source()
		#tag_recv = status.Get_tag()
		if tag_recv == dict_MPI_TAG['MORE']:
			if ListSerialTaskStrings:
				AssignedList = []
				IntJobPerNode = len(ReturnSubList(ListBranchedTree, source))
				AssignedNumberMax = IntJobMultiplier*IntJobPerNode
				AssignNumberFinal = min(AssignedNumberMax, len(ListSerialTaskStrings))
				while len(AssignedList)<AssignNumberFinal:
					AssignedList.append(ListSerialTaskStrings.pop())
				for Index in AssignedList:
					DictActiveJobs[Index] = source
				SendLog(FileLogFstream, comm, rank, AssignedList, 'CONTINUE', source)
				#comm.send(AssignedList, dest=source, tag=dict_MPI_TAG['CONTINUE'])
			else:
				SendLog(FileLogFstream, comm, rank, None, 'SHUTDOWN', source)
				#comm.send(None, dest=source, tag=dict_MPI_TAG['SHUTDOWN'])
		elif tag_recv == dict_MPI_TAG['REPORT']:
			FinishedSerialTaskCount += len(RecvValue[0])
			FinishedSerialTaskCount += len(RecvValue[1])
			ListDoneSerialTasks += RecvValue[0]
			ListDoneSerialTasks += RecvValue[1]
			ClosedSubMaster += 1
	while ListDoneSerialTasks:
		DoneSerialTaskTemp = ListDoneSerialTasks.pop()
		print 'Complete task %s' % DoneSerialTaskTemp #(DoneSerialTaskTemp.env_dict['ID'], DoneSerialTaskTemp.env_dict['FLIP'])
	while ListErrorSerialTasks:
		ErrorSerialTaskTemp = ListErrorSerialTasks.pop()
		print 'Complete task %s' % ErrorSerialTaskTemp #(ErrorSerialTaskTemp.env_dict['ID'], ErrorSerialTaskTemp.env_dict['FLIP'])
# START CODE FOR STATIC SUBMASTER
elif rank == LocalMaster:
	DictActiveJobs = {}
	AssignedSerialTaskStrings = []
	ErrorListJobSerialTasks = []
	DoneListJobSerialTasks = []
	ShutdownFlag = False
	LocalWorkerList = ReturnSubList(ListBranchedTree, rank)
	StartCount = len(LocalWorkerList)
	ClosedSubNodes = 0
	# print 'PRELOOP: rank=%s as submaster with master=0 and workers=%s' % (str(rank), str(LocalWorkerList))
	StartTime = CurrentTimeStamp()
	while ClosedSubNodes<StartCount:
		if (not AssignedSerialTaskStrings) \
		and (not ShutdownFlag):
			SendLog(FileLogFstream, comm, rank, None, 'MORE', 0)
			#comm.send(None, dest=0, tag=dict_MPI_TAG['MORE'])
			(RecvValue, source, tag_recv) = RecvLog(FileLogFstream, rank, comm, 0)
			#RecvValue = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
			#source = status.Get_source()
			#tag_recv = status.Get_tag()
			if tag_recv == dict_MPI_TAG['CONTINUE']:
				AssignedSerialTaskStrings.extend(RecvValue)
			elif tag_recv == dict_MPI_TAG['SHUTDOWN']:
				ShutdownFlag = True
		else:
			(RecvValue, source, tag_recv) = RecvLog(FileLogFstream, rank, comm, MPI.ANY_SOURCE)
			#RecvValue = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
			#source = status.Get_source()
			#tag_recv = status.Get_tag()
			if tag_recv == dict_MPI_TAG['READY']:
				if ShutdownFlag:
					SendLog(FileLogFstream, comm, rank, None, 'CLOSE', source)
					#comm.send(None, dest=source, tag=dict_MPI_TAG['CLOSE'])
					ClosedSubNodes += 1
				else:
					StringAssignment = AssignedSerialTaskStrings.pop()
					SendLog(FileLogFstream, comm, rank, StringAssignment, 'START', source)
					#comm.send(StringAssignment, dest=source, tag=dict_MPI_TAG['START'])
					DictActiveJobs[StringAssignment] = source
			elif tag_recv == dict_MPI_TAG['DONE']:
				DictActiveJobs.pop(RecvValue)
				DoneListJobSerialTasks.append(RecvValue)
			elif tag_recv == dict_MPI_TAG['ERROR']:
				DictActiveJobs.pop(RecvValue)
				ErrorListJobSerialTasks.append(RecvValue)
	SendLog(FileLogFstream, comm, rank, (DoneListJobSerialTasks, ErrorListJobSerialTasks), 'REPORT', 0)
	#comm.send((DoneListJobSerialTasks, ErrorListJobSerialTasks), dest=0, tag=dict_MPI_TAG['REPORT'])
# START CODE FOR STATIC WORKER
else:
	print 'HHHHHHHHHHHHHEEEEEEEEEEEEEEEEEEEEELLLLLLLLLLLLLLLOOOOOOOOOOOOOOO'
	FileLogFstream.write('\nTIME=%.17f\START: rank=%s with LocalMaster=%s' % (CurrentTimeStamp(), str(rank), str(LocalMaster)))
	print '\nTIME=%.17f\START: rank=%s with LocalMaster=%s' % (CurrentTimeStamp(), str(rank), str(LocalMaster))
	while True:
		SendLog(FileLogFstream, comm, rank, None, 'READY', LocalMaster)
		# comm.send(None, dest=LocalMaster, tag=dict_MPI_TAG['READY'])
		(RecvValue, source, tag_recv) = RecvLog(FileLogFstream, rank, comm, LocalMaster)
		#RecvValue = comm.recv(source=LocalMaster, tag=MPI.ANY_TAG, status=status)
		#source = status.Get_source()
		#tag_recv = status.Get_tag()
		if tag_recv == dict_MPI_TAG['START']:
			SerialTaskCurrent = SerialTask(RecvValue)
			print 'start execute of %s on %s under %s' % (RecvValue, str(rank), str(LocalMaster))
			# time.sleep(1)
			TempResultSerialTaskExecute = SerialTaskCurrent.Execute()
			print 'finish execute of %s on %s under %s' % (RecvValue, str(rank), str(LocalMaster))
			if TempResultSerialTaskExecute:
				print 'success of %s on %s under %s' % (RecvValue, str(rank), str(LocalMaster))
				SendLog(FileLogFstream, comm, rank, RecvValue, 'DONE', LocalMaster)
				#comm.send(RecvValue, dest=LocalMaster, tag=dict_MPI_TAG['DONE'])
			else:
				print 'error of %s on %s under %s' % (RecvValue, str(rank), str(LocalMaster))
				SendLog(FileLogFstream, comm, rank, RecvValue, 'ERROR', LocalMaster)
				#comm.send(RecvValue, dest=LocalMaster, tag=dict_MPI_TAG['ERROR'])
		elif tag_recv == dict_MPI_TAG['CLOSE']:
			break
	SendLog(FileLogFstream, comm, rank, None, 'EXIT', 0)
	#comm.send(None, dest=0, tag=dict_MPI_TAG['EXIT'])