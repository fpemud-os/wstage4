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
    WINDOWS_XP = "windows-xp"
    WINDOWS_7 = "windows-7"
    WINDOWS_8 = "windows-8"
    WINDOWS_10 = "windows-10"
    WINDOWS_11 = "windows-11"


class Variant(enum.Enum):
    WINDOWS_XP_HOME = "windows-xp-home"
    WINDOWS_XP_PROFESSIONAL = "windows-xp-professional"

    WINDOWS_7_HOME = "windows-7-home"
    WINDOWS_7_PROFESSIONAL = "windows-7-professional"
    WINDOWS_7_ULTIMATE = "windows-7-ultimate"

    WINDOWS_8 = "windows-8"
    WINDOWS_8_1 = "windows-8-1"

    WINDOWS_10 = "windows-10"

    WINDOWS_11 = "windows-11"


class Lang(enum.Enum):
    en_us = "en_us"
    zh_cn = "zh_cn"
    zh_tw = "zh_tw"


class BootMode(enmu.Enum):
    BIOS = enum.auto()
    EFI = enum.auto()
