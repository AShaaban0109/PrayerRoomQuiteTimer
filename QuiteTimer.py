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
        # Set the "always on top" window flag
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)


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

        timer_before_prayer_layout = QHBoxLayout()
        self.timer_before_prayer_label = QLabel("Timer before prayer (mins):", self.page1)
        self.timer_before_prayer_combobox = QComboBox(self.page1)
        self.timer_before_prayer_combobox.addItem("5")
        self.timer_before_prayer_combobox.addItem("10")
        self.timer_before_prayer_combobox.addItem("15")
        self.timer_before_prayer_combobox.addItem("20")
        self.timer_before_prayer_combobox.addItem("25")
        self.timer_before_prayer_combobox.addItem("30")
        self.timer_before_prayer_combobox.setCurrentIndex(1)  # Default font size
        timer_before_prayer_layout.addWidget(self.timer_before_prayer_label)
        timer_before_prayer_layout.addWidget(self.timer_before_prayer_combobox)

        timer_after_prayer_layout = QHBoxLayout()
        self.timer_after_prayer_label = QLabel("Timer after prayer (mins):", self.page1)
        self.timer_after_prayer_combobox = QComboBox(self.page1)
        self.timer_after_prayer_combobox.addItem("5")
        self.timer_after_prayer_combobox.addItem("10")
        self.timer_after_prayer_combobox.addItem("15")
        self.timer_after_prayer_combobox.addItem("20")
        self.timer_after_prayer_combobox.addItem("25")
        self.timer_after_prayer_combobox.addItem("30")
        self.timer_after_prayer_combobox.setCurrentIndex(1)  # Default font size
        timer_after_prayer_layout.addWidget(self.timer_after_prayer_label)
        timer_after_prayer_layout.addWidget(self.timer_after_prayer_combobox)


        self.load_button = QPushButton("Load CSV", self.page1)
        self.load_button.setFont(QFont("Helvetica", 14))
        self.load_button.setStyleSheet("background-color: #007acc; color: #ffffff;")
        self.load_button.clicked.connect(self.load_csv)

        layout.addLayout(font_size_layout)
        layout.addLayout(timer_before_prayer_layout)
        layout.addLayout(timer_after_prayer_layout)
        layout.addWidget(self.load_button)
        

    def init_page2(self):


        layout = QVBoxLayout(self.page2)
        
        message_layout = QHBoxLayout()
        self.message_label = QLabel(self.page2)
        self.message_label.setFont(QFont("Helvetica", 16))
        self.message_label.setAlignment(Qt.AlignCenter)
        message_layout.addWidget(self.message_label)

        timer_layout = QHBoxLayout()
        self.timer_label = QLabel(self.page2)
        self.timer_label.setFont(QFont("Helvetica", 16))
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setText("0")
        timer_layout.addWidget(self.timer_label)

        layout.addLayout(message_layout)
        layout.addLayout(timer_layout)

        self.prayer_timer = QTimer(self)
        self.prayer_timer.timeout.connect(self.check_prayer_time)
        
        self.auto_minimize_timer_active = False


    def minimizeTimer(self, seconds_till_minimize = 5000):
        self.auto_minimize_timer = QTimer(self)
        self.auto_minimize_timer.setSingleShot(True)
        self.auto_minimize_timer.timeout.connect(self.minimizeWindow)
        self.auto_minimize_timer.start(seconds_till_minimize)  # 5000 milliseconds (5 seconds)
        self.auto_minimize_timer_active = True

    def minimizeWindow(self):
        self.showMinimized()

    def restoreWindow(self):
        self.setWindowState(Qt.WindowActive)
        self.showNormal()
        self.auto_minimize_timer = False

    # def check_prayer_time(self):
    #     current_time = datetime.datetime.now().strftime("%H:%M")
    #     today = datetime.datetime.now().day
    #     timer_before_prayer = int(self.timer_before_prayer_combobox.currentText())
    #     timer_after_prayer = int(self.timer_after_prayer_combobox.currentText())

    #     if not self.df.empty:
    #         for col in self.df.columns:
    #             for row in range(len(self.df)):
    #                 prayer_time = self.df.loc[row, col]
    #                 if row + 1 == today:
    #                     prayer_datetime = datetime.datetime.strptime(prayer_time, "%H:%M")
    #                     current_datetime = datetime.datetime.strptime(current_time, "%H:%M")
    #                     time_till_prayer = prayer_datetime - current_datetime
                        
    #                     if (time_till_prayer<= datetime.timedelta(minutes= timer_before_prayer)
    #                         and time_till_prayer >= datetime.timedelta(minutes= -timer_after_prayer)):

    #                         if self.auto_minimize_timer_active == True:
    #                             self.restoreWindow()
                            

    #                         self.message_label.setText(f"Time to keep quiet for {col} prayer!")
    #                         self.timer_label.setText(str(prayer_datetime - current_datetime))
    #                         return

    #     self.message_label.setText("No prayer time now. You can relax!")
    #     if self.auto_minimize_timer_active == False:
    #         self.minimizeTimer()

    def check_prayer_time(self):
        current_time = datetime.datetime.now()
        today = current_time.day
        timer_before_prayer = int(self.timer_before_prayer_combobox.currentText())
        timer_after_prayer = int(self.timer_after_prayer_combobox.currentText())

        if not self.df.empty:
            for col in self.df.columns:
                for row in range(len(self.df)):
                    prayer_time = self.df.loc[row, col]
                    if row + 1 == today:
                        prayer_datetime = datetime.datetime(current_time.year, current_time.month, current_time.day,
                                                        int(prayer_time.split(':')[0]), int(prayer_time.split(':')[1]))
                        time_till_prayer = prayer_datetime - current_time

                        if (time_till_prayer <= datetime.timedelta(minutes=timer_before_prayer) and
                                time_till_prayer >= datetime.timedelta(minutes=-timer_after_prayer)):

                            if self.auto_minimize_timer_active == True:
                                self.restoreWindow()
                                self.timer_label.show()


                            minutes, seconds = divmod(time_till_prayer.total_seconds(), 60)
                            self.message_label.setText(f"Time to keep quiet for {col} prayer!")
                            if minutes > 0 and seconds > 0:
                                self.timer_label.setText(f"{int(minutes)} minutes and {int(seconds)} seconds")
                            else:
                                self.timer_label.setText(f"{int(abs(-timer_after_prayer - minutes))} minutes and {int(seconds)} seconds")
                            return

        self.message_label.setText("No prayer time now. You can relax!")
        if self.auto_minimize_timer_active == False:
            self.minimizeTimer()
            self.timer_label.hide()




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
            self.prayer_timer.start(1000)  # Check every second

            new_font = QFont("Helvetica", selected_font_size)
            self.message_label.setFont(new_font)

            self.stacked_widget.setCurrentWidget(self.page2)  # Switch to page 2
            self.check_prayer_time()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PrayerTimesApp()
    window.show()
    sys.exit(app.exec_())
