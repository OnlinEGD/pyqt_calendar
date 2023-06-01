from PyQt5.QtCore import QDate
from calendar_1 import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QColorDialog, QListWidgetItem
import sqlite3
from PyQt5.QtGui import QColor

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.calendarWidget.clicked[QDate].connect(self.selected_date)
        self.pushButton.clicked.connect(self.set_event)
        self.pushButton_2.clicked.connect(self.get_events)
        self.pushButton_3.clicked.connect(self.show_color_dialog)
        self.pushButton_4.clicked.connect(self.sort_events)
        self.listWidget.itemClicked.connect(self.delete_item)
        self.selected_date_str = ""
        self.color = "#ffffff"

    def selected_date(self, date):
        self.selected_date_str = date.toString("yyyy-MM-dd")

    def set_event(self):
        conn = sqlite3.connect('pyqt_calendar.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_name TEXT,
                event_date DATE,
                color TEXT
            )''')
        sql = "INSERT INTO events (event_name, event_date, color) VALUES (?, ?, ?)"
        if isinstance(self.color, str):
            values = (self.lineEdit.text(), self.selected_date_str, self.color)
        else:
            values = (self.lineEdit.text(), self.selected_date_str, self.color.name())
        cursor.execute(sql, values)
        conn.commit()
        conn.close()

    def get_events(self):
        conn = sqlite3.connect('pyqt_calendar.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_name TEXT,
                event_date DATE,
                color TEXT
            )''')
        cursor.execute("SELECT * FROM events")
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        self.listWidget.clear()
        for row in rows:
            event_item = QListWidgetItem()
            event_item.setText('  '.join(str(element) for element in row[0:3]))
            color = row[3]
            event_item.setForeground(QColor(color))
            self.listWidget.addItem(event_item)


    def delete_item(self, item):
        id = int(tuple(item.text().split())[0])
        message_box = QMessageBox()
        message_box.setWindowTitle("Okno decyzyjne")
        message_box.setText("Czy jesteś pewien, że chcesz usunąć zdarzenie?")
        message_box.setIcon(QMessageBox.Question)
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message_box.setDefaultButton(QMessageBox.No)

        result = message_box.exec_()
        if result == QMessageBox.Yes:
            conn = sqlite3.connect('pyqt_calendar.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM events WHERE id=?", (id,))
            conn.commit()
            conn.close()
            self.listWidget.removeItemWidget(item)
            self.listWidget.takeItem(self.listWidget.row(item))
        else:
            pass

    def show_color_dialog(self):
        self.color = QColorDialog.getColor()

    def sort_events(self):
        conn = sqlite3.connect('pyqt_calendar.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_name TEXT,
                event_date DATE,
                color TEXT
            )''')
        cursor.execute("SELECT * FROM events ORDER BY event_date")
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        self.listWidget.clear()
        for row in rows:
            print(row)
            event_item = QListWidgetItem()
            event_item.setText('  '.join(str(element) for element in row[0:3]))
            color = row[3]
            event_item.setForeground(QColor(color))
            self.listWidget.addItem(event_item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
