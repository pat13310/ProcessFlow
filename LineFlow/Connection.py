from PySide6.QtWidgets import QGraphicsLineItem
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPen

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
        self.setPen(QPen(color, width))
        self.signals = SignalShape()
        self.update_position()

    def update_position(self):
        # Mettre à jour la position de la ligne
        if self.start_port:
            start_pos = self.start_port.scenePos()
            if self.end_port:
                # Utiliser la position du port de fin si définie
                end_pos = self.end_port.scenePos()
            else:
                # Utiliser la position actuelle de la souris ou du port de départ
                end_pos = self.mapFromScene(self.start_port.scenePos())

            self.setLine(start_pos.x(), start_pos.y()+5, end_pos.x(), end_pos.y()+5)

    def get_properties(self):
        if self.start_port is None or self.end_port is None:
            return {}
        item1=self.start_port.get_parent()
        item2=self.end_port.get_parent()
        if not  isinstance(item1, RectangleShape) and not isinstance(item2, RectangleShape):
            return {

            }
        return {
            'Type': 'Connection',
            'De': item1.text if item1 else 'Inconnu',
            'Vers': item2.text if item2 and item2 else 'Inconnu',
            'Port de départ': self.start_port.name if self.start_port else 'Inconnu',
            'Port d\'arrivée': self.end_port.name if self.end_port else 'Inconnu',
            'Style de ligne': self.line_style,
            'Couleur': self.pen().color().name(),
            'Épaisseur': self.pen().width()
        }

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.is_drawing:
                # Si le traçage est en cours et le port de fin n'est pas encore défini
                self.end_port = self.start_port  # Utiliser temporairement le start_port comme point de fin
                self.update_position()
                self.is_drawing = False  # Arrêter le traçage
            else:
                # Si le traçage est terminé, vérifiez si le port de fin est défini correctement
                if not self.end_port:
                    self.end_port = self.start_port  # Définir le port de fin correct
                self.is_drawing = False  # Assurez-vous que le traçage est désactivé

            # Émettre les propriétés de la connexion
            self.signals.propertiesChanged.emit(self.get_properties())

        # Appeler l'événement de la super classe pour gérer d'autres comportements
        super().mousePressEvent(event)

    def set_end_port(self, end_port):
        # Méthode pour définir explicitement le port de fin
        self.end_port = end_port
        self.is_drawing = False
        self.update_position()
