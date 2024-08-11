import sys
import pyperclip
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QComboBox, QPushButton, QProgressBar
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPalette, QColor

from googletrans import Translator

class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.translator = Translator()
        self.previous_clipboard = ""
        self.source_lang = 'en'
        self.target_lang = 'fa'
        self.initUI()

    def initUI(self):
        self.setFixedSize(500, 250)
        self.set_dark_theme()

        # Main layout
        self.layout = QVBoxLayout()

        # Language selection combo box
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("English to Persian")
        self.lang_combo.addItem("Persian to English")
        self.lang_combo.addItem("Russian to Persian")
        self.lang_combo.addItem("Russian to English")
        self.lang_combo.currentIndexChanged.connect(self.update_languages)
        self.layout.addWidget(self.lang_combo)

        # Button to switch languages
        self.switch_button = QPushButton("Switch Languages", self)
        self.switch_button.clicked.connect(self.switch_languages)
        self.layout.addWidget(self.switch_button)

        # Progress bar for translation
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.layout.addWidget(self.progress_bar)

        # Label to display translation
        self.label = QLabel('Matn Entekhabi inja namayesh dade mishe', self)
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)
        
        self.setWindowTitle('Quick Translator')

        # Timer to check clipboard
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start(1000)

    def set_dark_theme(self):
        palette = QPalette()

        palette.setColor(QPalette.Window, QColor(40, 40, 40)) 
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))  
        palette.setColor(QPalette.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.AlternateBase, QColor(40, 40, 40))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255)) 
        palette.setColor(QPalette.Button, QColor(50, 50, 50)) 
        palette.setColor(QPalette.ButtonText, QColor(200, 200, 200)) 
        palette.setColor(QPalette.Highlight, QColor(0, 128, 255)) 
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

        self.setPalette(palette)

    def update_languages(self):
        index = self.lang_combo.currentIndex()
        if index == 0:
            self.source_lang = 'en'
            self.target_lang = 'fa'
        elif index == 1:
            self.source_lang = 'fa'
            self.target_lang = 'en'
        elif index == 2:
            self.source_lang = 'ru'
            self.target_lang = 'fa'
        elif index == 3:
            self.source_lang = 'ru'
            self.target_lang = 'en'

    def switch_languages(self):
        index = self.lang_combo.currentIndex()
        if index == 0:
            self.lang_combo.setCurrentIndex(1)
        elif index == 1:
            self.lang_combo.setCurrentIndex(0)
        elif index == 2:
            self.lang_combo.setCurrentIndex(3)
        elif index == 3:
            self.lang_combo.setCurrentIndex(2)

    def check_clipboard(self):
        current_clipboard = pyperclip.paste()
        if current_clipboard != self.previous_clipboard:
            self.previous_clipboard = current_clipboard
            self.translate_text()

    def translate_text(self):
        text = pyperclip.paste()
        if text:
            self.progress_bar.setValue(50)  
            try:
                translated_text = self.translator.translate(text, src=self.source_lang, dest=self.target_lang).text
                self.label.setText(translated_text)
            except Exception as e:
                self.label.setText("ERROR. Dobare talash konid { matn kotah tar}.")
            self.progress_bar.setValue(100)  
            QTimer.singleShot(500, lambda: self.progress_bar.setValue(0)) 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TranslatorApp()
    ex.show()
    sys.exit(app.exec_())
