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
from ._const import Arch, Category, Edition, Lang


class AnswerFileGenerator:

    def __init__(self, target_settings):
        self._ts = target_settings

    def generateFile(self, path):
        if self._ts.category == Category.WINDOWS_98:
            obj = AnswerFileGeneratorForWindows98()
            obj.generateFile(self._ts, path)
        elif self._ts.category == Category.WINDOWS_XP:
            obj = AnswerFileGeneratorForWindowsXP()
            obj.generateFile(self._ts, path)
        elif self._ts.category == Category.WINDOWS_VISTA:
            # FIXME
            assert False
        elif self._ts.category == Category.WINDOWS_7:
            obj = AnswerFileGeneratorForWindows7()
            obj.generateFile(self._ts, path)
        elif self._ts.category == Category.WINDOWS_8:
            # FIXME
            assert False
        elif self._ts.category == Category.WINDOWS_8_1:
            # FIXME
            assert False
        elif self._ts.category == Category.WINDOWS_10:
            # FIXME
            assert False
        elif self._ts.category == Category.WINDOWS_11:
            # FIXME
            assert False
        elif self._ts.category == Category.WINDOWS_SERVER_2008:
            # FIXME
            assert False
        elif self._ts.category == Category.WINDOWS_SERVER_2012:
            # FIXME
            assert False
        elif self._ts.category == Category.WINDOWS_SERVER_2016:
            # FIXME
            assert False
        elif self._ts.category == Category.WINDOWS_SERVER_2019:
            # FIXME
            assert False
        else:
            assert False

    def updateIso(self, isoObj):
        if self._ts.category == Category.WINDOWS_98:
            assert False
        elif self._ts.category == Category.WINDOWS_XP:
            assert False
        elif self._ts.category == Category.WINDOWS_VISTA:
            assert False
        elif self._ts.category == Category.WINDOWS_7:
            assert False
        elif self._ts.category == Category.WINDOWS_8:
            assert False
        elif self._ts.category == Category.WINDOWS_8_1:
            assert False
        elif self._ts.category == Category.WINDOWS_10:
            assert False
        elif self._ts.category == Category.WINDOWS_11:
            assert False
        elif self._ts.category == Category.WINDOWS_SERVER_2008:
            assert False
        elif self._ts.category == Category.WINDOWS_SERVER_2012:
            assert False
        elif self._ts.category == Category.WINDOWS_SERVER_2016:
            assert False
        elif self._ts.category == Category.WINDOWS_SERVER_2019:
            assert False
        else:
            assert False


