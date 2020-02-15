# pip3 install influxdb
# pip3 install python-dateutil

# Requires Python 3.6.x
# https://github.com/influxdata/influxdb-python

# NETSMART PYTHON INFLUXDB EXAMPLE CODE FOR HACK@CEWIT

from influxdb import InfluxDBClient
import json
import platform
import random
from dateutil.tz import tzlocal
from datetime import datetime
from time import sleep
from os import environ,getcwd


##############  CONNECTION STRING VARIABLES ##########
INFLUX_HOST="influx-cewit.netsmartdev.com"
INFLUX_DATABASE="db_team_69"
INFLUX_USER="user_team_69"
INFLUX_PASS="J9sdscUlGImEzBEP"
######################################################


class Ntst_Influx_Payload:
    def __init__(self, measurementName,tagKvDict,datestamp, fieldKvDict):
        self.measurement = measurementName
        self.tags = tagKvDict
        self.time = datestamp
        self.fields = fieldKvDict

# Get current user running your process
getUser = lambda: environ["USERNAME"] if "C:" in getcwd() else environ["USER"]
USERNAME = getUser()

# Add various tags (meta data) to 'group by' in the charts, providing many ways to filter and group on your measurements. 
tags = {"component":"primary_web_app","type":'method_timer',"hostname":platform.uname()[1],"os":platform.uname()[2],"user":USERNAME}

# Establish connection to database
client = InfluxDBClient(INFLUX_HOST, 443, INFLUX_USER, INFLUX_PASS, INFLUX_DATABASE,True,False)

def generate_data():
    # Send 10 random metric values into the database
    for x in range(10):
        try:
            #INFLUX client accepts an array of measurements.
            isoDate = datetime.now(tzlocal()).isoformat()
            # Random request size
            responseTime = random.randrange(50,10000)
            # Random response time
            payloadSize = random.randrange(1024,10000)
            # Multiple fields in a measurement
            fields = {'responseTimeMs':responseTime, 'requestSizeBytes':payloadSize}
    
            newPointObject = Ntst_Influx_Payload("request_timer",tags,isoDate,fields)
            
            # Influx requires an interable collection of dictionaries
            pointsArray=[newPointObject.__dict__]
            
            resultBool = client.write_points(pointsArray)
    
            print(f'[info] Wrote Point to InfluxDB @ {INFLUX_HOST}/{INFLUX_DATABASE} Result => {resultBool}')
            sleep(2)
        except Exception as e:
            print('[crit] An error occurred writing to influx: %s: %s' % (e.__class__, e))
            print(newPointObject.__dict__)
    
print(client.get_list_database())
print(client.get_list_measurements())
#client.drop_measurement('request_timer')
#generate_data()
print(client.get_list_measurements())
print(client.query('SELECT * from fake_sensor_data'))
