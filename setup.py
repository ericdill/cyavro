# Copyright (c) 2015 MaxPoint Interactive, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#    disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
#    products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
import numpy as np
import os

#import Cython.Compiler.Options
#Cython.Compiler.Options.annotate = True

prefix = os.getenv('PREFIX', None)
if prefix is not None:
    include_dirs = [os.path.join(prefix, 'include')]
    library_dirs = [os.path.join(prefix, 'lib')]
else:
    include_dirs = []
    library_dirs = []

include_dirs.append(np.get_include())

extensions = [
    Extension(
        'cyavro._cyavro', ['cyavro/*.pyx'],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=['avro', 'm', 'snappy'],
    )
]

version = str(os.environ.get('PKG_VERSION', "0.6.2"))


def write_version_py():
    content = """\
version = '%s'
""" % version

    filename = os.path.join(os.path.dirname(__file__), 'cyavro', 'version.py')
    with open(filename, 'w') as fo:
        fo.write(content)

write_version_py()


setup(name='cyavro',
      version=version,
      packages=['cyavro'],
      package_data={'cyavro': ['_cyavro.c', '*.pyx', '*.pxd']},
      description='Wrapper to avro-c-1.7.5',
      maintainer='MaxPoint Interactive',
      maintainer_email='marius.vanniekerk@maxpoint.com',
      author='MaxPoint Interactive',
      author_email='marius.vanniekerk@maxpoint.com',
      requires=['pandas (>=0.12)',
                'numpy (>=1.7.0)',
                'cython (>=0.19.1)'],
      ext_modules=cythonize(extensions, cython_gdb=True),
      url='https://github.com/maxpoint/cyavro',
      license='BSD',
      )
