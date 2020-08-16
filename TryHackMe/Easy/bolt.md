# recon 
3 open ports:
- 22/tcp   open  ssh
- 80/tcp   open  http, *apache it working page*
- 8000/tcp open  http-alt


## port 8000
- admin = Jake
```console
$ gobuster dir -u http://$IP:8000/ -w /usr/share/SecLists/Discovery/Web-Content/big.txt -t 54
.
/.htaccess (Status: 200)
/async (Status: 401)
/entries (Status: 200)
/pages (Status: 200)
/search (Status: 200)
.
```
notthing interesting from gobuster

let do a *happy path*, there are two posts:
- `entry/message-for-it-department` -> t! my password is `boltadmin123` just incase you need it!
- `/entry/message-from-admin`: myself Jake and my username is bolt

then I found link to this site https://bolt.cm/. The link can be found on `navbar` (The Bolt Site) and site footer (© 2020 • This website is Built with Bolt.) After some digging I found a cms/log in page: `/bolt`

now log into the cms using the credential we found here. Note that the website use **Bolt Version: 3.7.1**. If you goolge about bolt exploit you will easily find a RCE exploit on metasploit (check [here](https://www.rapid7.com/db/modules/exploit/unix/webapp/bolt_authenticated_rce))

so no more talk let run metasploit and get foothold

# foot hold/root
follow the steps on rapid7 link above, you need to `set` username,password,rhost, and lhost then `run`

Boom! you should get foothold to victim's server. run `which python/python3` to check if `python2.7` or `python3` is installed. we will use it to spawn a *tty shell*

```console
which python3
/usr/bin/python3
python3 -c 'import pty; pty.spawn("/bin/sh")'
# whoami
whoami
root
# pwd    
pwd
/home
# ls
ls
bolt  composer-setup.php  flag.txt
```
luckly we gain root by just get foothold, you see why you should not run any service on ur server as a root. coz if someone hack you, they gain root access on ur server at ones.
