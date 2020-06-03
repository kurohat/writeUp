# Recon
```console
kali@kali:~/vulnUniversity$ nmap -p- 10.10.154.5 # what port are open
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-30 19:32 EDT
Nmap scan report for 10.10.154.5
Host is up (0.045s latency).
Not shown: 65529 closed ports
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3128/tcp open  squid-http
3333/tcp open  dec-notes

Nmap done: 1 IP address (1 host up) scanned in 22.64 seconds
kali@kali:~/vulnUniversity$ nmap -p3128 -sV 10.10.154.5 # check service version on port 3128
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-30 19:34 EDT
Nmap scan report for 10.10.154.5
Host is up (0.045s latency).

PORT     STATE SERVICE    VERSION
3128/tcp open  http-proxy Squid http proxy 3.5.12

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.16 seconds

kali@kali:~/vulnUniversity$ nmap -p3333 -sV 10.10.154.5 # http and OS
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-30 19:47 EDT
Nmap scan report for 10.10.154.5
Host is up (0.047s latency).

PORT     STATE SERVICE VERSION
3333/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 22.23 seconds
```
# [Task 3] Locating directories using GoBuster 
```console
kali@kali:~/vulnUniversity$ gobuster dir -u http://10.10.154.5:3333 -w /usr/share/wordlists/dirbuster/directory-list-1.0.txt 
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.154.5:3333
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-1.0.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/05/30 19:52:11 Starting gobuster
===============================================================
/images (Status: 301)
/css (Status: 301)
/js (Status: 301)
/internal (Status: 301)
===============================================================
2020/05/30 20:03:18 Finished
=========================================================
```
Try each one of them and find out



```console
kali@kali:~/HTB$ cat prod.dtsConfig 
<DTSConfiguration>
    <DTSConfigurationHeading>
        <DTSConfigurationFileInfo GeneratedBy="..." GeneratedFromPackageName="..." GeneratedFromPackageID="..." GeneratedDate="20.1.2019 10:01:34"/>
    </DTSConfigurationHeading>
    <Configuration ConfiguredType="Property" Path="\Package.Connections[Destination].Properties[ConnectionString]" ValueType="String">
        <ConfiguredValue>Data Source=.;Password=M3g4c0rp123;User ID=ARCHETYPE\sql_svc;Initial Catalog=Catalog;Provider=SQLNCLI10.1;Persist Security Info=True;Auto Translate=False;</ConfiguredValue>
    </Configuration>
</DTSConfiguration>

#  type C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt 
net.exe use T: \\Archetype\backups /user:administrator MEGACORP_4dm1n!!
exit
```

C:\Users\Administrator\Desktop>type root.txt
b91ccec3305e98240082d4474b848528

C:\Users\sql_svc\Desktop
