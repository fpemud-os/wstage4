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
import platform
import robust_layer.simple_fops
from ._util import Util
from ._const import Arch, Variant, Lang


class VmBuilder:

    def createVm(self, arch, variant, lang, dstDir):
        # vm type
        self._qemuVmType = "pc"

        # cpu number
        self._cpuNumber = 1

        # memory size
        if arch == Arch.X86:
            self._memorySize = "1G"
        elif arch == Arch.X86_64:
            self._memorySize = "4G"
        else:
            assert False

        # disk image file name
        self._diskFile = os.path.join(dstDir, "disk-main.img")

        # disk size (10G)
        self._diskSize = 10

        # disk interface
        if variant in [Variant.WINDOWS_XP_HOME, Variant.WINDOWS_XP_PROFESSIONAL]:
            self._mainDiskInterface = "ide"
        else:
            self._mainDiskInterface = "scsi"

        # create virtual machine disk image file
        with open(self._diskFile, 'wb') as f:
            f.truncate(self._diskSize * 1000 * 1000 * 1000)

        # create virtual machine start script
        with open(os.path.join(dstDir, "vm.sh"), "w") as f:
            f.write(self._generateQemuCommand())
            f.write("\n")

    def _generateQemuCommand(self):
        """pci slot allcation:
                slot 0x0.0x0:    host bridge
                slot 0x1.0x0:    ISA bridge
                slot 0x1.0x1;    IDE controller
                slot 0x1.0x2:    USB controller
                slot 0x2.0x0:    VGA controller
                slot 0x3.0x0:    SCSI controller, main-disk"""

        if self._qemuVmType == "pc":
            pciBus = "pci.0"
            pciSlot = 3
        elif self._qemuVmType == "q35":
            pciBus = "pcie.0"
            pciSlot = 3
        else:
            assert False

        cmd = "/usr/bin/qemu-system-x86_64"
        cmd += " -enable-kvm"
        cmd += " -no-user-config"
        cmd += " -nodefaults"
        cmd += " -machine %s,usb=on" % (self._qemuVmType)

        # platform device
        cmd += " -cpu host"
        cmd += " -smp 1,sockets=1,cores=%d,threads=1" % (self._cpuNumber)
        cmd += " -m %d" % (self._memorySize)
        cmd += " -rtc base=localtime"

        # main-disk
        if True:
            cmd += " -drive \'file=%s,if=none,id=main-disk,format=%s\'" % (self._diskFile, "raw")
            if self._mainDiskInterface == "ide":
                cmd += " -device ide-hd,bus=ide.0,unit=0,drive=main-disk,id=main-disk,bootindex=1"
            elif self._mainDiskInterface == "scsi":
                cmd += " -device virtio-blk-pci,scsi=off,bus=%s,addr=0x%02x,drive=main-disk,id=main-disk,bootindex=1" % (pciBus, pciSlot)        # fixme
            else:
                assert False
            pciSlot += 1

    #     # graphics device
    #     if True:
    #         if self._graphicsAdapterInterface == "qxl":
    #             assert self.spicePort != -1
    #             cmd += " -spice port=%d,addr=127.0.0.1,disable-ticketing,agent-mouse=off" % (self.spicePort)
    #             cmd += " -vga qxl -global qxl-vga.ram_size_mb=64 -global qxl-vga.vram_size_mb=64"
    # #            cmd += " -device qxl-vga,bus=%s,addr=0x04,ram_size_mb=64,vram_size_mb=64"%(pciBus)                        # see https://bugzilla.redhat.com/show_bug.cgi?id=915352
    #         else:
    #             assert self.spicePort != -1
    #             cmd += " -spice port=%d,addr=127.0.0.1,disable-ticketing,agent-mouse=off" % (self.spicePort)
    #             cmd += " -device VGA,bus=%s,addr=0x%02x" % (pciBus, pciSlot)
    #         pciSlot += 1

        # network device
        if True:
            cmd += " -netdev user,id=eth0"
            cmd += " -device rtl8139,netdev=eth0,bus=%s,addr=0x%02x,romfile=" % (pciBus, pciSlot)
            pciSlot += 1

        # monitor interface
        if True:
            cmd += " -qmp \"tcp:127.0.0.1:%d,server,nowait\"" % (self.qmpPort)

        return cmd


class Vm:

    def __init__(self, image_file, boot_iso_file=None):
        self._diskPath = image_file
        self._bootFile = boot_iso_file

        self._scriptDirList = []

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    def is_running(self):
        pass

    def start(self):
        pass

    def stop(self, remove_scripts=True):
        pass

    def interactive_shell(self):
        assert len(self._mountList) > 0

        cmd = "bash"       # FIXME: change to read shell
        return Util.shellExec("chroot \"%s\" %s" % (self._dir, cmd))

    def shell_call(self, env, cmd):
        # "CLEAN_DELAY=0 emerge -C sys-fs/eudev" -> "CLEAN_DELAY=0 chroot emerge -C sys-fs/eudev"
        assert len(self._mountList) > 0

        # FIXME
        env = "LANG=C.utf8 PATH=/bin:/usr/bin:/sbin:/usr/sbin " + env
        assert self._detectArch() == platform.machine()

        return Util.shellCall("%s chroot \"%s\" %s" % (env, self._dir, cmd))

    def shell_test(self, env, cmd):
        assert len(self._mountList) > 0

        # FIXME
        env = "LANG=C.utf8 PATH=/bin:/usr/bin:/sbin:/usr/sbin " + env
        assert self._detectArch() == platform.machine()

        return Util.shellCallTestSuccess("%s chroot \"%s\" %s" % (env, self._dir, cmd))

    def shell_exec(self, env, cmd, quiet=False):
        assert len(self._mountList) > 0

        # FIXME
        env = "LANG=C.utf8 PATH=/bin:/usr/bin:/sbin:/usr/sbin " + env
        assert self._detectArch() == platform.machine()

        if not quiet:
            Util.shellExec("%s chroot \"%s\" %s" % (env, self._dir, cmd))
        else:
            Util.shellCall("%s chroot \"%s\" %s" % (env, self._dir, cmd))

    def script_exec(self, scriptObj, quiet=False):
        assert len(self._mountList) > 0

        path = os.path.join("/var", "tmp", "script_%d" % (len(self._scriptDirList)))
        hostPath = os.path.join(self._dir, path[1:])

        assert not os.path.exists(hostPath)
        os.makedirs(hostPath, mode=0o755)
        self._scriptDirList.append(hostPath)

        if not quiet:
            print(scriptObj.get_description())
        scriptObj.fill_script_dir(hostPath)
        self.shell_exec("", "sh -c \"cd %s ; ./%s\"" % (path, scriptObj.get_script()), quiet)

    def _unbind(self, remove_scripts):
        assert isinstance(remove_scripts, bool)

        for fullfn in reversed(self._mountList):
            if os.path.exists(fullfn) and Util.isMount(fullfn):
                Util.cmdCall("umount", "-l", fullfn)
        self._mountList = []

        robust_layer.simple_fops.rm(os.path.join(self._dir, "etc", "resolv.conf"))

        if remove_scripts:
            for hostPath in reversed(self._scriptDirList):
                robust_layer.simple_fops.rm(hostPath)
        self._scriptDirList = []

    def _detectArch(self):
        # FIXME: use profile function of pkgwh to get arch from CHOST
        return "x86_64"
