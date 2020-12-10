# pcap1.pcap
To search for icmp packets, type `icmp` in search bar. `http.request.method == GET` can be use to search for **HTTP GET request**.


for the 3rd task I ran `http.request.method == GET and ip.src == 10.10.67.199` filtering only HTTP get request from 10.10.67.199. where I find `/posts` which I assume that it directory for articles

# pcap2.pcap
filter only `ftp` traffic and find `elfmcskidy` password (wrong password)

# pcap3.pcap
I notice that there is a http traffic after analyzing the pcap. We learned how to import files from pcap by File -> explort file -> HTTP since we want to export data from http traffic. Here you will find `christmas.zip`, export it and extract the zip. You will find `elf_mcskidy_wishlist.txt` check the content of the file :D
