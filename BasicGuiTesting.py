import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout, QStackedWidget, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
import pandas as pd
import datetime

class PrayerTimesApp(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Prayer Times")
        self.setGeometry(100, 100, 800, 100)

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

        self.prayer_timer = QTimer(self)
        self.prayer_timer.timeout.connect(self.check_prayer_time)
        self.prayer_timer.start(60000)  # Check every minute

    def init_page1(self):
        layout = QVBoxLayout(self.page1)

        font_size_layout = QHBoxLayout()
        self.font_size_label = QLabel("Font Size:", self.page1)
        self.font_size_combobox = QComboBox(self.page1)
        self.font_size_combobox.addItem("12")
        self.font_size_combobox.addItem("16")
        self.font_size_combobox.addItem("20")
        self.font_size_combobox.addItem("24")
        self.font_size_combobox.addItem("28")
        self.font_size_combobox.setCurrentIndex(1)  # Default font size
        font_size_layout.addWidget(self.font_size_label)
        font_size_layout.addWidget(self.font_size_combobox)

        self.load_button = QPushButton("Load CSV", self.page1)
        self.load_button.setFont(QFont("Helvetica", 14))
        self.load_button.setStyleSheet("background-color: #007acc; color: #ffffff;")
        self.load_button.clicked.connect(self.load_csv)

        layout.addLayout(font_size_layout)
        layout.addWidget(self.load_button)

    def init_page2(self):
        layout = QVBoxLayout(self.page2)
        self.message_label = QLabel(self.page2)
        self.message_label.setFont(QFont("Helvetica", 16))
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)

    def check_prayer_time(self):
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
                            self.showNormal()
                            return

        self.message_label.setText("No prayer time now. You can relax!")
        self.showMinimized()

    def load_csv(self):
        self.showNormal()  # Show the app window before loading CSV
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select a CSV file", "", "CSV Files (*.csv);;All Files (*)")

        if file_path:
            self.df = pd.read_csv(file_path)
            self.df = self.df.drop("Days", axis=1)
            self.df = self.df.dropna()

            # Get the selected font size from the ComboBox
            selected_font_size = int(self.font_size_combobox.currentText())

            new_font = QFont("Helvetica", selected_font_size)
            self.message_label.setFont(new_font)

            self.stacked_widget.setCurrentWidget(self.page2)  # Switch to page 2
            self.check_prayer_time()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PrayerTimesApp()
    window.show()
    sys.exit(app.exec_())
