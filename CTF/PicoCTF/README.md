# Bases
```console
kuroHat@pico-2019-shell1:~$ echo 'bDNhcm5fdGgzX3IwcDM1' | base64 -d 
l3arn_th3_r0p35
```

# Fist grep
```console
cd /problems/first-grep_1_6788154ca7ee937f569985ff397203b6
kuroHat@pico-2019-shell1:/problems/first-grep_1_6788154ca7ee937f569985ff397203b6$ cat file | grep picoCTF
picoCTF{grep_is_good_to_find_things_205b65d7}
```
# dont-use-client-side
```js
if (checkpass.substring(0, split) == 'pico') {
      if (checkpass.substring(split*6, split*7) == 'a60f') {
        if (checkpass.substring(split, split*2) == 'CTF{') {
         if (checkpass.substring(split*4, split*5) == 'ts_p') {
          if (checkpass.substring(split*3, split*4) == 'lien') {
            if (checkpass.substring(split*5, split*6) == 'lz_4') {
              if (checkpass.substring(split*2, split*3) == 'no_c') {
                if (checkpass.substring(split*7, split*8) == '3}') {
                  alert("Password Verified")
                  }
                }
              }
      
            }
          }
        }
      }
    }
```
```picoCTF{no_clients_plz_4a60f3}```

