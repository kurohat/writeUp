```console
kali@kali:~/HTB/Admirer$ sudo nmap -p21,22,80 --script vuln -A  admirer
sudo: unable to resolve host kali: Name or service not known
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-08 19:23 EDT
Nmap scan report for admirer (10.10.10.187)
Host is up (0.035s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
|_sslv2-drown: 
22/tcp open  ssh     OpenSSH 7.4p1 Debian 10+deb9u7 (protocol 2.0)
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
80/tcp open  http    Apache httpd 2.4.25 ((Debian))
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
| http-csrf: 
| Spidering limited to: maxdepth=3; maxpagecount=20; withinhost=admirer
|   Found the following possible CSRF vulnerabilities: 
|     
|     Path: http://admirer:80/
|     Form id: name
|_    Form action: #
|_http-dombased-xss: Couldn't find any DOM based XSS.
| http-enum: 
|_  /robots.txt: Robots file
| http-fileupload-exploiter: 
|   
|     Couldn't find a file-type field.
|   
|_    Couldn't find a file-type field.
|_http-server-header: Apache/2.4.25 (Debian)
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
|_http-vuln-cve2017-1001000: ERROR: Script execution failed (use -d to debug)
| vulners: 
|   cpe:/a:apache:http_server:2.4.25: 
|       CVE-2017-7679   7.5     https://vulners.com/cve/CVE-2017-7679
|       CVE-2017-7668   7.5     https://vulners.com/cve/CVE-2017-7668
|       CVE-2017-3169   7.5     https://vulners.com/cve/CVE-2017-3169
|       CVE-2017-3167   7.5     https://vulners.com/cve/CVE-2017-3167
|       CVE-2019-0211   7.2     https://vulners.com/cve/CVE-2019-0211
|       CVE-2018-1312   6.8     https://vulners.com/cve/CVE-2018-1312
|       CVE-2017-15715  6.8     https://vulners.com/cve/CVE-2017-15715
|       CVE-2019-10082  6.4     https://vulners.com/cve/CVE-2019-10082
|       CVE-2017-9788   6.4     https://vulners.com/cve/CVE-2017-9788
|       CVE-2019-0217   6.0     https://vulners.com/cve/CVE-2019-0217
|       CVE-2020-1927   5.8     https://vulners.com/cve/CVE-2020-1927
|       CVE-2019-10098  5.8     https://vulners.com/cve/CVE-2019-10098
|       CVE-2020-1934   5.0     https://vulners.com/cve/CVE-2020-1934
|       CVE-2019-10081  5.0     https://vulners.com/cve/CVE-2019-10081
|       CVE-2019-0220   5.0     https://vulners.com/cve/CVE-2019-0220
|       CVE-2019-0196   5.0     https://vulners.com/cve/CVE-2019-0196
|       CVE-2018-17199  5.0     https://vulners.com/cve/CVE-2018-17199
|       CVE-2018-1333   5.0     https://vulners.com/cve/CVE-2018-1333
|       CVE-2017-9798   5.0     https://vulners.com/cve/CVE-2017-9798
|       CVE-2017-7659   5.0     https://vulners.com/cve/CVE-2017-7659
|       CVE-2017-15710  5.0     https://vulners.com/cve/CVE-2017-15710
|       CVE-2019-0197   4.9     https://vulners.com/cve/CVE-2019-0197
|       CVE-2019-10092  4.3     https://vulners.com/cve/CVE-2019-10092
|       CVE-2018-11763  4.3     https://vulners.com/cve/CVE-2018-11763
|_      CVE-2018-1283   3.5     https://vulners.com/cve/CVE-2018-1283
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.10 - 4.11 (94%), Linux 3.13 (94%), Linux 3.16 (94%), Linux 3.16 - 4.6 (94%), Linux 3.18 (94%), Linux 3.2 - 4.9 (94%), Linux 4.2 (94%), Linux 4.4 (94%), Linux 3.12 (94%), Linux 3.13 or 4.2 (94%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 21/tcp)
HOP RTT      ADDRESS
1   33.62 ms 10.10.14.1
2   33.73 ms admirer (10.10.10.187)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 43.89 seconds
```

let check ftp

```console
kali@kali:~/HTB/Admirer$ ftp admirer 
Connected to admirer.
220 (vsFTPd 3.0.3)
Name (admirer:kali): 
530 Permission denied.
Login failed.
ftp> 
```

# Enumerate

```console
kali@kali:~$ gobuster dir -t50 -u 10.10.10.187 ercase-2.3-medium.txt -x .php,.txt,.html
===============================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmau
===============================================
[+] Url:            http://10.10.10.187
[+] Threads:        50
[+] Wordlist:       /usr/share/wordlists/dirbus
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     php,txt,html
[+] Timeout:        10s
===============================================
2020/06/08 19:44:46 Starting gobuster
===============================================
/assets (Status: 301)
/images (Status: 301)
/index.php (Status: 200)
/robots.txt (Status: 200)
/server-status (Status: 403)
===============================================================
2020/06/08 20:00:59 Finished
===============================================================
```
checking robot.txt
```
User-agent: *

# This folder contains personal contacts and creds, so no one -not even robots- should see it - waldo
Disallow: /admin-dir
```
I check ```/admin-dir``` but I got 403. let brute force the content inside ```/admin-dir``` might find something good. In this case Im using ```/SecLists/Discovery/Web-Content/big.txt```. But suddenly my *gobuster* start acting werid...

