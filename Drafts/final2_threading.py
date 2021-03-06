from serial import Serial
from time import sleep
from pynput import keyboard
from threading import Thread
velocity = "0"
steering = "0"
ser_COM_velocity = "COM3" #set serial port that connecting Arduino controlling forward/backward movement
ser_COM_steering = "COM4" #set serial port that connecting Arduino controlling steering
#ser_velocity = Serial(ser_COM_velocity, baudrate=9600, timeout=1)
#ser_steering = Serial(ser_COM_steering, baudrate=9600, timeout=1)
sleep_timer = 0.1 #controls serial flooding in seconds (default = 50ms)

def on_press_velocity(key):
    global velocity
    try:
        if ((key.char == "w" or key.char == "s") and velocity == "0"):
            velocity = key.char
    except AttributeError:
        pass
    return(velocity)

def on_release_velocity(key):
    global velocity
    if key == keyboard.Key.esc:
        print("Listener stopped")
        return False
    else:
        try:
            if key.char == velocity:
                velocity = "0"
        except KeyError:
            pass
    return(velocity)

def on_press_steering(key):
    global steering
    try:
        if ((key.char == "a" or key.char == "d") and steering == "0"):
            steering = key.char
    except AttributeError:
        pass
    return(steering)

def on_release_steering(key):
    global steering
    if key == keyboard.Key.esc:
        print("Listener stopped")
        return False
    else:
        try:
            if key.char == steering:
                steering = "0"
        except KeyError:
            pass
    return(steering)

def communicate_velocity_serial():
    while listener_velocity.running == True and listener_steering.running == True:
        if velocity != "0":
            #print(velocity)
            f = open("velocity.txt", "a")
            f.write(velocity)
            f.close()
            # ser_velocity.write(velocity.encode())
            sleep(sleep_timer)

def communicate_steering_serial():
    while listener_velocity.running == True and listener_steering.running == True:
        if steering != "0":
            #print(steering)
            g = open("steering.txt", "a")
            g.write(steering)
            g.close()
            # ser_velocity.write(steering.encode())
            sleep(sleep_timer)

# Collect events until released
listener_velocity = keyboard.Listener(
    on_press=on_press_velocity,
    on_release=on_release_velocity)
thread_velocity

listener_steering= keyboard.Listener(
    on_press=on_press_steering,
    on_release=on_release_steering)
listener_steering.start()

thread_velocity_send = Thread(name = "velocity", target=communicate_velocity_serial())
thread_steering_send = Thread(name = "steering", target=communicate_steering_serial())

thread_velocity_send.start()
thread_steering_send.start()



#while listener_velocity.running == True and listener_steering.running == True:
#       sleep(sleep_timer)