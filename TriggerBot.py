import time
import threading
import keyboard
import win32api
import sys
import numpy as np
from datetime import datetime
from ctypes import WinDLL
from mss import mss as mss_module

# Function to handle program exit by forcing an exit in case of expiration or manual exit
def exiting():
    try:
        exec(type((lambda: 0).__code__)(0, 0, 0, 0, 0, 0, b'\x053', (), (), (), '', '', 0, b''))
    except:
        try:
            sys.exit()  # Try to exit using sys.exit
        except:
            raise SystemExit  # If that fails, raise SystemExit to force exit

# Function to check if the program has passed the expiration date
def check_expiration():
    expiration_datetime = datetime(2030, 10, 19, 1, 10)  # Set expiration date
    current_datetime = datetime.now()  # Get current date and time
    if current_datetime > expiration_datetime:  # If current time is past expiration, exit the program
        print("The program has expired and will now exit.")
        exiting()

# Run expiration check when the script starts
check_expiration()

# Load Windows DLLs for system interaction (screen capturing, audio feedback)
user32, kernel32, shcore = (
    WinDLL("user32", use_last_error=True),
    WinDLL("kernel32", use_last_error=True),
    WinDLL("shcore", use_last_error=True),
)

# Set DPI awareness to handle high-resolution displays correctly
shcore.SetProcessDpiAwareness(2)

# Get screen dimensions
WIDTH, HEIGHT = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
ZONE = 5  # Zone size for the color detection

# Define the screen region to capture around the center of the screen
GRAB_ZONE = (
    int(WIDTH / 2 - ZONE),
    int(HEIGHT / 2 - ZONE),
    int(WIDTH / 2 + ZONE),
    int(HEIGHT / 2 + ZONE),
)

# Define the trigger bot class
class triggerbot:
    def __init__(self):
        # Initialize the bot's internal state and parameters
        self.triggerbot = False  # Whether the bot is active
        self.triggerbot_toggle = True  # Allow toggling the bot on and off
        self.exit_program = False  # Flag for when to exit the bot
        self.toggle_lock = threading.Lock()  # Lock to avoid toggling errors
        
        # Set default parameters
        self.trigger_hotkey = 0x02  # Default hotkey (hex code for the "Del" key)
        self.always_enabled = False  # Whether the bot is always active
        self.trigger_delay = 40  # Delay percentage before action triggers
        self.base_delay = 0.01  # Base delay (in seconds)
        self.color_tolerance = 70  # Tolerance for color matching
        self.R, self.G, self.B = (255, 51, 255)  # Target RGB color to detect (purple)

    # Function to provide a cooldown period after toggling the bot
    def cooldown(self):
        time.sleep(0.1)  # Short delay before allowing the bot to be toggled again
        with self.toggle_lock:
            self.triggerbot_toggle = True  # Re-enable toggling
            # Play a beep sound to indicate the bot's state (on/off)
            kernel32.Beep(440, 75), kernel32.Beep(700, 100) if self.triggerbot else kernel32.Beep(440, 75), kernel32.Beep(200, 100)

    # Function to capture the screen and search for the target color in the defined region
    def searcherino(self):
        print("searching for colour....")
        # Use 'mss' to capture a screenshot in the defined grab zone
        with mss_module() as sct:
            img = np.array(sct.grab(GRAB_ZONE))  # Capture image as numpy array

            pmap = np.array(img)  # Create an image array
            pixels = pmap.reshape(-1, 4)  # Flatten the pixel array (RGBA)

            # Create a mask to find pixels that match the target RGB color within tolerance
            color_mask = (
                (pixels[:, 0] > self.R - self.color_tolerance) & (pixels[:, 0] < self.R + self.color_tolerance) &
                (pixels[:, 1] > self.G - self.color_tolerance) & (pixels[:, 1] < self.G + self.color_tolerance) &
                (pixels[:, 2] > self.B - self.color_tolerance) & (pixels[:, 2] < self.B + self.color_tolerance)
            )
            matching_pixels = pixels[color_mask]  # Find pixels that match the color

            # If the bot is active and matching pixels are found, trigger the action
            if self.triggerbot and len(matching_pixels) > 0:
                print("found colour......")
                delay_percentage = self.trigger_delay / 100.0  # Calculate delay based on trigger delay percentage
                actual_delay = self.base_delay + self.base_delay * delay_percentage  # Calculate actual delay
                time.sleep(actual_delay)  # Wait before simulating the key press
                keyboard.press_and_release("K")  # Simulate pressing the 'k' key

    # Function to toggle the bot on and off using the F10 key
    def toggle(self):
        if keyboard.is_pressed("f10"):
            with self.toggle_lock:
                if self.triggerbot_toggle:  # Only toggle if allowed
                    self.triggerbot = not self.triggerbot  # Switch the bot's state
                    print(self.triggerbot)  # Print the bot's state (True/False)
                    self.triggerbot_toggle = False  # Disable toggling until cooldown
                    threading.Thread(target=self.cooldown).start()  # Start cooldown in a new thread

        # Exit the program if 'ctrl+shift+x' is pressed
        if keyboard.is_pressed("ctrl+shift+x"):
            self.exit_program = True
            exiting()

    # Function to hold the trigger key and keep searching for the target color
    def hold(self):
        while True:
            # While the hotkey is pressed, search for the target color
            while win32api.GetAsyncKeyState(self.trigger_hotkey) < 0:
                self.triggerbot = True  # Enable the bot while the key is pressed
                self.searcherino()  # Call the color search function
            else:
                time.sleep(0.1)  # Small delay when not holding the key

            # Exit the program if 'ctrl+shift+x' is pressed
            if keyboard.is_pressed("ctrl+shift+x"):
                self.exit_program = True
                exiting()

    # Main loop to start the bot functionality
    def starterino(self):
        while not self.exit_program:  # Keep running until exit is triggered
            if self.always_enabled:
                self.toggle()  # Allow toggling if always enabled
                self.searcherino() if self.triggerbot else time.sleep(0.1)  # Search or sleep based on bot state
            else:
                self.hold()  # Handle hotkey holding for triggering the search