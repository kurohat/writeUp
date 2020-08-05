# Sudo Security Bypass CVE-2019-14287
- Sudo versions < **1.8.28**. To check sudo version run ```sudo -V```
- execute it as another user like this:``` sudo -u#<id> <command>```. This means that you would be pretending to be another user when you executed the chosen command, which can give you higher permissions than you might otherwise have had.

![sudo](pic/sudo-demo.png)

Like many commands on Unix systems, sudo can be configured by editing a configuration file on your system. In this case that file is called `/etc/sudoers`. Editing this file directly is not recommended due to its importance to the OS installation, however, you can safely edit it with the command `sudo visudo`, which checks when you're saving to ensure that there are no misconfigurations.

The vulnerability we're interested in for this task occurs **in a very particular scenario**. Say you have a user who you want to grant extra permissions to. You want to let this user execute a program as if they were any other user, but you don't want to let them execute it as root. You might add this line to the sudoers file:


`<user> ALL=(ALL:!root) NOPASSWD: ALL`


This would let your user execute any command as another user, but would (theoretically) prevent them from executing the command as the superuser/admin/root. In other words, you can pretend to be any user, except from the admin.


With the above configuration, using ```sudo -u#0 <command>``` (the **UID of root is always 0**) would not work, as we're not allowed to execute commands as root. If we try to execute commands as user 0 we will be given an error


Joe Vennix found that if you specify a **UID of -1** (or its unsigned equivalent: **4294967295**), Sudo would incorrectly read this as being 0 (i.e. root). This means that **by specifying a UID of -1 or 4294967295, you can execute a command as root**, despite being explicitly prevented from doing so. It is worth noting that this will **only work if you've been granted non-root sudo permissions for the command, as in the configuration above.**

Practically, the application of this is as follows: ```sudo -u#-1 <command>```

# action
```console
tryhackme@sudo-privesc:~$ sudo -l # check what cmd are we allow to execute as root
Matching Defaults entries for tryhackme on sudo-privesc:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User tryhackme may run the following commands on sudo-privesc:
    (ALL, !root) NOPASSWD: /bin/bash
tryhackme@sudo-privesc:~$ sudo -u#-1 /bin/bash 
root@sudo-privesc:~# cat /root/root.txt 
```