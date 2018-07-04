#!/usr/bin/env python3

"""
gcp: Goffi's CoPier -- unit tests
Copyright (c) 2010, 2011  Jérôme Poisson <goffi@goffi.org>
Copyright (c) 2018        Matteo Cypriani <mcy@lm7.fr>

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

import tempfile
import unittest
from os import getcwd, chdir, system, mkdir, makedirs, listdir
from os.path import join, isdir
from shutil import rmtree
from hashlib import sha1

# gcp command. This assumes gcp is in the PATH. Alternatively, we could use
# something like this to use gcp from the current directory:
#GCP = join(getcwd(), "gcp")
GCP = 'gcp'

# Size shorcuts
S10K = 1024 * 10
S100K = 1024 * 100
S1M = 1024 * 1024
S10M = 1024 * 1024 * 10
S100M = 1024 * 1024 * 100

def sha1sum(filename, buf_size=4096):
    """Returns the SHA1 hash of a file.
    @param filename: path to the file
    @param buf_size: size of the buffer to use for calculation
    """
    csum = sha1()
    with open(filename, 'rb') as fd:
        data = fd.read(buf_size)
        while data:
            csum.update(data)
            data = fd.read(buf_size)
    return csum.digest()

def dirCheck(dir_path):
    """Recursively calculates SHA1 sums in a directory.
    @param path: path of the dir to check
    @return: a dict in the form [{filepath: sum,...}]
    """
    def recursive_sum(directory, result):
        for current_path in listdir(directory):
            full_path = join(directory, current_path)
            if isdir(full_path):
                recursive_sum(full_path, result)
            else:
                result[full_path] = sha1sum(full_path)

    result = {}
    _ori_dir = getcwd()
    chdir(dir_path)
    recursive_sum(".", result)
    chdir(_ori_dir)
    return result

#def makeRandomFile(path, size, buf_size=4096):
#    """Creates a fake file.
#    @param path: where the file is created
#    @param size: size of the file to create in bytes
#    """
#    def seq(size):
#        return ''.join(chr(random.randrange(256)) for i in range(size))
#    fd = open(path, 'w')
#    for byte in range(size//buf_size):
#        fd.write(seq(buf_size))
#    fd.write(seq(size%buf_size))
#    fd.close()

