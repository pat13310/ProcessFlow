from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import QGraphicsEllipseItem
from DiagramFlow.SignalShape import SignalShape

class IOPort(QGraphicsEllipseItem):
    def __init__(self, parent_shape, is_input=True):
        super().__init__(0, 0, 10, 10, parent_shape)
        self.parent_shape = parent_shape
        self.is_input = is_input
        self.connected_to = None
        # Composez le nom du port en fonction du nom du parent et du type de port
        parent_name = parent_shape.shape_name if hasattr(parent_shape, 'shape_name') else 'Inconnu'
        suffix = "_E" if is_input else "_S"
        self.name = f"{parent_name}{suffix}"

        self.setPen(QPen(QColor("#000000")))
        self.setAcceptHoverEvents(True)
        self.setCursor(Qt.CrossCursor)
        self.signals = SignalShape()
        self.is_selected = False

        self.defaut_status()

    def defaut_status(self):
        if self.is_input:
            self.setBrush(QBrush(QColor("lightgreen")))
        else:
            self.setBrush(QBrush(QColor("#D9f970")))

    def hoverEnterEvent(self, event):
        if self.scene().is_connecting and not self.is_selected:
            self.setBrush(QBrush(QColor("lightyellow")))
        elif not self.is_selected:
            self.defaut_status()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        if not self.is_selected and not self.is_connected():
            self.defaut_status()

        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.set_selected(True)
            self.scene().startConnection()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.scene().endConnection()
        super().mouseReleaseEvent(event)

    def can_connect(self, other_port):

        if isinstance(other_port, IOPort):
        # Règle 2 et 3: Pas de connexion entre ports de même type
            if self.is_input == other_port.is_input:
                return False
            # Règle 4: Pas de connexion si déjà connecté
            if self.is_connected() or other_port.is_connected():
                return False
        return True

    def connect_to(self, other_port):
        if isinstance(other_port, IOPort):
            if self.can_connect(other_port):
                self.connected_to = other_port
                other_port.connected_to = self
                self.reset_state()
                other_port.reset_state()
                return True
        return False

    def disconnect(self):
        if self.connected_to:
            other_port = self.connected_to
            self.connected_to = None
            other_port.connected_to = None
            self.reset_state()
            other_port.reset_state()

    def is_connected(self):
        return self.connected_to is not None

    def get_parent(self):
        return self.parent_shape

    def set_selected(self, selected):
        self.is_selected = selected
        if selected:
            self.setBrush(QBrush(QColor("#A0A0FF")))
        else:
            self.defaut_status()


    def reset_state(self):
        self.set_selected(False)
        if self.scene():
            self.scene().is_connecting = False

    def set_color(self, color):
        # Méthode pour changer la couleur de l'IOPort
        self.setBrush(QBrush(QColor(color)))