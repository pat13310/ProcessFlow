from PySide6.QtCore import QObject, Signal
from enum import Enum

class ProcessState(Enum):
    INIT = "init"
    RUNNING = "marche"
    STOPPED = "arrêt"

class Process(QObject):
    # Définition d'un seul signal pour les changements d'état
    signalStateChanged = Signal(ProcessState)

    def __init__(self, name, process_type, inputs=None, outputs=None, state=ProcessState.INIT):
        """
        Initialise un nouveau processus.

        :param name: Le nom du processus.
        :param process_type: Le type du processus (e.g., 'Calcul', 'Décision', 'Entrée').
        :param inputs: Liste des entrées du processus.
        :param outputs: Liste des sorties du processus.
        :param state: État initial du processus (par défaut ProcessState.INIT).
        """
        super().__init__()  # Appel du constructeur de QObject
        self.name = name
        self.process_type = process_type
        self.inputs = inputs if inputs is not None else []
        self.outputs = outputs if outputs is not None else []
        self.state = state

    def add_input(self, input_data):
        """Ajoute une nouvelle entrée au processus."""
        self.inputs.append(input_data)

    def add_output(self, output_data):
        """Ajoute une nouvelle sortie au processus."""
        self.outputs.append(output_data)

    def set_state(self, new_state):
        """
        Modifie l'état du processus.

        :param new_state: Le nouvel état du processus (doit être une valeur de ProcessState).
        """
        if not isinstance(new_state, ProcessState):
            raise ValueError("État invalide pour le processus")

        if self.state != new_state:
            self.state = new_state
            self.signalStateChanged.emit(self.state)  # Émet le signal avec le nouvel état

    def get_properties(self):
        """Retourne un dictionnaire des propriétés du processus."""
        return {
            'Nom': self.name,
            'Type': self.process_type,
            'État': self.state.value,
            'Entrées': self.inputs,
            'Sorties': self.outputs
        }

    def get_state(self):
        return self.state.value

    def __str__(self):
        """Retourne une représentation textuelle du processus."""
        return f"Processus: {self.name}, Type: {self.process_type}, État: {self.state.value}"
