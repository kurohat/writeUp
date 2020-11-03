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
- `src/login.php`: cerdential  `tbhguest:WelcomeTBH1!`
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
- 