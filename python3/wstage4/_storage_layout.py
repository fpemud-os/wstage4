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


import abc
from ._const import Category
from ._const import BootMode


class StorageLayout:

    BOOT_MODE_BIOS = 1
    BOOT_MODE_EFI = 2

    @staticmethod
    def get_storage_layout(layout_name, base_dir):
        pass

    @staticmethod
    def mount_storage_layout(layout_name, base_dir):
        pass

    @classmethod
    def create_and_mount_storage_layout(cls, layout_name, boot_mode, base_dir):
        return cls._getSubClassDict(layout_name).create_and_mount(boot_mode, base_dir)

    def __init__(self, name, boot_mode, base_dir):
        self._name = name
        self._boot_mode = boot_mode
        self._base_dir = base_dir

    @property
    def name(self):
        return self._name

    @property
    def boot_mode(self):
        return self._boot_mode

    @property
    def base_dir(self):
        return self._base_dir

    @abc.abstractmethod
    def umount_and_dispose(self):
        pass

    @abc.abstractmethod
    def get_mount_entries(self):
        pass

    @staticmethod
    def _getSubClassDict():
        return {
            Category.WINDOWS_XP: StorageLayoutWindowsXP,
        }

    @classmethod
    def _getSubClass(cls, layout_name):
        for layoutClass in cls._getSubClassList():
            if layoutClass.name == layout_name:
                return layoutClass
        return None


class StorageLayoutWindowsXP(StorageLayout):

    @staticmethod
    def mount(boot_mode, base_dir):
        pass

    @staticmethod
    def create_and_mount(boot_mode, base_dir):
        pass

    def __init__(self, name, boot_mode, base_dir):
        assert boot_mode in [BootMode.BIOS, BootMode.EFI]
        self._name = name
        self._bootMode = boot_mode
        self._baseDir = base_dir

    @property
    def name(self):
        return self._name

    @property
    def boot_mode(self):
        return self._bootMode

    @property
    def base_dir(self):
        return self._baseDir

    def umount_and_dispose(self):
        assert False

    def get_mount_entries(self):
        assert False


