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
        Simulate a key press.
        """
        if key_name not in self.key_map:
            print(f"Warning: Key {key_name} not in key map.")
            return
            
        key_char = self.key_map[key_name]
        
        try:
            k = key_char
            self.keyboard.press(k)
            time.sleep(duration)
            self.keyboard.release(k)
            
        except Exception as e:
            print(f"Error pressing key: {e}")

    def execute_action(self, action: str):
        """
        Execute the action decided by the agent.
        Wrapper around press_key.
        """
        if action and action != 'STOP':
            self.press_key(action)

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
