# enumating
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

so what? just encrypt rockyou and try out to bruteforce it?

userlist.txt
admin
Ninja
Pars
Szymex
Bee
MuirlandOracle

