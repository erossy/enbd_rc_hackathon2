#from serial import Serial
from pynput import keyboard
import threading
#ser = Serial("COM3", baudrate=9600, timeout=1)
combination_velocity = {keyboard.KeyCode.from_char('w'), keyboard.KeyCode.from_char('s')}
current_velocity = set()
combination_steering = {keyboard.KeyCode.from_char('a'), keyboard.KeyCode.from_char('d')}
current_steering = set()
velocity = ""
steering = ""

def on_press(key):
    global velocity
    global steering
    try:
        if key in combination_velocity:
            current_velocity.add(key)
            if all(k in current_velocity for k in combination_velocity) == False:
                velocity = str(next(iter(current_velocity)))[1]
        if key in combination_steering:
            current_steering.add(key)
            if all(k in current_steering for k in combination_steering) == False:
                steering = str(next(iter(current_steering)))[1]
    except KeyError:
        pass
    return(velocity, steering)

def on_release(key):
    global velocity
    if key == keyboard.Key.esc:
        print("Listener stopped")
        return False
    else:
        try:
            current_velocity.remove(key)
            if len(current_velocity) == 0:
                velocity = "0"
            else:
                velocity = str(next(iter(current_velocity)))[1]
        except KeyError:
            pass
    return(velocity, steering)

# Collect events until released
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

while listener.running == True:
    print(velocity)