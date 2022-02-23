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
import pycdlib
from .. import Arch, Category, Edition, Lang, get_prefered_edition_by_category
from .. import WindowsInstallIsoFile
from .. import InstallMediaError


class CloudWindowsInstallIsoFile(WindowsInstallIsoFile):

    def __init__(self, arch, category, edition=None, lang=None, local_filepath=None):
        self._arch = arch
        self._category = category
        self._edition = edition
        self._lang = lang
        self._path = local_filepath

    def download(self):
        if self._edition == Edition.WINDOWS_7_ENTERPRISE:
            urlDict = {
                Arch.X86: "https://idatavn-my.sharepoint.com/:u:/g/personal/data01_phanmemchat_net/Eec-CsxcwntJkpS_qCnrYPEBp5GFlChmzzfFAlisjR96Kw?e=fpr76R",       # from https://techpp.com/2018/04/16/windows-7-iso-official-direct-download-links
                Arch.X86_64: "https://idatavn-my.sharepoint.com/:u:/g/personal/data01_phanmemchat_net/EbQ80EYnmyNFqprGKPmf3xgBzyHkeLvPTeGOpvhmePYh5Q?e=lwMDXi",    # from https://techpp.com/2018/04/16/windows-7-iso-official-direct-download-links
            }
            # FIXME: need to click button
            assert False
        else:
            urlDict = {
                Edition.WINDOWS_7_HOME_PREMIUM: {
                    Arch.X86: "https://download.microsoft.com/download/E/D/A/EDA6B508-7663-4E30-86F9-949932F443D0/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_HOMEPREMIUM_x86FRE_en-us.iso",       # from https://techpp.com/2018/04/16/windows-7-iso-official-direct-download-links
                    Arch.X86_64: "https://download.microsoft.com/download/E/A/8/EA804D86-C3DF-4719-9966-6A66C9306598/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_HOMEPREMIUM_x64FRE_en-us.iso",    # from https://techpp.com/2018/04/16/windows-7-iso-official-direct-download-links
                },
                Edition.WINDOWS_7_PROFESSIONAL: {
                    Arch.X86: "https://download.microsoft.com/download/C/0/6/C067D0CD-3785-4727-898E-60DC3120BB14/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_PROFESSIONAL_x86FRE_en-us.iso",      # from https://techpp.com/2018/04/16/windows-7-iso-official-direct-download-links
                    Arch.X86_64: "https://download.microsoft.com/download/5/1/9/5195A765-3A41-4A72-87D8-200D897CBE21/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_ULTIMATE_x64FRE_en-us.iso",       # from https://techpp.com/2018/04/16/windows-7-iso-official-direct-download-links
                },
                Edition.WINDOWS_7_ULTIMATE: {
                    Arch.X86: "https://download.microsoft.com/download/1/E/6/1E6B4803-DD2A-49DF-8468-69C0E6E36218/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_ULTIMATE_x86FRE_en-us.iso",          # from https://techpp.com/2018/04/16/windows-7-iso-official-direct-download-links
                    Arch.X86_64: "https://download.microsoft.com/download/5/1/9/5195A765-3A41-4A72-87D8-200D897CBE21/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_ULTIMATE_x64FRE_en-us.iso",       # from https://techpp.com/2018/04/16/windows-7-iso-official-direct-download-links
                },
            }
            url = urlDict[self._edition][self._arch]

        with urllib.request.urlopen(url) as resp:
            with open(self._path, "wb") as f:
                buf = resp.read(4096)
                while len(buf) > 0:
                    f.write(buf)
                    buf = resp.read(4096)

        self._set_info(self._path, {
            "arch": self._arch,
            "category": self._category,
            "editions": self._edition,
            "languages": self._lang,
        })
        assert False


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

        path = "/usr/share"
        path = os.path.join(path, "microsoft-" + categoryPathDict[category] + "-setup-" + MediaTypePostfixDict[category])
        if category == Category.WINDOWS_98:
            path = os.path.join(path, categoryPathDict[category] + "-setup.iso")
            edition_list = [get_prefered_edition_by_category(category)]                             # FIXME: should be from ISO
            lang_list = [Lang.en_US]                                                                # FIXME: should be from ISO
        elif category in Category.WINDOWS_XP:
            path = os.path.join(path, categoryPathDict[category] + "-setup-" + archNameDict[arch] + ".iso")
            edition_list = [get_prefered_edition_by_category(category)]                             # FIXME: should be from ISO
            lang_list = [Lang.en_US]                                                                # FIXME: should be from ISO
        elif category == Category.WINDOWS_7:
            path = os.path.join(path, categoryPathDict[category] + "-setup-" + archNameDict[arch] + ".iso")
            edition_list = [get_prefered_edition_by_category(category)]                             # FIXME: should be from ISO
            lang_list = [Lang.en_US]                                                                # FIXME: should be from ISO
        else:
            assert False

        if self.verify:
            if not os.path.exists(path):
                raise InstallMediaError("file \"%s\" does not exist" % (path))

            iso = pycdlib.PyCdlib()
            iso.open(self._path)
            try:
                if len(iso.pvds) != 1:
                    raise InstallMediaError("invalid ISO file, multiple PVDs")
                if iso.has_rock_ridge():
                    raise InstallMediaError("invalid ISO file, Rock Ridge extension found")

                # pycdlib has no direct method to get this value, sucks
                label = iso.pvds[0].volume_identifier.decode(iso.pvds[0].encoding).rstrip(" ")
                if edition == Edition.WINDOWS_98_SE:
                    if label != "WIN98 SE":
                        raise InstallMediaError("invalid ISO file, label not match")
                elif arch == Arch.X86 and edition == Edition.WINDOWS_XP_PROFESSIONAL:
                    if label == "GRTMPVOL_EN":
                        raise InstallMediaError("invalid ISO file, label not match")
                elif arch == Arch.X86_64 and edition == Edition.WINDOWS_XP_PROFESSIONAL:
                    if label == "CRMPXVOL_EN":
                        raise InstallMediaError("invalid ISO file, label not match")
                elif arch == Arch.X86 and edition == Edition.WINDOWS_7_ULTIMATE:
                    if label == "GRMCULFRER_EN_DVD":
                        raise InstallMediaError("invalid ISO file, label not match")
                elif arch == Arch.X86_64 and edition == Edition.WINDOWS_7_ULTIMATE:
                    if label == "GRMCULXFRER_EN_DVD":
                        raise InstallMediaError("invalid ISO file, label not match")
                else:
                    assert False
            finally:
                iso.close()

        self._set_info(path, {
            "arch": arch,
            "category": category,
            "editions": edition_list,
            "languages": lang_list,
        })
