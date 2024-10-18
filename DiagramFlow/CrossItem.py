from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QBrush, QColor
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsItem


class CrossItem(QGraphicsEllipseItem):
    def __init__(self, x, y, size, color, parent=None):
        super().__init__(x - size / 2, y - size / 2, size, size, parent)
        self.color = color
        self.size = size
        self.x = x
        self.y = y
        self.setPen(QPen(self.color))
        self.setBrush(QBrush(self.color))
        self.setVisible(False)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsRectItem.ItemIsMovable, False)
        self.original_rect = self.boundingRect()  # Stocker le rectangle original


    def hoverEnterEvent(self, event):
        color = QColor(50, 200, 0, 160)
        pen=QPen(color)
        pen.setWidth(10)
        self.setPen(pen)
        self.setBrush(QBrush(color))
        if self.parentItem() is not None:
            self.parentItem().setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setCursor(Qt.ArrowCursor)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        # Revenir à la couleur et la taille d'origine après avoir quitté le survol
        self.setPen(QPen(self.color))
        self.setBrush(QBrush(self.color))


        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if self.parentItem() is not None:
             self.parentItem().setFlag(QGraphicsItem.ItemIsSelectable, False)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.parentItem() is not None:
            self.parentItem().setFlag(QGraphicsItem.ItemIsSelectable, True)
        super().mouseReleaseEvent(event)

