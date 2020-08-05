## nmap
```
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
| http-robots.txt: 4 disallowed entries 
|_/bin/ /config/ /umbraco/ /umbraco_client/
|_http-title: Anthem.com - Welcome to our blog
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: WIN-LU09299160F
|   NetBIOS_Domain_Name: WIN-LU09299160F
|   NetBIOS_Computer_Name: WIN-LU09299160F
|   DNS_Domain_Name: WIN-LU09299160F
|   DNS_Computer_Name: WIN-LU09299160F
|   Product_Version: 10.0.17763
|_  System_Time: 2020-08-01T11:44:11+00:00
| ssl-cert: Subject: commonName=WIN-LU09299160F
| Not valid before: 2020-04-04T22:56:38
|_Not valid after:  2020-10-04T22:56:38
|_ssl-date: 2020-08-01T11:44:19+00:00; +1s from scanner time.
```
## task 1 web recon
- Jane Doe : JD@anthem.com
- /SiteMap
    - /archive/
    - /archive/we-are-hiring/
    - /archive/a-cheers-to-our-it-department/
    - /authors/
    - /authors/jane-doe/
- robots.txt
```
<admin password>

# Use for all search robots
User-agent: *

# Define the directories not to crawl
Disallow: /bin/
Disallow: /config/
Disallow: /umbraco/
Disallow: /umbraco_client/
```
- domain : Anthem.com. (on the web header & footer)
- /archive/a-cheers-to-our-it-department/: info about admin
```
As we all around here knows how much I love writing poems I decided to write one about him:

Born on a Monday,
Christened on Tuesday,
Married on Wednesday,
Took ill on Thursday,
Grew worse on Friday,
Died on Saturday,
Buried on Sunday.
That was the end…              
```
wanna know admin's name? google his name.
- admin email? Jane Doe has JD@anthem.com as his/her email, what can admin have? (XX@anthem.com)

# task 2: flags
1. metadata tag
2. view src
3. auther
4. metadata tag

# task 3:
we know that the server run remote desktop (RDP) service (port 3389). Moreover, we have user credential which we can remote login to the server. I'm using [Remmina](https://remmina.org/). Now filled in server ip, username, password, and lastly domain which we got from nmap scan. see figure below:
![rdp](pic/Screenshot%202020-08-01%20at%2016.16.24.png)
now press save and connect!! BOOM! we are in, grab user flag on the desktop.

before we enumerate the server, let start with fixing `File Explorer` so that we can see hidden file: how to do that?
![hidden](https://msegceporticoprodassets.blob.core.windows.net/inline-media/e84efe1a-ea59-4b5b-a19e-773ad9cbef3c-en)

now look aroud, you will find a interesting file in `C:` note that you cannot read the .txt file coz we dont have premission. The funny part is we are able to edit the premission. Add the `SG` to the permission list as the figure belows:
![permision](pic/Screenshot%202020-08-01%20at%2017.25.20.png)

Voilà ! it seem like it is a admin password. you can RDP to the server using Administrator as username to gain root OR. spawn a shell as root user, which a simple cmd that I found [here](https://superuser.com/questions/617732/running-programs-as-root-in-non-root-shell-powershell)

here is what I did,
![root](pic/Screenshot%202020-08-01%20at%2016.27.25.png)
