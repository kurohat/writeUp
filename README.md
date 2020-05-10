# writeUp
Just my write up for CTF

# some juicy  shit
```console
$ find / -user root -perm -4000 -exec ls -ldb {} \; # scan the whole file system to find all files with the SUID bit set that is own by root
$ find / -perm -4000 -exec ls -ldb {} \; # same as about but own by any user
```

<html>
 <script src="https://tryhackme.com/badge/58769"></script>
</html>