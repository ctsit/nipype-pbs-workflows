# Login to research computing machine:

Login to your research computing machine from the terminal using your credentials as follows:
	ssh <username>@hipergator.rc.ufl.edu

# Steps to execute bedpostx_parallel script:

## Loading necessary modules

Following is the list of software modules that are required to be loaded in the research computing machine to run bedpostx:

1) Python: Python is a programming language we use to write our scripts. For more information about python please refer `https://www.python.org`

2) Nipype: Nipype is open-source neuroimaging software written in python to provide tools to analyze data using variety of different algorithms. For more information about Nipype please refer `http://nipy.sourceforge.net/nipype/`
	
3) FSL: FSL is a comprehensive library of analysis tools for FMRI, MRI,and DTI brain imaging data.

To load these software modules onto your research computing machine, please run the following commands on your terminal:


	module load python/2.7.6

	module load nipype/0.8
	
	module load fsl/5.0.5
	
## Running bedpostx_parallel.py
To run bedpostx_parallel.py script, change directory (cd) to the directory which contains the script and run the script as shown below:

	cd nipype_scripts
	
	python bedpostx_parallel.py -m <email-id>

## Usage

    Mandatory command line argument:

     - -m, --mailid: Email id to which the report and errors if any should be sent.

    Optional command line arguments:

     - -h, --help: Show the help message
     - -p, --path: Path to the scratch folder, e.g. /scratch/lfs/$username. If this is not provided then the program assumes it to be /scratch/lfs/$username
     - -d, --data: Name of the folder in the scratch folder containing the input data. If this is not provided then the program assumes the name to be "data"


#required input files:

	bvals

	bvecs

	data.nii

	nodif_brain.nii

	nodif_brain_mask.nii

Note that the above mentioned files should be present in a folder under /scratch/lfs/$username. If the name of the that folder is different from "data", please provide it as a command line argument as shown in the usage.


#output:
	workflow folder


For more information on the contents of the input files and the workflow folder, please refer `http://fsl.fmrib.ox.ac.uk/fsl/fsl4.0/fdt/fdt_bedpostx.html`
