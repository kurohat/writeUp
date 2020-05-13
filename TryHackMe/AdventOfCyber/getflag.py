# made by gu2rks@github
import requests
r = requests.get("http://10.10.169.100:3000")
r = r.json()
# {"value":"s","next":"f"}
flag = r["value"]
while True:
    r = requests.get("http://10.10.169.100:3000/"+str(r["next"]))
    r = r.json()
    if r["next"] == "end":
        break
    flag = flag + r["value"]

print("the flag: "+ flag)