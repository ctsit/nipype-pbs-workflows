"""
Copyright 2014 University of Florida. All rights reserved. 
Use of this source code is governed by the license found in the LICENSE file.

For instructions on how to use this script please refer to doc/README_dcm2niiconverter.md
"""

import os                                    # system functions
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pypeline engine
from nipype.interfaces.dcm2nii import Dcm2nii
import getpass
import argparse


DEFAULT_DICOM_DIR = "DICOM"
DEFAULT_OUTPUT_DIR = 'output'

# ----------------Accepting command line argument----------------------------

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path",
    help="Path to the experiment directory, e.g. /scratch/lfs/user1/DICOM",
    default=None,
    required=True)
parser.add_argument("-d", "--dicom",
    help="Name of the folder in the experiment folder containing the DICOMS",
    default=DEFAULT_DICOM_DIR,
    required=False)
parser.add_argument("-o", "--output",
    help="Name of the folder to store the output",
    default=DEFAULT_OUTPUT_DIR,
    required=False)

args = vars(parser.parse_args())

"""
Define experiment specific parameters

"""

#Specification of the folder where the dicom-files are located at
experiment_dir = args['path'] 

#Specification of a list containing the identifier of each subject
subjects_data_list = ['64-axial','6-axial','6-sagittal','64-sagittal','FLAIR','T1-1','T1-2','T2']

#Specification of the name of the dicom and output folder 
dicom_dir_name = args['dicom'] #if the path to the dicoms is: '~SOMEPATH/experiment/dicom'
data_dir_name = args['output']   #if the path to the data should be: '~SOMEPATH/experiment/data'

# param_set =[]

for subject in subjects_data_list:
    if not os.path.exists(experiment_dir + '/' + data_dir_name +'/'+subject):
        os.makedirs(experiment_dir + '/' + data_dir_name +'/'+subject)



"""
Define nodes to use
"""

#Node: Infosource - we use IdentityInterface to create our own node, to specify
#                   the list of subjects the pipeline should be executed on
infosource = pe.Node(interface=util.IdentityInterface(fields=['subject_id']),name="infosource")

infosource.iterables =  [('subject_id',subjects_data_list)]

# #Node: Infosource - we use IdentityInterface to create our own node, to specify
# #                   the list of subjects the pipeline should be executed on
# subjectsource = pe.Node(interface=util.IdentityInterface(fields=['subject_id,subject_data_id']),
                                                      # name="subjectsource")
# subjectsource.iterables = ('subject_data_id', subjects_data_list)


dcm2nii_converter = pe.Node(interface=Dcm2nii(),name='dcm2nii')
dcm2nii_converter.inputs.gzip_output = True
dcm2nii_converter.inputs.reorient_and_crop = False


# Initiation of the preparation pipeline
prepareflow = pe.Workflow(name="prepareflow")
  
# Define where the workingdir of the all_consuming_workflow should be stored at
prepareflow.base_dir = experiment_dir + '/workingdir_prepareflow'

#Define pathfinder function
def pathfinder(subject, experiment_dir, foldername):
    import os
    from glob import glob
    print subject
    subject_dir =  os.path.join(experiment_dir, subject, foldername)
    filenames = glob(subject_dir+'/IM_*')
    return filenames[0]

def output_directory(subject, experiment_dir, data_dir_name):
    import os
    return os.path.join(experiment_dir, data_dir_name,subject)

#Connect all components
prepareflow.connect([(infosource, dcm2nii_converter,[(('subject_id',pathfinder, experiment_dir, dicom_dir_name),
                                                 'source_names'),(('subject_id', output_directory, experiment_dir, data_dir_name),
                                                 'output_dir')])
                     ])

# Run pipeline and create graph
prepareflow.run(plugin='MultiProc', plugin_args={'n_procs' : 7})