class AnswerFileGeneratorForWindows98:

    def generateFile(self, ts, dstDir):
        fn, buf = self._get_filename_and_buffer(ts)
        with open(os.path.join(dstDir, fn), "wb") as f:
            f.write(buf)

    def updateIso(self, ts, isoObj):
        fn, buf = self._get_filename_and_buffer(ts)

        # release some space, pycdlib sucks that it can't make iso file bigger when adding files
        if isoObj.exists(joliet_path="/cdsample"):
            isoObj.del_dir(joliet_path="/cdsample")
        if isoObj.exists(joliet_path="/add-ons"):
            isoObj.del_dir(joliet_path="/add-ons")
        isoObj.del_file(joliet_path="/readme.txt")
        isoObj.del_file(joliet_path="/setuptip.txt")

        # write target file
        fn = "/" + fn
        isoObj.add_file(joliet_path=fn, iso_path=fn.upper(), file_content=buf)

    @staticmethod
    def _get_filename_and_buffer(ts):
        # from https://www.tek-tips.com/viewthread.cfm?qid=612507

        if ts.product_key is None:
            key = _Util.getDefaultProductKeyByEdition(ts.arch, ts.category, ts.edition, ts.lang)
        else:
            key = ts.product_key

        timezone = "GMT"
        # FIXME: get timezone by lang

        buf = ""
        buf += "[Setup]\n"
        buf += "Express=1\n"                            # what does it mean?
        # buf += 'InstallDir="c:\windows"\n'
        buf += "InstallType=3\n"                        # what does it mean?
        buf += 'ProductKey="%s"\n' % (key)
        buf += "EBD=0\n"                                # what does it mean?
        buf += "ShowEula=0\n"                           # no effect?
        buf += "ChangeDir=0\n"                          # what does it mean?
        buf += "OptionalComponents=1\n"                 # what does it mean?
        buf += "Network=1\n"                            # what does it mean?
        buf += "System=0\n"                             # what does it mean?
        buf += "CCP=0\n"                                # what does it mean?
        buf += "CleanBoot=0\n"                          # what does it mean?
        buf += "Display=0\n"                            # what does it mean?
        buf += "DevicePath=0\n"                         # what does it mean?
        buf += "NoDirWarn=1\n"                          # what does it mean?
        buf += 'TimeZone="%s"\n' % (timezone)
        buf += "Uninstall=0\n"                          # what does it mean?
        buf += "NoPrompt2Boot=0\n"                      # here 0 means "do not prompt user". Sigh.
        # buf += "VRC=0\n"
        # buf += "PenWinWarning=0\n"

        return ("msbatch.inf", buf.encode("iso8859-1"))

        # [System]
        # Display="VBE Miniport" ; Comes from vbemp.inf
        # Monitor="QEMU Monitor"
        # DisplChar=24,1024,768 ; 16.7 million colors (24-bit) 1024 x 768
        # Locale=L0409
        # SelectedKeyboard=KEYBOARD_00000409
        #
        # [NameAndOrg]
        # Name="Retro User"
        # Org="Visual 2000"
        # Display=0
        #
        # [Network]
        # ComputerName="Paschke"
        # Workgroup="WORKGROUP"
        # Description="Just a generated image."
        # Display=0
        # PrimaryLogon=VREDIR
        # Clients=VREDIR
        # Protocols=MSTCP
        # Security=SHARE
        #
        # [MSTCP]
        # LMHOSTS=0
        # DHCP=1
        # DNS=0
        # WINS=D
        #
        # [VREDIR]
        # ValidatedLogon=0
        #
        # [OptionalComponents]
        # "Accessibility Options"=0
        # "Accessibility Tools"=0
        # "Briefcase"=1
        # "Calculator"=1
        # "Desktop Wallpaper"=1
        # "Document Templates"=0
        # "Games"=1
        # "Imaging"=0
        # "Mouse Pointers"=0
        # "Paint"=1
        # "Quick View"=0
        # "Windows Scripting Host"=1
        # "WordPad"=1
        # "Address Book"=0
        # "Dial-Up ATM Support"=0
        # "Dial-Up Networking"=0
        # "Dial-Up Server"=0
        # "Direct Cable Connection"=0
        # "HyperTerminal"=0
        # "Microsoft Chat 2.5"=0
        # "NetMeeting"=0
        # "Phone Dialer"=0
        # "Virtual Private Networking"=0
        # "Baseball"=0
        # "Dangerous Creatures"=0
        # "Inside your Computer"=0
        # "Jungle"=0
        # "Leonardo da Vinci"=1
        # "More Windows"=0
        # "Mystery"=0
        # "Nature"=0
        # "Science"=1
        # "Space"=0
        # "Sports"=0
        # "The 60's USA"=0
        # "The Golden Era"=0
        # "Travel"=0
        # "Underwater"=0
        # "Windows 98"=0
        # "Desktop Themes Support"=0
        # "Internet Connection Sharing"=0
        # "Microsoft Wallet"=0
        # "Personal Web Server"=0
        # "Web Publishing Wizard"=0
        # "Web-Based Enterprise Mgmt"=0
        # "Microsoft Outlook Express"=0
        # "Baltic"=0
        # "Central European"=0
        # "Cyrillic"=0
        # "Greek"=0
        # "Turkish"=0
        # "Audio Compression"=0
        # "CD Player"=0
        # "Macromedia Shockwave Director"=0
        # "Macromedia Shockwave Flash"=0
        # "Multimedia Sound Schemes"=0
        # "Sample Sounds"=0
        # "Sound Recorder"=0
        # "Video Compression"=0
        # "Volume Control"=0
        # "America Online"=0
        # "AT&T WorldNet Service"=0
        # "CompuServe"=0
        # "Prodigy Internet"=0
        # "The Microsoft Network"=0
        # "Additional Screen Savers"=0
        # "Flying Windows"=1
        # "OpenGL Screen Savers"=0
        # "Backup"=0
        # "Character Map"=0
        # "Clipboard Viewer"=0
        # "Disk compression tools"=0
        # "Drive Converter (FAT32)"=0
        # "Group policies"=0
        # "Net Watcher"=0
        # "System Monitor"=0
        # "System Resource Meter"=0
        # "Web TV for Windows"=0
        # "WaveTop Data Broadcasting"=0
        #
        # [Printers]
        #
        # [InstallLocationsMRU]
        #
        # [Install]
        # AddReg=RunOnce.BatchDelay,Run.Installed.Components,Skip.PCMCIA.Wizard,Registry.WinUpdate,RunOnce.PaschkeRuntimes,RegistrySettings
        #
        # [RunOnce.BatchDelay]
        # HKLM,%KEY_RUNONCE%,BatchRun1,,"%25%\rundll.exe setupx.dll,InstallHinfSection Delete.MSN.Icon 4 %1%\msbatch.inf"
        # HKLM,%KEY_RUNONCE%,BatchRun2,,"%25%\rundll.exe setupx.dll,InstallHinfSection Delete.Welcome 4 %1%\msbatch.inf"
        # HKLM,%KEY_RUNONCE%,BatchRun3,,"%25%\rundll.exe setupx.dll,InstallHinfSection Delete.Regwiz 4 %1%\msbatch.inf"
        #
        # [Run.Installed.Components]
        # HKLM,%KEY_INSTALLEDCOMPS%\>BatchSetupx,,,">Batch 98 - General Settings"
        # HKLM,%KEY_INSTALLEDCOMPS%\>BatchSetupx,IsInstalled,1,01,00,00,00
        # HKLM,%KEY_INSTALLEDCOMPS%\>BatchSetupx,Version,,"3,0,0,0"
        # HKLM,%KEY_INSTALLEDCOMPS%\>BatchSetupx,StubPath,,"%25%\rundll.exe setupx.dll,InstallHinfSection Installed.Components.General 4 %1%\MSBATCH.INF"
        # HKLM,%KEY_INSTALLEDCOMPS%\BatchSetupx,,,"ICW"
        # HKLM,%KEY_INSTALLEDCOMPS%\BatchSetupx,IsInstalled,1,01,00,00,00
        # HKLM,%KEY_INSTALLEDCOMPS%\BatchSetupx,Version,,"3,0,0,0"
        # HKLM,%KEY_INSTALLEDCOMPS%\BatchSetupx,StubPath,,"%24%\progra~1\intern~1\connec~1\icwconn1 /restoredesktop
        # HKLM,%KEY_INSTALLEDCOMPS%\>BatchAdvpack,,,">Batch 98 - Advanced Settings"
        # HKLM,%KEY_INSTALLEDCOMPS%\>BatchAdvpack,IsInstalled,1,01,00,00,00
        # HKLM,%KEY_INSTALLEDCOMPS%\>BatchAdvpack,Version,,"3,0,0,0"
        # HKLM,%KEY_INSTALLEDCOMPS%\>BatchAdvpack,StubPath,,"%25%\rundll32.exe advpack.dll,LaunchINFSection %1%\MSBATCH.INF,Installed.Components.Advanced"
        # HKLM,%KEY_INSTALLEDCOMPS%\>Batchwu,,,">Batch 98 - Windows Update"
        # HKLM,%KEY_INSTALLEDCOMPS%\>Batchwu,IsInstalled,1,01,00,00,00
        # HKLM,%KEY_INSTALLEDCOMPS%\>Batchwu,Version,,"3,0,0,0"
        # HKLM,%KEY_INSTALLEDCOMPS%\>Batchwu,StubPath,,"wupdmgr.exe -shortcut"
        #
        # [Installed.Components.General]
        # AddReg=Shell.Prep
        # BitReg=Shell.Settings
        #
        # [DelOEdesktop]
        # setup.ini, progman.groups,, "groupOE=..\..\desktop"
        # setup.ini, groupOE,, """Outlook Express"""                ;deletes icon
        #
        # [Installed.Components.Advanced]
        # DelFiles=OLS.Icons, QuickLaunch.Icons
        # CustomDestination=Custom.Dest
        # RunPostSetupCommands=DirCleanup
        #
        # [Custom.Dest]
        # 49070=DesktopLDIDSection,5
        # 49050=QuickLinksLDIDSection,5
        #
        # [Delete.MSN.Icon]
        # DelReg=MSN.Icon
        #
        # [MSN.Icon]
        # HKLM,SOFTWARE\Microsoft\Windows\CurrentVersion\explorer\Desktop\NameSpace\{4B876A40-4EE8-11D1-811E-00C04FB98EEC},,,
        #
        # [DesktopLDIDSection]
        # HKCU,"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders",Desktop,OLSFolder,"%25%\Desktop"
        #
        # [OLS.Icons]
        # americ~1.lnk
        # at&two~1.lnk
        # compus~1.lnk
        # prodig~1.lnk
        # themic~1.lnk
        # aboutt~1.lnk
        # abouto~1.txt
        # services.txt
        #
        # [DirCleanup]
        # rundll32.exe advpack.dll,DelNodeRunDLL32 %49070%\%OnlineLong%
        #
        # [Delete.Welcome]
        # DelReg=Registry.Welcome
        #
        # [Registry.Welcome]
        # HKLM,Software\Microsoft\Windows\CurrentVersion\Run,Welcome,,
        #
        # [Delete.Regwiz]
        # AddReg=Registry.Regwiz
        #
        # [Registry.Regwiz]
        # HKLM,Software\Microsoft\Windows\CurrentVersion\Welcome\Regwiz,@,1,01,00,00,00
        # HKLM,Software\Microsoft\Windows\CurrentVersion,RegDone,1,01,00,00,00
        #
        # [Registry.WinUpdate]
        # HKLM,Software\Microsoft\Windows\CurrentVersion\Policies\Explorer,NoDevMgrUpdate,0x10001,1
        # HKLM,Software\Microsoft\Windows\CurrentVersion\Policies\Explorer,NoWindowsUpdate,0x10001,1
        #
        # [Shell.Prep]
        # HKCU,"Software\Microsoft\Internet Explorer\Desktop\Components\0",Flags,01,00,00,00
        # HKCU,"Software\Microsoft\Internet Explorer\main",Show_ChannelBand,0,"no"
        #
        # [Shell.Settings]
        # HKCU,"Software\Microsoft\Internet Explorer\Desktop\Components\0",Flags,0,20,1
        #
        # [QuickLinksLDIDSection]
        # HKCU,"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders",AppData,QuickLaunch,"%25%\Application Data"
        #
        # [QuickLaunch.Icons]
        # viewch~1.scf
        #
        # [Skip.PCMCIA.Wizard]
        # HKLM,System\CurrentControlSet\Services\Class\PCMCIA,SkipWizardForBatchSetup,,1
        #
        # [DestinationDirs]
        # OLS.Icons=49070,Online~1
        # QuickLaunch.Icons=49050,Micros~1\Intern~1\QuickL~1
        #
        # [Strings]
        # KEY_RUNONCE="SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"
        # KEY_INSTALLEDCOMPS="SOFTWARE\Microsoft\Active Setup\Installed Components"
        # OnlineLong="Online Services"
        #
        # [RunOnce.PaschkeRuntimes]
        # HKLM,%KEY_RUNONCE%,BatchVBRUN60,,"%25%\rundll32.exe advpack.dll,LaunchINFSection C:\vbrun60\vbrun60.inf,DefaultInstall"
        # HKLM,%KEY_RUNONCE%,BatchSHORTCUT,,"%13%\cscript.exe C:\SETSTRT.VBS"
        # HKLM,%KEY_RUNONCE%,BatchCLEAN,,"%25%\rundll32.exe advpack.dll,DelNodeRunDLL32 C:\vbrun60"
        #
        # [RegistrySettings]
        # ; The registry files must be located in the
        # ; Windows 98 installation directory.
        # HKLM,%KEY_RUNONCE%,BatchReg1,,"%25%\regedit.exe /s %1%\science.reg"
        # HKLM,%KEY_RUNONCE%,BatchReg2,,"%25%\regedit.exe /s %1%\viewhidd.reg"


