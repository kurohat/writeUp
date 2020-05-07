to read [link](https://docs.google.com/document/d/1q0FziVZM3zCWhcgtPpljVPzkBX0fMAh6ebrXVM5rg08/edit)

# Nmap Quiz 
1. help = -h
2. Syn Scan = -sS
3. UDP Scan = -sU
4. OS detection = -O
5. service verstion detection = -sV
6. verbosity flag = -v
7. very verbose = -vv
8. output in xml format = -oX
9. Aggressive scan = -A
10. set timing to max = -T5 (1-5)
11. specific port = -p
12. every port = -p-
13. use a script = --script
14. use script in vulnerability category = --script vuln
15. skip ping = -Pn

# Nmap Scanning 
1. syn scan = ```nmap -sS```
2. scanning first 10000 port = ```2```
```console
nmap -sS 10.10.121.13
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-02 21:48 EDT
Nmap scan report for 10.10.121.13
Host is up (0.047s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```
3. communication protocol of the open ports = ```tcp```
4. service version on SSH = ```6.6.1p1```
```console
root@kali:~# nmap -sV -p 22 10.10.121.13
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-02 21:50 EDT
Nmap scan report for 10.10.121.13
Host is up (0.046s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.10 (Ubuntu Linux; protocol 2.0)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.77 seconds
```
5. find out what flag on port 80 by performing an aggressive scan = ```httponly```
```console
root@kali:~# nmap -A -p 80 10.10.121.13
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-02 21:51 EDT
Nmap scan report for 10.10.121.13
Host is up (0.044s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.7 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
| http-robots.txt: 1 disallowed entry 
|_/
|_http-server-header: Apache/2.4.7 (Ubuntu)
| http-title: Login :: Damn Vulnerable Web Application (DVWA) v1.10 *Develop...
|_Requested resource was login.php
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.10 - 3.13 (95%), ASUS RT-N56U WAP (Linux 3.4) (95%), Linux 3.16 (95%), Linux 3.1 (93%), Linux 3.2 (93%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (92%), Sony Android TV (Android 5.0) (92%), Android 5.0 - 6.0.1 (Linux 3.4) (92%), Android 5.1 (92%), Android 7.1.1 - 7.1.2 (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops

TRACEROUTE (using port 80/tcp)
HOP RTT      ADDRESS
1   45.09 ms 10.9.0.1
2   43.99 ms 10.10.121.13

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.76 seconds
```
6. Perform a script scan of vulnerabilities associated with this box, what denial of service (DOS) attack is this box susceptible to? Answer with the name for the vulnerability that is given as the section title in the scan output. A vuln scan can take a while to complete. In case you get stuck, the answer for this question has been provided in the hint, however, it's good to still run this scan and get used to using it as it can be invaluable. = ```http-slowris-check```
```console
root@kali:~# nmap --script vuln -p 80 10.10.121.13
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-02 21:56 EDT
Nmap scan report for 10.10.121.13
Host is up (0.045s latency).

PORT   STATE SERVICE
80/tcp open  http
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|       httponly flag not set
|   /login.php: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-csrf: Couldn't find any CSRF vulnerabilities.
|_http-dombased-xss: Couldn't find any DOM based XSS.
| http-enum: 
|   /login.php: Possible admin folder
|   /robots.txt: Robots file
|   /config/: Potentially interesting directory w/ listing on 'apache/2.4.7 (ubuntu)'
|   /docs/: Potentially interesting directory w/ listing on 'apache/2.4.7 (ubuntu)'
|_  /external/: Potentially interesting directory w/ listing on 'apache/2.4.7 (ubuntu)'
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

Nmap done: 1 IP address (1 host up) scanned in 321.99 seconds
```