"""Module for the App settings"""
from enum import Enum

from PyQt5.QtCore import QSettings


class AppSettings:
    """This is a class for storing and generating QSettings for the Manager App"""

    ORG_NAME = "Medicor"
    ORG_DOMAIN = "medicor.hu"
    APP_NAME = "Mediscara Manager"

    class Fields(Enum):
        """Enum class to store the keys to the settings"""

        SERVER_ADDRESS = "grafana_address"

    def __init__(self) -> None:
        self.__settings = QSettings(AppSettings.ORG_NAME, AppSettings.APP_NAME)

    @property
    def server_address(self):
        """Gets the grafana address from the settings"""
        value = self.__settings.value(AppSettings.Fields.SERVER_ADDRESS.value)
        return str(value) if value is not None else " "

    @server_address.setter
    def server_address(self, value: str):
        """Stores the server address in the settings"""
        self.__settings.setValue(AppSettings.Fields.SERVER_ADDRESS.value, value)
