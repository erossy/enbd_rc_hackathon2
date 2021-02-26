from time import sleep
from pynput import keyboard
import os
import sys
import AWSIoTPythonSDK
sys.path.insert(0, os.path.dirname(AWSIoTPythonSDK.__file__))
# Now the import statement should work
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

##Setting the initial parameters for velocity and steering
velocity = "0"
steering = "0"
sleep_timer = 0.1 #controls flooding in seconds (default = 50ms)

##Setting MQTT client variables (adjust certs paths and client name)
client_name = "Mikhail_PC"
root_ca_path = "C:\\Users\\veltu\\PycharmProjects\\hackathon\\root-ca.pem"
private_key_path = "C:\\Users\\veltu\\PycharmProjects\\hackathon\\private.pem.key"
cert_path = "C:\\Users\\veltu\\PycharmProjects\\hackathon\\certificate.pem.crt"

##Don't touch the following parameters
MQTT_endpoint_url = "a1v7jr8kt53ffp-ats.iot.me-south-1.amazonaws.com"
MQTT_TCP_port = 8883
MQTT_Topic_velocity = "home/velocity"
MQTT_Topic_steering = "home/steering"

##Setting MQTT client connectivity parameters
myMQTTClient = AWSIoTMQTTClient(client_name)
myMQTTClient.configureEndpoint(MQTT_endpoint_url, MQTT_TCP_port)
myMQTTClient.configureCredentials(root_ca_path, private_key_path, cert_path)
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)

def on_press(key):
    global velocity
    global steering
    try:
        if ((key.char == "w" or key.char == "s") and velocity == "0"):
            velocity = key.char
        elif ((key.char == "a" or key.char == "d") and steering == "0"):
            steering = key.char
    except AttributeError:
        pass
    return(velocity, steering)

def on_release(key):
    global velocity
    global steering
    if key == keyboard.Key.esc:
        print("Listener stopped")
        return False
    else:
        try:
            if key.char == velocity:
                velocity = "0"
            elif key.char == steering:
                steering = "0"
        except AttributeError:
            pass
    return(velocity, steering)

def MQTT_send_velocity():
    myMQTTClient.publish(
        topic=MQTT_Topic_velocity,
        QoS=1,
        payload=velocity
    )

def MQTT_send_steering():
    myMQTTClient.publish(
        topic=MQTT_Topic_steering,
        QoS=1,
        payload=steering
    )


# Collect events until released
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

print ('Connecting...')
myMQTTClient.connect()
print ('Connected...')

while listener.running == True:
        if velocity != "0":
            MQTT_send_velocity()
        if steering != "0":
            MQTT_send_steering()
        sleep(sleep_timer)
