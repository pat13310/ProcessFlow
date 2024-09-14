from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsEllipseItem
from PySide6.QtGui import QPen, QColor
from PySide6.QtCore import Qt, QPointF
from geometry_calculations import calculate_rectangle_middle_border, calculate_circle_tangent


class ConnectionLine(QGraphicsLineItem):
    def __init__(self, start_item, end_item):
        super().__init__()

        self.start_item = start_item
        self.end_item = end_item

        # Utiliser un QPen pour la ligne
        pen = QPen(Qt.black, 2)
        pen.setCosmetic(True)  # Optionnel
        self.setPen(pen)

        # Enregistrer la connexion
        self.start_item.connections.append(self)
        self.end_item.connections.append(self)

        # Initialiser les marqueurs
        self.start_point_marker = self.create_marker(QColor('blue'))
        self.end_point_marker = self.create_marker(QColor('blue'))

        # Mettre à jour la position de la ligne et des marqueurs
        self.update_position()

    def create_marker(self, color):
        marker = QGraphicsEllipseItem(-3, -3, 6, 6)  # (x, y, width, height)
        marker.setBrush(color)
        marker.setPen(Qt.NoPen)  # Pas de contour
        return marker

    def update_position(self):
        start_center = self.start_item.rect().center() + self.start_item.pos()
        end_center = self.end_item.rect().center() + self.end_item.pos()

        # Calculer les points de connexion
        if isinstance(self.start_item, CircleShape):
            start_point = calculate_circle_tangent(start_center, self.start_item.rect().width() / 2, end_center)
        else:  # Rectangle par défaut
            start_point = calculate_rectangle_middle_border(self.start_item.rect(), self.start_item.pos(), end_center)

        if isinstance(self.end_item, CircleShape):
            end_point = calculate_circle_tangent(end_center, self.end_item.rect().width() / 2, start_center)
        else:  # Rectangle par défaut
            end_point = calculate_rectangle_middle_border(self.end_item.rect(), self.end_item.pos(), start_center)

        # Mettre à jour la ligne
        self.setLine(start_point.x(), start_point.y(), end_point.x(), end_point.y())

        # Mettre à jour la position des marqueurs
        self.start_point_marker.setPos(start_point)
        self.end_point_marker.setPos(end_point)
