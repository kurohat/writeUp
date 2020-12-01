- linux server (from ping TTL)
- password length > 5, 
- running php. I found out by request for `index.php` -> return 200. index.html -> return 440

I created an account `kurohat:12345`. There is not much to see/do on the main page, only logout button. I then check dev tool -> cookie
```
auth:7b22636f6d70616e79223a22546865204265737420466573746976616c20436f6d70616e79222c2022757365726e616d65223a226b75726f686174227d
```
I assume that is a hex/base64 encoded string. let's use CyberChef to understand what the string represent! It turn out that it is a hex. This is the result when I convert it to a uft-8
```
{"company":"The Best Festival Company", "username":"kurohat"}
```
the plan is change username to santa (`{"company":"The Best Festival Company", "username":"santa"}`). Convert it into hex using CyberChef which will give us
```
7b22636f6d70616e79223a22546865204265737420466573746976616c20436f6d70616e79222c2022757365726e616d65223a2273616e7461227d
```
now remove your cookie value and replace it with Santa's cookie -> hit F5 (refresh). BOOM! we are in as Santa

Active each control to get flags

# etc
- SatNav = Satellite navigation
- never use poor cookie!!!