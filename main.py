import threading  # Import the threading module to handle concurrent execution
from TriggerBot import triggerbot, check_expiration  # Import the triggerbot class and check_expiration function from the core module
from gui import BotSettingsGUI  # Import the BotSettingsGUI class from the gui module
from PyQt5 import QtWidgets  # Import QtWidgets from PyQt5 for GUI elements

def launch_gui(bot):
    """
    Initializes and runs the GUI application.

    Args:
        bot (triggerbot): An instance of the triggerbot class that the GUI will interact with.
    """
    app = QtWidgets.QApplication([])  # Create a new Qt application instance
    gui = BotSettingsGUI(bot)  # Create an instance of the BotSettingsGUI class, passing the bot instance
    gui.show()  # Show the GUI window
    app.exec_()  # Start the Qt event loop, which keeps the GUI running

if __name__ == "__main__":
    """
    Entry point of the script. Runs when the script is executed directly.
    """
    check_expiration()  # Check if the program has expired; exits if it has
    bot = triggerbot()  # Create an instance of the triggerbot class
    # Start the bot's main loop in a new thread so it can run concurrently with the GUI
    threading.Thread(target=bot.starterino).start()
    launch_gui(bot)  # Initialize and run the GUI, passing the bot instancvalorae for interaction