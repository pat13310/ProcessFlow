from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QBrush, QColor
from PySide6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem
from enum import Enum

class ResizeDirection(Enum):
    V = "vertical"         # V
    H = "horizontal"         # H
    D = "diagonal"          # D


class HandleItem(QGraphicsEllipseItem):
    def __init__(self, x, y, size, color, direction:ResizeDirection, parent=None, min_size=20, max_size=300, maintain_aspect_ratio=False):
        super().__init__(x - size / 2, y - size / 2, size, size, parent)
        self.color = color
        self._size = size
        self.parent_item = parent  # Référence au rectangle parent
        self.setPen(QPen(self.color))
        self.setBrush(QBrush(self.color))
        self.direction = direction  # Direction de redimensionnement
        self.setVisible(False)
        self.setAcceptHoverEvents(True)
        #self.setAcceptedMouseButtons()
        self.cursor = Qt.ArrowCursor
        self.setCursor(self.cursor)
        self.setZValue(2)
        #self.setFlag(QGraphicsItem.ItemIsMovable, True)  # Permettre le déplacement de l'item
        self.min_size = min_size  # Taille minimale du rectangle parent
        self.max_size = max_size  # Taille maximale du rectangle parent
        self.maintain_aspect_ratio = maintain_aspect_ratio  # Conserver le rapport largeur/hauteur

        # Variables pour stocker les dimensions originales pour maintenir le rapport
        self.original_width = self.parent_item.boundingRect().width()
        self.original_height = self.parent_item.boundingRect().height()
        self.aspect_ratio = self.original_width/self.original_height
        self.is_selected=False

    def size(self):
        return float(self._size)


    def hoverEnterEvent(self, event):
        """Changer la couleur des poignées lors du survol."""
        self.setBrush(QBrush(QColor(255, 239, 50, 220)))  # Rouge lors du survol pour plus de visibilité
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        """Revenir à la couleur d'origine après avoir quitté le survol."""
        self.setBrush(QBrush(self.color))  # Retour à la couleur d'origine
        super().hoverLeaveEvent(event)

    def mouseReleaseEvent(self, event):
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.parent_item.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.is_selected=False
        self.parent_item.update_handles()



    def mousePressEvent(self, event):
        self.setCursor(Qt.BlankCursor)
        self.is_selected = True

        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.parent_item.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.prepareGeometryChange()


    def mouseMoveEvent(self, event):
        new_pos = self.parent_item.mapFromScene(event.scenePos())
        rect = self.parent_item.boundingRect()
        center = rect.center()
        if self.is_selected:
            self.setCursor(Qt.BlankCursor)
        else :
            self.setCursor(self.cursor)

        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.prepareGeometryChange()


        if self.direction == ResizeDirection.V:
            dy = abs(new_pos.y() - center.y()) * 2
            new_height = max(self.min_size, min(self.max_size, dy))
            new_top = center.y() - new_height / 2
            self.parent_item.update_geometry(rect.left(), new_top, rect.width(), new_height, self.direction)

        elif self.direction == ResizeDirection.H:
            dx = abs(new_pos.x() - center.x()) * 2
            new_width = max(self.min_size, min(self.max_size, dx))
            new_left = center.x() - new_width / 2
            self.parent_item.update_geometry(new_left, rect.top(), new_width, rect.height(), self.direction)


        elif self.direction == ResizeDirection.D:
            dy = abs(new_pos.y() - center.y()) * 2
            dx = abs(new_pos.x() - center.x()) * 2

            if self.maintain_aspect_ratio:
                self.aspect_ratio = self.original_width / self.original_height
                new_width = max(self.min_size, min(self.max_size, dx))
                new_height = new_width / self.aspect_ratio
            else:
                new_width = max(self.min_size, min(self.max_size, dx))
                new_height = max(self.min_size, min(self.max_size, dy))
                self.aspect_ratio = new_width / new_height

            new_left = center.x() - new_width / 2
            new_top = center.y() - new_height / 2
            self.parent_item.update_geometry(new_left, new_top, new_width, new_height,self.direction)
        self.parent_item.update_handles(False)
        super().mouseMoveEvent(event)