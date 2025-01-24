from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget, QApplication
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt
import os

class ChangelogWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("What's New")
        self.setGeometry(300, 200, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)
        
        self.apply_palette()
        self.load_changelog()

    def apply_palette(self):
        palette = QApplication.instance().palette()
        text_color = palette.color(QPalette.WindowText).name()
        background_color = palette.color(QPalette.Window).name()
        
        self.setStyleSheet(f"background-color: {background_color}; color: {text_color};")
        self.text_edit.setStyleSheet(f"background-color: {background_color}; color: {text_color};")

    def load_changelog(self):
        changelog_path = os.path.join(os.path.dirname(__file__), 'changelog.txt')
        try:
            with open(changelog_path, 'r') as file:
                content = file.read()
                self.text_edit.setPlainText(content)
        except FileNotFoundError:
            self.text_edit.setPlainText("Changelog file not found.")
