# recon
```
Not shown: 992 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
443/tcp  open  https
445/tcp  open  microsoft-ds
3306/tcp open  mysql
3389/tcp open  ms-wbt-server
```
Remember the email that `murphyf` got?
```
Dear Frank Murphy,

Due to the recent firing of the Timekeep developer who had access to our
database, we have decided to issue a password reset. You can do so by
replacing your user account name and your new password in the following
URL:

http://timekeep.throwback.local/dev/passwordreset.php?user=murphyf&password=PASSWORD

Thank you,
IT Security.
```
so let visit the page and reset his password `/dev/passwordreset.php?user=murphyf&password=PASSWORD`. Boom! we also get a flag!!! now login with his credential. seem like we can upload a `.xlsm` file.... 
