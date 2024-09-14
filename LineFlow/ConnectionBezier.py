from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsEllipseItem
from PySide6.QtGui import QPen, QColor, QBrush, QPainterPath
from PySide6.QtCore import Qt, QPointF, QObject, Signal

from DiagramFlow.CircleShape import CircleShape
from LineFlow.geometry_calculations import calculate_rectangle_middle_border, calculate_circle_tangent


class ConnectionSignal(QObject):
    propertiesChanged = Signal(dict)  # Signal pour émettre les propriétés


class ConnectionBezier(QGraphicsPathItem):
    MARKER_SIZE = 10  # Taille du marqueur
    MARKER_OFFSET = -MARKER_SIZE / 2  # Décalage du marqueur pour le centrer

    def __init__(self, start_item, end_item, color=Qt.black, width=3):
        super().__init__()

        if not start_item or not end_item:
            raise ValueError("Both start and end items must be provided")

        self.start_item = start_item
        self.end_item = end_item

        self.signals = ConnectionSignal()  # Instance de signal pour les propriétés

        # Personnalisation de l'apparence de la ligne
        self.line_color = color
        self.line_width = width
        self.is_selected = False  # Etat de sélection
        self.update_pen()

        # Enregistrer la connexion dans les objets de départ et d'arrivée
        self.start_item.add_connection(self)
        self.end_item.add_connection(self)

        # Initialiser les marqueurs de connexion avec un remplissage lightgreen et un contour noir
        self.start_point_marker = self.create_marker(QColor('lightgreen'), QColor('black'))
        self.end_point_marker = self.create_marker(QColor('lightgreen'), QColor('black'))

        # Ajouter les marqueurs à la scène initialement
        self.ensure_markers_in_scene()

        # Mettre à jour la position initiale de la connexion
        self.update_position()

        # Activer les événements de souris
        self.setAcceptHoverEvents(True)

        # Connecter les signaux de changement de position des objets connectés
        self.start_item.signals.positionChanged.connect(self.update_position)
        self.end_item.signals.positionChanged.connect(self.update_position)

    def create_marker(self, fill_color, border_color):
        # Créer un marqueur de point de connexion avec un remplissage et un contour personnalisés
        marker = QGraphicsEllipseItem(self.MARKER_OFFSET, self.MARKER_OFFSET, self.MARKER_SIZE, self.MARKER_SIZE, self)
        marker.setBrush(QBrush(fill_color))  # Remplir avec la couleur lightgreen
        marker.setPen(QPen(border_color, 2))  # Contour noir
        marker.setParentItem(self)  # Définir le marqueur comme enfant de la ligne pour qu'il suive automatiquement
        return marker

    def update_pen(self):
        # Mettre à jour les paramètres de l'apparence de la ligne
        pen = QPen(self.line_color, self.line_width)
        pen.setCosmetic(True)
        if self.is_selected:
            pen.setStyle(Qt.DashLine)  # Utiliser une ligne en tirets pour la sélection
        else:
            pen.setStyle(Qt.SolidLine)  # Utiliser une ligne pleine
        self.setPen(pen)

    def update_position(self):
        # Mettre à jour la position de la courbe de Bézier en fonction des positions des formes connectées
        if not self.start_item.scene() or not self.end_item.scene():
            return  # Ne pas effectuer de mise à jour si les éléments ne sont pas dans une scène

        # Calculer les centres des objets de départ et d'arrivée
        start_center = self.start_item.rect().center() + self.start_item.pos()
        end_center = self.end_item.rect().center() + self.end_item.pos()

        # Calculer les points de connexion sur les bords des formes
        start_point = self.calculate_connection_point(self.start_item, end_center)
        end_point = self.calculate_connection_point(self.end_item, start_center)

        # Calculer les points de contrôle pour la courbe de Bézier
        control_point1 = start_point + QPointF((end_point.x() - start_point.x()) / 2, 0)
        control_point2 = end_point + QPointF((start_point.x() - end_point.x()) / 2, 0)

        # Créer le chemin de la courbe de Bézier
        path = QPainterPath()
        path.moveTo(start_point)
        path.cubicTo(control_point1, control_point2, end_point)

        # Mettre à jour le chemin de la courbe
        self.setPath(path)

        # Mettre à jour la position des marqueurs
        self.start_point_marker.setPos(start_point - self.pos())  # Ajuster la position en fonction de la ligne
        self.end_point_marker.setPos(end_point - self.pos())  # Ajuster la position en fonction de la ligne

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

    def setSelected(self, selected):
        self.is_selected = selected
        self.update_pen()

    def mousePressEvent(self, event):
        # Gérer l'événement de clic de souris
        self.is_selected = not self.is_selected  # Inverser l'état de sélection
        self.update_pen()  # Mettre à jour l'apparence de la ligne
        self.emit_properties()  # Émettre les propriétés lors du clic
        super().mousePressEvent(event)

    def hoverEnterEvent(self, event):
        # Changer le curseur lorsqu'on survole la ligne
        self.setCursor(Qt.PointingHandCursor)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        # Rétablir le curseur lorsqu'on quitte la ligne
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(event)

    def emit_properties(self):
        properties = {
            'Type': 'ConnectionBezier',
            'Flux Départ': self.start_item.text,
            'Flux Fin': self.end_item.text,
            #'Color': self.line_color.name(),
            'Epaisseur': self.line_width
        }
        self.signals.propertiesChanged.emit(properties)

