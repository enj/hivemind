
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

subprocess.call('/home/sdmoore/.ksrt_profile', shell=True)

# subprocess.call('export HOMEDIR=/home/sdmoore/updatedKSRT', shell=True)

# subprocess.call('export KSRT_SRC="$HOMEDIR"/ksrt', shell=True)
# subprocess.call('export scriptDIR="$KSRT_SRC"/script_SKI10/scripts', shell=True)
# subprocess.call('export DataDIR="$HOMEDIR"/dataNotBackedUp/SKI10', shell=True)
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

# command_string_buffer = 'echo $ksrtAppDIR/ImageMath "$DataDIROut"/"$ID"/preprocess/image-"$ID"-correct.nhdr -sub "$DataDIROut"/"$ID"/preprocess/image-"$ID"-correct.nhdr -outfile "$CartilageSegOutDIR"/fem-fusion-"$ID".nhdr -type float'
# subprocess.call(command_string_buffer, shell=True)
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


# env_test_trainingFILE_filepath = '/home/sdmoore/updatedKSRT/ksrt/script_SKI10/Test.txt'
# env_1_trainingFILE_filepath = '/home/sdmoore/updatedKSRT/ksrt/script_SKI10/Train_1.txt'
# env_20_trainingFILE_filepath = '/home/sdmoore/updatedKSRT/ksrt/script_SKI10/Train_20.txt'
# env_ALL_trainingFILE_filepath = '/home/sdmoore/updatedKSRT/ksrt/script_SKI10/Train.txt'

# env_trainingFILE_filepath = env_test_trainingFILE_filepath;


list_row = []
with open(env_trainingFILE, 'r') as csvfile:
# with open(env_atlasFILE, 'r') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ')
	for row in spamreader:
		# current_string = string.split(row)
		# list_row = string.split(row)
		list_row.append(row) 
		# list_ID.append(row[0])
		# list_FLIP.append(row[1])
		
# create list of comparison examples to be compared with
comparison_row = []
with open(env_atlasFILE, 'r') as csvfile:
	spamreader_comparison = csv.reader(csvfile, delimiter=' ')
	for row in spamreader_comparison:
		comparison_row.append(row) 

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
start = time.time()

# rank = 0
# size = 1
# currentprocess = rank;
# start = time.time()


