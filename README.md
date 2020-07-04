# writeUp
Just my write up for CTF

# some juicy  shit
```console
$ find / -user root -perm -4000 -exec ls -ldb {} \; 2> /dev/null# scan the whole file system to find all files with the SUID bit set that is own by root
$ find / -perm -4000 -exec ls -ldb {} \; 2> /dev/null # same as about but own by any user
$ find / -type f -a \( -perm -u+s -o -perm -g+s \) -exec ls -l {} \; 2> /dev/null # both SUID and SUIG
```



<html>
<script src="https://tryhackme.com/badge/58769"></script>
</html>

