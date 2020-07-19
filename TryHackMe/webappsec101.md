# enumeratetion
- apache server 2.4.7
  - when request for not found page (info disclosure)
![respnse header](pic/Screenshot%202020-07-18%20at%2019.57.57.png)

- when looking for uploaded pics `/pictures/view.php?picid=10` you can chang *picid=X* to access different picture.

way to test web app: breaking down the testing into different stages/catagories(including but not limited to):
- Authorization
- Authentication
- Injection
- Client Side Controls
- Application Logic

# Authorization
Authentication can be tested in the following ways:
- **Brute Forcing/Weak Credentials**: In most cases, users usually pick common passwords that are easy to guess. This could be anything from the username to the names of animals. Attackers can use weak passwords to their advantage by using a list to guess possible users passwords.
- **Session Management**: Sessions are the mechanism by which the server retains state about the application. This is necessary in applications that need to remember users for transactions. In some cases, sessions(which are stored in cookies) store information about users such as their privilege level. This state can be manipulated and sent back to the server
  
1. admin page `/admin/index.php?page=login` username = admin, check hint for password


`/admin/index.php?page=create` return message
```
Warning: require_once(create.php): failed to open stream: No such file or directory in /app/admin/index.php on line 4

Fatal error: require_once(): Failed opening required 'create.php' (include_path='.:/usr/share/php:/usr/share/pear') in /app/admin/index.php on line 4
```
2. check devtool -> storage -> cookie
3. Looking for other users.
I found this in `/users/`
![view](pic/Screenshot%202020-07-18%20at%2020.20.56.png)
in homepage you will see link for* Check out a sample user!* which redirected you to`/users/sample.php?userid=1`. Moreover, I assume that `view.php` works same where as view.php in **/pictures/**. so let looking userid and such


it works, now start from 2 since userid=1 is the sample user.
1. same as username

# Injection
1. Perform command injection on the check password field
visit `/passcheck.php` and input something (in my case: I input `yo`)
```
The command "grep ^yo$ /etc/dictionaries-common/words" was used to check if the password was in the dictionary.
yo is a Bad Password 
```
so let try to escape from it. ```yo; ls -la #```. `#` = comment. I blow up the server everytime I did it lol. command injection to DOS

yo || ping -n 10 10.8.14.151
