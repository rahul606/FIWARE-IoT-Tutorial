import sys
import time
from random import randint

from fiotclient.context import FiwareContextClient
from fiotclient.iot import FiwareIotClient

if __name__ == '__main__':
    arguments = []
    if len(sys.argv) > 1:
        arguments = sys.argv

    DEVICE_FILE_ROOT = "./devices/"

    LDR_DEVICE_ID = "UL_LDR"
    LDR_ENTITY_ID = "LDR001"
    LDR_FILE_PATH = DEVICE_FILE_ROOT + "LDR.json"

    LED_DEVICE_ID = "UL_LED"
    LED_ENTITY_ID = "LED001"
    LED_FILE_PATH = DEVICE_FILE_ROOT + "LED.json"

    client_iot = FiwareIotClient("config.ini")
    client_context = FiwareContextClient("config.ini")

    if '--no-register-device' not in arguments:
        client_iot.register_device(LDR_FILE_PATH, LDR_DEVICE_ID, LDR_ENTITY_ID)
        client_iot.register_device(LED_FILE_PATH, LED_DEVICE_ID, LED_ENTITY_ID)

    if '--no-subscribe-cygnus' not in arguments:
        client_context.subscribe_cygnus(LDR_ENTITY_ID, ["luminosity"])
        client_context.subscribe_cygnus(LED_ENTITY_ID, ["state"])

    if '--no-subscribe-sth' not in arguments:
        client_context.subscribe_historical_data(LDR_ENTITY_ID, ["luminosity"])

    try:
        while True:
            reading = randint(0, 255)
            print('Sending LDR reading:', reading)
            client_iot.send_observation(LDR_DEVICE_ID, {'l': reading}, protocol='MQTT')
            time.sleep(10)
    except KeyboardInterrupt:
        pass
