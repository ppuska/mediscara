import logging
import os.path

import yaml
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from .layout.gui import Ui_MainWindow


class ManagerGUI(QMainWindow, Ui_MainWindow):

    CONFIG_FILE = "config.yaml"
    CONFIG_GRAFANA_ADDRESS = "grafana_address"

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setupUi(self)  # initialize the UI

        url = QUrl("https://www.google.com")

        config = self._load_config()

        if config is not None:

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
                url = QUrl(grafana_address)

        # display the webpage
        self.web_widget.setUrl(url)

    @staticmethod
    def _load_config() -> dict:
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
            return None

        if config is None:
            info = "Config file is empty, server connection is not available"
            logging.warning(info)

            msg.setInformativeText(info)
            msg.exec()

            return None

        return config
