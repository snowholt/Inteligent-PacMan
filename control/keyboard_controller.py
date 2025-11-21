from pynput.keyboard import Key, Controller
import time
import random

class KeyboardController:
    """
    Handles sending keyboard inputs to the OS.
    """

    def __init__(self):
        self.keyboard = Controller()
        self.key_map = {
            'UP': Key.up,
            'DOWN': Key.down,
            'LEFT': Key.left,
            'RIGHT': Key.right,
            'ESC': Key.esc
        }

    def press_key(self, key_name: str, duration: float = 0.05):
        """
        Press and release a key.
        
        Args:
            key_name: One of 'UP', 'DOWN', 'LEFT', 'RIGHT'.
            duration: How long to hold the key.
        """
        if key_name not in self.key_map:
            print(f"Warning: Key {key_name} not in key map.")
            return

        key = self.key_map[key_name]
        
        try:
            self.keyboard.press(key)
            time.sleep(duration)
            self.keyboard.release(key)
        except Exception as e:
            print(f"Error sending key {key_name}: {e}")

    def emergency_stop(self):
        """Stops all active inputs (if we were holding state, which we aren't currently)."""
        # In a more complex controller, we might release all held keys here.
        pass

if __name__ == "__main__":
    # Test
    print("Testing keyboard control in 3 seconds... Switch to a text editor!")
    time.sleep(3)
    controller = KeyboardController()
    
    directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    for _ in range(5):
        d = random.choice(directions)
        print(f"Pressing {d}")
        controller.press_key(d)
        time.sleep(0.5)
