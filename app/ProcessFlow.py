from PySide6.QtGui import QPainter, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView

from DiagramFlow.CircleShape import CircleShape
from DiagramFlow.RectangleShape import RectangleShape
from DiagramFlow.DiamondShape import DiamondShape
from LineFlow.Connection import Connection
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
        process1 = RectangleShape(50, 50, 100, 50, "Process1")
        process2 = RectangleShape(250, 50, 100, 50, "Process2")
        process3 = RectangleShape(50, 150, 150,50, "Process3")
        process4 = RectangleShape(250, 150, 150, 50, "Process4")
        self.addShape(process1)
        self.addShape(process2)
        self.addShape(process3)
        self.addShape(process4)


    def addShape(self, shape):
        self.scene.addItem(shape)
        self.shapes.append(shape)
        shape.signals.positionChanged.connect(self.updateLines)
        shape.signals.propertiesChanged.connect(self.updateProperties)

    def connectShapes(self):
        if len(self.shapes) >= 2:
            start_port = self.shapes[0].right_port
            end_port = self.shapes[1].left_port
            line = Connection(start_port, end_port)
            line.signals.propertiesChanged.connect(self.updateProperties)
            self.scene.addItem(line)
            self.lines.append(line)
            start_port.connect_to(end_port)

    def updateLines(self):
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
