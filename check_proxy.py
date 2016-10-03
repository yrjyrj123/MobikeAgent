from gevent import monkey
from gevent.pool import Pool
import requests

monkey.patch_all()

f_in=open("proxies.txt")
f_out=open("good_proxies.txt","w")


def check(proxy):
    try:
        r=requests.get("http://api.mobike.com/", proxies={"http": "http://"+proxy},timeout=5)
        if r.text=="working...\n":
            return proxy
        else:
            return None
    except:
        return None

tasks=[]
for line in f_in:
    line = line[:-1]
    tasks.append(line)
f_in.close()

tasks=list(set(tasks))

pool = Pool(128)
map_results = pool.map(check, tasks)

count=0
for item in map_results:
    if item!=None:
        f_out.write(item+"\n")
        count+=1
f_out.close()

print "find %d good proxies !" % count