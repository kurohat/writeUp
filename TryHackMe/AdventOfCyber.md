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