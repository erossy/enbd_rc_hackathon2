from pynput import keyboard
import threading

combination_velocity = {keyboard.KeyCode.from_char('w'), keyboard.KeyCode.from_char('s')}
current_velocity = set()
combination_turn = {keyboard.KeyCode.from_char('a'), keyboard.KeyCode.from_char('d')}
current_turn = set()
forward_busy = ""

def on_press_velocity(key):
    try:
        if key in combination_velocity:
            current_velocity.add(key)
            if all(k in current_velocity for k in combination_velocity):
                print("Cannot press W and S simultaneously")
            elif (key.char == 'w' and):
                write_velocity_fwd = threading.Thread(name ="write_velocity", target  = write_forward())
                write_velocity_fwd.start()

    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release_velocity(key):
    if key == keyboard.Key.esc:
        # Stop listenercal
        return False
    else:
        try:
            current_velocity.remove(key)
            print('{0} released'.format(
                key))
        except KeyError:
            pass

def on_press_turn(key):
    try:
        if key in combination_turn:
            current_turn.add(key)
            if all(k in current_turn for k in combination_turn):
                f = open("turn.txt", "a")
                f.write("Cannot press A and D at the same time")
                f.close()
            else:
                f = open("turn.txt", "a")
                f.write("{0} pressed".format(key))
                f.close()
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


def on_release_turn(key):
    if key == keyboard.Key.esc:
        return False
    else:
        try:
            current_turn.remove(key)
            print('{0} released'.format(
                key))
        except KeyError:
            pass

with keyboard.Listener(
        on_press=on_press_velocity,
        on_release=on_release_velocity) as listener:
    listener.join()


