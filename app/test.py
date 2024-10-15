import sys
import xml.etree.ElementTree as ET

from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow
from DiagramFlow.RectangleShape2 import RectangleShape2, Properties


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.view = None
        self.setWindowTitle("Diagram Viewer")
        self.setGeometry(100, 100, 1000, 600)
        self.scene = QGraphicsScene()


    def load_xml_content(self, xml_content):
        root = ET.fromstring(xml_content)
        mx_cells = root.findall('.//mxCell')
        for cell in mx_cells:
            properties = Properties.from_xml_element(cell)
            if 'rectangle' in properties.style:
                rectangle = RectangleShape2(properties)
                self.scene.addItem(rectangle)
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)


if __name__ == "__main__":
    str_xml="""
     <mxfile host="Electron" modified="2024-10-12T18:28:36.702Z" agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) draw.io/23.1.5 Chrome/120.0.6099.109 Electron/28.1.0 Safari/537.36" etag="eGa8U2hlxHhIUbvjggcc" version="23.1.5" type="device">
            <diagram id="saZLJ1-gX8K1ZKheShiA" name="Page-1">
                <mxGraphModel dx="965" dy="659" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
                    <root>
                        <mxCell id="0" />
                        <mxCell id="1" parent="0" />
                        <mxCell id="2" value="Rectangle 1" style="rectangle;fillColor=#fff2cc;strokeColor=#d6b656;rounded=1;glass=1;shadow=1;fontStyle=1;fontColor=#FFB570;" parent="1" vertex="1">
                            <mxGeometry x="50" y="50" width="100" height="50" as="geometry" />
                        </mxCell>
                        <mxCell id="3" value="Rectangle 2" style="rectangle;fillColor=#ffe6cc;strokeColor=#d79b00;gradientColor=#FF8000;glass=1;" parent="1" vertex="1">
                            <mxGeometry x="370" y="37.5" width="150" height="75" as="geometry" />
                        </mxCell>
                        <mxCell id="4" value="Connection 1" parent="1" source="2" target="3" edge="1">
                            <mxGeometry relative="1" as="geometry" />
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