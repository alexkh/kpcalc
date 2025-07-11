from PyQt6.QtGui import QPainter, QColor, QPen, QPixmap, QStaticText, QFont
from PyQt6.QtCore import Qt, QPoint, QPointF, QRect, QRectF

imw = 1284 # background image width
imh = 1844 # background image height
fw = 54 # fragment's half width
fh = 82 # fragment's half height

fw2 = fw * 2
fh2 = fh * 2

frags = [
    [
        [(4, 710, 54), (345, 710, 36), (655, 710, 48),
        (4, 1034, 54), (350, 1034, 36), (660, 1034, 48),
        (4, 1350, 50), (345, 1350, 44), (655, 1350, 48),
        (4, 1670, 50)],

        [(112, 700, 46), (424, 700, 44), (744, 700, 54),
        (112, 1028, 54), (424, 1028, 54), (744, 1028, 54),
        (108, 1356, 54), (425, 1356, 54), (744, 1356, 54),
        (108, 1670, 50)],

        [(210, 700, 54), (530, 700, 54), (852, 700, 54),
        (224, 1028, 44), (530, 1028, 54), (854, 1028, 52),
        (210, 1356, 54), (530, 1356, 54), (852, 1356, 54),
        (505, 1670, 64)],

        [(210, 568, 54), (530, 568, 54), (852, 568, 54),
        (214, 886, 52), (524, 886, 52), (854, 886, 52),
        (210, 1204, 54), (542, 1204, 44), (864, 1204, 44),
        (505, 1530, 64)],

        [(108, 568, 54), (454, 568, 44), (744, 568, 54),
        (108, 886, 52), (424, 886, 48), (764, 886, 46),
        (100, 1204, 56), (454, 1204, 44), (774, 1204, 44),
        (320, 1530, 64)],

        [(4, 568, 54), (350, 568, 56), (660, 568, 54),
        (4, 886, 52), (340, 886, 46), (660, 886, 46),
        (4, 1204, 40), (350, 1204, 54), (670, 1204, 54),
        (4, 1530, 64)]

    ],
    [
        [(4, 710, 54), (345, 710, 36), (655, 710, 48),
        (4, 1034, 54), (350, 1034, 36), (660, 1034, 48),
        (4, 1350, 50), (345, 1350, 44), (655, 1350, 48),
        (4, 1670, 50)],

        [(112, 700, 46), (424, 700, 44), (744, 700, 54),
        (112, 1028, 46), (424, 1028, 54), (744, 1028, 54),
        (108, 1356, 50), (425, 1356, 54), (744, 1356, 54),
        (108, 1670, 50)],

        [(210, 700, 54), (530, 700, 54), (852, 700, 54),
        (204, 1028, 58), (530, 1028, 54), (854, 1028, 52),
        (210, 1356, 54), (530, 1356, 54), (852, 1356, 54),
        (505, 1670, 64)],

        [(210, 568, 54), (530, 568, 54), (852, 568, 54),
        (228, 886, 46), (524, 886, 52), (854, 886, 52),
        (210, 1204, 54), (542, 1204, 44), (864, 1204, 44),
        (505, 1530, 64)],

        [(108, 568, 54), (454, 568, 44), (744, 568, 54),
        (108, 886, 58), (424, 886, 48), (764, 886, 46),
        (100, 1204, 56), (444, 1204, 44), (774, 1204, 44),
        (320, 1530, 64)],

        [(4, 568, 54), (350, 568, 56), (660, 568, 54),
        (4, 886, 52), (340, 886, 46), (660, 886, 46),
        (4, 1204, 40), (330, 1204, 54), (670, 1204, 54),
        (4, 1530, 64)]

    ],
]

def frag1(mode, mod, sc):
    fragments = []
    for fx, fy, w in frags[mode][mod]:
        fragments.append(QPainter.PixmapFragment.create(
            QPointF((fx + w) * sc, (fy + fh) * sc), # target position
            QRectF(fx, fy, # source position (crop from center)
            w * 2, fh2),   # source size
            sc, sc,        # scale
            0,             # no rotation
            1.0            # full opacity
        ))
    return fragments

# convert background image coordinates to key value
def bg_key(pos, sc):
    x = pos.x() / sc
    y = pos.y() / sc

    if y < 240.0:
        return None

    if x < 360.0:
        if y < 560.0:
            return None
        if y < 880.0:
            return Qt.Key.Key_7
        if y < 1200.0:
            return Qt.Key.Key_4
        if y < 1520.0:
            return Qt.Key.Key_1
        else:
            return Qt.Key.Key_0

    elif x < 642.0:
        if y < 560.0:
            return Qt.Key.Key_Slash
        if y < 880.0:
            return Qt.Key.Key_8
        if y < 1200.0:
            return Qt.Key.Key_5
        if y < 1520.0:
            return Qt.Key.Key_2
        else:
            return Qt.Key.Key_0

    elif x < 962.0:
        if y < 560.0:
            return Qt.Key.Key_Asterisk
        if y < 880.0:
            return Qt.Key.Key_9
        if y < 1200.0:
            return Qt.Key.Key_6
        if y < 1520.0:
            return Qt.Key.Key_3
        else:
            return Qt.Key.Key_Period

    else:
        if y < 560.0:
            return Qt.Key.Key_Minus
        if y < 1200.0:
            return Qt.Key.Key_Plus
        else:
            return Qt.Key.Key_Enter

    return None

