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
import robust_layer.simple_fops
from ._util import Util, TmpMount
from ._const import Category
from ._prototype import ScriptInChroot
from ._errors import SettingsError, InstallMediaError
from ._settings import Settings, TargetSettings
from ._vm import Vm, VmUtil
from ._win_install_media import InstallMedia
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
    MSWIN_EXTRA_ADDONS_INSTALLED = enum.auto()
    APPLICATIONS_INSTALLED = enum.auto()
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

        self._addonRepo = AddonRepo(self._ts.arch, self._ts.category, self._ts.edition, self._ts.lang)
        for i in self._ts.addons:
            if i not in self._addonRepo.getAddonNames():
                raise SettingsError("invalid addon %s" % (i))

        self._workDirObj = work_dir

        self._progress = BuildStep.INIT

    def get_progress(self):
        return self._progress

    @Action(BuildStep.INIT)
    def action_prepare_custom_install_media(self, path):
        m = InstallMedia(path)
        try:
            # check install media
            if self._ts.arch != m.getArch():
                raise InstallMediaError("invalid install media, arch not match")
            if self._ts.category != m.getCategory():
                raise InstallMediaError("invalid install media, category not match")
            if self._ts.edition not in m.getVariantList():
                raise InstallMediaError("invalid install media, edition not match")
            if self._ts.lang not in m.getLangList():
                raise InstallMediaError("invalid install media, language not match")

            # do work
            if self._ts.category in [Category.WINDOWS_98, Category.WINDOWS_XP, Category.WINDOWS_7]:
                floppyFile = os.path.join(self._workDirObj.path, "floppy.img")
                Util.createFormattedFloppy(floppyFile)
                with TmpMount(floppyFile) as mp:
                    AnswerFileGenerator(self._ts).generateFile(mp.mountpoint)

                self._workDirObj.save_record("custom-install-media", json.dumps({
                    "install-iso-filepath": path,
                    "floppy-filename": os.path.basename(floppyFile),
                }))
            else:
                assert False
        finally:
            m.dispose()

    @Action(BuildStep.CUSTOM_INSTALL_MEDIA_PREPARED)
    def action_install_windows(self):
        installIsoFile = None
        floppyFile = None
        if self._ts.category in [Category.WINDOWS_98, Category.WINDOWS_XP, Category.WINDOWS_7]:
            savedRecord = json.loads(self._workDirObj.load_record("custom-install-media"))
            installIsoFile = savedRecord["install-iso-filepath"]
            floppyFile = os.path.join(self._workDirObj.path, savedRecord["floppy-filename"])
        else:
            assert False

        with VmUtil.getBootstrapVm(self._ts.arch, self._ts.category, self._ts.edition, self._ts.lang, self._workDirObj.image_filepath, installIsoFile, floppyFile, cmdFile=self._workDirObj.qemu_cmd_filepath) as vm:
            vm.wait()

    @Action(BuildStep.MSWIN_INSTALLED)
    def action_install_windows_extra_addons(self):
        vm = Vm(self._workDirObj.image_filepath, cmd_file=self._workDirObj.qemu_cmd_filepath)

    @Action(BuildStep.MSWIN_INSTALLED, BuildStep.MSWIN_EXTRA_ADDONS_INSTALLED)
    def action_install_applications(self):
        pass

    @Action(BuildStep.MSWIN_INSTALLED, BuildStep.MSWIN_EXTRA_ADDONS_INSTALLED, BuildStep.APPLICATIONS_INSTALLED)
    def action_customize_system(self, custom_script_list=[]):
        assert all([isinstance(s, ScriptInChroot) for s in custom_script_list])

        if len(custom_script_list) > 0:
            with _MyVm(self) as m:
                for s in custom_script_list:
                    m.script_exec(s, quiet=self._getQuiet())

    @Action(BuildStep.MSWIN_INSTALLED, BuildStep.MSWIN_EXTRA_ADDONS_INSTALLED, BuildStep.APPLICATIONS_INSTALLED, BuildStep.SYSTEM_CUSTOMIZED)
    def action_cleanup(self):
        pass

    def _getQuiet(self):
        return (self._s.verbose_level == 0)


class _MyVm(Vm):

    def __init__(self, arch, edition, lang):
        super().__init__(arch, edition, lang)

    def bind(self):
        super().bind()
        try:
            t = TargetFilesAndDirs(self._w.chroot_dir_path)

            # log directory mount point
            if self._p._s.log_dir is not None:
                assert os.path.exists(t.logdir_hostpath) and not Util.isMount(t.logdir_hostpath)
                Util.shellCall("mount --bind \"%s\" \"%s\"" % (self._p._s.log_dir, t.logdir_hostpath))
                self._bindMountList.append(t.logdir_hostpath)

            # distdir mount point
            if self._p._s.host_distfiles_dir is not None:
                assert os.path.exists(t.distdir_hostpath) and not Util.isMount(t.distdir_hostpath)
                Util.shellCall("mount --bind \"%s\" \"%s\"" % (self._p._s.host_distfiles_dir, t.distdir_hostpath))
                self._bindMountList.append(t.distdir_hostpath)

            # pkgdir mount point
            if self._p._s.host_packages_dir is not None:
                assert os.path.exists(t.binpkgdir_hostpath) and not Util.isMount(t.binpkgdir_hostpath)
                Util.shellCall("mount --bind \"%s\" \"%s\"" % (self._p._s.host_packages_dir, t.binpkgdir_hostpath))
                self._bindMountList.append(t.binpkgdir_hostpath)

            # ccachedir mount point
            if self._p._s.host_ccache_dir is not None and os.path.exists(t.ccachedir_hostpath):
                assert os.path.exists(t.ccachedir_hostpath) and not Util.isMount(t.ccachedir_hostpath)
                Util.shellCall("mount --bind \"%s\" \"%s\"" % (self._p._s.host_ccache_dir, t.ccachedir_hostpath))
                self._bindMountList.append(t.ccachedir_hostpath)

            # mount points for MountRepository
            for myRepo in _MyRepoUtil.scanReposConfDir(self._w.chroot_dir_path):
                mp = myRepo.get_mount_params()
                if mp is not None:
                    assert os.path.exists(myRepo.datadir_hostpath) and not Util.isMount(myRepo.datadir_hostpath)
                    Util.shellCall("mount \"%s\" \"%s\" -o %s" % (mp[0], myRepo.datadir_hostpath, (mp[1] + ",ro") if mp[1] != "" else "ro"))
                    self._bindMountList.append(myRepo.datadir_hostpath)
        except BaseException:
            self.unbind(remove_scripts=False)
            raise

    def unbind(self):
        for fullfn in reversed(self._bindMountList):
            Util.cmdCall("umount", "-l", fullfn)
        self._bindMountList = []
        super().unbind()
