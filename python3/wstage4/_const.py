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


class Arch(enum.Enum):
    X86 = "X86"
    X86_64 = "X86_64"


class Category(enum.Enum):
    WINDOWS_95 = "windows-95"
    WINDOWS_98 = "windows-98"
    WINDOWS_XP = "windows-xp"
    WINDOWS_VISTA = "windows-vista"
    WINDOWS_7 = "windows-7"
    WINDOWS_8 = "windows-8"
    WINDOWS_8_1 = "windows-8"
    WINDOWS_10 = "windows-10"
    WINDOWS_11 = "windows-11"

    WINDOWS_SERVER_2008 = "windows-server-2008"
    WINDOWS_SERVER_2012 = "windows-server-2012"
    WINDOWS_SERVER_2016 = "windows-server-2016"
    WINDOWS_SERVER_2019 = "windows-server-2019"


class Edition(enum.Enum):
    WINDOWS_XP_HOME = "windows-xp-home"
    WINDOWS_XP_PROFESSIONAL = "windows-xp-professional"

    WINDOWS_VISTA = "windows-vista"

    # from https://www.windowsafg.com
    WINDOWS_7_STARTER = "windows-7-starter"                 # Windows 7 Starter
    WINDOWS_7_HOME_BASIC = "windows-7-home-basic"           # Windows 7 Home Basic
    WINDOWS_7_HOME_PREMIUM = "windows-7-home-premium"       # Windows 7 Home Premium
    WINDOWS_7_PROFESSIONAL = "windows-7-professional"       # Windows 7 Professional
    WINDOWS_7_ULTIMATE = "windows-7-ultimate"               # Windows 7 Ultimate
    WINDOWS_7_ENTERPRISE = "windows-7-enterprise"           # Windows 7 Enterprise

    # from https://www.windowsafg.com
    WINDOWS_8 = "windows-8"                                 # Windows 8
    WINDOWS_8_PRO = "windows-8-pro"                         # Windows 8 Pro
    WINDOWS_8_PRO_MC = "windows-8-pro-mc"                   # Windows 8 Pro with Media Center
    WINDOWS_8_ENTERPRISE = "windows-8-enterprise"           # Windows 8 Enterprise

    # from https://www.windowsafg.com
    WINDOWS_8_1 = "windows-8-1"                             # Windows 8.1
    WINDOWS_8_1_PRO = "windows-8-1-pro"                     # Windows 8.1 Pro
    WINDOWS_8_1_PRO_MC = "windows-8-1-pro-mc"               # Windows 8.1 Pro with Media Center
    WINDOWS_8_1_ENTERPRISE = "windows-8-1-enterprise"       # Windows 8.1 Enterprise

    # from https://www.windowsafg.com
    WINDOWS_10_HOME = "windows-10-home"                         # Windows 10 Home
    WINDOWS_10_PRO = "windows-10-pro"                           # Windows 10 Pro
    WINDOWS_10_EDUCATION = "windows-10-education"               # Windows 10 Education
    WINDOWS_10_ENTERPRISE = "windows-10-enterprise"             # Windows 10 Enterprise
    WINDOWS_10_ENTERPRISE_LTSB = "windows-10-enterprise-ltsb"   # Windows 10 Enterprise LTSB

    WINDOWS_11 = "windows-11"

    # from https://www.windowsafg.com
    WINDOWS_SERVER_2008 = "windows-server-2008"
    WINDOWS_SERVER_2012 = "windows-server-2012"
    WINDOWS_SERVER_2016 = "windows-server-2016"
    WINDOWS_SERVER_2019 = "windows-server-2019"


class Lang(enum.Enum):
    en_US = "en_us"
    zh_CN = "zh_cn"
    zh_TW = "zh_tw"


class BootMode(enmu.Enum):
    BIOS = enum.auto()
    EFI = enum.auto()
