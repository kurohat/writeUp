# recon
```console
kali@kali:~/script$ sudo python3 pymap.py -t $IP
[sudo] password for kali: 
created by gu2rks/kurohat 
find me here https://github.com/gu2rks

port scanning...
21/tcp open  ftp
22/tcp open  ssh
80/tcp open  http
Enumerating open ports...
Starting Nmap 7.80 ( https://nmap.org ) at 2020-08-09 12:30 EDT
Nmap scan report for 10.10.12.236
Host is up (0.041s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 c9:03:aa:aa:ea:a9:f1:f4:09:79:c0:47:41:16:f1:9b (RSA)
|   256 2e:1d:83:11:65:03:b4:78:e9:6d:94:d1:3b:db:f4:d6 (ECDSA)
|_  256 91:3d:e4:4f:ab:aa:e2:9e:44:af:d3:57:86:70:bc:39 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Beginning of the end
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.10 - 3.13 (95%), ASUS RT-N56U WAP (Linux 3.4) (95%), Linux 3.16 (95%), Linux 3.1 (93%), Linux 3.2 (93%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (92%), Linux 3.10 (92%), Linux 3.12 (92%), Linux 3.18 (92%), Linux 3.19 (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 22/tcp)
HOP RTT      ADDRESS
1   39.99 ms 10.11.0.1
2   40.52 ms 10.10.12.236

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 13.85 seconds
```

* /diningRoom/
  *  `<!-- SG93IGFib3V0_______= -->`
  *  yes for emblem flag
* How about the /teaRoom/
  * /master_of_unlock.html for lock_pick tool/flag
  * Barry also suggested that Jill should visit the /artRoom/
* /artRoom/
```
Look like a map

Location:
/diningRoom/
/teaRoom/
/artRoom/
/barRoom/
/diningRoom2F/
/tigerStatusRoom/
/galleryRoom/
/studyRoom/
/armorRoom/
/attic/
```
* /barRoom/ is lock
  * using lock_pick to unlock it
  * we found a note encoded in base__
    * ```NV2XG2LDL________``` 
  * play piano using the music sheet, the Secret bar room is opened
* Secret bar room
  * grab gold emblem flag
* /diningRoom2F/ encrypted ROT
  * `	<!-- Lbh trg gur oyhr trz ol chfuvat gur fgnghf gb gur ybjre sybbe. Gur trz vf ba gur qvavatEbbz svefg sybbe. Ivfvg fnccuver.ugzy -->       `
  *  You get the blue gem by pushing the status to the lower floor. The gem is on the diningRoom first floor. Visit `sa____.html`
  * visit `diningRoom/sa____.html `
  * grab the `blue_jewel`
* /tigerStatusRoom/ : ask for jewel/gem
```
crest 1:
S0pXRkVV____________
Hint 1: Crest 1 has been encoded twice
Hint 2: Crest 1 contanis 14 letters
Note: You need to collect all 4 crests, combine and decode to reavel another path
The combination should be crest 1 + crest 2 + crest 3 + crest 4. Also, the combination is a type of encoded base and you need to decode it
```
* /galleryRoom/
```
crest 2:
GVFWK5________
Hint 1: Crest 2 has been encoded twice
Hint 2: Crest 2 contanis 18 letters
Note: You need to collect all 4 crests, combine and decode to reavel another path
The combination should be crest 1 + crest 2 + crest 3 + crest 4. Also, the combination is a type of encoded base and you need to decode it
```
* /studyRoom/: ask for helmet emblem
* /armorRoom/: ask for sheild emblem
* /attic/: ask for sheild emblem


back to /dinnerRoom/ I put gold emblem flag and got this
`klfvg ks r wimgnd biz mpuiui ulg fiemok tqod. Xii jvmc tbkg ks tempgf <somethinghere>`

back to secret room in bar room. i put emblem and got a username ? `rebecca`

after thinking back and forward, we have a cipher and we got a username? From the look of cipher it is a subtitution cipher. Then it kicks me, `rebecca` might be a password of a cipher (Vigenere). decode it to get a 

```
there is a shield key inside the dining room. The html page is called the________
```
/diningRoom/the________ to get `shield_key`


now back to `/armorRoom/`, enther the `shield_key`
```
crest 3:
MDAx<and more>
Hint 1: Crest 3 has been encoded three times
Hint 2: Crest 3 contanis 19 letters
Note: You need to collect all 4 crests, combine and decode to reavel another path
The combination should be crest 1 + crest 2 + crest 3 + crest 4. Also, the combination is a type of encoded base and you need to decode it
```
now visit `/attic/` and put shield_key
```
crest 4:
gSUERau_________________
Hint 1: Crest 2 has been encoded twice
Hint 2: Crest 2 contanis 17 characters
Note: You need to collect all 4 crests, combine and decode to reavel another path
The combination should be crest 1 + crest 2 + crest 3 + crest 4. Also, the combination is a type of encoded base and you need to decode it
```


now let decode each **crests**
* crest 1: Base64 -> Base32
* crest 2: Base32 -> Base58
* crest 3: base 64 -> binary -> hex
* crest 4 base58 -> hex

