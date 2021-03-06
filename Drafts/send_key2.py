#from serial import Serial
from pynput import keyboard
import threading
#ser = Serial("COM3", baudrate=9600, timeout=1)




def on_press(key):
    try:
        if key.char == "w":
            print('{0} pressed, sending it to serial'.format(
                key.char))
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

# Collect events until released
def velocity_listener():
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
def bitch_listener():
    with keyboard.Listener(
            on_press=on_press) as listener:
        listener.join()
        w
thread1 = threading.Thread(target = velocity_listener)
thread2 = threading.Thread(target = bitch_listener)
thread1.start()
thread2.start()