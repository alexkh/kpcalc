from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QPixmap, QStaticText, QFont
from PyQt6.QtCore import Qt, QPoint, QPointF, QRect, QRectF
import sys

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.mouse_pos = QPoint(0, 0)

        self.bg_sci = QPixmap("img/bg_sci.webp")
        self.bg_hex = QPixmap("img/bg_hex.webp")
        self.bg2_sci = QPixmap("img/bg2_sci.webp")
        self.bg2_hex = QPixmap("img/bg2_hex.webp")

        self.text = "Welcome to Keypad Calculator!"
        self.static_text = QStaticText(self.text)
        self.font = QFont("Arial", 30)
        self.static_text.prepare(font = self.font)

        self.fragments = [
            QPainter.PixmapFragment.create(
                QPointF(29, 555),      # target position
                QRectF(2, 514,        # source position (crop from center)
                54, 82),        # source size
                1.0, 1.0,      # scale
                0,             # no rotation
                1.0            # full opacity
            ),
        ]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.bg2_sci);
        painter.drawPixmapFragments(self.fragments, self.bg_sci)
        painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.PenStyle.SolidLine))
        painter.drawRect(50, 50, 100, 80) # x, y, width, height

        painter.setPen(QPen(QColor(255, 255, 255), 2, Qt.PenStyle.SolidLine))
        painter.setFont(self.font)
        painter.drawStaticText(5, 2, self.static_text)

        painter.setFont(QFont("Arial", 12))
        painter.drawText(5, 80, "" + str(self.mouse_pos.x()) + ", " + str(self.mouse_pos.y()))

        painter.end()

    def mouseMoveEvent(self, e):
        self.mouse_pos = e.pos()
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Canvas()
    window.resize(642, 922)
    window.show()
    sys.exit(app.exec())
