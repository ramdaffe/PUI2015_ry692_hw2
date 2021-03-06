__author__ = "ry692@nyu.edu"

import json
import sys
import csv
import urllib2

API_KEY = sys.argv[1]
BASE_URL = "http://bustime.mta.info/api/siri/vehicle-monitoring.json"
BUS_ARG = sys.argv[2]
OUTFILE= sys.argv[3]
busdata = []
busline = ""
v_loc = []
size = 0

def main():
    busdata = loadRemoteData()
    size = len(busdata)
    busline = busdata[0]["MonitoredVehicleJourney"]["PublishedLineName"]
    for n in range(0,size):
        v = busdata[n]["MonitoredVehicleJourney"]
        v_loc.append({"name": n,"v_lat": getLat(v),"v_long": getLong(v), "v_next": getNextStop(v), "v_status":getStatus(v)})
    saveFile()
    print "File exported as " + OUTFILE

def getLat(b):
    return b["VehicleLocation"]["Latitude"]

def getLong(b):
    return b["VehicleLocation"]["Longitude"]

def getNextStop(b):
    val = b["OnwardCalls"]["OnwardCall"][0]["StopPointName"]
    if not val=="":
        return val
    else:
        return "N/A"

def getStatus(b):
    val = b["OnwardCalls"]["OnwardCall"][0]["Extensions"]["Distances"]["PresentableDistance"]
    if not val=="":
        return val
    else:
        return "N/A"


def displayData():
    print "Bus Line: " + busline
    print "Number of active buses: " + str(size)
    for m in range(0,len(v_loc)):
        print str(v_loc[m]["name"]) + str(v_loc[m]["v_lat"]) +str(v_loc[m]["v_long"]) + str(v_loc[m]["v_next"] + str(v_loc[m]["v_status"]))
        #print "Bus " + str(v_loc[m]["name"]) + " is at latitude " + str(v_loc[m]["v_lat"]) + " and longitude " + str(v_loc[m]["v_long"])

def saveFile():
    f = open(OUTFILE, 'wb')
    try:
        writer = csv.writer(f,quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(("Bus ID","Latitude","Longitude","Stop Name","Stop Status"))
        for m in range(0,len(v_loc)):
            currentVehicle = (v_loc[m]["name"],v_loc[m]["v_lat"],v_loc[m]["v_long"],v_loc[m]["v_next"],v_loc[m]["v_status"])
            writer.writerow(currentVehicle)
    finally:
        f.close()

def loadRemoteData():
    PARAM_DETAIL = "VehicleMonitoringDetailLevel=calls"
    PARAM_BUSLINE = "LineRef=" + BUS_ARG
    PARAM_KEY = "key=" + API_KEY
    url = BASE_URL + "?" + PARAM_KEY + "&" + PARAM_DETAIL + "&" + PARAM_BUSLINE
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    #print response.read()
    return data["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"][0]["VehicleActivity"]

if __name__ == '__main__':
    main()

#BUSLINE = sys.arg[0]
