# Tools
- linpeas.sh
- suid3num.py
- pspy
- ltrace

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
