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

```
