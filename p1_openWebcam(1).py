import sys, time
from itertools import permutations
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QClipboard

STYLE = """
QWidget { background:#0f0f1a; color:#f0f0ff; font-family:Segoe UI; font-size:13px; }
QLineEdit { background:#16213e; border:1px solid #3d3d6b; border-radius:6px; padding:6px; }
QPushButton { background:#7c3aed; border:none; border-radius:6px; padding:10px; font-size:14px; }
QPushButton:hover { background:#6d28d9; }
QListWidget { background:#16213e; border:1px solid #3d3d6b; border-radius:6px; }
QListWidget::item:hover { background:#2d2d5e; }
QListWidget::item:selected { background:#7c3aed; }
QLabel#status { color:#a78bfa; }
QLabel#hint { color:#9ca3af; font-size:11px; }
"""

class AnagramApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ترکیب‌ساز حروف")
        self.setMinimumSize(400, 560)
        self.setStyleSheet(STYLE)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(16, 16, 16, 16)

        title = QLabel("کدراه")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color:#a78bfa")
        layout.addWidget(title)

        layout.addWidget(QLabel("حروف را وارد کنید:"))
        self.letters_input = QLineEdit(placeholderText="مثال: abcde")
        layout.addWidget(self.letters_input)

        layout.addWidget(QLabel("تعداد حروف در هر ترکیب:"))
        self.length_input = QLineEdit(placeholderText="عدد", maximumWidth=80)
        layout.addWidget(self.length_input)

        btn = QPushButton("⚡  تولید ترکیب‌ها")
        btn.clicked.connect(self.generate)
        layout.addWidget(btn)

        self.status = QLabel("آماده")
        self.status.setObjectName("status")
        layout.addWidget(self.status)

        hint = QLabel("کلیک روی هر ترکیب → کپی در کلیپ‌بورد")
        hint.setObjectName("hint")
        layout.addWidget(hint)

        self.result_list = QListWidget()
        self.result_list.itemClicked.connect(
            lambda item: (QApplication.clipboard().setText(item.text()),
                          self.status.setText(f'"{item.text()}" کپی شد'))
        )
        layout.addWidget(self.result_list)

    def generate(self):
        letters = self.letters_input.text().replace(" ", "")
        raw = self.length_input.text().strip()

        if not letters:
            self.status.setText("⚠ حروف وارد نشده"); return
        if not raw.isdigit():
            self.status.setText("⚠ تعداد را عدد وارد کن"); return

        r = int(raw)
        if r < 1 or r > len(letters):
            self.status.setText(f"⚠ عدد بین ۱ تا {len(letters)} باشد"); return

        t0 = time.perf_counter()
        result = sorted(set("".join(p) for p in permutations(letters, r)))
        elapsed = time.perf_counter() - t0

        self.status.setText(f"✦ {len(result):,} ترکیب  |  {elapsed*1000:.1f} ms")
        self.result_list.clear()
        self.result_list.addItems(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AnagramApp()
    w.show()
    sys.exit(app.exec())
