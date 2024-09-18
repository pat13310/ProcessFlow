from PySide6.QtCore import QObject, QRunnable, Signal, Slot, QThreadPool


class TaskState:
    RUNNING = "running"
    STOPPED = "stopped"
    PAUSED = "paused"


class TaskSignals(QObject):
    # Signaux pour notifier des changements d'état
    signalStateChanged = Signal(object)


class Task(QRunnable):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.state = TaskState.STOPPED
        self.signals = TaskSignals()
        self._is_paused = False
        self._is_running = False

    @Slot()
    def run(self):
        """Exécute la tâche dans un thread séparé."""
        self._is_running = True
        self.state = TaskState.RUNNING
        self.signals.signalStateChanged.emit(self.state)
        print(f"Tâche '{self.name}' démarrée")

        # Simulation d'une tâche longue
        for i in range(10):  # Simulez un processus long
            if not self._is_running:
                break
            if self._is_paused:
                print(f"Tâche '{self.name}' en pause")
                while self._is_paused:
                    pass  # Attendre que la tâche soit reprise

            print(f"Exécution de la tâche '{self.name}' : étape {i+1}")
            # Simuler une pause de 1 seconde
            QThreadPool.globalInstance().waitForDone(1000)

        if self._is_running:
            self.state = TaskState.STOPPED
            self.signals.signalStateChanged.emit(self.state)
            print(f"Tâche '{self.name}' terminée")
        self._is_running = False

    def stop(self):
        """Arrête la tâche."""
        self._is_running = False
        self.state = TaskState.STOPPED
        self.signals.signalStateChanged.emit(self.state)
        print(f"Tâche '{self.name}' arrêtée")

    def pause(self):
        """Met la tâche en pause."""
        self._is_paused = True
        self.state = TaskState.PAUSED
        self.signals.signalStateChanged.emit(self.state)
        print(f"Tâche '{self.name}' en pause")

    def resume(self):
        """Reprend la tâche après une pause."""
        self._is_paused = False
        self.state = TaskState.RUNNING
        self.signals.signalStateChanged.emit(self.state)
        print(f"Tâche '{self.name}' reprise")

    def get_state(self):
        """Retourne l'état actuel de la tâche."""
        return self.state

    def get_properties(self):
        """Retourne un dictionnaire des propriétés de la tâche."""
        return {
            'Nom de la tâche': self.name,
            'État de la tâche': self.state
        }

    def reset(self):
        """Réinitialise la tâche pour permettre son redémarrage."""
        self._is_paused = False
        self._is_running = False
        self.state = TaskState.STOPPED
        self.signals.signalStateChanged.emit(self.state)
        print(f"Tâche '{self.name}' réinitialisée")
