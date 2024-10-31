from pynput import mouse

# Define the event handlers
def on_move(x, y):
    print(f"Mouse moved to ({x}, {y})")

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y}) with {button}")
    else:
        print(f"Mouse released at ({x}, {y}) with {button}")

def on_scroll(x, y, dx, dy):
    print(f"Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy})")

# Set up the listener
with mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll) as listener:
    listener.join()
