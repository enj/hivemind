#!/usr/bin/env python
import functools
import os
import string
import subprocess
import sys
import shutil
import time
import numpy
import csv
import copy
import datetime


# arbitrary return job from set of totally parallel independent jobs
def NextJobZeroDependence(InputBatchBatchJob):
	try:
		ReturnValue = InputBatchBatchJob.WaitingSetSerialTask.pop()
		return ReturnValue
	except KeyError:
		return False

# base class defining requirements for independently executing tasks
# class SerialTask:
	# def __init__(self):
	# def ExecuteSerialTask(self):
		# return self

# class defining an Parallel Job Class
class ParallelJob:
	def __init__(self,
		AssignedSerialTasks,
		NextJobDistributionAlgorithm = NextJobZeroDependence):
		self.WaitingSetSerialTask = AssignedSerialTasks
		self.AttemptedSetSerialTasks = set()
		self.CompletedSerialTasks = set()
		self.NextJobDistributionAlgorithm = NextJobDistributionAlgorithm
	def NextJob(self):
		return self.NextJobDistributionAlgorithm(self)
def CheckPath(filepath):
	if not os.path.exists(filepath):
		return False
	else:
		return True
def CheckCreateFile(filepath):
	try:
		filesteam = os.open(filepath,os.O_CREAT | os.O_EXCL,'w')
		return (filesteam, filepath)
	except:
		return (False, '')
def CheckCreateFileRetry(filepath, max_int_suffix = 99999, FileSuffix = 'txt'):
	current_int_suffix = 0
	FirstIteration = True
	CurrentFilepathNoSuffix = filepath
	(filesteam, FinalFilepath) = CheckCreateFile(CurrentFilepathNoSuffix + FileSuffix)
	while not filesteam:
		CurrentFilepathNoSuffix = filepath + '_' + str(current_int_suffix)
		if FirstIteration:
			FirstIteration = False
		elif current_int_suffix<=max_int_suffix:
			current_int_suffix += 1
			(filesteam, FinalFilepath) = CheckCreateFile(CurrentFilepathNoSuffix + FileSuffix)
		elif current_int_suffix>max_int_suffix:
			return (None, '')
	return (filesteam, FinalFilepath)
def CheckCreateDir(directory):
	if not os.path.exists(directory):
		try:
			os.makedirs(directory)
			return directory
		except OSError:
			return False
	else:
		return directory
def CheckCreateDirRetry(directory, max_int_suffix = 99999):
	current_int_suffix = 0
	FirstIteration = True
	current_directory = directory
	while not CheckCreateDir(current_directory):
		current_directory = directory + '_' + str(current_int_suffix)
		if FirstIteration:
			FirstIteration = False
		elif current_int_suffix<=max_int_suffix:
			current_int_suffix += 1
		elif current_int_suffix>max_int_suffix:
			return False
	return current_directory
def ForceCheckCreateDirRetry(directory, max_int_suffix = 99999):
	current_int_suffix = 0
	FirstIteration = True
	current_directory = directory
	while os.path.exists(current_directory):
		current_directory = directory + '_' + str(current_int_suffix)
		if FirstIteration:
			FirstIteration = False
		elif current_int_suffix<=max_int_suffix:
			current_int_suffix += 1
		elif current_int_suffix>max_int_suffix:
			return False
	return CheckCreateDir(current_directory)