while currentprocess<len(list_row):
	
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

	list_string = list_row[currentprocess]
	# list_string = string.split(setname)
	node_env_ID = list_string[0]
	node_env_FLIP = list_string[1]
	
	
	# Performs the segmentations of femur and the tibia for the id $ID
	print('Read: ID=' + node_env_ID + ' and flip=' + node_env_FLIP)
	
	# output_dirpath = env_DataDIROut + '/'
	# output_bone_segmentation_dirpath = env_DataDIROut + '/bone_segmentation/'
	# output_moved_bone_atlas_dirpath = env_DataDIROut + '/moved_bone_atlas/'
	# output_cartilage_segmentation_dirpath = env_DataDIROut + '/cartilage_segmentation/'
	
	node_env_DataDIROut = env_DataDIROut + '/' + node_env_ID
	env_BoneSegOutDIR = env_DataDIROut + '/' + node_env_ID + '/bone_segmentation'
	env_BoneRegOutDIR = env_DataDIROut + '/' + node_env_ID + '/moved_bone_atlas'
	env_CartilageSegOutDIR = env_DataDIROut + '/' + node_env_ID + '/cartilage_segmentation'
	
	checkcreatedir(env_DataDIROut)
	checkcreatedir(env_BoneSegOutDIR)
	checkcreatedir(env_BoneRegOutDIR)
	checkcreatedir(env_CartilageSegOutDIR)
	
	# Performs the segmentations of femoral and the tibial cartilage for the id $ID
	print('Running DoCartilageSegmentationForID for ID = ' + node_env_ID)
	if checkfile(env_CartilageSegOutDIR + '/result-orig-' + node_env_ID + '.mhd'):
		print('File ' + env_CartilageSegOutDIR + '/result-orig-' + node_env_ID + '.mhd already exists.')
		print('Not recomputing.')
		print('Delete the file if you want to force recomputation.')
	# create two zero images
	print('Creating empty image for femoral cartilage fusion: ' + env_CartilageSegOutDIR + '/fem-fusion-' + node_env_ID + '.nhdr')
	subprocess.call(env_ksrtAppDIR + '/ImageMath ' + \
		node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct.nhdr -sub '+ \
		node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct.nhdr -outfile '+ \
		env_CartilageSegOutDIR + '/fem-fusion-' + node_env_ID + '.nhdr -type float', shell=True)
	# print('\nAttempt command:' + command_string_buffer + '\n')
	# subprocess.call(command_string_buffer, shell=True)
	# subprocess.call(env_ksrtAppDIR + '/ImageMath ' + \
		# env_DataDIROut + '/' + node_env_ID + '/preprocess/image-' + node_env_ID + '-correct.nhdr -sub '+ \
		# env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct.nhdr -outfile '+ \
		# env_CartilageSegOutDIR + '/fem-fusion-' + node_env_ID + '.nhdr -type float', shell=True)
	print('Creating empty image for tibial cartilage fusion: ' + env_CartilageSegOutDIR + '/tib-fusion-' + node_env_ID + '.nhdr')
	subprocess.call(env_ksrtAppDIR + '/ImageMath '+ \
		node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct.nhdr -sub '+ \
		node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct.nhdr -outfile '+ \
		env_CartilageSegOutDIR + '/tib-fusion-' + node_env_ID + '.nhdr -type float', shell=True)
	# print('\nAttempt command:' + command_string_buffer + '\n')
	# subprocess.call(command_string_buffer, shell=True)
	# subprocess.call(env_ksrtAppDIR + '/ImageMath '+ \
		# env_DataDIROut + '/' + node_env_ID + '/preprocess/image-' + node_env_ID + '-correct.nhdr -sub '+ \
		# env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct.nhdr -outfile '+ \
		# env_CartilageSegOutDIR + '/tib-fusion-' + node_env_ID + '.nhdr -type float	', shell=True)

	var_n=0
	var_n_all=0
	# if there is already patch data, remove it
	if checkfile(env_CartilageSegOutDIR + '/patch-' + node_env_ID + '.txt'):
		subprocess.call('rm' + env_CartilageSegOutDIR + '/patch-' + node_env_ID + '.txt', shell=True)

	# loop over all the atlas files to do cartilage segmentations
	for comparison_string in comparison_row:
		comparison_ID = comparison_string[0]
		# comparison_FLIP = comparison_string[1]
		 
		env_BoneSegOutDIR_A = env_DataDIROut + '/' + comparison_ID + '/bone_segmentation'

		# computing affine registration
		print('Affinely registering femur bone ' + comparison_ID + ' to ' + node_env_ID)

		# TODO: not sure if this cutting is such a good idea for the registration, needs to be revisited
		subprocess.call(env_ksrtAppDIR + '/ksrtComputeAffineRegistration ' + \
			env_BoneSegOutDIR + '/femur-seg-' + node_env_ID + '-cut.nhdr ' + \
			env_BoneSegOutDIR_A + '/femur-seg-' + comparison_ID + '-cut.nhdr --metric SSD ' + \
			env_BoneRegOutDIR + '/femur-' + node_env_ID + '-' + comparison_ID + '.nhdr ' + \
			env_BoneRegOutDIR + '/affine-femur-' + node_env_ID + '-' + comparison_ID + '.tfm', shell=True)
		subprocess.call(env_ksrtAppDIR + '/ksrtComputeAffineRegistration ' + \
			env_BoneSegOutDIR + '/tibia-seg-' + node_env_ID + '-cut.nhdr ' + \
			env_BoneSegOutDIR_A + '/tibia-seg-' + comparison_ID + '-cut.nhdr --metric SSD ' + \
			env_BoneRegOutDIR + '/tibia-' + node_env_ID + '-' + comparison_ID + '.nhdr ' + \
			env_BoneRegOutDIR + '/affine-tibia-' + node_env_ID + '-' + comparison_ID + '.tfm', shell=True)

		# TODO: Maybe add B-spline here??
		var_n_all = var_n_all + 1
		affine_femur_file_flag = checkfile(env_BoneRegOutDIR + '/affine-femur-' + node_env_ID + '-' + comparison_ID + '.tfm') # -f
		affine_tibia_file_flag = checkfile(env_BoneRegOutDIR + '/affine-tibia-' + node_env_ID + '-' + comparison_ID + '.tfm') # a -f 
		if affine_femur_file_flag and affine_tibia_file_flag:
			var_n = var_n + 1

			# for femur
			subprocess.call(env_ksrtAppDIR + '/ksrtApplyAffineTransform ' + \
				env_BoneRegOutDIR + '/affine-femur-' + node_env_ID + '-' + comparison_ID + '.tfm ' + \
				env_DataDIROut + '/' + comparison_ID + '/preprocess/fem-' + comparison_ID + '.nhdr ' + \
				node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr ' + \
				env_BoneRegOutDIR + '/fem-' + node_env_ID + '-' + comparison_ID + '.nhdr', shell=True)

			# for tibia
			subprocess.call(env_ksrtAppDIR + '/ksrtApplyAffineTransform ' + \
				env_BoneRegOutDIR + '/affine-tibia-' + node_env_ID + '-' + comparison_ID + '.tfm ' + \
				env_DataDIROut + '/' + comparison_ID + '/preprocess/tib-' + comparison_ID + '.nhdr ' + \
				node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr ' + \
				env_BoneRegOutDIR + '/tib-' + node_env_ID + '-' + comparison_ID + '.nhdr', shell=True)

			# now add it to the fusion file
			subprocess.call(env_ksrtAppDIR + '/ImageMath ' + \
				env_CartilageSegOutDIR + '/fem-fusion-' + node_env_ID + '.nhdr -add ' + \
				env_BoneRegOutDIR + '/fem-' + node_env_ID + '-' + comparison_ID + '.nhdr -outfile ' + \
				env_CartilageSegOutDIR + '/fem-fusion-' + node_env_ID + '.nhdr -type float', shell=True)
			subprocess.call(env_ksrtAppDIR + '/ImageMath ' + \
				env_CartilageSegOutDIR + '/tib-fusion-' + node_env_ID + '.nhdr -add ' + \
				env_BoneRegOutDIR + '/tib-' + node_env_ID + '-' + comparison_ID + '.nhdr -outfile ' + \
				env_CartilageSegOutDIR + '/tib-fusion-' + node_env_ID + '.nhdr -type float', shell=True)
			# creating patch information
			subprocess.call(env_ksrtAppDIR + '/ksrtApplyAffineTransform ' + \
				env_BoneRegOutDIR + '/affine-femur-' + node_env_ID + '-' + comparison_ID + '.tfm ' + \
				env_DataDIROut + '/' + comparison_ID + '/preprocess/image-' + comparison_ID + '-correct-scale.nhdr ' + \
				node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr ' + \
				env_BoneRegOutDIR + '/mri-femur-' + node_env_ID + '-' + comparison_ID + '.nhdr', shell=True)
			subprocess.call(env_ksrtAppDIR + '/ksrtApplyAffineTransform ' + \
				env_BoneRegOutDIR + '/affine-tibia-' + node_env_ID + '-' + comparison_ID + '.tfm ' + \
				env_DataDIROut + '/' + comparison_ID + '/preprocess/image-' + comparison_ID + '-correct-scale.nhdr ' + \
				node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-smooth.nhdr ' + \
				env_BoneRegOutDIR + '/mri-tibia-' + node_env_ID + '-' + comparison_ID + '.nhdr', shell=True)
			env_1 = env_BoneRegOutDIR + '/mri-femur-' + node_env_ID + '-' + comparison_ID + '.nhdr'
			env_2 = env_BoneRegOutDIR + '/fem-' + node_env_ID + '-' + comparison_ID + '.nhdr'
			env_3 = env_BoneRegOutDIR + '/mri-tibia-' + node_env_ID + '-' + comparison_ID + '.nhdr'
			env_4 = env_BoneRegOutDIR + '/tib-' + node_env_ID + '-' + comparison_ID + '.nhdr'
			
			subprocess.call('echo ' + env_1 + ' ' + env_2 + ' ' + env_3 + ' ' + env_4 + ' >> ' + \
				env_CartilageSegOutDIR + '/patch-' + node_env_ID + '.txt', shell=True)
	print('Registered ' + var_n + '/' + var_n_all + ' images')

	# computing the probability maps for femoral and for tibial cartilage
	print('Computing the probability maps for femoral and tibial cartilage')
	subprocess.call(env_ksrtAppDIR + '/ImageMath ' + \
		env_CartilageSegOutDIR + '/fem-fusion-' + node_env_ID + '.nhdr -constOper 3,' + var_n + ' -outfile ' + \
		env_CartilageSegOutDIR + '/fem-fusion-' + node_env_ID + '.nhdr -type float', shell=True)
	subprocess.call(env_ksrtAppDIR + '/ImageMath ' + \
		env_CartilageSegOutDIR + '/tib-fusion-' + node_env_ID + '.nhdr -constOper 3,' + var_n + ' -outfile ' + \
		env_CartilageSegOutDIR + '/tib-fusion-' + node_env_ID + '.nhdr -type float', shell=True)

	# computing the patch information
	print('Computing the patch information')
	subprocess.call(env_ksrtAppDIR + '/ksrtPatchBasedLabelFusion ' + \
		node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale.nhdr ' + \
		env_CartilageSegOutDIR + '/patch-' + node_env_ID + '.txt ' + \
		env_CartilageSegOutDIR + '/fem-fusion-' + node_env_ID + '-patch.nhdr ' + \
		env_CartilageSegOutDIR + '/tib-fusion-' + node_env_ID + '-patch.nhdr --patchSize 2 --neighborhoodSize 2 --nearestNeighbors 1', shell=True)

	# scaling the image for SVM
	print('Scaling the image')
	subprocess.call(env_ksrtAppDIR + '/ImageMath ' + \
		node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale.nhdr -constOper 2,300 -outfile ' + \
		node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-30000.nhdr', shell=True)

	# extract the features used for the SVM classification
	print('Extracting features for SVM')
	subprocess.call(env_ksrtAppDIR + '/ksrtExtractTestingFeatures_SVM ' + \
		node_env_DataDIROut + '/preprocess/image-' + node_env_ID + '-correct-scale-30000.nhdr ' + \
		env_CartilageSegOutDIR + '/fem-fusion-' + node_env_ID + '.nhdr ' + \
		env_CartilageSegOutDIR + '/tib-fusion-' + node_env_ID + '.nhdr --scales 0.39,0.78,1.0 --threshold 0.0 ' + \
		env_svmOutDIR + '/f-' + node_env_ID, shell=True)

	# do prediction using svm
	print('Performing SVM prediction')
	subprocess.call(env_svmDIR + '/svm-predict -b 1 ' + \
		env_svmOutDIR + '/f-' + node_env_ID + ' ' + \
		env_svmOutDIR + '/train_new_small.model ' + \
		env_svmOutDIR + '/p-' + node_env_ID, shell=True)

	# compute probabilites based on SVM
	print('Computing probabilities based on SVM')
	subprocess.call(env_ksrtAppDIR + '/ksrtComputeClassificationProbabilities_SVM ' + \
		env_CartilageSegOutDIR + '/fem-fusion-' + node_env_ID + '.nhdr ' + \
		env_CartilageSegOutDIR + '/tib-fusion-' + node_env_ID + '.nhdr ' + \
		env_svmOutDIR + '/p-' + node_env_ID + ' ' + \
		env_CartilageSegOutDIR + '/pFem-' + node_env_ID + '-svm.nhdr ' + \
		env_CartilageSegOutDIR + '/pTib-' + node_env_ID + '-svm.nhdr -t 0.0', shell=True)

	# compute normals
	print('Computing normals')
	subprocess.call(env_ksrtAppDIR + '/ksrtComputeNormalDirection ' + \
		env_BoneSegOutDIR + '/femur-seg-' + node_env_ID + '.nhdr ' + \
		env_BoneSegOutDIR + '/tibia-seg-' + node_env_ID + '.nhdr ' + \
		env_BoneSegOutDIR + '/nx-' + node_env_ID + '.nhdr ' + \
		env_BoneSegOutDIR + '/ny-' + node_env_ID + '.nhdr ' + \
		env_BoneSegOutDIR + '/nz-' + node_env_ID + '.nhdr -u 1,1,1', shell=True)

	# compute the overall labeling cost to be used for the cartilage segmentation
	print('Computing overall labeling cost')
	subprocess.call(env_ksrtAppDIR + '/ksrtComputeCartilageLabelingCost ' + \
		env_CartilageSegOutDIR + '/pFem-' + node_env_ID + '-svm.nhdr ' + \
		env_CartilageSegOutDIR + '/pTib-' + node_env_ID + '-svm.nhdr ' + \
		env_CartilageSegOutDIR + '/fem-fusion-' + node_env_ID + '-patch.nhdr ' + \
		env_CartilageSegOutDIR + '/tib-fusion-' + node_env_ID + '-patch.nhdr ' + \
		env_CartilageSegOutDIR + '/fem-cost-' + node_env_ID + '.nhdr ' + \
		env_CartilageSegOutDIR + '/bkg-cost-' + node_env_ID + '.nhdr ' + \
		env_CartilageSegOutDIR + '/tib-cost-' + node_env_ID + '.nhdr', shell=True)

	# perform the anisotropic segmentation
	print('Performing anisotropic 3 label segmentation')
	subprocess.call(env_ksrtAppDIR + '/ksrtSegmentation_3label_anisotropic ' + \
		env_CartilageSegOutDIR + '/fem-cost-' + node_env_ID + '.nhdr ' + \
		env_CartilageSegOutDIR + '/bkg-cost-' + node_env_ID + '.nhdr ' + \
		env_CartilageSegOutDIR + '/tib-cost-' + node_env_ID + '.nhdr ' + \
		env_BoneSegOutDIR + '/nx-' + node_env_ID + '.nhdr ' + \
		env_BoneSegOutDIR + '/ny-' + node_env_ID + '.nhdr ' + \
		env_BoneSegOutDIR + '/nz-' + node_env_ID + '.nhdr ' + \
		env_CartilageSegOutDIR + '/fem-seg-' + node_env_ID + '-svm-patch-1.0-0.1.nhdr ' + \
		env_CartilageSegOutDIR + '/tib-seg-' + node_env_ID + '-svm-patch-1.0-0.1.nhdr -g 1.0 -a 0.1', shell=True)

	# merge the segmentation labels
	print('Merging the segmentation labels')
	subprocess.call(env_ksrtAppDIR + '/ksrtMergeSegmentations ' + \
		env_BoneSegOutDIR + '/femur-seg-' + node_env_ID + '.nhdr ' + \
		env_CartilageSegOutDIR + '/fem-seg-' + node_env_ID + '-svm-patch-1.0-0.1.nhdr ' + \
		env_BoneSegOutDIR + '/tibia-seg-' + node_env_ID + '.nhdr ' + \
		env_CartilageSegOutDIR + '/tib-seg-' + node_env_ID + '-svm-patch-1.0-0.1.nhdr ' + \
		env_CartilageSegOutDIR + '/result-' + node_env_ID + '-svm-patch-1.0-0.1.nhdr', shell=True)

	# flip the result back if needed
	print('Flipping the segmentation result back if needed')
	subprocess.call(env_ksrtAppDIR + '/ksrtFlip ' + \
		env_CartilageSegOutDIR + '/result-' + node_env_ID + '-svm-patch-1.0-0.1.nhdr -f 0,0,' + node_env_FLIP + ' ' + \
		env_CartilageSegOutDIR + '/result-orig-' + node_env_ID + '.mhd -c 0', shell=True)
	currentprocess += size
end = time.time()
print "Total time: %f seconds" % (end - start)
