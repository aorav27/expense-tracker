from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QMessageBox, QDateEdit
)
from PySide6.QtCore import QDate
import sys
import csv
import os

class ExpenseTracker(QWidget):
    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 550, 500)

        # Create UI components
        self.label = QLabel("Enter Expense Details:", self)

        # Input fields
        self.expense_name = QLineEdit(self)
        self.expense_name.setPlaceholderText("Expense Name")

        self.expense_amount = QLineEdit(self)
        self.expense_amount.setPlaceholderText("Amount (e.g., 50.00)")

        # Date selector (default: today)
        self.expense_date = QDateEdit(self)
        self.expense_date.setCalendarPopup(True)
        self.expense_date.setDate(QDate.currentDate())

        # Dropdown for category
        self.category_dropdown = QComboBox(self)
        self.category_dropdown.addItems(["All", "Food", "Transport", "Rent", "Entertainment", "Other"])

        # Buttons
        self.add_button = QPushButton("Add Expense", self)
        self.remove_button = QPushButton("Remove Selected", self)
        self.export_button = QPushButton("Export to Excel", self)

        # Expense table
        self.expense_table = QTableWidget(0, 4, self)
        self.expense_table.setHorizontalHeaderLabels(["Date", "Name", "Amount", "Category"])

        # Summary label
        self.total_label = QLabel("Total Expenses: $0.00", self)

        # Filter dropdown
        self.filter_dropdown = QComboBox(self)
        self.filter_dropdown.addItems(["All", "Food", "Transport", "Rent", "Entertainment", "Other"])
        self.filter_dropdown.currentIndexChanged.connect(self.filter_expenses)

        # Button actions
        self.add_button.clicked.connect(self.add_expense)
        self.remove_button.clicked.connect(self.remove_expense)
        self.export_button.clicked.connect(self.export_to_excel)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.expense_name)
        layout.addWidget(self.expense_amount)
        layout.addWidget(self.expense_date)
        layout.addWidget(self.category_dropdown)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.export_button)

        layout.addLayout(button_layout)
        layout.addWidget(self.expense_table)
        layout.addWidget(self.total_label)
        layout.addWidget(QLabel("Filter by Category:", self))
        layout.addWidget(self.filter_dropdown)

        self.setLayout(layout)

        # Load existing expenses
        self.load_expenses()

    def add_expense(self):
        """Adds a new expense to the table and saves it."""
        name = self.expense_name.text().strip()
        amount = self.expense_amount.text().strip()
        date = self.expense_date.date().toString("yyyy-MM-dd")
        category = self.category_dropdown.currentText()

        if not name or not amount:
            self.show_error("Both Name and Amount fields are required!")
            return

        try:
            amount = float(amount)  # Validate amount
        except ValueError:
            self.show_error("Amount must be a valid number!")
            return

        # Add to table
        row_position = self.expense_table.rowCount()
        self.expense_table.insertRow(row_position)
        self.expense_table.setItem(row_position, 0, QTableWidgetItem(date))
        self.expense_table.setItem(row_position, 1, QTableWidgetItem(name))
        self.expense_table.setItem(row_position, 2, QTableWidgetItem(f"${amount:.2f}"))
        self.expense_table.setItem(row_position, 3, QTableWidgetItem(category))

        # Save expense
        self.save_expense(date, name, amount, category)
        self.update_total()

        # Clear inputs
        self.expense_name.clear()
        self.expense_amount.clear()

    def remove_expense(self):
        """Removes selected expenses and updates the file."""
        selected_rows = self.expense_table.selectionModel().selectedRows()
        if not selected_rows:
            self.show_error("No expense selected for removal!")
            return

        for row in sorted(selected_rows, reverse=True):
            self.expense_table.removeRow(row.row())

        self.save_all_expenses()
        self.update_total()

    def save_expense(self, date, name, amount, category):
        """Saves new expense to the file."""
        with open("expenses.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date, name, amount, category])

    def load_expenses(self):
        """Loads expenses from the file."""
        if not os.path.exists("expenses.csv"):
            return

        with open("expenses.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 4:
                    date, name, amount, category = row
                    row_position = self.expense_table.rowCount()
                    self.expense_table.insertRow(row_position)
                    self.expense_table.setItem(row_position, 0, QTableWidgetItem(date))
                    self.expense_table.setItem(row_position, 1, QTableWidgetItem(name))
                    self.expense_table.setItem(row_position, 2, QTableWidgetItem(f"${float(amount):.2f}"))
                    self.expense_table.setItem(row_position, 3, QTableWidgetItem(category))

        self.update_total()

    def save_all_expenses(self):
        """Saves all expenses after removals."""
        with open("expenses.csv", "w", newline="") as file:
            writer = csv.writer(file)
            for row in range(self.expense_table.rowCount()):
                date = self.expense_table.item(row, 0).text()
                name = self.expense_table.item(row, 1).text()
                amount = self.expense_table.item(row, 2).text().replace("$", "")
                category = self.expense_table.item(row, 3).text()
                writer.writerow([date, name, amount, category])

    def export_to_excel(self):
        """Exports expenses to an Excel file."""
        try:
            import pandas as pd
            data = []

            for row in range(self.expense_table.rowCount()):
                date = self.expense_table.item(row, 0).text()
                name = self.expense_table.item(row, 1).text()
                amount = self.expense_table.item(row, 2).text().replace("$", "")
                category = self.expense_table.item(row, 3).text()
                data.append([date, name, amount, category])

            df = pd.DataFrame(data, columns=["Date", "Name", "Amount", "Category"])
            df.to_excel("expenses.xlsx", index=False)

            QMessageBox.information(self, "Export Successful", "Expenses have been exported to 'expenses.xlsx'.")
        except ImportError:
            self.show_error("Pandas is not installed. Run 'pip install pandas' to enable export.")

    def update_total(self):
        """Calculates and updates total expenses."""
        total = sum(float(self.expense_table.item(row, 2).text().replace("$", "")) for row in range(self.expense_table.rowCount()))
        self.total_label.setText(f"Total Expenses: ${total:.2f}")

    def filter_expenses(self):
        """Filters expenses by category."""
        selected_category = self.filter_dropdown.currentText()
        for row in range(self.expense_table.rowCount()):
            match = selected_category == "All" or self.expense_table.item(row, 3).text() == selected_category
            self.expense_table.setRowHidden(row, not match)

# Run application
app = QApplication(sys.argv)
window = ExpenseTracker()
window.show()
sys.exit(app.exec())