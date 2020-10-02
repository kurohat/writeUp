# SAMBA
Samba is the standard Windows interoperability suite of programs for Linux and Unix. It allows end users to access and use files, printers and other commonly shared resources on a companies intranet or internet. Its often refereed to as a network file system.


Samba is based on the common client/server protocol of Server Message Block (SMB). SMB is developed only for Windows, without Samba, other computer platforms would be isolated from Windows machines, even if they were part of the same network.
![pic](https://i.imgur.com/bkgVNy3.png)
# enumerate using nmap
```
nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse <ip>
```

# smbclient
- connect to smb : ```smbclient //<ip>/<dir>```
- list dirs : ```smbclient -L //<ip>```

# smbget
wget-like utility for download files over SMB
- recursive geting all files in smb
