import RPi.GPIO as GPIO
from time import sleep
from time import sleep
from serial import Serial
from pynput import keyboard
import os
import sys
import AWSIoTPythonSDK
sys.path.insert(0, os.path.dirname(AWSIoTPythonSDK.__file__))
# Now the import statement should work
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

#Setting serial
#Setting serial port parameters
serial_port_velocity = "COM3" ## set your serial port
serial_baudrate_velocity = 9600 ## set your baudrate
serial_timeout_velocity = 1 ## set your serial timeout

serial_port_steering = "/dev/ttyACM0" ## set your serial port
serial_baudrate_steering = 115200 ## set your baudrate
serial_timeout_steering = 1 ## set your serial timeout

##Setting the initial parameters for velocity and steering
sleep_timer = 0.1
output_velocity = "gpio" ## can be "print", "gpio" or "serial"
output_steering = "serial" ## can be "print", "gpio" or "serial"

if output_velocity == "serial":
    ser_velocity = Serial(serial_port_velocity, baudrate=serial_baudrate_velocity, timeout=serial_timeout_velocity)

if output_steering == "serial":
    ser_steering = Serial(serial_port_steering, baudrate=serial_baudrate_steering, timeout=serial_timeout_steering)

##Setting MQTT client variables (adjust certs paths and client name)
client_name = "Mikhail_PC_listen"
root_ca_path = "root-ca.pem"
private_key_path = "private.pem.key"
cert_path = "certificate.pem.crt"

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



def listener_velocity(self, params, packet):
	if output_velocity == "print":
		print (packet.payload)
	elif output_velocity == "serial":
		 ser_velocity.write(packet.payload)
	elif output_velocity == "gpio":
		if packet.payload == b'w':
			print("sending HIGH to dir")
			#GPIO.output(velocity_dir_gpio_port, 1)
			print("sending HIGH to speed")
		elif packet.payload == b's':
			print("sending LOW to dir")
			print ("sending HIGH to speed")



def listener_steering(self, params, packet):
	if output_steering == "print":
		print (packet.payload)
	elif output_steering == "serial":
		ser_steering.write(packet.payload)
		print(packet.payload)
		sleep(0.2)



def on_press(key):
    try:
        pass
    except AttributeError:
        pass

def on_release(key):
    try:
        if key == keyboard.Key.esc:
            print("Listener stopped")
            return False
    except KeyError:
            pass

# Collect events until released
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

print ('Connecting...')
myMQTTClient.connect()
print('Connected')
myMQTTClient.subscribe("home/velocity",1,listener_velocity)
myMQTTClient.subscribe("home/steering",1,listener_steering)

while listener.running == True:
    sleep(sleep_timer)
