import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from fiotclient.iot import FiwareIotClient

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.IN)     # read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)     # FAN output pin

PIR_DEVICE_ID = "STELA_PIR"
FAN_DEVICE_ID = "STELA_FAN"

MQTT_BROKER_ADDRESS = '10.7.49.163'
SERVICE_NAME = 'RpiService'
SERVICE_PATH = '/rpi'
SERVICE_API_KEY = "6026bc2a8c4f11e79f9eb827eb3e58ef"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/{}/{}/cmd".format(SERVICE_API_KEY, FAN_DEVICE_ID))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    topic = msg.topic
    print("Topic: " + topic)
    incoming_message = msg.payload.decode("utf-8")  # ex: STELA_FAN@change_state|ON
    print("Message: " + incoming_message)

    splitted_incoming_message = incoming_message.split('@')
    device_id = splitted_incoming_message[0]
    cmd = splitted_incoming_message[1]
    splitted_cmd = cmd.split('|')
    cmd_name = splitted_cmd[0]
    cmd_param = splitted_cmd[1]

    response_topic = topic + 'exe'
    payload_response_ok = '{}@{}|{}'.format(device_id, cmd_name, 'SUCCESS')
    payload_response_error = '{}@{}|{}'.format(device_id, cmd_name, 'ERROR')

    if cmd_name == 'change_state':
        if cmd_param == 'ON':
            print('Change state to ON')
            GPIO.output(3, 1)
            client.publish(response_topic, payload_response_ok)
        elif cmd_param == 'OFF':
            print('Change state to OFF')
            GPIO.output(3, 0)
            client.publish(response_topic, payload_response_ok)
        else:
            print('Unknown parameter')
            client.publish(response_topic, payload_response_error)
    else:
        print('Unknown command')
        client.publish(response_topic, payload_response_error)


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_BROKER_ADDRESS, 1883, 60)

mqtt_client.loop_start()

iot_client = FiwareIotClient("config.ini")
iot_client.set_service(SERVICE_NAME, SERVICE_PATH)
iot_client.set_api_key(SERVICE_API_KEY)

while True:
    presence_read = GPIO.input(11)
    presence = True if presence_read == 1 else False
    iot_client.send_observation(PIR_DEVICE_ID, {'p': presence}, protocol='MQTT')

    if not presence:                 # when output from motion sensor is LOW
        print("No presence")
        GPIO.output(3, 0)            # turn OFF FAN
    else:                            # when output from motion sensor is HIGH
        print("Presence detected")
        GPIO.output(3, 1)            # turn ON FAN

    time.sleep(5)                    # wait for 5 seconds