def ksrtLoadTrainerData(filename):
	list_row = []
	list_row_TEMP = []
	with open(filename, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ')
		for row in spamreader:
			list_row.append(row)
	return list_row
class ksrtSubmitPreprocessSerialTask:
	def __init__(self, ID, FLIP):
		# SerialTask.__init__(self)
		self.env_dict = {}
		self.env_dict['ID'] = ID
		self.env_dict['FLIP'] = FLIP
	def ExecuteSerialTask(self):
		return self.FxnSubmitPreprocessing()

	def BoolJobCommandClaim(self, PairListDict, env_DataDIROut_WORKING):
		ReturnVal = True
		for CurrentCommand in PairListDict[0]:
			if CurrentCommand in PairListDict[1]:
				DictLocalLocationsCurrent = \
					self.GetDictLocationsCpMvMv(CurrentCommand, env_DataDIROut_WORKING)
				current_result_start = DictLocalLocationsCurrent['start']
				try:
					file_handle = \
						os.open(current_result_start, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
					continue
				except OSError:
					ReturnVal = False
		return ReturnVal
	def BoolJobCommandFinished(self, PairListDict, env_DataDIROut_WORKING):
		ReturnVal = False
		for CurrentCommand in PairListDict[0]:
			if CurrentCommand in PairListDict[1]:
				DictLocalLocationsCurrent = \
					self.GetDictLocationsCpMvMv(CurrentCommand, env_DataDIROut_WORKING)
				if CheckPath(CurrentCommand):
					ReturnVal = True
		return ReturnVal
	def FxnConditionalTmpfsWorkingDirectory(self):
		CurrentSubProcess = subprocess.Popen(['df','-t','tmpfs'], stdout=subprocess.PIPE)
		output = CurrentSubProcess.communicate()[0]
		output_lines = output.split('\n')[1:]
		if output_lines:
			(device, size, used, available, percent, mountpoint) = \
				output_lines[0].split()
			if int(available)>2500000:
				return mountpoint
			else:
				return False
		else:
			return False
	def FxnCpMvMv(self, CurrentCommand, env_DataDIROut_WORKING):
		DictLocalLocationsCurrent = \
			self.GetDictLocationsCpMvMv(CurrentCommand, env_DataDIROut_WORKING)
		CopyDirName = ForceCheckCreateDirRetry(os.path.dirname(CurrentCommand) + '/' + 'TEMP')
		CopiedVersionName = os.path.basename(CurrentCommand)
		#print 'verdict is for working:'
		#print os.path.exists(DictLocalLocationsCurrent['working'])
		shutil.copyfile( \
			DictLocalLocationsCurrent['working'], \
			DictLocalLocationsCurrent['copy'])
		#print 'verdict is for copy:'
		#print os.path.exists(DictLocalLocationsCurrent['copy'])
		shutil.move( \
			DictLocalLocationsCurrent['copy'], \
			DictLocalLocationsCurrent['temp'])
		#print 'verdict is for temp:'
		#print os.path.exists(DictLocalLocationsCurrent['temp'])
		shutil.move( \
			DictLocalLocationsCurrent['temp'], \
			DictLocalLocationsCurrent['final'])
		#print 'verdict is for final:'
		#print os.path.exists(DictLocalLocationsCurrent['final'])
		os.rmdir(CopyDirName)
		return True
	def CommandResultCopy(self, CommandResultPair, env_DataDIROut_WORKING):
		TimeStart = self.TimeSinceStartMilliseconds()
		#for dirname, dirnames, filenames in os.walk('/dev/shm'):
			#for subdirname in dirnames:
				#print(os.path.join(dirname, subdirname))
			#for filename in filenames:
				#print(os.path.join(dirname, filename))
		subprocess.call([' '.join(CommandResultPair[0])], shell=True)
		for CurrentCommand in CommandResultPair[0]:
			if CurrentCommand in CommandResultPair[1]:
				DictLocalLocationsCurrent = \
					self.GetDictLocationsCpMvMv(CurrentCommand, env_DataDIROut_WORKING)
				self.FxnCpMvMv(CurrentCommand, env_DataDIROut_WORKING)
		TimeEnd = self.TimeSinceStartMilliseconds()
		self.FileLogFstream.write('\nSTART_TIME=' + str(TimeStart) +' milliseconds' + \
			'\tEND_TIME=' + str(TimeEnd) + ' milliseconds' + \
			'\tTIMEDURATION=' + str(TimeEnd - TimeStart) +' milliseconds' + \
			'\tCOMMAND:' + ' '.join(CommandResultPair[0]) + \
			'\tRESULTS:' + ' '.join(CommandResultPair[1]))
		
		return True
	def GetDictLocationsCpMvMv(self, CurrentCommand, env_DataDIROut_WORKING):
		ReturnValue = {}
		ReplacedFinalVersion = \
			CurrentCommand.replace(env_DataDIROut_WORKING, self.env_dict['DataDIROut'])
		ReturnValue['start'] = \
			ReplacedFinalVersion + '.start'
		ReturnValue['working'] = \
			CurrentCommand
		ReturnValue['copy'] = \
			CurrentCommand + '.copy'
		ReturnValue['temp'] =  \
			ReplacedFinalVersion + '.temp'
		ReturnValue['final'] =  \
			ReplacedFinalVersion
		return ReturnValue
	def GenerateRequirementCommandResultLists(self, env_DataDIROut_WORKING, env_DataDIRIn_WORKING):	
		# os.call('ls ' + env_ksrtAppDIR)
		# os.path.exists(commandpath_ksrtCopy + )
		
		commandpath_ksrtCopy = self.env_dict['ksrtAppDIR'] + '/ksrtCopy'
		commandpath_ImageMath = self.env_dict['ksrtAppDIR'] + '/ImageMath'
		commandpath_ksrtFlip = self.env_dict['ksrtAppDIR'] + '/ksrtFlip'
		commandpath_N4ITKBiasFieldCorrection = self.env_dict['ksrtAppDIR'] + '/N4ITKBiasFieldCorrection'
		commandpath_ksrtScaleIntensities = self.env_dict['ksrtAppDIR'] + '/ksrtScaleIntensities'
		commandpath_CurvatureAnisotropicDiffusion = self.env_dict['ksrtAppDIR'] + '/CurvatureAnisotropicDiffusion'
		commandpath_ksrtResample = self.env_dict['ksrtAppDIR'] + '/ksrtResample'
		
		filename_preprocess_orig_image_nhdr = \
			'image-' + self.env_dict['ID'] + '.nhdr'
		filepath_preprocess_orig_image_nhdr = \
			env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess-orig/' + filename_preprocess_orig_image_nhdr
		filename_preprocess_orig_image_nhdr_unaltered = \
			'image-' + self.env_dict['ID'] + '_unaltered.nhdr'
		filepath_preprocess_orig_image_nhdr_unaltered = \
			env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess-orig/' + filename_preprocess_orig_image_nhdr_unaltered
		filename_preprocess_orig_labels_nhdr = \
			'labels-' + self.env_dict['ID'] + '.nhdr'
		filepath_preprocess_orig_labels_nhdr = \
			env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess-orig/' + filename_preprocess_orig_labels_nhdr
		filename_preprocess_orig_labels_nhdr_unaltered = \
			'labels-' + self.env_dict['ID'] + '_unaltered.nhdr'
		filepath_preprocess_orig_labels_nhdr_unaltered = \
			env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess-orig/' + filename_preprocess_orig_labels_nhdr_unaltered
		filename_preprocess_orig_roi_image_nhdr = \
			'roi-image-' + self.env_dict['ID'] + '.nhdr'
		filepath_preprocess_orig_roi_image_nhdr = \
			env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess-orig/' + filename_preprocess_orig_roi_image_nhdr
		filename_preprocess_orig_roi_image_nhdr_unaltered = \
			'roi-image-' + self.env_dict['ID'] + '_unaltered.nhdr'
		filepath_preprocess_orig_roi_image_nhdr_unaltered = \
			env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess-orig/' + filename_preprocess_orig_roi_image_nhdr_unaltered
		filename_preprocess_image_nhdr = \
			'image-' + self.env_dict['ID'] + '_unaltered.nhdr'
		filepath_preprocess_image_nhdr = \
			env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess/' + filename_preprocess_image_nhdr
		filename_preprocess_labels_nhdr = \
			'labels-' + self.env_dict['ID'] + '.nhdr'
		filepath_preprocess_labels_nhdr = \
			env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess/' + filename_preprocess_labels_nhdr
		filename_preprocess_roi_image_nhdr = \
			'roi-image-' + self.env_dict['ID'] + '.nhdr'
		filepath_preprocess_roi_image_nhdr = \
			env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess/' + filename_preprocess_roi_image_nhdr
		filename_preprocess_bias_nhdr = \
			'bias-' + self.env_dict['ID'] + '.nhdr'
		filepath_preprocess_bias_nhdr = \
			env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess/' + filename_preprocess_bias_nhdr
		filename_preprocess_image_correct_nhdr = \
			'image-' + self.env_dict['ID'] + '-correct.nhdr'
		filepath_preprocess_image_correct_nhdr = \
			env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess/' + filename_preprocess_image_correct_nhdr
		filename_preprocess_image_correct_scale_nhdr = \
			'image-' + self.env_dict['ID'] + '-correct-scale.nhdr'
		filepath_preprocess_image_correct_scale_nhdr = \
			env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess/' + filename_preprocess_image_correct_scale_nhdr
		filename_preprocess_image_correct_scale_smooth_nhdr = \
			'image-' + self.env_dict['ID'] + '-correct-scale-smooth.nhdr'
		filepath_preprocess_image_correct_scale_smooth_nhdr = \
			env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess/' + filename_preprocess_image_correct_scale_smooth_nhdr
		filename_preprocess_image_correct_scale_smooth_small_nhdr = \
			'image-' + self.env_dict['ID'] + '-correct-scale-smooth-small.nhdr'
		filepath_preprocess_image_correct_scale_smooth_small_nhdr = \
			env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess/' + filename_preprocess_image_correct_scale_smooth_small_nhdr
		filename_preprocess_femur_nhdr = \
			'femur-' + self.env_dict['ID'] + '.nhdr'
		filepath_preprocess_femur_nhdr = \
			env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess/' + filename_preprocess_femur_nhdr
		filename_preprocess_fem_nhdr = \
			'fem-' + self.env_dict['ID'] + '.nhdr'
		filepath_preprocess_fem_nhdr = \
			env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess/' + filename_preprocess_fem_nhdr
		filename_preprocess_tibia_nhdr = \
			'tibia-' + self.env_dict['ID'] + '.nhdr'
		filepath_preprocess_tibia_nhdr = \
			env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess/' + filename_preprocess_tibia_nhdr
		filename_preprocess_tib_nhdr = \
			'tib-' + self.env_dict['ID'] + '.nhdr'
		filepath_preprocess_tib_nhdr = \
			env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess/' + filename_preprocess_tib_nhdr
		filename_preprocess_femur_small_nhdr = \
			'femur-' + self.env_dict['ID'] + '-small.nhdr'
		filepath_preprocess_femur_small_nhdr = \
			env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess/' + filename_preprocess_femur_small_nhdr
		filename_preprocess_tibia_small_nhdr = \
			'tibia-' + self.env_dict['ID'] + '-small.nhdr'
		filepath_preprocess_tibia_small_nhdr = \
			env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess/' + filename_preprocess_tibia_small_nhdr
		
		filename_input_image_mhd = 'image-' + self.env_dict['ID'] + '.mhd'
		filename_input_labels_mhd = 'labels-' + self.env_dict['ID'] + '.mhd'
		filename_input_roi_image_mhd = 'roi-image-' + self.env_dict['ID'] + '.mhd'
		filename_input_image_raw = 'image-' + self.env_dict['ID'] + '.raw'
		filename_input_labels_raw = 'labels-' + self.env_dict['ID'] + '.raw'
		filename_input_roi_image_raw = 'roi-image-' + self.env_dict['ID'] + '.raw'
		
		filepath_start_input_image_mhd = self.env_dict['DataDIRIn'] + '/' + filename_input_image_mhd 
		filepath_start_input_labels_mhd = self.env_dict['DataDIRIn'] + '/' + filename_input_labels_mhd 
		filepath_start_input_roi_image_mhd = self.env_dict['DataDIRIn'] + '/' + filename_input_roi_image_mhd 
		filepath_start_input_image_raw = self.env_dict['DataDIRIn'] + '/' + filename_input_image_raw 
		filepath_start_input_labels_raw = self.env_dict['DataDIRIn'] + '/' + filename_input_labels_raw 
		filepath_start_input_roi_image_raw = self.env_dict['DataDIRIn'] + '/' + filename_input_roi_image_raw 
		
		filepath_input_image_mhd = env_DataDIRIn_WORKING + '/' + filename_input_image_mhd 
		filepath_input_labels_mhd = env_DataDIRIn_WORKING + '/' + filename_input_labels_mhd 
		filepath_input_roi_image_mhd = env_DataDIRIn_WORKING + '/' + filename_input_roi_image_mhd 
		filepath_input_image_raw = env_DataDIRIn_WORKING + '/' + filename_input_image_raw 
		filepath_input_labels_raw = env_DataDIRIn_WORKING + '/' + filename_input_labels_raw 
		filepath_input_roi_image_raw = env_DataDIRIn_WORKING + '/' + filename_input_roi_image_raw 
		
		CommandResultLists = []
		self.ListWorkingInputFiles = []
		if os.path.exists(filepath_start_input_image_mhd):
			shutil.copy( \
				filepath_start_input_image_mhd, \
				filepath_input_image_mhd)
			if os.path.exists(filepath_input_image_mhd):
				self.ListWorkingInputFiles.append(filepath_input_image_mhd)
		if os.path.exists(filepath_start_input_labels_mhd):
			shutil.copy( \
				filepath_start_input_labels_mhd, \
				filepath_input_labels_mhd)
			if os.path.exists(filepath_input_labels_mhd):
				self.ListWorkingInputFiles.append(filepath_input_labels_mhd)
		if os.path.exists(filepath_start_input_roi_image_mhd):
			shutil.copy( \
				filepath_start_input_roi_image_mhd, \
				filepath_input_roi_image_mhd)
			if os.path.exists(filepath_input_roi_image_mhd):
				self.ListWorkingInputFiles.append(filepath_input_roi_image_mhd)
		if os.path.exists(filepath_start_input_image_raw):
			shutil.copy( \
				filepath_start_input_image_raw, \
				filepath_input_image_raw)
			if os.path.exists(filepath_input_image_raw):
				self.ListWorkingInputFiles.append(filepath_input_image_raw)
		if os.path.exists(filepath_start_input_labels_raw):
			shutil.copy( \
				filepath_start_input_labels_raw, \
				filepath_input_labels_raw)
			if os.path.exists(filepath_input_labels_raw):
				self.ListWorkingInputFiles.append(filepath_input_labels_raw)
		if os.path.exists(filepath_start_input_roi_image_raw):
			shutil.copy( \
				filepath_start_input_roi_image_raw, \
				filepath_input_roi_image_raw)
			if os.path.exists(filepath_input_roi_image_raw):
				self.ListWorkingInputFiles.append(filepath_input_roi_image_raw)
		#print 'input files are here as:'
		#print self.ListWorkingInputFiles
		# CommandResultLists.append([[filepath_input_image_mhd]]) 
		# CommandResultLists.append([[filepath_input_labels_mhd]]) 
		# CommandResultLists.append([[filepath_input_roi_image_mhd]]) 
		# CommandResultLists.append([[filepath_input_image_raw]]) 
		# CommandResultLists.append([[filepath_input_labels_raw]]) 
		# CommandResultLists.append([[filepath_input_roi_image_raw]])
		# string_ANGER = '/pvfs2/sdmoore/updatedKSRT/ksrt/ksrt-build/KSRT-Build/bin/ksrtCopy'
		# string_RAGE = '/dev/shm/SKI10/image-003.mhd'
		# string_MEH = '/dev/shm/SKI10_out/003/preprocess-orig/image-003.nhdr'
		# list_ANGER_RAGE_MEH = [string_ANGER,string_RAGE,string_MEH]
		# print 'ugh... subpreprocess'
		# subprocess.call([' '.join(list_ANGER_RAGE_MEH)], shell=True)
		# print 'ugh... popen'
		# CurrentSubProcess = subprocess.Popen([' '.join(list_ANGER_RAGE_MEH)], stdout=subprocess.PIPE)
		# CommandResultLists.append([['echo','Running AdjustOriginAndFlipTrainingImagesIfNeededForID for ID = ' + self.env_dict['ID']],{}])
		self.ResultFilenameList = []
		# Adjusts the origin and flips images if needed. The end result will end up in the Train directory
		
		# CommandResultLists.append([['echo','Running AdjustOriginAndFlipTrainingImagesIfNeededForID for ID = ' + self.env_dict['ID']],{}])

		# CommandResultLists.append([['echo','Converting ID to nrrd format and adjusting origin'],{}])
		
		CommandResultLists.append([[commandpath_ksrtCopy,
			filepath_input_image_mhd,
			filepath_preprocess_orig_image_nhdr],
			[filepath_preprocess_orig_image_nhdr],[]])

		# CommandResultLists.append([['cp',
			# filepath_preprocess_orig_image_nhdr,
			# filepath_preprocess_orig_image_nhdr_unaltered],
			# [filepath_preprocess_orig_image_nhdr_unaltered],[]])
			
		CommandResultLists.append([[commandpath_ImageMath, 
			filepath_preprocess_orig_image_nhdr, 
			'-changeOrig', '0,0,0', '-outfile', 
			filepath_preprocess_orig_image_nhdr],
			[filepath_preprocess_orig_image_nhdr],[]])
		if filepath_input_roi_image_mhd in self.ListWorkingInputFiles:
			CommandResultLists.append([[commandpath_ksrtCopy,
				filepath_input_labels_mhd,
				filepath_preprocess_orig_labels_nhdr],
				[filepath_preprocess_orig_labels_nhdr],[]])
			# CommandResultLists.append([['cp',
				# filepath_preprocess_orig_labels_nhdr,
				# filepath_preprocess_orig_labels_nhdr_unaltered],
				# [filepath_preprocess_orig_labels_nhdr_unaltered],[]])
			CommandResultLists.append([[commandpath_ImageMath,
				filepath_preprocess_orig_labels_nhdr, 
				'-changeOrig', '0,0,0', '-outfile',
				filepath_preprocess_orig_labels_nhdr],
				[filepath_preprocess_orig_labels_nhdr],[]])
		if filepath_input_roi_image_mhd in self.ListWorkingInputFiles:
			CommandResultLists.append([[commandpath_ksrtCopy,
				filepath_input_roi_image_mhd,
				filepath_preprocess_orig_roi_image_nhdr],
				[filepath_preprocess_orig_roi_image_nhdr],[]])
			# CommandResultLists.append([[filepath_preprocess_orig_roi_image_nhdr],['cp',
				# filepath_preprocess_orig_roi_image_nhdr,
				# filepath_preprocess_orig_roi_image_nhdr_unaltered],
				# [filepath_preprocess_orig_roi_image_nhdr_unaltered],[]])
			CommandResultLists.append([[commandpath_ImageMath,
				filepath_preprocess_orig_roi_image_nhdr, 
				'-changeOrig', '0,0,0', '-outfile',
				filepath_preprocess_orig_roi_image_nhdr],
				[filepath_preprocess_orig_roi_image_nhdr],[]])
		# CommandResultLists.append([['echo','Flipping ID if necessary'],{}])
		
		CommandResultLists.append([[commandpath_ksrtFlip,
			filepath_preprocess_orig_image_nhdr, 
			'-f', '0,0,' + self.env_dict['FLIP'],
			filepath_preprocess_image_nhdr],
			[filepath_preprocess_image_nhdr],[]])
		if filepath_input_roi_image_mhd in self.ListWorkingInputFiles:
			CommandResultLists.append([[commandpath_ksrtFlip,
				filepath_preprocess_orig_labels_nhdr, 
				'-f', '0,0,' + self.env_dict['FLIP'],
				filepath_preprocess_labels_nhdr],
				[filepath_preprocess_labels_nhdr],[]])
		if filepath_input_roi_image_mhd in self.ListWorkingInputFiles:
			CommandResultLists.append([[commandpath_ksrtFlip,
				filepath_preprocess_orig_roi_image_nhdr, 
				'-f', '0,0,' + self.env_dict['FLIP'],
				filepath_preprocess_roi_image_nhdr],
				[filepath_preprocess_roi_image_nhdr],[]])

		# now normalize the image: bias field correction, intensity adjustment, smoothing and scaling

		# 
		# Normalized the image with id ' + self.env_dict['ID'] + '
		# by scaling intensities, performing bias field correction,
		# smoothing and scaling image size
		# 
		
		# CommandResultLists.append([['echo','Running NormalizeImageForID for ID = ID'],{}])

		# CommandResultLists.append([['echo','Performing bias field correction'],{}])
		CommandResultLists.append([[commandpath_N4ITKBiasFieldCorrection,
			'--outputbiasfield',
			filepath_preprocess_bias_nhdr, 
			filepath_preprocess_image_nhdr,
			filepath_preprocess_image_correct_nhdr],
			[filepath_preprocess_image_correct_nhdr,
				filepath_preprocess_bias_nhdr],[]])
		
		# CommandResultLists.append([['echo','Scaling intensities'],{}])
		CommandResultLists.append([[commandpath_ksrtScaleIntensities, 
			filepath_preprocess_image_correct_nhdr,
			filepath_preprocess_image_correct_scale_nhdr,
			'-m', '100'],[filepath_preprocess_image_correct_scale_nhdr],[]])

		# CommandResultLists.append([['echo','Performing anisotropic smoothing'],{}])
		CommandResultLists.append([[commandpath_ImageMath,
			filepath_preprocess_image_correct_scale_nhdr, 
			 '-smooth', '-curveEvol', '-iter', '20', '-outfile',
			filepath_preprocess_image_correct_scale_smooth_nhdr],
			[filepath_preprocess_image_correct_scale_smooth_nhdr],[]])
		CommandResultLists.append([[commandpath_CurvatureAnisotropicDiffusion, 
			'--timeStep', '0.01', '--iterations', '50',
			filepath_preprocess_image_correct_scale_nhdr,
			filepath_preprocess_image_correct_scale_smooth_nhdr],
			[filepath_preprocess_image_correct_scale_smooth_nhdr],[]])

		CommandResultLists.append([[commandpath_ksrtResample,
			filepath_preprocess_image_correct_scale_smooth_nhdr, 
			'-r', 'newSize', '-v', '100,100,100',
			filepath_preprocess_image_correct_scale_smooth_small_nhdr],
			[filepath_preprocess_image_correct_scale_smooth_small_nhdr],[]])

		# extract the labels for femur, tibia, femoral and tibial cartilage from the label images (if they exist; which they will not for testing images)

		# 
		# Extracts femur, tibia, femoral, and tibial cartilage
		# from the label files
		# 

		# CommandResultLists.append([['echo','Running ExtractIndividualLabelsForID for ID = $ID'],{}])
		if filepath_input_roi_image_mhd in self.ListWorkingInputFiles:
			# only extract the labels if these files truly exist (only the case for training data)
			CommandResultLists.append([[commandpath_ImageMath,
				filepath_preprocess_labels_nhdr, 
				'-extractLabel', '1', '-outfile', 
				filepath_preprocess_femur_nhdr],
				[filepath_preprocess_femur_nhdr],[]])
			CommandResultLists.append([[commandpath_ImageMath,
				filepath_preprocess_labels_nhdr, 
				'-extractLabel', '2', '-outfile', 
				filepath_preprocess_fem_nhdr],
				[filepath_preprocess_fem_nhdr],[]])
			CommandResultLists.append([[commandpath_ImageMath,
				filepath_preprocess_labels_nhdr, 
				'-extractLabel', '3', '-outfile', 
				filepath_preprocess_tibia_nhdr],
				[filepath_preprocess_tibia_nhdr],[]])
			CommandResultLists.append([[commandpath_ImageMath,
				filepath_preprocess_labels_nhdr, 
				'-extractLabel', '4', '-outfile', 
				filepath_preprocess_tib_nhdr],
				[filepath_preprocess_tib_nhdr],[]])
				
			CommandResultLists.append([[commandpath_ksrtResample,
				filepath_preprocess_femur_nhdr, 
				'-r', 'newSize', '-v', '100,100,100', 
				filepath_preprocess_femur_small_nhdr],
				[filepath_preprocess_femur_small_nhdr],[]])
			CommandResultLists.append([[commandpath_ksrtResample,
				filepath_preprocess_tibia_nhdr, 
				'-r', 'newSize', '-v', '100,100,100',
				filepath_preprocess_tibia_small_nhdr],
				[filepath_preprocess_tibia_small_nhdr],[]])
		for CommandResult in CommandResultLists:
			for Result in CommandResult[1]:
				if Result not in self.ResultFilenameList:
					self.ResultFilenameList.append(Result)
		RunningListOfListsFiles = []
		for CurrentCommandResultListPair in CommandResultLists:
			self.FileLogFstream.write('\nSTDIN=' + ' '.join(CurrentCommandResultListPair[0]))
			self.FileLogFstream.write('\nTESTS=' + ' '.join(CurrentCommandResultListPair[1]))
			for CurrentResult in CurrentCommandResultListPair[1]:
				for CurrentRunningList in RunningListOfListsFiles:
					if CurrentResult in CurrentRunningList:
						CurrentRunningList.remove(CurrentResult)
			if CurrentCommandResultListPair[1]:
				RunningListOfListsFiles.append(copy.deepcopy(CurrentCommandResultListPair[1]))
			CurrentCommandResultListPair[2] = [IndexList for IndexList in RunningListOfListsFiles if IndexList]
		UnacceptableResultListOfLists = []
		for CurrentCommandResultListPair in CommandResultLists:
			for SubCurrentCommandResultListPair in CommandResultLists:
				if CurrentCommandResultListPair[2]==SubCurrentCommandResultListPair[2] and CurrentCommandResultListPair[2]:
					if CurrentCommandResultListPair[2] not in UnacceptableResultListOfLists:
						UnacceptableResultListOfLists.append(CurrentCommandResultListPair[2])
		for CurrentCommandResultListPair in CommandResultLists:
			if CurrentCommandResultListPair[2] in UnacceptableResultListOfLists:
				CurrentCommandResultListPair[2] = []
		return CommandResultLists
	def TimeSinceStart(self):
		FxnSubmitPreprocessingStart = time.time()
		FxnSubmitPreprocessingNow = time.time()
		return (FxnSubmitPreprocessingNow - self.FxnSubmitPreprocessingStart)
	def TimeSinceStartMilliseconds(self):
		return (self.TimeSinceStart() * 1000.0)
	def FxnSubmitPreprocessing(self):
		self.FxnSubmitPreprocessingStart = time.time()
		self.ShellLogStdInOutErr = []
		subprocess.call(['~/.ksrt_profile'], shell=True)
		self.env_dict['HOMEDIR'] = os.environ['HOMEDIR']
		self.env_dict['KSRT_SRC'] = os.environ['KSRT_SRC']
		self.env_dict['scriptDIR'] = os.environ['scriptDIR'] 
		self.env_dict['DataDIR'] = os.environ['DataDIR'] 
		self.env_dict['DataDIRIn'] = os.environ['DataDIRIn']
		self.env_dict['DataDIROut'] = ForceCheckCreateDirRetry(os.environ['DataDIROut'])
		self.env_dict['KSRT'] = os.environ['KSRT'] 
		self.env_dict['ksrtAppDIR'] = os.environ['ksrtAppDIR'] 
		self.env_dict['svmDIR'] = os.environ['svmDIR'] 
		self.env_dict['svmOutDIR'] = os.environ['svmOutDIR'] 
		self.env_dict['trainingFILE'] = os.environ['trainingFILE'] 
		self.env_dict['testingFILE'] = os.environ['testingFILE'] 
		self.env_dict['atlasFILE'] = os.environ['atlasFILE']
		self.FileLogName = self.env_dict['HOMEDIR'] + '_LOGFILE_HDD.txt'
		self.FileLogFstream = open(self.FileLogName,'a')
		self.CommandResultSuccess = []
		today = datetime.date.today()
		self.FileLogFstream.write('\n' + today.ctime())
		self.CommandResultAttempt = None
		start_time_subjob = time.time() 
		self.env_dict['ID'] = self.env_dict['ID']
		self.env_dict['FLIP'] = self.env_dict['FLIP']
		print('Read: ID=' + self.env_dict['ID'] + ' and flip=' + self.env_dict['FLIP'])
		tmpfs_mountpoint = self.FxnConditionalTmpfsWorkingDirectory()
		# ssd_mountpoint = self.FxnConditionalSSDWorkingDirectory()
		if False: #tmpfs_mountpoint:
			env_DataDIROut_WORKING = \
				ForceCheckCreateDirRetry(tmpfs_mountpoint + '/SKI10_out')
			env_DataDIRIn_WORKING = \
				ForceCheckCreateDirRetry(tmpfs_mountpoint + '/SKI10')
		else:
			env_DataDIROut_WORKING = \
				ForceCheckCreateDirRetry(self.env_dict['DataDIROut'] + '/TEMP')
			env_DataDIRIn_WORKING = \
				ForceCheckCreateDirRetry(self.env_dict['DataDIRIn'] + '/TEMP')
		if env_DataDIROut_WORKING and env_DataDIRIn_WORKING \
			and CheckCreateDir(self.env_dict['DataDIROut'] + '/' + self.env_dict['ID'] + '/preprocess/') \
			and CheckCreateDir(self.env_dict['DataDIROut'] + '/' + self.env_dict['ID'] + '/preprocess-orig/') \
			and CheckCreateDir(self.env_dict['DataDIROut'] + '/' + self.env_dict['ID']) \
			and CheckCreateDir(env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess/') \
			and CheckCreateDir(env_DataDIROut_WORKING + '/' + self.env_dict['ID'] + '/preprocess-orig/') \
			and CheckCreateDir(env_DataDIROut_WORKING + '/' + self.env_dict['ID']):
			self.RequirementCommandResultListLocalized = \
				self.GenerateRequirementCommandResultLists(env_DataDIROut_WORKING, env_DataDIRIn_WORKING)
			for CommandResultPair in self.RequirementCommandResultListLocalized:
				if self.BoolJobCommandFinished(CommandResultPair, env_DataDIROut_WORKING):
					continue
				else:
					if self.BoolJobCommandClaim(CommandResultPair, env_DataDIROut_WORKING):
						self.CommandResultCopy(CommandResultPair, env_DataDIROut_WORKING)
					else:
						break
		shutil.rmtree(env_DataDIROut_WORKING)
		shutil.rmtree(env_DataDIRIn_WORKING)
		return True
# sorted_list = []
# for object in my_list_of_objects:
    # i = my_number_giving_function(object)
    # sorted_list.insert(i, object)
def FxnGetModificationTime(FilePath):
	return os.path.getmtime(FilePath)

def OrderConsistent(InputList, InputListsOfLists):
	CopyInputList = copy.deepcopy(InputList)
	CopyInputListOfLists = copy.deepcopy(InputListsOfLists)
	while CopyInputList or CopyInputListOfLists:
		CurrentValue = copy.deepcopy(CopyInputList[0])
		print CurrentValue
		print CopyInputList
		print CopyInputListOfLists
		print InputList
		print InputListsOfLists
		if CopyInputListOfLists[0]:
			if CurrentValue in CopyInputListOfLists[0]:
				CopyInputList.remove(CurrentValue)
				CopyInputListOfLists[0].remove(CurrentValue)
			else:
				return False
		else:
			CopyInputListOfLists.remove(CopyInputListOfLists[0])
	return True
# def IndexOfLastMention(InputString)
	# for CurrentRequirementCommandResult in self.RequirementCommandResultListLocalized[]
		# for CurrentRequirementCommandResult[]
		# InputString
# sort(my_list_of_objects, key=my_number_giving_function)
# functools.cmp_to_key(os.path.getmtime(FilePath))
# functools.cmp_to_key(PosetComparison)

# def FxnPosetComparison(Input0, Input1, ListOfLists, SubIndex):
	# for self.RequirementCommandResultListLocalized[1]:
		# if 
