start with ```echo '<ip> blunder' >> /etc/hosts```


from now we can use ```blunder``` when we scan/enumerate and such no need to remember ip address.
now scan for open port
```console
kali@kali:~/HTB/blunder$ sudo nmap -sS -p- -vv blunder
.
.
PORT   STATE  SERVICE REASON
21/tcp closed ftp     reset ttl 63
80/tcp open   http    syn-ack ttl 63
.
kali@kali:~/HTB/blunder$ sudo nmap -A -p21,80 blunder
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-04 19:56 EDT
Nmap scan report for blunder (10.10.10.191)
Host is up (0.15s latency).                                                                        
                                                                                                   
PORT   STATE  SERVICE VERSION                                                                      
21/tcp closed ftp                                                                                  
80/tcp open   http    Apache httpd 2.4.41 ((Ubuntu))                                               
|_http-generator: Blunder                                                                          
|_http-server-header: Apache/2.4.41 (Ubuntu)                                                       
|_http-title: Blunder | A blunder of interesting facts                                             
Aggressive OS guesses: HP P2000 G3 NAS device (91%), Linux 2.6.32 (90%), Infomir MAG-250 set-top box (90%), Ubiquiti AirMax NanoStation WAP (Linux 2.6.32) (90%), Ubiquiti AirOS 5.5.9 (90%), Ubiquiti Pico Station WAP (AirOS 5.2.6) (89%), Linux 2.6.32 - 3.13 (89%), Linux 3.3 (89%), Linux 2.6.32 - 3.1 (89%), Linux 3.7 (89%)                                                                          
No exact OS matches for host (test conditions non-ideal).                                          
Network Distance: 2 hops

TRACEROUTE (using port 21/tcp)
HOP RTT       ADDRESS
1   34.97 ms  10.10.14.1
2   148.57 ms blunder (10.10.10.191)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 19.92 seconds
```
Note that there 2 ports open, *21 ftp* which means nothing to use since it is close and *80 http run on Apache httpd 2.4.41 ((Ubuntu))*


I recon web app, did find anything juicy so I decided to run nmap vuln scan to find out if more about port 80
```console
kali@kali:~/HTB/blunder$ nmap --script vuln -p80 blunder
PORT   STATE SERVICE REASON
80/tcp open  http    syn-ack ttl 63
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
|_http-csrf: Couldn't find any CSRF vulnerabilities.
|_http-dombased-xss: Couldn't find any DOM based XSS.
| http-enum: 
|   /admin/: Possible admin folder
|   /admin/admin/: Possible admin folder
|   /admin/account.php: Possible admin folder
|   /admin/index.php: Possible admin folder
|   /admin/login.php: Possible admin folder
|   /admin/admin.php: Possible admin folder
|   /admin/index.html: Possible admin folder
|   /admin/login.html: Possible admin folder
|   /admin/admin.html: Possible admin folder
|   /admin/home.php: Possible admin folder
|   /admin/controlpanel.php: Possible admin folder
|   /admin/account.html: Possible admin folder
|   /admin/admin_login.html: Possible admin folder
|   /admin/cp.php: Possible admin folder
|   /admin/admin_login.php: Possible admin folder
|_  /admin/admin-login.php: Possible admin folder
|_http-jsonp-detection: Couldn't find any JSONP endpoints.
|_http-litespeed-sourcecode-download: Request with null byte did not work. This web server might not be vulnerable
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
|_http-wordpress-users: [Error] Wordpress installation was not found. We couldn't find wp-login.php
```
seem like there is a admin login page and I found out that the web app is build on ```BLUDIT```, but any way we still need a cerdential


let run ```gobuster``` and try to find more pages
```console
kali@kali:~/HTB/blunder$ gobuster dir -u http://10.10.10.191 -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt -x txt,.php,.html -t 40
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.10.191
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     txt
[+] Timeout:        10s
===============================================================
2020/06/04 20:38:21 Starting gobuster
===============================================================
/about (Status: 200)
/0 (Status: 200)
/admin (Status: 301)
/empty (Status: 200)
/robots.txt (Status: 200)
/todo.txt (Status: 200)
/usb (Status: 200)
.
.
.
```
after go through some of those. I found something really intressting ```todo.txt```, I found a username.


Seem like ```BLUDIT``` have some anti brutefoce mechanism. read [here](https://docs.bludit.com/en/security/brute-force-protection)


after keep diging more I found [CVE-2019-17240](https://nvd.nist.gov/vuln/detail/CVE-2019-17240). now we are talking woop woop. I found a script [here](https://rastating.github.io/bludit-brute-force-mitigation-bypass/). It should work after some fixing and make it read password from ```rockyou.txt```


I spend a lot of thime try to work on the script. But then I found out that there is **no need bruteforce on any box in HTB**
So I spend more time on looking for ```BLUDIT``` CVE on this [link](https://www.cvedetails.com/vulnerability-list/vendor_id-17229/product_id-41420/Bludit-Bludit.html) BUT I didn't find anything interesting.


So I went back to the web page and read each post, I might missed something. I try a lot of stuff out lol, I started with *USB* then move on to *stadia*, lastly, *stephen-king-0*.


in *stephen-king-0* a charrector is mentioned and it looks weird for me, a name should sperate firstname and lastname but in this case it merge together. Moreover, any name that mentioned in this post always spererated so I give it a try and........


BINGO, I got ```fergus``` credential

