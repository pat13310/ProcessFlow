from PySide6.QtGui import QPen, QColor
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import Qt


class CustomGraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_size = 25  # Taille de chaque cellule de la grille
        self.grid_color = QColor("#C8C8C8")  # Couleur de la grille en hexadécimal (gris clair)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # Définir la couleur et le style de la grille
        pen = QPen(self.grid_color)
        pen.setStyle(Qt.DotLine)
        painter.setPen(pen)

        # Dessiner la grille
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)

        # Lignes verticales
        for x in range(left, int(rect.right()), self.grid_size):
            painter.drawLine(x, int(rect.top()), x, int(rect.bottom()))

        # Lignes horizontales
        for y in range(top, int(rect.bottom()), self.grid_size):
            painter.drawLine(int(rect.left()), y, int(rect.right()), y)

    def mousePressEvent(self, event):
        # Vérifier si le clic est effectué en dehors des éléments
        if not self.itemAt(event.scenePos(), self.views()[0].transform()):
            # Aucun élément cliqué, donc désélectionner tous les éléments
            for item in self.items():
                if hasattr(item, 'setSelected'):  # Vérifier si l'élément a la méthode 'set_selected'
                    item.setSelected(False)  # Réinitialiser l'état de sélection
        super().mousePressEvent(event)


