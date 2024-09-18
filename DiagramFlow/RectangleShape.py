from PySide6.QtCore import Qt, QPointF, QThreadPool
from PySide6.QtGui import QBrush, QPen, QColor, QFont, QAction
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsTextItem, QMenu

from DiagramFlow.SignalShape import SignalShape
from LineFlow.IOPort import IOPort
from Process.Task import Task, TaskState


class RectangleShape(QGraphicsRectItem):

    def __init__(self, x, y, width, height, shape_name: str,
                 task: Task = None, default_color=QColor("#FFC8C8"), selected_color=QColor("#C8C8FF"), grid=25):
        super().__init__(x, y, width, height)
        self.signals = SignalShape()
        self.connections = []
        self.shape_name = shape_name
        self.task = task  # Peut être None au départ
        self.handles = []
        self.connection_points = []
        self.grid = grid

        # Couleurs pour différents états
        self.color_running = QColor("#A8FF8A")  # Vert clair pour "Running"
        self.color_stopped = QColor("#FF8A8A")  # Rouge clair pour "Stopped"
        self.color_paused = QColor("#FFFF8A")  # Jaune clair pour "Paused"

        # Apparence par défaut
        self.default_pen = QPen(QColor("#000000"), 1)
        self.selected_pen = QPen(QColor("#0000FF"), 1, Qt.DashLine)
        self.current_pen = self.default_pen
        self.default_brush = QBrush(default_color)
        self.selected_brush = QBrush(selected_color)
        self.current_brush = self.default_brush
        self.setPen(self.current_pen)
        self.setBrush(self.current_brush)

        # Flags pour l'interactivité
        self.setAcceptHoverEvents(True)
        self.setFlags(QGraphicsRectItem.ItemIsMovable |
                      QGraphicsRectItem.ItemSendsGeometryChanges |
                      QGraphicsRectItem.ItemIsSelectable)

        # Initialisation
        self.init_handles()
        self.init_connection_points()
        self.init_text()
        self.position = QPointF(x, y)
        self.snap_to_grid()

        # Connexion des signaux de l'état de la tâche
        if self.task:
            self.task.signals.signalStateChanged.connect(self.update_appearance)

    def init_handles(self):
        """Initialise les poignées pour redimensionner la forme."""
        for _ in range(4):
            handle = QGraphicsRectItem(0, 0, 6, 6, self)
            handle.setPen(QPen(QColor("#AFFA00"), 2, Qt.SolidLine))
            handle.setBrush(QBrush(QColor("#FFFF00")))
            handle.setVisible(False)
            self.handles.append(handle)
        self.update_handles()

    def init_connection_points(self):
        """Initialise les points de connexion (ports d'entrée et de sortie)."""
        self.left_port = IOPort(self, is_input=True)
        self.right_port = IOPort(self, is_input=False)
        self.connection_points.append(self.left_port)
        self.connection_points.append(self.right_port)
        self.calculate_positions()

    def init_text(self):
        """Initialise le texte associé à la forme."""
        display_text = self.get_display_text()
        self.text_item = QGraphicsTextItem(display_text, self)
        self.text_item.setFont(QFont("Arial", 9))
        self.update_text_position()

    def get_display_text(self):
        """Génère le texte à afficher sur la forme."""
        if self.task:
            return f"{self.shape_name}\n({self.task.name})"
        return self.shape_name

    def update_handles(self):
        """Met à jour les positions des poignées en fonction de la forme."""
        rect = self.rect()
        positions = [rect.topLeft(), rect.topRight(), rect.bottomLeft(), rect.bottomRight()]
        for handle, pos in zip(self.handles, positions):
            handle.setPos(pos - QPointF(3, 3))

    def set_selected(self, selected):
        """Change l'état de sélection de la forme."""
        if selected:
            self.emit_properties()
        for handle in self.handles:
            handle.setVisible(selected)

        if not self.task:
            self.current_pen = self.selected_pen if selected else self.default_pen
            self.current_brush = self.selected_brush if selected else self.default_brush

        self.setPen(self.current_pen)
        self.setBrush(self.current_brush)

    def emit_properties(self):
        """Émet les propriétés actuelles de la forme."""
        x, y = self.scenePos().x(), self.scenePos().y()
        properties = {
            'Type de forme': 'RectangleShape',
            'Nom de la forme': self.shape_name,
            'Position X': x,
            'Position Y': y,
            'Largeur': self.rect().width(),
            'Hauteur': self.rect().height()
        }

        if self.task:
            properties.update(self.task.get_properties())

        self.signals.propertiesChanged.emit(properties)

    def mousePressEvent(self, event):
        """Gestion de l'événement de clic de souris."""
        self.set_selected(True)
        super().mousePressEvent(event)

    def itemChange(self, change, value):
        """Gestion des changements d'état de l'élément."""
        if change == QGraphicsRectItem.ItemPositionChange:
            # Calcule la nouvelle position alignée sur la grille
            new_pos = self.snap_to_grid_position(value)

            # Émet un signal de changement de position
            self.signals.positionChanged.emit(new_pos)

            # Émet les propriétés mises à jour
            self.emit_properties()

            # Met à jour les poignées, les points de connexion, et la position du texte
            self.update_handles()
            self.update_connection_points()
            self.update_text_position()

            # Notifie toutes les connexions associées
            self.notify_connections()

            return new_pos

        elif change == QGraphicsRectItem.ItemSelectedChange:
            self.set_selected(value)

        return super().itemChange(change, value)

    def calculate_positions(self):
        """Calcule les positions des points de connexion."""
        rect = self.rect()
        self.left_port.setPos(rect.left() - 5, rect.center().y() - 5)
        self.right_port.setPos(rect.right() - 5, rect.center().y() - 5)

    def update_connection_points(self):
        """Met à jour les positions des points de connexion."""
        self.calculate_positions()

    def update_text_position(self):
        """Met à jour la position du texte pour le centrer dans la forme."""
        rect = self.rect()
        self.text_item.setPos(rect.center() - self.text_item.boundingRect().center())

    def snap_to_grid(self):
        """Aligne la forme sur la grille."""
        self.setPos(self.snap_to_grid_position(self.pos()))

    def snap_to_grid_position(self, position):
        """Calcule la position alignée sur la grille la plus proche."""
        self.position = QPointF(
            round(position.x() / self.grid) * self.grid,
            round(position.y() / self.grid) * self.grid)
        return self.position

    def add_connection(self, connection):
        """Ajoute une connexion à la liste des connexions associées."""
        if connection not in self.connections:
            self.connections.append(connection)

    def remove_connection(self, connection):
        """Supprime une connexion de la liste des connexions associées."""
        if connection in self.connections:
            self.connections.remove(connection)

    def notify_connections(self):
        """Notifie toutes les connexions associées d'une mise à jour."""
        for connection in self.connections:
            connection.update_position()

    def set_task(self, new_task):
        """Associe une nouvelle tâche à la forme."""
        self.task = new_task
        self.update_text_position()

    def get_input_port(self):
        """Retourne le port d'entrée de la forme."""
        return self.left_port

    def get_output_port(self):
        """Retourne le port de sortie de la forme."""
        return self.right_port

    def contextMenuEvent(self, event):
        """Affiche un menu contextuel lors d'un clic droit sur le rectangle."""
        menu = QMenu()

        # Ajouter des actions au menu
        run_action = QAction("Démarrer", menu)
        stop_action = QAction("Arrêter", menu)
        pause_action = QAction("Pause", menu)

        # Connecter les actions aux fonctions de slot correspondantes
        run_action.triggered.connect(self.run_process)
        stop_action.triggered.connect(self.stop_process)
        pause_action.triggered.connect(self.pause_process)

        # Ajouter les actions au menu
        menu.addAction(run_action)
        menu.addAction(stop_action)
        menu.addAction(pause_action)
        menu.exec(event.screenPos())

    def run_process(self):
        """Exécute la tâche associée au rectangle."""
        if self.task is None or self.task.get_state() == TaskState.STOPPED:
            self.task = Task(self.shape_name)  # Créer une nouvelle instance de Task
            self.task.signals.signalStateChanged.connect(self.update_appearance)

        # Exécuter la nouvelle tâche dans un thread séparé via le thread pool
        QThreadPool.globalInstance().start(self.task)
        self.emit_properties()

    def stop_process(self):
        """Arrête la tâche associée au rectangle."""
        print("Stop action triggered")
        if self.task:
            self.task.stop()  # Arrête la tâche
        self.emit_properties()

    def pause_process(self):
        """Met en pause la tâche associée au rectangle."""
        print("Pause action triggered")
        if self.task:
            self.task.pause()  # Met en pause la tâche
        self.emit_properties()

    def update_appearance(self, state):
        """Met à jour l'apparence de la forme en fonction de l'état de la tâche."""
        if state == TaskState.RUNNING:
            self.current_brush = QBrush(self.color_running)
        elif state == TaskState.STOPPED:
            self.current_brush = QBrush(self.color_stopped)
        elif state == TaskState.PAUSED:
            self.current_brush = QBrush(self.color_paused)

        # Applique le pinceau mis à jour à l'élément
        self.setBrush(self.current_brush)
        self.update()
        if self.scene():
            self.scene().invalidate(self.boundingRect())
