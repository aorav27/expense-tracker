from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QHBoxLayout
)
import sys

class ExpenseTracker(QWidget):
    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 500, 400)

        # Create UI components
        self.label = QLabel("Enter Expense Details:", self)

        # Input fields
        self.expense_name = QLineEdit(self)
        self.expense_name.setPlaceholderText("Expense Name")

        self.expense_amount = QLineEdit(self)
        self.expense_amount.setPlaceholderText("Amount (e.g., 50.00)")

        # Dropdown for category
        self.category_dropdown = QComboBox(self)
        self.category_dropdown.addItems(["Food", "Groceries", "Transport", "Rent", "Entertainment", "Other"])

        # Buttons
        self.add_button = QPushButton("Add Expense", self)
        self.remove_button = QPushButton("Remove Selected", self)

        # Table to display expenses
        self.expense_table = QTableWidget(0, 3, self)
        self.expense_table.setHorizontalHeaderLabels(["Name", "Amount", "Category"])

        # Connect buttons to functions
        self.add_button.clicked.connect(self.add_expense)
        self.remove_button.clicked.connect(self.remove_expense)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.expense_name)
        layout.addWidget(self.expense_amount)
        layout.addWidget(self.category_dropdown)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)

        layout.addLayout(button_layout)
        layout.addWidget(self.expense_table)

        self.setLayout(layout)

    def add_expense(self):
        """Adds a new expense to the table."""
        name = self.expense_name.text().strip()
        amount = self.expense_amount.text().strip()
        category = self.category_dropdown.currentText()

        if name and amount:  # Ensure both fields are filled
            row_position = self.expense_table.rowCount()
            self.expense_table.insertRow(row_position)
            self.expense_table.setItem(row_position, 0, QTableWidgetItem(name))
            self.expense_table.setItem(row_position, 1, QTableWidgetItem(amount))
            self.expense_table.setItem(row_position, 2, QTableWidgetItem(category))

            # Clear inputs after adding
            self.expense_name.clear()
            self.expense_amount.clear()
        else:
            print("Please enter both name and amount.")  # Placeholder error handling

    def remove_expense(self):
        """Removes the selected expense from the table."""
        selected_rows = self.expense_table.selectionModel().selectedRows()
        for row in sorted(selected_rows, reverse=True):  # Reverse order to prevent shifting issues
            self.expense_table.removeRow(row.row())

# Run application
app = QApplication(sys.argv)
window = ExpenseTracker()
window.show()
sys.exit(app.exec())
