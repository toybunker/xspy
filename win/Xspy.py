import pynput
from pynput.keyboard import Key, Listener

# Define key mappings
key_map = {
    Key.space: " ",
    Key.enter: "\n"
}

def on_press(key):
    try:
        if key in key_map:
            print(key_map[key], end='', flush=True)
        else:
            print(key.char, end='', flush=True)
    except AttributeError:
        print(f" {key} ", end='', flush=True)

def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False

# Collect events until released
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
