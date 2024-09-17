from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from PySide6.QtGui import QBrush, QPen, QColor, QFont
from DiagramFlow.SignalShape import SignalShape
from LineFlow.IOPort import IOPort

class RectangleShape(QGraphicsRectItem):
    GRID_SIZE = 25

    def __init__(self, x, y, width, height, text, default_color=QColor("#FFC8C8"), selected_color=QColor("#C8C8FF")):
        super().__init__(x, y, width, height)
        self.signals = SignalShape()
        self.connections = []
        self.text = text
        self.handles = []
        self.connection_points = []

        # Apparence
        self.default_pen = QPen(QColor("#000000"), 1)
        self.selected_pen = QPen(QColor("#0000FF"), 1, Qt.DashLine)
        self.current_pen = self.default_pen
        self.default_brush = QBrush(default_color)
        self.selected_brush = QBrush(selected_color)
        self.current_brush = self.default_brush
        self.setPen(self.current_pen)
        self.setBrush(self.current_brush)

        # Flags
        self.setAcceptHoverEvents(True)
        self.setFlags(QGraphicsRectItem.ItemIsMovable |
                      QGraphicsRectItem.ItemSendsGeometryChanges |
                      QGraphicsRectItem.ItemIsSelectable)

        # Initialisation
        self.init_handles()
        self.init_connection_points()
        self.init_text()
        self.snap_to_grid()

    def init_handles(self):
        for _ in range(4):
            handle = QGraphicsRectItem(0, 0, 6, 6, self)
            handle.setPen(QPen(QColor("#AFFA00"), 2, Qt.SolidLine))
            handle.setBrush(QBrush(QColor("#FFFF00")))
            handle.setVisible(False)
            self.handles.append(handle)
        self.update_handles()

    def init_connection_points(self):
        self.left_port = IOPort(self, is_input=True)
        self.right_port = IOPort(self, is_input=False)
        self.connection_points.append(self.left_port)
        self.connection_points.append(self.right_port)
        self.calculate_positions()

    def init_text(self):
        self.text_item = QGraphicsTextItem(self.text, self)
        self.text_item.setFont(QFont("Arial", 10))
        self.update_text_position()

    def update_handles(self):
        rect = self.rect()
        positions = [rect.topLeft(), rect.topRight(), rect.bottomLeft(), rect.bottomRight()]
        for handle, pos in zip(self.handles, positions):
            handle.setPos(pos - QPointF(3, 3))

    def set_selected(self, selected):
        self.current_pen = self.selected_pen if selected else self.default_pen
        self.current_brush = self.selected_brush if selected else self.default_brush
        for handle in self.handles:
            handle.setVisible(selected)
        self.setPen(self.current_pen)
        self.setBrush(self.current_brush)
        if selected:
            self.emit_properties()

    def emit_properties(self):
        properties = {
            'Texte': self.text,
            'Position X': self.pos().x(),
            'Position Y': self.pos().y(),
            'Largeur': self.rect().width(),
            'Hauteur': self.rect().height()
        }
        self.signals.propertiesChanged.emit(properties)

    def mousePressEvent(self, event):
        self.set_selected(not self.isSelected())
        super().mousePressEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.ItemPositionChange:
            new_pos = self.snap_to_grid_position(value)
            self.signals.positionChanged.emit(new_pos)
            self.update_handles()
            self.update_connection_points()
            self.update_text_position()
            return new_pos
        elif change == QGraphicsRectItem.ItemSelectedChange:
            self.set_selected(value)
        return super().itemChange(change, value)

    def calculate_positions(self):
        rect = self.rect()
        self.left_port.setPos(rect.left() - 5, rect.center().y() - 5)
        self.right_port.setPos(rect.right() - 5, rect.center().y() - 5)

    def update_connection_points(self):
        self.calculate_positions()

    def update_text_position(self):
        rect = self.rect()
        self.text_item.setPos(rect.center() - self.text_item.boundingRect().center())

    def snap_to_grid(self):
        self.setPos(self.snap_to_grid_position(self.pos()))

    def snap_to_grid_position(self, position):
        return QPointF(
            round(position.x() / self.GRID_SIZE) * self.GRID_SIZE,
            round(position.y() / self.GRID_SIZE) * self.GRID_SIZE
        )

    def add_connection(self, connection):
        if connection not in self.connections:
            self.connections.append(connection)

    def remove_connection(self, connection):
        if connection in self.connections:
            self.connections.remove(connection)

    def is_selected(self):
        return self.isSelected()

    def set_text(self, new_text):
        self.text = new_text
        self.text_item.setPlainText(new_text)
        self.update_text_position()

    def get_input_port(self):
        return self.left_port

    def get_output_port(self):
        return self.right_port
