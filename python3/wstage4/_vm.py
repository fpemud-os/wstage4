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
import subprocess
from ._util import Util
from ._const import Arch, Category, Edition, Lang


class Vm:

    def __init__(self, main_disk_filepath):
        data = None
        with open(main_disk_filepath, "rb") as f:
            f.seek(512)
            data = Util.readUntil(f, '\n\0', max=512, bTextOrBinary=False)

        data = json.loads(data.decode("iso8859-1"))
        self._init(data["arch"], data["category"], data["edition"], data["lang"], main_disk_filepath, None)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    def is_running(self):
        return self._proc is not None

    def start(self):
        try:
            self._qmpPort = Util.getFreeTcpPort()
            self._proc = subprocess.Popen(self._generateQemuCommand(), shell=True)
        except BaseException:
            self.stop()
            raise

    def stop(self, remove_scripts=True):
        if self._proc is not None:
            # send to qmp shutdown machine
            self._proc = None
            self._qmpPort = None

    def wait(self):
        self._proc.wait()
        self._proc = None
        self._qmpPort = None

    def _init(self, arch, category, edition, lang, mainDiskFile, bootIsoFile):
        # vm type
        if category in [Category.WINDOWS_XP]:
            self._qemuVmType = "pc"
        elif category in [Category.WINDOWS_7]:
            self._qemuVmType = "q35"
        else:
            assert False

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
        if category in [Category.WINDOWS_98, Category.WINDOWS_XP]:
            self._mainDiskInterface = "ide"
        elif category in [Category.WINDOWS_7]:
            self._mainDiskInterface = "scsi"
        else:
            assert False

        # main disk file path
        self._diskPath = mainDiskFile

        # boot iso file path, can be None
        self._bootFile = bootIsoFile

        # runtime variables
        self._proc = None
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
        if os.getuid() == 0:
            # non-priviledged user can use us with a performance pernalty
            cmd += " -enable-kvm"
        cmd += " -no-user-config"
        # cmd += " -nodefaults"
        cmd += " -machine %s,usb=on" % (self._qemuVmType)

        # platform device
        cmd += " -cpu host"
        cmd += " -smp 1,sockets=1,cores=%d,threads=1" % (self._cpuNumber)
        cmd += " -m %s" % (self._memorySize)
        cmd += " -rtc base=localtime"

        # boot-iso-file
        if self._bootFile is not None:
            cmd += " -drive \'file=%s,if=none,id=boot-cdrom,readonly=on,format=raw\'" % (self._bootFile)
            cmd += " -device ide-cd,bus=ide.1,unit=0,drive=boot-cdrom,id=boot-cdrom,bootindex=1"

        # main-disk
        if True:
            cmd += " -drive \'file=%s,if=none,id=main-disk,format=raw\'" % (self._diskPath)
            if self._mainDiskInterface == "ide":
                cmd += " -device ide-hd,bus=ide.0,unit=0,drive=main-disk,id=main-disk,bootindex=2"
            elif self._mainDiskInterface == "scsi":
                cmd += " -device virtio-blk-pci,scsi=off,bus=%s,addr=0x%02x,drive=main-disk,id=main-disk,bootindex=2" % (pciBus, pciSlot)        # FIXME
                pciSlot += 1
            else:
                assert False

        # graphics device
        cmd += " -display gtk"
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


class VmUtil:

    @staticmethod
    def getBootstrapVm(arch, category, edition, lang, mainDiskPath, bootIsoFile):
        buf = json.dumps({
            "arch": arch,
            "category": category,
            "edition": edition,
            "lang": lang,
        }) + "\n"

        with open(mainDiskPath, 'wb') as f:
            f.truncate(VmUtil.getMainDiskSize(arch, edition, lang) * 1000 * 1000 * 1000)
            if True:
                f.seek(512)
                f.write(buf.encode("iso8859-1"))

        ret = Vm.__new__(Vm)
        ret._init(arch, category, edition, lang, mainDiskPath, bootIsoFile)
        return ret

    @staticmethod
    def getMainDiskSize(arch, edition, lang):
        # disk size (10G)
        return 10
