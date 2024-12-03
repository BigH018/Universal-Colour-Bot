from PyQt5 import QtWidgets, QtGui, QtCore

class BotSettingsGUI(QtWidgets.QWidget):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.dark_mode = False  # Default to light mode
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Creator - BigH")
        self.setGeometry(100, 100, 500, 400)  # Adjusted size for better layout
        ##self.setWindowIcon(QtGui.QIcon('icon.png'))
        
        layout = QtWidgets.QVBoxLayout()

        # Window shadow effect
        self.setGraphicsEffect(self.create_shadow())

        # Add a toggle for dark/light mode
        self.mode_toggle = QtWidgets.QPushButton("Switch to Dark Mode")
        self.mode_toggle.clicked.connect(self.toggle_mode)
        layout.addWidget(self.mode_toggle)

        # Styling for better visual appeal
        self.setStyleSheet(self.get_stylesheet())

        # Group Box for Hotkey Section
        hotkey_group = QtWidgets.QGroupBox("Hotkey Settings")
        hotkey_layout = QtWidgets.QVBoxLayout()

        # Dropdown for hotkey selection
        self.hotkey_label = QtWidgets.QLabel("Trigger Hotkey:")
        self.hotkey_combo = QtWidgets.QComboBox()
        self.hotkey_combo.addItems(["Left Shift", "Right Mouse Click", "Mouse Button 5", "Mouse Button 6", "Custom"])
        self.hotkey_combo.currentIndexChanged.connect(self.update_hotkey_input)
        hotkey_layout.addWidget(self.hotkey_label)
        hotkey_layout.addWidget(self.hotkey_combo)

        # Custom input field for hex code
        self.hotkey_input = QtWidgets.QLineEdit()
        self.hotkey_input.setPlaceholderText("Enter hex code (e.g., 0x02)")
        self.hotkey_input.setVisible(False)  # Hide by default
        hotkey_layout.addWidget(self.hotkey_input)

        hotkey_group.setLayout(hotkey_layout)
        layout.addWidget(hotkey_group)

        # Group Box for Timing Settings
        timing_group = QtWidgets.QGroupBox("Timing Settings")
        timing_layout = QtWidgets.QVBoxLayout()
        self.trigger_delay_input = self.create_input_field(timing_layout, "Trigger Delay (%):", str(self.bot.trigger_delay))
        self.base_delay_input = self.create_input_field(timing_layout, "Base Delay (s):", f"{self.bot.base_delay:.4f}", is_decimal=True)
        timing_group.setLayout(timing_layout)
        layout.addWidget(timing_group)

        # Group Box for Color Settings
        color_group = QtWidgets.QGroupBox("Color Detection Settings")
        color_layout = QtWidgets.QVBoxLayout()
        self.tolerance_input = self.create_input_field(color_layout, "Color Tolerance:", str(self.bot.color_tolerance))
        self.r_input = self.create_input_field(color_layout, "RGB Values: (Red)", str(self.bot.R))
        self.g_input = self.create_input_field(color_layout, "RGB Values: (Green)", str(self.bot.G))
        self.b_input = self.create_input_field(color_layout, "RGB Values: (Blue)", str(self.bot.B))
        color_group.setLayout(color_layout)
        layout.addWidget(color_group)

        # Save button with rounded corners
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        # Add a Tutorial button
        self.tutorial_button = QtWidgets.QPushButton("Tutorial")
        self.tutorial_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.tutorial_button.clicked.connect(self.show_tutorial)
        layout.addWidget(self.tutorial_button)

        self.setLayout(layout)
        self.update_hotkey_input()  # Update visibility of the custom input field based on the default selection

    def create_input_field(self, layout, label_text, default_value, is_decimal=False):
        layout.addWidget(QtWidgets.QLabel(label_text))
        input_field = QtWidgets.QLineEdit(default_value)
        if is_decimal:
            input_field.setValidator(QtGui.QDoubleValidator(0.0, 99.99, 4))  # Set validator for 4 decimal places
        layout.addWidget(input_field)
        return input_field

    def get_stylesheet(self):
        if self.dark_mode:
            return """
            QWidget {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #4C4C4C;
                color: #FFFFFF;
                border: 1px solid #6C6C6C;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #6C6C6C;
            }
            QLabel {
                color: #FFFFFF;
            }
            QLineEdit {
                background-color: #3E3E3E;
                color: #FFFFFF;
                border: 1px solid #6C6C6C;
                padding: 5px;
                border-radius: 5px;
            }
            QComboBox {
                background-color: #3E3E3E;
                color: #FFFFFF;
                border: 1px solid #6C6C6C;
                padding: 5px;
                border-radius: 5px;
            }
            """
        else:
            return """
            QWidget {
                background-color: #F7F7F7;
                color: #333333;
            }
            QPushButton {
                background-color: #E0E0E0;
                color: #333333;
                border: 1px solid #B0B0B0;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D0D0D0;
                border-color: #A0A0A0;
            }
            QLabel {
                color: #333333;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #FFFFFF;
                color: #333333;
                border: 1px solid #B0B0B0;
                padding: 5px;
                border-radius: 5px;
            }
            QComboBox {
                background-color: #FFFFFF;
                color: #333333;
                border: 1px solid #B0B0B0;
                padding: 5px;
                border-radius: 5px;
            }
            """

    def toggle_mode(self):
        
        self.dark_mode = not self.dark_mode
        self.mode_toggle.setText("Switch to Light Mode" if self.dark_mode else "Switch to Dark Mode")
        # Clear the existing stylesheet before applying the new one
        self.setStyleSheet("")
        self.setStyleSheet(self.get_stylesheet())

    def update_hotkey_input(self):
        if self.hotkey_combo.currentText() == "Custom":
            self.hotkey_input.setVisible(True)
            self.hotkey_input.setText(f"0x{self.bot.trigger_hotkey:02X}")
        else:
            self.hotkey_input.setVisible(False)
            default_keys = {
                "Left Shift": 0x10,  # Example key codes
                "Right Mouse Click": 0x02,
                "Mouse Button 5": 0x05,
                "Mouse Button 6": 0x06
            }
            self.bot.trigger_hotkey = default_keys.get(self.hotkey_combo.currentText(), 0x00)
            self.hotkey_input.setText("")

    def save_settings(self):
        try:
            if self.hotkey_combo.currentText() == "Custom":
                self.bot.trigger_hotkey = int(self.hotkey_input.text(), 16)
            else:
                default_keys = {
                    "Left Shift": 0x10,
                    "Right Mouse Click": 0x02,
                    "Mouse Button 5": 0x05,
                    "Mouse Button 6": 0x06
                }
                self.bot.trigger_hotkey = default_keys.get(self.hotkey_combo.currentText(), 0x00)
            self.bot.trigger_delay = int(self.trigger_delay_input.text())
            self.bot.base_delay = float(self.base_delay_input.text())
            self.bot.color_tolerance = int(self.tolerance_input.text())
            self.bot.R = int(self.r_input.text())
            self.bot.G = int(self.g_input.text())
            self.bot.B = int(self.b_input.text())
            self.close()
        except ValueError:
            print("Invalid input, please check your values.")

    def show_tutorial(self):
        tutorial_window = TutorialWindow(is_dark_mode=self.dark_mode)  # Pass the current dark mode state
        tutorial_window.exec_()  # Show the tutorial window modally

    def create_shadow(self):
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 0)
        return shadow

