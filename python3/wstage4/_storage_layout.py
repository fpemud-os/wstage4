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
import abc
from ._const import Category
from ._const import BootMode


class StorageLayout:

    @classmethod
    def mount(cls, name, disk_list, base_dir):
        assert len(disk_list) > 0
        assert base_dir.startswith("/") and len(os.listdir(base_dir)) == 0
        return cls._getSubClass(name)._mount(disk_list, base_dir)

    @classmethod
    def create_and_mount(cls, name, disk_list, base_dir):
        assert len(disk_list) > 0
        assert base_dir.startswith("/") and len(os.listdir(base_dir)) == 0
        return cls._getSubClass(name)._create_and_mount(disk_list, base_dir)

    @abc.abstractmethod
    @property
    def name(self):
        pass

    @abc.abstractmethod
    @property
    def base_dir(self):
        pass

    @abc.abstractmethod
    def umount_and_dispose(self):
        pass

    @abc.abstractmethod
    def get_mount_entries(self):
        pass

    @abc.abstractmethod
    def _mount(self, disk_list, base_dir):
        pass

    @abc.abstractmethod
    def _create_and_mount(self, disk_list, base_dir):
        pass

    @staticmethod
    def _getSubClass(name):
        d = {
            "fat-win": StorageLayoutFatWin,
            "fat-win-data": None,                                       # FIXME
            "ntfs-win": StorageLayoutNtfsWin,
            "ntfs-win-data": None,                                      # FIXME
            "ntfs-sys-win": StorageLayoutNtfsSysWin,
            "ntfs-sys-win-data": None,                                  # FIXME
            "ntfs-sys-msr-win": None,                                   # FIXME
            "ntfs-sys-msr-win-data": None,                              # FIXME
        }
        ret = d[name]
        assert ret is not None
        return ret


class StorageLayoutFatWin(StorageLayout):

    """single FAT32 partition in single harddisk"""

    @property
    def name():
        return "fat-win"

    @property
    def base_dir(self):
        pass

    def _mount(self, disk_list, base_dir):
        assert len(disk_list) == 1
        Util.initializeDisk(hdd, Util.diskPartTableMbr, [
            ("*", Util.fsTypeExt4),
        ])


    def _create_and_mount(self, disk_list, base_dir):
        pass

class StorageLayoutNtfsWin(StorageLayout):

    """single NTFS partition in single harddisk"""

    @property
    def name():
        return "ntfs-win"

    @property
    def base_dir(self):
        pass


class StorageLayoutNtfsSysWin(StorageLayout):

    """System Reserved partition(NTFS) + windows partition(NTFS) in single harddisk"""

    @property
    def name():
        return "sys-win"

    @property
    def base_dir(self):
        pass


class StorageLayoutNtfsSysMsrWin(StorageLayout):

    """System Reserved partition(NTFS) + MSR partition(FAT32) + windows partition(NTFS) in single harddisk, for EFI boot"""

    @property
    def name():
        return "sys-msr-win"

    @property
    def base_dir(self):
        pass


# There should be:
#   ntfs-multi-vol: multiple harddisk in spanned volume (soft raid)
#   ntfs-multi-vol: multiple harddisk in stripped volume (soft raid)

driveC = "C:"
driveD = "D:"
driveReserve = "reserve"
