import sys
import time

#library required to read the AM2302 sensor used in the example, available at:
#https://github.com/adafruit/Adafruit_Python_DHT
import Adafruit_DHT


import fiotclient
from fiotclient.context import FiwareContextClient
from fiotclient.iot import FiwareIotClient

if __name__ == '__main__':
    arguments = []
    if len(sys.argv) > 1:
        arguments = sys.argv



    #device directory definition
    DEVICE_FILE_ROOT = "/home/pi/exemploFiware/"

    #Service Name Setting
    SERVICE_NAME ='RaspberryPiUFRNStela'

    #service path name definition
    SERVICE_PATH ='/RaspberryDHTStela'

    #api_key definition generated in the creation of the service
    API_KEY = '250e10409ada11e7b137b827eb1df5b0'

    #id of the device to be sent
    DHT_DEVICE_ID = "STELA_DHT"

    #id of the entity that is attached to the device
    DHT_ENTITY_ID = "01"

    #device to be used in the application
    Device = "DHT.json"

    #complete device directory
    DHT_FILE_PATH = DEVICE_FILE_ROOT + Device

    #sensor setting used
    sensor = Adafruit_DHT.AM2302

    #definition of the GPIO pin used in Raspberry pi
    GPIOpin = '4'

    #time between measurements
    DELAY_MEASUREMENT = 10

    #creating an instance of the iot and context classes of the fiotclient library
    client_iot = FiwareIotClient("config.ini")
    client_context = FiwareContextClient("config.ini")


    #assigning the service and the service path
    if '--no-set-service' not in arguments:
        client_iot.set_service(SERVICE_NAME, SERVICE_PATH)

    #assigning api_key
    if '--no-set-api-key' not in arguments:
        client_iot.set_api_key(API_KEY)

    #registering the device
    if '--no-register-device' not in arguments:
        client_iot.register_device(DHT_FILE_PATH, DHT_DEVICE_ID, DHT_ENTITY_ID)

    #assigning the entity
    if '--no-set-service' not in arguments:
        client_context.set_service(SERVICE_NAME, SERVICE_PATH)

    #making the entry in cygnus, using the arguments (Entity_ID, [attrs ..])
    if '--no-subscribe-cygnus' not in arguments:
        client_context.subscribe_cygnus(DHT_ENTITY_ID, ["humidity","temperature"])

    #making the entry for data history, using the arguments (Entity_ID, [attrs ..])
    if '--no-subscribe-sth' not in arguments:
        client_context.subscribe_historical_data(DHT_ENTITY_ID, ["humidity","temperature"])

    try:
        while True:
            #reading of the AM2302 sensor, used in this example
            humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIOpin)

            #send the measurement to the server, using the arguments ('ID_DEVICE', {'ATTR_01': VAL_01, 'ATTR_02': 'VAL_02', protocol = 'PROTOCOL')
            client_iot.send_observation(DHT_DEVICE_ID, {'humidity': humidity,'temperature':temperature}, protocol='MQTT')

            print("measurement sent!")
            time.sleep(DELAY_MEASUREMENT)
    except KeyboardInterrupt:
        pass
