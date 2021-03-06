
import time
import os
import sys
import AWSIoTPythonSDK
from pynput import keyboard
sys.path.insert(0, os.path.dirname(AWSIoTPythonSDK.__file__))
# Now the import statement should work
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

#Connection to the AWS IoT Core with Root CA certificate and unique device credentials (keys and certificate) previously$
def helloworld(self, params, packet):
 print ('Recived Message')
 print('Topic'+packet.topic)
 print("payload: ", (packet.payload))


# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("Testclientid2")

# For TLS mutual authentication
myMQTTClient.configureEndpoint("a1v7jr8kt53ffp-ats.iot.me-south-1.amazonaws.com", 8883)
#Provide your AWS IoT Core endpoint (Example: "abcdef12345-ats.iot.us-east-1.amazonaws.com")
myMQTTClient.configureCredentials("C:\\Users\\veltu\\PycharmProjects\\hackathon\\root-ca.pem", "C:\\Users\\veltu\\PycharmProjects\\hackathon\\private.pem.key", "C:\\Users\\veltu\\PycharmProjects\\hackathon\\certificate.pem.crt")


#Set path for Root CA and unique device credentials (use the private key and certificate retrieved from the logs in Step$
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)
print ('Connecting...')
myMQTTClient.connect()
#myMQTTClient.subscribe("home/helloworld",1,helloworld)

#while True:
#          time.sleep(5)

def on_press(key):
    try:
        print('{0} pressed, sending it to AWS'.format(
        key.char))
        myMQTTClient.publish(
            topic="home/helloworld",
            QoS=1,
            payload=key.char)
        #ser.write("w".encode())
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listenercal
        return False


with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

