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


from ._const import Arch
from ._errors import SettingsError


class Settings:

    def __init__(self):
        self.program_name = None

        self.log_dir = None

        self.verbose_level = 1

    @classmethod
    def check_object(cls, obj, raise_exception=None):
        assert raise_exception is not None

        if not isinstance(obj, cls):
            if raise_exception:
                raise SettingsError("invalid object type")
            else:
                return False

        if not isinstance(obj.program_name, str):
            if raise_exception:
                raise SettingsError("invalid value for key \"program_name\"")
            else:
                return False

        if obj.log_dir is not None and not isinstance(obj.log_dir, str):
            if raise_exception:
                raise SettingsError("invalid value for key \"log_dir\"")
            else:
                return False

        if not (0 <= obj.verbose_level <= 2):
            if raise_exception:
                raise SettingsError("invalid value for key \"verbose_level\"")
            else:
                return False

        return True


class TargetSettings:

    def __init__(self):
        self.arch = None
        self.category = None
        self.edition = None
        self.lang = None

        self.serial = None

    @classmethod
    def check_object(cls, obj, raise_exception=None):
        assert raise_exception is not None

        try:
            if not isinstance(obj, cls):
                raise SettingsError("invalid object type")

            if obj.arch == "alpha":
                pass
            elif obj.arch == "amd64":
                pass
            elif obj.arch == "arm":
                pass
            elif obj.arch == "hppa":
                pass
            elif obj.arch == "ia64":
                pass
            elif obj.arch == "m68k":
                pass
            elif obj.arch == "mips":
                pass
            elif obj.arch == "ppc":
                pass
            elif obj.arch == "riscv":
                pass
            elif obj.arch == "s390":
                pass
            elif obj.arch == "sh":
                pass
            elif obj.arch == "sparc":
                pass
            elif obj.arch == Arch.X86:
                pass
            elif obj.arch == Arch.X86_64:
                pass
            else:
                raise SettingsError("invalid value of arch")





            return True
        except SettingsError:
            if raise_exception:
                raise
            else:
                return False
