import os

import setuptools
from pip._internal.network.session import PipSession
from pip._internal.req import parse_requirements

import bigpipe_response

dir_path = os.path.dirname(os.path.realpath(__file__))
install_reqs = parse_requirements(os.path.join(dir_path, 'requirements.txt'), session=PipSession)

with open(os.path.join(dir_path, "README.md"), "r") as fh:
   long_description = fh.read()


setuptools.setup(
   name='bigpipe_response',
   version=bigpipe_response.__version__,
   description='Bigpipe, Pipelining web pages for high performance, django response object',
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://github.com/shay-te/bigpipe-response",
   setup_requires=['wheel'],
   author='Shay Tessler',
   author_email='shay.te@gmail.com',
   packages=setuptools.find_packages(),
   include_package_data=True,
   install_requires=[str(ir.requirement) for ir in install_reqs],
   license="MIT",
   classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
   ],
   python_requires='>=3.7'
)