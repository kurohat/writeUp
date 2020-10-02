# general
```console
kali@kali:~$ sudo apt-get install gobuster
kali@kali:~$ sudo apt-get install python3-pip
kali@kali:~$ sudo apt-get install openvpn
kali@kali:~$ sudo apt-get install seclists
kali@kali:/opt$ sudo wget https://raw.githubusercontent.com/Anon-Exploiter/SUID3NUM/master/suid3num.py
kali@kali:~$ sudo apt-get install golang
```
# terminator
- [unlimited-scroll](https://askubuntu.com/questions/618464/unlimited-scroll-in-terminator) 
```console
$ sudo apt-get install terminator
$ nano terminator/config # Open the terminator config file
```
under the `[profiles]` entry add those lines
```
  [[default]]
    scrollback_infinite = True
```
Now save and exit then restart your terminator. enjoy

# pymap
```console
kali@kali:/opt$ sudo wget https://raw.githubusercontent.com/gu2rks/pymap/master/pymap.py
kali@kali:/opt$ sudo chmod +x pymap.py 
```
# impacket
```console
$ sudo git clone https://github.com/SecureAuthCorp/impacket.git
$ cd impacket && pip3 install -r requirements.txt
$ sudo python3 setup.py install
```
# privilege-escalation-awesome-scripts-suite
```console
$ sudo git clone https://github.com/SecureAuthCorp/impacket.git
$ sudo mkdir privesc
kali@kali:/opt$ sudo cp privilege-escalation-awesome-scripts-suite/winPEAS/winPEASexe/winPEAS/obj/x64/Release/winPEAS.exe privesc/winPEAS-x64.exe
kali@kali:/opt$ sudo cp privilege-escalation-awesome-scripts-suite/winPEAS/winPEASexe/winPEAS/obj/x86/Release/winPEAS.exe privesc/winPEAS-x86.exe
kali@kali:/opt$ sudo cp privilege-escalation-awesome-scripts-suite/winPEAS/winPEASbat/winPEAS.bat privesc/
kali@kali:/opt$ sudo cp privilege-escalation-awesome-scripts-suite/linPEAS/linpeas.sh privesc/
```

# Evilnigx
```console

```