class AnswerFileGeneratorForWindowsXP:

    def generateFile(self, ts, dstDir):
        fn, buf = self._get_filename_and_buffer(ts)
        with open(os.path.join(dstDir, fn), "wb") as f:
            f.write(buf)

    def updateIso(self, ts, isoObj):
        fn, buf = self._get_filename_and_buffer(ts)
        isoObj.add_file(udf_path=("/" + fn), file_content=buf)

    @staticmethod
    def _get_filename_and_buffer(ts):
        if ts.product_key is None:
            key = _Util.getDefaultProductKeyByEdition(ts.arch, ts.category, ts.edition, ts.lang)
        else:
            key = ts.product_key

        buf = ""
        buf += "[Data]\n"
        buf += "AutoPartition=0\n"
        buf += "MsDosInitiated=0\n"
        buf += "UnattendedInstall=Yes\n"
        buf += "AutomaticUpdates=No\n"              # disable automatic updates initially
        buf += "\n"
        buf += "[Unattended]\n"
        buf += "UnattendMode=FullUnattended\n"
        buf += "OemPreinstall=No\n"
        buf += "OemSkipEula=Yes\n"
        buf += "FileSystem=NTFS\n"                  # supports NTFS only
        buf += "WaitForReboot=No\n"
        buf += "NoWaitAfterTextMode=1\n"
        buf += "NoWaitAfterGUIMode=1\n"
        buf += "DriverSigningPolicy=Ignore\n"
        buf += "NonDriverSigningPolicy=Ignore\n"
        buf += "Repartition=Yes\n"
        buf += "UnattendSwitch=Yes\n"
        buf += "\n"
        buf += "[GuiUnattended]\n"
        buf += "AdminPassword=*\n"
        buf += "TimeZone=%s\n" % (_Util.getTimezoneCodeByLang(ts.lang))
        buf += "OEMSkipRegional=1\n"
        buf += "OemSkipWelcome=1\n"
        buf += "\n"
        buf += "[UserData]\n"
        buf += "ProductID=%s\n" % (key)
        buf += "ComputerName=*\n"
        buf += "FullName=*\n"
        buf += "OrgName=*\n"
        buf += "\n"
        buf += "[RegionalSettings]\n"
        buf += "LanguageGroup=%s\n" % (_Util.getLanguageGroupCodeByLang(ts.lang))
        buf += "Language=%s\n" % (_Util.getLanguageIdByLang(ts.lang))
        buf += "\n"
        buf += "[Networking]\n"
        buf += "InstallDefaultComponents=Yes\n"
        buf += "\n"
        buf += "[GuiRunOnce]\n"
        buf += "\"shutdown /s /t 60\"\n"

        return ("winnt.sif", buf.encode("iso8859-1"))

        # buf += "EncryptedAdminPassword=No\n"          # FIXME: in [GuiUnattended]
        # buf += "\n"
        # buf += "[Display]\n"
        # buf += "Xresolution=1024\n"
        # buf += "Yresolution=768\n"
        # buf += "\n"
        # buf += "[TapiLocation]\n"
        # buf += "CountryCode=%s\n" % ("86")
        # buf += "AreaCode=%s\n" % ("00")
        # buf += "Dialing=%s\n" % ("Tone")
        # buf += "\n"
        # buf += "[Identification]\n"
        # buf += "JoinWorkgroup=WORKGROUP\n"
        # buf += "\n"


