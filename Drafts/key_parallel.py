
from pynput import keyboard
def on_press_velocity(key):
    try:
        if key.char == "w" or key.char == "s":
            print('{0} pressed, sending it to serial'.format(
                key.char))
            #ser.write("w".encode())
        else:
            print('{0} pressed, not interesting'.format(
            key.char))
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
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
