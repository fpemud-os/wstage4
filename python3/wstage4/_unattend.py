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
from ._const import Lang

class AnswerFileGenerator:

    def __init__(self, target_settings):
        self._ts = target_settings

    def updateIso(self, isoObj):
        if self._ts.category == Category.WINDOWS_XP:
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


def updateIsoForWindowsXP(ts, isoObj):
    buf = ""
    buf += "[Data]\n"
    buf += "AutoPartition=0\n"
    buf += "MsDosInitiated=0\n"
    buf += "UnattendedInstall=Yes\n"
    buf += "AutomaticUpdates=Yes\n"
    buf += "\n"
    buf += "[Unattended]\n"
    buf += "UnattendMode=FullUnattended\n"
    buf += "OemSkipEula=Yes\n"
    buf += "TargetPath=\\WINDOWS\n"
    buf += "Repartition=Yes\n"
    buf += "FileSystem=*\n"
    buf += "UnattendSwitch=Yes\n"
    buf += "DriverSigningPolicy=Ignore\n"
    buf += "WaitForReboot=No\n"
    buf += "NonDriverSigningPolicy=Ignore\n"
    buf += "\n"
    buf += "[GuiUnattended]\n"
    buf += "AdminPassword=*\n"
    buf += "EncryptedAdminPassword=No\n"
    buf += "OEMSkipRegional=1\n"
    buf += "TimeZone=%s\n" % (MsWinCommon.getTimezoneByLang(ts.lang))
    buf += "OemSkipWelcome=1\n"
    buf += "\n"
    buf += "[UserData]\n"
    if ts.serial is not None:
        buf += "ProductID=%s\n" % (ts.serial)
    buf += "FullName=*\n"
    buf += "OrgName=*\n"
    buf += "ComputerName=*\n"
    buf += "\n"
    buf += "[Display]\n"
    buf += "Xresolution=1024\n"
    buf += "Yresolution=768\n"
    buf += "\n"
    buf += "[TapiLocation]\n"
    buf += "CountryCode=%s\n" % ("86")
    buf += "AreaCode=%s\n" % ("00")
    buf += "Dialing=%s\n" % ("Tone")
    buf += "\n"
    buf += "[RegionalSettings]\n"
    buf += "LanguageGroup=%s\n" % ("10")
    buf += "Language=%s\n" % ("00000804")
    buf += "\n"
    buf += "[Identification]\n"
    buf += "JoinWorkgroup=WORKGROUP\n"
    buf += "\n"
    buf += "[Networking]\n"
    buf += "InstallDefaultComponents=Yes\n"
    buf += "\n"
    buf += "[GuiRunOnce]\n"
    buf += "\"shutdown /s /t 60\"\n"

    buf = buf.encode("UTF-8")
    isoObj.add_fp(BytesIO(buf), len(buf), '/WINNT.SIF')



def updateIsoForWindows7(self, isoObj):
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
                            <Key>@@serial_id@@</Key>
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
    buf = buf.replace("@@serial_id@@", ts.serial)
    buf = buf.replace("@@timezone@@", MsWinCommon.getTimezoneByLang(ts.lang))

    buf = buf.encode("UTF-8")
    isoObj.add_fp(BytesIO(buf), len(buf), '/autounattend.xml')


class MsWinCommon:

    @staticmethod
    def getTimezoneByLang(lang):
        if lang == Lang.en_us:
            return "85"
        elif lang == Lang.zh_cn:
            return "85"
        elif lang == Lang.zh_tw:
            return "85"
        else:
            assert False

