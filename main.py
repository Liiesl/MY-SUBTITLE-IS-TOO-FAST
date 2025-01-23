import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QScrollArea, QMessageBox, QListWidget, QListWidgetItem
from PyQt5.QtGui import QPalette, QColor, QFont, QPainter, QPolygon, QIcon, QPixmap  # Import QPixmap
from PyQt5.QtCore import Qt, QPoint
from tools.subtitle_converter import SubtitleConverter
from settings import Settings  # Import the Settings class

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SRT Editor")
        self.setGeometry(100, 100, 800, 400)
        self.setStyleSheet("background-color: #2c2f38;")

        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.side_page = None

        self.main_menu()

    def main_menu(self):
        # Clear the central widget layout
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Add safe area around the edges
        self.layout.setContentsMargins(100, 100, 100, 100)

        # Create a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget(scroll)
        scroll_layout = QHBoxLayout(scroll_content)
        scroll.setWidget(scroll_content)

        self.layout.addWidget(scroll)

        # Add tool buttons
        tools = [
            ("Longer Appearance SRT", "Increase the duration each subtitle appears."),
            ("Merge SRT Files", "Combine multiple SRT files into one."),
            ("Subtitle Converter", "Convert subtitles between different formats."),
            ("Coming Soon", "New tools will be added here.")
        ]

        for tool in tools:
            scroll_layout.addWidget(self.create_tool_button(tool[0], tool[1]))

        scroll_layout.addStretch()

        # Add triangle button
        triangle_button = QPushButton()
        triangle_button.setFixedSize(50, 50)
        triangle_button.setIcon(self.create_triangle_icon())
        triangle_button.setIconSize(triangle_button.size())
        triangle_button.setStyleSheet("border: none; background: transparent;")
        triangle_button.clicked.connect(self.show_side_page)
        self.layout.addWidget(triangle_button, alignment=Qt.AlignTop | Qt.AlignLeft)

    def create_tool_button(self, tool_name, tool_description):
        button = QPushButton()
        button.setStyleSheet("""
            QPushButton {
                border: 2px solid #4f86f7;
                color: white;
                border-radius: 10px;
                padding: 10px;
                min-width: 150px;
                min-height: 200px;
                margin: 10px;
                background-color: #4f86f7;
                text-align: center;
            }
            QPushButton:hover {
                border-color: #3a6dbf;
                background-color: #3a6dbf;
            }
        """)

        name_label = QLabel(tool_name)
        name_label.setFont(QFont("Arial", 18, QFont.Bold))
        name_label.setStyleSheet("color: #4f86f7;")
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignCenter)

        description_label = QLabel(tool_description)
        description_label.setFont(QFont("Arial", 12))
        description_label.setStyleSheet("color: white;")
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)

        button_layout = QVBoxLayout(button)
        button_layout.addWidget(name_label)
        button_layout.addWidget(description_label)

        button.clicked.connect(lambda: self.tool_selected(tool_name))
        return button

    def tool_selected(self, tool_name):
        if tool_name == "Longer Appearance SRT":
            from tools.longer_appearance import LongerAppearanceSRT
            self.load_tool(LongerAppearanceSRT)
        elif tool_name == "Merge SRT Files":
            from tools.merge_srt import MergeSRT
            self.load_tool(MergeSRT)
        elif tool_name == "Subtitle Converter":
            self.load_tool(SubtitleConverter)
        else:
            QMessageBox.information(self, "Coming Soon", "This feature is coming soon!")

    def load_tool(self, tool_class):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        tool_widget = tool_class(parent=self.central_widget, back_callback=self.main_menu)
        self.layout.addWidget(tool_widget)
        tool_widget.show()

    def create_triangle_icon(self):
        pixmap = QPixmap(50, 50)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setBrush(Qt.black)
        points = [QPoint(25, 5), QPoint(5, 45), QPoint(45, 45)]
        triangle = QPolygon(points)
        painter.drawPolygon(triangle)
        painter.end()
        return QIcon(pixmap)

    def show_side_page(self):
        if self.side_page is None:
            self.side_page = SidePage(self)
        self.side_page.show()

class SidePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Side Page")
        self.setGeometry(0, 0, 200, 400)
        self.setStyleSheet("background-color: #2c2f38;")
        
        layout = QVBoxLayout(self)

        # Add list of clickable texts
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # Add settings item
        settings_item = QListWidgetItem("Settings")
        self.list_widget.addItem(settings_item)

        # Connect item click to the corresponding function
        self.list_widget.itemClicked.connect(self.handle_item_clicked)

    def handle_item_clicked(self, item):
        if item.text() == "Settings":
            self.parent().settings_window = Settings(self)
            self.parent().settings_window.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(44, 47, 56))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(44, 47, 56))
    palette.setColor(QPalette.AlternateBase, QColor(66, 69, 79))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(44, 47, 56))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(75, 110, 175))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
