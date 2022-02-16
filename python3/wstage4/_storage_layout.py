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

    @classmethod
    def get_storage_layout(cls, os_category, base_dir):
        assert base_dir.startswith("/") and len(os.listdir(base_dir)) == 0

        boot_mode = BootMode.BIOS                      # FIXME
        return cls._getSubClass(os_category)(boot_mode, base_dir)

    @classmethod
    def mount_storage_layout(cls, os_category, boot_mode, base_dir):
        assert isinstance(boot_mode, BootMode)
        assert base_dir.startswith("/") and len(os.listdir(base_dir)) == 0

        return cls._getSubClass(os_category).mount(boot_mode, base_dir)

    @classmethod
    def create_and_mount_storage_layout(cls, os_category, boot_mode, disk_list, base_dir):
        assert isinstance(boot_mode, BootMode)
        assert base_dir.startswith("/") and len(os.listdir(base_dir)) == 0

        return cls._getSubClass(os_category).create_and_mount(boot_mode, disk_list, base_dir)

    def __init__(self, os_category, boot_mode, base_dir):
        assert isinstance(os_category, Category)
        assert isinstance(boot_mode, BootMode)
        assert base_dir.startswith("/")

        self._category = os_category
        self._boot_mode = boot_mode
        self._base_dir = base_dir

    @property
    def os_category(self):
        return self._category

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
    def _getSubClass(os_category):
        d = {
            Category.WINDOWS_98: StorageLayoutWindows98,
            Category.WINDOWS_XP: StorageLayoutWindowsXP,
            Category.WINDOWS_7: StorageLayoutWindows7,
        }
        return d[os_category]


class StorageLayoutWindows98(StorageLayout):

    @staticmethod
    def mount(boot_mode, base_dir):
        os.mkdir(os.path.jion(base_dir, driveC))


    @staticmethod
    def create_and_mount(boot_mode, disk_list, base_dir):
        pass

    def __init__(self, boot_mode, base_dir):
        super().__init__(Category.WINDOWS_98, boot_mode, base_dir)

    def umount_and_dispose(self):
        assert False

    def get_mount_entries(self):
        assert False


class StorageLayoutWindowsXP(StorageLayout):

    @staticmethod
    def mount(boot_mode, base_dir):
        pass

    @staticmethod
    def create_and_mount(boot_mode, disk_list, base_dir):
        pass

    def __init__(self, boot_mode, base_dir):
        super().__init__(Category.WINDOWS_XP, boot_mode, base_dir)

    def umount_and_dispose(self):
        assert False

    def get_mount_entries(self):
        assert False


class StorageLayoutWindows7(StorageLayout):

    @staticmethod
    def mount(boot_mode, base_dir):
        pass

    @staticmethod
    def create_and_mount(boot_mode, disk_list, base_dir):
        pass

    def __init__(self, boot_mode, base_dir):
        super().__init__(Category.WINDOWS_7, boot_mode, base_dir)

    def umount_and_dispose(self):
        assert False

    def get_mount_entries(self):
        assert False

driveC = "C:"
driveD = "D:"
driveReserve = "reserve"
