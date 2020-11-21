# Colabcat
[youtube](https://www.youtube.com/watch?v=pYOncitu7W8) guide how to use this tool. here is what you need to do
1. Click on `Runtime`, `Change runtime type`, and set `Hardware accelerator` to GPU.
2. Go to your Google Drive and create a directory called `dothashcat`, with a `hashes` subdirectory where you can store hashes.
3. Upload [rule](https://github.com/NotSoSecure/password_cracking_rules/blob/master/OneRuleToRuleThemAll.rule) and your hashes in `hashes` subdirectory.
4. Come back to Google Colab, click on `Runtime` and then `Run all`.
5. When it asks for a Google Drive *token*, go to the link it provides and authenticate with your Google Account to get the token
6. add code cell (`+code`)
7. run `!bash` and press play button
8. `cd drive/'My Drive'/dothashcat/hashes` and run hashcat

# Hashcat
```console
$ hashcat -m <op> -a 0 -o crack.txt 'hash' /usr/share/wordlists/rockyou.txt --force
$ hashcat -m 13100 -a 0 hash.txt Pass.txt --force # kerberos 
```
# john
```console
root@kali:~# john -wordlist=/usr/share/wordlists/rockyou.txt <hash>
```
