
from mpi4py import MPI
import time
import csv
import os
import string
import subprocess

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

subprocess.call('~/.ksrt_profile', shell=True)
 

# subprocess.call('export HOMEDIR=/home/sdmoore/updatedKSRT', shell=True, shell=True)

# subprocess.call('export KSRT_SRC="$HOMEDIR"/ksrt', shell=True, shell=True)
# subprocess.call('export scriptDIR="$KSRT_SRC"/script_SKI10/scripts', shell=True, shell=True)
# subprocess.call('export DataDIR="$HOMEDIR"/dataNotBackedUp/SKI10', shell=True, shell=True)
# subprocess.call('export DataDIRIn="$HOMEDIR"/dataNotBackedUp/SKI10', shell=True)
# subprocess.call('export DataDIROut="$HOMEDIR"/dataNotBackedUp/SKI10_out', shell=True)
# subprocess.call('export KSRT="$KSRT_SRC"/ksrt-build/KSRT-Build', shell=True)

# subprocess.call('export ksrtAppDIR="$KSRT"/bin', shell=True)
# subprocess.call('export svmDIR="$KSRT_SRC"/lib/libsvm-3.18', shell=True)
# subprocess.call('export svmOutDIR="$DataDIROut"/SVM', shell=True)

# subprocess.call('export trainingFILE="$scriptDIR"/../Train.txt', shell=True)
# subprocess.call('export testingFILE="$scriptDIR"/../Test.txt', shell=True)
# subprocess.call('export atlasFILE="$scriptDIR"/../atlas.txt', shell=True)


# env_HOMEDIR = '/home/sdmoore/updatedKSRT'

# env_KSRT_SRC = env_HOMEDIR + '/ksrt'
# env_scriptDIR = env_KSRT_SRC + '/script_SKI10/scripts'
# env_DataDIR = env_HOMEDIR + '/dataNotBackedUp/SKI10'
# env_DataDIRIn = env_HOMEDIR + '/dataNotBackedUp/SKI10'
# env_DataDIROut = env_HOMEDIR + '/dataNotBackedUp/SKI10_out'
# env_KSRT = env_KSRT_SRC + '/ksrt-build/KSRT-Build'

# env_ksrtAppDIR = env_KSRT + '/bin'
# env_svmDIR = env_KSRT_SRC + '/lib/libsvm-3.18'
# env_svmOutDIR = env_DataDIROut + '/SVM'

# env_trainingFILE = env_scriptDIR + '/../Train.txt'
# env_testingFILE = env_scriptDIR + '/../Test.txt'
# env_atlasFILE = env_scriptDIR + '/../atlas.txt'


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

env_trainingFILE_filepath = env_1_trainingFILE_filepath;


# create list of files to be processed
list_row = []
print('list_row = ')
with open(env_trainingFILE, 'r') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ')
	for row in spamreader:
		print(row[0] + ' ')
		list_row.append(row) 
print('\n')

# create list of comparison examples to be compared with
comparison_row = []
print('comparison_row = ')
with open(env_atlasFILE, 'r') as csvfile:
	spamreader_comparison = csv.reader(csvfile, delimiter=' ')
	for row in spamreader_comparison:
		print(row[0] + ' ')
		comparison_row.append(row) 
print('\n')

# create list of data comparison pairs to be prcoessed
# comparison_pair_list[]
# for current_ID in list_row:
	# for comparison_ID in comparison_row:
		# if current_ID==comparison_ID:
			# continue
		# sublist[]
		# sublist.append(current_ID)
		# sublist.append(comparison_ID)
		# comparison_pair_list.append(sublist)
# getting basic MPI info
comm = MPI.COMM_WORLD
rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()
name = MPI.Get_processor_name()
currentprocess = rank;

# start system clock timing for process
start = time.time()

