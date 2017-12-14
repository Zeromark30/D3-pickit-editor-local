from paver.easy import *
import paver.doctools
from paver.setuputils import setup, find_packages
from setuptools import find_packages as fp

#pdata = paver.setuputils.find_package_data(package='pickit_cl', only_in_packages=False) 
pdata_include = {'pickit_cl': ['*.txt', 'data/*.txt', 'data/*.json', 'output/*.ini']}
pdata_exclude = {'pickit_cl': ['data/*.py']}

setup(
    name="pickit-cl",
    packages=['pickit_cl'],
    #package_dir={'':'pickit_cl'},
    version="0.1.0",
    author="Thomas Kersten",
    author_email="tkersten09@gmail.com",
    install_requires=[],
    scripts= ["bin/pickit-cl"],
    entry_points={
        'console_scripts': [
            'pickit-cl = pickit_cl.pickit_cl:run'
        ],
    },
    include_package_data=True,
    package_data=pdata_include,
    exclude_package_data=pdata_exclude,
    zip_safe=True,
)

@task
@needs('generate_setup', 'minilib')
def build():
    """Build the release and install it"""
    
    sh('paver bdist_egg')
    sh('paver sdist')
    
    eggdir = path('.').glob('*.egg-info')
    for p in eggdir:
        p.rmtree()
    path('build').rmtree()
    
    pass

# the pass that follows is to work around a weird bug. It looks like
# you can't compile a Python module that ends in a comment.
pass

