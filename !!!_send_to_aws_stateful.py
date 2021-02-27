from time import sleep
from pynput import keyboard
# import os
# import sys
import AWSIoTPythonSDK
# sys.path.insert(0, os.path.dirname(AWSIoTPythonSDK.__file__))
# Now the import statement should work
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Setting the initial parameters for velocity and steering
velocity = 0
steering = 0
payload = 0
direction_dict = {
  "00": "s",
  "01": "a",
  "02": "d",
  "10": "w",
  "11": "q",
  "12": "e",
  "20": "x",
  "21": "z",
  "22": "c"
}

sleep_timer = 0.1  # controls flooding in seconds (default = 50ms)

# Setting MQTT client variables (adjust certs paths and client name)
client_name = "Mikhail_PC"
root_ca_path = "root-ca.pem"
private_key_path = "private.pem.key"
cert_path = "certificate.pem.crt"

# Don't touch the following parameters
MQTT_endpoint_url = "a1v7jr8kt53ffp-ats.iot.me-south-1.amazonaws.com"
MQTT_TCP_port = 8883
MQTT_Topic_velocity = "home/velocity"
MQTT_Topic_steering = "home/steering"

# Setting MQTT client connectivity parameters
myMQTTClient = AWSIoTMQTTClient(client_name)
myMQTTClient.configureEndpoint(MQTT_endpoint_url, MQTT_TCP_port)
myMQTTClient.configureCredentials(root_ca_path, private_key_path, cert_path)
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(1000)
myMQTTClient.configureMQTTOperationTimeout(1000)


def MQTT_send_state(payload):  # Sends data to AWS IOT core
    try:
        myMQTTClient.publish(
            topic=MQTT_Topic_velocity,
            QoS=0,
            payload=payload
        )
        print(payload+"Published")
    except RuntimeError:
        print("Connection lost, re-establishing...")
        myMQTTClient.connect()
        print("Connection re-established")
        myMQTTClient.publish(
            topic=MQTT_Topic_velocity,
            QoS=0,
            payload=payload
        )


def on_press(key):  # Computes payload on press
    global velocity
    global steering
    global payload
    try:
        if (key.char == "w" and velocity == 0):
            velocity = 1
        if (key.char == "s" and velocity == 0):
            velocity = 2
        if (key.char == "a" and steering == 0):
            steering = 1
        if (key.char == "d" and steering == 0):
            steering = 2
    except AttributeError:
        pass
    if str(velocity)+str(steering) != payload:
        payload = str(velocity)+str(steering)
        direction = direction_dict[payload]
        print("Payload: "+payload+"; Direction: "+direction)
        MQTT_send_state(direction)


def on_release(key):  # Computes payload on release
    global velocity
    global steering
    global payload
    if key == keyboard.Key.esc:
        print("Listener stopped")
        try:
            myMQTTClient.disconnect()
        except:
            pass
        return False
    else:
        try:
            if ((key.char == "w" and velocity != 2) or
                    (key.char == "s" and velocity != 1)):
                velocity = 0
            if ((key.char == "a" and steering != 2) or
                    (key.char == "d" and steering != 1)):
                steering = 0
        except AttributeError:
            pass
    if str(velocity)+str(steering) != payload:
        payload = str(velocity)+str(steering)
        direction = direction_dict[payload]
        print("Payload: "+payload+"; Direction: "+direction)
        MQTT_send_state(direction)


# MQTT connection
print('Connecting...')
myMQTTClient.connect()
print('Connected...')

# Collect events until released
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

while listener.running:
    sleep(sleep_timer*2)
