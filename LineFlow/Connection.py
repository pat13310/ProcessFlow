from PySide6.QtWidgets import QGraphicsLineItem
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPen, QCursor, QColor

from DiagramFlow.RectangleShape import RectangleShape
from DiagramFlow.SignalShape import SignalShape


class Connection(QGraphicsLineItem):
    def __init__(self, start_port, end_port=None, line_style='straight', color=Qt.black, width=4):
        super().__init__()
        self.start_port = start_port
        self.end_port = end_port
        self.line_style = line_style
        self.is_drawing = True  # Indique si la connexion est en cours de traçage
        self.setZValue(-1)

        # Couleur et épaisseur par défaut
        self.default_color = color
        self.hover_color = QColor('#C0C0FF')  # Couleur à utiliser au survol
        self.setPen(QPen(self.default_color, width))

        self.signals = SignalShape()
        self.update_position()
        self.setAcceptHoverEvents(True)

    def update_position(self):
        # Mettre à jour la position de la ligne
        if self.start_port:
            start_pos = self.start_port.scenePos()
            if self.end_port:
                end_pos = self.end_port.scenePos()
            else:
                end_pos = self.mapFromScene(self.start_port.scenePos())

            self.setLine(start_pos.x(), start_pos.y() + 5, end_pos.x(), end_pos.y() + 5)

    def get_properties(self):
        if self.start_port is None or self.end_port is None:
            return {}
        item1 = self.start_port.get_parent()
        item2 = self.end_port.get_parent()
        if not isinstance(item1, RectangleShape) and not isinstance(item2, RectangleShape):
            return {}

        return {
            'Type': 'Connection',
            'De': item1.shape_name if item1 else 'Inconnu',
            'Vers': item2.shape_name if item2 and item2 else 'Inconnu',
            'Port de départ': self.start_port.name if self.start_port else 'Inconnu',
            'Port d\'arrivée': self.end_port.name if self.end_port else 'Inconnu',
            'Style de ligne': self.line_style,
            'Couleur': self.pen().color().name(),
            'Épaisseur': self.pen().width()
        }

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.update_position()
            self.signals.propertiesChanged.emit(self.get_properties())

        super().mousePressEvent(event)

    def set_end_port(self, end_port):
        self.end_port = end_port
        self.is_drawing = False
        self.update_position()

    def hoverEnterEvent(self, event):
        """Gérer l'événement quand la souris entre dans le rectangle"""
        self.setPen(QPen(self.hover_color, self.pen().width()))  # Change la couleur de la ligne
        self.setCursor(QCursor(Qt.PointingHandCursor))  # Change le curseur en main
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        """Gérer l'événement quand la souris quitte le rectangle"""
        self.setPen(QPen(self.default_color, self.pen().width()))  # Restaure la couleur d'origine
        self.setCursor(QCursor(Qt.ArrowCursor))  # Restaure le curseur par défaut
        super().hoverLeaveEvent(event)

    def paint(self, painter, option, widget=None):
        """Peindre la ligne avec des effets de survol"""
        super().paint(painter, option, widget)
        # Vous pouvez ajouter d'autres effets de peinture ici si nécessaire