```console
kali@kali:~$ gobuster dir -t50 -u 10.10.10.187/admin-dir -w /usr/share/SecLists/Discovery/Web-Content/big.txt -x .php,.txt,.html
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.10.187/admin-dir
[+] Threads:        50
[+] Wordlist:       /usr/share/SecLists/Discovery/Web-Content/big.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     txt,html,php
[+] Timeout:        10s
===============================================================
2020/06/08 20:28:33 Starting gobuster
===============================================================
Error: error on running goubster: unable to connect to http://10.10.10.187/admin-dir/: Get http://10.10.10.187/admin-dir/: net/http: request canceled (Client.Timeout exceeded while awaiting headers)
```
I then try to use wfuzz instead.
```console
ali@kali:~$ wfuzz -c -u http://10.10.10.187/admin-dir/FUZZ.FUZ2Z -w /usr/share/SecLists/Discovery/Web-Content/big.txt -z list,txt-php-html -t 100 --hc 404

Warning: Pycurl is not compiled against Openssl. Wfuzz might not work correctly when fuzzing SSL sites. Check Wfuzz's documentation for more information.

********************************************************
* Wfuzz 2.4.5 - The Web Fuzzer                         *
********************************************************

Target: http://10.10.10.187/admin-dir/FUZZ.FUZ2Z
Total requests: 61419

===================================================================
ID           Response   Lines    Word     Chars       Payload                           
===================================================================

000000043:   403        9 L      28 W     277 Ch      ".htaccess - txt"                 
000000044:   403        9 L      28 W     277 Ch      ".htaccess - php"                 
000000045:   403        9 L      28 W     277 Ch      ".htaccess - html"                
000000046:   403        9 L      28 W     277 Ch      ".htpasswd - txt"                 
000000047:   403        9 L      28 W     277 Ch      ".htpasswd - php"                 
000000048:   403        9 L      28 W     277 Ch      ".htpasswd - html"                
000015592:   200        29 L     39 W     350 Ch      "contacts - txt"                  
000016327:   200        11 L     13 W     136 Ch      "credentials - txt"     
```
Here is contacts.txt
```
##########
# admins #
##########
# Penny
Email: p.wise@admirer.htb


##############
# developers #
##############
# Rajesh
Email: r.nayyar@admirer.htb

# Amy
Email: a.bialik@admirer.htb

# Leonard
Email: l.galecki@admirer.htb



#############
# designers #
#############
# Howard
Email: h.helberg@admirer.htb

# Bernadette
Email: b.rauch@admirer.htb
```
just email... nothing really interestting here. now let check ```credentials.txt```
```
[Internal mail account]
w.cooper@admirer.htb
fgJr6q#S\W:$P

[FTP account]
ftpuser
%n?4Wz}R$tTF7

[Wordpress account]
admin
w0rdpr3ss01!
```
I got the password for ftp server. let connect to it
```console
kali@kali:~/HTB/Admirer$ ftp admirer 
Connected to admirer.
220 (vsFTPd 3.0.3)
Name (admirer:kali): ftpuser
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 0        0            3405 Dec 02  2019 dump.sql
-rw-r--r--    1 0        0         5270987 Dec 03  2019 html.tar.gz
226 Directory send OK.
ftp> binary
200 Switching to Binary mode.
ftp> get dump.sql
local: dump.sql remote: dump.sql
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for dump.sql (3405 bytes).
226 Transfer complete.
3405 bytes received in 0.00 secs (13.8181 MB/s)
ftp> get html.tar.gz
local: html.tar.gz remote: html.tar.gza
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for html.tar.gz (5270987 bytes).
226 Transfer complete.
5270987 bytes received in 5.11 secs (1008.0114 kB/s)
ftp> exit
221 Goodbye
```
As you can see. I dump all files in the server. In html.tar.gz you will find a lot of juicy stuff. I seem like it is a old version of the target web app. here is: ```credentials.txt```. it include a bank account...
```
[Bank Account]
waldo.11
Ezy]m27}OREc$

[Internal mail account]
w.cooper@admirer.htb
fgJr6q#S\W:$P

[FTP account]
ftpuser
%n?4Wz}R$tTF7

[Wordpress account]
admin
w0rdpr3ss01!
```
```index.php```
```php
$servername = "localhost";
$username = "waldo";
$password = "]F7jLHw:*G>UPrTo}~A"d6b";
$dbname = "admirerdb";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT * FROM items";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "<article class='thumb'>";
        echo "<a href='".$row["image_path"]."' class='image'><img src='".$row["thumb_path"]."' alt='' /></a>";
        echo "<h2>".$row["title"]."</h2>";
        echo "<p>".$row["text"]."</p>";
        echo "</article>";
    }
} else {
    echo "0 results";
}
$conn->close();
```
inside ```utility-scripts```
```console
kali@kali:~/HTB/Admirer/html/utility-scripts$ ls
admin_tasks.php  db_admin.php  info.php  phptest.php
```
now let check all those directory on the current web app. all this php might still there, ```admin_task.php``` might help us get smth

I tried to play around with ```admin_task.php```, removed the **disabled** tag so that I can press *Backup shadow file* but I do not have permission so I think I was going to the wrong direction.

Out of all the file in ```utility-scripts```, ```db_admin.php``` is the only page that do not exist in the current version. let check ```db_admin.php```:
```php
<?php
  $servername = "localhost";
  $username = "waldo";
  $password = "Wh3r3_1s_w4ld0?";

  // Create connection
  $conn = new mysqli($servername, $username, $password);

  // Check connection
  if ($conn->connect_error) {
      die("Connection failed: " . $conn->connect_error);
  }
  echo "Connected successfully";


  // TODO: Finish implementing this or find a better open source alternative
?>
```
https://medium.com/bugbountywriteup/adminer-script-results-to-pwning-server-private-bug-bounty-program-fe6d8a43fe6f
https://www.foregenix.com/blog/serious-vulnerability-discovered-in-adminer-tool