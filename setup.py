from distutils.core import setup
setup(
	name='nipype-pbs-workflows',
    version='1.0',
    author='https://www.ctsi.ufl.edu/research/study-development/informatics-consulting/',
    author_email='ctsit@ctsi.ufl.edu',
    description='Neuroimaging workflows writtten in nipype with a focus on PBS job scheduler',
    long_description=open('README.md').read(),
    url='https://github.com/ctsit/nipype-pbs-workflows',
    package_dir={'': 'nipype-pbs-workflows'},
    packages=[''],
)
