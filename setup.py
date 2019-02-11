# -*- coding: utf-8 -*-
from os import path
from setuptools import setup
# from setuptools import find_packages

NAME = 'pcdhit'
MODULES = [
    'pcdhit',
]
PACKAGES = []
VERSION_FILE = 'version.json'
SETUP_REQUIRES = []
INSTALL_REQUIRES = [
    'lilbio @ http://github.com/simomarsili/lilbio/archive/v0.6.tar.gz']
INSTALL_REQUIRES = [
    # # this is an example of URL based requirement (see PEP508):
    # 'repo @ http://github.com/user/repo/asrchive/master.tar.gz',
]
EXTRAS_REQUIRES = {'test': ['pytest']}


def get_version(source):
    """ Retrieve version number."""
    import json
    with open(source, 'r') as fp:
        version_data = json.load(fp)
    try:
        return version_data['version']
    except KeyError:
        # no version number in version.json
        raise KeyError("check version file: no version number")


def get_long_description(here):
    """Get the long description from the README file."""
    import codecs
    with codecs.open(path.join(here, 'README.rst'), encoding='utf-8') as _rf:
        return _rf.read()


HERE = path.abspath(path.dirname(__file__))
VERSION = get_version(path.join(HERE, VERSION_FILE))
LONG_DESCRIPTION = get_long_description(HERE)

setup(
    name=NAME,
    version=VERSION,
    description='A template project with packages',
    long_description=LONG_DESCRIPTION,
    author='Simone Marsili',
    author_email='simo.marsili@gmail.com',
    url='https://github.com/simomarsili/' + NAME,
    py_modules=MODULES,
    packages=PACKAGES,
    # packages=find_packages(exclude=['tests']),
    package_data={'': ['LICENSE.txt', 'README.rst', 'requirements.txt']},
    include_package_data=True,
    setup_requires=SETUP_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRES,
    license='BSD 3-Clause',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
