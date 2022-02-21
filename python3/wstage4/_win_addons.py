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


from ._const import Category


class AddonRepo:

    def __init__(self, arch, category, edition, lang):
        self._arch = arch
        self._category = category
        self._variantList = edition
        self._langList = lang
    
    def getAddonNames(self):
        if self._category == Category.WINDOWS_98:
            return ["lang-packs", "virtio-drivers", "common-drivers"]
        elif self._category == Category.WINDOWS_XP:
            return ["lang-packs", "virtio-drivers", "common-drivers"]
        elif self._category == Category.WINDOWS_7:
            return ["lang-packs", "virtio-drivers", "common-drivers"]
        else:
            assert False

    def getAddon(self, name):
        if self._category == Category.WINDOWS_98:
            if name == "lang-packs":
                pass
            elif name == "virtio-drivers":
                pass
            elif name == "common-drivers":
                pass
            else:
                assert False
        elif self._category == Category.WINDOWS_XP:
            if name == "lang-packs":
                pass
            elif name == "virtio-drivers":
                pass
            elif name == "common-drivers":
                pass
            else:
                assert False
        elif self._category == Category.WINDOWS_7:
            if name == "lang-packs":
                pass
            elif name == "virtio-drivers":
                pass
            elif name == "common-drivers":
                pass
            else:
                assert False
        else:
            assert False


class Windows98Addon:
    pass


# Mainstream support for Windows 98 and 98 SE ended on June 30, 2002
# Extended support for Windows 98 and 98 SE ended on July 11, 2006.

# Mainstream support for Windows XP ended on April 14, 2009
# Extended support for Windows XP ended on April 8, 2014
# Extended support for Windows Embedded POSReady 2009 (based on Windows XP SP3) systems ends on April 9th, 2019

# Support for Windows 7 ended on 14 January 2020
