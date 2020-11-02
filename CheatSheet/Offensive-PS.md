# Table of Contents
- [Table of Contents](#table-of-contents)
- [intro](#intro)
  - [importing modules](#importing-modules)
  - [Get-ADDomain](#get-addomain)
  - [Get-ADForest](#get-adforest)
  - [Get-ADTrust](#get-adtrust)
- [PowerView](#powerview)
  - [Get-NetDomain](#get-netdomain)
  - [Get-NetDomainController](#get-netdomaincontroller)
  - [Get-NetForest](#get-netforest)
  - [Get-NetDomainTrust](#get-netdomaintrust)

# intro
## importing modules
start by importing `ActiveDirectory` Module
```
Import-Module <Module>
Import-Module ActiveDirectory
. .\Module.ps1
```
## Get-ADDomain
- list all of the Domain Controllers for a given environment, tell you the NetBIOS Domain name, the FQDN (Fully Qualified Domain name)
```
Get-ADDomain
Get-ADDomain | Select-Object NetBIOSName, DNSRoot, InfrastructureMaster # filtering
```
## Get-ADForest
pulls all the Domains within a Forest and lists them out to the user. This may be useful if a bidirectional trust is setup, it may allow you to gain a foothold in another domain on the LAN. Just like Get-ADDomain
```
Get-ADForest
Get-ADForest | Select-Object Domains
```
## Get-ADTrust 
Get-ADTrust provides a ton of information about the Trusts within the AD Domain. It can tell you if it’s a one way or bidirectional trust, who the source is, who the target is, and much more. 
```
Get-ADTrust -Filter * | Select-Object Direction,Source,Target
```
# PowerView
- https://github.com/PowerShellMafia/PowerSploit
- kali: `/usr/share/windows-resources/powersploit`
```console
$ Import-Module .\PowerView.ps1
```
## Get-NetDomain
Basic info such as the Forest, Domain Controllers, and Domain Name are enumerated.
```console
$ Get-NetDomain
```
## Get-NetDomainController
list all of the Domain Controllers within the network. This is incredibly useful for initial reconnaissance, especially if you do not have a Windows device that’s joined to the domain.
```console
$ Get-NetDomainController    
```
## Get-NetForest    
It provides all the associated Domains, the root domain, as well as the Domain Controllers for the root domain.
```console
$ Get-NetForest    
```
## Get-NetDomainTrust
Get-NetDomainTrust is similar to Get-ADTrust with our SelectObject filter applied to it. It’s short, sweet and to the point!
```console
$ Get-NetDomainTrust 
```