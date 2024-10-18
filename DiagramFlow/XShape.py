import dataclasses

from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QBrush, QColor, QLinearGradient, QPen, QCursor, QFont, QPainterPath, QPainter
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsDropShadowEffect, QGraphicsTextItem, QGraphicsEllipseItem, \
    QGraphicsItem, QGraphicsPathItem

from DiagramFlow.CrossItem import CrossItem
from DiagramFlow.EditableTextItem import EditableTextItem
from DiagramFlow.HandleItem import HandleItem, ResizeDirection


@dataclasses.dataclass
class Geometry:
    x: float = 0.0
    y: float = 0.0
    width: float = 100.0
    height: float = 50.0
    relative: bool = False


@dataclasses.dataclass
class Font:
    style: str = 'normal'
    color: str = '#000000'
    size: int = 10
    name: str = 'Helvetica'

    @classmethod
    def from_style_string(cls, style_string):
        font_name = "Helvetica"
        style_parts = style_string.split(';')
        font_style = 'normal'
        font_color = '#000000'
        font_size = 10
        for part in style_parts:
            if part.startswith('fontStyle='):
                font_style = part.split('=')[1]
            elif part.startswith('fontColor='):
                font_color = part.split('=')[1]
            elif part.startswith('fontName='):
                font_name = part.split('=')[1]
            elif part.startswith('fontSize='):
                try:
                    font_size = int(part.split('=')[1])
                except ValueError:
                    font_size = 12
        return cls(style=font_style, color=font_color, size=font_size, name=font_name)


@dataclasses.dataclass
class Properties:
    id: str = ''
    value: str = ''
    style: str = ''
    vertex: bool = False
    edge: bool = False
    parent: str = ''
    source: str = ''
    target: str = ''
    geometry: Geometry = None
    font: Font = None
    glass_type: int = 0

    @classmethod
    def from_xml_element(cls, xml_element):
        geometry_element = xml_element.find('mxGeometry')
        geometry = None
        if geometry_element is not None:
            geometry = Geometry(
                x=float(geometry_element.get('x', 0)),
                y=float(geometry_element.get('y', 0)),
                width=float(geometry_element.get('width', 100)),
                height=float(geometry_element.get('height', 50)),
                relative=geometry_element.get('relative', '0') == '1'
            )
        font = Font.from_style_string(xml_element.get('style', ''))
        glass_type = 0
        style_parts = xml_element.get('style', '').split(';')
        for part in style_parts:
            if part.startswith('glass='):
                glass_value = part.split('=')[1]
                if glass_value == '1':
                    glass_type = 1  # Ellipse type
                elif glass_value == '2':
                    glass_type = 2  # Rectangle type
        return cls(
            id=xml_element.get('id', ''),
            value=xml_element.get('value', ''),
            style=xml_element.get('style', ''),
            vertex=xml_element.get('vertex', '0') == '1',
            edge=xml_element.get('edge', '0') == '1',
            parent=xml_element.get('parent', ''),
            source=xml_element.get('source', ''),
            target=xml_element.get('target', ''),
            geometry=geometry,
            font=font,
            glass_type=glass_type

        )


def detect_shape_type(style):
    """Détecte le type de forme géométrique en fonction du style."""
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
        return 'Rectangle'


