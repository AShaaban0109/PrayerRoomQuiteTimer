import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout, QStackedWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import pandas as pd
import datetime

class PrayerTimesApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Prayer Times")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.page1 = QWidget()
        self.page2 = QWidget()

        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)

        self.init_page1()
        self.init_page2()

    def init_page1(self):
        layout = QVBoxLayout(self.page1)
        load_button_layout = QHBoxLayout()
        
        self.load_button = QPushButton("Load CSV", self.page1)
        self.load_button.setFont(QFont("Helvetica", 14))
        self.load_button.setStyleSheet("background-color: #007acc; color: #ffffff;")
        self.load_button.clicked.connect(self.load_csv)
        
        load_button_layout.addWidget(self.load_button)
        layout.addLayout(load_button_layout)

    def init_page2(self):
        layout = QVBoxLayout(self.page2)
        self.message_label = QLabel(self.page2)
        font = QFont()
        font.setFamily("Helvetica")
        font.setPointSize(16)
        self.message_label.setFont(font)
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)

    def update_message(self):
        current_time = datetime.datetime.now().strftime("%H:%M")
        today = datetime.datetime.now().day

        if not self.df.empty:
            for col in self.df.columns:
                for row in range(len(self.df)):
                    prayer_time = self.df.loc[row, col]
                    if row + 1 == today:
                        prayer_datetime = datetime.datetime.strptime(prayer_time, "%H:%M")
                        current_datetime = datetime.datetime.strptime(current_time, "%H:%M")
                        if (
                            prayer_datetime - current_datetime
                            <= datetime.timedelta(minutes=15)
                            and prayer_datetime - current_datetime
                            >= datetime.timedelta(minutes=-15)
                        ):
                            self.message_label.setText(f"Time to keep quiet for {col} prayer!")
                            return

        self.message_label.setText("No prayer time now. You can relax!")

    def load_csv(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select a CSV file", "", "CSV Files (*.csv);;All Files (*)")

        if file_path:
            self.df = pd.read_csv(file_path)
            self.df = self.df.drop("Days", axis=1)
            self.df = self.df.dropna()

            self.stacked_widget.setCurrentWidget(self.page2)  # Switch to page 2
            self.update_message()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PrayerTimesApp()
    window.show()
    sys.exit(app.exec_())
