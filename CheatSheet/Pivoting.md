# msfconsole
* meterpreter session is requried
## Auto-Routing
```
background
use post/multi/manage/autoroute
set SESSION X
set SUBNET x.x.x.0
exploit
```
## Setting up a Proxy
1. use `auxiliary/server/socks4a`
2. (optional) Change you port, you can either keep the default 1080 port or change it to an open port of your choice.
3. `run`

# Proxy Chain
1. sudo nano /etc/proxychains.conf > socks4 socks4 	127.0.0.1 <port>
   1. the same port that you specify when `auxiliary/server/socks4a`
2. now run `proxychains <command>`
