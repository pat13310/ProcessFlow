from PySide6.QtGui import Qt
from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem


from PySide6.QtGui import QTextCursor

class EditableTextItem(QGraphicsTextItem):
    """QGraphicsTextItem modifiable lors d'un double-clic."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)

    def mouseDoubleClickEvent(self, event):
        """Activer l'édition du texte lors d'un double-clic."""
        self.setTextInteractionFlags(Qt.TextEditorInteraction)  # Permet la modification du texte
        self.setFocus()  # Donner le focus pour activer la saisie
        super().mouseDoubleClickEvent(event)

    def focusOutEvent(self, event):
        """Terminer l'édition du texte lorsque le focus est perdu."""
        self.setTextInteractionFlags(Qt.NoTextInteraction)  # Désactiver la modification
        self.deselect_text()  # Désélectionner le texte
        self.setCursor(Qt.ArrowCursor)  # Réinitialiser le curseur en mode flèche
        self.parentItem().text_changed(self.toPlainText())  # Mettre à jour le texte de l'élément parent
        super().focusOutEvent(event)

    def keyPressEvent(self, event):
        """Terminer l'édition du texte lors de la validation (touche Entrée)."""
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.clearFocus()  # Enlever le focus pour valider
            self.setCursor(Qt.ArrowCursor)  # Réinitialiser le curseur en mode flèche
            self.deselect_text()  # Désélectionner le texte après validation
        else:
            super().keyPressEvent(event)

    def deselect_text(self):
        """Désélectionner le texte en réinitialisant le curseur sans sélection."""
        cursor = self.textCursor()  # Récupérer le curseur actuel
        cursor.clearSelection()  # Désélectionner tout
        self.setTextCursor(cursor)  # Appliquer le nouveau curseur sans sélection
