# LV null
```console
root@kali:~# ssh bandit0@bandit.labs.overthewire.org -p 2220
```
password bandit0
# LV0
```console
bandit0@bandit:~$ ls
readme
bandit0@bandit:~$ cat readme 
boJ9jbbUNNfktd78OOpsqOltutMc3MY1
```
# LV1
```console
root@kali:~# ssh bandit1@bandit.labs.overthewire.org -p 2220
bandit1@bandit:~$ ls
-
bandit1@bandit:~$ cat < -
CV1DtqXWVFXTvM2F0k09SHz0YwRINYA9
bandit1@bandit:~$ cat ./-
CV1DtqXWVFXTvM2F0k09SHz0YwRINYA9
```
read:
- http://tldp.org/LDP/abs/html/special-chars.html
- https://unix.stackexchange.com/queshttp://tldp.org/LDP/abs/html/special-chars.htmltions/16357/usage-of-dash-in-place-of-a-filename
# LV2
```console
root@kali:~# ssh bandit2@bandit.labs.overthewire.org -p 2220
bandit2@bandit:~$ cat spaces\ in\ this\ filename 
UmHadQclWmgdLOKQ3YNgjWxGoRMb5luK
bandit2@bandit:~$ cat "spaces in this filename"
UmHadQclWmgdLOKQ3YNgjWxGoRMb5luK
```
OR use ```TAP```
read: https://cets.seas.upenn.edu/answers/bad-name.html
# LV3
```console
root@kali:~# ssh bandit3@bandit.labs.overthewire.org -p 2220
bandit3@bandit:~$ ls
inhere
bandit3@bandit:~$ cd inhere/
bandit3@bandit:~/inhere$ ls
bandit3@bandit:~/inhere$ ls -a
.  ..  .hidden
bandit3@bandit:~/inhere$ cat .hidden 
pIwrPrtPN36QITSp3EQaw936yaFoFgAB
```
NOTE: -a OR --all = do not ignore entries starting with .

# LV4
human-readable file ?
```console
root@kali:~# ssh bandit4@bandit.labs.overthewire.org -p 2220
bandit4@bandit:~$ cd inhere/
bandit4@bandit:~/inhere$ ls
-file00  -file01  -file02  -file03  -file04  -file05  -file06  -file07  -file08  -file09
bandit4@bandit:~/inhere$ file ./*
./-file00: data
./-file01: data
./-file02: data
./-file03: data
./-file04: data
./-file05: data
./-file06: data
./-file07: ASCII text
./-file08: data
./-file09: data
bandit4@bandit:~/inhere$ cat ./-file07
koReBOKuIDDepwhWk7jZC0RTdopnAYKh
```
NOTE: ASCII text = human-readable file 

# LV5
human-readable = ```find . -type f -exec file {} + | grep ASCII```
size 1033 byte = ```find . -size 1033c```
LINK:
- http://www.ducea.com/2008/02/12/linux-tips-find-all-files-of-a-particular-size/
- https://unix.stackexchange.com/questions/9619/script-to-list-only-files-of-type-ascii-text-in-the-current-directory
```console
root@kali:~# ssh bandit5@bandit.labs.overthewire.org -p 2220
bandit4@bandit:~$ cd inhere/
bandit4@bandit:~$ find . -size 1033c -type f -exec file {} + | grep ASCII
./maybehere07/.file2: ASCII text, with very long lines
bandit5@bandit:~/inhere$ cat ./maybehere07/.file2
DXjZPULLxYr17uwoI01bNLQbtFemEgo7
```

# LV6
- somewhere on the server = can be anywhere -> move to root directory by ```cd /```
- find owner ```find -user```
- find group ```find -group```
LINK:
https://www.cyberciti.biz/faq/how-do-i-find-all-the-files-owned-by-a-particular-user-or-group/

```console
root@kali:~# ssh bandit6@bandit.labs.overthewire.org -p 2220
bandit6@bandit:~$ cd /
[1]+  Done                    cd  (wd: ~)
(wd now: /)
bandit6@bandit:/$ find . -user bandit7 -group bandit6 -size 33c
find: ‘./run/lvm’: Permission denied
find: ‘./run/screen/S-bandit25’: Permission denied
.
.
.
./var/lib/dpkg/info/bandit7.password
.
.
.
find: ‘./proc/12189/fd/5’: No such file or directory
find: ‘./proc/12189/fdinfo/5’: No such file or directory
find: ‘./boot/lost+found’: Permission denied
bandit6@bandit:/$ cat ./var/lib/dpkg/info/bandit7.password
HKBPTKQnIay4Fw76bEy8PVxKEDQRKTzs
```
# LV7

