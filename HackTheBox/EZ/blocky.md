# recon
```
port scanning...
21/tcp    open   ftp
22/tcp    open   ssh
80/tcp    open   http
8192/tcp  closed sophos
25565/tcp open   minecraft
Enumerating open ports...
Starting Nmap 7.80 ( https://nmap.org ) at 2020-09-25 16:02 EDT
Nmap scan report for blocky.htb (10.10.10.37)
Host is up (0.042s latency).

PORT      STATE  SERVICE   VERSION
21/tcp    open   ftp       ProFTPD 1.3.5a
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
|_sslv2-drown: 
| vulners: 
|   ProFTPD 1.3.5a: 
|     	CVE-2019-12815	7.5	https://vulners.com/cve/CVE-2019-12815
|     	CVE-2019-19272	5.0	https://vulners.com/cve/CVE-2019-19272
|     	CVE-2019-19271	5.0	https://vulners.com/cve/CVE-2019-19271
|     	CVE-2019-19270	5.0	https://vulners.com/cve/CVE-2019-19270
|     	CVE-2019-18217	5.0	https://vulners.com/cve/CVE-2019-18217
|     	CVE-2016-3125	5.0	https://vulners.com/cve/CVE-2016-3125
|_    	CVE-2017-7418	2.1	https://vulners.com/cve/CVE-2017-7418
22/tcp    open   ssh       OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
| vulners: 
|   cpe:/a:openbsd:openssh:7.2p2: 
|     	CVE-2008-3844	9.3	https://vulners.com/cve/CVE-2008-3844
|     	CVE-2016-8858	7.8	https://vulners.com/cve/CVE-2016-8858
|     	CVE-2016-6515	7.8	https://vulners.com/cve/CVE-2016-6515
|     	CVE-2016-10009	7.5	https://vulners.com/cve/CVE-2016-10009
|     	CVE-2016-10012	7.2	https://vulners.com/cve/CVE-2016-10012
|     	CVE-2015-8325	7.2	https://vulners.com/cve/CVE-2015-8325
|     	CVE-2016-10010	6.9	https://vulners.com/cve/CVE-2016-10010
|     	CVE-2019-6111	5.8	https://vulners.com/cve/CVE-2019-6111
|     	CVE-2018-15919	5.0	https://vulners.com/cve/CVE-2018-15919
|     	CVE-2018-15473	5.0	https://vulners.com/cve/CVE-2018-15473
|     	CVE-2017-15906	5.0	https://vulners.com/cve/CVE-2017-15906
|     	CVE-2016-10708	5.0	https://vulners.com/cve/CVE-2016-10708
|     	CVE-2019-16905	4.4	https://vulners.com/cve/CVE-2019-16905
|     	CVE-2016-6210	4.3	https://vulners.com/cve/CVE-2016-6210
|     	CVE-2007-2768	4.3	https://vulners.com/cve/CVE-2007-2768
|     	CVE-2019-6110	4.0	https://vulners.com/cve/CVE-2019-6110
|     	CVE-2019-6109	4.0	https://vulners.com/cve/CVE-2019-6109
|     	CVE-2014-9278	4.0	https://vulners.com/cve/CVE-2014-9278
|     	CVE-2018-20685	2.6	https://vulners.com/cve/CVE-2018-20685
|_    	CVE-2016-10011	2.1	https://vulners.com/cve/CVE-2016-10011
80/tcp    open   http      Apache httpd 2.4.18 ((Ubuntu))
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
| http-csrf: 
| Spidering limited to: maxdepth=3; maxpagecount=20; withinhost=blocky.htb
|   Found the following possible CSRF vulnerabilities: 
|     
|     Path: http://blocky.htb:80/
|     Form id: search-form-5f6e4d717f408
|_    Form action: http://10.10.10.37/
|_http-dombased-xss: Couldn't find any DOM based XSS.
| http-enum: 
|   /wiki/: Wiki
|   /wp-login.php: Possible admin folder
|   /phpmyadmin/: phpMyAdmin
|   /readme.html: Wordpress version: 2 
|   /: WordPress version: 4.8
|   /wp-includes/images/rss.png: Wordpress version 2.2 found.
|   /wp-includes/js/jquery/suggest.js: Wordpress version 2.5 found.
|   /wp-includes/images/blank.gif: Wordpress version 2.6 found.
|   /wp-includes/js/comment-reply.js: Wordpress version 2.7 found.
|   /wp-login.php: Wordpress login page.
|   /wp-admin/upgrade.php: Wordpress login page.
|_  /readme.html: Interesting, a readme.
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
| http-wordpress-users: 
| Username found: notch
|_Search stopped at ID #25. Increase the upper limit if necessary with 'http-wordpress-users.limit'
| vulners: 
|   Apache httpd 2.4.18: 
|     	HTTPD:F564BBA32AA088833DA032B7EB77CA29	7.5	https://vulners.com/httpd/HTTPD:F564BBA32AA088833DA032B7EB77CA29
|     	HTTPD:E74D6161229FA3D00A1783E6C3426C5D	7.5	https://vulners.com/httpd/HTTPD:E74D6161229FA3D00A1783E6C3426C5D
|     	HTTPD:C7D2DA1ACB016A5220CA8E74647BED26	7.5	https://vulners.com/httpd/HTTPD:C7D2DA1ACB016A5220CA8E74647BED26
|     	HTTPD:8F00FB1DD7567228376803FEDB0EC3B6	7.5	https://vulners.com/httpd/HTTPD:8F00FB1DD7567228376803FEDB0EC3B6
|     	HTTPD:7EEE138FD834328B3FC98E4B7FCAD266	7.5	https://vulners.com/httpd/HTTPD:7EEE138FD834328B3FC98E4B7FCAD266
|     	HTTPD:24E96D438275A8177C289509C796525C	7.5	https://vulners.com/httpd/HTTPD:24E96D438275A8177C289509C796525C
|     	HTTPD:237FAB5DE739A612077A245192137A48	7.5	https://vulners.com/httpd/HTTPD:237FAB5DE739A612077A245192137A48
|     	HTTPD:143F3A43D871E3AFFF956DB1049A6A2A	7.5	https://vulners.com/httpd/HTTPD:143F3A43D871E3AFFF956DB1049A6A2A
|     	HTTPD:0C6EE30D77005EBF2B39E351B1F3E2C4	7.5	https://vulners.com/httpd/HTTPD:0C6EE30D77005EBF2B39E351B1F3E2C4
|     	HTTPD:FC354B921BA807DFCACD7CD3C1D02FF9	7.2	https://vulners.com/httpd/HTTPD:FC354B921BA807DFCACD7CD3C1D02FF9
|     	HTTPD:9CDB89FBD1162B1E462FDF5BEA375759	6.8	https://vulners.com/httpd/HTTPD:9CDB89FBD1162B1E462FDF5BEA375759
|     	HTTPD:13B5FCC9676077F8FD08063C83511140	6.8	https://vulners.com/httpd/HTTPD:13B5FCC9676077F8FD08063C83511140
|     	HTTPD:B057D0A07B0AC97248CE6210E08ACAF7	6.4	https://vulners.com/httpd/HTTPD:B057D0A07B0AC97248CE6210E08ACAF7
|     	HTTPD:99188FFDCAF9C4932D00C218A2E58EC7	6.4	https://vulners.com/httpd/HTTPD:99188FFDCAF9C4932D00C218A2E58EC7
|     	HTTPD:531CF2A74E1A5A02A1D6AE2505AD586F	6.4	https://vulners.com/httpd/HTTPD:531CF2A74E1A5A02A1D6AE2505AD586F
|     	HTTPD:1696C4DDCBC58CE20005FCB002958C09	6.0	https://vulners.com/httpd/HTTPD:1696C4DDCBC58CE20005FCB002958C09
|     	HTTPD:BC81F521379C9038153151EAA84492CA	5.8	https://vulners.com/httpd/HTTPD:BC81F521379C9038153151EAA84492CA
|     	HTTPD:01BB9C701A4D4302EF59FA7EA89D9115	5.8	https://vulners.com/httpd/HTTPD:01BB9C701A4D4302EF59FA7EA89D9115
|     	HTTPD:F292DF1CEE1729E4240D1D62A10F5D32	5.1	https://vulners.com/httpd/HTTPD:F292DF1CEE1729E4240D1D62A10F5D32
|     	HTTPD:CE14FA5A5B1A2BE3A35EA809C9D8CFF7	5.1	https://vulners.com/httpd/HTTPD:CE14FA5A5B1A2BE3A35EA809C9D8CFF7
|     	HTTPD:79096CA36FAE041205EFAB66A6D4EF4B	5.1	https://vulners.com/httpd/HTTPD:79096CA36FAE041205EFAB66A6D4EF4B
|     	HTTPD:E91F31FD116386F2922B3EDA4BE3899B	5.0	https://vulners.com/httpd/HTTPD:E91F31FD116386F2922B3EDA4BE3899B
|     	HTTPD:E05CACB9D575871BA1E3088D02930266	5.0	https://vulners.com/httpd/HTTPD:E05CACB9D575871BA1E3088D02930266
|     	HTTPD:D7BF4648C333C0F770A30DEB0A23601C	5.0	https://vulners.com/httpd/HTTPD:D7BF4648C333C0F770A30DEB0A23601C
|     	HTTPD:D5609C15618DCADFDAD5AD396F2B83D7	5.0	https://vulners.com/httpd/HTTPD:D5609C15618DCADFDAD5AD396F2B83D7
|     	HTTPD:D5091608B1DC5DB5CABE405261B7658E	5.0	https://vulners.com/httpd/HTTPD:D5091608B1DC5DB5CABE405261B7658E
|     	HTTPD:D26626D944F16D90B877FB157E4A128F	5.0	https://vulners.com/httpd/HTTPD:D26626D944F16D90B877FB157E4A128F
|     	HTTPD:D0D55654F7429E8A4965CBBE30779CD6	5.0	https://vulners.com/httpd/HTTPD:D0D55654F7429E8A4965CBBE30779CD6
|     	HTTPD:C191D6FAD0C97D0A2E0A2A9F7BFE6B38	5.0	https://vulners.com/httpd/HTTPD:C191D6FAD0C97D0A2E0A2A9F7BFE6B38
|     	HTTPD:BD5F2FE0FF24D28F3450C11422A68AC8	5.0	https://vulners.com/httpd/HTTPD:BD5F2FE0FF24D28F3450C11422A68AC8
|     	HTTPD:B2B68FFCE0FB45D09BE91EE9ECBA07F6	5.0	https://vulners.com/httpd/HTTPD:B2B68FFCE0FB45D09BE91EE9ECBA07F6
|     	HTTPD:A5459AF02C9EC35CE80EA173C36C3F47	5.0	https://vulners.com/httpd/HTTPD:A5459AF02C9EC35CE80EA173C36C3F47
|     	HTTPD:99477914E1BE8FA85CEA0E956232C4C2	5.0	https://vulners.com/httpd/HTTPD:99477914E1BE8FA85CEA0E956232C4C2
|     	HTTPD:824D39D8A30F1234C966CBDA41E1C446	5.0	https://vulners.com/httpd/HTTPD:824D39D8A30F1234C966CBDA41E1C446
|     	HTTPD:73656ED41609146303D488C86337BC2D	5.0	https://vulners.com/httpd/HTTPD:73656ED41609146303D488C86337BC2D
|     	HTTPD:6CAC4F8B58BB2BE168795A6BA0CA26A1	5.0	https://vulners.com/httpd/HTTPD:6CAC4F8B58BB2BE168795A6BA0CA26A1
|     	HTTPD:5D6E315A1B98558C0DF8CBE51264FBA5	5.0	https://vulners.com/httpd/HTTPD:5D6E315A1B98558C0DF8CBE51264FBA5
|     	HTTPD:4EC9662496A151DDE6D030D9127572E7	5.0	https://vulners.com/httpd/HTTPD:4EC9662496A151DDE6D030D9127572E7
|     	HTTPD:42FA2547862AB3B3F5E7F776E2D90614	5.0	https://vulners.com/httpd/HTTPD:42FA2547862AB3B3F5E7F776E2D90614
|     	HTTPD:3647863A8E4AE972669D5EE60974E777	5.0	https://vulners.com/httpd/HTTPD:3647863A8E4AE972669D5EE60974E777
|     	HTTPD:18105DABC6D0ADE97D12B90F63EAE025	5.0	https://vulners.com/httpd/HTTPD:18105DABC6D0ADE97D12B90F63EAE025
|     	HTTPD:174A0D44882BCA7E2F229BC91D6D5A09	5.0	https://vulners.com/httpd/HTTPD:174A0D44882BCA7E2F229BC91D6D5A09
|     	HTTPD:04C30566E99EFB3C0D60F08EE2524591	5.0	https://vulners.com/httpd/HTTPD:04C30566E99EFB3C0D60F08EE2524591
|     	HTTPD:FF57290724543D4766EDDC4666992FE8	4.3	https://vulners.com/httpd/HTTPD:FF57290724543D4766EDDC4666992FE8
|     	HTTPD:F4FBBB7467F08F96828B98E753E5FE7D	4.3	https://vulners.com/httpd/HTTPD:F4FBBB7467F08F96828B98E753E5FE7D
|     	HTTPD:D94ACD37B5627A621B2D592BD44873F2	4.3	https://vulners.com/httpd/HTTPD:D94ACD37B5627A621B2D592BD44873F2
|     	HTTPD:D26FFC4C8AA598C5F130A0223836644E	4.3	https://vulners.com/httpd/HTTPD:D26FFC4C8AA598C5F130A0223836644E
|     	HTTPD:A5773ECB3CB67826707B252F21BB80BB	4.3	https://vulners.com/httpd/HTTPD:A5773ECB3CB67826707B252F21BB80BB
|     	HTTPD:86C509FC37A85DC3C01E3CE10402C6DC	4.3	https://vulners.com/httpd/HTTPD:86C509FC37A85DC3C01E3CE10402C6DC
|     	HTTPD:714A18409AEB3B8362DC4FA2B923CA7A	4.3	https://vulners.com/httpd/HTTPD:714A18409AEB3B8362DC4FA2B923CA7A
|     	HTTPD:43E63F90DCA6F418ACF2327C4F88C3D8	4.3	https://vulners.com/httpd/HTTPD:43E63F90DCA6F418ACF2327C4F88C3D8
|     	HTTPD:2E568217BC35E0AA91DF49E7CE65CA67	3.5	https://vulners.com/httpd/HTTPD:2E568217BC35E0AA91DF49E7CE65CA67
|     	HTTPD:B6CF5630624F83951A477D36DC8FD634	0.0	https://vulners.com/httpd/HTTPD:B6CF5630624F83951A477D36DC8FD634
|     	HTTPD:94C27BCF50CA81A222019B9F06735AA1	0.0	https://vulners.com/httpd/HTTPD:94C27BCF50CA81A222019B9F06735AA1
|     	HTTPD:914D0BB6DF64CDA58BDF1461563DCBC2	0.0	https://vulners.com/httpd/HTTPD:914D0BB6DF64CDA58BDF1461563DCBC2
|     	HTTPD:7ED2E94FC8175AF57B0B84C966E78986	0.0	https://vulners.com/httpd/HTTPD:7ED2E94FC8175AF57B0B84C966E78986
|     	HTTPD:55F8C86BB4FE80544B301C6F772E1F21	0.0	https://vulners.com/httpd/HTTPD:55F8C86BB4FE80544B301C6F772E1F21
|     	HTTPD:53F7D531D201D0209EE31F3FA8829F5B	0.0	https://vulners.com/httpd/HTTPD:53F7D531D201D0209EE31F3FA8829F5B
|_    	HTTPD:21A860C56B7B6A55960FB17E72B7E4B4	0.0	https://vulners.com/httpd/HTTPD:21A860C56B7B6A55960FB17E72B7E4B4
8192/tcp  closed sophos
25565/tcp open   minecraft Minecraft 1.11.2 (Protocol: 127, Message: A Minecraft Server, Users: 0/20)
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
```
* Apache/2.4.18 (Ubuntu)
* WordPress version 4.8: user=notch

gobuster
```
/.htaccess (Status: 403)
/.htpasswd (Status: 403)
/javascript (Status: 301)
/phpmyadmin (Status: 301)
/plugins (Status: 301)
/server-status (Status: 403)
/wiki (Status: 301)
/wp-admin (Status: 301)
/wp-content (Status: 301)
/wp-includes (Status: 301)
```


```console
kali@kali:~/HTB/blocky$ jar -xf BlockyCore.jar 
Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
kali@kali:~/HTB/blocky$ ls
BlockyCore.jar  com  META-INF
kali@kali:~/HTB/blocky$ cd com/myfirstplugin/
kali@kali:~/HTB/blocky/com/myfirstplugin$ ls
BlockyCore.class
```

```console
$ strings BlockyCore.class
.
.
Code
	localhost	
root	
8YsqfCTnvxAUeduzjNSXe22	
```
now let run all script
```
```