now put it together: crest 1 + crest 2 + crest 3 + crest 4: and decode base64
  * ```RlRQIHVzZXI6IGh1bnRlciwgRlRQIHBhc3M_________________==```

## ftp
```console
kali@kali:~/THM/biohazard$ ftp $IP
Connected to 10.10.12.236.
220 (vsFTPd 3.0.3)
Name (10.10.12.236:kali): hunter
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 0        0            7994 Sep 19  2019 001-key.jpg
-rw-r--r--    1 0        0            2210 Sep 19  2019 002-key.jpg
-rw-r--r--    1 0        0            2146 Sep 19  2019 003-key.jpg
-rw-r--r--    1 0        0             121 Sep 19  2019 helmet_key.txt.gpg
-rw-r--r--    1 0        0             170 Sep 20  2019 important.txt
```

```console
kali@kali:~/THM/biohazard$ cat important.txt 
Jill,

I think the helmet key is inside the text file, but I have no clue on decrypting stuff. Also, I come across a /hidden_closet/ door but it was locked.

From,
Barry
```
so new clue.. `/hidden_closet/`

# steganography
- 001-key.jpg
```
kali@kali:~/THM/biohazard$ stegcracker 001-key.jpg 
kali@kali:~/THM/biohazard$ cat 001-key.jpg.out 
cGxhbnQ_____
```

- 002-key.jpg: in comment
```
kali@kali:~/THM/biohazard$ exiftool 002-key.jpg 
ExifTool Version Number         : 11.99
File Name                       : 002-key.jpg
Directory                       : .
File Size                       : 2.2 kB
File Modification Date/Time     : 2020:08:09 13:42:25-04:00
File Access Date/Time           : 2020:08:09 13:45:35-04:00
File Inode Change Date/Time     : 2020:08:09 13:42:25-04:00
File Permissions                : rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
Comment                         : 5fYmVf_____
Image Width                     : 100
Image Height                    : 80
Encoding Process                : Progressive DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 100x80
Megapixels                      : 0.008
```

- 003-key.jpg 
```console
[10.11.14.220]  kali@kali:~/THM/biohazard$ binwalk -e 003-key.jpg

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
1930          0x78A           Zip archive data, at least v2.0 to extract, uncompressed size: 14, name: key-003.txt
2124          0x84C           End of Zip archive, footer length: 22

[10.11.14.220]  kali@kali:~/THM/biohazard$ ls
001-key.jpg      002-key.jpg  _003-key.jpg.extracted  important.txt
001-key.jpg.out  003-key.jpg  helmet_key.txt.gpg
[10.11.14.220]  kali@kali:~/THM/biohazard$ cd _003-key.jpg.extracted/
[10.11.14.220]  kali@kali:~/THM/biohazard/_003-key.jpg.extracted$ ls
78A.zip  key-003.txt
[10.11.14.220]  kali@kali:~/THM/biohazard/_003-key.jpg.extracted$ cat key-003.txt 
3aXRoX______
```

plant42_can_be_destroy_with_vjolt
```console
kali@kali:~/THM/biohazard$ gpg -d helmet_key.txt.gpg 
gpg: AES256 encrypted data
gpg: encrypted with 1 passphrase
helmet_key{458493193501________}
```

back to `/studyRoom/` put `helmet_key`. download the .tar and extract it. you will get SSH username 
`SSH user: umbrella_guest`

in `/hidden_closet/` you will find `wolf_medal.txt` which contain ssh password 
```
SSH password: T_virus_rules
```
also you will find a cipher again. I guess it is encoded with Vigenere, again.. let ssh to victim server and find the key to the cipher.


## foot hold
```console
umbrella_guest@umbrella_corp:~/.jailcell$ cat chris.txt 
Jill: Chris, is that you?
Chris: Jill, you finally come. I was locked in the Jail cell for a while. It seem that weasker is behind all this.
Jil, What? Weasker? He is the traitor?
Chris: Yes, Jill. Unfortunately, he play us like a damn fiddle.
Jill: Let's get out of here first, I have contact brad for helicopter support.
Chris: Thanks Jill, here, take this MO Disk 2 with you. It look like the key to decipher something.
Jill: Alright, I will deal with him later.
Chris: see ya.

MO disk 2: albert 
```

albert is the key to the cipher we fond at `/hidden_closet/`. now decipher it.
`weasker` login password, `stars__________`

# root

```console
weasker@umbrella_corp:~$ sudo -l
[sudo] password for weasker: 
Matching Defaults entries for weasker on umbrella_corp:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User weasker may run the following commands on umbrella_corp:
    (ALL : ALL) ALL
```
damn we can run anything as with sudo!.
```console
weasker@umbrella_corp:~$ sudo cat /root/root.txt
In the state of emergency, Jill, Barry and Chris are reaching the helipad and awaiting for the helicopter support.

Suddenly, the Tyrant jump out from nowhere. After a tough fight, brad, throw a rocket launcher on the helipad. Without thinking twice, Jill pick up the launcher and fire at the Tyrant.

The Tyrant shredded into pieces and the Mansion was blowed. The survivor able to escape with the helicopter and prepare for their next fight.

The End

flag: 3c5794a00__________
weasker@umbrella_corp:~$ 
```