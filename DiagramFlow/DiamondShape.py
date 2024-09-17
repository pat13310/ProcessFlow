from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import QGraphicsPolygonItem
from PySide6.QtGui import QBrush, QPen, QColor, QPolygonF
from DiagramFlow.SignalShape import SignalShape  # Assurez-vous que SignalShape est bien importé

class DiamondShape(QGraphicsPolygonItem):
    GRID_SIZE = 25  # Taille de chaque cellule de la grille

    def __init__(self, x, y, width, height, text, default_color=QColor("#FFC8C8"), selected_color=QColor("#C8C8FF")):
        super().__init__()

        # Instance de SignalShape pour émettre des signaux
        self.signals = SignalShape()

        self.connections = []  # Stocker les connexions associées
        self.text = text
        self.handles = []  # Poignées de sélection

        # Définir la forme en losange
        self.width = width
        self.height = height
        self.set_polygon()

        # Personnalisation de l'apparence de la forme avec des couleurs personnalisées
        self.default_pen = QPen(QColor("#000000"), 1)  # Contour noir par défaut
        self.selected_pen = QPen(QColor("#0000FF"), 1, Qt.DashLine)  # Contour bleu en tirets lorsque sélectionné
        self.current_pen = self.default_pen

        # Utiliser les couleurs passées en paramètre pour définir les couleurs par défaut et sélectionnées
        self.default_brush = QBrush(default_color)  # Remplissage par défaut
        self.selected_brush = QBrush(selected_color)  # Remplissage lorsque sélectionné
        self.current_brush = self.default_brush

        # Appliquer l'apparence par défaut
        self.setPen(self.current_pen)
        self.setBrush(self.current_brush)

        # Activer les événements et les flags nécessaires
        self.setAcceptHoverEvents(True)  # Gérer les événements de survol
        self.setFlags(QGraphicsPolygonItem.ItemIsMovable |
                      QGraphicsPolygonItem.ItemSendsGeometryChanges |
                      QGraphicsPolygonItem.ItemIsSelectable)  # Permettre le déplacement et la sélection

        # Poignées de sélection (carrés jaunes)
        self.init_handles()

        # Magnétiser le losange sur la grille à la création
        self.snap_to_grid()

    def set_polygon(self):
        # Définir la forme en losange
        half_width = self.width / 2
        half_height = self.height / 2
        points = [
            QPointF(0, -half_height),  # Sommet haut
            QPointF(half_width, 0),  # Coin droit
            QPointF(0, half_height),  # Sommet bas
            QPointF(-half_width, 0)  # Coin gauche
        ]
        polygon = QPolygonF(points)
        self.setPolygon(polygon)

    def init_handles(self):
        # Crée quatre poignées pour les coins du losange
        for i in range(4):
            handle = QGraphicsPolygonItem(self)
            handle.setPen(QPen(QColor("#AFFA00"), 2, Qt.SolidLine))  # Couleur de bordure des poignées en jaune
            handle.setBrush(QBrush(QColor("#FFFF00")))
            handle.setVisible(False)
            self.handles.append(handle)
        self.update_handles()

    def update_handles(self):
        # Positionner les poignées aux quatre coins du losange
        polygon = self.polygon()
        for i, handle in enumerate(self.handles):
            handle.setPos(polygon[i] - QPointF(3, 3))

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
            'Largeur': self.width,
            'Hauteur': self.height
        }
        self.signals.propertiesChanged.emit(properties)

    def mousePressEvent(self, event):
        # Gérer l'événement de clic de souris pour sélectionner/désélectionner manuellement
        self.set_selected(not self.is_selected())  # Inverser l'état de sélection
        super().mousePressEvent(event)  # Appeler l'événement de base pour gérer les autres comportements

    def itemChange(self, change, value):
        if change == QGraphicsPolygonItem.ItemPositionChange:
            # Magnétiser la position sur la grille
            new_pos = value
            snapped_pos = self.snap_to_grid_position(new_pos)

            # Émettre le signal de changement de position avec la nouvelle position
            self.signals.positionChanged.emit(snapped_pos)

            # Mettre à jour les poignées de sélection
            self.update_handles()
            return snapped_pos

        # Si l'état de sélection change, mettre à jour l'apparence
        elif change == QGraphicsPolygonItem.ItemSelectedChange:
            self.set_selected(value)

        return super().itemChange(change, value)

    def snap_to_grid(self):
        # Magnétiser la position initiale du losange sur la grille
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
