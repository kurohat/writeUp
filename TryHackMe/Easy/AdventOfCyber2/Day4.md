1. `wfuzz -c -z file,big.txt http://shibes.xyz/api.php?breed=FUZZ`

on `/api` you will find `site-log.php`, download the wordlist given by THM to your kali
```console
$ wc -l wordlist                                                         
63 wordlist
```
63 lines, not bad, it will go really fast. now use wfuzz to fuzz different param
```console
$ wfuzz -c -z file,wordlist http://10.10.148.58/api/site-log.php?date=FUZZ

===================================================================
ID           Response   Lines    Word     Chars       Payload                                                
===================================================================
.
000000001:   200        0 L      0 W      0 Ch        "20201100"                                             
.
.
000000026:   200        0 L      1 W      13 Ch       "20201125"                                             
.
.
.
```
most of the response return 0 char. note that `20201125` returned 13 char!! so let check it out by visit `http://10.10.148.58/api/site-log.php?date=20201125`