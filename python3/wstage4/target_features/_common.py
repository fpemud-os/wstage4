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


import crypt
from gstage4.scripts import ScriptFromBuffer
from gstage4.scripts import PlacingFilesScript


class InstallLanguagePack:
    pass


class UseChocolaty:
    pass



class SetPasswordForUserRoot:

    def __init__(self, password):
        self._hash = crypt.crypt(password)

    def update_custom_script_list(self, custom_script_list):
        buf = ""
        buf += "#!/bin/sh\n"
        buf += "sed -i 's#^root:[^:]*:#root:%s:#' /etc/shadow\n" % (self._hash)      # modify /etc/shadow directly so that password complexity check won't be in our way

        s = ScriptFromBuffer("Set root's password", buf)
        assert s not in custom_script_list
        custom_script_list.append(s)


class AddUser:

    def __init__(self, username, password, comment=""):
        self._user = username
        self._pwd = password
        self._comment = comment

    def update_custom_script_list(self, custom_script_list):
        assert False
