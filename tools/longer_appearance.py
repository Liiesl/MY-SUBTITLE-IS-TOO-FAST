import os
import re
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QMessageBox, QListWidget, QLabel, QComboBox
from PyQt5.QtGui import QFont, QPalette
from assets.modules.config import Config

class LongerAppearanceSRT(QWidget):
    def __init__(self, parent=None, back_callback=None):
        super().__init__(parent)
        self.back_callback = back_callback
        self.setFont(QFont("Inter Regular"))
        self.config = Config()
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        text_size = self.config.get_text_size()
        font_size = {
            "small": 18,
            "default": 26,
            "large": 34,
            "huge": 42
        }.get(text_size, 26)

        # Create a horizontal layout for the back and select files buttons
        button_layout = QHBoxLayout()

        self.back_button = QPushButton("Back to Main Menu")
        self.back_button.clicked.connect(self.back_callback)
        button_layout.addWidget(self.back_button)

        self.file_button = QPushButton("Select Files")
        self.file_button.clicked.connect(self.browse_files)
        button_layout.addWidget(self.file_button)

        layout.addLayout(button_layout)

        self.file_list = QListWidget()
        layout.addWidget(self.file_list)

        # Create a horizontal layout for the dropdown and export button
        dropdown_layout = QHBoxLayout()

        self.seconds_label = QLabel("Add Seconds:")
        dropdown_layout.addWidget(self.seconds_label)

        self.seconds_dropdown = QComboBox()
        self.seconds_dropdown.addItems([str(i) for i in range(1, 6)])
        dropdown_layout.addWidget(self.seconds_dropdown)

        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.export_files)
        dropdown_layout.addWidget(self.export_button)

        layout.addLayout(dropdown_layout)

    def apply_theme(self):
        # Retrieve the current palette colors
        palette = self.parent().palette()
        text_color = palette.color(QPalette.WindowText).name()
        background_color = palette.color(QPalette.Window).name()
        button_color = palette.color(QPalette.Button).name()
        button_text_color = palette.color(QPalette.ButtonText).name()
        highlight_color = palette.color(QPalette.Highlight).name()
        hover_color = palette.color(QPalette.Highlight).darker().name()

        self.setStyleSheet(f"background-color: {background_color};")
        self.file_list.setStyleSheet(f"background-color: {background_color}; color: {text_color};")
        self.seconds_label.setStyleSheet(f"color: {text_color};")
        self.seconds_dropdown.setStyleSheet(f"background-color: {background_color}; color: {text_color};")

        self.back_button.setStyleSheet(f"""
            QPushButton {{
                border: 2px solid {highlight_color};
                color: {button_text_color};
                border-radius: 10px;
                padding: 10px;
                background-color: {button_color};
            }}
            QPushButton:hover {{
                border-color: {hover_color};
                background-color: {hover_color};
            }}
        """)

        self.file_button.setStyleSheet(self.back_button.styleSheet())
        self.export_button.setStyleSheet(self.back_button.styleSheet())

    def browse_files(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Subtitle Files", "", "Subtitle Files (*.srt)")
        if file_paths:
            self.file_list.clear()
            for file_path in file_paths:
                self.file_list.addItem(os.path.basename(file_path))
            self.file_list.file_paths = file_paths

    def export_files(self):
        add_seconds = int(self.seconds_dropdown.currentText())
        file_paths = getattr(self.file_list, 'file_paths', [])
        self.adjust_stop_time_in_files(file_paths, add_seconds)

    def adjust_stop_time_in_files(self, file_paths, add_seconds):
        if not file_paths:
            QMessageBox.critical(self, "Error", "No files selected.")
            return

        converted_files = 0
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    srt_data = file.read()

                def adjust_stop_time(match):
                    stop_time = match.group(2)
                    hours, minutes, seconds, milliseconds = map(int, re.split('[:,]', stop_time))
                    total_seconds = hours * 3600 + minutes * 60 + seconds + add_seconds
                    new_hours = total_seconds // 3600
                    new_minutes = (total_seconds % 3600) // 60
                    new_seconds = total_seconds % 60
                    new_time = f"{new_hours:02}:{new_minutes:02}:{new_seconds:02},{milliseconds:03}"
                    return f"{match.group(1)} --> {new_time}"

                updated_srt = re.sub(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", adjust_stop_time, srt_data)

                save_path, _ = QFileDialog.getSaveFileName(self, "Save Modified File", f"modified_{os.path.basename(file_path)}", "Subtitle Files (*.srt)")
                if save_path:
                    with open(save_path, 'w', encoding='utf-8') as file:
                        file.write(updated_srt)
                    converted_files += 1
                else:
                    print(f"Save operation cancelled for {file_path}")

            except Exception as e:
                print(f"Failed to process {file_path}: {e}")

        if converted_files == 0:
            QMessageBox.information(self, "No Files Converted", "No files were successfully converted.")
        else:
            QMessageBox.information(self, "Success", f"{converted_files} files converted successfully!")
