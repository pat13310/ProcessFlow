from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QProgressBar, QStatusBar
from PySide6.QtCore import QTimer
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Barre d'État avec plusieurs panneaux")

        # Créer plusieurs widgets pour la barre d'état
        label_left = QLabel("Panneau Gauche")
        progress_bar = QProgressBar()
        progress_bar.setMaximum(100)
        progress_bar.setValue(75)
        label_right = QLabel("Panneau Droit")

        # Ajouter les widgets permanents à la barre d'état
        self.statusBar().addPermanentWidget(label_left, 1)  # Panneau gauche
        self.statusBar().addPermanentWidget(progress_bar, 2)  # Panneau central (barre de progression)
        self.statusBar().addPermanentWidget(label_right, 1)  # Panneau droit

        # Ajouter un message temporaire dans la barre d'état
        self.statusBar().showMessage("Message temporaire : Chargement en cours...", 5000)  # 5 secondes

        # Après 5 secondes, remplacer le message temporaire par un pane temporaire (label temporaire)
        QTimer.singleShot(5000, self.show_temporary_pane)

    def show_temporary_pane(self):
        # Créer un label temporaire et l'ajouter à la barre d'état de manière temporaire
        temp_label = QLabel("Panneau Temporaire")

        # Ajouter le widget temporaire à la barre d'état (en utilisant addWidget, donc il n'est pas permanent)
        self.statusBar().addWidget(temp_label, 1)

        # Supprimer ce panneau temporaire après 3 secondes
        QTimer.singleShot(3000, lambda: self.statusBar().removeWidget(temp_label))


# Initialisation de l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
