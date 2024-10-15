from PySide6.QtGui import QPainter, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView

from DiagramFlow.RectangleShape import RectangleShape
from LineFlow.Connection import Connection
from Process.Task import Task
from app.CustomGraphicsScene import CustomGraphicsScene  # Importer la scène personnalisée
from ui.Ui_ProcessFlow import Ui_ProcessFlow


def func_compteur(compteur=1000000):
    for i in range(compteur):
        print(i)

def func_paire(compteur=1000000):
    for i in range(compteur):
        if i % 2 == 0:
            print(i)


class ProcessFlow(QMainWindow, Ui_ProcessFlow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Initialisation de la scène graphique personnalisée
        self.scene = CustomGraphicsScene(self)
        self.graphicsView.setScene(self.scene)
        self.scene.signals.connectionCreated.connect(self.onCreatedConnection)
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
        self.setWindowTitle("Process Flow - Designer")


    def onCreatedConnection(self, connection:Connection):
        connection.signals.propertiesChanged.connect(self.updateProperties)

    def addShapes(self):
        # Ajouter un rectangle
        p1=Task("Calcul")
        p2=Task("Trier")
        process1 = RectangleShape(50, 50, 100, 50, "Compteur",function=func_compteur)
        process2 = RectangleShape(250, 50, 100, 50, "Compteur2",function=func_paire)
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

        # Déterminer le type de la forme
        shape_type = properties.get('Type', None)

        properties_order = {
            'RectangleShape': ['Nom', 'X', 'Y', 'Largeur', 'Hauteur','Type',"Tâche","État"],
            'CircleShape': ['Nom de la forme', 'Position X', 'Position Y', 'Rayon'],
            'DiamondShape': ['Nom de la forme', 'Position X', 'Position Y', 'Largeur', 'Hauteur', 'Angle'],
        }

        order = properties_order.get(shape_type, list(
            properties.keys()))  # Défaut à l'ordre naturel des clés si le type n'est pas trouvé

        # Ajouter les propriétés à la table dans l'ordre défini
        for prop in order:
            if prop in properties:
                prop_item = QStandardItem(str(prop))
                value_item = QStandardItem(str(properties[prop]))
                self.property_table_model.appendRow([prop_item, value_item])

    def clearTableData(self):
        self.property_table_model.removeRows(0, self.property_table_model.rowCount())

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = ProcessFlow()
    mainWindow.show()
    sys.exit(app.exec())
