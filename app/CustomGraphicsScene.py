from PySide6.QtGui import QPen, QColor
from PySide6.QtWidgets import QGraphicsScene
from DiagramFlow.SignalShape import SignalShape
from LineFlow.Connection import Connection
from LineFlow.IOPort import IOPort


class CustomGraphicsScene(QGraphicsScene):
    def __init__(self, parent=None, grid=25):
        super().__init__(parent)
        self.start_port = None
        self.end_port = None
        #self.temp_line = None
        self.is_connecting = False
        self.grid = grid
        self.signals = SignalShape()

    def startConnection(self):
        """Initialise la connexion en créant une ligne temporaire."""
        if not isinstance(self.start_port, IOPort):
            return
        if not self.start_port.is_connected():  # Vérifier que le port n'est pas déjà connecté
            self.is_connecting = True
            start_pos = self.start_port.scenePos()
            # Créer une ligne de connexion temporaire
            #self.temp_line = Connection(self.start_port)
            #self.addItem(self.temp_line)
            # Initialiser la ligne temporaire à la position du port de départ
            #self.temp_line.setLine(start_pos.x(), start_pos.y(), start_pos.x(), start_pos.y())

    def endConnection(self):
        """Termine la connexion en validant et en ajoutant une connexion permanente."""
        if self.start_port and self.start_port.can_connect(self.end_port):
            if self.start_port.connect_to(self.end_port):
                # Créer une connexion entre les deux ports
                connection = Connection(self.start_port, self.end_port)
                self.addItem(connection)

                # Connecter les signaux de changement de position des rectangles
                self.start_port.parentItem().signals.positionChanged.connect(connection.update_position)
                self.end_port.parentItem().signals.positionChanged.connect(connection.update_position)
                self.signals.connectionCreated.emit(connection)
                print("Connexion créée et ajoutée à la scène")  # Débogage
            else:
                print("Connexion non permise")  # Débogage
        else:
            print("Pas un port valide ou le même port de départ")  # Débogage

        # Terminer la connexion en nettoyant les objets temporaires
        self.cancelConnection()

    def cancelConnection(self):
        """Annule la connexion en nettoyant les objets temporaires."""
        # if self.temp_line:
        #     print("Suppression de la ligne temporaire")  # Débogage
        #     self.removeItem(self.temp_line)
        #     self.temp_line = None
        # else:
        #     print("Aucune ligne temporaire à supprimer")  # Débogage

        # Réinitialiser les valeurs
        self.start_port = None
        self.end_port = None
        self.is_connecting = False

    def mouseMoveEvent(self, event):
        """Met à jour la position de la ligne temporaire pendant le traçage."""
        # if self.is_connecting and self.temp_line:
        #     end_pos = event.scenePos()
        #     self.temp_line.setLine(self.temp_line.line().x1(), self.temp_line.line().y1(), end_pos.x(), end_pos.y())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Gère l'événement de relâchement de la souris pour établir une connexion."""
        item = self.itemAt(event.scenePos(), self.views()[0].transform())

        if isinstance(item, IOPort):
            if not self.is_connecting:
                print(f"Port de départ sélectionné: {item.name}")
                self.start_port = item
                self.startConnection()
            else:
                print(f"Port d'arrivée sélectionné: {item.name}")
                self.end_port = item
                self.endConnection()
        else:
            print("Aucun Élément sélectionné")  # Débogage
            self.cancelConnection()  # Annuler la connexion si l'élément n'est pas un port

        super().mouseReleaseEvent(event)

    def drawBackground(self, painter, rect):
        """Dessine une grille de carreaux de taille GRID_SIZE."""
        # Couleur de la grille
        grid_color = QColor(141,141, 141)  # Gris clair

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
        for x in range(left - (left % self.grid), right, self.grid):
            painter.drawLine(x, top, x, bottom)

        # Dessiner les lignes horizontales de la grille
        for y in range(top - (top % self.grid), bottom, self.grid):
            painter.drawLine(left, y, right, y)

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos(), self.views()[0].transform())
        super().mousePressEvent(event)  # Appeler la méthode de la classe parente
