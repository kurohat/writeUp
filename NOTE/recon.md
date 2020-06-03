# Passive Recon 
- One of the most important part
- More info about the target -> easier to attack it
- 
can be devided in 2 catagory 
## Physical or Social:
1. Localtion information:
   - Satellite image (Google map)
   - Drone recon
   - Building layout:
     - badge reader
     - blueprint of the building
     - security
     - fencing
     - break areas (smoke place)
2. Job info : use social media (linkin, fb, twitter) so when u see ppl on site u know who they are 
  - Employess
    - name, jobtitle, phone nr, etc
    - **who is IT guys**
  - Picture
    - badge photos, desk photo, destop ss, etc

## Web/host:
1. Target Validation:
 - WHOIS. nslookup, dnsrecon
2. Finding Subdomains  
 - Google Fu, dig, Nmap, Sublist3r, Bluto, crt.sh, etc
3. Fingerprinting/Footprinting
 - Nmap, Wappalyzer, WhatWeb, BuiltWith, Netcat
4. Data Breaches
 - HaveIBeenPwned, BreachParse, WeLeakInfo

# Tool
## Hunting employess's info
- huter.io: put the domain and then get list of the Employess. You can get
  - Email adess
  - department
  - Emil structure
  - where huter.io get information from (linlin, fb)
- theharvester: bad tho but come with kali. hunter.io is far better
- breach-parse.sh: https://github.com/hmaverickadams/breach-parse
## Hunting sub-domain
- crt.sh (a web)
- Sublist3r: serch for subdomain on search engine. Some time it give you dead link, you can use httprobe to check it
- tomnomnom httprobe: check if the domain is alive https://github.com/tomnomnom/httprobe
- OWASP Amass: **TO GO TOOL!!!**
## What did website build with
- BuildWith.com: A LOT of info
- Wappalyzer: a add-on on webbrowser, kinda active scanning site we need to move on to different page
  - get webserver info
  - programing laguague
  - which version
- whatweb: build-in tool on kali


how to use google https://ahrefs.com/blog/google-advanced-search-operators/
