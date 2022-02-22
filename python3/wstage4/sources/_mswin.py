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
from .. import Arch, Category, Edition, Lang, get_prefered_edition_by_category
from .. import WindowsInstallIsoFile
from .. import InstallMediaError


class CloudWindowsInstallIsoFile(WindowsInstallIsoFile):

    def __init__(self, arch, category, edition=None, lang=None):
        pass





class LocalWindowsInstallIsoFile(WindowsInstallIsoFile):

    def __init__(self, arch, category, edition=None, lang=None, verify=True):
        categoryPathDict = {
            Category.WINDOWS_98: "windows-98",
            Category.WINDOWS_XP: "windows-xp",
            Category.WINDOWS_7: "windows-7",
        }
        MediaTypePostfixDict = {
            Category.WINDOWS_98: "cd",
            Category.WINDOWS_XP: "cd",
            Category.WINDOWS_7: "dvd",
        }
        archNameDict = {
            Arch.X86: "x86",
            Arch.X86_64: "amd64",
        }

        if edition is not None:
            # FIXME
            # assert edition in get_editions_by_category(category)
            assert edition == get_prefered_edition_by_category(category)

        if lang is not None:
            # FIXME
            assert lang == Lang.en_US

        self._path = "/usr/share"
        self._path = os.path.join(self._path, "microsoft-" + categoryPathDict[category] + "-setup-" + MediaTypePostfixDict[category])
        if category == Category.WINDOWS_98:
            self._path = os.path.join(self._path, categoryPathDict[category] + "-setup.iso")
            edition_list = [get_prefered_edition_by_category(category)]                             # FIXME: should be from ISO
            lang_list = [Lang.en_US]                                                                # FIXME: should be from ISO
        elif category in Category.WINDOWS_XP:
            self._path = os.path.join(self._path, categoryPathDict[category] + "-setup-" + archNameDict[arch] + ".iso")
            edition_list = [get_prefered_edition_by_category(category)]                             # FIXME: should be from ISO
            lang_list = [Lang.en_US]                                                                # FIXME: should be from ISO
        elif category == Category.WINDOWS_7:
            self._path = os.path.join(self._path, categoryPathDict[category] + "-setup-" + archNameDict[arch] + ".iso")
            edition_list = [get_prefered_edition_by_category(category)]                             # FIXME: should be from ISO
            lang_list = [Lang.en_US]                                                                # FIXME: should be from ISO
        else:
            assert False

        if self.verify:
            if not os.path.exists(self._path):
                raise InstallMediaError("file \"%s\" does not exist" % (self._path))
            # FIXME: check content

        self._set_os_info({
            "arch": arch,
            "category": category,
            "editions": edition_list,
            "languages": lang_list,
        })

    @property
    def path(self):
        return self._path
