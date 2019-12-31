# Description
This VM tells us that there are a couple of lovers namely Alice and Bob, where the couple was originally very romantic, but since Alice worked at a private company, "Ceban Corp", something has changed from Alice's attitude towards Bob like something is "hidden", And Bob asks for your help to get what Alice is hiding and get full access to the company!

* Difficulty LevelBeginner
* Notes: there are 2 flag files
* Learning: Web Application | Simple Privilege Escalation

# Footprinting
We need more information about the target by
starting with, find out the ip address of the target by using Nmap

```console
nmap -F [ip address/mask]
```

The figure below shows the results:
<p align="center">
<img src="/meAndMyGf1/pic/target.png">
</p>

at this point, we can now use the web browser to access to target's web page. Follow by ***inspect element***. the result:

```html
Who are you? Hacker? Sorry This Site Can Only Be Accessed local!<!-- Maybe you can search how to use x-forwarded-for -->
```

As you can see, the create of this CTF gave use a hint that we should use **x-forwarded-for** get the first flag

to find **more** information about the target

```console
nmap -A -sV -O [ip address] > meAndMyGf.txt
```
Where:
* -sV = Version scanning
* -A = Version scanning
* -O = OS detection

We also put the result from nmap in a file. This will help us to save some time since we do not need to run this command to get target info again.

here is the result from runing the command above:
```
Starting Nmap 7.80 ( https://nmap.org ) at 2019-12-31 13:24 EST
Nmap scan report for 192.168.0.30
Host is up (0.00056s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 3b:26:4d:e4:a0:3b:f8:75:d9:6e:15:55:82:8c:71:97 (RSA)
|   256 8f:48:97:9b:55:11:5b:f1:6c:1d:b3:4a:bc:36:bd:b0 (ECDSA)
|_  256 d0:c3:02:a1:c4:c2:a8:ac:3b:84:ae:8f:e5:79:66:76 (ED25519)
80/tcp open  http    Apache httpd 2.4.7 ((Ubuntu))
|_http-server-header: Apache/2.4.7 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
MAC Address: 00:0C:29:0D:53:C5 (VMware)
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.2 - 4.9
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE
HOP RTT     ADDRESS
1   0.56 ms 192.168.0.30

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 19.42 seconds
```