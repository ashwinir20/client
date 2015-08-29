#!/usr/bin/env python
# ----------------------------------------------------------------------- #
# Copyright 2008-2010, Gregor von Laszewski                               #
# Copyright 2010-2013, Indiana University                                 #
# #
# Licensed under the Apache License, Version 2.0 (the "License"); you may #
# not use this file except in compliance with the License. You may obtain #
# a copy of the License at                                                #
#                                                                         #
# http://www.apache.org/licenses/LICENSE-2.0                              #
#                                                                         #
# Unless required by applicable law or agreed to in writing, software     #
# distributed under the License is distributed on an "AS IS" BASIS,       #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.#
# See the License for the specific language governing permissions and     #
# limitations under the License.                                          #
# ------------------------------------------------------------------------#
from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from setuptools.command.install import install
import os
import shutil
import sys

try:
    import cloudmesh_base
    print ("Using cloudmesh_base version:", cloudmesh_base.__version__)
except:
    # os.system("pip install cloudmesh_base")
    os.system("pip install git+https://github.com/cloudmesh/base.git")

from cloudmesh_base.util import banner
from cloudmesh_base.util import path_expand
from cloudmesh_base.Shell import Shell
from cloudmesh_base.util import auto_create_version
from cloudmesh_base.setup import parse_requirements, os_execute, get_version_from_git

version = get_version_from_git()

banner("Installing Cloudmesh_client {:}".format(version))

requirements = parse_requirements('requirements.txt')


auto_create_version("cloudmesh_client", version, filename="version.py")
        
class UploadToPypi(install):
    """Upload the package to pypi. -- only for Maintainers."""

    description = __doc__

    def run(self):
        auto_create_version("cloudmesh_client", version, filename="version.py")
        os.system("make clean")
        commands = """
            python setup.py install
            python setup.py bdist_wheel            
            python setup.py sdist --format=bztar,zip upload
            """
        os_execute(commands)    

class InstallBase(install):
    """Install the cloudmesh_client package."""

    description = __doc__

    def run(self):
        banner("Install readline")
        commands = """
            easy_install readline
            """
        os_execute(commands)    
        import cloudmesh_client
        banner("Install Cloudmesh_client {:}".format(version))
        install.run(self)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


home = os.path.expanduser("~")

#home + '/.cloudmesh'
#print [ (home + '/.cloudmesh/' + d, [os.path.join(d, f) for f in files]) for d, folders, files in os.walk('etc')],
#sys.exit()

data_files= [ (home + '/.cloudmesh/' + d.lstrip('cloudmesh_client/'),
                [os.path.join(d, f) for f in files]) for d, folders, files in os.walk('cloudmesh_client/etc')]


import fnmatch
import os

matches = []
for root, dirnames, filenames in os.walk('cloudmesh_client/etc'):
  for filename in fnmatch.filter(filenames, '*'):
    matches.append(os.path.join(root, filename).lstrip('cloudmesh_client/'))
data_dirs = matches

#
# Hack because for some reason requirements does not work
#
# os.system("pip install -r requirements.txt")

class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


APP = ['cloudmesh_client/shell.py']
OPTIONS = {'argv_emulation': True}
            
setup(
#    setup_requires=['py2app'],
#    options={'py2app': OPTIONS},
#    app=APP,
    version=version,
    name="cloudmesh_client",
    description="cloudmesh_client - A dynamic CMD shell with plugins",
    long_description=read('README.rst'),
    license="Apache License, Version 2.0",
    author="Gregor von Laszewski",
    author_email="laszewski@gmail.com",
    url="https://github.com/cloudmesh/cloudmesh_client",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering",
        "Topic :: System :: Clustering",
        "Topic :: System :: Distributed Computing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Console"
    ],
    keywords="cloud cmd commandshell plugins",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    data_files= data_files,
    package_data={'cloudmesh_client': data_dirs},
    #entry_points={
    #    'console_scripts': [
    #        'cm = cloudmesh_client.shell:main',
    #    ],
    #},
    tests_require=['tox'],
    cmdclass={
        'install': InstallBase,
        'pypi': UploadToPypi,
        'test': Tox
    },
    #dependency_links =
    #    ['git+https://github.com/cloudmesh/base.git@sh']
)
