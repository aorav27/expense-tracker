from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
import sys

# Create the application instance
app = QApplication(sys.argv)

# Create the main window
window = QWidget()
window.setWindowTitle("Expense Tracker")
window.setGeometry(100, 100, 400, 300)

# Create a label and a button
label = QLabel("Welcome to the Expense Tracker!", window)
button = QPushButton("Click Me", window)

# Set up layout
layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(button)
window.setLayout(layout)

# Show the window
window.show()
sys.exit(app.exec())