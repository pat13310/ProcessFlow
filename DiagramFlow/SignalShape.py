from PySide6.QtCore import Signal, QObject, QPointF


class SignalShape(QObject):
    positionChanged = Signal(QPointF)  # Définir le signal
    propertiesChanged = Signal(dict)  # Signal émis pour envoyer les propriétés

    def __init__(self):
        super().__init__()

    def emit_position_changed(self):
        # Méthode pour émettre le signal
        self.positionChanged.emit()

