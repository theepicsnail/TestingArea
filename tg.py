import urllib
feed = urllib.urlopen("http://www.reddit.com/r/teen_girls/new/.json?sort=new")
true,false,null = True,False,None
json = eval(feed.read())

import pprint
pprint.pprint(json)

for item in json["data"]["children"]:
    item["data"].get("url","")