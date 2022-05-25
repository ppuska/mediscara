"""Module for the GUI elements and classes"""
import logging
import os.path

import yaml
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from .layout.gui import Ui_MainWindow
from .layout.preferences import Ui_preferencesWindow


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

        self.__grafana_address = "https://www.google.com"

        self._load_config()

        # display the webpage
        self.web_widget.setUrl(QUrl(self.__grafana_address))

        # connect the actions
        self.action_preferences.triggered.connect(self._open_preferences)

    def _open_preferences(self):
        """Callback method from the menubar to open the preferences menu"""
        preferences = Preferences(parent=self)
        preferences.show()

    def _load_config(self):
        """This method attemts to load the config file"""
        # open the config file

        config_file_path = os.path.abspath(ManagerGUI.CONFIG_FILE)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning")
        msg.setText("Conmfiguration error")
        msg.setStandardButtons(QMessageBox.Ok)

        try:
            with open(config_file_path, "r", encoding="utf-8") as config_file:
                config = yaml.safe_load(config_file)

        except FileNotFoundError:
            info = "Could not locate config file at %s, server connection is not be available"
            logging.warning(info, config_file_path)

            msg.setInformativeText(info % config_file_path)
            msg.exec()

        if config is None:
            info = "Config file is empty, server connection is not available"
            logging.warning(info)

            msg.setInformativeText(info)
            msg.exec()

        else:

            grafana_address = config.get(ManagerGUI.CONFIG_GRAFANA_ADDRESS)

            if grafana_address is None:
                info = "The configuration file should contain a 'grafana_address' value"
                logging.warning(info)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Warning")
                msg.setText("Configuration file error")
                msg.setInformativeText(info)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()

            else:
                self.__grafana_address = grafana_address


class Preferences(QMainWindow, Ui_preferencesWindow):
    """Class for displaying a preferences window"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)
