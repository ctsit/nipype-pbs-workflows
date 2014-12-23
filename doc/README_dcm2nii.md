# Login to research computing machine:

Login to your research computing machine from the terminal using your credentials as follows:
	ssh <username>@hipergator.rc.ufl.edu

# Steps to execute dcm2niiconverter.py script:

## Loading necessary modules

Following is the list of software modules that are required to be loaded in the research computing machine to run bedpostx:

1) Python: Python is a programming language we use to write our scripts. For more information about python please refer `https://www.python.org`

2) Nipype: Nipype is open-source neuroimaging software written in python to provide tools to analyze data using variety of different algorithms. For more information about Nipype please refer `http://nipy.sourceforge.net/nipype/`
	
3) FSL: FSL is a comprehensive library of analysis tools for FMRI, MRI,and DTI brain imaging data.

4) MRIcron: provides dcm2nii for the nipype, which attempts to convert images from the proprietary scanner format to the NIfTI format used by brain imaging tools.

To load these software modules onto your research computing machine, please run the following commands on your terminal:


	module load python/2.7.6

	module load nipype/0.8
	
	module load fsl/5.0.5

	module load mricron/201306
	
## Running dcm2niiconverter.py
To run dcm2niiconverter.py script, change directory (cd) to the directory which contains the script and run the script as shown below:

	cd nipype_scripts
	
	python dcm2niiconverter.py -p /scratch/lfs/<your-username>/<name-of-the-folder-in-the-experiment-folder-containing-the-dicoms>

	(e.g.: python dcm2niiconverter.py -p /scratch/lfs/user1/DICOM)

## Usage

    Mandatory command line argument:

     - -p, --path: Full path to the experiment folder
                   e.g.: /scratch/lfs/user1/DICOM

    Optional command line arguments:

     - -h, --help: Show the help message
     - -d, --data: Name of the folder in the experiment folder containing the DICOMS.
                   If this is not provided then the program assumes it to be "DICOM".
     - -o, --output: Name of the folder to store the output.
                     If this is not provided the the program assumes it to be "output".


#required input files:

	+ DICOM
    |--6-axial
    |--6-sagittal
    |--64-axial
    |--64-sagittal
    |--FLAIR
    |--T1-1
    |--T1-2
    |__T2

Note that the above mentioned files should be present in a folder under /scratch/lfs/$username.


#output:

	+ output
    |--6-axial
    |--6-sagittal
    |--64-axial
    |--64-sagittal
    |--FLAIR
    |--T1-1
    |--T1-2
    |__T2
