from PySide6.QtCore import QObject, QRunnable, Signal, Slot, QThreadPool


class TaskState:
    RUNNING = "en cours"
    STOPPED = "arrêtée"
    PAUSED = "en pause"


class TaskSignals(QObject):
    # Signaux pour notifier des changements d'état
    signalStateChanged = Signal(object)
    result = Signal(object)  # Signal pour transmettre le résultat
    error = Signal(Exception)  # Signal pour transmettre une exception


class Task(QRunnable):
    def __init__(self, name: str, worker_function=None,*args, **kwargs):
        super().__init__()
        self.name = name
        self.worker_function = worker_function
        self.args = args
        self.kwargs = kwargs
        self.state = TaskState.STOPPED
        self.signals = TaskSignals()
        self._is_paused = False
        self._is_running = False

    @Slot()
    def run(self):
        """Exécute la tâche dans un thread séparé."""
        self._is_running = True

        if self.worker_function:
            try:
                print(f"Tâche '{self.name}' démarrée")
                self.state = TaskState.RUNNING
                self.signals.signalStateChanged.emit(self.state)
                print("Appel de la fonction...")
                result = self.worker_function(*self.args, **self.kwargs)
                self.signals.result.emit(result)
            except Exception as e:
                self.signals.error.emit(e)
                self._is_running = False
        else:
            self.signals.error.emit("aucune fonction")

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
            'Tâche': self.name,
            'État': self.state
        }

    def reset(self):
        """Réinitialise la tâche pour permettre son redémarrage."""
        self._is_paused = False
        self._is_running = False
        self.state = TaskState.STOPPED
        self.signals.signalStateChanged.emit(self.state)
        print(f"Tâche '{self.name}' réinitialisée")

    def set_worker_function(self, func, *args, **kwargs):
        """Définit une fonction worker à appeler avec ses arguments."""
        if callable(func):
            self.worker_function = func
            self.args = args
            self.kwargs = kwargs
        else:
            raise ValueError("La fonction fournie n'est pas appelable")
