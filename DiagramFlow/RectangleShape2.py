import dataclasses

from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QBrush, QColor, QLinearGradient, QPen, QCursor, QFont, QPainterPath, QPainter
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsDropShadowEffect, QGraphicsTextItem, QGraphicsEllipseItem, \
    QGraphicsItem


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
        font_name="Helvetica"
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


class CrossItem(QGraphicsEllipseItem):
    def __init__(self, x, y, size, color, parent=None):
        super().__init__(x - size / 2, y - size / 2, size, size, parent)
        self.color = color
        self.size = size
        self.x = x
        self.y = y
        self.setPen(QPen(self.color))
        self.setBrush(QBrush(self.color))
        self.setVisible(False)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsRectItem.ItemIsMovable, False)
        self.original_rect = self.rect()  # Stocker le rectangle original


    def hoverEnterEvent(self, event):
        color = QColor(50, 200, 0, 160)
        pen=QPen(color)
        pen.setWidth(10)
        self.setPen(pen)
        self.setBrush(QBrush(color))
        if self.parentItem() is not None:
            self.parentItem().setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setCursor(Qt.ArrowCursor)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        # Revenir à la couleur et la taille d'origine après avoir quitté le survol
        self.setPen(QPen(self.color))
        self.setBrush(QBrush(self.color))


        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if self.parentItem() is not None:
             self.parentItem().setFlag(QGraphicsItem.ItemIsSelectable, False)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.parentItem() is not None:
            self.parentItem().setFlag(QGraphicsItem.ItemIsSelectable, True)
        super().mouseReleaseEvent(event)



class HandleItem(QGraphicsEllipseItem):
    def __init__(self, x, y, size, color, direction, parent=None, min_size=20, max_size=500, maintain_aspect_ratio=False):
        super().__init__(x - size / 2, y - size / 2, size, size, parent)
        self.color = color
        self._size = size
        self.parent_item = parent  # Référence au rectangle parent
        self.setPen(QPen(self.color))
        self.setBrush(QBrush(self.color))
        self.direction = direction  # Direction de redimensionnement
        self.setVisible(False)
        self.setAcceptHoverEvents(True)
        self.cursor = Qt.ArrowCursor
        self.setCursor(self.cursor)
        self.setZValue(2)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)  # Permettre le déplacement de l'item
        self.min_size = min_size  # Taille minimale du rectangle parent
        self.max_size = max_size  # Taille maximale du rectangle parent
        self.maintain_aspect_ratio = maintain_aspect_ratio  # Conserver le rapport largeur/hauteur

        # Variables pour stocker les dimensions originales pour maintenir le rapport
        self.original_width = self.parent_item.rect().width()
        self.original_height = self.parent_item.rect().height()
        self.aspect_ratio = self.original_width/self.original_height

    def size(self):
        return float(self._size)

    def set_cursor(self, cursor):
        self.cursor = cursor
        self.setCursor(self.cursor)

    def hoverEnterEvent(self, event):
        """Changer la couleur des poignées lors du survol."""
        self.setBrush(QBrush(QColor(255, 239, 50, 220)))  # Rouge lors du survol pour plus de visibilité
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        """Revenir à la couleur d'origine après avoir quitté le survol."""
        self.setBrush(QBrush(self.color))  # Retour à la couleur d'origine
        super().hoverLeaveEvent(event)

    def mouseReleaseEvent(self, event):
        self.setFlag(QGraphicsItem.ItemIsMovable, True)


    def mouseMoveEvent(self, event):
        """Gère le déplacement de la poignée et ajuste la taille du rectangle parent en fonction de la direction."""
        new_pos = self.parent_item.mapFromScene(event.scenePos())  # Obtenir la position dans le référentiel du parent
        #new_pos = event.screenPos()  # Obtenir la position dans le référentiel du parent
        rect = self.parent_item.rect()  # Rectangle actuel du parent
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        # Redimensionnement en fonction de la direction de la poignée
        self.prepareGeometryChange()
        if self.direction == 'horizontal':
            dx = new_pos.x() - rect.left()  # Décalage par rapport à la gauche
            new_width = max(self.min_size, min(self.max_size, dx))  # Empêcher une largeur trop petite ou trop grande
            self.parent_item.update_geometry(rect.left(), rect.top(), new_width, rect.height())

        elif self.direction == 'vertical':
            dy = new_pos.y() - rect.top()  # Décalage par rapport au haut
            new_height = max(self.min_size, min(self.max_size, dy))  # Empêcher une hauteur trop petite ou trop grande
            self.parent_item.update_geometry(rect.left(), rect.top(), rect.width(), new_height)

        elif self.direction == 'diagonal':
            dx = new_pos.x() - rect.left()
            dy = new_pos.y() - rect.top()

            if self.maintain_aspect_ratio:
                # Maintenir le ratio original (largeur / hauteur) si spécifié
                self.aspect_ratio = self.original_width / self.original_height
                new_width = max(self.min_size, min(self.max_size, dx))
                new_height = new_width / self.aspect_ratio
            else:
                new_width = max(self.min_size, min(self.max_size, dx))
                new_height = max(self.min_size, min(self.max_size, dy))
                self.aspect_ratio = new_width/ new_height


            self.parent_item.update_geometry(rect.left(), rect.top(), new_width, new_height)

        # Ne pas déplacer la poignée elle-même, elle sera repositionnée avec update_handles
        super().mouseMoveEvent(event)


