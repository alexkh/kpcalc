window_width = 642 # initial window width
window_height = 922 # initial window height
window_aspect_ratio = window_width / window_height

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QPixmap, QStaticText, QFont, QKeyEvent
from PyQt6.QtCore import Qt, QPoint, QPointF, QRect, QRectF, QSize
import sys
import fragments

class Canvas(QWidget):
    def __init__(self):
        super().__init__()

        self.mode = 0 # 0 for scientific, 1 for hex
        self.unit = 0 # 0 for radians, 1 for degrees
        self.mod = 0 # active modifier: 1. 2+ 3- 4* 5/
        self.num_str = "0" # number string

        self.aspect_ratio = window_aspect_ratio
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
        bg_img_scale = self.width() / fragments.imw
        # only if modifier pressed, highlight the possible choices
        if self.mod == 0:
            painter.drawPixmap(0, 0, self.width(), self.height(),
                self.bg_sci if self.mode == 0 else self.bg_hex)
        else:
            painter.drawPixmap(0, 0, self.width(), self.height(),
                self.bg2_sci if self.mode == 0 else self.bg2_hex)
            painter.drawPixmapFragments(fragments.frag1(self.mode, self.mod,
                bg_img_scale), self.bg_sci if self.mode == 0 else self.bg_hex)

    def paintEvent(self, event):
        win_scale = self.width() / window_width

        painter = QPainter(self)
        self.draw_bg(painter)

        # highlight mode: scientific/hexadecimal
        painter.setPen(QPen(QColor(255, 255, 255), 2, Qt.PenStyle.SolidLine))
        if self.mode == 0: # scientific mode
            painter.drawRect(int(374 * win_scale), int(530 * win_scale),
                int(60 * win_scale), int(27 * win_scale)) # x, y, width, height
        else: # hexadecimal mode
            painter.drawRect(int(374 * win_scale), int(565 * win_scale),
                int(60 * win_scale), int(27 * win_scale)) # x, y, width, height

        # highlight units: radians/degrees
        if self.mode == 0: # units only apply to scientific mode
            if self.unit == 0: # radians units
                painter.drawRect(int(42 * win_scale), int(606 * win_scale),
                    int(60 * win_scale), int(32 * win_scale))
            else: # degrees units
                painter.drawRect(int(42 * win_scale), int(647 * win_scale),
                    int(60 * win_scale), int(32 * win_scale))


        painter.setPen(QPen(QColor(255, 255, 255), 2, Qt.PenStyle.SolidLine))
        painter.setFont(self.font)
        painter.drawStaticText(5, 2, self.static_text)

        painter.setFont(QFont("Arial", int(12 * win_scale)))
        painter.drawText(5, 80, "" + str(self.mouse_pos.x()) +
            ", " + str(self.mouse_pos.y()))

        # draw the big number:
        num_rect = QRect(int(6 * win_scale), int(50 * win_scale),
            int(625 * win_scale), int(60 * win_scale))
        # painter.drawRect(num_rect)
        painter.setFont(QFont("Arial", int(40 * win_scale)))
        painter.drawText(num_rect, Qt.AlignmentFlag.AlignRight, self.num_str)

        painter.end()

    def num_append(self, c):
        if self.num_str == "0":
            if c == "0":
                return
            self.num_str = c
            self.update()
            return
        else:
            self.num_str += c
            self.update()
            return

    def mouseMoveEvent(self, e):
        self.mouse_pos = e.pos()
        self.update()

    def keyPressEvent(self, event: QKeyEvent):
        if event.isAutoRepeat():
            return
        # print(event.key())
        match event.key():
            case Qt.Key.Key_Period | Qt.Key.Key_F1:
                self.mod = 1
                self.update()
            case Qt.Key.Key_Plus | Qt.Key.Key_F2:
                self.mod = 2
                self.update()
            case Qt.Key.Key_Minus | Qt.Key.Key_F3:
                self.mod = 3
                self.update()
            case Qt.Key.Key_Asterisk | Qt.Key.Key_F4:
                self.mod = 4
                self.update()
            case Qt.Key.Key_Slash | Qt.Key.Key_F5:
                self.mod = 5
                self.update()
            case Qt.Key.Key_0:
                match self.mod:
                    case 0:
                        self.num_append("0")
            case Qt.Key.Key_1:
                match self.mod:
                    case 0:
                        self.num_append("1");
                    case 4:
                        self.unit = 1 if self.unit == 0 else 0
                        self.update()
            case Qt.Key.Key_2:
                match self.mod:
                    case 0:
                        self.num_append("2");
            case Qt.Key.Key_3:
                match self.mod:
                    case 0:
                        self.num_append("3");
            case Qt.Key.Key_4:
                match self.mod:
                    case 0:
                        self.num_append("4");
            case Qt.Key.Key_5:
                match self.mod:
                    case 0:
                        self.num_append("5");
            case Qt.Key.Key_6:
                match self.mod:
                    case 0:
                        self.num_append("6");
                    case 1:
                        self.mode = 1 if self.mode == 0 else 0
                        self.update()
            case Qt.Key.Key_7:
                match self.mod:
                    case 0:
                        self.num_append("7");
            case Qt.Key.Key_8:
                match self.mod:
                    case 0:
                        self.num_append("8");
            case Qt.Key.Key_9:
                match self.mod:
                    case 0:
                        self.num_append("9");

    def keyReleaseEvent(self, event: QKeyEvent):
        if event.isAutoRepeat():
            return
        match event.key():
            case Qt.Key.Key_Period | Qt.Key.Key_F1:
                if self.mod == 1:
                    self.mod = 0
                    self.update()
            case Qt.Key.Key_Plus | Qt.Key.Key_F2:
                if self.mod == 2:
                    self.mod = 0
                    self.update()
            case Qt.Key.Key_Minus | Qt.Key.Key_F3:
                if self.mod == 3:
                    self.mod = 0
                    self.update()
            case Qt.Key.Key_Asterisk | Qt.Key.Key_F4:
                if self.mod == 4:
                    self.mod = 0
                    self.update()
            case Qt.Key.Key_Slash | Qt.Key.Key_F5:
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
    app.setKeyboardInputInterval(0)
    window = Canvas()
    window.resize(window_width, window_height)
    window.show()
    sys.exit(app.exec())
