# import time
from time import sleep
import serial
from serial import Serial
from serial import serialutil
from pebble import ProcessPool
# from pynput import keyboard
# from statistics import mean
# import os
# import sys
import AWSIoTPythonSDK
# sys.path.insert(0, os.path.dirname(AWSIoTPythonSDK.__file__))
# Now the import statement should work
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Setting serial
# Setting serial port parameters
serial_port = "/dev/ttyACM0"  # set your serial port
serial_baudrate = 115200  # set your baudrate
serial_timeout = 1  # set your serial timeout
ser_send = "s".encode()
ser_queue = []
counter = []

# Opening serial connectivity
try:
    ser = Serial(serial_port, baudrate=serial_baudrate, timeout=serial_timeout)
    print("The port {0} is available".format(ser))
except serialutil.SerialException:
    print("The port is at use, attempting to close and reopen")
    ser.close()
    ser.open()
    print("The port {0} is available".format(ser))


# Setting the initial parameters for velocity and steering
sleep_timer = 0.1
# Setting MQTT client variables (adjust certs paths and client name)
client_name = "Mikhail_PC_listen"
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


def listener_aws(self, params, packet):
    sleep(sleep_timer*1.5)
    try:
        if len(ser_queue) == 0:
            ser_queue.append(packet.payload)
            #ser.write(packet.payload)
        print("Current queue: ")
        print(ser_queue)
    except AWSIoTMQTTClientSDK.exception.AWSIoTExceptions.connectTimeoutException:
        print("###_MQTT CONNECTION ERROR_###")
        myMQTTClient.connect()
        myMQTTClient.subscribe("home/velocity", 1, listener_aws)

def serial_test():
    try:
        print(ser.readline().decode().strip())
    except (UnicodeDecodeError, serial.serialutil.SerialException) as serial_error:
        print("###_Serial error, resetting serial...###")
        ser.close()
        ser.open()

def send_to_serial():
    global ser_send
    global ser_queue
    if len(ser_queue) > 0:
        ser_send = ser_queue.pop(-1)
        ser_queue = []
    print("Writing to serial: " + ser_send.decode()) ## this guy hangs
    ser.write(ser_send)
    serial_test()
    with ProcessPool(max_workers=1, max_tasks=1) as pool:
        future = pool.schedule(serial_test, timeout=sleep_timer*10)
        try:
            result = future.result()  # blocks until results are ready
        except TimeoutError:
            print("Function took longer than {0} seconds.".format(sleep_timer*10)
            ser.close()
            ser.open()
    sleep(sleep_timer)

# Collect events until released

# MQTT connectivity
print('Connecting...')
myMQTTClient.connect()
print('Connected')

# MQTT subscription
myMQTTClient.subscribe("home/velocity", 1, listener_aws)

while True:
    try:
        send_to_serial()
    except KeyboardInterrupt:
            ser.close()
            MQTT.disconnect()
            print("Listener stopped")
