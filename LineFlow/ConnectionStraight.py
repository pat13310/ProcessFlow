from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsEllipseItem
from PySide6.QtGui import QPen, QColor
from PySide6.QtCore import Qt, QPointF

from DiagramFlow.CircleShape import CircleShape
from LineFlow.geometry_calculations import calculate_rectangle_middle_border, calculate_circle_tangent

class ConnectionStraight(QGraphicsLineItem):
    def __init__(self, start_item, end_item, color=Qt.black, width=2, dashed=False):
        super().__init__()

        if not start_item or not end_item:
            raise ValueError("Both start and end items must be provided")

        self.start_item = start_item
        self.end_item = end_item

        # Personnalisation de l'apparence de la ligne
        self.line_color = color
        self.line_width = width
        self.dashed = dashed
        self.update_pen()

        # Enregistrer la connexion dans les objets de départ et d'arrivée
        self.start_item.add_connection(self)
        self.end_item.add_connection(self)

        # Initialiser les marqueurs de connexion
        self.start_point_marker = self.create_marker(QColor('red'))
        self.end_point_marker = self.create_marker(QColor('red'))

        # Mettre à jour la position initiale de la connexion
        self.update_position()

    def create_marker(self, color):
        # Créer un marqueur de point de connexion
        marker = QGraphicsEllipseItem(-3, -3, 6, 6)
        marker.setBrush(color)
        marker.setPen(Qt.NoPen)
        return marker

    def update_pen(self):
        # Mettre à jour les paramètres de l'apparence de la ligne
        pen = QPen(self.line_color, self.line_width)
        pen.setCosmetic(True)
        if self.dashed:
            pen.setStyle(Qt.DashLine)  # Style pointillé pour la ligne
        self.setPen(pen)

    def update_position(self):
        # Mettre à jour la position de la ligne droite en fonction des positions des formes connectées
        if not self.start_item.scene() or not self.end_item.scene():
            return  # Ne pas effectuer de mise à jour si les éléments ne sont pas dans une scène

        # Calculer les centres des objets de départ et d'arrivée
        start_center = self.start_item.rect().center() + self.start_item.pos()
        end_center = self.end_item.rect().center() + self.end_item.pos()

        # Calculer les points de connexion sur les bords des formes
        start_point = self.calculate_connection_point(self.start_item, end_center)
        end_point = self.calculate_connection_point(self.end_item, start_center)

        # Mettre à jour la ligne droite entre les points de connexion
        self.setLine(start_point.x(), start_point.y(), end_point.x(), end_point.y())

        # Assurer que les marqueurs sont ajoutés à la scène si nécessaire
        self.ensure_markers_in_scene()

        # Mettre à jour la position des marqueurs
        self.start_point_marker.setPos(start_point)
        self.end_point_marker.setPos(end_point)

    def calculate_connection_point(self, item, target_point):
        # Calculer le point de connexion sur le bord de l'objet en fonction de la forme
        item_center = item.rect().center() + item.pos()
        if isinstance(item, CircleShape):
            # Calculer la tangente du cercle pour le point de connexion
            return calculate_circle_tangent(item_center, item.rect().width() / 2, target_point)
        else:
            # Calculer le point sur le bord du rectangle
            return calculate_rectangle_middle_border(item.rect(), item.pos(), target_point)

    def ensure_markers_in_scene(self):
        # Ajouter les marqueurs à la scène s'ils n'y sont pas déjà
        if self.scene():
            if self.start_point_marker.scene() is None:
                self.scene().addItem(self.start_point_marker)
            if self.end_point_marker.scene() is None:
                self.scene().addItem(self.end_point_marker)

    def remove(self):
        # Déconnecter les signaux de position
        self.start_item.remove_connection(self)
        self.end_item.remove_connection(self)

        # Supprimer les marqueurs de la scène
        if self.start_point_marker.scene():
            self.scene().removeItem(self.start_point_marker)
        if self.end_point_marker.scene():
            self.scene().removeItem(self.end_point_marker)

        # Se supprimer de la scène
        if self.scene():
            self.scene().removeItem(self)

    def set_color(self, color):
        # Mettre à jour la couleur de la ligne
        self.line_color = color
        self.update_pen()

    def set_width(self, width):
        # Mettre à jour la largeur de la ligne
        self.line_width = width
        self.update_pen()

    def set_dashed(self, dashed):
        # Définir si la ligne est pointillée ou pleine
        self.dashed = dashed
        self.update_pen()
