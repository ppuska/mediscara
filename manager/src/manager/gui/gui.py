"""Module for the GUI elements and classes"""

import logging
import re

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QLineEdit


from .layout.gui import Ui_MainWindow
from .layout.preferences import Ui_preferencesWindow
from .cell_industrial import IndustrialCell

from .settings import AppSettings


class ManagerGUI(QMainWindow, Ui_MainWindow):
    """
    PyQt application for the GUI app

    This application can use the FIWARE connector and publish messages to the OCB
    """

    CONFIG_FILE = "config.yaml"
    CONFIG_GRAFANA_ADDRESS = "grafana_address"

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setupUi(self)  # initialize the UI

        self.__settings = AppSettings()

        # connect the actions
        self.action_preferences.triggered.connect(self._open_preferences)
        self.action_collaborative.triggered.connect(self._open_collab_window)
        self.action_industrial.triggered.connect(self._open_industrial_window)

        self.load_page()

    def load_page(self):
        """Loads the contents of the main page"""

        self.__grafana_address = f"http://{self.__settings.server_address}:3003"

        # display the webpage
        self.web_widget.setUrl(QUrl(self.__grafana_address))

    def _open_preferences(self):
        """Callback method from the menubar to open the preferences menu"""
        preferences = Preferences(settings=self.__settings, parent=self)
        preferences.show()

        if preferences.settings_changed:
            self.load_page()  # reload the page after changing settings

    def _open_collab_window(self):
        """Callback function from the menubar to open the collab cell editor"""

    def _open_industrial_window(self):
        """Callback function from the menubar to open the industrial cell editor"""
        window = IndustrialCell(server_address=self.__settings.server_address, parent=self)
        window.show()


class Preferences(QMainWindow, Ui_preferencesWindow):
    """Class for displaying a preferences window"""

    def __init__(self, settings: AppSettings, parent=None):
        super().__init__(parent=parent)

        self.__settings = settings
        self.__settings_changed = False

        self.setupUi(self)

        # connecting signals
        self.line_edit_server_address.textChanged.connect(self._evaluate_inputs)

        self.button_save.clicked.connect(self._save_settings)
        self.button_cancel.clicked.connect(self.close)

        self._load_settings()

    def _evaluate_inputs(self):
        """Evaluates the inputs given to the line edits"""

        line_edit = self.sender()

        assert isinstance(line_edit, QLineEdit)

        if line_edit == self.line_edit_server_address:
            text = line_edit.text()

            if re.search(r"^(\d{1,3}\.){3}(\d{1,3})$", text) is not None:
                line_edit.setStyleSheet("color: green")
                self.button_save.setEnabled(True)

            else:
                line_edit.setStyleSheet("color: red")
                self.button_save.setEnabled(False)

    def _save_settings(self):
        """Saves the current values to the settings"""
        self.__settings.server_address = self.line_edit_server_address.text()

        self.__settings_changed = True

        logging.info("Settings stored")
        self.close()

    def _load_settings(self):
        """Loads and displays the settings from the stored values"""

        self.line_edit_server_address.setText(self.__settings.server_address)

    # region properties

    @property
    def settings_changed(self) -> bool:
        """Returns whether or not the settings have been changed"""
        return self.__settings_changed

    # endregion
