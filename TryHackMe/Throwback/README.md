![topo](pic/topo.png)
- THROWBACK-PROD: 10.200.11.219
- THROWBACK-FW01: 10.200.11.138
- THROWBACK-MAIL: 10.200.11.232
# Important notes
- http://timekeep.throwback.local/dev/passwordreset.php?user=murphyf&password=PASSWORD **to reset password!!** got it from MAIL

# ipsweep
```console
kali@kali:/opt$ sudo ./pymap.py -t 10.200.11.0/24 -pS
                                                    
@@@@@@@   @@@ @@@  @@@@@@@@@@    @@@@@@   @@@@@@@  
@@@@@@@@  @@@ @@@  @@@@@@@@@@@  @@@@@@@@  @@@@@@@@  
@@!  @@@  @@! !@@  @@! @@! @@!  @@!  @@@  @@!  @@@  
!@!  @!@  !@! @!!  !@! !@! !@!  !@!  @!@  !@!  @!@  
@!@@!@!    !@!@!   @!! !!@ @!@  @!@!@!@!  @!@@!@!   
!!@!!!      @!!!   !@!   ! !@!  !!!@!!!!  !!@!!!    
!!:         !!:    !!:     !!:  !!:  !!!  !!:       
:!:         :!:    :!:     :!:  :!:  !:!  :!:       
 ::          ::    :::     ::   ::   :::   ::       
 :           :      :      :     :   : :   :        
Author: kuroHat
Github: https://github.com/gu2rks

sweeping on network: 10.200.11.0/24 
Looking for alive hosts...
Nmap scan report for 10.200.11.138
Nmap scan report for 10.200.11.219
Nmap scan report for 10.200.11.230
Nmap scan report for 10.200.11.232
```

4 hosts
- FW01 = 10.200.11.138
- PROD = 10.200.11.219
- MAIL = 10.200.11.232
- **HOW IS 10.200.11.230? DC01?** : I try to ping this address and it return TTL 64, so I guess it is me lol


# Road map

## [Introductory to AD and PowerShell Section]
- [x] [Task 5] AD Basics (Reading)
- [x] [Task 6] Let’s Get Offensive (Reading)
- [x] [Task 7] Entering the Breach
- [x] [Task 8] Exploring the Caverns

## [Path 1 (Firewall Exploitation)]
- [x] [Task 9] Web Shells and You!
- [x] [Task 10] First Contact
- [x] [Task 14] We Will, We Will, Rockyou
- [ ] [Leads to Going Through the Transporter Path]

## [Path 2 (Phishing)]
- [x] [Task 11] Wait, just you mean just one this time?
- [x] [Task 12] Gone Phishing
- [ ] [Task 21] You Dawg, I heard you like proxies
- [ ] [Leads to Main Path]

## [Path 3 (LLMNR Poisoning & C2 Overview)]
- [x] [Task 13] Just a Drop Will Do
- [x] [Task 14] We Will, We Will, Rockyou
- [x] [Task 15] Building Your Own Dark... er DeathStar
- [x] [Task 16] Deploy the Grunts!
- [x] [Task 17] Get-Help Invoke-WorldDomination
- [x] [Task 18] SEATBELT CHECK!
- [ ] [Task 19] Dump It Like It's Hot
- [ ] [Task 20] Not the soft and fluffy kind
- [ ] [Leads to Going Through the Transporter Path]

## [Going Through the Transporter Path (Proxies and Pivoting)]
- [ ] [Task 21] You Dawg, I heard you like proxies.
- [ ] [Task 22] Good Intentions, Courtesy of Microsoft
- [ ] [Leads to Main Path]

## [Main Path (Lateral Movement)]
- [ ] [Task 23] Wallace and Gromit
- [ ] [Task 24] With three heads you'd think they'd at least agree once
- [ ] [Task 25] You're Five Minutes Late...
- [ ] [Task 26] Word to your Mother
- [ ] [Task 27] Meterpreter session 1 closed. Reason: World-Domination 
- [ ] [Task 28] We gotta drop the load!
- [ ] [Task 29] So we're doing this again...
- [ ] [Task 30] SYNCHRONIZE
- [ ] [Task 31] This Forest has trust issues
- [ ] [Task 32] r/badcode would like a word
- [ ] [Task 33] Identity Theft is not a Joke Jim
- [ ] [Task 34] So anyways, I just started hiring..
- [ ] [Task 35] Lost and Found
- [ ] [Task 36] You've Got Mail!
- [ ] [Task 37] Kerberoasting II Electric Boogaloo
- [ ] [Task 38] Endgame