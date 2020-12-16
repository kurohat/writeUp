# Tools
- linpeas.sh
- suid3num.py
- pspy
- ltrace
- enum4linux


# links
- https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation/

# get linux OS info
- https://www.cyberciti.biz/faq/how-to-check-os-version-in-linux-command-line/
```console
$ cat /etc/*release
$ uname -a 
```

# TTY shell
```console
$ python -c 'import pty; pty.spawn("/bin/bash")'
$ python3 -c 'import pty; pty.spawn("/bin/sh")'
$ echo os.system('/bin/bash')
$ /bin/sh -i
```
now `^z` (background) it
```
stty raw -echo;fg
export TERM=xterm
```
auto tab is good to go!
# Linux capacity
```console
$ getcap -r / 2>/dev/null
```
# cronjob
```console
$ for i in d hourly daily weekly monthly; do echo; echo "--cron.$i--"; ls -l /etc/cron.$i; done
```

# echo "#!/bin/bash"
```console
$ set +H
$ echo "#!/bin/bash" > shell.sh
```

# enum4linux
@ `/usr/share/enum4linux/enum4linux.pl` by default
- samba/smb
```console
/usr/share/enum4linux/enum4linux.pl -U 10.10.223.29 # user
/usr/share/enum4linux/enum4linux.pl -S 10.10.223.29 # sharelist
```