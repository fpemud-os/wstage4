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


from ._const import Arch, Category, Edition, Lang
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

        self.product_key = None

        self.addons = []

    @classmethod
    def check_object(cls, obj, raise_exception=None):
        assert raise_exception is not None

        try:
            if not isinstance(obj, cls):
                raise SettingsError("invalid object type")

            # check obj.arch
            if not isinstance(obj.arch, Arch):
                raise SettingsError("invalid value of arch")

            # check obj.category
            if not isinstance(obj.arch, Category):
                raise SettingsError("invalid value of category")
            if True:
                if obj.category in [Category.WINDOWS_98]:
                    if obj.arch not in [Arch.X86]:
                        raise SettingsError("arch and category are not match")
                elif obj.category in [Category.WINDOWS_XP, Category.WINDOWS_7]:
                    if obj.arch not in [Arch.X86, Arch.X86_64]:
                        raise SettingsError("arch and category are not match")
                else:
                    assert False

            # check obj.edition
            if not isinstance(obj.edition, Edition):
                raise SettingsError("invalid value of edition")
            if True:
                if obj.edition in [Edition.WINDOWS_98, Edition.WINDOWS_98_SE]:
                    if obj.category != Category.WINDOWS_98:
                        raise SettingsError("category and edition are not match")
                elif obj.edition in [Edition.WINDOWS_XP_HOME, Edition.WINDOWS_XP_PROFESSIONAL]:
                    if obj.category != Category.WINDOWS_XP:
                        raise SettingsError("category and edition are not match")
                elif obj.edition in [Edition.WINDOWS_7_STARTER, Edition.WINDOWS_7_HOME_BASIC, Edition.WINDOWS_7_HOME_PREMIUM, Edition.WINDOWS_7_PROFESSIONAL, Edition.WINDOWS_7_ULTIMATE, Edition.WINDOWS_7_ENTERPRISE]:
                    if obj.category != Category.WINDOWS_7:
                        raise SettingsError("category and edition are not match")
                else:
                    assert False

            # check obj.lang
            if not isinstance(obj.lang, Lang):
                raise SettingsError("invalid value of lang")

            return True
        except SettingsError:
            if raise_exception:
                raise
            else:
                return False
