# system enum
```cmd
>systeminfo :: system info
>systeminfo | findstr /B /C:"OS Name" /C:"OS version" /C:"System type"
>hostname
>wmic qfe :: using for check what is available, what been patched. windows management instrumentation, C = commandline.
>wmic qfe get Caption,Description,HotFixID,InstalledOn
>logicaldisk get caption,description,providername
```

# user enum
```cmd
>whoami /priv :: check priv
>whoami /group :: check what group we are involed
>net user :: get all users
>net user <usernam> :: get info about the specific user
>net localgroup
>net localgroup administrators :: find all user in admin group
```

# network enum
```cmd
>ipconfig
>ipconfig /all :: get domain server, dns, default gateway
>arp -a :: not much to do on CTF
>route print :: routing table
>netstat -ano :: compare with nmap, maybe you find service that only works inside network
```

# Password Hunting
check the bookmarked
1. https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md#eop---looting-for-passwords
2. https://sushant747.gitbooks.io/total-oscp-guide/privilege_escalation_windows.html 
```cmd
>findstr /si password *.txt *.ini *.config:: only search on current directory
```
# A/V & firewall enum
```cmd
> sc query windefend :: using sc (service controll) to find out more aboute a specific service.
> sc queryex type= service :: get all servic that is running.
> netsh advfirewall firewall dump :: get info about fw
> netsh firewall show state
```