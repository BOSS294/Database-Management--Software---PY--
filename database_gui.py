import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QComboBox, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import pyqtSlot
from db_connector import DatabaseConnector

class DatabaseViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Database Viewer')
        self.setStyleSheet("background-color: #1c1c1c; color: white;")

        layout = QVBoxLayout()

        self.title = QLabel("Database Connection", self)
        self.title.setFont(QFont("Arial", 20))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        self.host_input = QLineEdit(self)
        self.host_input.setPlaceholderText("Host")
        layout.addWidget(self.host_input)

        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Username")
        layout.addWidget(self.user_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.database_input = QLineEdit(self)
        self.database_input.setPlaceholderText("Database Name")
        layout.addWidget(self.database_input)

        self.connect_button = QPushButton("Connect", self)
        self.connect_button.setStyleSheet("background-color: #333333; color: white; padding: 10px;")
        self.connect_button.clicked.connect(self.connect_to_database)
        layout.addWidget(self.connect_button)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet("QProgressBar::chunk {background-color: #00ff00;}")
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.tables_combo = QComboBox(self)
        self.tables_combo.setStyleSheet("background-color: #333333; color: white; padding: 5px;")
        self.tables_combo.currentIndexChanged.connect(self.load_columns)
        layout.addWidget(self.tables_combo)

        self.table_widget = QTableWidget(self)
        layout.addWidget(self.table_widget)

        self.setLayout(layout)

        self.db = DatabaseConnector()

    @pyqtSlot()
    def connect_to_database(self):
        self.progress_bar.setValue(20)
        QTimer.singleShot(500, self.complete_connection)

    def complete_connection(self):
        connected = self.db.connect(
            self.host_input.text(),
            self.user_input.text(),
            self.password_input.text(),
            self.database_input.text()
        )
        if connected:
            self.progress_bar.setValue(100)
            self.title.setText("Connection Successful")
            self.load_tables()
        else:
            self.progress_bar.setValue(0)
            self.title.setText("Connection Failed")

    def load_tables(self):
        tables = self.db.get_tables()
        self.tables_combo.clear()
        for table in tables:
            self.tables_combo.addItem(table[0])

    def load_columns(self):
        table_name = self.tables_combo.currentText()
        columns = self.db.get_columns(table_name)
        self.table_widget.setColumnCount(len(columns))
        self.table_widget.setHorizontalHeaderLabels([col[0] for col in columns])

        self.load_data(table_name)

    def load_data(self, table_name):
        cursor = self.db.connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        self.table_widget.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                self.table_widget.setItem(i, j, QTableWidgetItem(str(col)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = DatabaseViewer()
    viewer.show()
    sys.exit(app.exec_())
