from PySide6.QtGui import QPen, QColor
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import Qt

from LineFlow.Connection import Connection
from LineFlow.IOPort import IOPort


class CustomGraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_port = None
        self.end_port = None
        self.temp_line = None
        self.is_connecting = False
        self.click_count = 0  # Compteur de clics
        self.GRID_SIZE=25

    def startConnection(self):
        if not isinstance(self.start_port, IOPort):
            return
        if not self.start_port.is_connected():  # Vérifier que le port n'est pas déjà connecté

            self.is_connecting = True
            start_pos = self.start_port.scenePos()
            # Créer une ligne de connexion temporaire
            self.temp_line = Connection(self.start_port.parent_shape, None)
            self.addItem(self.temp_line)
            self.temp_line.setLine(start_pos.x(), start_pos.y(), start_pos.x(), start_pos.y())

    def endConnection(self):

        if self.start_port and self.start_port.can_connect(self.end_port):
            if self.start_port.connect_to(self.end_port):
                # Créer une connexion entre les deux ports
                connection = Connection(self.start_port, self.end_port)
                self.addItem(connection)

                # Connecter les signaux de changement de position des rectangles
                self.start_port.parentItem().signals.positionChanged.connect(connection.update_position)
                self.end_port.parentItem().signals.positionChanged.connect(connection.update_position)

                print("Connexion créée et ajoutée à la scène")  # Débogage
            else:
                print("Connexion non permise")  # Débogage
        else:
            print("Pas un port valide ou le même port de départ")  # Débogage

        # Terminer la connexion en nettoyant les objets temporaires
        if self.temp_line:
            self.removeItem(self.temp_line)
        self.temp_line = None
        self.start_port = None
        self.end_port = None
        self.is_connecting = False
        self.click_count = 0  # Réinitialiser le compteur de clics

    def mouseMoveEvent(self, event):
        # Mettre à jour la position de la ligne temporaire pendant le traçage
        if self.is_connecting and self.temp_line:
            end_pos = event.scenePos()
            self.temp_line.setLine(self.temp_line.line().x1(), self.temp_line.line().y1(), end_pos.x(), end_pos.y())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        # Incrémenter le compteur de clics à chaque clic
        self.click_count += 1

        if self.click_count == 1:
            # Premier clic : Définir le port de départ
            start_item = self.itemAt(event.scenePos(), self.views()[0].transform())

            if isinstance(start_item, IOPort):
                print(start_item.name)
                self.start_port = start_item
                self.startConnection()
                #print("Premier IOPort sélectionné")  # Débogage
            else:
                #print("Élément sélectionné non valide")  # Débogage
                self.click_count = 0  # Réinitialiser le compteur si le port de départ est invalide

        elif self.click_count == 2:
            # Deuxième clic : Définir le port de destination
            end_item = self.itemAt(event.scenePos(), self.views()[0].transform())

            if isinstance(end_item, IOPort) :
                print(end_item.name)
                self.end_port = end_item
                self.endConnection()

        super().mouseReleaseEvent(event)

    def drawBackground(self, painter, rect):
        """Dessine une grille de carreaux de taille GRID_SIZE."""
        # Couleur de la grille
        grid_color = QColor(220, 220, 220)  # Gris clair

        # Initialisation du stylo de dessin pour la grille
        pen = QPen(grid_color)
        pen.setWidth(1)
        painter.setPen(pen)

        # Déterminer les bornes du rectangle visible
        left = int(rect.left())
        right = int(rect.right())
        top = int(rect.top())
        bottom = int(rect.bottom())

        # Dessiner les lignes verticales de la grille
        for x in range(left - (left % self.GRID_SIZE), right, self.GRID_SIZE):
            painter.drawLine(x, top, x, bottom)

        # Dessiner les lignes horizontales de la grille
        for y in range(top - (top % self.GRID_SIZE), bottom, self.GRID_SIZE):
            painter.drawLine(left, y, right, y)
