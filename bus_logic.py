import requests
import json
from datetime import datetime, timezone

current_time = datetime.now(timezone.utc)
current_time_str = current_time.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
headers ={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Ocp-Apim-Subscription-Key": "630688984d38409689932a37a8641bb9",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://journeyplanner-production.transportforireland.ie",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Accept-Encoding": "gzip, deflate, br",

    }

def getStopId(stopnum):
    url = "https://api-lts.transportforireland.ie/lts/lts/v1/public/locationOrServiceLookup"
    
    data ={"query":stopnum,"operatorCodes":[],"language":"en","resultOrder":["POST_CODE","TRAIN_STATION","TRAM_STOP_AREA","BUS_STOP","LOCALITY","SERVICE","STREET"]}

    response = requests.post(url, headers=headers, json=data)
    #print(response.json())
    return([response.json()[0]['id'],response.json()[0]['name']])


def getService(stop_id,stop_name):

    url = "https://api-lts.transportforireland.ie/lts/lts/v1/public/departures"
    data ={
        "clientTimeZoneOffsetInMS":0,
        "departureDate":current_time_str,
        "departureTime":current_time_str,
        "stopIds":[stop_id],
        "stopType":"BUS_STOP",
        "stopName":stop_name,
        "requestTime":current_time_str,
        "departureOrArrival":"DEPARTURE",
        "refresh":False}

    response = requests.post(url, headers=headers, json=data)
    return(response.json())

if __name__ == "__main__":
    stopnum = input("Enter Stop Number: ")
    resp_j = getStopId(stopnum)
    resp_j = getService(resp_j[0],resp_j[1])

def list_out(resp_j):
    out =""
    for i in range(len(resp_j['stopDepartures'])):
        
        if resp_j['stopDepartures'][i]['realTimeDeparture']!=None:

            real_time = resp_j['stopDepartures'][i]['realTimeDeparture']
            flag = True
        else:
            real_time = resp_j['stopDepartures'][i]['scheduledDeparture']
            flag = False
        real_time = datetime.fromisoformat(real_time)
        
        service_name = resp_j['stopDepartures'][i]['serviceNumber']
        serviceDisplayName = resp_j['stopDepartures'][i]['serviceDisplayName']
        current_time = datetime.now(timezone.utc)
        difference_minutes = round((real_time-current_time).total_seconds() / 60)
        if difference_minutes <=0:
            continue
        minutes = "minutes"
        if difference_minutes>60:
            difference_minutes = round(difference_minutes/60)
            minutes = "hours"
        if flag:
            
            out += str(service_name)+" " +str(serviceDisplayName)+ " In " + str(difference_minutes)+ " " +minutes +"\n"
        else:        

            out += str(service_name)+" " +str(serviceDisplayName)+ " Scheduled in: "+ str(difference_minutes)+" " +minutes+"\n"

    return(out)

