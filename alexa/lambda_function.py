import httplib
import urllib
import json
particleServer = "api.particle.io";
particlePath = "/v1/devices/";

def lambda_handler(event, context):
    access_token = event['payload']['accessToken']

    if (event['header']['namespace'] == 'Alexa.ConnectedHome.Discovery'):
        return handleDiscovery(context, event, access_token)

    elif event['header']['namespace'] == 'Alexa.ConnectedHome.Control':
        return handleControl(context, event, access_token)

def handleDiscovery(context, event, access_token):
    payload = ''
    header =''
    conn = httplib.HTTPSConnection(particleServer, 443)
    conn.request("GET", particlePath + "?access_token=" + access_token)
    response = conn.getresponse()
    data = json.loads(response.read())
    status = response.status
    print(data)
    print(response.status)
    if (event['header']['name'] == 'DiscoverAppliancesRequest') and (status == 200):
        device_id = data[0]['id']
        payload = {
            "discoveredAppliances":[
                {
                    "applianceId":device_id,
                    "manufacturerName":"Rich",
                    "modelName":"model 01",
                    "version":"v0.1",
                    "friendlyName":"television",
                    "friendlyDescription":"Particle Device connected to IR LED.",
                    "isReachable":True,
                    "actions":[
                        "turnOn",
                        "turnOff"
                    ],
                    "additionalApplianceDetails":{
                        "deviceID":"3d0042001047343339383037"
                    }
                }
            ]
        }
        header = {
            "namespace": "Alexa.ConnectedHome.Discovery",
            "name": "DiscoverAppliancesResponse",
            "payloadVersion": "2"
        }
    return { 'header': header, 'payload': payload}

def handleControl(context, event, access_token):
    payload = ''
    device_id = event['payload']['appliance']['applianceId']
    message_id = event['header']['messageId']
    conn = httplib.HTTPSConnection(particleServer, 443)
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    if event['header']['name'] == 'TurnOnRequest':
        params = urllib.urlencode({'access_token': access_token, 'arg': "on"})
        payload = { }
        conn.request("POST", particlePath + device_id + "/led", params, headers)
        response = conn.getresponse()
        print(response)
        header = {
            "namespace":"Alexa.ConnectedHome.Control",
            "name":"TurnOnConfirmation",
            "payloadVersion":"2",
            "messageId": message_id
        }
    elif event['header']['name'] == 'TurnOffRequest':
        params = urllib.urlencode({'access_token': access_token, 'arg': "off"})
        payload = { }
        conn.request("POST", particlePath + device_id + "/led", params, headers)
        response = conn.getresponse()
        print(response)
        header = {
            "namespace":"Alexa.ConnectedHome.Control",
            "name":"TurnOffConfirmation",
            "payloadVersion":"2",
            "messageId": message_id
        }
        
    
    return { 'header': header, 'payload': payload }