class AnswerFileGeneratorForWindows7:

    def generateFile(self, ts, dstDir):
        fn, buf = self._get_filename_and_buffer(ts)
        with open(os.path.join(dstDir, fn), "wb") as f:
            f.write(buf)

    def updateIso(self, ts, isoObj):
        fn, buf = self._get_filename_and_buffer(ts)
        isoObj.add_file(udf_path=("/" + fn), file_content=buf)

    @staticmethod
    def _get_filename_and_buffer(ts):
        if ts.product_key is None:
            key = _Util.getDefaultProductKeyByEdition(ts.arch, ts.category, ts.edition, ts.lang)
        else:
            key = ts.product_key

        archDict = {
            Arch.X86: "x86",
            Arch.X86_64: "amd64",
        }

        langDict = {
            Lang.en_US: "en-US",
            Lang.zh_CN: "zh-CN",
            Lang.zh_TW: "zh-TW",
        }

        localeCodeDict = {
            Lang.en_US: "1033:00000409",
            Lang.zh_CN: "2052:00000804",
            Lang.zh_TW: "1028:00000404",
        }

        timezoneDict = {
            Lang.en_US: "Eastern Standard Time",
            Lang.zh_CN: "China Standard Time",
            Lang.zh_TW: "China Standard Time",
        }

        buf = """
            <?xml version="1.0" encoding="utf-8"?>
            <unattend xmlns="urn:schemas-microsoft-com:unattend">
                <settings pass="windowsPE">
                    <component name="Microsoft-Windows-International-Core-WinPE" @@component_tag_postfix@@>
                        <SetupUILanguage>
                            <UILanguage>@@pe_lang@@</UILanguage>
                        </SetupUILanguage>
                        <InputLocale>@@pe_input_lang@@</InputLocale>
                        <SystemLocale>@@pe_lang@@</SystemLocale>
                        <UILanguage>@@pe_lang@@</UILanguage>
                        <UserLocale>@@pe_lang@@</UserLocale>
                    </component>
                    <component name="Microsoft-Windows-Setup" @@component_tag_postfix@@>
                        <DiskConfiguration>
                            <Disk>
                                <DiskID>0</DiskID>
                                <WillWipeDisk>true</WillWipeDisk>
                                <CreatePartitions>
                                    <CreatePartition>               <!-- system reserved partition -->
                                        <Order>1</Order>
                                        <Type>Primary</Type>
                                        <Size>100</Size>
                                    </CreatePartition>
                                    <CreatePartition>               <!-- windows partition -->
                                        <Order>2</Order>
                                        <Type>Primary</Type>
                                        <Extend>true</Extend>       <!-- use all remaining space -->
                                    </CreatePartition>
                                </CreatePartitions>
                                <ModifyPartitions>
                                    <ModifyPartition>
                                        <Order>1</Order>
                                        <PartitionID>1</PartitionID>
                                        <Active>true</Active>
                                        <Format>NTFS</Format>
                                        <Label>System Reserved</Label>
                                    </ModifyPartition>
                                    <ModifyPartition>
                                        <Order>2</Order>
                                        <PartitionID>2</PartitionID>
                                        <Format>NTFS</Format>
                                        <Letter>C</Letter>
                                    </ModifyPartition>
                                </ModifyPartitions>
                            </Disk>
                            <WillShowUI>OnError</WillShowUI>
                        </DiskConfiguration>
                        <ImageInstall>
                            <OSImage>
                                <InstallTo>
                                    <DiskID>0</DiskID>
                                    <PartitionID>2</PartitionID>
                                </InstallTo>
                                <WillShowUI>OnError</WillShowUI>
                            </OSImage>
                        </ImageInstall>
                        <UserData>
                            <ProductKey>
                                <WillShowUI>OnError</WillShowUI>
                                <Key>@@product_key@@</Key>
                            </ProductKey>
                            <AcceptEula>true</AcceptEula>
                            <FullName>@@username@@</FullName>
                        </UserData>
                    </component>
                </settings>
                <settings pass="oobeSystem">                        <!-- system Out-Of-Box-Experience -->
                    <component name="Microsoft-Windows-Shell-Setup" @@component_tag_postfix@@>
                        <OOBE>
                            <HideEULAPage>true</HideEULAPage>
                            <ProtectYourPC>1</ProtectYourPC>
                            <NetworkLocation>Other</NetworkLocation>
                        </OOBE>
                        <TimeZone>@@timezone@@</TimeZone>
                        <UserAccounts>
                            <LocalAccounts>
                                <LocalAccount>
                                    <Group>Administrators</Group>
                                    <Name>@@username@@</Name>
                                    <Password>
                                        <Value>@@password@@</Value>
                                        <PlainText>true</PlainText>
                                    </Password>
                                </LocalAccount>
                            </LocalAccounts>
                        </UserAccounts>
                        <FirstLogonCommands>
                            <SynchronousCommand wcm:action="add">
                                <Order>1</Order>
                                <CommandLine>shutdown /s /t 60</CommandLine>
                                <Description>shutdown after install</Description>
                            </SynchronousCommand>
                        </FirstLogonCommands>
                    </component>
                </settings>
                <settings pass="specialize">
                    <component name="Microsoft-Windows-Shell-Setup" @@component_tag_postfix@@>
                        <ComputerName>@@username@@-PC</ComputerName>
                    </component>
                    <!-- disable the welcome window of IE -->
                    <component name="Microsoft-Windows-IE-InternetExplorer" @@component_tag_postfix@@>
                        <DisableAccelerators>true</DisableAccelerators>
                        <DisableOOBAccelerators>true</DisableOOBAccelerators>
                        <SuggestedSitesEnabled>false</SuggestedSitesEnabled>
                        <Home_Page>about:blank</Home_Page>
                    </component>
                </settings>
            </unattend>
        """
