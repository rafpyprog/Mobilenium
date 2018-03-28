import os
import re
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

version_file = os.path.join(here, 'mobilenium', '__version__.py')
with open(version_file) as init:
    version_file = init.read()
version_pattern = '[0-9]{1,2}\.[0-9]{1,2}.[0-9]{1,2}'
version = re.search(version_pattern, version_file).group()


pkgs = ['mobilenium']

# Dependencies
with open('requirements.txt') as f:
    dependencies = f.readlines()
install_requires = [t.strip() for t in dependencies]

config = dict(
    name='mobilenium',
    version=version,
    description='Mobilenium uses BrowserMob Proxy to give superpowers to Selenium.',
    long_description=open('README.rst').read(),
    author='Rafael Alves Ribeiro',
    author_email='rafael.alves.ribeiro@gmail.com',
    url='https://github.com/rafpyprog/Mobilenium.git',
    keywords='selenium browsermob proxy',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 2 - Pre-Alpha'],
    packages=pkgs,
    license='License :: OSI Approved :: MIT License',
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest',
        'pytest-cov',
    ],
)

setup(**config)
