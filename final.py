
#from serial import Serial
from time import sleep
from pynput import keyboard
velocity = "0"
steering = "0"
ser_COM_velocity = "COM3" #set serial port that connecting Arduino controlling forward/backward movement
ser_COM_steering = "COM4" #set serial port that connecting Arduino controlling steering
#ser_velocity = Serial(ser_COM_velocity, baudrate=9600, timeout=1)
#ser_steering = Serial(ser_COM_steering, baudrate=9600, timeout=1)
sleep_timer = 0.1 #controls serial flooding in seconds (default = 50ms)

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
        except KeyError:
            pass
    return(velocity, steering)

# Collect events until released
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

while listener.running == True:
        if velocity != "0":
            print(velocity)
            #ser_velocity.write(velocity.encode())
        if steering != "0":
            print(steering)
            #ser_steering.write(steering.encode())
        sleep(sleep_timer)
