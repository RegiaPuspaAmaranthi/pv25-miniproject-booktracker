import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtGui import QFont

class BookTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("booktracker.ui", self)
        self.setWindowTitle("Book Tracker")

        self.books = []
        self.selected_row = None

        self.setup_ui()
        self.setup_connections()
        self.show()

    def setup_ui(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #fefefe;
            }
            QPushButton {
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton#addButton {
                background-color: #2196F3; 
                color: white;
            }
            QPushButton#addButton:hover {
                background-color: #1976D2;
            }
            QPushButton#updateButton {
                background-color: #FF9800; 
                color: white;
            }
            QPushButton#updateButton:hover {
                background-color: #FB8C00;
            }
            QPushButton#deleteButton {
                background-color: #F44336; 
                color: white;
            }
            QPushButton#deleteButton:hover {
                background-color: #D32F2F;
            }
            QPushButton#btnStar1, QPushButton#btnStar2, QPushButton#btnStar3, QPushButton#btnStar4, QPushButton#btnStar5 {
                background-color: transparent;
                color: #FFB200;
                font-size: 28px;
                font-family: "Segoe UI Symbol"; 
                border: none;
            }
            QPushButton#btnStar1:hover, QPushButton#btnStar2:hover, QPushButton#btnStar3:hover, QPushButton#btnStar4:hover, QPushButton#btnStar5:hover {
                color: #FFC107;
            }
            QTableWidget {
                background-color: white;
                gridline-color: #ddd;
                font-size: 13px;
                border: 1px solid #ccc;
            }
            QHeaderView::section {
                background-color: #3F51B5;  
                color: white;
                padding: 6px;
                border: 1px solid #3F51B5;
                font-weight: bold;
                font-size: 14px;
                font-family: "Segoe UI"; 
            }        

            QTableWidget::item {
                padding: 6px;
            }
            QTableWidget::item:selected {
                background-color: #B0BEC5; 
                color: black;
            }
            QProgressBar {
                border: 1px solid #bbb;
                border-radius: 6px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #578FCA; 
                width: 12px;
            }
            QComboBox, QSpinBox, QLineEdit, QTextEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 6px;
            }
        """)

        self.totalPagesSpinBox.setMaximum(10000)
        self.lastPageSpinBox.setMaximum(10000)

        self.bookTable.setColumnCount(7)
        self.bookTable.setHorizontalHeaderLabels(["Title", "Author", "Genre", "Total Pages", "Last Page", "Status", "Rating"])

        self.bookTable.horizontalHeader().setStretchLastSection(True)

        self.progressBar.setValue(0)

        self.textEdit.setPlaceholderText("Write your notes or review here...")

        star_buttons = [self.btnStar1, self.btnStar2, self.btnStar3, self.btnStar4, self.btnStar5]
        for btn in star_buttons:
            btn.setFixedSize(40, 40)  


    def setup_connections(self):
        self.addButton.clicked.connect(self.add_book)
        self.updateButton.clicked.connect(self.update_book)
        self.deleteButton.clicked.connect(self.delete_book)
        self.bookTable.cellClicked.connect(self.load_book_to_form)

        self.btnStar1.clicked.connect(lambda: self.set_rating(1))
        self.btnStar2.clicked.connect(lambda: self.set_rating(2))
        self.btnStar3.clicked.connect(lambda: self.set_rating(3))
        self.btnStar4.clicked.connect(lambda: self.set_rating(4))
        self.btnStar5.clicked.connect(lambda: self.set_rating(5))

        self.totalPagesSpinBox.valueChanged.connect(self.update_progress)
        self.lastPageSpinBox.valueChanged.connect(self.update_progress)

    def add_book(self):
        book = self.get_form_data()
        if book:
            self.books.append(book)
            self.refresh_table()
            self.clear_form()
            QMessageBox.information(self, "Success", "Book added successfully!")

    def update_book(self):
        if self.selected_row is not None:
            book = self.get_form_data()
            if book:
                self.books[self.selected_row] = book
                self.refresh_table()
                self.clear_form()
                QMessageBox.information(self, "Success", "Book updated successfully!")

    def delete_book(self):
        if self.selected_row is not None:
            reply = QMessageBox.question(self, 'Confirm Delete', 'Are you sure you want to delete this book?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                del self.books[self.selected_row]
                self.refresh_table()
                self.clear_form()
                QMessageBox.information(self, "Success", "Book deleted successfully!")

    def load_book_to_form(self, row, column):
        self.selected_row = row
        book = self.books[row]
        self.titleLineEdit.setText(book["title"])
        self.authorLineEdit.setText(book["author"])
        self.genreComboBox.setCurrentText(book["genre"])
        self.totalPagesSpinBox.setValue(book["total_pages"])
        self.lastPageSpinBox.setValue(book["last_page"])
        self.textEdit.setPlainText(book["note"])
        self.set_status(book["status"])
        self.set_rating(book["rating"])
        self.update_progress()

    def refresh_table(self):
        self.bookTable.setRowCount(0)
        for book in self.books:
            row_position = self.bookTable.rowCount()
            self.bookTable.insertRow(row_position)
            self.bookTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(book["title"]))
            self.bookTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(book["author"])) 
            self.bookTable.setItem(row_position, 2, QtWidgets.QTableWidgetItem(book["genre"]))
            self.bookTable.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(book["total_pages"])))
            self.bookTable.setItem(row_position, 4, QtWidgets.QTableWidgetItem(str(book["last_page"])))
            self.bookTable.setItem(row_position, 5, QtWidgets.QTableWidgetItem(book["status"]))
            self.bookTable.setItem(row_position, 6, QtWidgets.QTableWidgetItem(str(book["rating"])))

    def clear_form(self):
        self.titleLineEdit.clear()
        self.authorLineEdit.clear()
        self.genreComboBox.setCurrentIndex(0)
        self.totalPagesSpinBox.setValue(0)
        self.lastPageSpinBox.setValue(0)
        self.textEdit.clear()
        self.notStartedCheckBox.setChecked(False)
        self.readingCheckBox.setChecked(False)
        self.finishedCheckBox.setChecked(False)
        self.set_rating(0)
        self.progressBar.setValue(0)
        self.selected_row = None

    def get_form_data(self):
        title = self.titleLineEdit.text()
        author = self.authorLineEdit.text()
        genre = self.genreComboBox.currentText()
        total_pages = self.totalPagesSpinBox.value()
        last_page = self.lastPageSpinBox.value()
        note = self.textEdit.toPlainText()
        status = self.get_status()
        rating = self.get_rating()

        if not title:
            QMessageBox.warning(self, "Warning", "Title cannot be empty!")
            return None
        
        if not author:
            QMessageBox.warning(self, "Warning", "Author cannot be empty!")  
            return None

        return {
            "title": title,
            "author": author,
            "genre": genre,
            "total_pages": total_pages,
            "last_page": last_page,
            "note": note,
            "status": status,
            "rating": rating
        }

    def get_status(self):
        if self.notStartedCheckBox.isChecked():
            return "Not Started"
        elif self.readingCheckBox.isChecked():
            return "Reading"
        elif self.finishedCheckBox.isChecked():
            return "Finished"
        return ""

    def set_status(self, status):
        self.notStartedCheckBox.setChecked(status == "Not Started")
        self.readingCheckBox.setChecked(status == "Reading")
        self.finishedCheckBox.setChecked(status == "Finished")

    def get_rating(self):
        rating = 0
        if self.btnStar1.text() == "★": rating += 1
        if self.btnStar2.text() == "★": rating += 1
        if self.btnStar3.text() == "★": rating += 1
        if self.btnStar4.text() == "★": rating += 1
        if self.btnStar5.text() == "★": rating += 1
        return rating

    def set_rating(self, rating):
        buttons = [self.btnStar1, self.btnStar2, self.btnStar3, self.btnStar4, self.btnStar5]
        for i in range(5):
            buttons[i].setText("★" if i < rating else "☆")

    def update_progress(self):
        total = self.totalPagesSpinBox.value()
        last = self.lastPageSpinBox.value()
        if total > 0:
            progress = min(int((last / total) * 100), 100)
        else:
            progress = 0
        self.progressBar.setValue(progress)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookTracker()
    sys.exit(app.exec_())
