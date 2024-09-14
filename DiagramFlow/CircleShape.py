from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtGui import QBrush, QPen, QColor, QPainter, QFont

from DiagramFlow.SignalShape import SignalShape


class CircleShape(QGraphicsEllipseItem):
    GRID_SIZE = 25  # Taille de chaque cellule de la grille

    def __init__(self, x, y, diameter, text):
        super().__init__(x, y, diameter, diameter)

        self.signals = SignalShape()

        self.connections = []
        self.text = text
        self.handles = []

        # Personnalisation de l'apparence de la forme
        self.default_pen = QPen(QColor("#000000"), 1)
        self.selected_pen = QPen(QColor("#0000FF"), 1, Qt.DashLine)
        self.current_pen = self.default_pen

        self.default_brush = QBrush(QColor("#C8FFC8"))
        self.selected_brush = QBrush(QColor("#C8C8FF"))
        self.current_brush = self.default_brush

        # Appliquer l'apparence par défaut
        self.setPen(self.current_pen)
        self.setBrush(self.current_brush)

        # Activer les événements et les flags nécessaires
        self.setAcceptHoverEvents(True)
        self.setFlags(QGraphicsEllipseItem.ItemIsMovable |
                      QGraphicsEllipseItem.ItemSendsGeometryChanges |
                      QGraphicsEllipseItem.ItemIsSelectable)

        # Poignées de sélection
        self.init_handles()

        # Magnétiser le cercle sur la grille à la création
        self.snap_to_grid()

    def init_handles(self):
        for i in range(4):
            handle = QGraphicsEllipseItem(0, 0, 6, 6, self)
            handle.setPen(QPen(QColor("#AFFA00"), 2, Qt.SolidLine))
            handle.setBrush(QBrush(QColor("#FFFF00")))
            handle.setVisible(False)
            self.handles.append(handle)
        self.update_handles()

    def update_handles(self):
        rect = self.rect()
        self.handles[0].setPos(rect.center() + QPointF(-3, -rect.height() / 2 - 3))
        self.handles[1].setPos(rect.center() + QPointF(-3, rect.height() / 2 - 3))
        self.handles[2].setPos(rect.center() + QPointF(-rect.width() / 2 - 3, -3))
        self.handles[3].setPos(rect.center() + QPointF(rect.width() / 2 - 3, -3))

    def paint(self, painter, option, widget=None):
        # Dessiner le cercle
        painter.setPen(self.current_pen)
        painter.setBrush(self.current_brush)
        painter.drawEllipse(self.rect())

        # Configurer le style du texte
        painter.setPen(QPen(QColor("#000000")))  # Couleur du texte
        font = QFont()
        font.setBold(True)
        painter.setFont(font)

        # Centrer le texte
        rect = self.rect()
        painter.drawText(rect, Qt.AlignCenter, self.text)

    def set_selected(self, selected):
        if selected:
            self.current_pen = self.selected_pen
            self.current_brush = self.selected_brush
            for handle in self.handles:
                handle.setVisible(True)
            self.emit_properties()
        else:
            self.current_pen = self.default_pen
            self.current_brush = self.default_brush
            for handle in self.handles:
                handle.setVisible(False)
        self.setPen(self.current_pen)
        self.setBrush(self.current_brush)

    def emit_properties(self):
        properties = {
            'Texte': self.text,
            'Position X': self.pos().x(),
            'Position Y': self.pos().y(),
            'Diamètre': self.rect().width()
        }
        self.signals.propertiesChanged.emit(properties)

    def mousePressEvent(self, event):
        self.set_selected(not self.is_selected())  # Inverser l'état de sélection
        super().mousePressEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsEllipseItem.ItemPositionChange:
            new_pos = value
            snapped_pos = self.snap_to_grid_position(new_pos)
            self.signals.positionChanged.emit(snapped_pos)
            self.update_handles()
            return snapped_pos
        elif change == QGraphicsEllipseItem.ItemSelectedChange:
            self.set_selected(value)
        return super().itemChange(change, value)

    def snap_to_grid(self):
        current_pos = self.pos()
        snapped_pos = self.snap_to_grid_position(current_pos)
        self.setPos(snapped_pos)

    def snap_to_grid_position(self, position):
        snapped_x = round(position.x() / self.GRID_SIZE) * self.GRID_SIZE
        snapped_y = round(position.y() / self.GRID_SIZE) * self.GRID_SIZE
        return QPointF(snapped_x, snapped_y)

    def add_connection(self, connection):
        self.connections.append(connection)

    def remove_connection(self, connection):
        if connection in self.connections:
            self.connections.remove(connection)

    def is_selected(self):
        return self.current_pen == self.selected_pen
