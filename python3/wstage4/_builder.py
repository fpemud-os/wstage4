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
import json
import enum
from ._util import Util, TmpMount
from ._const import Version
from ._prototype import WindowsInstallIsoFile, ScriptInChroot
from ._errors import SettingsError, InstallMediaError
from ._settings import Settings, TargetSettings
from ._vm import Vm, VmUtil
from ._win_addons import AddonRepo
from ._win_unattend import AnswerFileGenerator


def Action(*progressStepTuple):
    def decorator(func):
        def wrapper(self, *kargs, **kwargs):
            progressStepList = list(progressStepTuple)
            assert sorted(progressStepList) == list(progressStepList)
            assert self._progress in progressStepList
            func(self, *kargs, **kwargs)
            self._progress = BuildStep(progressStepList[-1] + 1)
        return wrapper
    return decorator


class BuildStep(enum.IntEnum):
    INIT = enum.auto()
    CUSTOM_INSTALL_MEDIA_PREPARED = enum.auto()
    MSWIN_INSTALLED = enum.auto()
    CORE_APPS_INSTALLED = enum.auto()
    EXTRA_APPS_INSTALLED = enum.auto()
    SYSTEM_CUSTOMIZED = enum.auto()
    CLEANED_UP = enum.auto()


class Builder:
    """
    This class does all of the jobs, including create custom install ISO file, setup VM, install windows and addons, etc.
    It is the driver class for pretty much everything that wstage4 does.
    """

    def __init__(self, settings, target_settings, work_dir):
        assert Settings.check_object(settings, raise_exception=False)
        assert TargetSettings.check_object(target_settings, raise_exception=False)
        assert work_dir.verify_existing(raise_exception=False)

        self._s = settings
        if self._s.log_dir is not None:
            os.makedirs(self._s.log_dir, mode=0o750, exist_ok=True)

        self._ts = target_settings

        self._addonRepo = AddonRepo(self._ts.arch, self._ts.version, self._ts.edition, self._ts.lang)
        for i in self._ts.addons:
            if i not in self._addonRepo.getAddonNames():
                raise SettingsError("invalid addon %s" % (i))

        self._workDirObj = work_dir

        self._progress = BuildStep.INIT

    def get_progress(self):
        return self._progress

    @Action(BuildStep.INIT)
    def action_prepare_custom_install_media(self, install_iso_file):
        assert isinstance(install_iso_file, WindowsInstallIsoFile)

        # check install iso file
        if self._ts.arch != install_iso_file.get_arch():
            raise InstallMediaError("invalid install ISO file, arch not match")
        if self._ts.version != install_iso_file.get_version():
            raise InstallMediaError("invalid install ISO file, version not match")
        if self._ts.edition not in install_iso_file.get_editions():
            raise InstallMediaError("invalid install ISO file, edition not match")
        if self._ts.lang not in install_iso_file.get_languages():
            raise InstallMediaError("invalid install ISO file, language not match")

        # do work
        if self._ts.version in [Version.WINDOWS_98, Version.WINDOWS_XP, Version.WINDOWS_7]:
            floppyFile = os.path.join(self._workDirObj.path, "floppy.img")
            Util.createFormattedFloppy(floppyFile)
            with TmpMount(floppyFile) as mp:
                AnswerFileGenerator(self._ts).generateFile(mp.mountpoint)

            self._workDirObj.save_record("custom-install-media", json.dumps({
                "install-iso-filepath": install_iso_file.get_path(),
                "floppy-filename": os.path.basename(floppyFile),
            }))
        else:
            assert False

    @Action(BuildStep.CUSTOM_INSTALL_MEDIA_PREPARED)
    def action_install_windows(self):
        installIsoFile = None
        floppyFile = None
        if self._ts.version in [Version.WINDOWS_98, Version.WINDOWS_XP, Version.WINDOWS_7]:
            savedRecord = json.loads(self._workDirObj.load_record("custom-install-media"))
            installIsoFile = savedRecord["install-iso-filepath"]
            floppyFile = os.path.join(self._workDirObj.path, savedRecord["floppy-filename"])
        else:
            assert False

        vm = VmUtil.getBootstrapVm(self._ts.arch, self._ts.version, self._ts.edition, self._ts.lang, self._workDirObj.image_filepath, installIsoFile, floppyFile)
        vm.start(show=True)
        self._workDirObj.save_qemu_cmd_record(vm.get_qemu_command())
        vm.wait_until_stop()

    @Action(BuildStep.MSWIN_INSTALLED)
    def action_install_core_applications(self):
        pass

    @Action(BuildStep.MSWIN_INSTALLED, BuildStep.CORE_APPS_INSTALLED)
    def action_install_extra_applications(self):
        pass

    @Action(BuildStep.MSWIN_INSTALLED, BuildStep.CORE_APPS_INSTALLED, BuildStep.EXTRA_APPS_INSTALLED)
    def action_customize_system(self, custom_script_list=[]):
        assert all([isinstance(s, ScriptInChroot) for s in custom_script_list])

        if len(custom_script_list) > 0:
            with Vm() as m:
                for s in custom_script_list:
                    m.script_exec(s, quiet=self._getQuiet())

    @Action(BuildStep.MSWIN_INSTALLED, BuildStep.CORE_APPS_INSTALLED, BuildStep.EXTRA_APPS_INSTALLED, BuildStep.SYSTEM_CUSTOMIZED)
    def action_cleanup(self):
        pass

    def _getQuiet(self):
        return (self._s.verbose_level == 0)
