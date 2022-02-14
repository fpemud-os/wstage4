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
from ._util import Util
from ._util import TmpMount
from ._const import Arch
from ._const import Edition
from ._const import Lang


class InstallMedia:

    def __init__(self, path):
        self._path = path

        self._arch = None
        self._variantList = []
        self._langList = []

        label = Util.getCdromLabel(self._path)
        if label == "GRTMPVOL_EN":
            # FIXME
            self._arch = Arch.X86
            self._variantList = [Edition.WINDOWS_XP_PROFESSIONAL]
            self._langList = [Lang.en_us, Lang.zh_cn]
        elif label == "GRMCULFRER_EN_DVD":
            # FIXME
            with TmpMount(self._path) as mp:
                out = Util.cmdCall("file", "-L", os.path.join(mp, "setup.exe"))
                if "80386" in out:
                    self._arch = Arch.X86
                elif "x86-64" in out:
                    self._arch = Arch.X86_64
                else:
                    assert False
            self._variantList = [Edition.WINDOWS_7_ULTIMATE]
            self._langList = [Lang.en_us, Lang.zh_cn]
        else:
            assert False

    @property
    def path(self):
        return self._path

    def getArch(self):
        return self._arch

    def getVariantList(self):
        return self._variantList

    def getLangList(self):
        return self._langList
