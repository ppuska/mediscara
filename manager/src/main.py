"""Main module"""
import sys

from PyQt5.QtWidgets import QApplication

from manager.gui.gui import ManagerGUI


def main():
    """Main entry point for the GUI application"""
    app = QApplication(sys.argv)
    window = ManagerGUI(parent=None)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
