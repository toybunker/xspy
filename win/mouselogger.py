from pynput import mouse, keyboard

# Define the event handlers for mouse
def on_move(x, y):
    print(f"Mouse moved to ({x}, {y})")

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y}) with {button}")
    else:
        print(f"Mouse released at ({x}, {y}) with {button}")

def on_scroll(x, y, dx, dy):
    print(f"Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy})")

# Define the event handler for keyboard
def on_press(key):
    try:
        if key.char == 'q':  # Press 'q' to stop the script
            return False
    except AttributeError:
        if key == keyboard.Key.esc:  # Press 'Esc' to stop the script
            return False

# Set up the mouse listener
mouse_listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)

# Set up the keyboard listener
keyboard_listener = keyboard.Listener(on_press=on_press)

# Start the listeners
mouse_listener.start()
keyboard_listener.start()

# Join the listeners to keep the script running
mouse_listener.join()
keyboard_listener.join()
