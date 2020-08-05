link to [read](https://hashcat.net/wiki/doku.php?id=example_hashes). and [this](https://hkh4cks.com/blog/2018/02/05/password-cracking-tools/#hashcat) 

# Task 1 
Can you complete the level 1 tasks by cracking the hashes?


find out what XXX stand for!! GL
1. ```hashcat -m XXX -a 0 -o task.txt "48bb6e862e54f2a795ffc4e541caed4d" /usr/share/wordlists/rockyou.txt --force```
2. sha1
3. sha256
4. kill me, it will take me 11 to crake this
5. https://md5decrypt.net/en/Md4/
6. 

# Task 2

1. ```hashcat -m 1400 -a 0 -o task.txt "F09EDCB1FCEFC6DFB23DC3505A882655FF77375ED8AA2D1C13F640FCCC2D0C85" /usr/share/wordlists/rockyou.txt --force```
2. ```hashcat -m 1000 -a 0 -o task.txt "1DFECA0C002AE40B8619ECF94819CC1B" /usr/share/wordlists/rockyou.txt --force```
3. dothis
```console
$ ehco "$6$aReallyHardSalt$6WKUTqzq.UQQmrm0p/T7MPpMbGNnzXPMAXi4bJMl9be.cfi3/qxIf.hsGpS41BqMhSrHVXgMpdjS6xeKZAs02." > unix.hash
$ hashcat -m 1800 -a 0 -o task.txt unix.lst wordlist/rockyou.txt --force --self-test-disable #took like 1 hr
```
4. ```hashcat -m 160 -a 0 -o task.txt "e5d8870e5bdd26602cab8dbe07a942c8669e56d6:tryhackme" /usr/share/wordlists/rockyou.txt --force```

```console
hashcat -m 3200 -a 0 -o crack.txt '$2a$06$7yoU3Ng8dHTXphAg913cyO6Bjs3K5lBnwq5FJyA6d01pMSrddr1ZG' /usr/share/wordlists/rockyou.txt --force
1800
$6$GQXVvW4EuM$ehD6jWiMsfNorxy5SINsgdlxmAEl3.yif0/c3NqzGLa0P.S7KRDYjycw5bnYkF5ZtB8wQy8KnskuWQS3Yr1wQ0
hashcat -m 1800 -a 0 -o crack.txt '$6$xQmTDVmT$hgSLG3ebs.8Tc/F4qqXNnvBBnG736EWpWKaprFVARjAsZ6JyoL4WaJdGv5.qddMWF4/MoJgN6Hekri8wyJ97k/' /usr/share/wordlists/rockyou.txt --force
```


$6$xQmTDVmT$hgSLG3ebs.8Tc/F4qqXNnvBBnG736EWpWKaprFVARjAsZ6JyoL4WaJdGv5.qddMWF4/MoJgN6Hekri8wyJ97k/