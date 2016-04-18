from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kssh.py',
    version='1.0.7',
    description='kSSH is a simple utility for managing SSH hosts and tracking aliases in an SSH config file.',
    long_description=long_description,
    url='https://github.com/kris-nova/kssh.py',
    author='Kris Applesauce',
    author_email='kris@nivenly.com',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: System',
        'License :: OSI Approved :: MIT License',
        'Environment :: MacOS X'
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='SSH, ssh, manager, management, wrapper, config, configuration, tool, utility, cli, command line, command, line',
    py_modules=["kssh"],
    entry_points={
        'console_scripts': [
            'kssh=kssh.kssh:main',
        ],
    },
)