```console
root@kali:~# ssh bandit7@bandit.labs.overthewire.org -p 2220
bandit7@bandit:~$ cat data.txt | grep millionth
millionth       cvX2JJa4CFALtqS87jk27qwqGhBM9plV
```
# LV8

```console
root@kali:~# ssh bandit8@bandit.labs.overthewire.org -p 2220
bandit8@bandit:~$ sort data.txt | uniq -u
UsvVyFSfZZWbi6wgC7dAFyFuR6jQQUhR
```
```sort data.txt | uniq -u``` sort data filter by uniq value

# LV9

```console
root@kali:~# ssh bandit9@bandit.labs.overthewire.org -p 2220
bandit9@bandit:~$ strings data.txt | grep ==
2========== the
========== password
========== isa
========== truKLdjsbJ5g7yyJ2X2R0o3a5HQJFuLk
```

# LV10
```console
root@kali:~# ssh bandit10@bandit.labs.overthewire.org -p 2220
bandit10@bandit:~$ base64 -d data.txt 
The password is IFukwKGsFW8MOq3IRFqrxE1hxTNEbUPR
```
```-d``` for decode.

# LV11
- ROT13

| input                      | output                     |
|----------------------------|----------------------------|
| ABCDEFGHIJKLMNOPQRSTUVWXYZ | NOPQRSTUVWXYZABCDEFGHIJKLM |
| abcdefghijklmnopqrstuvwxyz | nopqrstuvwxyzabcdefghijklm |

```console
root@kali:~# ssh bandit11@bandit.labs.overthewire.org -p 2220
bandit11@bandit:~$ cat data.txt | tr '[A-Za-z]' '[NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm]'
The password is 5Te8Y4drgCRfCx8ugdwuEX8KFC6k2EUu
```

# LV12
```console
root@kali:~# ssh bandit12@bandit.labs.overthewire.org -p 2220
bandit12@bandit:~$ mkdir /tmp/kuroHat
bandit12@bandit:~$ cp data.txt /tmp/kuroHat
bandit12@bandit:~$ cd /tmp/kuroHat
bandit12@bandit:/tmp/kuroHat$ cat data.txt | xxd -r > output
bandit12@bandit:/tmp/kuroHat$ file output 
output: gzip compressed data, was "data2.bin", last modified: Tue Oct 16 12:00:23 2018, max compression, from Unix
```
now we know that the file gzip compressed data -> change name to output.gz by run
```console
bandit12@bandit:/tmp/kuroHat$ mv output output.gz
bandit12@bandit:/tmp/kuroHat$ gzip -d output.gz
bandit12@bandit:/tmp/kuroHat$ cat output 
�▒▒h��6��@4▒bi���h▒ϟ���������������׽��9��
    �mF�h�h44
▒��B��,0��   ��4@�����@2▒C@h�� �
          �v;�P��;z�����s�!��+�f����0`h�e�^���m��K�l��5n�+tÔhY���R�Br"�<(Hت$    $���KBs��%l�ɋ�^-K�����}�\,�▒ǿ�}E�F�_!r�U�g?E�i��9x��TB@�lȲ���BF.hM�SC4�V�F�

��\��WQO4�p�i�����S�#&��/�#��[j▒�<D�uԐ^_�H.�-��wAt
                                                  �[��UP�G�CP��&:�2�*�)�\�������H�
