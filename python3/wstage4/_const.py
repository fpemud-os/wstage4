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


import enum


class Arch(enum.IntEnum):   # use enum.IntEnum so it's serializable, sucks
    X86 = enum.auto()
    X86_64 = enum.auto()


class Category(enum.IntEnum):
    WINDOWS_95 = enum.auto()
    WINDOWS_98 = enum.auto()
    WINDOWS_XP = enum.auto()
    WINDOWS_VISTA = enum.auto()
    WINDOWS_7 = enum.auto()
    WINDOWS_8 = enum.auto()
    WINDOWS_8_1 = enum.auto()
    WINDOWS_10 = enum.auto()
    WINDOWS_11 = enum.auto()

    WINDOWS_SERVER_2008 = enum.auto()
    WINDOWS_SERVER_2012 = enum.auto()
    WINDOWS_SERVER_2016 = enum.auto()
    WINDOWS_SERVER_2019 = enum.auto()


class Edition(enum.IntEnum):
    # from https://en.wikipedia.org/wiki/Microsoft_Windows_version_history
    WINDOWS_95 = enum.auto()                   # Windows 95

    # from https://en.wikipedia.org/wiki/Microsoft_Windows_version_history
    WINDOWS_98 = enum.auto()                   # Windows 98
    WINDOWS_98_SE = enum.auto()                # Windows 98 SE

    WINDOWS_XP_HOME = enum.auto()
    WINDOWS_XP_PROFESSIONAL = enum.auto()

    WINDOWS_VISTA = enum.auto()

    # from https://www.windowsafg.com
    WINDOWS_7_STARTER = enum.auto()            # Windows 7 Starter
    WINDOWS_7_HOME_BASIC = enum.auto()         # Windows 7 Home Basic
    WINDOWS_7_HOME_PREMIUM = enum.auto()       # Windows 7 Home Premium
    WINDOWS_7_PROFESSIONAL = enum.auto()       # Windows 7 Professional
    WINDOWS_7_ULTIMATE = enum.auto()           # Windows 7 Ultimate
    WINDOWS_7_ENTERPRISE = enum.auto()         # Windows 7 Enterprise

    # from https://www.windowsafg.com
    WINDOWS_8 = enum.auto()                    # Windows 8
    WINDOWS_8_PRO = enum.auto()                # Windows 8 Pro
    WINDOWS_8_PRO_MC = enum.auto()             # Windows 8 Pro with Media Center
    WINDOWS_8_ENTERPRISE = enum.auto()         # Windows 8 Enterprise

    # from https://www.windowsafg.com
    WINDOWS_8_1 = enum.auto()                  # Windows 8.1
    WINDOWS_8_1_PRO = enum.auto()              # Windows 8.1 Pro
    WINDOWS_8_1_PRO_MC = enum.auto()           # Windows 8.1 Pro with Media Center
    WINDOWS_8_1_ENTERPRISE = enum.auto()       # Windows 8.1 Enterprise

    # from https://www.windowsafg.com
    WINDOWS_10_HOME = enum.auto()              # Windows 10 Home
    WINDOWS_10_PRO = enum.auto()               # Windows 10 Pro
    WINDOWS_10_EDUCATION = enum.auto()         # Windows 10 Education
    WINDOWS_10_ENTERPRISE = enum.auto()        # Windows 10 Enterprise
    WINDOWS_10_ENTERPRISE_LTSB = enum.auto()   # Windows 10 Enterprise LTSB

    WINDOWS_11 = enum.auto()

    # from https://www.windowsafg.com
    WINDOWS_SERVER_2008 = enum.auto()
    WINDOWS_SERVER_2012 = enum.auto()
    WINDOWS_SERVER_2016 = enum.auto()
    WINDOWS_SERVER_2019 = enum.auto()


class Lang(enum.IntEnum):
    en_US = enum.auto()
    zh_CN = enum.auto()
    zh_TW = enum.auto()


class BootMode(enum.IntEnum):
    BIOS = enum.auto()
    EFI = enum.auto()
