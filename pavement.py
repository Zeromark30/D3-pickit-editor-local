from paver.easy import *
import paver.doctools
from paver.setuputils import setup
from pathlib import Path


setup(
    name="pickit-cl",
    packages=['pickit-cl/',],
    version="0.1.0",
    author="Thomas Kersten",
    author_email="tkersten09@gmail.com",
    install_requires=[],
    scripts= ["bin/pickit-cl"],
    entry_points={
        'console_scripts': [
            'pickit-cl = pickit-cl.pickit-cl:run'
        ],
    },
)

@task
@needs('generate_setup', 'minilib')
def makeSetup():
    """Overrides sdist to make sure that our setup.py is generated."""
    #eggdir = Path('THz.egg-info')
    #eggdir.rmtree()
    
    pass


# the pass that follows is to work around a weird bug. It looks like
# you can't compile a Python module that ends in a comment.
pass