�\�
bandit12@bandit:/tmp/kuroHat$ file output 
output: bzip2 compressed data, block size = 900k
```
after run ```cat``` the output still weird, I then run ```file``` to check the type of file. turn out that it is bzip2 compressed data.
```console
bandit12@bandit:/tmp/kuroHat$ mv output output.bz2
zip2 -d output.bz2 
bandit12@bandit:/tmp/kuroHat$ ls
data.txt  output
bandit12@bandit:/tmp/kuroHat$ cat output 
���[data4.bin��=H����T,▒��)C�,D�ތ�K"*�"����*ե�^��k
 b�
   E)|�8�[E��R�/4-�U'E�tl��`������������N�>�Z6�_Yp)u���
                                                       #�5���
H��~E�}}�u����S]���uU5L�����▒b=uZ�
�Ya��$Df����D���=�����"�8^W��IG�%��zZv���S�t>�nN��=�Z������*��ȼz����?&����g���ZВ�y۷��W��G2GnG�����畡�O�Rݗ�}k���[�<�
                        Zw3��y������n��ҺyO~7��ˇ�Y�E�NM6>>Ȟ���z�0s�{�z�;�J��Y��o�!����   ����[F\Pbandit12@bandit:/tmp/kuroHat$ file output 
output: gzip compressed data, was "data4.bin", last modified: Tue Oct 16 12:00:23 2018, max compression, from Unix
bandit12@bandit:/tmp/kuroHat$ mv output output.gz
bandit12@bandit:/tmp/kuroHat$ gzip -d output.gz 
bandit12@bandit:/tmp/kuroHat$ file output 
output: POSIX tar archive (GNU)
```
As you can see the ```.gz``` was compressed in ```.bz2```. The last lines show that the file is ```.tar```
```console
bandit12@bandit:/tmp/kuroHat$ mv output output.tar
bandit12@bandit:/tmp/kuroHat$ tar -xvf output.tar 
data5.bin
bandit12@bandit:/tmp/kuroHat$ file data5.bin 
data5.bin: POSIX tar archive (GNU)
bandit12@bandit:/tmp/kuroHat$ mv data5.bin data5.tar
bandit12@bandit:/tmp/kuroHat$ tar -xvf data5.tar 
data6.bin
bandit12@bandit:/tmp/kuroHat$ file data6.bin 
data6.bin: bzip2 compressed data, block size = 900k
bandit12@bandit:/tmp/kuroHat$ mv data6.bin data6.bz2
bandit12@bandit:/tmp/kuroHat$ bzip2 -d data6.bz2 
bandit12@bandit:/tmp/kuroHat$ file data6 
data6: POSIX tar archive (GNU)
```
DAMNNNN not again
```console
andit12@bandit:/tmp/kuroHat$ mv data6 data6.tar
bandit12@bandit:/tmp/kuroHat$ tar -xvf data6.tar 
data8.bin
bandit12@bandit:/tmp/kuroHat$ file data8.bin
data8.bin: gzip compressed data, was "data9.bin", last modified: Tue Oct 16 12:00:23 2018, max compression, from Unix
bandit12@bandit:/tmp/kuroHat$ mv data8.bin data8.gz
bandit12@bandit:/tmp/kuroHat$ gzip -d data8.gz 
bandit12@bandit:/tmp/kuroHat$ ls
data5.tar  data6.tar  data8  data.txt  output.tar
bandit12@bandit:/tmp/kuroHat$ file data8
data8: ASCII text
```
FINALLY
```console
bandit12@bandit:/tmp/kuroHat$ cat data8
The password is 8ZjyCRiBWFYkneahHwxCv3wb2a1ORpYL
```

# LV13
```console
bandit13@bandit:~$ ls
sshkey.private
bandit13@bandit:~$ ssh -i sshkey.private bandit14@localhost
bandit14@bandit:~$ cat /etc/bandit_pass/bandit14
4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e
```

# LV14
```console
bandit14@bandit:~$ nc 127.0.0.1 30000
4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e
Correct!
BfMYroe26WYalil77FoDi9qh59eK5xNr
```

# LV15
```console
bandit14@bandit:~$openssl s_client -connect 127.0.0.1:30001
CONNECTED(00000003)
depth=0 CN = localhost
verify error:num=18:self signed certificate
verify return:1
depth=0 CN = localhost
verify return:1
.
.
.
    Start Time: 1580824257
    Timeout   : 7200 (sec)
    Verify return code: 18 (self signed certificate)
    Extended master secret: yes
---
BfMYroe26WYalil77FoDi9qh59eK5xNr
Correct!
cluFn7wTiGryunymYOu4RcffSxQluehd

closed
```

# LV16
```console
bandit14@bandit:~$ nmap -p 31000-32000 127.0.0.1

Starting Nmap 7.40 ( https://nmap.org ) at 2020-02-04 14:58 CET
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00025s latency).
Not shown: 999 closed ports
PORT      STATE SERVICE
31518/tcp open  unknown
31790/tcp open  unknown
```
as you can see, there are 2 open port. We are looking for the port that speak SSL and which don't
```console
bandit14@bandit:~$ nmap -sV -p 31518 127.0.0.1

Starting Nmap 7.40 ( https://nmap.org ) at 2020-02-04 15:00 CET
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00026s latency).
PORT      STATE SERVICE  VERSION
31518/tcp open  ssl/echo

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 52.61 seconds
bandit14@bandit:~$ nmap -sV -p 31790 127.0.0.1

Starting Nmap 7.40 ( https://nmap.org ) at 2020-02-04 15:12 CET
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00012s latency).
PORT      STATE SERVICE     VERSION
31790/tcp open  ssl/unknown
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port31790-TCP:V=7.40%T=SSL%I=7%D=2/4%Time=5E397BE6%P=x86_64-pc-linux-gn
SF:u%r(GenericLines,31,"Wrong!\x20Please\x20enter\x20the\x20correct\x20cur
SF:rent\x20password\n")%r(GetRequest,31,"Wrong!\x20Please\x20enter\x20the\
SF:x20correct\x20current\x20password\n")%r(HTTPOptions,31,"Wrong!\x20Pleas
SF:e\x20enter\x20the\x20correct\x20current\x20password\n")%r(RTSPRequest,3
SF:1,"Wrong!\x20Please\x20enter\x20the\x20correct\x20current\x20password\n
SF:")%r(Help,31,"Wrong!\x20Please\x20enter\x20the\x20correct\x20current\x2
SF:0password\n")%r(SSLSessionReq,31,"Wrong!\x20Please\x20enter\x20the\x20c
SF:orrect\x20current\x20password\n")%r(TLSSessionReq,31,"Wrong!\x20Please\
SF:x20enter\x20the\x20correct\x20current\x20password\n")%r(Kerberos,31,"Wr
SF:ong!\x20Please\x20enter\x20the\x20correct\x20current\x20password\n")%r(
SF:FourOhFourRequest,31,"Wrong!\x20Please\x20enter\x20the\x20correct\x20cu
SF:rrent\x20password\n")%r(LPDString,31,"Wrong!\x20Please\x20enter\x20the\
SF:x20correct\x20current\x20password\n")%r(LDAPSearchReq,31,"Wrong!\x20Ple
SF:ase\x20enter\x20the\x20correct\x20current\x20password\n")%r(SIPOptions,
SF:31,"Wrong!\x20Please\x20enter\x20the\x20correct\x20current\x20password\
SF:n");

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 88.75 seconds
```
NOTE: There is only 1 server that will give the next credentials, the others will simply send back to you whatever you send to it.
- 31790/tcp open  ssl/unknown
- 31518/tcp open  ssl/echo
Which mean we need to openssl s_client to 31790
```console
bandit14@bandit:~$ openssl s_client -connect 127.0.0.1:31790
CONNECTED(00000003)
depth=0 CN = localhost
verify error:num=18:self signed certificate
.
.
.
    Verify return code: 18 (self signed certificate)
    Extended master secret: yes
---
cluFn7wTiGryunymYOu4RcffSxQluehd
Correct!
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAvmOkuifmMg6HL2YPIOjon6iWfbp7c3jx34YkYWqUH57SUdyJ
imZzeyGC0gtZPGujUSxiJSWI/oTqexh+cAMTSMlOJf7+BrJObArnxd9Y7YT2bRPQ
Ja6Lzb558YW3FZl87ORiO+rW4LCDCNd2lUvLE/GL2GWyuKN0K5iCd5TbtJzEkQTu
DSt2mcNn4rhAL+JFr56o4T6z8WWAW18BR6yGrMq7Q/kALHYW3OekePQAzL0VUYbW
JGTi65CxbCnzc/w4+mqQyvmzpWtMAzJTzAzQxNbkR2MBGySxDLrjg0LWN6sK7wNX
x0YVztz/zbIkPjfkU1jHS+9EbVNj+D1XFOJuaQIDAQABAoIBABagpxpM1aoLWfvD
KHcj10nqcoBc4oE11aFYQwik7xfW+24pRNuDE6SFthOar69jp5RlLwD1NhPx3iBl
J9nOM8OJ0VToum43UOS8YxF8WwhXriYGnc1sskbwpXOUDc9uX4+UESzH22P29ovd
d8WErY0gPxun8pbJLmxkAtWNhpMvfe0050vk9TL5wqbu9AlbssgTcCXkMQnPw9nC
YNN6DDP2lbcBrvgT9YCNL6C+ZKufD52yOQ9qOkwFTEQpjtF4uNtJom+asvlpmS8A
vLY9r60wYSvmZhNqBUrj7lyCtXMIu1kkd4w7F77k+DjHoAXyxcUp1DGL51sOmama
+TOWWgECgYEA8JtPxP0GRJ+IQkX262jM3dEIkza8ky5moIwUqYdsx0NxHgRRhORT
8c8hAuRBb2G82so8vUHk/fur85OEfc9TncnCY2crpoqsghifKLxrLgtT+qDpfZnx
SatLdt8GfQ85yA7hnWWJ2MxF3NaeSDm75Lsm+tBbAiyc9P2jGRNtMSkCgYEAypHd
HCctNi/FwjulhttFx/rHYKhLidZDFYeiE/v45bN4yFm8x7R/b0iE7KaszX+Exdvt
SghaTdcG0Knyw1bpJVyusavPzpaJMjdJ6tcFhVAbAjm7enCIvGCSx+X3l5SiWg0A
R57hJglezIiVjv3aGwHwvlZvtszK6zV6oXFAu0ECgYAbjo46T4hyP5tJi93V5HDi
Ttiek7xRVxUl+iU7rWkGAXFpMLFteQEsRr7PJ/lemmEY5eTDAFMLy9FL2m9oQWCg
R8VdwSk8r9FGLS+9aKcV5PI/WEKlwgXinB3OhYimtiG2Cg5JCqIZFHxD6MjEGOiu
L8ktHMPvodBwNsSBULpG0QKBgBAplTfC1HOnWiMGOU3KPwYWt0O6CdTkmJOmL8Ni
blh9elyZ9FsGxsgtRBXRsqXuz7wtsQAgLHxbdLq/ZJQ7YfzOKU4ZxEnabvXnvWkU
YOdjHdSOoKvDQNWu6ucyLRAWFuISeXw9a/9p7ftpxm0TSgyvmfLF2MIAEwyzRqaM
77pBAoGAMmjmIJdjp+Ez8duyn3ieo36yrttF5NSsJLAbxFpdlc1gvtGCWW+9Cq0b
dxviW8+TFVEBl1O4f7HVm6EpTscdDxU+bCXWkfjuRb7Dy9GOtt9JPsX8MBTakzh3
vBgsyi/sN3RqRBcGU40fOoZyfAMT8s1m/uYv52O6IgeuZ/ujbjY=
-----END RSA PRIVATE KEY-----

closed
```
now use the RSA private key to ssh to next state. but first let save the key
```console
bandit14@bandit:~$ mkdir /tmp/kuro16
bandit14@bandit:~$ cd /tmp/kuro16
bandit14@bandit:/tmp/kuro16$ nano bandit16key
```
copy and paste the RSA private key file. Now SSH to bandit17 using the key
```console
bandit14@bandit:/tmp/kuro16$ chmod 600 bandit16key 
bandit14@bandit:/tmp/kuro16$ ssh -i bandit16key bandit17@localhost
```

# LV 17
There are 2 files in the homedirectory: **passwords.old and passwords.new**. The password for the next level is in **passwords.new** and is the only line that has been changed between **passwords.old and passwords.new**

**NOTE: if you have solved this level and see ‘Byebye!’ when trying to log into bandit18, this is related to the next level, bandit19**

```console
bandit17@bandit:~$ ls
passwords.new  passwords.old
bandit17@bandit:~$ diff passwords.old passwords.new
42c42
< hlbSBPAWJmL6WFDb06gpTx1pPButblOA
---
> kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd
```
42c42 = line 42 of 1st file is different than line 42 of 2nd file

``<`` are lines from the 1st file

``>`` are lines from the 2st file

changed between **passwords.old and passwords.new** -> password = ```kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd```

# LV 18

```
Level Goal
The password for the next level is stored in a file readme in the homedirectory. Unfortunately, someone has modified .bashrc to log you out when you log in with SSH.

Commands you may need to solve this level: ssh, ls, cat
```
Since someone has modified .bashrc to log you out when you log in with SSH.
There are many solution to this lv,
1. tell ssh to launch the bash shell instead of logging directly into bandit18 user shell
2. use ssh to run a bash command on the remote server [link](https://www.shellhacks.com/ssh-execute-remote-command-script-linux/)

Here is how to use ssh to run a bash command on the remote server

```console
$ ssh bandit18@bandit.labs.overthewire.org -p 2220 "cat readme"
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit18@bandit.labs.overthewire.org's password: 
IueksS7Ubh8G3DCwVzrTd8rAVOwq3M5x
```

# LV 19
```
Level Goal
To gain access to the next level, you should use the setuid binary in the homedirectory. Execute it without arguments to find out how to use it. The password for this level can be found in the usual place (/etc/bandit_pass), after you have used the setuid binary.
```
[setuid](https://en.wikipedia.org/wiki/Setuid)

in home directory you will fine ./bandit20-do. this program allow you to execute bash command as bandit20. So just ```cat``` the ```/etc/bandit_pass/bandit20``` to see the password

```console
bandit19@bandit:~$ ./bandit20-do
Run a command as another user.
  Example: ./bandit20-do id
bandit19@bandit:~$ ./bandit20-do cat /etc/bandit_pass/bandit20
GbKksEFF4yrVs6il55v6gwY5aVje5f0j
```

# LV 20
```
Level Goal
There is a setuid binary in the homedirectory that does the following: it makes a connection to localhost on the port you specify as a commandline argument. It then reads a line of text from the connection and compares it to the password in the previous level (bandit20). If the password is correct, it will transmit the password for the next level (bandit21).

NOTE: Try connecting to your own network daemon to see if it works as you think

Commands you may need to solve this level:

ssh, nc, cat, bash, screen, tmux, Unix ‘job control’ (bg, fg, jobs, &, CTRL-Z, …)

```

```console
$ ls
suconnect
$ ./suconnect 
Usage: ./suconnect <portnumber>
This program will connect to the given port on localhost using TCP. If it receives the correct password from the other side, the next password is transmitted back.
```
in a simple word, the program will act as a client and connect to a "server" (which we need to set up). The program will send the password for next lv (bandit21) back to the server **only if** it receives the correct password (bandit20) from the server. This means the "server"  need to send ```GbKksEFF4yrVs6il55v6gwY5aVje5f0j``` to the client (program) when the connection is established

to solve this, we need to run **an experiment on our machine**:
```nc``` or netcat can be use for many tasks (check ```man nc```). we will use ```nc -l -p [port]``` to listen to a specific port for connections. open another tab and run ```nc localhost [port]```. at this point you can now send messages on either side of the connection and they will be seen on either end. [How To Use Netcat to Establish and Test TCP and UDP Connections on a VPS](https://www.digitalocean.com/community/tutorials/how-to-use-netcat-to-establish-and-test-tcp-and-udp-connections-on-a-vps)

Now let try something else, we will try to echo "wazzap" when a connection is established on port 22222. Then we use another tab to connect to port 22222. let see what happen
```console
$ echo "wazzap" | nc -l -p 22222 # tab 1 "server"
$ nc localhost 22222 # tab 2 "client"
wazzap
```
At you can see, tab2 (client) got a wazzap text from tab1 (server)


Now just apply the same concept on bandit20 by open 2 tab using ```screen``` which is a terminal emulator (check ```man screen```). we dont need to open two tab and ssh to bandit 20 if we use ```screen```. However, if you want to open 2 tab then just skip the screen part.
```console
$ screen
$ echo "GbKksEFF4yrVs6il55v6gwY5aVje5f0j" | nc -l -p 22222 # tab 1 "server"
$ # press ctrl + a + d to go back to original screen
$ # now we are back to original screen
$ ./suconnect 22222
Read: GbKksEFF4yrVs6il55v6gwY5aVje5f0j
Password matches, sending next password
$ # it works, let go back to our old screen
$ screen -list # find out which screen is up
$ screen -r pid.tty.name # jump to the screen which we run the server on
$ echo "GbKksEFF4yrVs6il55v6gwY5aVje5f0j" | nc -l -p 22222
gE269g2h3mw3pwgrj0Ha9Uoqen1c9DGr
```

another way to do it
```console
bandit20@bandit:~$ echo "GbKksEFF4yrVs6il55v6gwY5aVje5f0j" | nc -l -p 22222 &
[1] 30416
bandit20@bandit:~$ ./suconnect 22222
Read: GbKksEFF4yrVs6il55v6gwY5aVje5f0j
Password matches, sending next password
gE269g2h3mw3pwgrj0Ha9Uoqen1c9DGr
[1]+  Done                    echo "GbKksEFF4yrVs6il55v6gwY5aVje5f0j" | nc -l -p 22222
```

password to next lv : ```gE269g2h3mw3pwgrj0Ha9Uoqen1c9DGr```

# LV 21
```
Level Goal

A program is running automatically at regular intervals from cron, the time-based job scheduler. Look in /etc/cron.d/ for the configuration and see what command is being executed.

Commands you may need to solve this level:

cron, crontab, crontab(5) (use “man 5 crontab” to access this)
```

```console
bandit21@bandit:~$ ls /etc/cron.d/
atop  cronjob_bandit22  cronjob_bandit23  cronjob_bandit24
bandit21@bandit:~$ cat /etc/cron.d/cronjob_bandit22
@reboot bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
* * * * * bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
bandit21@bandit:~$ cat /usr/bin/cronjob_bandit22.sh # what do this program do?
#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
$ aha cat the password to bandit 22 and put it in /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
bandit21@bandit:~$ /usr/bin/cronjob_bandit22.sh # run it
chmod: changing permissions of '/tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv': Operation not permitted
/usr/bin/cronjob_bandit22.sh: line 3: /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv: Permission denied
bandit21@bandit:~$ cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv # open it
Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI
```

password to next lv : ```Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI```

# LV 22
```
Level Goal

A program is running automatically at regular intervals from cron, the time-based job scheduler. Look in /etc/cron.d/ for the configuration and see what command is being executed.

NOTE: Looking at shell scripts written by other people is a very useful skill. The script for this level is intentionally made easy to read. If you are having problems understanding what it does, try executing it to see the debug information it prints.
Commands you may need to solve this level

cron, crontab, crontab(5) (use “man 5 crontab” to access this)
```

this lv is similar to lv 21 so, go check the crontab file the you will found that there is a cronjob_bandit23 which execute ```/usr/bin/cronjob_bandit23.sh``` to find out what it does:

```console
$ /usr/bin/cronjob_bandit23.sh # let see what it does
Copying passwordfile /etc/bandit_pass/bandit22 to /tmp/8169b67bd894ddbb4412f91573b38db3
$ cat /tmp/8169b67bd894ddbb4412f91573b38db3 #okey what is in this file?
Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI
```
so it seam like what the progame does get the content of /etc/bandit_pass/bandit22 which contain password of bandit22 and output it as /tmp/8169b67bd894ddbb4412f91573b38db3.


now let read the shell script and understand it in detail:
```console
$ cat /usr/bin/cronjob_bandit23.sh
#!/bin/bash

myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)

echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"

cat /etc/bandit_pass/$myname > /tmp/$mytarget
```
```cat /etc/bandit_pass/$myname > /tmp/$mytarget```take the content base on myname and output it into a file in /tmp directory. To find out what is the name of the file we need to understand this line ```mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)```. the varible mytarget is the file name which is a the md5 sum of string "echo I am user $myname" which cut something something. and the varivle myname is the name of the user name associated with the current effective user ID


So if we change $myname to bandit23 we will get the name of the file which contains password to next lv:
```console
bandit22@bandit:~$ (echo I am user bandit23 | md5sum | cut -d ' ' -f 1)
8ca319486bfbbc3663ea0fbe81326349
bandit22@bandit:~$ cat /tmp/8ca319486bfbbc3663ea0fbe81326349
jc1udXuA1tiHqjIsL8yaapX5XIAI6i0n
```

passpassword to the next lv : ```jc1udXuA1tiHqjIsL8yaapX5XIAI6i0n```

# lv 23
```
Level Goal

