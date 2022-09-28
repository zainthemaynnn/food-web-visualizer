import math
import sys
from app import Diet, Organism
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Food web visualizer")

    scene = QGraphicsScene()

    organisms = define_organisms()
    arrange(scene, organisms)

    view = QGraphicsView(scene)
    view.setWindowState(Qt.WindowState.WindowMaximized)
    view.show()

    app.exec()


def arrange(scene: QGraphicsScene, organisms: list[Organism]):
    n = len(organisms)
    for i, organism in enumerate(organisms):
        a = 2 * math.pi / n * i
        organism.setPos(
            QPointF(
                (math.cos(a) + 1),
                (math.sin(a) + 1),
            )
            * 320  # type: ignore
        )
        scene.addItem(organism)
        organism.draw_segments()


def define_organisms() -> list[Organism]:
    # TODO
    return []


if __name__ == "__main__":
    main()
