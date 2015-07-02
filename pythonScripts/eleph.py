import requests
import json

groups = {'external':['0.0.0.0/0'],'internal':['10.0.0.0/8']}
flows = {'keys':'ipsource,ipdestination','value':'frames','filter':'sourcegroup=external&destinationgroup=internal'}
threshold = {'metric':'incoming','value':1000}
target = 'http://localhost:8008'
controller = 'http://localhost:8080'

#define address internal and external address groups
r = requests.put(target + '/group/json',data=json.dumps(groups))
#define flows
r = requests.put(target + '/flow/incoming/json',data=json.dumps(flows))
#define thresholds (1000 pkt per sec)
r = requests.put(target + '/threshold/incoming/json',data=json.dumps(threshold))
#polling to get the threshold events for the next 60 seconds, the max number of events is limited at 1000
eventurl = target + '/events/json?maxEvents=1000&timeout=60'
eventID = -1
while True:
  r = requests.get(eventurl + '&eventID=' + str(eventID))
  if r.status_code != 200: break
  events = r.json()
  if len(events) == 0: continue

  eventID = events[0]["eventID"]
  for e in events:
    if 'incoming' == e['metric']:
      r = requests.get(target + '/metric/' + e['agent'] + '/' + e['dataSource'] + '.' + e['metric'] + '/json')
      metric = r.json()
      if len(metric) > 0:
        ippair=metric[0]["topKeys"][0]["key"]
        ippair=ippair.split(',')
        #assume the elephant flow was going thru port 1, we now direct it to port 2.
        elephant = {'src-ip':ippair[0],'dst-ip':ippair[1],'action':'enqueue=2:1'}
        r = request.put(controller + '/wm/staticflowpusher/json',data=json.dumps(elephant))
