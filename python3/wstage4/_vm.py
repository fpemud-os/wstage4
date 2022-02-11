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


import subprocess
from ._util import Util
from ._const import Arch, Variant, Lang


class Vm:

    @staticmethod
    def create_main_disk(arch, variant, lang, path):
        with open(path, 'wb') as f:
            f.truncate(_getDiskSize(arch, variant, lang) * 1000 * 1000 * 1000)

    def __init__(self, arch, variant, lang, main_disk_filepath, boot_iso_filepath=None):
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

        # disk interface
        if variant in [Variant.WINDOWS_XP_HOME, Variant.WINDOWS_XP_PROFESSIONAL]:
            self._mainDiskInterface = "ide"
        else:
            self._mainDiskInterface = "scsi"

        # main disk file path
        self._diskPath = main_disk_filepath

        # boot iso file path, can be None
        self._bootFile = boot_iso_filepath

        # FIXME
        self._scriptDirList = []

        self._pid = None
        self._qmpPort = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    def is_running(self):
        return self._pid is not None

    def start(self):
        try:
            self._qmpPort = Util.getFreeTcpPort()
            self._pid = subprocess.Popen(self._generateQemuCommand(), shell=True)
        except BaseException:
            self.stop()
            raise

    def stop(self, remove_scripts=True):
        if self._pid is not None:
            # send to qmp shutdown machine
            self._pid = None
            self._qmpPort = None

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
            cmd += " -qmp \"tcp:127.0.0.1:%d,server,nowait\"" % (self._qmpPort)

        return cmd


def _getDiskSize(arch, variant, lang):
    # disk size (10G)
    return 10
