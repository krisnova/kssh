from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kssh',
    version='1.0.0',
    description='kSSH is a simple utility for managing SSH hosts and tracking aliases in an SSH config file.',
    long_description=long_description,
    url='https://github.com/kris-nova/kssh',
    author='Kris Applesauce',
    author_email='kris@nivenly.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: SSH',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='SSH, ssh, manager, management, wrapper, config, configuration, tool, utility, cli, command line, command, line',
    py_modules=["kssh"],
    entry_points={
        'console_scripts': [
            'command-name=kssh',
        ],
    },
)