def makeRandomFile(path, size=S10K, buf_size=4096):
    """Creates a fake file using /dev/urandom.
    @param path: where the file must be created
    @param size: size of the file to create in bytes
    """
    source = open('/dev/urandom', 'rb')
    dest = open(path, 'wb')
    for _ in range(size // buf_size):
        dest.write(source.read(buf_size))
    dest.write(source.read(size % buf_size))
    dest.close()
    source.close()

def makeTestDir(path):
    """Helper method to easily create a test directory.
    @param path: where the dir must be created
    """
    for i in range(2):
        subdir = join(path,'subdir_%d' % i)
        makedirs(subdir)
        for j in range(2):
            makeRandomFile(join(subdir, 'file_%d' % j), S10K)
    for i in range(2):
        makeRandomFile(join(path,'file_%d' % i), S10K)

class TestCopyCases(unittest.TestCase):
    """Test basic copy use cases, using gcp externally.
    """
    #TODO: check journal

    def setUp(self):
        self.ori_dir = getcwd()
        self.tmp_dir = tempfile.mkdtemp()
        chdir(self.tmp_dir)

    def tearDown(self):
        chdir(self.ori_dir)
        rmtree(self.tmp_dir)

    def test_one_file_copy(self):
        """Copies one file and tests the result.
        """
        makeRandomFile('file_1', S10K)
        ori_sum = sha1sum('file_1')
        ret = system(GCP + " file_1 file_2")
        self.assertEqual(ret,0)
        dest_sum = sha1sum('file_2')
        self.assertEqual(ori_sum, dest_sum)

    def test_one_file_copy_already_exists(self):
        """Checks that an existing file is not overwritten.
        """
        makeRandomFile('file_1', S10K)
        makeRandomFile('file_2', S10K)
        file_2_sum = sha1sum('file_2')
        ret = system(GCP + " file_1 file_2")
        self.assertNotEqual(ret,0)
        file_2_sum_bis = sha1sum('file_2')
        self.assertEqual(file_2_sum, file_2_sum_bis)

    def test_one_file_copy_already_exists_force(self):
        """Checks that an existing file is overwritten with --force.
        """
        makeRandomFile('file_1', S10K)
        makeRandomFile('file_2', S10K)
        file_1_sum = sha1sum('file_1')
        ret = system(GCP + " -f file_1 file_2")
        self.assertEqual(ret,0)
        file_2_sum_bis = sha1sum('file_2')
        self.assertEqual(file_1_sum, file_2_sum_bis)

    def test_one_dir_copy(self):
        """Checks copy of a directory to a non-existent path.
        """
        makeTestDir('dir_1')
        check_1 = dirCheck('dir_1')
        ret = system(GCP + " -r dir_1 dir_2")
        self.assertEqual(ret,0)
        check_2 = dirCheck('dir_2')
        self.assertEqual(check_1, check_2)

    def test_one_dir_copy_nocopy(self):
        """Checks that a directory is not copied without the recursive option.
        """
        makeTestDir('dir_1')
        check_before = dirCheck('.')
        ret = system(GCP + " dir_1 dir_2")
        self.assertEqual(ret,0)
        check_after = dirCheck('.')
        self.assertEqual(check_before, check_after)

    def test_one_dir_copy_existing_dest(self):
        """Checks that a directory is copied inside an existing destination.
        """
        makeTestDir('dir_1')
        mkdir('dir_2')
        check_1 = dirCheck('dir_1')
        ret = system(GCP + " -r dir_1 dir_2")
        self.assertEqual(ret,0)
        self.assertEqual(listdir('dir_2'), ['dir_1'])
        check_2 = dirCheck('dir_2/dir_1')
        self.assertEqual(check_1, check_2)

    def test_mixed_copy_existing_dest(self):
        """Mixed copy (files + dir) to an existing destination.
        """
        for i in range(2):
            makeRandomFile('file_%d' % i, S10K)
            makeTestDir('dir_%d' % i)
        check_1 = dirCheck('.')
        mkdir('dest_dir')
        ret = system(GCP + " -r file_0 file_1 dir_0 dir_1 dest_dir")
        self.assertEqual(ret,0)
        check_2 = dirCheck('dest_dir')
        self.assertEqual(check_1, check_2)

    def test_mixed_copy_nonexisting_dest(self):
        """Mixed copy (files + dir) to an inexistant destination.
        /!\\ The behaviour is different than cp's! (cp doesn't copy at all,
        while gcp create the destintation directory.)
        """
        for i in range(2):
            makeRandomFile('file_%d' % i, S10K)
            makeTestDir('dir_%d' % i)
        check_1 = dirCheck('.')
        ret = system(GCP + " -r file_0 file_1 dir_0 dir_1 dest_dir")
        self.assertEqual(ret,0)
        check_2 = dirCheck('dest_dir')
        self.assertEqual(check_1, check_2)

    def test_mixed_copy_existing_dest_nonrecursive(self):
        """Non-recursive mixed copy (files + dir) to an existing destination.
        """
        for i in range(2):
            makeRandomFile('file_%d' % i, S10K)
            makeTestDir('dir_%d' % i)
        mkdir('dest_dir')
        ret = system(GCP + " file_0 file_1 dir_0 dir_1 dest_dir")
        self.assertEqual(ret,0)
        self.assertEqual(set(listdir('dest_dir')), set(['file_0', 'file_1']))
        self.assertEqual(sha1sum('file_0'), sha1sum('dest_dir/file_0'))
        self.assertEqual(sha1sum('file_1'), sha1sum('dest_dir/file_1'))

    def test_mixed_copy_nonexisting_dest_nonrecursive(self):
        """Non-recursive mixed copy (files + dir) to an inexistant destination.
        """
        for i in range(2):
            makeRandomFile('file_%d' % i, S10K)
            makeTestDir('dir_%d' % i)
        check_before = dirCheck('.')
        ret = system(GCP + " file_0 file_1 dir_0 dir_1 dest_dir")
        self.assertEqual(ret >> 8, 1)
        check_after = dirCheck('.')
        self.assertEqual(check_before, check_after)


if __name__ == '__main__':
    unittest.main()
