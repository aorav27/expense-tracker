from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QMessageBox, QDateEdit, QFileDialog
)
from PySide6.QtCore import QDate
from PySide6.QtGui import QFont
import sys
import csv
import os
import matplotlib.pyplot as plt
import pandas as pd
import openpyxl


class ExpenseTracker(QWidget):
    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 550, 500)
        self.setStyleSheet("""
                    QWidget {
                        background-color: #2d2d2d;
                        color: #f0f0f0;
                        font-family: Arial, sans-serif;
                        font-size: 14px;
                    }
                    QLabel {
                        font-size: 16px;
                        color: #f0f0f0;
                    }
                    QLineEdit {
                        background-color: #444444;
                        color: #f0f0f0;
                        border: 2px solid #888888;
                        padding: 5px;
                        border-radius: 12px;
                    }
                    QLineEdit:focus {
                        border: 2px solid #5c87b3;
                    }
                    QComboBox {
                        background-color: #444444;
                        color: #f0f0f0;
                        border: 2px solid #888888;
                        padding: 5px;
                        border-radius: 12px;
                    }
                    QPushButton {
                        background-color: #5c87b3;
                        color: #ffffff;
                        border: 2px solid #888888;
                        padding: 8px 16px;
                        border-radius: 12px;
                        font-weight: bold;
                        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3);
                    }
                    QPushButton:hover {
                        background-color: #4c77a3;
                        cursor: pointer;
                    }
                    QPushButton:pressed {
                        background-color: #3c6583;
                    }
                    QTableWidget {
                        border-radius: 10px;
                        background-color: #333333;
                        border: 1px solid #444444;
                    }
                    QTableWidget::item {
                        padding: 8px;
                        border-bottom: 1px solid #444444;
                    }
                    QTableWidget::item:hover {
                        background-color: #444444;
                    }
                    QTableWidget::horizontalHeader {
                        background-color: #555555;
                        font-weight: bold;
                    }
                    QTableWidget::verticalHeader {
                        background-color: #555555;
                    }
                    QDateEdit {
                        background-color: #444444;
                        color: #f0f0f0;
                        border: 2px solid #888888;
                        padding: 5px;
                        border-radius: 12px;
                    }
                """)

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
        self.category_dropdown.addItems(["All", "Income", "Food", "Transport", "Groceries", "Rent", "Entertainment", "Other"])

        # Buttons
        self.add_button = QPushButton("Add Entry", self)
        self.remove_button = QPushButton("Remove Selected", self)
        self.export_button = QPushButton("Export to Excel", self)
        self.graph_button = QPushButton("Show Monthly Balance Graph", self)

        # Expense table
        self.expense_table = QTableWidget(0, 4, self)
        self.expense_table.setHorizontalHeaderLabels(["Date", "Name", "Amount", "Category"])

        # Set font for the table
        font = QFont("Arial", 12)
        self.expense_table.setFont(font)  # Apply font to the table

        # Summary label
        self.total_label = QLabel("Total Expenses: $0.00", self)

        # Button actions
        self.add_button.clicked.connect(self.add_expense)
        self.remove_button.clicked.connect(self.remove_expense)
        self.export_button.clicked.connect(self.export_to_excel)
        self.graph_button.clicked.connect(self.show_graph)

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
        button_layout.addWidget(self.graph_button)

        layout.addLayout(button_layout)
        layout.addWidget(self.expense_table)
        layout.addWidget(self.total_label)

        self.setLayout(layout)

        # Load existing expenses
        self.load_expenses()

    def show_graph(self):
        """Generates a line graph of net balances per month."""
        if not os.path.exists("expenses.csv"):
            self.show_error("No expense data available to generate graph.")
            return

        # Read the data from CSV
        df = pd.read_csv("expenses.csv", names=["Date", "Name", "Amount", "Category"], parse_dates=["Date"])
        df["Amount"] = df["Amount"].astype(float)
        df["Month"] = df["Date"].dt.to_period("M")

        # Classify as income or expense
        df['Amount'] = df.apply(lambda row: row['Amount'] if row['Category'] == "Income" else -row['Amount'], axis=1)

        # Group by month and sum the amounts
        monthly_balance = df.groupby("Month")["Amount"].sum()

        # Plot the graph
        plt.figure(figsize=(8, 5))
        plt.plot(monthly_balance.index.astype(str), monthly_balance.values, marker='o', linestyle='-', color='b',
                 label="Net Balance")
        plt.axhline(0, color='red', linestyle='--')  # Show 0 line for clarity
        plt.xlabel("Month")
        plt.ylabel("Net Balance ($)")
        plt.title("Net Balance Over Time")
        plt.legend()
        plt.grid()
        plt.xticks(rotation=45)
        plt.show()

    def add_expense(self):
        """Adds a new expense or income entry to the table and saves it."""
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

    def save_expense(self, date, name, amount, category):
        """Saves new expense or income to the file."""
        with open("expenses.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date, name, amount, category])

    def load_expenses(self):
        """Loads existing expenses from the file."""
        if os.path.exists("expenses.csv"):
            with open("expenses.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        self.add_expense_from_file(row)

    def add_expense_from_file(self, row):
        """Adds an expense from the CSV file to the table."""
        date, name, amount, category = row
        row_position = self.expense_table.rowCount()
        self.expense_table.insertRow(row_position)
        self.expense_table.setItem(row_position, 0, QTableWidgetItem(date))
        self.expense_table.setItem(row_position, 1, QTableWidgetItem(name))
        self.expense_table.setItem(row_position, 2, QTableWidgetItem(f"${float(amount):.2f}"))
        self.expense_table.setItem(row_position, 3, QTableWidgetItem(category))

    def export_to_excel(self):
        """Exports the table data to an Excel file."""
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Expenses"

        # Set header row
        sheet.append(["Date", "Name", "Amount", "Category"])

        # Add expense data from the table to the Excel sheet
        for row in range(self.expense_table.rowCount()):
            date_item = self.expense_table.item(row, 0)
            name_item = self.expense_table.item(row, 1)
            amount_item = self.expense_table.item(row, 2)
            category_item = self.expense_table.item(row, 3)

            date = date_item.text() if date_item else ""
            name = name_item.text() if name_item else ""
            amount = amount_item.text() if amount_item else ""
            category = category_item.text() if category_item else ""

            sheet.append([date, name, amount, category])

        # Save the Excel file
        filename, _ = QFileDialog.getSaveFileName(self, "Save Excel File", "", "Excel Files (*.xlsx)")
        if filename:
            workbook.save(filename)
            self.show_message("Export Successful", f"Expenses exported to {filename}")
        else:
            self.show_error("Export canceled")

    def update_total(self):
        """Updates the total expenses label."""
        total = 0
        for row in range(self.expense_table.rowCount()):
            amount_item = self.expense_table.item(row, 2)
            if amount_item:
                amount = float(amount_item.text().replace('$', '').replace(',', ''))
                total += amount
        self.total_label.setText(f"Total Expenses: ${total:.2f}")

    def show_message(self, title, message):
        """Displays a success message."""
        QMessageBox.information(self, title, message)

    def show_error(self, message):
        """Displays an error message."""
        QMessageBox.critical(self, "Error", message)

    def remove_expense(self):
        """Removes the selected expense entry from the table and the CSV file."""
        selected_row = self.expense_table.currentRow()
        if selected_row >= 0:  # Ensure a row is selected
            # Get the data from the selected row
            date_item = self.expense_table.item(selected_row, 0)
            date_item = self.expense_table.item(selected_row, 0)
            name_item = self.expense_table.item(selected_row, 1)
            amount_item = self.expense_table.item(selected_row, 2)
            category_item = self.expense_table.item(selected_row, 3)

            if date_item and name_item and amount_item and category_item:
                date = date_item.text()
                name = name_item.text()
                amount = amount_item.text()
                category = category_item.text()

                # Remove the row from the table
                self.expense_table.removeRow(selected_row)

                # Remove the entry from the CSV file
                self.remove_expense_from_file(date, name, amount, category)

                # Update the total expenses
                self.update_total()

    def remove_expense_from_file(self, date, name, amount, category):
        """Removes an expense from the CSV file."""
        if os.path.exists("expenses.csv"):
            # Read the current data
            with open("expenses.csv", "r") as file:
                rows = list(csv.reader(file))

            # Remove the matching row
            rows = [row for row in rows if not (
                    row[0] == date and
                    row[1] == name and
                    row[2].replace('$', '') == amount.replace('$', '') and  # Remove '$' for comparison
                    row[3] == category
            )]

            # Write the updated data back to the CSV file
            with open("expenses.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)

            # Print file contents for debugging
            print("Updated CSV contents:")
            with open("expenses.csv", "r") as file:
                print(file.read())  # You can check if the removed entry is no longer in the file


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseTracker()
    window.show()
    sys.exit(app.exec())
