import json


json_data=open('leveltest.json')

data = json.load(json_data)
json_data.close()

switches = data["switches"]
for switch in switches:
    print switch["position"]
    print switch["targets"]
    
testdict = {}
testdict[(1,2)] = "pass!"

print testdict[(1,2)]
print "dfd" in testdict
