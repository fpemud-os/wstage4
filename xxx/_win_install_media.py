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


import io
import pycdlib
from ..python3.wstage4._const import Arch, Version, Edition, Lang
from ..python3.wstage4._errors import InstallMediaError


class InstallMediaCustomizer:

    def __init__(self, src_iso_obj, target_iso_file):
        self._src = src_iso_obj
        self._target = target_iso_file

    def exists(self, udf_path=None, joliet_path=None, iso_path=None):
        # existence check, pycdlib doesn't support this function

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
        # delete recursively, pycdlib doesn't support this function
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