class TutorialWindow(QtWidgets.QDialog):
    def __init__(self, is_dark_mode=False):
        super().__init__()
        self.setWindowTitle("Tutorial")
        self.setGeometry(150, 150, 600, 400)  # Adjusted size for detailed content
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.current_page = 0  # Keep track of the current page
        self.dark_mode = is_dark_mode  # Inherit dark mode from the main window
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        # QStackedWidget to hold different pages
        self.page_stack = QtWidgets.QStackedWidget(self)
        layout.addWidget(self.page_stack)

        # Add tutorial pages to the stacked widget with better spacing and readability
        self.add_page("Hotkey Settings", """
    <h3 style="font-size: 20px; font-weight: bold;">What is the Hotkey?</h3>
    <p>The <strong>Trigger Hotkey</strong> is the key or mouse button that activates the bot. This key tells the bot when to start or stop performing its actions.</p>
    
    <h4 style="font-size: 18px; font-weight: bold;">How to Use:</h4>
    <ul>
        <li>Choose from predefined options like "Left Shift," "Right Mouse Click," "Mouse Button 5," or "Mouse Button 6."</li>
        <li>Select the <strong>Custom</strong> option to enter any hex code for a key of your choice.</li>
    </ul>
    
    <p><strong>Tip:</strong> Go to you browser and type in virtual key codes and click on the microsoft website. find the value of the hotkey you want for example 0x04 is middle mouse button.</p>
""")

        self.add_page("Timing Settings", """
    <h3 style="font-size: 20px; font-weight: bold;">Understanding Timing</h3>
    <p><strong>Trigger Delay (%)</strong> and <strong>Base Delay (s)</strong> allow you to control how fast the bot reacts.</p>

    <h4 style="font-size: 18px; font-weight: bold;">What Do These Settings Do?</h4>
    <ul>
        <li><strong>Trigger Delay (%)</strong>: Adjusts how much delay (as a percentage) is applied before the bot performs its action.</li>
        <li><strong>Base Delay (s)</strong>: The base time in seconds that the bot waits before pressing a key.</li>
    </ul>

    <h4 style="font-size: 18px; font-weight: bold;">How to Adjust:</h4>
    <p>You can change both the percentage of delay and the base delay to fine-tune the bot’s speed and responsiveness to suit your needs.</p>
""")

        self.add_page("Color Detection Settings", """
    <h3 style="font-size: 20px; font-weight: bold;">What is Color Detection?</h3>
    <p>The bot uses RGB color values to detect specific colors on your screen. This is helpful for automating tasks based on color changes.</p>

    <h4 style="font-size: 18px; font-weight: bold;">How to Use:</h4>
    <ul>
        <li>Set the Red, Green, and Blue (RGB) values to match the color you want the bot to detect.</li>
        <li>Adjust the <strong>Color Tolerance</strong> to allow more or less variation in the color match.</li>
    </ul>

    <p><strong>Note:</strong> A higher tolerance allows for more color variation, while a lower tolerance requires a more exact match.</p>
""")


        # Navigation buttons
        self.button_layout = QtWidgets.QHBoxLayout()
        
        self.next_button = QtWidgets.QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        self.next_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;  /* Rounded corners */
                padding: 10px 20px;   /* Adjust padding to make button bigger */
                font-size: 16px;      /* Increase font size */
                background-color: #4C4C4C; /* Dark button color */
                color: white;         /* White text */
                border: 1px solid #6C6C6C; /* Border matching dark mode */
            }
            QPushButton:hover {
                background-color: #6C6C6C; /* Lighter dark color on hover */
            }
        """)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.next_button)
        
        layout.addLayout(self.button_layout)
        self.setLayout(layout)
        
        self.update_navigation_buttons()  # Set the correct label for the next/close button
        
        self.apply_stylesheet()  # Apply the correct stylesheet based on dark/light mode


    def add_page(self, title, content):
        """
        Adds a page to the stacked widget with a title and rich text content, formatted for better readability.
    
        Args:
            title (str): The title of the tutorial page.
            content (str): The rich text content to display on the page.
        """
        page_widget = QtWidgets.QWidget()
        page_layout = QtWidgets.QVBoxLayout()
    
        # Title of the page with larger font
        label_title = QtWidgets.QLabel(f"<h2 style='font-size: 28px;'>{title}</h2>")
        label_title.setAlignment(QtCore.Qt.AlignCenter)
    
        # Content of the page with larger font for better readability
        label_content = QtWidgets.QLabel(content)
        label_content.setTextFormat(QtCore.Qt.RichText)
        label_content.setWordWrap(True)
        label_content.setAlignment(QtCore.Qt.AlignTop)  # Align to the top for better spacing
        label_content.setStyleSheet("font-size: 16px;")  # Increase font size
    
        page_layout.addWidget(label_title)
        page_layout.addSpacing(10)  # Add space between title and content
        page_layout.addWidget(label_content)
        page_layout.addStretch(1)  # Add stretch to push content upwards, ensuring good spacing
    
        page_widget.setLayout(page_layout)
        self.page_stack.addWidget(page_widget)


    def next_page(self):
        """
        Moves to the next page of the tutorial. If it's the last page, close the window.
        """
        if self.current_page < self.page_stack.count() - 1:
            self.current_page += 1
        else:
            self.close()  # Close if it's the last page

        self.page_stack.setCurrentIndex(self.current_page)
        self.update_navigation_buttons()

    def update_navigation_buttons(self):
        """
        Updates the label of the next button based on the current page.
        """
        if self.current_page == self.page_stack.count() - 1:
            self.next_button.setText("Close")
        else:
            self.next_button.setText("Next")

    def apply_stylesheet(self):
        """
        Applies the correct stylesheet based on whether dark mode is enabled.
        """
        if self.dark_mode:
            self.setStyleSheet("""
                QWidget {
                    background-color: #2E2E2E;
                    color: #FFFFFF;
                }
                QPushButton {
                    background-color: #4C4C4C;
                    color: #FFFFFF;
                    border: 1px solid #6C6C6C;
                }
                QPushButton:hover {
                    background-color: #6C6C6C;
                }
                QLabel {
                    color: #FFFFFF;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #FFFFFF;
                    color: #000000;
                }
                QPushButton {
                    background-color: #E0E0E0;
                    color: #000000;
                    border: 1px solid #B0B0B0;
                }
                QPushButton:hover {
                    background-color: #B0B0B0;
                }
                QLabel {
                    color: #000000;
                }
            """)
            