import sys
import time
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import pygame

class StretchReminderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stretch Reminder")
        self.setGeometry(100, 100, 400, 200)
        self.setStyleSheet("background-color: #2E3440; color: #D8DEE9;")

        # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Timer label
        self.timer_label = QLabel("Set Timer (minutes):")
        self.timer_label.setStyleSheet("font-size: 14px;")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.timer_label)

        # Timer input
        self.timer_entry = QLineEdit()
        self.timer_entry.setPlaceholderText("Enter minutes")
        self.timer_entry.setStyleSheet(
            "font-size: 14px; background-color: #3B4252; color: #ECEFF4; border: 1px solid #4C566A; padding: 5px;"
        )
        self.layout.addWidget(self.timer_entry)

        # Add sound button
        self.add_sound_button = QPushButton("Select Alert Sound")
        self.add_sound_button.setStyleSheet(
            "font-size: 12px; background-color: #4C566A; color: #ECEFF4; border: none; padding: 10px;"
        )
        self.add_sound_button.clicked.connect(self.select_sound)
        self.layout.addWidget(self.add_sound_button)

        # Start button
        self.start_button = QPushButton("Start Timer")
        self.start_button.setStyleSheet(
            "font-size: 14px; background-color: #5E81AC; color: #ECEFF4; border: none; padding: 10px;"
        )
        self.start_button.clicked.connect(self.start_timer)
        self.layout.addWidget(self.start_button)

        # Stop button
        self.stop_button = QPushButton("Stop Timer")
        self.stop_button.setStyleSheet(
            "font-size: 14px; background-color: #BF616A; color: #ECEFF4; border: none; padding: 10px;"
        )
        self.stop_button.clicked.connect(self.stop_timer)
        self.layout.addWidget(self.stop_button)

        # Current sound file
        self.sound_file = None
        self.sound_label = QLabel("No sound selected")
        self.sound_label.setStyleSheet("font-size: 10px; color: #D08770;")
        self.sound_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.sound_label)

        # Timer thread control
        self.running = False

    def select_sound(self):
        self.sound_file, _ = QFileDialog.getOpenFileName(
            self, "Select Alert Sound", "", "Audio Files (*.mp3 *.wav)"
        )
        if self.sound_file:
            self.sound_label.setText(f"Sound selected: {self.sound_file.split('/')[-1]}")
            self.sound_label.setStyleSheet("color: #A3BE8C;")
        else:
            self.sound_label.setText("No sound selected")
            self.sound_label.setStyleSheet("color: #D08770;")

    def start_timer(self):
        try:
            minutes = float(self.timer_entry.text())
            if minutes <= 0:
                raise ValueError("Time must be positive.")

            self.timer_entry.setText("Running...")
            self.running = True
            threading.Thread(target=self.run_timer, args=(minutes,), daemon=True).start()
        except ValueError:
            QMessageBox.critical(self, "Invalid Input", "Please enter a valid number of minutes.")

    def stop_timer(self):
        self.running = False
        self.timer_entry.setText("Stopped")

    def run_timer(self, minutes):
        while self.running:
            time.sleep(minutes * 60)  # Convert minutes to seconds

            if not self.running:
                break

            # Alert user
            QMessageBox.information(self, "Time to Stretch!", "It's time to get up and stretch!")
            self.play_sound()

    def play_sound(self):
        if self.sound_file:
            pygame.mixer.init()
            pygame.mixer.music.load(self.sound_file)
            pygame.mixer.music.play()

if __name__ == "__main__":
    pygame.init()
    app = QApplication(sys.argv)
    window = StretchReminderApp()
    window.show()
    sys.exit(app.exec_())