# begin looping through modulus-based pre-assigned data inputs
while currentprocess<len(list_row):
	list_string = list_row[currentprocess]
	# list_string = string.split(setname)
	node_env_ID = list_string[0]
	# node_env_FLIP = list_string[1]
	text_file = open('output_' + node_env_ID + '.txt', 'w')

	text_file.write('Start file write:\n')
	
	print('KSRT directories set to:\n')
	print('KSRT_SRC         = ' + env_KSRT_SRC)
	print('ksrtAppDIR       = ' + env_ksrtAppDIR)
	print('scriptDIR        = ' + env_scriptDIR)
	print('DataDIRIn        = ' + env_DataDIRIn)
	print('DataDIROut       = ' + env_DataDIROut)
	print('svmDIR           = ' + env_svmDIR)
	print('trainingFILE     = ' + env_trainingFILE)
	print('atlasFILE        = ' + env_atlasFILE)
	print('testingFILE      = ' + env_testingFILE + '\n')
	print('Running preprocessing')


		
	# Performs the segmentations of femur and the tibia for the id $ID
	# print('Read: ID=' + node_env_ID + ' and flip=' + node_env_FLIP)
	
	# output_dirpath = node_env_DataDIROut + '/'
	# output_bone_segmentation_dirpath = node_env_DataDIROut + '/bone_segmentation/'
	# output_moved_bone_atlas_dirpath = node_env_DataDIROut + '/moved_bone_atlas/'
	# output_cartilage_segmentation_dirpath = node_env_DataDIROut + '/cartilage_segmentation/'
	
	node_env_DataDIROut = env_DataDIROut + '/' + node_env_ID #+ '/'
	node_env_BoneSegOutDIR = node_env_DataDIROut + '/bone_segmentation' #+ '/'
	node_env_BoneRegOutDIR = node_env_DataDIROut + '/moved_bone_atlas' #+ '/'
	node_env_CartilageSegOutDIR = node_env_DataDIROut + '/cartilage_segmentation' #+ '/'
	
	checkcreatedir(node_env_DataDIROut)
	checkcreatedir(node_env_BoneSegOutDIR)
	checkcreatedir(node_env_BoneRegOutDIR)
	checkcreatedir(node_env_CartilageSegOutDIR)
	
	print('Running DoBoneSegmentationForID for ID = ' + node_env_ID)
	print('Creating empty image for femur fusion: ' + \
		node_env_BoneSegOutDIR + '/femur-fusion-' + node_env_ID + '.nhdr')
	command_string_buffer = env_ksrtAppDIR + '/ImageMath ' + \
		node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr -sub ' + \
		node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr -outfile ' + \
		node_env_BoneSegOutDIR + '/femur-fusion-' + node_env_ID + '.nhdr -type float'
	print('\nAttempt command:' + command_string_buffer + '\n')
	subprocess.call(command_string_buffer, shell=True)
	text_file.write(command_string_buffer + 'n')
	# subprocess.call(env_ksrtAppDIR + '/ImageMath ' 
		# + node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr -sub ' 
		# + node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr -outfile ' 
		# + node_env_BoneSegOutDIR + '/femur-fusion-' + node_env_ID + '.nhdr -type float', shell=True)

	print('Creating empty image for tibia fusion: ' + \
		node_env_BoneSegOutDIR + '/tibia-fusion-' + node_env_ID + '.nhdr')
	command_string_buffer = env_ksrtAppDIR + '/ImageMath ' + \
		node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr -sub ' + \
		node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr -outfile ' + \
		node_env_BoneSegOutDIR + '/tibia-fusion-' + node_env_ID + '.nhdr -type float'
	print('\nAttempt command:' + command_string_buffer + '\n')
	subprocess.call(command_string_buffer, shell=True)
	text_file.write(command_string_buffer + 'n')
	# subprocess.call(env_ksrtAppDIR + '/ImageMath ' 
		# + node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr -sub ' 
		# + node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr -outfile ' 
		# + node_env_BoneSegOutDIR + '/tibia-fusion-' + node_env_ID + '.nhdr -type float', shell=True)


	# Performs the segmentations of femur and the tibia for the id $ID
	print('Running DoBoneSegmentationForID for ID = ' + node_env_ID)

	print('Creating empty image for femur fusion: ' + \
		node_env_BoneSegOutDIR + '/femur-fusion-' + node_env_ID + '.nhdr')
	command_string_buffer = env_ksrtAppDIR + '/ImageMath ' + \
		node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr -sub ' + \
		node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr -outfile ' + \
		node_env_BoneSegOutDIR + '/femur-fusion-' + node_env_ID + '.nhdr -type float'
	print('\nAttempt command:' + command_string_buffer + '\n')
	subprocess.call(command_string_buffer, shell=True)
	text_file.write(command_string_buffer + 'n')
	# subprocess.call(env_ksrtAppDIR + '/ImageMath ' 
		# + node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr -sub ' 
		# + node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr -outfile ' 
		# + node_env_BoneSegOutDIR + '/femur-fusion-' + node_env_ID + '.nhdr -type float', shell=True)

	print('Creating empty image for tibia fusion: ' + \
		node_env_BoneSegOutDIR + '/tibia-fusion-' + node_env_ID + '.nhdr')
	command_string_buffer = env_ksrtAppDIR + '/ImageMath ' + \
		node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr -sub ' + \
		node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr -outfile ' + \
		node_env_BoneSegOutDIR + '/femur-fusion-' + node_env_ID + '.nhdr -type float'
	print('\nAttempt command:' + command_string_buffer + '\n')
	subprocess.call(command_string_buffer, shell=True)
	text_file.write(command_string_buffer + 'n')
	# subprocess.call(env_ksrtAppDIR + '/ImageMath ' 
		# + node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr -sub ' 
		# + node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr -outfile ' 
		# + node_env_BoneSegOutDIR + '/femur-fusion-' + node_env_ID + '.nhdr -type float', shell=True)
	
	var_n = 0
	var_n_all = 0
	
	for comparison_string in comparison_row:
		comparison_ID = comparison_string[0]
		# comparison_FLIP = comparison_string[1]
		# $ksrtAppDIR/ksrtComputeKneeAffineRegistration
		# "$DataDIROut"/"$ID"/preprocess/image-"$ID"-correct-scale-smooth.nhdr
		# "$DataDIROut"/"$ID_A"/preprocess/image-"$ID_A"-correct-scale-smooth.nhdr --metric MI 
		# "$BoneRegOutDIR"/affine-"$ID"-"$ID_A".nhdr 
		# "$BoneRegOutDIR"/affine-"$ID"-"$ID_A".tfm

		# computing affine registration
		print('Affinely registering ' + comparison_ID + ' to ' + node_env_ID)
		command_string_buffer = env_ksrtAppDIR + '/ksrtComputeKneeAffineRegistration ' + \
			node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr ' + \
			env_DataDIROut + '/' + comparison_ID + '/preprocess/image-' + comparison_ID + '-correct-scale-smooth.nhdr --metric MI ' + \
			node_env_BoneRegOutDIR + '/affine-' + node_env_ID + '-' + comparison_ID + '.nhdr ' + \
			node_env_BoneRegOutDIR + '/affine-' + node_env_ID + '-' + comparison_ID + '.tfm'
		print('\nAttempt command:' + command_string_buffer + '\n')
		subprocess.call(command_string_buffer, shell=True)
		text_file.write(command_string_buffer + 'n')
		# subprocess.call(env_ksrtAppDIR + '/ksrtComputeKneeAffineRegistration ' 
			# + node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr ' 
			# + env_DataDIROut + '/' + comparison_ID + '/preprocess/image-' + comparison_ID + '-correct-scale-smooth.nhdr --metric MI ' 
			# + node_env_BoneRegOutDIR + '/affine-' + node_env_ID + '-' + comparison_ID + '.nhdr ' 
			# + node_env_BoneRegOutDIR + '/affine-' + node_env_ID + '-' + comparison_ID + '.tfm', shell=True)

		print('Computing B-spline registration from ' + comparison_ID + ' to ' + node_env_ID)
		command_string_buffer = env_ksrtAppDIR + '/BSplineDeformableRegistration ' + \
			node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr ' + \
			node_env_BoneRegOutDIR + '/affine-' + node_env_ID + '-' + comparison_ID + '.nhdr --histogrambins 20 --spatialsamples 100000 --iterations 200 --constrain --maximumDeformation 10.0 --resampledmovingfilename ' + \
			node_env_BoneRegOutDIR + '/bspline-' + node_env_ID + '-' + comparison_ID + '.nhdr --outputtransform ' + \
			node_env_BoneRegOutDIR + '/bspline-' + node_env_ID + '-' + comparison_ID + '.tfm'
		print('\nAttempt command:' + command_string_buffer + '\n')
		subprocess.call(command_string_buffer, shell=True)
		text_file.write(command_string_buffer + 'n')
		# subprocess.call(env_ksrtAppDIR + '/BSplineDeformableRegistration ' 
			# + node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr ' 
			# + node_env_BoneRegOutDIR + '/affine-' + node_env_ID + '-' + comparison_ID + '.nhdr --histogrambins 20 --spatialsamples 100000 --iterations 200 --constrain --maximumDeformation 10.0 --resampledmovingfilename ' 
			# + node_env_BoneRegOutDIR + '/bspline-' + node_env_ID + '-' + comparison_ID + '.nhdr --outputtransform ' 
			# + node_env_BoneRegOutDIR + '/bspline-' + node_env_ID + '-' + comparison_ID + '.tfm', shell=True)
	
		var_n_all = var_n_all + 1
		affine_file_flag = checkfile(node_env_BoneRegOutDIR + '/affine-' + node_env_ID + '-' + comparison_ID + '.tfm') # -f
		bspline_file_flag = checkfile(node_env_BoneRegOutDIR + '/bspline-' + node_env_ID + '-' + comparison_ID + '.tfm') # -a -f 
		if affine_file_flag and bspline_file_flag:
			var_n = var_n + 1
			# here we are moving the segmentations
			print('Transforming the segmentations')
			# for femur
			command_string_buffer = env_ksrtAppDIR + '/ksrtApplyAffineTransform ' + \
				node_env_BoneRegOutDIR + '/affine-' + node_env_ID + '-' + comparison_ID + '.tfm ' + \
				env_DataDIROut + '/' + comparison_ID + '/preprocess/femur-' + comparison_ID + '.nhdr ' + \
				node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr ' + \
				node_env_BoneRegOutDIR + '/femur-' + node_env_ID + '-' + comparison_ID + '.nhdr'
			print('\nAttempt command:' + command_string_buffer + '\n')
			subprocess.call(command_string_buffer, shell=True)
			text_file.write(command_string_buffer + 'n')
			# subprocess.call(env_ksrtAppDIR + '/ksrtApplyAffineTransform ' 
				# + node_env_BoneRegOutDIR + '/affine-' + node_env_ID + '-' + comparison_ID + '.tfm ' 
				# + env_DataDIROut + '/' + comparison_ID + '/preprocess/femur-' + comparison_ID + '.nhdr ' 
				# + node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr ' 
				# + node_env_BoneRegOutDIR + '/femur-' + node_env_ID + '-' + comparison_ID + '.nhdr', shell=True)
			# for tibia
			command_string_buffer = env_ksrtAppDIR + '/ksrtApplyBSplineTransform ' + \
				node_env_BoneRegOutDIR + '/bspline-' + node_env_ID + '-' + comparison_ID + '.tfm ' + \
				node_env_BoneRegOutDIR + '/femur-' + node_env_ID + '-' + comparison_ID + '.nhdr ' + \
				node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr ' + \
				node_env_BoneRegOutDIR + '/femur-' + node_env_ID + '-' + comparison_ID + '.nhdr'
			print('\nAttempt command:' + command_string_buffer + '\n')
			subprocess.call(command_string_buffer, shell=True)
			text_file.write(command_string_buffer + 'n')
			# subprocess.call(env_ksrtAppDIR + '/ksrtApplyBSplineTransform ' 
				# + node_env_BoneRegOutDIR + '/bspline-' + node_env_ID + '-' + comparison_ID + '.tfm ' 
				# + node_env_BoneRegOutDIR + '/femur-' + node_env_ID + '-' + comparison_ID + '.nhdr ' 
				# + node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr ' 
				# + node_env_BoneRegOutDIR + '/femur-' + node_env_ID + '-' + comparison_ID + '.nhdr', shell=True)
			# TODO: could use concatenated transform
			command_string_buffer = env_ksrtAppDIR + '/ksrtApplyAffineTransform ' + \
				node_env_BoneRegOutDIR + '/affine-' + node_env_ID + '-' + comparison_ID + '.tfm ' + \
				env_DataDIROut + '/' + comparison_ID + '/preprocess/tibia-' + comparison_ID + '.nhdr ' + \
				node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr ' + \
				node_env_BoneRegOutDIR + '/tibia-' + node_env_ID + '-' + comparison_ID + '.nhdr'
			print('\nAttempt command:' + command_string_buffer + '\n')
			subprocess.call(command_string_buffer, shell=True)
			text_file.write(command_string_buffer + 'n')
			# subprocess.call(env_ksrtAppDIR + '/ksrtApplyAffineTransform ' 
				# + env_DataDIROut + '/' + comparison_ID + '/preprocess/tibia-' + comparison_ID + '.nhdr ' 
				# + node_env_BoneRegOutDIR + '/affine-' + node_env_ID + '-' + comparison_ID + '.tfm ' 
				# + node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr ' 
				# + node_env_BoneRegOutDIR + '/tibia-' + node_env_ID + '-' + comparison_ID + '.nhdr', shell=True)
			# TODO: could use concatenated spline
			
			command_string_buffer = env_ksrtAppDIR + '/ksrtApplyBSplineTransform ' + \
				node_env_BoneRegOutDIR + '/bspline-' + node_env_ID + '-' + comparison_ID + '.tfm ' + \
				node_env_BoneRegOutDIR + '/tibia-' + node_env_ID + '-' + comparison_ID + '.nhdr ' + \
				node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr ' + \
				node_env_BoneRegOutDIR + '/tibia-' + node_env_ID + '-' + comparison_ID + '.nhdr'
			print('\nAttempt command:' + command_string_buffer + '\n')
			subprocess.call(command_string_buffer, shell=True)
			text_file.write(command_string_buffer + 'n')
			# subprocess.call(env_ksrtAppDIR + '/ksrtApplyBSplineTransform ' 
				# + node_env_BoneRegOutDIR + '/bspline-' + node_env_ID + '-' + comparison_ID + '.tfm ' 
				# + node_env_BoneRegOutDIR + '/tibia-' + node_env_ID + '-' + comparison_ID + '.nhdr ' 
				# + node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr ' 
				# + node_env_BoneRegOutDIR + '/tibia-' + node_env_ID + '-' + comparison_ID + '.nhdr', shell=True)
			# now add it to the fusion file
			
			command_string_buffer = env_ksrtAppDIR + '/ImageMath ' + \
				node_env_BoneSegOutDIR + '/femur-fusion-' + node_env_ID + '.nhdr -add ' + \
				node_env_BoneRegOutDIR + '/femur-' + node_env_ID + '-' + comparison_ID + '.nhdr -outfile ' + \
				node_env_BoneSegOutDIR + '/femur-fusion-' + node_env_ID + '.nhdr -type float'
			print('\nAttempt command:' + command_string_buffer + '\n')
			subprocess.call(command_string_buffer, shell=True)
			text_file.write(command_string_buffer + 'n')
			# subprocess.call(env_ksrtAppDIR + '/ImageMath ' 
				# + node_env_BoneSegOutDIR + '/femur-fusion-' + node_env_ID + '.nhdr -add ' 
				# + node_env_BoneRegOutDIR + '/femur-' + node_env_ID + '-' + comparison_ID + '.nhdr -outfile ' 
				# + node_env_BoneSegOutDIR + '/femur-fusion-' + node_env_ID + '.nhdr -type float', shell=True)

			command_string_buffer = env_ksrtAppDIR + '/ImageMath ' + \
				node_env_BoneSegOutDIR + '/tibia-fusion-' + node_env_ID + '.nhdr -add ' + \
				node_env_BoneRegOutDIR + '/tibia-' + node_env_ID + '-' + comparison_ID + '.nhdr -outfile ' + \
				node_env_BoneSegOutDIR + '/tibia-fusion-' + node_env_ID + '.nhdr -type float'
			print('\nAttempt command:' + command_string_buffer + '\n')
			subprocess.call(command_string_buffer, shell=True)
			text_file.write(command_string_buffer + 'n')
			# subprocess.call(env_ksrtAppDIR + '/ImageMath ' 
				# + node_env_BoneSegOutDIR + '/tibia-fusion-' + node_env_ID + '.nhdr -add ' 
				# + node_env_BoneRegOutDIR + '/tibia-' + node_env_ID + '-' + comparison_ID + '.nhdr -outfile ' 
				# + node_env_BoneSegOutDIR + '/tibia-fusion-' + node_env_ID + '.nhdr -type float', shell=True)
		print('Successfully registered ' + str(var_n) + '/' + str(var_n_all) + ' images')
	# now do division to get the probability map
	print('Computing bone probability maps')
	
	command_string_buffer = env_ksrtAppDIR + '/ImageMath ' + \
		node_env_BoneSegOutDIR + '/femur-fusion-' + node_env_ID + '.nhdr -constOper 3,' + str(var_n) + ' -outfile ' + \
		node_env_BoneSegOutDIR + '/femur-fusion-' + node_env_ID + '.nhdr -type float'
	print('\nAttempt command:' + command_string_buffer + '\n')
	subprocess.call(command_string_buffer, shell=True)
	text_file.write(command_string_buffer + 'n')
	# subprocess.call(env_ksrtAppDIR + '/ImageMath ' 
		# + node_env_BoneSegOutDIR + '/femur-fusion-' + node_env_ID + '.nhdr -constOper 3,' + str(var_n, shell=True) + ' -outfile ' 
		# + node_env_BoneSegOutDIR + '/femur-fusion-' + node_env_ID + '.nhdr -type float')
	
	command_string_buffer = env_ksrtAppDIR + '/ImageMath ' + \
		node_env_BoneSegOutDIR + '/tibia-fusion-' + node_env_ID + '.nhdr -constOper 3,' + str(var_n) + ' -outfile ' + \
		node_env_BoneSegOutDIR + '/tibia-fusion-' + node_env_ID + '.nhdr -type float'
	print('\nAttempt command:' + command_string_buffer + '\n')
	subprocess.call(command_string_buffer, shell=True)
	text_file.write(command_string_buffer + 'n')
	# subprocess.call(env_ksrtAppDIR + '/ImageMath ' 
		# + node_env_BoneSegOutDIR + '/tibia-fusion-' + node_env_ID + '.nhdr -constOper 3,' + str(var_n, shell=True) + ' -outfile ' 
		# + node_env_BoneSegOutDIR + '/tibia-fusion-' + node_env_ID + '.nhdr -type float')
	
	# compute the costs for the segmentation
	print('Compute labeling costs')
	command_string_buffer = env_ksrtAppDIR + '/ksrtComputeBoneProbabilityUsingAssumption ' + \
		node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr ' + \
		node_env_BoneSegOutDIR + '/pBone-' + node_env_ID + '.nhdr'
	print('\nAttempt command:' + command_string_buffer + '\n')
	subprocess.call(command_string_buffer, shell=True)
	text_file.write(command_string_buffer + 'n')
	# subprocess.call(env_ksrtAppDIR + '/ksrtComputeBoneProbabilityUsingAssumption ' + \
		# node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr ' + \
		# node_env_BoneSegOutDIR + '/pBone-' + node_env_ID + '.nhdr', shell=True)
	
	command_string_buffer = env_ksrtAppDIR + '/ksrtComputeBoneLabelingCost ' + \
		node_env_BoneSegOutDIR + '/pBone-' + node_env_ID + '.nhdr ' + \
		node_env_BoneSegOutDIR + '/femur-fusion-' + node_env_ID + '.nhdr ' + \
		node_env_BoneSegOutDIR + '/tibia-fusion-' + node_env_ID + '.nhdr ' + \
		node_env_BoneSegOutDIR + '/femur-cost-' + node_env_ID + '.nhdr ' + \
		node_env_BoneSegOutDIR + '/bkgrd-cost-' + node_env_ID + '.nhdr ' + \
		node_env_BoneSegOutDIR + '/tibia-cost-' + node_env_ID + '.nhdr'
	print('\nAttempt command:' + command_string_buffer + '\n')
	subprocess.call(command_string_buffer, shell=True)
	text_file.write(command_string_buffer + 'n')
	# subprocess.call(env_ksrtAppDIR + '/ksrtComputeBoneLabelingCost ' + \
		# node_env_BoneSegOutDIR + '/pBone-' + node_env_ID + '.nhdr ' + \
		# node_env_BoneSegOutDIR + '/femur-fusion-' + node_env_ID + '.nhdr ' + \
		# node_env_BoneSegOutDIR + '/tibia-fusion-' + node_env_ID + '.nhdr ' + \
		# node_env_BoneSegOutDIR + '/femur-cost-' + node_env_ID + '.nhdr ' + \
		# node_env_BoneSegOutDIR + '/bkgrd-cost-' + node_env_ID + '.nhdr ' + \
		# node_env_BoneSegOutDIR + '/tibia-cost-' + node_env_ID + '.nhdr', shell=True)
	# do the segmentation
	print('Doing 3 label bone segmentation')
	command_string_buffer = env_ksrtAppDIR + '/ksrtSegmentation_3label ' + \
		node_env_BoneSegOutDIR + '/femur-cost-' + node_env_ID + '.nhdr ' + \
		node_env_BoneSegOutDIR + '/bkgrd-cost-' + node_env_ID + '.nhdr ' + \
		node_env_BoneSegOutDIR + '/tibia-cost-' + node_env_ID + '.nhdr ' + \
		node_env_BoneSegOutDIR + '/femur-seg-' + node_env_ID + '.nhdr ' + \
		node_env_BoneSegOutDIR + '/tibia-seg-' + node_env_ID + '.nhdr -g 0.5'
	print('\nAttempt command:' + command_string_buffer + '\n')
	subprocess.call(command_string_buffer, shell=True)
	text_file.write(command_string_buffer + 'n')
	# subprocess.call(env_ksrtAppDIR + '/ksrtSegmentation_3label ' + \
		# node_env_BoneSegOutDIR + '/femur-cost-' + node_env_ID + '.nhdr ' + \
		# node_env_BoneSegOutDIR + '/bkgrd-cost-' + node_env_ID + '.nhdr ' + \
		# node_env_BoneSegOutDIR + '/tibia-cost-' + node_env_ID + '.nhdr ' + \
		# node_env_BoneSegOutDIR + '/femur-seg-' + node_env_ID + '.nhdr ' + \
		# node_env_BoneSegOutDIR + '/tibia-seg-' + node_env_ID + '.nhdr -g 0.5', shell=True)
	# extract the largest component, which will be tibia/femur respectively
	print('Extracting largest connected component')
	command_string_buffer = env_ksrtAppDIR + '/ExtractLargestConnectedComponentFromBinaryImage ' + \
		node_env_BoneSegOutDIR + '/femur-seg-' + node_env_ID + '.nhdr ' + \
		node_env_BoneSegOutDIR + '/femur-seg-' + node_env_ID + '.nhdr'
	print('\nAttempt command:' + command_string_buffer + '\n')
	subprocess.call(command_string_buffer, shell=True)
	text_file.write(command_string_buffer + 'n')
	# subprocess.call(env_ksrtAppDIR + '/ExtractLargestConnectedComponentFromBinaryImage ' + \
		# node_env_BoneSegOutDIR + '/femur-seg-' + node_env_ID + '.nhdr ' + \
		# node_env_BoneSegOutDIR + '/femur-seg-' + node_env_ID + '.nhdr', shell=True)

	command_string_buffer = env_ksrtAppDIR + '/ExtractLargestConnectedComponentFromBinaryImage ' + \
		node_env_BoneSegOutDIR + '/tibia-seg-' + node_env_ID + '.nhdr ' + \
		node_env_BoneSegOutDIR + '/tibia-seg-' + node_env_ID + '.nhdr'
	print('\nAttempt command:' + command_string_buffer + '\n')
	subprocess.call(command_string_buffer, shell=True)
	text_file.write(command_string_buffer + 'n')
	# subprocess.call(env_ksrtAppDIR + '/ExtractLargestConnectedComponentFromBinaryImage ' + \
		# node_env_BoneSegOutDIR + '/tibia-seg-' + node_env_ID + '.nhdr ' + \
		# node_env_BoneSegOutDIR + '/tibia-seg-' + node_env_ID + '.nhdr', shell=True)
	# cut bones
	print('Cutting bones')
	command_string_buffer = env_ksrtAppDIR + '/ksrtCutFemur ' + \
		node_env_BoneSegOutDIR + '/tibia-seg-' + node_env_ID + '.nhdr 45 ' + \
		node_env_BoneSegOutDIR + '/tibia-seg-' + node_env_ID + '-cut.nhdr'
	print('\nAttempt command:' + command_string_buffer + '\n')
	subprocess.call(command_string_buffer, shell=True)
	text_file.write(command_string_buffer + 'n')
	# subprocess.call(env_ksrtAppDIR + '/ksrtCutFemur ' + \
		# node_env_BoneSegOutDIR + '/tibia-seg-' + node_env_ID + '.nhdr 45 ' + \
		# node_env_BoneSegOutDIR + '/tibia-seg-' + node_env_ID + '-cut.nhdr', shell=True)
	
	command_string_buffer = env_ksrtAppDIR + '/ImageMath ' + \
		node_env_BoneSegOutDIR + '/tibia-seg-' + node_env_ID + '.nhdr -mul ' + \
		node_env_BoneSegOutDIR + '/tibia-seg-' + node_env_ID + '-cut.nhdr -outfile ' + \
		node_env_BoneSegOutDIR + '/tibia-seg-' + node_env_ID + '-cut.nhdr'
	print('\nAttempt command:' + command_string_buffer + '\n')
	subprocess.call(command_string_buffer, shell=True)
	text_file.write(command_string_buffer + 'n')
	# subprocess.call(env_ksrtAppDIR + '/ImageMath ' + \
		# node_env_BoneSegOutDIR + '/tibia-seg-' + node_env_ID + '.nhdr -mul ' + \
		# node_env_BoneSegOutDIR + '/tibia-seg-' + node_env_ID + '-cut.nhdr -outfile ' + \
		# node_env_BoneSegOutDIR + '/tibia-seg-' + node_env_ID + '-cut.nhdr', shell=True)
	
	command_string_buffer = env_ksrtAppDIR + '/ksrtCutTibia ' + \
		node_env_BoneSegOutDIR + '/femur-seg-' + node_env_ID + '.nhdr 45 ' + \
		node_env_BoneSegOutDIR + '/femur-seg-' + node_env_ID + '-cut.nhdr'
	print('\nAttempt command:' + command_string_buffer + '\n')
	subprocess.call(command_string_buffer, shell=True)
	text_file.write(command_string_buffer + 'n')
	# subprocess.call(env_ksrtAppDIR + '/ksrtCutTibia ' + \
		# node_env_BoneSegOutDIR + '/femur-seg-' + node_env_ID + '.nhdr 45 ' + \
		# node_env_BoneSegOutDIR + '/femur-seg-' + node_env_ID + '-cut.nhdr', shell=True)
	
	command_string_buffer = env_ksrtAppDIR + '/ImageMath ' + \
		node_env_BoneSegOutDIR + '/femur-seg-' + node_env_ID + '.nhdr -mul ' + \
		node_env_BoneSegOutDIR + '/femur-seg-' + node_env_ID + '-cut.nhdr -outfile ' + \
		node_env_BoneSegOutDIR + '/femur-seg-' + node_env_ID + '-cut.nhdr'
	print('\nAttempt command:' + command_string_buffer + '\n')
	subprocess.call(command_string_buffer, shell=True)
	text_file.write(command_string_buffer + 'n')
	# subprocess.call(env_ksrtAppDIR + '/ImageMath ' + \
		# node_env_BoneSegOutDIR + '/femur-seg-' + node_env_ID + '.nhdr -mul ' + \
		# node_env_BoneSegOutDIR + '/femur-seg-' + node_env_ID + '-cut.nhdr -outfile ' + \
		# node_env_BoneSegOutDIR + '/femur-seg-' + node_env_ID + '-cut.nhdr', shell=True)
	text_file.close()
	break
	currentprocess += size
end = time.time()
print "Total time: %f seconds" % (end - start)
