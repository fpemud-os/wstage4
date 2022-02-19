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
        if self._iso.has_rock_ridge():
            raise InstallMediaError("invalid install media, Rock Ridge extension")

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

    def getCategory(self):
        return self._category

    def getVariantList(self):
        return self._variantList

    def getLangList(self):
        return self._langList

    def getIsoObj(self):
        return self._iso

    def _parserWindowns98(self):
        if self._label == "WIN98 SE":
            return (Arch.X86, Category.WINDOWS_98, [Edition.WINDOWS_98_SE], [Lang.en_US])
        return None

    def _parserWindownsXP(self):
        if self._label == "GRTMPVOL_EN":
            return (Arch.X86, Category.WINDOWS_XP, [Edition.WINDOWS_XP_PROFESSIONAL], [Lang.en_US, Lang.zh_CN])
        return None

    def _parserWindowns7(self):
        if self._label == "GRMCULFRER_EN_DVD":
            return (Arch.X86, Category.WINDOWS_7, [Edition.WINDOWS_7_ULTIMATE], [Lang.en_US, Lang.zh_CN])
        if self._label == "GRMCULXFRER_EN_DVD":
            return (Arch.X86_64, Category.WINDOWS_7, [Edition.WINDOWS_7_ULTIMATE], [Lang.en_US, Lang.zh_CN])
        return None


class InstallMediaCustomizer:

    def __init__(self, src_iso_obj, target_iso_file):
        self._src = src_iso_obj
        self._target = target_iso_file

    def exists(self, udf_path=None, joliet_path=None, iso_path=None):
        def __getAndCheck(rec, flen):
            if rec is None:
                if flen is not None:
                    raise InstallMediaError("invalid paths specified")
            else:
                if rec.is_dir():
                    if flen is not None:
                        if flen != -1:
                            raise InstallMediaError("invalid paths specified")
                    else:
                        flen = -1
                elif rec.is_file():
                    if flen is not None:
                        if flen != rec.get_data_length():
                            raise InstallMediaError("invalid paths specified")
                    else:
                        flen = rec.get_data_length()
                else:
                    raise InstallMediaError("invalid paths specified")
            return flen

        flen = None
        if udf_path is not None:
            try:
                rec = self._src.get_record(udf_path=udf_path)
                flen = __getAndCheck(rec, flen)
            except pycdlib.pycdlibexception.PyCdlibInvalidInput as e:
                # for udf_path, exception is raised if not found, strange
                if str(e) == 'Could not find path':
                    return False
                raise
        if joliet_path is not None:
            rec = self._src.get_record(joliet_path=joliet_path)
            flen = __getAndCheck(rec, flen)
        if iso_path is not None:
            rec = self._src.get_record(iso_path=iso_path)
            flen = __getAndCheck(rec, flen)

        return (flen is not None)

    def add_dir(self, udf_path=None, joliet_path=None, iso_path=None):
        self._src.add_directory(**self._getKwAll(udf_path, joliet_path, iso_path))

    def del_dir(self, udf_path=None, joliet_path=None, iso_path=None):
        for child in self._src.list_children(**self._getKwOne(udf_path, joliet_path, iso_path)):
            if child.is_dir():
                if child is None or child.is_dot() or child.is_dotdot():
                    continue
                self.del_dir(**self._getKwNew(udf_path, joliet_path, iso_path, self._src.full_path_from_dirrecord(child)))
            elif child.is_file():
                self._src.rm_file(**self._getKwNew(udf_path, joliet_path, iso_path, self._src.full_path_from_dirrecord(child)))
            else:
                raise InstallMediaError("invalid record type")
        self._src.rm_directory(**self._getKwOne(udf_path, joliet_path, iso_path))

    def add_file(self, udf_path=None, joliet_path=None, iso_path=None, file_content=None):
        self._src.add_fp(io.BytesIO(file_content), len(file_content), **self._getKwAll(udf_path, joliet_path, iso_path))

    def del_file(self, udf_path=None, joliet_path=None, iso_path=None):
        print(udf_path, joliet_path, iso_path)
        self._src.rm_file(**self._getKwOne(udf_path, joliet_path, iso_path))

    def export(self):
        self._src.write(self._target)

    def dispose(self):
        del self._target
        del self._src

    def _getKwOne(self, udf_path, joliet_path, iso_path):
        if udf_path is not None:
            assert udf_path.startswith("/")
        if joliet_path is not None:
            assert joliet_path.startswith("/")
        if iso_path is not None:
            assert iso_path.startswith("/")
        if udf_path is not None:
            return {"udf_path": udf_path}
        if joliet_path is not None:
            return {"joliet_path": joliet_path}
        if iso_path is not None:
            return {"iso_path": iso_path}
        assert False

    def _getKwAll(self, udf_path, joliet_path, iso_path):
        ret = {}
        if udf_path is not None:
            assert udf_path.startswith("/")
            ret["udf_path"] = udf_path
        if joliet_path is not None:
            assert joliet_path.startswith("/")
            ret["joliet_path"] = joliet_path
        if iso_path is not None:
            assert iso_path.startswith("/")
            ret["iso_path"] = iso_path
        assert len(ret) > 0
        return ret

    def _getKwNew(self, udf_path, joliet_path, iso_path, path):
        assert path.startswith("/")
        if udf_path is not None:
            return {"udf_path": path}
        if joliet_path is not None:
            return {"joliet_path": path}
        if iso_path is not None:
            return {"iso_path": path}
        assert False


