"""this is internal stuff. don't worry about it. unless you want to worry about it. --zain"""

from enum import Enum
import math
import typing
import urllib.request

from PyQt6.QtCore import (
    QLineF,
    QPoint,
    QPointF,
    QRect,
    QSize,
    Qt,
)
from PyQt6.QtGui import (
    QBrush,
    QFont,
    QPen,
    QPixmap,
    QPolygonF,
    QRegion,
)
from PyQt6.QtWidgets import (
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsPixmapItem,
    QGraphicsPolygonItem,
    QGraphicsTextItem,
)

Organism = typing.TypeVar("TOrganism", bound="Organism")


def vec_from_angle(a: float) -> QPointF:
    return QPointF(math.cos(a), math.sin(a))


class Segment(QGraphicsLineItem):
    rpen = QPen(Qt.GlobalColor.red)
    rpen_bold = QPen(Qt.GlobalColor.red, 4.0)
    arrow_brush = QBrush(Qt.GlobalColor.red, Qt.BrushStyle.SolidPattern)

    def __init__(self, predator: Organism, prey: Organism):
        super().__init__(QLineF())
        self.setPen(self.rpen_bold)
        self.setZValue(1.0)

        self.predator = predator
        self.prey = prey

        points = []
        for i in range(3):
            points.append(vec_from_angle(2 * math.pi / 3 * i) * 8.0)  # type: ignore
        self.arrowhead = QGraphicsPolygonItem(QPolygonF(points), self)
        self.arrowhead.setPen(self.rpen)
        self.arrowhead.setBrush(self.arrow_brush)

        self.update()

    def update_line(self):
        self.dirn = self.prey.pos() - self.predator.pos()  # type: ignore
        udirn = self.dirn / math.sqrt(
            math.pow(self.dirn.x(), 2) + math.pow(self.dirn.y(), 2)
        )
        self.setLine(
            QLineF(self.predator.pos() + udirn * 64.0, self.prey.pos() - udirn * 64.0)
        )

    def update(self):
        self.update_line()
        self.update_arrowhead()

    def update_arrowhead(self):
        self.arrowhead.setPos(self.line().p2())
        self.arrowhead.setRotation(
            math.degrees(math.atan2(self.dirn.y(), self.dirn.x()))
        )


class Diet(Enum):
    OTHER = 1
    HERBIVORE = 2
    OMNIVORE = 3
    CARNIVORE = 4


class Organism(QGraphicsPixmapItem):
    ksize = QSize(128, 128)
    ktext_scale = 2.0
    kmask = QRegion(QRect(QPoint(), ksize), QRegion.RegionType.Ellipse)

    def __init__(self, name: str, diet: Diet, img: str):
        pixmap = QPixmap()
        if img.find("http") > -1:
            req = urllib.request.Request(
                img,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
                },
            )
            data = urllib.request.urlopen(req).read()
            pixmap.loadFromData(data)
        else:
            pixmap.load(img)
        pixmap = pixmap.scaled(self.ksize)

        super().__init__(pixmap)

        ofst = self.pos() - QPointF(self.ksize.width() / 2, self.ksize.height() / 2)  # type: ignore

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setOffset(ofst)

        self.predators: list[Segment] = []
        self.prey: list[Segment] = []

        text = QGraphicsTextItem(name, self)
        if diet == diet.OTHER:
            color = Qt.GlobalColor.white
        elif diet == diet.HERBIVORE:
            color = Qt.GlobalColor.green
        elif diet == diet.OMNIVORE:
            color = Qt.GlobalColor.blue
        elif diet == diet.CARNIVORE:
            color = Qt.GlobalColor.red
        text.setDefaultTextColor(color)
        font = QFont("Roboto", 18, 2)
        font.setBold(True)
        text.setFont(font)
        text.moveBy(ofst.x(), ofst.y())

    def consume(self, organism: Organism):
        s = Segment(self, organism)
        self.prey.append(s)
        organism.predators.append(s)

    def draw_segments(self):
        for s in self.prey:
            self.scene().addItem(s)

    def update_segments(self):
        for s in self.predators:
            s.update()
        for s in self.prey:
            s.update()

    def setPos(self, pos: QPointF):
        super().setPos(pos)
        self.update_segments()

    def mouseMoveEvent(self, event: "QGraphicsSceneMouseEvent"):  # type: ignore
        super().mouseMoveEvent(event)
        self.update_segments()
