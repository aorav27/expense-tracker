from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
import sys

class ExpenseTracker(QWidget):
    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 400, 300)

        # Create UI components
        self.label = QLabel("Welcome to the Expense Tracker!", self)
        self.button = QPushButton("Click Me", self)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseTracker()
    window.show()
    sys.exit(app.exec())
