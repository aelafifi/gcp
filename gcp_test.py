#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
gcp: Goffi's CoPier
Copyright (C) 2010, 2011  Jérôme Poisson <goffi@goffi.org>
          (c) 2011        Thomas Preud'homme <robotux@celest.fr>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import with_statement
import tempfile
import unittest
from os import getcwd, chdir, system
from shutil import rmtree
from random import randrange
from hashlib import sha1

#size shorcuts
S10K = 1024 * 10
S100K = 1024 * 100
S1M = 1024 * 1024
S10M = 1024 * 1024 * 10
S100M = 1024 * 1024 * 100


def sha1sum(filename, buf_size=4096):
    csum = sha1()
    with open(filename) as fd:
        data = fd.read(buf_size)
        while data:
            csum.update(data)
            data = fd.read(buf_size)
    return csum.digest()

#def makeRandomFile(path, size, buf_size=4096):
#    """Create a fake file
#    @param path: where the file is created
#    @param size: size of the file to create in bytes"""
#    def seq(size):
#        return ''.join(chr(randrange(256)) for i in range(size))
#    fd = open(path, 'w')
#    for byte in range(size//buf_size):
#        fd.write(seq(buf_size))
#    fd.write(seq(size%buf_size))
#    fd.close()

def makeRandomFile(path, size, buf_size=4096):
    """Create a fake file using /dev/urandom
    @param path: where the file is created
    @param size: size of the file to create in bytes"""
    source = open('/dev/urandom','r')
    dest = open(path, 'w')
    for byte in range(size//buf_size):
        dest.write(source.read(buf_size))
    dest.write(source.read(size%buf_size))
    dest.close()


class TestCopyCases(unittest.TestCase):
    """Test basic copy use cases, using gcp externally
    gcp must be available in the PATH"""
    #TODO: check journal

    def setUp(self):
        self.ori_dir = getcwd()
        self.tmp_dir = tempfile.mkdtemp()
        chdir(self.tmp_dir)

    def tearDown(self):
        chdir(self.ori_dir)
        rmtree(self.tmp_dir)
        

    def test_one_file_copy(self):
        """Copy one file and test the result"""
        makeRandomFile('file_1', S10K)
        ori_sum = sha1sum('file_1')
        ret = system("gcp file_1 file_2")
        self.assertEqual(ret,0)
        dest_sum = sha1sum('file_2')
        self.assertEqual(ori_sum, dest_sum)

    def test_one_file_copy_already_exists(self):
        """Check that an existing file is not overwritten"""
        makeRandomFile('file_1', S10K)
        makeRandomFile('file_2', S10K)
        file_2_sum = sha1sum('file_2')
        ret = system("gcp file_1 file_2")
        self.assertNotEqual(ret,0)
        file_2_sum_bis = sha1sum('file_2')
        self.assertEqual(file_2_sum, file_2_sum_bis)

    def test_one_file_copy_already_exists_force(self):
        """Check that an existing file is overwritten with --force"""
        makeRandomFile('file_1', S10K)
        makeRandomFile('file_2', S10K)
        file_1_sum = sha1sum('file_1')
        ret = system("gcp -f file_1 file_2")
        self.assertEqual(ret,0)
        file_2_sum_bis = sha1sum('file_2')
        self.assertEqual(file_1_sum, file_2_sum_bis)


if __name__ == '__main__':
    unittest.main()
