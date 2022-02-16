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


from io import BytesIO
from ._const import Category, Edition, Lang


class AnswerFileGenerator:

    def __init__(self, target_settings):
        self._ts = target_settings

    def updateIso(self, isoObj):
        # from https://www.windowsafg.com

        if self._ts.category == Category.WINDOWS_98:
            updateIsoForWindows98(self._ts, isoObj)
        elif self._ts.category == Category.WINDOWS_XP:
            updateIsoForWindowsXP(self._ts, isoObj)
        elif self._ts.category == Category.WINDOWS_VISTA:
            # FIXME
            assert False
        elif self._ts.category == Category.WINDOWS_7:
            updateIsoForWindows7(self._ts, isoObj)
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


def updateIsoForWindows98(ts, isoObj):
    # from https://www.tek-tips.com/viewthread.cfm?qid=612507

    if ts.product_key is None:
        key = _Util.getDefaultProductKeyByEdition(ts.edition)
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

    buf = buf.encode("iso8859-1")
    isoObj.add_fp(BytesIO(buf), len(buf), '/MSBATCH.INF')

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


def updateIsoForWindowsXP(ts, isoObj):
    if ts.product_key is None:
        key = _Util.getDefaultProductKeyByEdition(ts.edition)
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

    buf = buf.encode("UTF-8")
    isoObj.add_fp(BytesIO(buf), len(buf), '/WINNT.SIF')

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


def updateIsoForWindows7(ts, isoObj):
    buf = """
        <?xml version="1.0" encoding="utf-8"?>
        <unattend xmlns="urn:schemas-microsoft-com:unattend">
            <settings pass="windowsPE">
                <component name="Microsoft-Windows-International-Core-WinPE" processorArchitecture="@@arch@@" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                    <SetupUILanguage>
                        <UILanguage>@@lang@@</UILanguage>
                    </SetupUILanguage>
                    <InputLocale>@@lang@@</InputLocale>
                    <SystemLocale>@@lang@@</SystemLocale>
                    <UILanguage>@@lang@@</UILanguage>
                    <UserLocale>@@lang@@</UserLocale>
                </component>
                <component name="Microsoft-Windows-Setup" processorArchitecture="@@arch@@" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                    <DiskConfiguration>
                        <Disk>
                            <DiskID>0</DiskID>
                            <WillWipeDisk>true</WillWipeDisk>
                            <CreatePartitions>
                                <!-- system reserved partition for windows-7 -->
                                <CreatePartition>
                                    <Order>1</Order>
                                    <Type>Primary</Type>                            
                                    <Size>100</Size>
                                </CreatePartition>
                                <!-- windows partition -->
                                <CreatePartition>
                                    <Order>2</Order>
                                    <Type>Primary</Type>
                                    <Extend>true</Extend>
                                </CreatePartition>
                            </CreatePartitions>
                            <ModifyPartitions>
                                <ModifyPartition>
                                    <Order>1</Order>
                                    <PartitionID>1</PartitionID>
                                    <Active>true</Active>
                                    <Format>NTFS</Format>
                                </ModifyPartition>
                                <ModifyPartition>
                                    <Order>2</Order>
                                    <PartitionID>2</PartitionID>
                                    <Letter>C</Letter>
                                    <Format>NTFS</Format>
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
            <settings pass="oobeSystem">
                <component name="Microsoft-Windows-Shell-Setup" processorArchitecture="@@arch@@" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
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
                <component name="Microsoft-Windows-Shell-Setup" processorArchitecture="@@arch@@" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                    <ComputerName>@@username@@-PC</ComputerName>
                </component>
                <!-- disable the welcome window of IE -->
                <component name="Microsoft-Windows-IE-InternetExplorer" processorArchitecture="@@arch@@" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                    <DisableAccelerators>true</DisableAccelerators>
                    <DisableOOBAccelerators>true</DisableOOBAccelerators>
                    <SuggestedSitesEnabled>false</SuggestedSitesEnabled>
                    <Home_Page>about:blank</Home_Page>
                </component>
            </settings>
            <cpi:offlineImage cpi:source="catalog:h:/sources/install_windows 7 ultimate.clg" xmlns:cpi="urn:schemas-microsoft-com:cpi" />
        </unattend>
    """
    buf = buf.replace("@@arch@@", ts.arch)
    buf = buf.replace("@@lang@@", ts.lang)
    buf = buf.replace("@@username@@", "A")
    buf = buf.replace("@@password@@", "")
    buf = buf.replace("@@product_key@@", ts.product_key)
    buf = buf.replace("@@timezone@@", _Util.getTimezoneCodeByLang(ts.lang))

    buf = buf.encode("UTF-8")
    isoObj.add_fp(BytesIO(buf), len(buf), '/autounattend.xml')


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
    def getDefaultProductKeyByEdition(edition):
        if edition == Edition.WINDOWS_98:
            # ?
            return "F73WT-WHD3J-CD4VR-2GWKD-T38YD"
        elif edition == Edition.WINDOWS_98_SE:
            # This is the "public knowledge" abandonware key supplied by Microsoft for Win98.
            # from https://github.com/visual2000/paschke/blob/master/02runsetup/MSBATCH.INF
            return "F73WT-WHD3J-CD4VR-2GWKD-T38YD"
        elif edition == Edition.WINDOWS_XP_HOME:
            # ?
            return "NG4HW-VH26C-733KW-K6F98-J8CK4"
        elif edition == Edition.WINDOWS_XP_PROFESSIONAL:
            # ?
            return "NG4HW-VH26C-733KW-K6F98-J8CK4"
        elif edition == Edition.WINDOWS_7_STARTER:
            # from https://www.windowsafg.com/keys.html
            return "7Q28W-FT9PC-CMMYT-WHMY2-89M6G"
        elif edition == Edition.WINDOWS_7_HOME_BASIC:
            # from https://www.windowsafg.com/keys.html
            return "YGFVB-QTFXQ-3H233-PTWTJ-YRYRV"
        elif edition == Edition.WINDOWS_7_HOME_PREMIUM:
            # from https://www.windowsafg.com/keys.html
            return "RHPQ2-RMFJH-74XYM-BH4JX-XM76F"
        elif edition == Edition.WINDOWS_7_PROFESSIONAL:
            # from https://www.windowsafg.com/keys.html
            return "HYF8J-CVRMY-CM74G-RPHKF-PW487"
        elif edition == Edition.WINDOWS_7_ULTIMATE:
            # from https://www.windowsafg.com/keys.html
            return "D4F6K-QK3RD-TMVMJ-BBMRX-3MBMV"
        elif edition == Edition.WINDOWS_7_ENTERPRISE:
            # from https://www.windowsafg.com/keys.html
            return "H7X92-3VPBB-Q799D-Y6JJ3-86WC6"
        else:
            assert False
