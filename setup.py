from setuptools import setup, find_packages

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
    zip_safe=False,
    include_package_data=True,
    package_data=pdata_include,
    exclude_package_data=pdata_exclude
)