#                <cpi:offlineImage cpi:source="catalog:h:/sources/install_windows 7 ultimate.clg" xmlns:cpi="urn:schemas-microsoft-com:cpi" />

        buf = buf.replace("@@component_tag_postfix", " ".join([
                'processorArchitecture="%s"' % (archDict[ts.arch]),
                'publicKeyToken="31bf3856ad364e35"',
                'language="neutral"',
                'versionScope="nonSxS"',
                'xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State"',
                'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
            ])
        )
        buf = buf.replace("@@arch@@", archDict[ts.arch])
        buf = buf.replace("@@pe_lang@@", langDict[Lang.en_US])                  # use fixed PE language, no one reads it ;)
        buf = buf.replace("@@pe_input_lang@@", localeCodeDict[Lang.en_US])      # same above
        buf = buf.replace("@@lang@@", langDict[ts.lang])
        buf = buf.replace("@@username@@", "A")
        buf = buf.replace("@@password@@", "")
        buf = buf.replace("@@product_key@@", key)
        buf = buf.replace("@@timezone@@", timezoneDict[ts.lang])

        return ("autounattend.xml", buf.encode("utf-8"))


class _Util:

    @staticmethod
    def getTimezoneCodeByLang(lang):
        if lang == Lang.en_US:
            return "85"
        elif lang == Lang.zh_CN:
            return "85"
        elif lang == Lang.zh_TW:
            return "85"
        else:
            assert False

    @staticmethod
    def getLanguageGroupCodeByLang(lang):
        d = {
            Lang.en_US: "10",
            Lang.zh_CN: "10",
            Lang.zh_TW: "10",
        }
        return d[lang]

    @staticmethod
    def getLanguageIdByLang(lang):
        # from https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-lcid
        d = {
            Lang.en_US: "00000804",
            Lang.zh_CN: "00000804",
            Lang.zh_TW: "00000804",
        }
        return d[lang]

    @staticmethod
    def getLanguageTagByLang(lang):
        pass

    @staticmethod
    def getDefaultProductKeyByEdition(arch, category, edition, lang):
        # these are the "public knowledge" abandonware key supplied by Microsoft
        # there may be additional logic in future, so we don't use dict here

        if edition == Edition.WINDOWS_98:
            # ?
            return "F73WT-WHD3J-CD4VR-2GWKD-T38YD"

        if edition == Edition.WINDOWS_98_SE:
            # from https://github.com/visual2000/paschke/blob/master/02runsetup/MSBATCH.INF
            return "F73WT-WHD3J-CD4VR-2GWKD-T38YD"

        if edition == Edition.WINDOWS_XP_HOME:
            # ?
            return "NG4HW-VH26C-733KW-K6F98-J8CK4"

        if arch == Arch.X86 and edition == Edition.WINDOWS_XP_PROFESSIONAL:
            # ?
            return "HCQ9D-TVCWX-X9QRG-J4B2Y-GR2TT"

        if arch == Arch.X86_64 and edition == Edition.WINDOWS_XP_PROFESSIONAL:
            # ?
            return "B66VY-4D94T-TPPD4-43F72-8X4FY"

        if edition == Edition.WINDOWS_7_STARTER:
            # from https://www.windowsafg.com/keys.html
            return "7Q28W-FT9PC-CMMYT-WHMY2-89M6G"

        if edition == Edition.WINDOWS_7_HOME_BASIC:
            # from https://www.windowsafg.com/keys.html
            return "YGFVB-QTFXQ-3H233-PTWTJ-YRYRV"

        if edition == Edition.WINDOWS_7_HOME_PREMIUM:
            # from https://www.windowsafg.com/keys.html
            return "RHPQ2-RMFJH-74XYM-BH4JX-XM76F"

        if edition == Edition.WINDOWS_7_PROFESSIONAL:
            # from https://www.windowsafg.com/keys.html
            return "HYF8J-CVRMY-CM74G-RPHKF-PW487"

        if edition == Edition.WINDOWS_7_ULTIMATE:
            # from https://www.windowsafg.com/keys.html
            return "D4F6K-QK3RD-TMVMJ-BBMRX-3MBMV"

        if edition == Edition.WINDOWS_7_ENTERPRISE:
            # from https://www.windowsafg.com/keys.html
            return "H7X92-3VPBB-Q799D-Y6JJ3-86WC6"

        assert False










