# recon
```console
$ sudo ./pymap.py -t 10.200.11.219 -A
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH for_Windows_7.7 (protocol 2.0)
| ssh-hostkey: 
|   2048 85:b8:1f:80:46:3d:91:0f:8c:f2:f2:3f:5c:87:67:72 (RSA)
|   256 5c:0d:46:e9:42:d4:4d:a0:36:d6:19:e5:f3:ce:49:06 (ECDSA)
|_  256 e2:2a:cb:39:85:0f:73:06:a9:23:9d:bf:be:f7:50:0c (ED25519)


PORT     STATE SERVICE       VERSION
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: THROWBACK
|   NetBIOS_Domain_Name: THROWBACK
|   NetBIOS_Computer_Name: THROWBACK-PROD
|   DNS_Domain_Name: THROWBACK.local
|   DNS_Computer_Name: THROWBACK-PROD.THROWBACK.local
|   DNS_Tree_Name: THROWBACK.local
|   Product_Version: 10.0.17763
|_  System_Time: 2020-11-02T20:40:44+00:00
| ssl-cert: Subject: commonName=THROWBACK-PROD.THROWBACK.local
| Not valid before: 2020-07-27T22:26:10
|_Not valid after:  2021-01-26T22:26:10
|_ssl-date: 2020-11-02T20:40:44+00:00; 0s from scanner time.


PORT   STATE SERVICE VERSION
80/tcp open  http    Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Throwback Hacks


PORT     STATE SERVICE VERSION
5985/tcp open  http    Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found


PORT    STATE SERVICE VERSION
135/tcp open  msrpc   Microsoft Windows RPC


PORT     STATE SERVICE VERSION
5357/tcp open  http    Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Service Unavailable


PORT    STATE SERVICE     VERSION
139/tcp open  netbios-ssn Microsoft Windows netbios-ssn

Host script results:
|_smb2-security-mode: SMB: Couldn't find a NetBIOS name that works for the server. Sorry!
|_smb2-time: ERROR: Script execution failed (use -d to debug)


PORT    STATE SERVICE       VERSION
445/tcp open  microsoft-ds?

Host script results:
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2020-11-02T20:40:47
|_  start_date: N/A


PORT      STATE SERVICE VERSION
49667/tcp open  msrpc   Microsoft Windows RPC


PORT      STATE SERVICE VERSION
49673/tcp open  msrpc   Microsoft Windows RPC


PORT      STATE SERVICE VERSION
49669/tcp open  msrpc   Microsoft Windows RPC
```