class XShape(QGraphicsPathItem):
    def __init__(self, properties: Properties, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connected_lines = []
        self.properties = properties
        self.x = properties.geometry.x if properties.geometry else 0
        self.y = properties.geometry.y if properties.geometry else 0
        self.width = properties.geometry.width if properties.geometry else 100
        self.height = properties.geometry.height if properties.geometry else 50
        self.font = properties.font
        self.glass_type = properties.glass_type
        self.is_selected = False
        self.radius = 10
        # Gestion du dégradé, des angles arrondis, de l'ombrage et de l'effet glass
        style_parts = properties.style.split(';')
        fill_color = "#FFC8C8"
        gradient_color = None
        stroke_color = "#000000"
        self.rounded = False
        shadow = False
        glass = False
        for part in style_parts:
            if part.startswith('fillColor='):
                fill_color = part.split('=')[1]
            elif part.startswith('gradientColor='):
                gradient_color = part.split('=')[1]
            elif part.startswith('strokeColor='):
                stroke_color = part.split('=')[1]
            elif part.startswith('rounded=') and part.split('=')[1] == '1':
                self.rounded = True
            elif part.startswith('shadow=') and part.split('=')[1] == '1':
                shadow = True
            elif part.startswith('glass=') and (part.split('=')[1] == '1' or part.split('=')[1] == '2'):
                glass = True

        # Initialisation de l'apparence
        # self.setRect(self.x, self.y, self.width, self.height)
        self.default_pen = QPen(QColor(stroke_color), 1)
        self.setPen(self.default_pen)

        if gradient_color:
            gradient = QLinearGradient(self.boundingRect().topRight(), self.boundingRect().bottomRight())
            gradient.setColorAt(0, QColor(fill_color))
            gradient.setColorAt(1, QColor(gradient_color))
            self.default_brush = QBrush(gradient)
        else:
            self.default_brush = QBrush(QColor(fill_color))

        self.setBrush(self.default_brush)

        # Application de l'ombrage si défini
        if shadow:
            shadow_effect = QGraphicsDropShadowEffect()
            shadow_effect.setBlurRadius(10)
            shadow_effect.setOffset(3, 3)
            shadow_effect.setColor(QColor(0, 0, 0, 100))  # Ombre noire semi-transparente
            self.setGraphicsEffect(shadow_effect)

        # Enregistrer l'effet glass si défini
        self.glass = glass

        # Initialisation du texte
        self.init_text()

        # Initialisation des croix d'indication
        self.crosses = []
        self.handles = []
        self.shape_type = detect_shape_type(properties.style)
        self.init_shape()
        self.init_crosses()
        self.init_handles()

        # Flags pour l'interactivité
        self.setAcceptHoverEvents(True)
        self.setFlags(QGraphicsRectItem.ItemIsMovable |
                      QGraphicsRectItem.ItemSendsGeometryChanges)

        # Définir le curseur par défaut
        self.setCursor(QCursor(Qt.SizeAllCursor))
        self.update_text_position()

    def get_positions(self):
        rect = self.boundingRect()
        self._positions = [
            (rect.center().x(), rect.top(), ResizeDirection.V, Qt.SizeVerCursor),  # Haut milieu
            (rect.center().x(), rect.bottom(), ResizeDirection.V, Qt.SizeVerCursor),  # Bas milieu
            (rect.left(), rect.center().y(), ResizeDirection.H, Qt.SizeHorCursor),  # Gauche milieu
            (rect.right(), rect.center().y(), ResizeDirection.H, Qt.SizeHorCursor),  # Droite milieu
            (rect.topLeft().x(), rect.topLeft().y(), ResizeDirection.D, Qt.SizeFDiagCursor),  # Point Haut gauche
            (rect.topRight().x(), rect.topRight().y(), ResizeDirection.D, Qt.SizeBDiagCursor),  # Point Haut droit
            (rect.bottomLeft().x(), rect.bottomLeft().y(), ResizeDirection.D, Qt.SizeBDiagCursor),  # Point Bas gauche
            (rect.bottomRight().x(), rect.bottomRight().y(), ResizeDirection.D, Qt.SizeFDiagCursor)  # Point Bas droit
        ]
        return self._positions

    def add_connected_line(self, line):
        """Ajoute une ligne connectée à cette forme."""
        self.connected_lines.append(line)

    def mouseMoveEvent(self, event):
        self.prepareGeometryChange()
        super().mouseMoveEvent(event)
        self.update_connected_lines()


    def update_connected_lines(self):
        """Met à jour toutes les lignes connectées à cette forme."""
        for line in self.connected_lines:
            line.update_line_position()

    def mousePressEvent(self, event):
        self.is_selected = True

        """Gestion de l'événement de pression de souris."""
        for cross in self.crosses:
            cross.setVisible(not self.is_selected)
        for selected in self.handles:
            selected.setVisible(self.is_selected)

        self.setFlag(QGraphicsRectItem.ItemIsMovable, self.is_selected)

        if self.is_selected:
            self.setCursor(QCursor(Qt.SizeAllCursor))

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Gestion de l'événement de relâchement de souris."""

        super().mouseReleaseEvent(event)

    def hoverEnterEvent(self, event):
        """Afficher les croix d'indication lorsque la souris entre dans la zone."""
        if self.is_selected:
            pass
        else:
            for cross in self.crosses:
                cross.setVisible(True)

        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        """Masquer les croix d'indication lorsque la souris quitte la zone."""
        for cross in self.crosses:
            cross.setVisible(False)
        for handle in self.handles:
            handle.setVisible(False)
        self.is_selected = False
        super().hoverLeaveEvent(event)

    def paint(self, painter, option, widget=None):
        """Redéfinit la méthode de peinture pour gérer les coins arrondis et l'effet glass."""
        painter.setRenderHint(QPainter.Antialiasing)
        if self.rounded:
            path = QPainterPath()
            path.addRoundedRect(self.boundingRect(), self.radius, self.radius)
            painter.setBrush(self.brush())
            painter.setPen(self.pen())
            painter.drawPath(path)
        else:
            super().paint(painter, option, widget)

        if self.glass:
            self.draw_glass_effect(painter)

    def draw_glass_effect(self, painter):
        """Dessine l'effet de verre en fonction du type de forme avec clipping."""
        rect = self.boundingRect()

        # Créer un dégradé général pour simuler l'effet glass
        gradient = QLinearGradient(rect.topLeft(), rect.bottomLeft())
        gradient.setColorAt(0.0, QColor(255, 255, 255, 120))  # Blanc semi-transparent en haut
        gradient.setColorAt(0.5, QColor(255, 255, 255, 60))  # Moins opaque au milieu
        gradient.setColorAt(1.0, QColor(255, 255, 255, 0))  # Transparent en bas
        glass_brush = QBrush(gradient)

        painter.setBrush(glass_brush)
        painter.setPen(Qt.NoPen)

        # Clipper l'effet pour l'adapter à la forme actuelle
        path = QPainterPath()

        if self.shape_type == 'Rectangle':
            path.addRect(rect)
            painter.setClipPath(path)
            self.draw_glass_rectangle(painter, rect)
        elif self.shape_type == 'Ellipse':
            path.addEllipse(rect)
            painter.setClipPath(path)
            self.draw_glass_full_ellipse(painter, rect)
        else:
            path = self.get_shape_path(rect)
            painter.setClipPath(path)
            self.draw_glass_generic_shape(painter, rect)

    def draw_glass_rectangle(self, painter, rect):
        """Dessine l'effet glass avec une demi-ellipse pour les rectangles."""
        # Demi-ellipse au centre du rectangle pour l'effet incurvé
        ellipse_rect = QRectF(rect.left(), rect.top(), rect.width(), rect.height() * 0.6)
        painter.drawPie(ellipse_rect, 180 * 16, 180 * 16)  # Arc de 180° (demi-ellipse inversée)
        ellipse_rect.setHeight(rect.height() * 0.3)
        painter.drawRoundedRect(ellipse_rect, 0, 0)

    def draw_glass_full_ellipse(self, painter, rect):
        """Dessine un effet glass complet pour les ellipses."""
        # Le clipping est déjà appliqué pour restreindre le rendu à l'ellipse
        painter.drawEllipse(rect)

    def draw_glass_generic_shape(self, painter, rect):
        """Dessine un effet glass générique pour les autres formes géométriques."""
        # Appliquer le gradient uniquement sur la partie supérieure de la forme
        glass_rect = QRectF(rect.left(), rect.top(), rect.width(), rect.height() / 2)
        painter.drawRect(glass_rect)

    def get_shape_path(self, rect):
        """Crée et retourne un chemin basé sur le type de la forme pour appliquer le clipping."""
        path = QPainterPath()

        if self.shape_type == 'Losange':
            path.moveTo(rect.center().x(), rect.top())  # Haut milieu
            path.lineTo(rect.right(), rect.center().y())  # Droite milieu
            path.lineTo(rect.center().x(), rect.bottom())  # Bas milieu
            path.lineTo(rect.left(), rect.center().y())  # Gauche milieu
            path.closeSubpath()

        elif self.shape_type == 'Triangle':
            path.moveTo(rect.center().x(), rect.top())  # Haut
            path.lineTo(rect.right(), rect.bottom())  # Bas droite
            path.lineTo(rect.left(), rect.bottom())  # Bas gauche
            path.closeSubpath()

        elif self.shape_type == 'Parallélogramme':
            offset = rect.width() * 0.2
            path.moveTo(rect.left() + offset, rect.top())  # Point haut gauche déplacé
            path.lineTo(rect.right(), rect.top())  # Point haut droite
            path.lineTo(rect.right() - offset, rect.bottom())  # Point bas droite
            path.lineTo(rect.left(), rect.bottom())  # Point bas gauche
            path.closeSubpath()

        elif self.shape_type == 'Hexagone':
            path.moveTo(rect.center().x(), rect.top())  # Haut milieu
            path.lineTo(rect.right(), rect.top() + rect.height() * 0.25)  # Droite haut
            path.lineTo(rect.right(), rect.bottom() - rect.height() * 0.25)  # Droite bas
            path.lineTo(rect.center().x(), rect.bottom())  # Bas milieu
            path.lineTo(rect.left(), rect.bottom() - rect.height() * 0.25)  # Gauche bas
            path.lineTo(rect.left(), rect.top() + rect.height() * 0.25)  # Gauche haut
            path.closeSubpath()

        else:
            # Par défaut, un rectangle
            path.addRect(rect)

        return path

    def init_text(self):
        """Initialise le texte associé à la forme."""
        self.text_item = EditableTextItem(self.properties.value, self)
        self.text_item.setFont(QFont(self.font.name, self.font.size))
        self.text_item.setDefaultTextColor(QColor(self.font.color))
        self.update_text_position()

    def update_text_position(self):
        """Met à jour la position du texte pour le centrer dans la forme."""
        text_rect = self.text_item.boundingRect()
        # Calculer le décalage nécessaire pour centrer le texte
        x = self.x + (self.boundingRect().width() - text_rect.width()) / 2
        y = self.y + (self.boundingRect().height() - text_rect.height()) / 2
        # Appliquer la nouvelle position du texte
        self.text_item.setPos(x, y)

    def text_changed(self, new_text):
        """Met à jour la propriété de texte quand il est modifié."""
        self.properties.value = new_text
        self.update_text_position()

    def init_crosses(self):
        """Initialise les petites croix le long du rectangle."""
        cross_size = 9  # Taille des croix réduite à 5
        cross_color = QColor(0, 220, 255, 255)  # Bleu clair avec opacité complète

        rect = self.boundingRect()  # Utiliser les dimensions actuelles du rectangle

        # Positions des croix autour du rectangle (quatre côtés)
        positions = [
            (rect.center().x(), rect.top()),  # Haut milieu
            (rect.center().x(), rect.bottom()),  # Bas milieu
            (rect.left(), rect.center().y()),  # Gauche milieu
            (rect.right(), rect.center().y())  # Droite milieu
        ]

        for x, y in positions:
            cross = CrossItem(x, y, cross_size, cross_color, self)
            cross.setVisible(False)
            self.crosses.append(cross)

    def update_crosses(self):
        """Met à jour les positions des croix après redimensionnement ou changement de position."""
        rect = self.boundingRect()  # Utiliser les dimensions actuelles du rectangle

        # Positions des croix autour du rectangle (quatre côtés)
        positions = [
            (rect.center().x(), rect.top()),  # Haut milieu
            (rect.center().x(), rect.bottom()),  # Bas milieu
            (rect.left(), rect.center().y()),  # Gauche milieu
            (rect.right(), rect.center().y())  # Droite milieu
        ]

        # Repositionner chaque croix en fonction des nouvelles positions calculées
        for cross, (x, y) in zip(self.crosses, positions):
            if rect.contains(x, y):  # Vérifier que la nouvelle position est dans les limites du rectangle
                cross.setRect(x - cross.size / 2, y - cross.size / 2, cross.size, cross.size)
                cross.prepareGeometryChange()

    def init_handles(self):
        cross_size = 8
        cross_color = QColor(0, 120, 255, 128)  # Bleu clair avec opacité complète

        for x, y, direction, cursor in self.get_positions():
            handle = HandleItem(x, y, cross_size, cross_color, direction, self)
            handle.setCursor(cursor)
            handle.setVisible(False)
            self.handles.append(handle)

    def update_handles(self, visible=True):
        """Met à jour les positions des poignées après redimensionnement ou changement de position."""
        cross_size = 8  # Taille des poignées (croix)
        # Repositionner chaque poignée en fonction des nouvelles positions calculées
        for handle, (x, y, direction, cursor) in zip(self.handles, self.get_positions()):
            handle.setRect(x - handle.size() / 2, y - handle.size() / 2, handle.size(), handle.size())
            handle.direction = direction  # Assigner la direction correcte à la poignée

            if handle.is_selected:
                handle.setVisible(True)
                handle.setCursor(Qt.BlankCursor)
            else:
                handle.setCursor(cursor)  # Mettre à jour le curseur
                handle.setVisible(visible)

    def update_geometry(self, x, y, width, height, direction):
        """Mise à jour de la géométrie et du chemin de la forme."""
        if direction == ResizeDirection.V:
            self.y = y  # Changer la position X uniquement
            self.height = height

        elif direction == ResizeDirection.H:
            self.x = x  # Changer la position X uniquement
            self.width = width

        else:
            self.x = x
            self.y = y

            self.width = width
            self.height = height

        # Recalculer la forme en fonction de la nouvelle géométrie
        self.init_shape()
        self.update_text_position()
        self.update_crosses()

    def init_shape(self):
        """Initialise la forme en fonction du type détecté."""
        path = QPainterPath()

        if self.shape_type == 'Rectangle':
            if self.rounded:
                path.addRoundedRect(self.x, self.y, self.width, self.height, self.radius, self.radius)
            else:
                path.addRect(self.x, self.y, self.width, self.height)

        elif self.shape_type == 'Ellipse':
            path.addEllipse(self.x, self.y, self.width, self.height)

        elif self.shape_type == 'Losange':
            path.moveTo(self.x + self.width / 2, self.y)
            path.lineTo(self.x + self.width, self.y + self.height / 2)
            path.lineTo(self.x + self.width / 2, self.y + self.height)
            path.lineTo(self.x, self.y + self.height / 2)
            path.closeSubpath()

        elif self.shape_type == 'Triangle':
            path.moveTo(self.x + self.width / 2, self.y)
            path.lineTo(self.x + self.width, self.y + self.height)
            path.lineTo(self.x, self.y + self.height)
            path.closeSubpath()

        elif self.shape_type == 'Parallélogramme':
            offset = self.width * 0.2
            path.moveTo(self.x + offset, self.y)
            path.lineTo(self.x + self.width, self.y)
            path.lineTo(self.x + self.width - offset, self.y + self.height)
            path.lineTo(self.x, self.y + self.height)
            path.closeSubpath()

        elif self.shape_type == 'Hexagone':
            path.moveTo(self.x + self.width * 0.5, self.y)
            path.lineTo(self.x + self.width, self.y + self.height * 0.25)
            path.lineTo(self.x + self.width, self.y + self.height * 0.75)
            path.lineTo(self.x + self.width * 0.5, self.y + self.height)
            path.lineTo(self.x, self.y + self.height * 0.75)
            path.lineTo(self.x, self.y + self.height * 0.25)
            path.closeSubpath()

        # Appliquer le chemin à l'élément
        self.setPath(path)

    @property
    def id(self):
        return self.properties.id

    @property
    def value(self):
        return self.properties.value

    @property
    def style(self):
        return self.properties.style

    @property
    def geometry(self):
        return self.properties.geometry

    @property
    def font_details(self):
        return self.properties.font

    def update_font(self, style=None, color=None, size=None):
        if style is not None:
            self.properties.font.style = style
        if color is not None:
            self.properties.font.color = color
        if size is not None:
            self.properties.font.size = size
        self.text_item.setFont(self.properties.font.name, self.properties.font.size)
        self.text_item.setDefaultTextColor(QColor(self.properties.font.color))

    def __str__(self):
        return (f"RectangleShape(value={self.value}, x={self.x}, y={self.y}, width={self.width}, height={self.height}, "
                f"font=Font(style={self.font.style}, color={self.font.color}, size={self.font.size}))")