# https://www.itsupportguides.com/knowledge-base/windows-7/time-zone-value-for-windows-7-deployment

# 000
# Dateline Standard Time
# (GMT-12:00) International Date Line West

# 001
# Samoa Standard Time
# (GMT-11:00) Midway Island, Samoa

# 002
# Hawaiian Standard Time
# (GMT-10:00) Hawaii

# 003
# Alaskan Standard Time
# (GMT-09:00) Alaska

# 004
# Pacific Standard Time
# (GMT-08:00) Pacific Time (US and Canada); Tijuana

# 010
# Mountain Standard Time
# (GMT-07:00) Mountain Time (US and Canada)

# 013
# Mexico Standard Time 2
# (GMT-07:00) Chihuahua, La Paz, Mazatlan

# 015
# U.S. Mountain Standard Time
# (GMT-07:00) Arizona

# 020
# Central Standard Time
# (GMT-06:00) Central Time (US and Canada)

# 025
# Canada Central Standard Time
# (GMT-06:00) Saskatchewan

# 030
# Mexico Standard Time
# (GMT-06:00) Guadalajara, Mexico City, Monterrey

# 033
# Central America Standard Time
# (GMT-06:00) Central America

# 035
# Eastern Standard Time
# (GMT-05:00) Eastern Time (US and Canada)

