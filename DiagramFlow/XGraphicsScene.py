from PySide6.QtCore import Qt, QRectF, QLineF
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QGraphicsView


class XGraphicsViewScene(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(QColor(245, 245, 245))  # Couleur de fond gris clair
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        # Taille du quadrillage
        self.small_grid_size = 10  # Taille des petits carreaux
        self.large_grid_size = self.small_grid_size * 4  # Les grands carreaux sont un multiple des petits

        # Couleurs et styles de la grille
        self.small_grid_color = QColor(200, 200, 200,80)  # Couleur des petits carreaux (gris clair)
        self.large_grid_color = QColor(100, 149, 237,30)  # Couleur des grands carreaux (bleu "CornflowerBlue")

        # Épaisseur des lignes
        self.small_grid_pen = QPen(self.small_grid_color, 0)  # Lignes fines pour les petits carreaux
        self.large_grid_pen = QPen(self.large_grid_color, 1.5)  # Lignes plus épaisses pour les grands carreaux

    def drawBackground(self, painter, rect):
        """Dessine le quadrillage en arrière-plan."""
        super().drawBackground(painter, rect)

        # Déterminer les limites du rectangle visible dans la scène
        left = int(rect.left()) - (int(rect.left()) % self.small_grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.small_grid_size)

        # Dessiner les petits carreaux (grille fine)
        self.draw_grid(painter, rect, self.small_grid_size, self.small_grid_pen)

        # Dessiner les grands carreaux (grille épaisse)
        self.draw_grid(painter, rect, self.large_grid_size, self.large_grid_pen)

    def draw_grid(self, painter, rect, grid_size, pen):
        """Dessine le quadrillage à une taille donnée et avec un style de ligne donné."""
        lines = []

        # Calcul des lignes verticales
        x_start = int(rect.left()) - (int(rect.left()) % grid_size)
        for x in range(x_start, int(rect.right()), grid_size):
            lines.append(QLineF(x, rect.top(), x, rect.bottom()))

        # Calcul des lignes horizontales
        y_start = int(rect.top()) - (int(rect.top()) % grid_size)
        for y in range(y_start, int(rect.bottom()), grid_size):
            lines.append(QLineF(rect.left(), y, rect.right(), y))

        # Dessiner les lignes
        painter.setPen(pen)
        painter.drawLines(lines)
