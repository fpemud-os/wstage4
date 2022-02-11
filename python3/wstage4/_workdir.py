#!/usr/bin/env python3

# Copyright (c) 2020-2021 Fpemud <fpemud@sina.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import os
import stat
import pathlib
import robust_layer.simple_fops
from ._errors import WorkDirError


class WorkDir:
    """
    This class manipulates wstage4's working directory.
    """

    def __init__(self, path):
        assert path is not None

        self._MODE = 0o40700

        self._path = path
        self._qemuCfgFile = os.path.join(path, "qemu.cfg")
        self._imageFile = os.path.join(path, "disk.img")

    @property
    def path(self):
        return self._path

    @property
    def qemu_cfg_filepath(self):
        return self._qemuCfgFile

    @property
    def image_filepath(self):
        return self._imageFile

    def initialize(self):
        if not os.path.exists(self._path):
            os.mkdir(self._path, mode=self._MODE)
        else:
            self._verifyDir(True)
            robust_layer.simple_fops.truncate_dir(self._path)

    def verify_existing(self, raise_exception=None):
        assert raise_exception is not None
        if not self._verifyDir(raise_exception):
            return False
        return True

    def load_record(self, record_name, default_value=None):
        fullfn = os.path.join(self._path, record_name + ".save")
        if os.path.isfile(fullfn):
            return pathlib.Path(fullfn).read_text()
        else:
            return default_value

    def save_record(self, record_name, value):
        fullfn = os.path.join(self._path, record_name + ".save")
        with open(fullfn, "w") as f:
            f.write(value)

    def delete_record(self, record_name):
        fullfn = os.path.join(self._path, record_name + ".save")
        robust_layer.simple_fops.rm(fullfn)

    def _verifyDir(self, raiseException):
        # work directory can be a directory or directory symlink
        # so here we use os.stat() instead of os.lstat()
        s = os.stat(self._path)
        if not stat.S_ISDIR(s.st_mode):
            if raiseException:
                raise WorkDirError("\"%s\" is not a directory" % (self._path))
            else:
                return False
        if s.st_mode != self._MODE:
            if raiseException:
                raise WorkDirError("invalid mode for \"%s\"" % (self._path))
            else:
                return False
        if s.st_uid != os.getuid():
            if raiseException:
                raise WorkDirError("invalid uid for \"%s\"" % (self._path))
            else:
                return False
        if s.st_gid != os.getgid():
            if raiseException:
                raise WorkDirError("invalid gid for \"%s\"" % (self._path))
            else:
                return False
        return True
