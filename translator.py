import sys
import pyperclip
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QComboBox, QPushButton, QProgressBar
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from googletrans import Translator


class QuickTranslator(QWidget):
    def __init__(self):
        super().__init__()
        self.translator = Translator()
        self.previous_clipboard = ""
        self.source_lang = 'en'
        self.target_lang = 'fa'

        self.init_ui()

    def init_ui(self):
        self.setFixedSize(520, 320)
        self.setWindowTitle("Quick Translator ⚡")
        self.set_dark_theme()

        # Layout اصلی
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)

        # عنوان خوش‌آمدگویی
        title = QLabel("Quick Translator")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #00AAFF; margin-bottom: 10px;")
        layout.addWidget(title)

        # کامبوباکس انتخاب زبان
        self.lang_combo = QComboBox()
        self.lang_combo.setFixedHeight(45)
        self.lang_combo.setFont(QFont("Segoe UI", 11))
        self.lang_combo.addItems([
            "English → Persian",
            "Persian → English",
            "Russian → Persian",
            "Russian → English"
        ])
        self.lang_combo.currentIndexChanged.connect(self.update_languages)
        self.lang_combo.setStyleSheet("""
            QComboBox {
                background-color: #2D2D2D;
                border: 2px solid #00AAFF;
                border-radius: 12px;
                padding: 10px;
                color: white;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);  /* می‌تونی یه آیکون بذاری */
                width: 20px;
                height: 20px;
            }
        """)
        layout.addWidget(self.lang_combo)

        # دکمه تعویض سریع زبان
        self.switch_button = QPushButton("🔄 Switch Direction")
        self.switch_button.setFixedHeight(40)
        self.switch_button.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.switch_button.clicked.connect(self.switch_languages)
        self.switch_button.setStyleSheet("""
            QPushButton {
                background-color: #00AAFF;
                color: white;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #0088CC;
            }
        """)
        layout.addWidget(self.switch_button)

        # پروگرس‌بار زیبا
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # حالت indeterminate برای انیمیشن نرم
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #2D2D2D;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background-color: #00FFAA;
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.progress_bar)

        # نمایش متن ترجمه‌شده
        self.label = QLabel("متن انتخابی و کپی‌شده اینجا نمایش داده می‌شود...")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setFont(QFont("Vazir", 12) if self.is_persian() else QFont("Segoe UI", 12))
        self.label.setStyleSheet("""
            QLabel {
                background-color: #1E1E1E;
                border: 2px dashed #444444;
                border-radius: 15px;
                padding: 20px;
                color: #E0E0E0;
                min-height: 100px;
            }
        """)
        layout.addWidget(self.label)

        self.setLayout(layout)

        # تایمر چک کردن کلیپ‌بورد هر ۱ ثانیه
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start(1000)

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(25, 25, 25))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(45, 45, 45))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.Highlight, QColor(0, 170, 255))
        self.setPalette(palette)

    def is_persian(self):
        return self.target_lang == 'fa'

    def update_languages(self):
        idx = self.lang_combo.currentIndex()
        mappings = [(0, 'en', 'fa'), (1, 'fa', 'en'), (2, 'ru', 'fa'), (3, 'ru', 'en')]
        _, self.source_lang, self.target_lang = mappings[idx]
        self.label.setFont(QFont("Vazir", 12) if self.is_persian() else QFont("Segoe UI", 12))

    def switch_languages(self):
        current = self.lang_combo.currentIndex()
        switches = {0: 1, 1: 0, 2: 3, 3: 2}
        self.lang_combo.setCurrentIndex(switches.get(current, current))

    def check_clipboard(self):
        current = pyperclip.paste().strip()
        if current and current != self.previous_clipboard:
            self.previous_clipboard = current
            self.translate_text(current)

    def translate_text(self, text):
        self.progress_bar.setRange(0, 0)  # شروع انیمیشن
        self.label.setText("در حال ترجمه...")
        
        try:
            translated = self.translator.translate(text, src=self.source_lang, dest=self.target_lang)
            self.label.setText(translated.text)
        except Exception as e:
            self.label.setText("⚠️ خطا در ترجمه!\nمتن کوتاه‌تر امتحان کنید یا اینترنت را چک کنید.")
        finally:
            QTimer.singleShot(800, lambda: self.progress_bar.setRange(0, 1))  # پایان انیمیشن


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QuickTranslator()
    window.show()
    sys.exit(app.exec_())
