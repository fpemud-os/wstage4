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
    def mount(cls, disk_list, base_dir):
        assert len(disk_list) > 0
        assert base_dir.startswith("/") and len(os.listdir(base_dir)) == 0

        if len(disk_list) == 1:
            return StorageLayoutNtfsSysWin._create_and_mount(disk_list, base_dir)
        else:
            assert False

    @classmethod
    def create_and_mount(cls, name, disk_list, base_dir):
        assert len(disk_list) > 0
        assert base_dir.startswith("/") and len(os.listdir(base_dir)) == 0

        d = {
            "fat-win": None,                                            # FIXME
            "fat-win-data": None,                                       # FIXME
            "ntfs-win": None,                                           # FIXME
            "ntfs-win-data": None,                                      # FIXME
            "ntfs-sys-win": StorageLayoutNtfsSysWin,
            "ntfs-sys-win-data": None,                                  # FIXME
            "ntfs-sys-msr-win": None,                                   # FIXME
            "ntfs-sys-msr-win-data": None,                              # FIXME
        }
        return d[name]._create_and_mount(boot_mode, disk_list, base_dir)

    @abc.abstractmethod
    @property
    def name(self):
        pass

    @abc.abstractmethod
    @property
    def boot_mode(self):
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

    @classmethod
    @abc.abstractmethod
    def _mount(cls, disk_list, base_dir):
        pass

    @classmethod
    @abc.abstractmethod
    def _create_and_mount(cls, disk_list, base_dir):
        pass

    @staticmethod
    def _getSubClass(name):
        d = {
            "fat-win": None,                                            # FIXME
            "fat-win-data": None,                                       # FIXME
            "ntfs-win": None,                                           # FIXME
            "ntfs-win-data": None,                                      # FIXME
            "ntfs-sys-win": StorageLayoutNtfsSysWin,
            "ntfs-sys-win-data": None,                                  # FIXME
            "ntfs-sys-msr-win": None,                                   # FIXME
            "ntfs-sys-msr-win-data": None,                              # FIXME
        }
        ret = d[name]
        assert ret is not None
        return ret


class MountEntry:

    def __init__(self):
        self.mnt_point = None
        self.real_dir_path = None
        self.target = None
        self.fs_type = None
        self.mnt_opts = None


###############################################################################


class StorageLayoutFatWin(StorageLayout):

    """single FAT32 partition in single harddisk"""

    @property
    def name():
        return "fat-win"


class StorageLayoutNtfsWin(StorageLayout):

    """single NTFS partition in single harddisk"""

    @property
    def name():
        return "ntfs-win"


class StorageLayoutNtfsSysWin(StorageLayout):

    """System Reserved partition(NTFS) + windows partition(NTFS) in single harddisk"""

    def __init__(self):
        self._hdd = None
        self._hddSysParti = None
        self._hddWinParti = None
        self._mnt = None

    @property
    def name():
        return "sys-win"

    @property
    def boot_mode(self):
        return BootMode.BIOS

    @property
    def base_dir(self):
        return self._mnt.mount_point

    def umount_and_dispose(self):
        if True:
            self._mnt.umount()
            del self._mnt
        del self._hddWinParti
        del self._hddSysParti
        del self._hdd

    def get_mount_entries(self):
        self._mnt.get_mount_entries()

    @classmethod
    def _mount(cls, disk_list, base_dir):
        assert len(disk_list) == 1

    @classmethod
    def _create_and_mount(cls, disk_list, base_dir):
        assert len(disk_list) == 1

        # initialize disk
        Util.initializeDisk(disk_list[0], Util.diskPartTableMbr, [
            ("100M", Util.fsTypeNtfs),
            ("*", Util.fsTypeNtfs),
        ])

        # return
        ret = cls()
        ret._hdd = hdd
        ret._hddSysParti = sysParti
        ret._hddWinParti = winParti
        ret._mnt = _Mount(False, base_dir, [
            _MountParam(Util.driveReserve, ret._hddSysParti, Util.fsTypeNtfs, ""),
            _MountParam(Util.driveC, ret._hddWinParti, Util.fsTypeNtfs, ""),
        ], {})
        return ret


###############################################################################


class _Mount:

    def __init__(self, bIsMounted, mntDir, mntParams, kwargsDict):
        assert len(mntParams) > 0
        assert all([isinstance(x, MountParam) for x in mntParams])

        self._mntDir = mntDir
        self._mntParams = mntParams

        # FIXME: we'll use kwargsDict later
        pass

        # do mount
        if not bIsMounted:
            for p in self._mntParams:
                if not os.path.exists(p.getRealDir()):
                    os.mkdir(p.getRealDir())
                elif os.path.isdir(p.getRealDir()) and not os.path.islink(p.getRealDir()):
                    pass
                else:
                    raise errors.StorageLayoutMountError("mount directory \"%s\" is invalid" % (p.getRealDir()))
                Util.cmdCall("mount", "-t", p.fs_type, "-o", p.mnt_opts, p.target, p.getRealDir())

    @property
    def mount_point(self):
        return self._mntDir

    @property
    def mount_params(self):
        return self._mntParams

    def get_mount_entries(self):
        ret = []
        for p in self._mntParams:
            item = MountEntry()
            item.mnt_point = p.dir_path
            item.real_dir_path = p.getRealDir()
            item.target = p.target
            item.fs_type = p.fs_type
            item.mnt_opts = PhysicalDiskMounts.find_entry_by_mount_point(p.getRealDir()).mnt_opts
            ret.append(item)
        return ret

    def umount(self):
        for p in reversed(self._mntParams):
            Util.cmdCall("umount", p.getRealDir())
            os.rmdir(p.getRealDir())


class _MountParam:

    def __init__(self, dir_path, target, fs_type, mnt_opt_list):
        assert not dir_path.startswith("/")
        assert target is not None
        assert fs_type is not None
        assert mnt_opt_list is not None

        self.dir_path = dir_path
        self.target = target
        self.fs_type = fs_type
        self.mnt_opt_list = mnt_opt_list

    @property
    def mnt_opts(self):
        return ",".join(self.mnt_opt_list)

    def getRealDir(self):
        return os.path.join(mountObj.mount_point, self.dir_path)
