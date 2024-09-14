from PySide6.QtGui import QPainter, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView

from DiagramFlow.CircleShape import CircleShape
from DiagramFlow.RectangleShape import RectangleShape
from LineFlow.ConnectionBezier import ConnectionBezier
from app.CustomGraphicsScene import CustomGraphicsScene  # Importer la scène personnalisée
from ui.Ui_ProcessFlow import Ui_ProcessFlow


class ProcessFlow(QMainWindow, Ui_ProcessFlow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)


        # Initialisation de la scène graphique personnalisée
        self.scene = CustomGraphicsScene(self)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setRenderHint(QPainter.Antialiasing)
        self.graphicsView.setDragMode(QGraphicsView.RubberBandDrag)

        # Stocker les formes et les lignes
        self.shapes = []
        self.lines = []
        # Ajouter des formes à la scène
        self.addShapes()
        # Connecter les formes avec des lignes
        self.connectShapes()

        self.property_table_model = QStandardItemModel()
        self.tableView.setModel(self.property_table_model)
        self.property_table_model.setHorizontalHeaderLabels(["Propriété", "Valeur"])


    def addShapes(self):
        # Ajouter un rectangle
        process_shape = RectangleShape(50, 50, 100, 50, "Process")
        self.scene.addItem(process_shape)
        self.shapes.append(process_shape)

        # Ajouter un autre rectangle
        another_shape = CircleShape(200, 100, 50, "Process 2")
        self.scene.addItem(another_shape)
        self.shapes.append(another_shape)

        # Connecter les signaux de déplacement des formes à la mise à jour des lignes
        process_shape.signals.positionChanged.connect(self.updateLines)
        another_shape.signals.positionChanged.connect(self.updateLines)

        # Connecter les signaux des propriétés des formes à la méthode de mise à jour de la table
        process_shape.signals.propertiesChanged.connect(self.updateProperties)
        another_shape.signals.propertiesChanged.connect(self.updateProperties)

    def connectShapes(self):
        if len(self.shapes) >= 2:
            # Créer une ligne de connexion entre les deux premiers objets
            line = ConnectionBezier(self.shapes[0], self.shapes[1])
            line.signals.propertiesChanged.connect(self.updateProperties)
            self.scene.addItem(line)
            self.lines.append(line)

    def updateLines(self):
        # Mettre à jour les positions des lignes de connexion
        for line in self.lines:
            line.update_position()

    def updateProperties(self, properties):
        # Effacer toutes les lignes existantes du modèle
        self.clearTableData()

        # Ajouter les nouvelles propriétés à la table
        for prop, value in properties.items():
            prop_item = QStandardItem(str(prop))
            value_item = QStandardItem(str(value))
            self.property_table_model.appendRow([prop_item, value_item])

    def clearTableData(self):
        # Supprimer toutes les lignes du modèle
        self.property_table_model.removeRows(0, self.property_table_model.rowCount())

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = ProcessFlow()
    mainWindow.show()
    sys.exit(app.exec())
