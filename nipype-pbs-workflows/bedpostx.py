"""
Copyright 2014 University of Florida. All rights reserved. 
Use of this source code is governed by the license found in the LICENSE file.

For instructions on how to use this script please refer to doc/README_bedpostx.md
"""

from nipype.workflows.dmri.fsl.dti import create_bedpostx_pipeline
import nipype.pipeline.engine
import argparse
import getpass
import os

USERNAME = getpass.getuser()
DEFAULT_BASE_DIR = os.path.join('/scratch/lfs/', USERNAME)
DEFAULT_INPUT_DIR = 'data'
OUTPUT_DIR = 'workflow'   # this directory is relative to base_dir
JOB_TEMPLATE_NAME = 'bedpostx_job.sh'


# ----------------Accepting command line argument----------------------------

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path",
    help="Path to the scratch folder, e.g. /scratch/lfs/$username",
    default=DEFAULT_BASE_DIR,
    required=False)
parser.add_argument("-d", "--data",
    help="Name of the folder in the scratch folder containing the input data",
    default=DEFAULT_INPUT_DIR,
    required=False)
parser.add_argument("-m", "--mailid",
    help="Email id to which the report and errors if any should be sent. "\
    "This is a required argument",
    default=None,
    required=False)

args = vars(parser.parse_args())

base_dir = args['path']
input_dir = os.path.join(base_dir, args['data'])
mailid = args['mailid']

if mailid is None:
    print "Error: Email address needs to be provided as an argument. Please refer README_bedpostx.md for assistance."

elif not os.path.exists(input_dir):
    print "Error: Cannot find " + input_dir + ". Please make sure that input files are located as mentioned in README_bedpostx.md."

else:
    # ------------------Generating PBS template on the fly-----------------------

    template = '''#PBS -N bedpostx_via_nipype
    #PBS -M ''' + mailid + '''
    #PBS -l nodes=1:ppn=1
    #PBS -l pmem=600mb
    #PBS -l walltime=4:00:00
    #PBS -e ''' + base_dir + '''my_job.err
    #PBS -o ''' + base_dir + '''my_job.log
    module load python/2.7.6
    module load nipype/0.8
    module load fsl/5.0.5
    '''

    with open(os.path.join(base_dir, JOB_TEMPLATE_NAME), "w") as temp_file:
        temp_file.write(template)


    # ---------------Creating nipype workflow for bedpostx-----------------------

    nipype_bedpostx = create_bedpostx_pipeline("nipype_bedpostx")

    nipype_bedpostx.inputs.inputnode.dwi = os.path.join(input_dir, 'data.nii')
    nipype_bedpostx.inputs.inputnode.mask = os.path.join(input_dir, 'nodif_brain_mask.nii')
    nipype_bedpostx.inputs.inputnode.bvecs = os.path.join(input_dir, 'bvecs')
    nipype_bedpostx.inputs.inputnode.bvals = os.path.join(input_dir, 'bvals')
    nipype_bedpostx.inputs.xfibres.n_fibres = 1
    nipype_bedpostx.inputs.xfibres.fudge = 1
    nipype_bedpostx.inputs.xfibres.burn_in = 1000
    nipype_bedpostx.inputs.xfibres.n_jumps = 1250
    nipype_bedpostx.inputs.xfibres.sample_every = 25

    workflow = nipype.pipeline.engine.Workflow(name = OUTPUT_DIR)
    workflow.add_nodes([nipype_bedpostx])
    workflow.base_dir = base_dir
    workflow.config['execution'] = {'logging': 'DEBUG'}

    result = workflow.run(plugin='PBS', plugin_args=dict(template=os.path.join(base_dir, JOB_TEMPLATE_NAME)))


    # cleaning up
    try:
        os.remove(os.path.join(base_dir, JOB_TEMPLATE_NAME))
    except OSError:
        print "Error while deleting " + os.path.join(base_dir, JOB_TEMPLATE_NAME)