# 040
# U.S. Eastern Standard Time
# (GMT-05:00) Indiana (East)

# 045
# S.A. Pacific Standard Time
# (GMT-05:00) Bogota, Lima, Quito

# 050
# Atlantic Standard Time
# (GMT-04:00) Atlantic Time (Canada)

# 055
# S.A. Western Standard Time
# (GMT-04:00) Caracas, La Paz

# 056
# Pacific S.A. Standard Time
# (GMT-04:00) Santiago

# 060
# Newfoundland and Labrador Standard Time
# (GMT-03:30) Newfoundland and Labrador

# 065
# E. South America Standard Time
# (GMT-03:00) Brasilia

# 070
# S.A. Eastern Standard Time
# (GMT-03:00) Buenos Aires, Georgetown

# 073
# Greenland Standard Time
# (GMT-03:00) Greenland

# 075
# Mid-Atlantic Standard Time
# (GMT-02:00) Mid-Atlantic

# 080
# Azores Standard Time
# (GMT-01:00) Azores

# 083
# Cape Verde Standard Time
# (GMT-01:00) Cape Verde Islands

# 085
# GMT Standard Time
# (GMT) Greenwich Mean Time : Dublin, Edinburgh, Lisbon, London

# 090
# Greenwich Standard Time
# (GMT) Casablanca, Monrovia