class RectangleShape2(QGraphicsRectItem):
    def __init__(self, properties: Properties, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.properties = properties
        self.x = properties.geometry.x if properties.geometry else 0
        self.y = properties.geometry.y if properties.geometry else 0
        self.width = properties.geometry.width if properties.geometry else 100
        self.height = properties.geometry.height if properties.geometry else 50
        self.font = properties.font
        self.glass_type = properties.glass_type
        self.is_selected = False
        self.radius=10
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
        self.setRect(self.x, self.y, self.width, self.height)
        self.default_pen = QPen(QColor(stroke_color), 1)
        self.setPen(self.default_pen)

        if gradient_color:
            gradient = QLinearGradient(self.rect().topRight(), self.rect().bottomRight())
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

        self.init_crosses()
        self.init_handles()

        # Flags pour l'interactivité
        self.setAcceptHoverEvents(True)
        self.setFlags(QGraphicsRectItem.ItemIsMovable |
                      QGraphicsRectItem.ItemSendsGeometryChanges)

        # Définir le curseur par défaut
        self.setCursor(QCursor(Qt.SizeAllCursor))

    def mousePressEvent(self, event):
        self.is_selected = not self.is_selected

        """Gestion de l'événement de pression de souris."""
        for cross in self.crosses:
            cross.setVisible(not self.is_selected)
        for selected in self.handles:
            selected.setVisible(self.is_selected)

        self.setFlag(QGraphicsRectItem.ItemIsMovable, not self.is_selected)


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
        self.is_selected=False
        super().hoverLeaveEvent(event)

    def paint(self, painter, option, widget=None):
        """Redéfinit la méthode de peinture pour gérer les coins arrondis et l'effet glass."""
        painter.setRenderHint(QPainter.Antialiasing)
        if self.rounded:
            path = QPainterPath()
            path.addRoundedRect(self.rect(), self.radius, self.radius)
            painter.setBrush(self.brush())
            painter.setPen(self.pen())
            painter.drawPath(path)
        else:
            super().paint(painter, option, widget)

        if self.glass:
            self.draw_glass_effect(painter)
                # Ajout de l'effet de brillance pour donner l'effet glass
                # gradient = QLinearGradient(self.rect().topLeft(), self.rect().bottomLeft())
                # gradient.setColorAt(0.0, QColor(255, 255, 255, 180))  # Couleur blanche transparente au sommet
                # gradient.setColorAt(0.5, QColor(255, 255, 255, 100))  # Couleur blanche légèrement transparente
                # gradient.setColorAt(1.0, QColor(255, 255, 255, 0))  # Complètement transparent en bas
                # glass_brush = QBrush(gradient)
                # painter.setBrush(glass_brush)
                # painter.setPen(Qt.NoPen)
                # if self.glass_type == 1:
                #     # Dessiner une demi-ellipse inversée collée sur le bord supérieur
                #     rect = self.rect().adjusted(0, 0, 0, -self.height / 2)
                #     painter.drawPie(rect, 180 * 16,
                #                     180 * 16)  # Dessine une demi-ellipse inversée couvrant toute la partie supérieure
                #     rect.setHeight(rect.height() * 0.5)
                #     painter.drawRoundedRect(rect, 0, 0)

    def draw_glass_effect(self, painter):
        """Dessine l'effet de verre en haut de la forme."""


        # Selon le type de glass, dessiner une demi-ellipse ou un rectangle
        if self.glass_type == 1:  # Type demi-ellipse
            self.draw_glass_ellipse(painter)
        elif self.glass_type == 2:  # Type rectangle avec coins arrondis
            self.draw_glass_rect(painter)
        else:
            rect = self.rect()
            # Par défaut, on applique un effet de verre avec un rectangle semi-transparent
            rect_glass = QRectF(rect.left(), rect.top(), rect.width(), rect.height() / 2)
            painter.drawRect(rect_glass)

    def draw_glass_rect(self, painter):
        rect = self.rect()

        # Créer un dégradé pour l'effet de verre
        gradient = QLinearGradient(rect.topLeft(), rect.bottomLeft())
        gradient.setColorAt(0.0, QColor(255, 255, 255, 180))  # Couleur blanche semi-transparente au sommet
        gradient.setColorAt(0.5, QColor(255, 255, 255, 100))  # Couleur blanche légèrement transparente
        gradient.setColorAt(1.0, QColor(255, 255, 255, 0))  # Complètement transparent en bas
        glass_brush = QBrush(gradient)
        painter.setBrush(glass_brush)
        painter.setPen(Qt.NoPen)
        rect_glass = QRectF(rect.left() + 2, rect.top() + 2, rect.width() - 4, rect.height() / 2 - 4)
        painter.drawRoundedRect(rect_glass, self.radius, self.radius)

    def draw_glass_ellipse(self, painter):
        """Dessine un effet glass avec des courbes de Bézier pour créer un arrondi au milieu du haut du rectangle."""
        # Créer un dégradé pour simuler l'effet glass
        rect = self.rect()
        gradient = QLinearGradient(rect.topRight(), rect.bottomRight())
        gradient.setColorAt(0.0, QColor(255, 255, 255, 150))  # Blanc semi-transparent en haut
        gradient.setColorAt(0.5, QColor(255, 255, 255, 80))  # Moins opaque au milieu
        gradient.setColorAt(1.0, QColor(255, 255, 255, 0))  # Transparent vers le bas

        glass_brush = QBrush(gradient)
        painter.setBrush(glass_brush)
        # Dessiner une demi-ellipse au centre du rectangle pour l'effet incurvé
        ellipse_rect = QRectF(rect.left(), rect.top(), rect.width(), rect.height() * 0.6)
        painter.setBrush(gradient)  # Bleu clair semi-transparent
        painter.setPen(Qt.NoPen)

        # Demi-ellipse inversée (effet incurvé)
        painter.drawPie(ellipse_rect, 180*16, 180 * 16)  # Arc de 180°
        ellipse_rect.setHeight(rect.height()*0.3)
        painter.drawRoundedRect(ellipse_rect, 0, 0)

    def init_text(self):
        """Initialise le texte associé à la forme."""
        self.text_item = QGraphicsTextItem(self.properties.value, self)
        self.text_item.setFont(QFont("Arial", self.font.size))
        self.text_item.setDefaultTextColor(QColor(self.font.color))
        self.update_text_position()

    def update_text_position(self):
        """Met à jour la position du texte pour le centrer dans la forme."""
        rect = self.rect()
        self.text_item.setPos(rect.center() - self.text_item.boundingRect().center())

    def init_crosses(self):
        """Initialise les petites croix le long du rectangle."""
        cross_size = 9  # Taille des croix réduite à 5
        cross_color = QColor(0, 220, 255, 255)  # Bleu clair avec opacité complète

        rect = self.rect()  # Utiliser les dimensions actuelles du rectangle

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
        rect = self.rect()  # Utiliser les dimensions actuelles du rectangle

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
        rect = self.rect()  # Utiliser les dimensions actuelles du rectangle

        # Positions et directions des poignées autour du rectangle (huit positions)
        positions = [
            (rect.center().x(), rect.top(), 'vertical', Qt.SizeVerCursor),  # Haut milieu
            (rect.center().x(), rect.bottom(), 'vertical', Qt.SizeVerCursor),  # Bas milieu
            (rect.left(), rect.center().y(), 'horizontal', Qt.SizeHorCursor),  # Gauche milieu
            (rect.right(), rect.center().y(), 'horizontal', Qt.SizeHorCursor),  # Droite milieu
            (rect.topLeft().x(), rect.topLeft().y(), 'diagonal', Qt.SizeFDiagCursor),  # Point Haut gauche
            (rect.topRight().x(), rect.topRight().y(), 'diagonal', Qt.SizeBDiagCursor),  # Point Haut droit
            (rect.bottomLeft().x(), rect.bottomLeft().y(), 'diagonal', Qt.SizeBDiagCursor),  # Point Bas gauche
            (rect.bottomRight().x(), rect.bottomRight().y(), 'diagonal', Qt.SizeFDiagCursor)  # Point Bas droit
        ]

        for x, y, direction, cursor in positions:
            handle = HandleItem(x, y, cross_size, cross_color, direction, self)
            handle.set_cursor(cursor)
            handle.setVisible(False)
            self.handles.append(handle)

    def update_handles(self):
        """Met à jour les positions des poignées après redimensionnement ou changement de position."""
        cross_size = 8  # Taille des poignées (croix)
        rect = self.rect()  # Récupérer les dimensions actuelles du rectangle

        # Positions et directions des poignées autour du rectangle (huit positions)
        positions = [
            (rect.center().x(), rect.top(), 'vertical', Qt.SizeVerCursor),  # Haut milieu
            (rect.center().x(), rect.bottom(), 'vertical', Qt.SizeVerCursor),  # Bas milieu
            (rect.left(), rect.center().y(), 'horizontal', Qt.SizeHorCursor),  # Gauche milieu
            (rect.right(), rect.center().y(), 'horizontal', Qt.SizeHorCursor),  # Droite milieu
            (rect.topLeft().x(), rect.topLeft().y(), 'diagonal', Qt.SizeFDiagCursor),  # Point Haut gauche
            (rect.topRight().x(), rect.topRight().y(), 'diagonal', Qt.SizeBDiagCursor),  # Point Haut droit
            (rect.bottomLeft().x(), rect.bottomLeft().y(), 'diagonal', Qt.SizeBDiagCursor),  # Point Bas gauche
            (rect.bottomRight().x(), rect.bottomRight().y(), 'diagonal', Qt.SizeFDiagCursor)  # Point Bas droit
        ]
        # Repositionner chaque poignée en fonction des nouvelles positions calculées
        for handle, (x, y, direction, cursor) in zip(self.handles, positions):
            handle.setRect(x - handle.size() / 2, y - handle.size() / 2, handle.size(), handle.size())
            handle.direction = direction  # Assigner la direction correcte à la poignée
            handle.set_cursor(cursor)  # Mettre à jour le curseur

    def update_geometry(self, x, y, width, height):
        """Mise à jour de la géométrie du rectangle et repositionnement des éléments associés."""
        self.properties.geometry = Geometry(x, y, width, height)
        self.setRect(x, y, width, height)
        self.update_text_position()  # Mettre à jour la position du texte
        self.update_handles()  # Repositionner les poignées
        self.update_crosses()

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
        self.text_item.setFont(QFont("Arial", self.properties.font.size))
        self.text_item.setDefaultTextColor(QColor(self.properties.font.color))

    def __str__(self):
        return (f"RectangleShape(value={self.value}, x={self.x}, y={self.y}, width={self.width}, height={self.height}, "
                f"font=Font(style={self.font.style}, color={self.font.color}, size={self.font.size}))")
