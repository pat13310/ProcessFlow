from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtGui import QBrush, QPen, QColor, QPainter, QFont

from DiagramFlow.SignalShape import SignalShape


class RectangleShape(QGraphicsRectItem):
    GRID_SIZE = 25  # Taille de chaque cellule de la grille

    def __init__(self, x, y, width, height, text):
        super().__init__(x, y, width, height)

        # Instance de SignalShape pour émettre des signaux
        self.signals = SignalShape()

        self.connections = []  # Stocker les connexions associées
        self.text = text
        self.handles = []  # Poignées de sélection

        # Personnalisation de l'apparence de la forme
        self.default_pen = QPen(QColor("#000000"), 1)  # Contour noir par défaut
        self.selected_pen = QPen(QColor("#0000FF"), 1, Qt.DashLine)  # Contour bleu en tirets lorsque sélectionné
        self.current_pen = self.default_pen

        self.default_brush = QBrush(QColor("#FFC8C8"))  # Remplissage par défaut
        self.selected_brush = QBrush(QColor("#C8C8FF"))  # Remplissage lorsque sélectionné
        self.current_brush = self.default_brush

        # Appliquer l'apparence par défaut
        self.setPen(self.current_pen)
        self.setBrush(self.current_brush)

        # Activer les événements et les flags nécessaires
        self.setAcceptHoverEvents(True)  # Gérer les événements de survol
        self.setFlags(QGraphicsRectItem.ItemIsMovable |
                      QGraphicsRectItem.ItemSendsGeometryChanges |
                      QGraphicsRectItem.ItemIsSelectable)  # Permettre le déplacement et la sélection

        # Poignées de sélection (carrés jaunes)
        self.init_handles()

        # Magnétiser le rectangle sur la grille à la création
        self.snap_to_grid()

    def init_handles(self):
        # Crée quatre poignées pour les coins du rectangle
        for i in range(4):
            handle = QGraphicsRectItem(0, 0, 6, 6, self)
            handle.setPen(QPen(QColor("#AFFA00"), 2, Qt.SolidLine))  # Couleur de bordure des poignées en jaune
            handle.setBrush(QBrush(QColor("#FFFF00")))
            handle.setVisible(False)
            self.handles.append(handle)
        self.update_handles()

    def update_handles(self):
        # Positionner les poignées aux quatre coins du rectangle
        rect = self.rect()
        self.handles[0].setPos(rect.topLeft() - QPointF(3, 3))
        self.handles[1].setPos(rect.topRight() - QPointF(3, 3))
        self.handles[2].setPos(rect.bottomLeft() - QPointF(3, 3))
        self.handles[3].setPos(rect.bottomRight() - QPointF(3, 3))

    def paint(self, painter, option, widget=None):
        # Dessiner le rectangle
        painter.setPen(self.current_pen)
        painter.setBrush(self.current_brush)
        painter.drawRect(self.rect())

        # Configurer le style du texte
        painter.setPen(QPen(QColor("#000000")))  # Couleur du texte
        font = QFont()
        font.setBold(True)
        painter.setFont(font)

        # Centrer le texte
        rect = self.rect()
        painter.drawText(rect, Qt.AlignCenter, self.text)

    def set_selected(self, selected):
        # Mettre à jour l'état de sélection et l'apparence
        if selected:
            self.current_pen = self.selected_pen
            self.current_brush = self.selected_brush
            for handle in self.handles:
                handle.setVisible(True)  # Afficher les poignées de sélection

            # Envoyer les propriétés via le signal
            self.emit_properties()
        else:
            self.current_pen = self.default_pen
            self.current_brush = self.default_brush
            for handle in self.handles:
                handle.setVisible(False)  # Masquer les poignées de sélection

        # Appliquer l'apparence mise à jour
        self.setPen(self.current_pen)
        self.setBrush(self.current_brush)

    def emit_properties(self):
        # Émettre les propriétés de l'objet sous forme de dictionnaire
        properties = {
            'Texte': self.text,
            'Position X': self.pos().x(),
            'Position Y': self.pos().y(),
            'Largeur': self.rect().width(),
            'Hauteur': self.rect().height()
        }
        self.signals.propertiesChanged.emit(properties)

    def mousePressEvent(self, event):
        # Gérer l'événement de clic de souris pour sélectionner/désélectionner manuellement
        self.set_selected(not self.is_selected())  # Inverser l'état de sélection
        super().mousePressEvent(event)  # Appeler l'événement de base pour gérer les autres comportements

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.ItemPositionChange:
            # Magnétiser la position sur la grille
            new_pos = value
            snapped_pos = self.snap_to_grid_position(new_pos)

            # Émettre le signal de changement de position avec la nouvelle position
            self.signals.positionChanged.emit(snapped_pos)

            # Mettre à jour les poignées de sélection
            self.update_handles()
            return snapped_pos

        # Si l'état de sélection change, mettre à jour l'apparence
        elif change == QGraphicsRectItem.ItemSelectedChange:
            self.set_selected(value)

        return super().itemChange(change, value)

    def snap_to_grid(self):
        # Magnétiser la position initiale du rectangle sur la grille
        current_pos = self.pos()
        snapped_pos = self.snap_to_grid_position(current_pos)
        self.setPos(snapped_pos)

    def snap_to_grid_position(self, position):
        # Calculer la position magnétisée sur la grille
        snapped_x = round(position.x() / self.GRID_SIZE) * self.GRID_SIZE
        snapped_y = round(position.y() / self.GRID_SIZE) * self.GRID_SIZE
        return QPointF(snapped_x, snapped_y)

    def add_connection(self, connection):
        self.connections.append(connection)

    def remove_connection(self, connection):
        if connection in self.connections:
            self.connections.remove(connection)

    def is_selected(self):
        # Retourner l'état de sélection actuel
        return self.current_pen == self.selected_pen
