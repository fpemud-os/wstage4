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
import io
import pycdlib
import collections
from ._util import Util, TmpMount
from ._const import Arch, Category, Edition, Lang
from ._errors import InstallMediaError


class InstallMedia:

    def __init__(self, path):
        self._path = path

        # parsed data
        self._arch = None
        self._category = None
        self._variantList = []
        self._langList = []

        # get cdrom object
        self._iso = pycdlib.PyCdlib()
        self._iso.open(path)
        if len(self._iso.pvds) != 1:
            raise InstallMediaError("invalid install media, multiple PVDs")
        if self._src.has_rock_ridge():
            raise InstallMediaError("invalid install media, Rock Ridge extension")
        if self._src.has_udf():
            raise InstallMediaError("invalid install media, UDF format")

        # pycdlib has no direct method to get this value, sucks
        self._label = self._iso.pvds[0].volume_identifier.decode(self._iso.pvds[0].encoding).rstrip(" ")

        # parse cdrom
        funcList = [
            self._parserWindowns98,
            self._parserWindownsXP,
            self._parserWindowns7,
        ]
        for func in funcList:
            ret = func()
            if ret is not None:
                self._arch, self._category, self._variantList, self._langList = ret
                return
        assert False

    def dispose(self):
        if hasattr(self, "_iso"):
            self._iso.close()
            del self._iso
        del self._langList
        del self._variantList
        del self._category
        del self._arch
        del self._path

    @property
    def path(self):
        return self._path

    def getArch(self):
        return self._arch

    def getVariantList(self):
        return self._variantList

    def getLangList(self):
        return self._langList

    def getIsoObj(self):
        return self._iso

    def _parserWindowns98(self):
        if self._label == "WIN98 SE":
            # FIXME
            return (Arch.X86, Category.WINDOWS_98, [Edition.WINDOWS_98_SE], [Lang.en_US])
        return None

    def _parserWindownsXP(self):
        if self._label == "GRTMPVOL_EN":
            # FIXME
            return (Arch.X86, Category.WINDOWS_XP, [Edition.WINDOWS_XP_PROFESSIONAL], [Lang.en_US, Lang.zh_CN])
        return None

    def _parserWindowns7(self):
        if self._label == "GRMCULFRER_EN_DVD":
            # FIXME
            with TmpMount(self._path) as mp:
                out = Util.cmdCall("file", "-L", os.path.join(mp, "setup.exe"))
                if "80386" in out:
                    arch = Arch.X86
                elif "x86-64" in out:
                    arch = Arch.X86_64
                else:
                    assert False
            return (arch, Category.WINDOWS_7, [Edition.WINDOWS_7_ULTIMATE], [Lang.en_US, Lang.zh_CN])
        return None


class InstallMediaCustomizer:

    def __init__(self, src_iso_obj, target_iso_file):
        self._src = src_iso_obj
        self._target = target_iso_file
        self._newFiles = dict()

    def add_dir(self, dir_path):
        assert dir_path.startswith("/")
        assert dir_path not in self._newFiles

        self._newFiles[dir_path] = None

    def add_file(self, file_path, file_content):
        assert file_path.startswith("/")
        assert file_path not in self._newFiles
        assert isinstance(file_content, bytearray)

        self._newFiles[file_path] = file_content

    def update_file(self, file_path, file_content):
        assert file_path.startswith("/")
        assert file_path not in self._newFiles
        assert isinstance(file_content, bytearray)

        self._newFiles[file_path] = file_content

    def add_or_update_file(self, file_path, file_content):
        assert file_path.startswith("/")
        assert isinstance(file_content, bytearray)

        self._newFiles[file_path] = file_content

    def export(self):
        # should have the same parameter as self._src
        theDstIso = pycdlib.PyCdlib()
        theDstIso.new(interchange_level=self._src.interchange_level,
                      sys_ident=self._src.pvds[0].system_identifier.decode(self._src.pvds[0].encoding).rstrip(" "),
                      vol_ident=self._src.pvds[0].volume_identifier.decode(self._src.pvds[0].encoding).rstrip(" "),
                      set_size=self._src.pvds[0].set_size,
                      seqnum=self._src.pvds[0].seqnum,
                      vol_set_ident=self._src.pvds[0].volume_set_identifier.decode(self._src.pvds[0].encoding).rstrip(" "),
                      pub_ident_str=self._src.pvds[0].publisher_identifier.text.decode(self._src.pvds[0].encoding).rstrip(" "),
                      preparer_ident_str=self._src.pvds[0].preparer_identifier.text.decode(self._src.pvds[0].encoding).rstrip(" "),
                      app_ident_str=self._src.pvds[0].application_identifier.text.decode(self._src.pvds[0].encoding).rstrip(" "),
                      copyright_file=self._src.pvds[0].copyright_file_identifier.decode(self._src.pvds[0].encoding).rstrip(" "),
                      abstract_file=self._src.pvds[0].abstract_file_identifier.decode(self._src.pvds[0].encoding).rstrip(" "),
                      bibli_file=self._src.pvds[0].bibliographic_file_identifier.decode(self._src.pvds[0].encoding).rstrip(" "),
                      joliet=(3 if self._src.has_joliet() else None),
                      rock_ridge=("1.12" if self._src.has_rock_ridge() else None),
                      xa=self._src.xa,
                      udf=None)
        try:
            root_entry = self._src.get_record(iso_path="/")
            dirs = collections.deque([root_entry])
            while dirs:
                dir_record = dirs.popleft()
                fullfn = self._src.full_path_from_dirrecord(dir_record)
                if dir_record.is_link():
                    raise InstallMediaError("invalid install media, it has symlink %s" % (fullfn))
                elif dir_record.is_dir():
                    kargDict = {}
                    if self._src.has_rock_ridge():
                        kargDict["rr_name"] = dir_record.rock_ridge.name()
                    if self._src.has_joliet():
                        kargDict["joliet_path"] = fullfn
                    self._src.add_directory(fullfn, **kargDict)

                    for child in self._src.list_children(iso_path=fullfn):
                        if child is None or child.is_dot() or child.is_dotdot():
                            continue
                        dirs.append(child)
                elif dir_record.is_file():
                    kargDict = {}
                    if self._src.has_rock_ridge():
                        kargDict["rr_name"] = dir_record.rock_ridge.name()
                    if self._src.has_joliet():
                        kargDict["joliet_path"] = fullfn
                    theDstIso.add_file(fullfn, **kargDict)
                else:
                    assert False

            for fullfn, fbuf in self._newFiles.items():
                kargDict = {}
                if self._src.has_rock_ridge():
                    kargDict["rr_name"] = os.path.basename(fullfn)
                if self._src.has_joliet():
                    kargDict["joliet_path"] = fullfn

                if fbuf is None:
                    isoPath = pycdlib.utils.mangle_dir_for_iso9660(fullfn, theDstIso.interchange_level)
                    theDstIso.add_directory(iso_path=isoPath, **kargDict)
                else:
                    isoPath = pycdlib.utils.mangle_file_for_iso9660(fullfn, theDstIso.interchange_level)
                    theDstIso.add_fp(io.BytesIO(fbuf), len(fbuf), iso_path=isoPath, **kargDict)

            theDstIso.write(self._target)
        finally:
            theDstIso.close()

    def dispose(self):
        del self._newFiles
        del self._target
        del self._src
