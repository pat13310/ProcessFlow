from PySide6.QtCore import QPointF
from PySide6.QtGui import QPen, QColor, QFont
from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsTextItem, QGraphicsRectItem


class XLine(QGraphicsLineItem):
    def __init__(self, source_shape, target_shape, properties, label_text="Connection", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source_shape = source_shape
        self.target_shape = target_shape
        self.properties = properties
        self.style = self.properties.get("style", "")

        # Définir l'apparence de la ligne
        self.setPen(QPen(QColor("#000000"), 2))  # Ligne noire de 2px

        # Ajouter un texte centré sur la ligne
        self.text_item = QGraphicsTextItem(label_text, self)
        self.text_item.setFont(QFont("Arial", 10))
        self.text_item.setDefaultTextColor(QColor("#000000"))

        # Enregistrer la ligne dans les formes source et cible
        self.source_shape.add_connected_line(self)
        self.target_shape.add_connected_line(self)

        # Charger les propriétés et mettre à jour la position de la ligne
        self.load_properties()
        self.update_line_position()

    def extract_style_value(self, style, key, default):
        """Extrait une valeur spécifique d'une chaîne de style sous forme 'clé=valeur'."""
        try:
            return float(style.get(key, default))
        except (ValueError, KeyError):
            return default

    def load_properties(self):
        style_parts = dict(part.split('=') for part in self.style.split(';') if '=' in part)

        # Récupérer les paramètres exit et entry
        self.exit_x = self.extract_style_value(style_parts, 'exitX', 0.5)
        self.exit_y = self.extract_style_value(style_parts, 'exitY', 0.5)
        self.exit_dx = self.extract_style_value(style_parts, 'exitDx', 0.0)
        self.exit_dy = self.extract_style_value(style_parts, 'exitDy', 0.0)

        self.entry_x = self.extract_style_value(style_parts, 'entryX', 0.5)
        self.entry_y = self.extract_style_value(style_parts, 'entryY', 0.5)
        self.entry_dx = self.extract_style_value(style_parts, 'entryDx', 0.0)
        self.entry_dy = self.extract_style_value(style_parts, 'entryDy', 0.0)

    def update_line_position(self):
        """Met à jour la position de la ligne en fonction des points de sortie et d'entrée."""
        source_rect = self.source_shape.boundingRect()
        target_rect = self.target_shape.boundingRect()

        # Point de sortie de la forme source (global)
        source_exit_point = self.source_shape.mapToScene(
            QPointF(
                source_rect.left() + self.exit_x * source_rect.width() + self.exit_dx,
                source_rect.top() + self.exit_y * source_rect.height() + self.exit_dy
            )
        )

        # Point d'entrée dans la forme cible (global)
        target_entry_point = self.target_shape.mapToScene(
            QPointF(
                target_rect.left() + self.entry_x * target_rect.width() + self.entry_dx,
                target_rect.top() + self.entry_y * target_rect.height() + self.entry_dy
            )
        )
        # Mettre à jour la ligne entre ces deux points
        self.setLine(source_exit_point.x(), source_exit_point.y(), target_entry_point.x(), target_entry_point.y())

        # Mettre à jour la position du texte pour qu'il soit centré sur la ligne
        self.update_text_position(source_exit_point, target_entry_point)

    def update_text_position(self, source_point, target_point):
        """Met à jour la position du texte pour qu'il soit centré au-dessus de la ligne."""
        # Calculer le milieu de la ligne
        mid_x = (source_point.x() + target_point.x()) / 2
        mid_y = (source_point.y() + target_point.y()) / 2

        # Obtenir les dimensions du texte
        text_rect = self.text_item.boundingRect()

        # Positionner le texte centré au-dessus de la ligne
        self.text_item.setPos(mid_x - text_rect.width() / 2, mid_y - text_rect.height() / 2 - 8)

    def update_on_shape_move(self):
        """Met à jour la ligne lorsque l'une des formes est déplacée."""
        self.update_line_position()