# 095
# Central Europe Standard Time
# (GMT+01:00) Belgrade, Bratislava, Budapest, Ljubljana, Prague

# 100
# Central European Standard Time
# (GMT+01:00) Sarajevo, Skopje, Warsaw, Zagreb

# 105
# Romance Standard Time
# (GMT+01:00) Brussels, Copenhagen, Madrid, Paris

# 110
# W. Europe Standard Time
# (GMT+01:00) Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna

# 113
# W. Central Africa Standard Time
# (GMT+01:00) West Central Africa

# 115
# E. Europe Standard Time
# (GMT+02:00) Bucharest

# 120
# Egypt Standard Time
# (GMT+02:00) Cairo

# 125
# FLE Standard Time
# (GMT+02:00) Helsinki, Kiev, Riga, Sofia, Tallinn, Vilnius

# 130
# GTB Standard Time
# (GMT+02:00) Athens, Istanbul, Minsk

# 135
# Israel Standard Time
# (GMT+02:00) Jerusalem

# 140
# South Africa Standard Time
# (GMT+02:00) Harare, Pretoria

# 145
# Russian Standard Time
# (GMT+03:00) Moscow, St. Petersburg, Volgograd

# 150
# Arab Standard Time
# (GMT+03:00) Kuwait, Riyadh

# 155
# E. Africa Standard Time
# (GMT+03:00) Nairobi

# 158
# Arabic Standard Time
# (GMT+03:00) Baghdad

# 160
# Iran Standard Time
# (GMT+03:30) Tehran

# 165
# Arabian Standard Time
# (GMT+04:00) Abu Dhabi, Muscat

# 170
# Caucasus Standard Time
# (GMT+04:00) Baku, Tbilisi, Yerevan

# 175
# Transitional Islamic State of Afghanistan Standard Time
# (GMT+04:30) Kabul

# 180
# Ekaterinburg Standard Time
# (GMT+05:00) Ekaterinburg

# 185
# West Asia Standard Time
# (GMT+05:00) Islamabad, Karachi, Tashkent

# 190
# India Standard Time
# (GMT+05:30) Chennai, Kolkata, Mumbai, New Delhi

# 193
# Nepal Standard Time
# (GMT+05:45) Kathmandu

# 195
# Central Asia Standard Time
# (GMT+06:00) Astana, Dhaka

# 200
# Sri Lanka Standard Time
# (GMT+06:00) Sri Jayawardenepura

# 201
# N. Central Asia Standard Time
# (GMT+06:00) Almaty, Novosibirsk

# 203
# Myanmar Standard Time
# (GMT+06:30) Yangon (Rangoon)

# 205
# S.E. Asia Standard Time
# (GMT+07:00) Bangkok, Hanoi, Jakarta

# 207
# North Asia Standard Time
# (GMT+07:00) Krasnoyarsk

# 210
# China Standard Time
# (GMT+08:00) Beijing, Chongqing, Hong Kong SAR, Urumqi

# 215
# Singapore Standard Time
# (GMT+08:00) Kuala Lumpur, Singapore

# 220
# Taipei Standard Time
# (GMT+08:00) Taipei

# 225
# W. Australia Standard Time
# (GMT+08:00) Perth

# 227
# North Asia East Standard Time
# (GMT+08:00) Irkutsk, Ulaanbaatar

# 230
# Korea Standard Time
# (GMT+09:00) Seoul

# 235
# Tokyo Standard Time
# (GMT+09:00) Osaka, Sapporo, Tokyo

# 240
# Yakutsk Standard Time
# (GMT+09:00) Yakutsk

# 245
# A.U.S. Central Standard Time
# (GMT+09:30) Darwin

# 250
# Cen. Australia Standard Time
# (GMT+09:30) Adelaide

# 255
# A.U.S. Eastern Standard Time
# (GMT+10:00) Canberra, Melbourne, Sydney

# 260
# E. Australia Standard Time
# (GMT+10:00) Brisbane

# 265
# Tasmania Standard Time
# (GMT+10:00) Hobart

# 270
# Vladivostok Standard Time
# (GMT+10:00) Vladivostok

# 275
# West Pacific Standard Time
# (GMT+10:00) Guam, Port Moresby

# 280
# Central Pacific Standard Time
# (GMT+11:00) Magadan, Solomon Islands, New Caledonia

# 285
# Fiji Islands Standard Time
# (GMT+12:00) Fiji Islands, Kamchatka, Marshall Islands

# 290
# New Zealand Standard Time
# (GMT+12:00) Auckland, Wellington

# 300
# Tonga Standard Time
# (GMT+13:00) Nuku'alofa





# http://docs.microsoft.com/en-us/windows-hardware/customize/desktop/unattend

