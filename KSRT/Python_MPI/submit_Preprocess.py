# This is a python version of the submit_Preprocess shell script
# as it was originally created by Amir Bahmani.  This is a parallel  
# version that pre-sorts N jobs across M nodes such that the number 
# of jobs per node is N divided by M rounded up.
# 
# NOTE:  This is a potentially inefficient parallization.  The jobs 
# per node times the percentage variance of runtime will give the 
# average number of jobs worth of deadtime for a given node.  A 
# queue system would correct this deficiency.
#

from mpi4py import MPI
import time
import csv
import os
import string
import subprocess
# this creates a table 
def loadtrainerdata(filename):
	with open(filename, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ')
	return spamreader

def checkcreatedir(directory):
	if not os.path.exists(directory):
		print('Creating directory: ' + directory)
		os.makedirs(directory)
	return

def checkfile(filepath):
	if not os.path.exists(filepath):
		return False
	else:
		return True


os.system('~/.ksrt_profile')

# os.system('export HOMEDIR=/home/sdmoore/updatedKSRT')

# os.system('export KSRT_SRC="$HOMEDIR"/ksrt')
# os.system('export scriptDIR="$KSRT_SRC"/script_SKI10/scripts')
# os.system('export DataDIR="$HOMEDIR"/dataNotBackedUp/SKI10')
# os.system('export DataDIRIn="$HOMEDIR"/dataNotBackedUp/SKI10')
# os.system('export DataDIROut="$HOMEDIR"/dataNotBackedUp/SKI10_out')
# os.system('export KSRT="$KSRT_SRC"/ksrt-build/KSRT-Build')

# os.system('export ksrtAppDIR="$KSRT"/bin')
# os.system('export svmDIR="$KSRT_SRC"/lib/libsvm-3.18')
# os.system('export svmOutDIR="$DataDIROut"/SVM')

# os.system('export trainingFILE="$scriptDIR"/../Train.txt')
# os.system('export testingFILE="$scriptDIR"/../Test.txt')
# os.system('export atlasFILE="$scriptDIR"/../atlas.txt')

start = time.time()
env_HOMEDIR = os.environ['HOMEDIR']

env_KSRT_SRC = os.environ['KSRT_SRC']
env_scriptDIR = os.environ['scriptDIR'] 
env_DataDIR = os.environ['DataDIR'] 
env_DataDIRIn = os.environ['DataDIRIn'] 
env_DataDIROut = os.environ['DataDIROut'] 
env_KSRT = os.environ['KSRT'] 

env_ksrtAppDIR = os.environ['ksrtAppDIR'] 
env_svmDIR = os.environ['svmDIR'] 
env_svmOutDIR = os.environ['svmOutDIR'] 

env_trainingFILE = os.environ['trainingFILE'] 
env_testingFILE = os.environ['testingFILE'] 
env_atlasFILE = os.environ['atlasFILE']


env_1_trainingFILE_filepath = '/home/sdmoore/updatedKSRT/ksrt/script_SKI10/Train_1.txt'
env_20_trainingFILE_filepath = '/home/sdmoore/updatedKSRT/ksrt/script_SKI10/Train_20.txt'
env_ALL_trainingFILE_filepath = '/home/sdmoore/updatedKSRT/ksrt/script_SKI10/Train.txt'

# This is where the list to preprocess is is set manually
env_trainingFILE_filepath = env_1_trainingFILE_filepath;

ksrtCopy_command = env_ksrtAppDIR + '/ksrtCopy '
ImageMath_command = env_ksrtAppDIR + '/ImageMath'
ksrtFlip_command = env_ksrtAppDIR + '/ksrtFlip'
N4ITKBiasFieldCorrection_command = env_ksrtAppDIR + '/N4ITKBiasFieldCorrection'
ksrtScaleIntensities_command = env_ksrtAppDIR + '/ksrtScaleIntensities'
CurvatureAnisotropicDiffusion_command = env_ksrtAppDIR + '/CurvatureAnisotropicDiffusion'
ksrtResample_command = env_ksrtAppDIR + '/ksrtResample'

list_row = []
with open(env_trainingFILE, 'r') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ')
	for row in spamreader:
		# current_string = string.split(row)
		# list_row = string.split(row)
		list_row.append(row) 
		# list_ID.append(row[0])
		# list_FLIP.append(row[1])

# getting basic info
comm = MPI.COMM_WORLD
rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()
name = MPI.Get_processor_name()


os.system('/home/sdmoore/.ksrt_profile')

# Take care of directories

#
# Displays the directories that have should have been set 
# through .ksrt_profile
#

print('KSRT directories set to:')
print('\n')
print('KSRT_SRC         = ' + env_KSRT_SRC)
print('ksrtAppDIR       = ' + env_ksrtAppDIR)
print('scriptDIR        = ' + env_scriptDIR)
print('DataDIRIn        = ' + env_DataDIRIn)
print('DataDIROut       = ' + env_DataDIROut)
print('svmDIR           = ' + env_svmDIR)
print('trainingFILE     = ' + env_trainingFILE) 
print('atlasFILE        = ' + env_atlasFILE)
print('testingFILE      = ' + env_testingFILE)
print('\n')

# Determine the task ID, so we can run it as a qsub program or as single user program 
currentprocess = rank

while currentprocess<len(list_row):
	list_string = list_row[currentprocess]
	# list_string = string.split(setname)
	node_env_ID = list_string[0]
	node_env_FLIP = list_string[1]

	# determine subject ID and if it needs to be flipped
	# this is done based on the trainingFILE
	# which contains *all* training cases
	print('Read: ID=' + node_env_ID + ' and flip=' + node_env_FLIP)

	# create directory for output
	# Creates directories for the storage of intermediate results for a particular ID

	checkcreatedir(env_DataDIROut + '/' + node_env_ID + '/')
	checkcreatedir(env_DataDIROut + '/' + node_env_ID + '/preprocess-orig/')
	checkcreatedir(env_DataDIROut + '/' + node_env_ID + '/preprocess/')
	
	# now move the current subject ID files in the output data directory and correct for flip if necessary
	# the resulting files will end up in the ' + env_DataDIROut + '/' + node_env_ID + '/preprocess directory

	# Adjusts the origin and flips images if needed. The end result will end up in the Train directory

	print('Running AdjustOriginAndFlipTrainingImagesIfNeededForID for ID = ' + node_env_ID)

	print('Converting ID to nrrd format and adjusting origin')

	os.system(env_ksrtAppDIR + '/ksrtCopy '
		+ env_DataDIRIn + '/image-' + node_env_ID + '.mhd '
		+ env_DataDIROut + '/' + node_env_ID + '/preprocess-orig/image-' + node_env_ID + '.nhdr')
	os.system(env_ksrtAppDIR + '/ImageMath ' 
		+ env_DataDIROut + '/' + node_env_ID + '/preprocess-orig/image-' + node_env_ID + '.nhdr -changeOrig 0,0,0 -outfile ' 
		+ env_DataDIROut + '/' + node_env_ID + '/preprocess-orig/image-' + node_env_ID + '.nhdr')

	if checkfile(env_DataDIRIn + '/labels-' + node_env_ID + '.mhd'):
		os.system(env_ksrtAppDIR + '/ksrtCopy '
			+ env_DataDIRIn + '/labels-' + node_env_ID + '.mhd '
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess-orig/labels-' + node_env_ID + '.nhdr')
		os.system(env_ksrtAppDIR + '/ImageMath '
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess-orig/labels-' + node_env_ID + '.nhdr -changeOrig 0,0,0 -outfile '
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess-orig/labels-' + node_env_ID + '.nhdr')

	if checkfile(env_DataDIRIn + '/roi-image-' + node_env_ID + '.mhd'):
		os.system(env_ksrtAppDIR + '/ksrtCopy '
			+ env_DataDIRIn + '/roi-image-' + node_env_ID + '.mhd '
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess-orig/roi-image-' + node_env_ID + '.nhdr')
		os.system(env_ksrtAppDIR + '/ImageMath '
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess-orig/roi-image-' + node_env_ID + '.nhdr -changeOrig 0,0,0 -outfile '
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess-orig/roi-image-' + node_env_ID + '.nhdr')
	print('Flipping ID if necessary')

	os.system(env_ksrtAppDIR + '/ksrtFlip '
		+ env_DataDIROut + '/' + node_env_ID + '/preprocess-orig/image-' + node_env_ID + '.nhdr -f 0,0,' + node_env_FLIP + ' '
		+ env_DataDIROut + '/' + node_env_ID + '/preprocess/image-' + node_env_ID + '.nhdr')

	if checkfile(env_DataDIROut + '/' + node_env_ID + '/preprocess-orig/labels-' + node_env_ID + '.nhdr'):
		os.system(env_ksrtAppDIR + '/ksrtFlip '
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess-orig/labels-' + node_env_ID + '.nhdr -f 0,0,' + node_env_FLIP + ' '
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess/labels-' + node_env_ID + '.nhdr')

	if checkfile(env_DataDIROut + '/' + node_env_ID + '/preprocess-orig/roi-image-' + node_env_ID + '.nhdr'):
		os.system(env_ksrtAppDIR + '/ksrtFlip '
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess-orig/roi-image-' + node_env_ID + '.nhdr -f 0,0,'
			+ node_env_FLIP + ' ' + 
	env_DataDIROut + '/' + node_env_ID + '/preprocess/roi-image-' + node_env_ID + '.nhdr')

	# now normalize the image: bias field correction, intensity adjustment, smoothing and scaling

	# 
	# Normalized the image with id ' + node_env_ID + '
	# by scaling intensities, performing bias field correction,
	# smoothing and scaling image size
	# 

	print('Running NormalizeImageForID for ID = ID')

	print('Performing bias field correction')
	os.system(env_ksrtAppDIR + '/N4ITKBiasFieldCorrection --outputbiasfield '
		+ env_DataDIROut + '/' + node_env_ID + '/preprocess/bias-' + node_env_ID + '.nhdr ' 
		+ env_DataDIROut + '/' + node_env_ID + '/preprocess/image-' + node_env_ID + '.nhdr '
		+ env_DataDIROut + '/' + node_env_ID + '/preprocess/image-' + node_env_ID + '-correct.nhdr')

	print('Scaling intensities')
	os.system(env_ksrtAppDIR + '/ksrtScaleIntensities ' 
		+ env_DataDIROut + '/' + node_env_ID + '/preprocess/image-' + node_env_ID + '-correct.nhdr '
		+ env_DataDIROut + '/' + node_env_ID + '/preprocess/image-' + node_env_ID + '-correct-scale.nhdr -m 100')

	print('Performing anisotropic smoothing')
	os.system(env_ksrtAppDIR + '/ImageMath ' 
		+ env_DataDIROut + '/' + node_env_ID + '/preprocess/image-' + node_env_ID + '-correct-scale.nhdr -smooth -curveEvol -iter 20 -outfile ' 
		+ env_DataDIROut + '/' + node_env_ID + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr')
	os.system(env_ksrtAppDIR + '/CurvatureAnisotropicDiffusion --timeStep 0.01 --iterations 50 '
		+ env_DataDIROut + '/' + node_env_ID + '/preprocess/image-' + node_env_ID + '-correct-scale.nhdr '
		+ env_DataDIROut + '/' + node_env_ID + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr')

	os.system(env_ksrtAppDIR + '/ksrtResample '
		+ env_DataDIROut + '/' + node_env_ID + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr -r newSize -v 100,100,100 '
		+ env_DataDIROut + '/' + node_env_ID + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth-small.nhdr')

	# extract the labels for femur, tibia, femoral and tibial cartilage from the label images (if they exist; which they will not for testing images)

	# 
	# Extracts femur, tibia, femoral, and tibial cartilage
	# from the label files
	# 

	print('Running ExtractIndividualLabelsForID for ID = ID')

	# only extract the labels if these files truly exist (only the case for training data)
	if checkfile(env_DataDIROut + '/' + node_env_ID + '/preprocess/labels-' + node_env_ID + '.nhdr'):
		os.system(env_ksrtAppDIR + '/ImageMath '
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess/labels-' + node_env_ID + '.nhdr -extractLabel 1 -outfile ' 
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess/femur-' + node_env_ID + '.nhdr')
		os.system(env_ksrtAppDIR + '/ImageMath '
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess/labels-' + node_env_ID + '.nhdr -extractLabel 2 -outfile ' 
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess/fem-' + node_env_ID + '.nhdr')
		os.system(env_ksrtAppDIR + '/ImageMath '
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess/labels-' + node_env_ID + '.nhdr -extractLabel 3 -outfile ' 
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess/tibia-' + node_env_ID + '.nhdr')
		os.system(env_ksrtAppDIR + '/ImageMath '
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess/labels-' + node_env_ID + '.nhdr -extractLabel 4 -outfile ' 
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess/tib-' + node_env_ID + '.nhdr')
		os.system(env_ksrtAppDIR + '/ksrtResample '
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess/femur-' + node_env_ID + '.nhdr -r newSize -v 100,100,100 ' 
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess/femur-' + node_env_ID + '-small.nhdr')
		os.system(env_ksrtAppDIR + '/ksrtResample '
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess/tibia-' + node_env_ID + '.nhdr -r newSize -v 100,100,100 '
			+ env_DataDIROut + '/' + node_env_ID + '/preprocess/tibia-' + node_env_ID + '-small.nhdr')
	currentprocess += size
end = time.time()
print "Total time: %f seconds" % (end - start)


