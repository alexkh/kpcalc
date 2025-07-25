window_width = 642 # initial window width
window_height = 922 # initial window height
window_aspect_ratio = window_width / window_height

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QPixmap, QStaticText, QFont, QKeyEvent, QKeySequence
from PyQt6.QtCore import Qt, QPoint, QPointF, QRect, QRectF, QSize, QEvent, QCoreApplication
import sys
import fragments
from asteval import Interpreter
import re
import time

aeval = Interpreter()

mod_keys = [ Qt.Key.Key_Period, Qt.Key.Key_F1, Qt.Key.Key_Plus, Qt.Key.Key_F2,
    Qt.Key.Key_Minus, Qt.Key.Key_F3, Qt.Key.Key_Asterisk, Qt.Key.Key_F4,
    Qt.Key.Key_Slash, Qt.Key.Key_F5 ]

class Canvas(QWidget):
    def __init__(self):
        super().__init__()

        self.mode = 0 # 0 for scientific, 1 for hex
        self.unit = 0 # 0 for radians, 1 for degrees
        self.mod = 0 # active modifier: 1. 2+ 3- 4* 5/
        self.mod_used = False # modifier key has been used, not trigger operator
        self.mod_pressed_ts = 0 # when modifier key was pressed
        self.num_str = "0" # number string
        self.ans_str = "0" # last answer. num_str copied here when Enter pressed
        self.num_appendable = False # set to false after +, -, /, * etc pressed
        self.eval_str = "Welcome to Keypad Calculator!" # evaluation string
        self.eval_appendable = False # set to false after =
        self.show_equals = False # show = after eval_str

        self.aspect_ratio = window_aspect_ratio
        self.setMouseTracking(True)
        self.mouse_pos = QPoint(0, 0)
        self.mouse_key = '6'

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
                QPointF(29, 555),     # target position
                QRectF(2, 514,        # source position (crop from center)
                54, 82),              # source size
                1.0, 1.0,             # scale
                0,                    # no rotation
                1.0                   # full opacity
            ),
        ]

    def fix_eval_str(self):
        if self.eval_str.startswith('W'):
            self.eval_str = ""

    def clear(self): # CLEAR OPERATION when (+ 9) is pressed, for example
        self.eval_str = ""
        self.num_str = "0" if self.mode == 0 else "0x0"
        self.num_appendable = False
        self.eval_appendable = False
        self.show_equals = False

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

        # painter.setFont(QFont("Arial", int(12 * win_scale)))
        # painter.drawText(5, 80, "" + str(self.mouse_pos.x()) +
        #    ", " + str(self.mouse_pos.y()) + " : " + self.mouse_key)

        # draw the eval string:
        painter.setFont(QFont("Arial", int(30 * win_scale)))
        painter.drawText(int(5 * win_scale), int(35 * win_scale), self.eval_str
            + ("=" if self.show_equals == True else ""))

        # draw the big number:
        num_rect = QRect(int(6 * win_scale), int(50 * win_scale),
            int(625 * win_scale), int(60 * win_scale))
        # painter.drawRect(num_rect)
        painter.setFont(QFont("Arial", int(40 * win_scale)))
        painter.drawText(num_rect, Qt.AlignmentFlag.AlignRight, self.num_str)

        painter.end()

    def do_backspace(self):
        self.mod_used = True
        if self.num_str == "0" or self.num_str == "0x0":
            return
        self.num_str = self.num_str[:-1]
        self.update()

    def num_append(self, c):
        print("trying to append " + c)
        if self.num_appendable:
            self.num_str += c
            self.update()
        else:
            if self.num_str == "0" or self.num_str == "0x0":
                if c == "0":
                    return
            if not self.eval_appendable:
                self.clear()
            if self.mode == 1: # in hex mode numbers start with 0x
                self.num_str = aeval("hex(" + c + ")")
            else:
                self.num_str = c
            self.num_appendable = True
            self.update()

    def eval_append(self, s):
        if self.eval_appendable:
            self.eval_str += s
            self.update()
        else:
            self.eval_str = s
            self.update()

    def mouseMoveEvent(self, e):
        self.mouse_pos = e.pos()
        self.update()

    def mousePressEvent(self, e):
        self.mouse_pos = e.pos()
        bg_img_scale = self.width() / fragments.imw
        key = fragments.bg_key(self.mouse_pos, bg_img_scale)

        if key in mod_keys:
            self.mouse_key = QKeySequence(key).toString()
            event = QKeyEvent(QEvent.Type.KeyPress, key,
                Qt.KeyboardModifier.NoModifier)
            QCoreApplication.postEvent(self, event)

    def mouseReleaseEvent(self, e):
        self.mouse_pos = e.pos()
        bg_img_scale = self.width() / fragments.imw
        key = fragments.bg_key(self.mouse_pos, bg_img_scale)
        if key is None:
            return

        if (key in mod_keys) or (self.mod != 0):
            event = QKeyEvent(QEvent.Type.KeyRelease, key,
                Qt.KeyboardModifier.NoModifier)
            QCoreApplication.postEvent(self, event)
        else:
            self.mouse_key = QKeySequence(key).toString()
            event = QKeyEvent(QEvent.Type.KeyPress, key,
                Qt.KeyboardModifier.NoModifier)
            QCoreApplication.postEvent(self, event)

    def key_pressed_dec(self, key):
        match key:
            case Qt.Key.Key_0:
                match self.mod:
                    case 0:
                        self.num_append("0")
                        self.update()
                    case 2:
                        self.do_uop(self.ans_str)
                    case 3:
                        self.do_uop("-(" + self.num_str + ")")
                    case _:
                        self.num_appendable = False
            case Qt.Key.Key_1:
                match self.mod:
                    case 0:
                        self.num_append("1")
                    case 1:
                        self.do_uop("1-" + self.num_str)
                    case 2:
                        self.do_uop(self.num_str + "+1")
                    case 3:
                        self.do_uop(self.num_str + "-1")
                    case 4:
                        self.unit = 1 if self.unit == 0 else 0
                        self.num_appendable = False
                        self.update()
                    case 5:
                        self.do_uop("1/" + self.num_str)
                    case _:
                        self.num_appendable = False
            case Qt.Key.Key_2:
                match self.mod:
                    case 0:
                        self.num_append("2")
                    case 1:
                        self.do_uop("e")
                    case 2:
                        self.do_uop("2*" + self.num_str)
                    case 3:
                        self.do_uop(self.num_str + "/2")
                    case 4:
                        self.do_uop(self.num_str + "**2")
                    case 5:
                        self.do_uop("sqrt(" + self.num_str + ")")
                    case _:
                        self.num_appendable = False
            case Qt.Key.Key_3:
                match self.mod:
                    case 0:
                        self.num_append("3")
                    case 1:
                        self.do_uop("pi")
                    case 2:
                        self.do_uop("3*" + self.num_str)
                    case 3:
                        self.do_uop(self.num_str + "/3")
                    case 4:
                        self.do_uop(self.num_str + "**3")
                    case 5:
                        self.do_uop(self.num_str + "**(1/3)")
                    case _:
                        self.num_appendable = False
            case Qt.Key.Key_4:
                match self.mod:
                    case 0:
                        self.num_append("4")
                    case 3:
                        if self.unit == 0:
                            self.do_uop("sin(" + self.num_str + ")")
                        else:
                            self.do_uop("sin(radians(" + self.num_str + "))")
                    case 4:
                        self.do_op(self.num_str + '**')
                    case 5:
                        self.do_op("100*(" + self.num_str + "/")
                    case _:
                        self.num_appendable = False
            case Qt.Key.Key_5:
                match self.mod:
                    case 0:
                        self.num_append("5")
                    case 2: # 2 operands required for atan2() TODO: degrees
                        self.do_op("atan2(" + self.num_str + ',')
                    case 3:
                        if self.unit == 0:
                            self.do_uop("tan(" + self.num_str + ")")
                        else:
                            self.do_uop("tan(radians(" + self.num_str + "))")
                    case 4:
                        self.do_uop(self.num_str + "!")
                    case _:
                        self.num_appendable = False
            case Qt.Key.Key_6:
                match self.mod:
                    case 0:
                        self.num_append("6")
                    case 1:
                        self.mode = 1 if self.mode == 0 else 0
                        self.num_appendable = False
                        self.update()
                    case 2:
                        if self.num_str.startswith("0x") :
                            self.do_uop("int(" + self.num_str + ")")
                        else:
                            self.do_uop("hex(int(" + self.num_str + "))")
                    case 3:
                        if self.unit == 0:
                            self.do_uop("1/cos(" + self.num_str + ")")
                        else:
                            self.do_uop("1/cos(radians(" + self.num_str + "))")
                    case 5:
                        self.do_uop("log(" + self.num_str + ")/log(2)")
                    case _:
                        self.num_appendable = False
            case Qt.Key.Key_7:
                match self.mod:
                    case 0:
                        self.num_append("7")
                    case _:
                        self.num_appendable = False
            case Qt.Key.Key_8:
                match self.mod:
                    case 0:
                        self.num_append("8")
                    case 2:
                        self.num_append("e")
                        self.mod_used = True
                    case 3:
                        self.num_append("-")
                        self.mod_used = True
                    case 5:
                        self.do_op(self.num_str + '%')
                    case _:
                        self.num_appendable = False
            case Qt.Key.Key_9:
                match self.mod:
                    case 0:
                        self.num_append("9")
                    case 2:
                        self.clear()
                    case 3:
                        self.do_backspace()
                    case 5:
                        self.do_uop("log(" + self.num_str + ")")
                    case _:
                        self.num_appendable = False

    def key_pressed_hex(self, key):
        match key:
            case Qt.Key.Key_0:
                match self.mod:
                    case 0:
                        self.num_append("0")
                    case 1:
                        self.num_append("a")
                    case 2:
                        self.do_uop(self.ans_str)
                    case 3:
                        self.do_uop("hex(-(" + self.num_str + "))")
                    case _:
                        self.num_appendable = False
            case Qt.Key.Key_1:
                match self.mod:
                    case 0:
                        self.num_append("1")
                    case 1:
                        self.num_append("b")
                    case 2:
                        self.do_uop(self.num_str + "+1")
                    case 3:
                        self.do_uop(self.num_str + "-1")
                    case 4:
                        self.do_op(self.num_str + "&")
                    case 5:
                        self.do_op(self.num_str + "|")
                    case _:
                        self.num_appendable = False
            case Qt.Key.Key_2:
                match self.mod:
                    case 0:
                        self.num_append("2")
                    case 1:
                        self.num_append("c")
                    case 2:
                        self.do_uop("2*" + self.num_str)
                    case 3:
                        self.do_uop(self.num_str + "/2")
                    case 4:
                        self.do_uop(self.num_str + "**2")
                    case 5:
                        self.do_uop("sqrt(" + self.num_str + ")")
                    case _:
                        self.num_appendable = False
            case Qt.Key.Key_3:
                match self.mod:
                    case 0:
                        self.num_append("3")
                    case 1:
                        self.num_append("d")
                    case 2:
                        self.do_uop("3*" + self.num_str)
                    case 3:
                        self.do_uop(self.num_str + "/3")
                    case 4:
                        self.do_uop(self.num_str + "**3")
                    case 5:
                        self.do_uop(self.num_str + "**(1/3)")
                    case _:
                        self.num_appendable = False
            case Qt.Key.Key_4:
                match self.mod:
                    case 0:
                        self.num_append("4")
                    case 1:
                        self.num_append("e")
                    case 2:
                        self.do_op(self.num_str + "^")
                    case 3:
                        self.do_uop("~" + self.num_str)
                    case _:
                        self.num_appendable = False
            case Qt.Key.Key_5:
                match self.mod:
                    case 0:
                        self.num_append("5")
                    case 1:
                        self.num_append("f")
                    case 3:
                        if self.unit == 0:
                            self.do_uop("tan(" + self.num_str + ")")
                        else:
                            self.do_uop("tan(radians(" + self.num_str + "))")
                    case 4:
                        self.do_uop(self.num_str + "!")
                    case _:
                        self.num_appendable = False
            case Qt.Key.Key_6:
                match self.mod:
                    case 0:
                        self.num_append("6")
                    case 1:
                        self.mode = 1 if self.mode == 0 else 0
                        self.num_appendable = False
                        self.update()
                    case 2:
                        if self.num_str.startswith("0x") :
                            self.do_uop("int(" + self.num_str + ")")
                        else:
                            self.do_uop("hex(int(" + self.num_str + "))")
                    case 3:
                        if self.unit == 0:
                            self.do_uop("1/cos(" + self.num_str + ")")
                        else:
                            self.do_uop("1/cos(radians(" + self.num_str + "))")
                    case 5:
                        self.do_uop("log(" + self.num_str + ")/log(2)")
                    case _:
                        self.num_appendable = False
            case Qt.Key.Key_7:
                match self.mod:
                    case 0:
                        self.num_append("7")
                    case _:
                        self.num_appendable = False
            case Qt.Key.Key_8:
                match self.mod:
                    case 0:
                        self.num_append("8")
                    case 5:
                        self.do_op(self.num_str + '%')
                    case _:
                        self.num_appendable = False
            case Qt.Key.Key_9:
                match self.mod:
                    case 0:
                        self.num_append("9")
                    case 2:
                        self.clear()
                    case 3:
                        self.do_backspace()
                    case 5:
                        self.do_uop("log(" + self.num_str + ")")
                    case _:
                        self.num_appendable = False

    def keyPressEvent(self, event: QKeyEvent):
        if event.isAutoRepeat():
            return
        # print(event.key())
        self.fix_eval_str()
        match event.key():
            case Qt.Key.Key_Period | Qt.Key.Key_F1:
                self.mod = 1
                self.mod_pressed_ts = time.time()
                self.num_appendable = True
                self.update()
            case Qt.Key.Key_Plus | Qt.Key.Key_F2:
                self.mod = 2
                self.mod_pressed_ts = time.time()
                self.num_appendable = True
                self.update()
            case Qt.Key.Key_Minus | Qt.Key.Key_F3:
                self.mod = 3
                self.mod_pressed_ts = time.time()
                self.num_appendable = True
                self.update()
            case Qt.Key.Key_Asterisk | Qt.Key.Key_F4:
                self.mod = 4
                self.mod_pressed_ts = time.time()
                self.num_appendable = True
                self.update()
            case Qt.Key.Key_Slash | Qt.Key.Key_F5:
                self.mod = 5
                self.mod_pressed_ts = time.time()
                self.num_appendable = True
                self.update()
            case Qt.Key.Key_Enter: # ENTER OPERATION
                if self.show_equals: # repeated enter press: repeat last op
                    self.eval_append(re.sub(r'\d+', str(self.num_str), self.eval_str, count = 1))
                else:
                    self.eval_append(self.num_str)
                # check if there is unclosed left parenthesis
                if self.eval_str.count('(') > self.eval_str.count(')'):
                    self.eval_str += ')'
                if self.mode == 1: # hex mode
                    self.num_str = self.ans_str = str(
                        aeval("hex(" + self.eval_str + ")"))
                else:
                    self.num_str = self.ans_str = str(aeval(self.eval_str))
                self.show_equals = True
                self.eval_appendable = False
                self.num_appendable = False
            case _:
                if self.mode == 0: # dec mode
                    self.key_pressed_dec(event.key())
                else:
                    self.key_pressed_hex(event.key())

    def keyReleaseEvent(self, event: QKeyEvent):
        if event.isAutoRepeat():
            return
        mod_time = time.time() - self.mod_pressed_ts
        mod_only = mod_time > 1.0
        print("time: ", mod_time)
        match event.key():
            case Qt.Key.Key_Period | Qt.Key.Key_F1:
                if self.mod == 1:
                    self.mod = 0
                    if self.mode == 1: # no dot in hex mode
                        self.mod_used = False
                        self.update()
                        return
                    if (self.num_appendable and not self.mod_used
                        and not mod_only):
                        self.mod_used = False
                        if '.' in self.num_str:
                            self.update()
                            return
                        self.num_str += '.'
                    self.mod_used = False
                    self.update()
            case Qt.Key.Key_Plus | Qt.Key.Key_F2:
                if self.mod == 2: # PLUS OPERATION
                    self.mod = 0
                    if (self.num_appendable and not self.mod_used
                        and not mod_only):
                        self.do_op(self.num_str + '+')
                    self.mod_used = False
                    self.update()
            case Qt.Key.Key_Minus | Qt.Key.Key_F3:
                if self.mod == 3: # MINUS OPERATION
                    self.mod = 0
                    if (self.num_appendable and not self.mod_used
                        and not mod_only):
                        self.do_op(self.num_str + '-')
                    self.mod_used = False
                    self.update()
            case Qt.Key.Key_Asterisk | Qt.Key.Key_F4:
                if self.mod == 4: # MULTIPLY OPERATION
                    self.mod = 0
                    if (self.num_appendable and not self.mod_used
                        and not mod_only):
                        self.do_op(self.num_str + '*')
                    self.mod_used = False
                    self.update()
            case Qt.Key.Key_Slash | Qt.Key.Key_F5:
                if self.mod == 5: # DIVIDE OPERATION
                    self.mod = 0
                    if (self.num_appendable and not self.mod_used
                        and not mod_only):
                        self.do_op(self.num_str + '/')
                    self.mod_used = False
                    self.update()

    def do_op(self, op):
        self.mod = 0
        self.eval_append(op)
        self.num_appendable = False
        self.eval_appendable = True
        self.show_equals = False
        self.update()

    def do_uop(self, uop):
        self.num_appendable = False
        self.num_append(str(aeval(uop)))
        self.num_appendable = False
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
