# recon
Like always, start with nmap. I use my own tool to automate nmap scan, check it out [pymap](https://github.com/gu2rks/pymap)
```console
$ python3 pymap.py -t $IP 
```
There are 2 open ports:
- 22/tcp open  ssh
- 80/tcp open  http

If web is up, I alway start with running `gobuster` to brute forcing web directory. While `gobuster` is running, I explore the web or walking the "happy path" by using the web in the way it was meant to be used by a normal user.

## rabbit hole + user credential
I start by checking the source code and I found this:
`<!--(Check console for extra surprise!)-->`. ofc I open dev-tool and check what is in the console. I found the array with then pokemon name...
```js
[
  "Bulbasaur",
  "Charmander",
  "Squirtle",
  "Snorlax",
  "Zapdos",
  "Mew",
  "Charizard",
  "Grimer",
  "Metapod",
  "Magikarp"
]
```
more over I found this js script.
```js
<script type="text/javascript">
    const randomPokemon = [
        'Bulbasaur', 'Charmander', 'Squirtle',
        'Snorlax',
        'Zapdos',
        'Mew',
        'Charizard',
        'Grimer',
        'Metapod',
        'Magikarp'
    ];
    const original = randomPokemon.sort((pokemonName) => {
        const [aLast] = pokemonName.split(', ');
    });

    console.log(original);
</script>
```
I try to understand it but it seem like it lead me nowhere... So I go back to the source and check it again in case I missed something.


Yep I missed not just something. There is username:password hidden somewhere close to `<!--(Check console for extra surprise!)-->`. But I was so focus on check console log message.......

# foot hold
now that we have user credential. Lets ssh to the victim server and enumerate the server a bit.

```console
pokemon@root:~$ sudo -l
[sudo] password for pokemon: 
Sorry, user pokemon may not run sudo on root.
pokemon@root:~$ id
uid=1000(pokemon) gid=1000(pokemon) groups=1000(pokemon),4(adm),24(cdrom),30(dip),46(plugdev),113(lpadmin),128(sambashare)
 4096 Jun 24 13:48 ..
drwx------  6 root    root    4096 Jun 24 14:14 ash
drwxr-xr-x 18 pokemon pokemon 4096 Aug 10 09:53 pokemon
-rwx------  1 ash     root       8 Jun 22 23:21 roots-pokemon.txt
```
so as you can see, the current user is not allow to run sudo. Moreover, there are 2 users in this server. the current user and `ash`. I assume that `ash` is a root user since he is main guy in pokemon :P. 

now let enumerate more. and I end up find a `.zip` file in `Desktop`. Unzip and u will find our fist flag!!
```console
pokemon@root:~$ cd Desktop/
pokemon@root:~/Desktop$ ls
P0kEmOn.zip
pokemon@root:~/Desktop$ unzip P0kEmOn.zip 
Archive:  P0kEmOn.zip
   creating: P0kEmOn/
  inflating: P0kEmOn/grass-type.txt  
pokemon@root:~/Desktop$ ls
P0kEmOn  P0kEmOn.zip
pokemon@root:~/Desktop$ cd P0kEmOn/
pokemon@root:~/Desktop/P0kEmOn$ ls
grass-type.txt
pokemon@root:~/Desktop/P0kEmOn$ cat grass-type.txt 
50 __ __ __ __ __ __
```
the flag is encoded, decode it and submit the flag!


At this point we know the format of the flag. We can craft a simple regex to and using `find` to look for more flags. The name of the 1st flag call `grass-type.txt`. So I assume that the flag should looks something likt `pokemontype-type.txt`. Where *pokemontype* can be grass, frie, water, electric, etc. The regex will be `*-type.txt`


now let run find command
```console
pokemon@root:~$ find / -user pokemon -name *type.txt 2> /dev/null 
/var/www/html/water-type.txt
/home/pokemon/Desktop/P0kEmOn/grass-type.txt
```
Bingo ! grab the flag! note that the flag is encoded (agian). Decoded and submit the flag
**hint**: <details>ROT</details>


The current user home directory is huge. There are many sub directory and such. let enumerate all of them at ones with `pokemon@root:~$ ls -la *`. you will find a really interesting directory. Dig deeper and you will find a file call `Could__________for?.cplusplus`

```console
pokemon@root:~/__________$ cat Could__________for?.cplusplus
# include <iostream>

int main() {
	std::cout << "ash : <something_here>"
	return 0;
}
```

We found a `ash` credential which I gussed that he is a root user. now let log into `ash`

# root
there is many way to log into as `ash`. You can `ssh` as `ash` or use `su`. In this case, I will use `su`:
```console
pokemon@root:~$ su ash
Password: 
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

bash: /home/ash/.bashrc: Permission denied
ash@root:/home/pokemon$
```
yea let grab the `roots-pokemon.txt`.
```console
ash@root: cat /home/roots-pokemon.txt
```
we still have need to find the 3rd flag. Since we already have the regex for finding the flag, let re-use it again!!
```console
ash@root:/$ find / -user ash -name *type.txt 2> /dev/null 
ash@root:/$ find / -user root -name *type.txt 2> /dev/null 
/____/________/fire-type.txt
```
Grab the flag and decode it
**hint**: <details>BASE__</details>, GL and happy hacking