import sys

from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow, QMenuBar, QFileDialog, \
    QGraphicsLineItem
from PySide6.QtGui import QAction
import xml.etree.ElementTree as ET

from DiagramFlow.XGraphicsScene import XGraphicsViewScene
from DiagramFlow.XLine import XLine
from DiagramFlow.XShape import Properties, XShape


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.view = None
        self.setWindowTitle("Diagram Viewer")
        self.setGeometry(100, 100, 1000, 600)
        self.scene = QGraphicsScene()

        self.create_menu()
        self.view = XGraphicsViewScene(self.scene)
        self.setCentralWidget(self.view)

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Fichier")

        open_action = QAction("Ouvrir", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Sauver", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Ouvrir fichier Drawio", "", "XML Files (*.drawio)")
        if file_name:
            with open(file_name, 'r') as file:
                xml_content = file.read()
                self.load_xml_content(xml_content)

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Drawio File", "", "XML Files (*.drawio)")
        if file_name:
            # Ici, vous devez implémenter la logique pour sauvegarder le contenu actuel en XML
            # Par exemple :
            # xml_content = self.generate_xml_content()
            # with open(file_name, 'w') as file:
            #     file.write(xml_content)
            pass

    def load_xml_content(self, xml_content):
        # Effacer la scène actuelle
        self.scene.clear()

        # Charger le contenu XML et trouver tous les éléments 'mxCell'
        root = ET.fromstring(xml_content)
        mx_cells = root.findall('.//mxCell')

        # Créer un dictionnaire pour stocker les formes par leur ID
        shapes_by_id = {}

        # Première boucle : charger les formes géométriques
        for cell in mx_cells:
            properties = Properties.from_xml_element(cell)  # Créer les propriétés à partir de l'élément XML

            # Si c'est une arête (edge), on ignore pour cette boucle
            if cell.get('edge') == '1':
                continue

            # Créer et ajouter la forme appropriée à la scène
            if properties.geometry:  # On ne traite que les cellules avec une géométrie
                shape = XShape(properties)
                shape.setZValue(1)
                self.scene.addItem(shape)
                shapes_by_id[properties.id] = shape  # Stocker la forme avec son ID pour l'utiliser dans les connexions

        # Deuxième boucle : charger les connexions entre les formes (arêtes)
        for cell in mx_cells:
            if cell.get('edge') == '1':  # Traiter uniquement les arêtes
                source_id = cell.get('source')
                target_id = cell.get('target')

                # Récupérer les formes source et cible
                source_shape = shapes_by_id.get(source_id)
                target_shape = shapes_by_id.get(target_id)

                if source_shape and target_shape:
                    if source_shape and target_shape:
                        # Créer une ligne XLine
                        line = XLine(source_shape, target_shape, properties=cell)
                        line.setZValue(-1)
                        self.scene.addItem(line)
                        # Ajouter cette ligne aux formes source et cible
                        #source_shape.add_connected_line(line)
                        #target_shape.add_connected_line(line)

    def detect_shape_type(self, style):
        """Détecte le type de forme géométrique à partir du style donné."""
        if 'ellipse' in style:
            return 'Ellipse'
        elif 'rhombus' in style:
            return 'Losange'
        elif 'triangle' in style:
            return 'Triangle'
        elif 'shape=parallelogram' in style:
            return 'Parallélogramme'
        elif 'shape=hexagon' in style:
            return 'Hexagone'
        else:
            return 'Rectangle'  # Par défaut, c'est un rectangle


if __name__ == "__main__":
    str_xml = """
    <mxfile host="Electron" modified="2024-10-17T07:42:12.448Z" agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) draw.io/23.1.5 Chrome/120.0.6099.109 Electron/28.1.0 Safari/537.36" version="23.1.5" etag="aFC6uGDlKmlwxz3g6zQA" type="device">
  <diagram id="jPVGQL-rKCRgdcBdRN32" name="Page-1">
    <mxGraphModel dx="963" dy="656" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="MSs7MxiRivUBDTYrBmWL-3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="MSs7MxiRivUBDTYrBmWL-1" target="MSs7MxiRivUBDTYrBmWL-2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="MSs7MxiRivUBDTYrBmWL-1" value="Flux" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;gradientColor=#ea6b66;shadow=1;glass=1;" vertex="1" parent="1">
          <mxGeometry x="140" y="170" width="120" height="60" as="geometry" />
        </mxCell>
        <mxCell id="MSs7MxiRivUBDTYrBmWL-2" value="Test" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffcd28;strokeColor=#d79b00;glass=1;gradientColor=#ffa500;" vertex="1" parent="1">
          <mxGeometry x="370" y="170" width="120" height="60" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.load_xml_content(str_xml)
    window.show()
    sys.exit(app.exec())