A program is running automatically at regular intervals from cron, the time-based job scheduler. Look in /etc/cron.d/ for the configuration and see what command is being executed.

NOTE: This level requires you to create your own first shell-script. This is a very big step and you should be proud of yourself when you beat this level!

NOTE 2: Keep in mind that your shell script is removed once executed, so you may want to keep a copy around…
Commands you may need to solve this level

cron, crontab, crontab(5) (use “man 5 crontab” to access this)
```
okey.. this will be my first time writing a shell scrip too...
same as last time, check out what it crontab and find the original script
```console
bandit23@bandit:~$ cat /etc/cron.d/cronjob_bandit24
@reboot bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
* * * * * bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
bandit23@bandit:~$ cat /usr/bin/cronjob_bandit24.sh
#!/bin/bash

myname=$(whoami)

cd /var/spool/$myname
echo "Executing and deleting all scripts in /var/spool/$myname:"
for i in * .*;
do
    if [ "$i" != "." -a "$i" != ".." ];
    then
        echo "Handling $i"
        timeout -s 9 60 ./$i
        rm -f ./$i
    fi
done
```
each 60 sec, the script execute all script in /var/spool/$myname and remove it. 
so now let make it execute when we want (not each 1 min) by just copy the code and change $myname to bandit24
```console
$ mkdir /tmp/kurohat23
$ cd /tmp/kurohat23
§ nano bandit23.sh # copy script below, not that I commented timeout out,
#!/bin/bash

