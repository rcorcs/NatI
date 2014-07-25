# -*- coding:utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

from distutils.core import setup

__path__ = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(__path__, 'src'))

import grooveshark.version as version

setup(name=version.__short_name__,
      version=version.__version__,
      description=version.__desc_short__,
      long_description=version.__desc_long__,
      author=version.__author__,
      author_email=version.__email__,
      url=version.__website__,
      download_url=version.__download_url__,
      license='GPLv3+',
      packages=['grooveshark', 'grooveshark.classes'],
      package_dir={'': 'src'},
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: MacOS :: MacOS X', # Should work on MacOS X I think...
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Multimedia :: Sound/Audio'])
