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