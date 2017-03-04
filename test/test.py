import httplib
import urllib
import json
particleServer = "api.particle.io";
particlePath = "/v1/devices/";
access_token = "6fe872f4848ab100432e84ba7f4f51341f9f0318";
conn = httplib.HTTPSConnection(particleServer, 443)
headers = {"Content-type": "application/x-www-form-urlencoded"}
params = urllib.urlencode({'access_token': access_token, 'arg': "off"})
payload = { }
conn.request("GET", particlePath + "?access_token=" + access_token)
response = conn.getresponse()
data = json.loads(response.read())
device_id = data[0]["id"]