# class InstallMediaCustomizer2:

#     def __init__(self, src_iso_obj, target_iso_file):
#         self._src = src_iso_obj
#         self._target = target_iso_file
#         self._newFiles = dict()

#     def add_dir(self, dir_path):
#         assert dir_path.startswith("/")
#         assert dir_path not in self._newFiles

#         self._newFiles[dir_path] = None

#     def add_file(self, file_path, file_content):
#         assert file_path.startswith("/")
#         assert file_path not in self._newFiles
#         assert isinstance(file_content, bytes)

#         self._newFiles[file_path] = file_content

#     def update_file(self, file_path, file_content):
#         assert file_path.startswith("/")
#         assert file_path not in self._newFiles
#         assert isinstance(file_content, bytes)

#         self._newFiles[file_path] = file_content

#     def add_or_update_file(self, file_path, file_content):
#         assert file_path.startswith("/")
#         assert isinstance(file_content, bytes)

#         self._newFiles[file_path] = file_content

#     def export(self):
#         # should have the same parameter as self._src
#         theDstIso = pycdlib.PyCdlib()
#         theDstIso.new(interchange_level=self._src.interchange_level,
#                       sys_ident=self._src.pvds[0].system_identifier.decode(self._src.pvds[0].encoding).rstrip(" "),
#                       vol_ident=self._src.pvds[0].volume_identifier.decode(self._src.pvds[0].encoding).rstrip(" "),
#                       set_size=self._src.pvds[0].set_size,
#                       seqnum=self._src.pvds[0].seqnum,
#                       vol_set_ident=self._src.pvds[0].volume_set_identifier.decode(self._src.pvds[0].encoding).rstrip(" "),
#                       pub_ident_str=self._src.pvds[0].publisher_identifier.text.decode(self._src.pvds[0].encoding).rstrip(" "),
#                       preparer_ident_str="",
#                       app_ident_str=self._src.pvds[0].application_identifier.text.decode(self._src.pvds[0].encoding).rstrip(" "),
#                       copyright_file=self._src.pvds[0].copyright_file_identifier.decode(self._src.pvds[0].encoding).rstrip(" "),
#                       abstract_file=self._src.pvds[0].abstract_file_identifier.decode(self._src.pvds[0].encoding).rstrip(" "),
#                       bibli_file=self._src.pvds[0].bibliographic_file_identifier.decode(self._src.pvds[0].encoding).rstrip(" "),
#                       joliet=(3 if self._src.has_joliet() else None),
#                       rock_ridge=None,
#                       xa=self._src.xa,
#                       udf=None)

#         # mswin98 iso has 74 characters of preparer_ident_str, joliet extension can not convert it to utf-16 byte array of length 128, so we force it to ""
#         # preparer_ident_str=self._src.pvds[0].preparer_identifier.text.decode(self._src.pvds[0].encoding).rstrip(" "),

#         try:
#             root_entry = self._src.get_record(iso_path="/")
#             dirs = collections.deque([root_entry])
#             while dirs:
#                 dir_record = dirs.popleft()
#                 fullfn = self._src.full_path_from_dirrecord(dir_record)
#                 if dir_record.is_symlink():
#                     raise InstallMediaError("invalid install media, it has symlink %s" % (fullfn))
#                 elif dir_record.is_dir():
#                     if fullfn != "/":
#                         kargDict = {}
#                         if self._src.has_joliet():
#                             kargDict["joliet_path"] = fullfn
#                         theDstIso.add_directory(iso_path=fullfn, **kargDict)

#                     for child in self._src.list_children(iso_path=fullfn):
#                         if child is None or child.is_dot() or child.is_dotdot():
#                             continue
#                         dirs.append(child)
#                 elif dir_record.is_file():
#                     kargDict = {}
#                     if self._src.has_joliet():
#                         kargDict["joliet_path"] = fullfn
#                     bio = io.BytesIO()
#                     self._src.get_file_from_iso_fp(bio, iso_path=fullfn)
#                     bioLen = bio.tell()
#                     bio.seek(0)
#                     theDstIso.add_fp(bio, bioLen, iso_path=fullfn, **kargDict)
#                 else:
#                     assert False

#             for fullfn, fbuf in self._newFiles.items():
#                 kargDict = {}
#                 if self._src.has_joliet():
#                     kargDict["joliet_path"] = fullfn

#                 if fbuf is None:
#                     # isoPath = pycdlib.utils.mangle_dir_for_iso9660(fullfn, theDstIso.interchange_level)
#                     theDstIso.add_directory(iso_path=fullfn, **kargDict)
#                 else:
#                     # basename, ext = pycdlib.utils.mangle_file_for_iso9660(fullfn, theDstIso.interchange_level)
#                     # isoPath = '.'.join([basename, ext])
#                     theDstIso.add_fp(io.BytesIO(fbuf), len(fbuf), iso_path=fullfn, **kargDict)

#             theDstIso.write(self._target)
#         finally:
#             theDstIso.close()

#     def dispose(self):
#         del self._newFiles
#         del self._target
#         del self._src
