start of with nmap.
```
22/tcp  open  ssh
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds
```
let's use enum4linux to enumerate smb, start with sharelist 
```
```console
$ /usr/share/enum4linux/enum4linux.pl -S 10.10.223.29

 ========================================= 
|    Share Enumeration on 10.10.223.29    |
 ========================================= 

	Sharename       Type      Comment
	---------       ----      -------
	tbfc-hr         Disk      tbfc-hr
	tbfc-it         Disk      tbfc-it
	tbfc-santa      Disk      tbfc-santa
	IPC$            IPC       IPC Service (tbfc-smb server (Samba, Ubuntu))
```
now let's enumerate users
```console
$ /usr/share/enum4linux/enum4linux.pl -U 10.10.223.29
 ============================= 
|    Users on 10.10.223.29    |
 ============================= 
index: 0x1 RID: 0x3e8 acb: 0x00000010 Account: elfmcskidy	Name: 	Desc: 
index: 0x2 RID: 0x3ea acb: 0x00000010 Account: elfmceager	Name: elfmceager	Desc: 
index: 0x3 RID: 0x3e9 acb: 0x00000010 Account: elfmcelferson	Name: 	Desc: 
```
let use nmap (pymap) to enumerate smb and each sharelink to check if any of it allow anonymous login
```console
$ sudo /opt/pymap.py -t 10.10.223.29 -smb
Host script results:
| smb-enum-shares: 
|   account_used: guest
|   \\10.10.223.29\IPC$: 
|     Type: STYPE_IPC_HIDDEN
|     Comment: IPC Service (tbfc-smb server (Samba, Ubuntu))
|     Users: 1
|     Max Users: <unlimited>
|     Path: C:\tmp
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
|   \\10.10.223.29\tbfc-hr: 
|     Type: STYPE_DISKTREE
|     Comment: tbfc-hr
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\shares\tbfc-hr
|     Anonymous access: <none>
|     Current user access: <none>
|   \\10.10.223.29\tbfc-it: 
|     Type: STYPE_DISKTREE
|     Comment: tbfc-it
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\shares\tbfc-hr
|     Anonymous access: <none>
|     Current user access: <none>
|   \\10.10.223.29\tbfc-santa: 
|     Type: STYPE_DISKTREE
|     Comment: tbfc-santa
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\shares\tbfc-santa
|     Anonymous access: READ/WRITE
|_    Current user access: READ/WRITE
|_smb-enum-users: ERROR: Script execution failed (use -d to debug)
```
as you can see, `tbfc-santa` have Anonymous READ/WRITE permission, connect to the share using `smbclient`, no need to enter password since it allows anonymous login
```console
$ smbclient \\\\10.10.223.29\\tbfc-santa       
```