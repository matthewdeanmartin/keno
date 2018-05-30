#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os
import sys
from shutil import rmtree

# WHAT A MESS.
from distutils.core import setup, Command

from setuptools import find_packages #, setup, Command

PROJECT_NAME = "keno"

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()
about = {}
with open(os.path.join(here, PROJECT_NAME, "__version__.py")) as f:
    exec (f.read(), about)
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()
required = [
]


# https://pypi.python.org/pypi/stdeb/0.8.5#quickstart-2-just-tell-me-the-fastest-way-to-make-a-deb
class DebCommand(Command):
    """Support for setup.py deb"""
    description = 'Build and publish the .deb package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'deb_dist'))
        except FileNotFoundError:
            pass
        self.status(u'Creating debian mainfest…')
        os.system(
            'python setup.py --command-packages=stdeb.command sdist_dsc -z artful --package3=' + PROJECT_NAME
            # --depends3=python3-virtualenv-clone'
        )
        self.status(u'Building .deb…')
        os.chdir('deb_dist/pipenv-{0}'.format(about['__version__']))
        os.system('dpkg-buildpackage -rfakeroot -uc -us')


class UploadCommand(Command):
    """Support setup.py publish."""
    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except FileNotFoundError:
            pass
        self.status('Building Source distribution…')
        os.system('{0} setup.py sdist'.format(sys.executable))

        self.status('Not uploading to PyPi, not tagging github…')
        self.status('Uploading the package to PyPi via Twine…')

        # os.system('twine upload dist/*')
        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')
        sys.exit()


setup(
    name=PROJECT_NAME,
    version=about['__version__'],
    description='MD Keno Simulator',
    long_description=long_description,
    # markdown is not supported. Easier to just convert md to rst with pandoc
    # long_description_content_type='text/markdown',
    author='Matthew Martin',
    author_email='matthew.martin@bm.com',
    url='https://github.com/matthewdeanmartin/' + PROJECT_NAME,
    packages=find_packages(exclude=['test']),
    entry_points={
        'console_scripts': [
            # 'pipenv=pipenv:cli',
        ]
    },
    install_requires=required,
    extras_require={},
    include_package_data=True,
    license='See git repo',
    keywords="ui",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    cmdclass={'upload': UploadCommand, 'deb': DebCommand},
    # setup_cfg=True,
    setup_requires=['pbr'],
    pbr=True,

    data_files=[]
)