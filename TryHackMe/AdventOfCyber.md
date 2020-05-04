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
echo '***' > christmas_list.txt
```
```***``` is the answer to this question
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
$6$3GvJsNPG$ZrSFprHS13divBhlaKg1rYrYLJ7m1xsYRKxlLh0A1sUc/6SUd7UvekBOtSnSyBwk3vCDqBhrgxQpkdsNN6aYP1:*******
```
find out what ```*******``` is. GL