cd /var/spool/bandit24
echo "Executing and deleting all scripts in /var/spool/bandit24:"
for i in * .*;
do
    if [ "$i" != "." -a "$i" != ".." ];
    then
        echo "Handling $i"
        # timeout -s 9 60 ./$i
        rm -f ./$i
    fi
done
$ chmod 777 bandit23.sh #make it execute able
```
now let make a script which will fetch the password and output it to us
```console
$ nano fetchkey.sh
#!/bin/bash
cat /etc/bandit_pass/bandit24 > /tmp/kurohat23/key.txt #get password and put it in key.txt
$ chmod 777 fetchkey.sh  #make it execute able
$ touch key.txt # create key.txt for recieving password
$ chmod 666 key.txt # give everyone read/write permission
$ cp fetchkey.sh /var/spool/bandit24 # copy the script and put it in /var/spool/bandit24
$ ./bandit23.sh #run bandit23.sh
Executing and deleting all scripts in /var/spool/bandit24
Handling *
Handling .*
$ cat key.txt 
UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ
```
passpassword to the next lv : ```UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ```

# lv 24
```
Level Goal
A daemon is listening on port 30002 and will give you the password for bandit25 if given the password for bandit24 and a secret numeric 4-digit pincode. There is no way to retrieve the pincode except by going through all of the 10000 combinations, called brute-forcing.
```
So by read the goal we need to use netcat sending a current password + 4 digit pincode (0000-9999) let try out.
```console
bandit24@bandit:~$ echo "UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ 0000" | nc localhost 30002
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
Wrong! Please enter the correct pincode. Try again.
```
I got it right now we have to bructe force the pin code using shell script
```console
$ mkdir /tmp/kurohat24 # create directory
$ touch test.sh # create file
$ chmod 777 test.sh # make it execute able
$ nano test.sh # add this
#!/bin/bash
for i in {0000..00003}
do
   echo "pin $i"
