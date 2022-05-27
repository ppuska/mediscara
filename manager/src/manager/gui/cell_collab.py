"""Module for the GUI elements and code in Cell 1"""

from PyQt5.QtWidgets import QMainWindow

from .layout.collaborative import Ui_collaborativeWindow


class CollaborativeCell(QMainWindow, Ui_collaborativeWindow):
    """UI class for displaying the Cell1 editor window"""

    #
    #
    #
    #
    #

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)
