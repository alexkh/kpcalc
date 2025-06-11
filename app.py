from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QPixmap, QStaticText, QFont, QKeyEvent
from PyQt6.QtCore import Qt, QPoint, QPointF, QRect, QRectF, QSize
import sys
import fragments

class Canvas(QWidget):
    def __init__(self):
        super().__init__()

        self.mode = 0 # 0 for scientific, 1 for hex
        self.mod = 0 # active modifier: 1. 2+ 3- 4* 5/

        self.aspect_ratio = 642 / 922
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

    def draw_bg(self, painter):
        size = self.size()
        scale = size.width() / fragments.imw
        # only if modifier pressed, highlight the possible choices
        if self.mod == 0:
            painter.drawPixmap(0, 0, self.width(), self.height(),
                self.bg_sci if self.mode == 0 else self.bg_hex)
        else:
            painter.drawPixmap(0, 0, self.width(), self.height(),
                self.bg2_sci if self.mode == 0 else self.bg2_hex)
            painter.drawPixmapFragments(fragments.frag1(self.mode, self.mod,
                scale), self.bg_sci if self.mode == 0 else self.bg_hex)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_bg(painter)

        #painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.PenStyle.SolidLine))
        #painter.drawRect(50, 50, 100, 80) # x, y, width, height

        painter.setPen(QPen(QColor(255, 255, 255), 2, Qt.PenStyle.SolidLine))
        painter.setFont(self.font)
        painter.drawStaticText(5, 2, self.static_text)

        painter.setFont(QFont("Arial", 12))
        painter.drawText(5, 80, "" + str(self.mouse_pos.x()) +
            ", " + str(self.mouse_pos.y()))

        painter.end()

    def mouseMoveEvent(self, e):
        self.mouse_pos = e.pos()
        self.update()

    def keyPressEvent(self, event: QKeyEvent):
        match event.key():
            case Qt.Key.Key_Period:
                self.mod = 1
                self.update()
            case Qt.Key.Key_Plus:
                self.mod = 2
                self.update()
            case Qt.Key.Key_Minus:
                self.mod = 3
                self.update()
            case Qt.Key.Key_Asterisk:
                self.mod = 4
                self.update()
            case Qt.Key.Key_Slash:
                self.mod = 5
                self.update()

    def keyReleaseEvent(self, event: QKeyEvent):
        match event.key():
            case Qt.Key.Key_Period:
                if self.mod == 1:
                    self.mod = 0
                    self.update()
            case Qt.Key.Key_Plus:
                if self.mod == 2:
                    self.mod = 0
                    self.update()
            case Qt.Key.Key_Minus:
                if self.mod == 3:
                    self.mod = 0
                    self.update()
            case Qt.Key.Key_Asterisk:
                if self.mod == 4:
                    self.mod = 0
                    self.update()
            case Qt.Key.Key_Slash:
                if self.mod == 5:
                    self.mod = 0
                    self.update()

    def resizeEvent(self, event):
        # Get the new size
        new_size = event.size()
        width = new_size.width()
        height = new_size.height()

        # Calculate what the height should be based on width
        target_height = int(width / self.aspect_ratio)

        # Calculate what the width should be based on height
        target_width = int(height * self.aspect_ratio)

        # Choose the smaller dimension to fit within current size
        if target_height <= height:
            # Width is the limiting factor
            final_width = width
            final_height = target_height
        else:
            # Height is the limiting factor
            final_width = target_width
            final_height = height

        # Only resize if different from current size
        if final_width != width or final_height != height:
            self.resize(final_width, final_height)

        super().resizeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Canvas()
    window.resize(642, 922)
    window.show()
    sys.exit(app.exec())