done
$ ./test.sh # run it
pin 00000
pin 00001
pin 00002
pin 00003
```
now we have brute force pin that is wroking for 0000 - 0003. let add fucntion, let make it send stuff with netcat (```echo "UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ [pin]" | nc localhost 30002```)
```bash
#!/bin/bash
for i in {0000..00003}
do
  echo "UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ $i" 
done | nc localhost 30002
```
this is the result of running the script
```console
bandit24@bandit:/tmp/kurohat24$ ./test.sh 
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
Wrong! Please enter the correct pincode. Try again.
Wrong! Please enter the correct pincode. Try again.
Wrong! Please enter the correct pincode. Try again.
Wrong! Please enter the correct pincode. Try again.
Timeout. Exiting.
```
it works, now it is time for the action. The plan I will create 2 shell script. 1 will start from 0000 to 5000, another one start from 5001 to 9999. The respone from the server will be put in a file call 5000.txt and 50001.txt
```console
$ touch brute1.sh
$ touch brute2.sh
$ chmod 777 brute1.sh
$ chmod 777 brute2.sh
$ nano brute1.sh # put the script below
$ nano brute2.sh # put the script below
```
in brute1.sh
```bash
#!/bin/bash
for i in {0000..5000}
do
    echo "UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ $i"
done | nc localhost 30002 > 5000.txt # output the respons in a file

echo "done 0000-5000"
```
brute2.sh
```bash
#!/bin/bash
for i in {5001..9999}
do
    echo "UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ $i"
done | nc localhost 30002 > 5001.txt

echo "done 5001-9999"
```
now execute the scripts
```console
$ ./brute1.sh &
[1] 27330
$ ./brute2.sh 
done 5001-9999
$ done 0000-5000
[1]+  Done                    ./brute1.sh
$ cat 5000.txt | grep -v "Wrong" # 
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
Timeout. Exiting.
bandit24@bandit:/tmp/kurohat24$ cat 5001.txt | grep -v "Wrong"
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
Correct!
The password of user bandit25 is uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG

Exiting.
```

password to next the lv is: ```uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG```