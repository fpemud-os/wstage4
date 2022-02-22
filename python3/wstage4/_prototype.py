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


class WindowsInstallIsoFile:

    def __init__(self):
        self._path = None
        self._osInfo = None

    @property
    def path(self):
        return self._path

    @property
    def arch(self):
        return self._osInfo["arch"]

    @property
    def category(self):
        return self._osInfo["category"]

    @property
    def editions(self):
        return self._osInfo["editions"]

    @property
    def languages(self):
        return self._osInfo["languages"]

    def _set_info(self, iso_filepath, os_info):
        self._path = iso_filepath
        self._osInfo = os_info


class StorageLayout:

    @classmethod
    def mount(cls, disk_list, base_dir):
        assert len(disk_list) > 0
        assert base_dir.startswith("/") and len(os.listdir(base_dir)) == 0

        if len(disk_list) == 1:
            from ._win_storage_layouts import StorageLayouts
            return StorageLayouts().get_storage_layout("ntfs-sys-win")._create_and_mount(disk_list, base_dir)
        else:
            assert False

    @classmethod
    def create_and_mount(cls, name, disk_list, base_dir):
        assert len(disk_list) > 0
        assert base_dir.startswith("/") and len(os.listdir(base_dir)) == 0

        from ._win_storage_layouts import StorageLayouts
        return StorageLayouts().get_storage_layout(name)._create_and_mount(boot_mode, disk_list, base_dir)

    @property
    @abc.abstractmethod
    def name(self):
        pass

    @property
    @abc.abstractmethod
    def partition_type(self):
        pass

    @property
    @abc.abstractmethod
    def base_dir(self):
        pass

    @abc.abstractmethod
    def umount_and_dispose(self):
        pass

    @abc.abstractmethod
    def get_mount_entries(self):
        pass

    @classmethod
    @abc.abstractmethod
    def _mount(cls, disk_list, base_dir):
        pass

    @classmethod
    @abc.abstractmethod
    def _create_and_mount(cls, disk_list, base_dir):
        pass


class StorageLayoutMountEntry:

    def __init__(self):
        self.mnt_point = None
        self.real_dir_path = None
        self.target = None
        self.fs_type = None
        self.mnt_opts = None


class ScriptInChroot(abc.ABC):

    @abc.abstractmethod
    def fill_script_dir(self, script_dir_hostpath):
        pass

    @abc.abstractmethod
    def get_description(self):
        pass

    @abc.abstractmethod
    def get_script(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, ScriptInChroot):
            return False
        if self.get_description() != other.get_description():
            return False
        return True

    def __ne__(self, other):
        return (not self.__eq__(other))
