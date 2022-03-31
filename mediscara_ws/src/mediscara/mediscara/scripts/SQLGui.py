import dataclasses
import sys
import threading
from typing import Tuple

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHeaderView, QTableWidgetItem, QMessageBox

from widgets.sql_gui_ui import Ui_MainWindow
from widgets.statusbar_widget_ui import Ui_StatusBarWidget

from mediscara.scripts.logger import Logger
from mediscara.scripts.sql import SQLManager, Bell, SQLDataClass, Cell2Data
from mediscara.scripts.thread_manager import WorkerThread
from mediscara.config import SQLTableNames


class SQLGuiApp(QMainWindow, Ui_MainWindow):
    """Class for displaying a user interface for editing the contents of the MySQL database"""

    CELL1DM = Bell
    CELL2DM = Cell2Data

    SQL_UPDATE_INTERVAL = 1000  # ms

    class StatusBarWidget(QWidget, Ui_StatusBarWidget):

        DB_CONNECTED_STR = "Database connected"
        DB_DISCONNECTED_STR = "Database not connected"

        def __init__(self):
            super(SQLGuiApp.StatusBarWidget, self).__init__()
            self.setupUi(self)

        def set_connection_label(self, connected: bool):
            if connected:
                self.label_db_connected.setText(self.DB_CONNECTED_STR)
                self.label_db_connected.setStyleSheet('background-color: green')

            else:
                self.label_db_connected.setText(self.DB_DISCONNECTED_STR)
                self.label_db_connected.setStyleSheet("background-color: red")

    class TableWidgetSQLItem(QTableWidgetItem):
        """Class for storing additional information in the QTableWidgetItem"""

        def __init__(self, data: SQLDataClass, field_name: str):
            try:
                dict_ = dataclasses.asdict(data)
                self.__data_id = dict_[SQLDataClass.COL_ID]  # get id value

                super(SQLGuiApp.TableWidgetSQLItem, self).__init__(str(dict_[field_name]))

                if data.in_production:
                    self.setBackground(QtCore.Qt.green)

            except KeyError:
                raise ValueError(f"Field name '{field_name}' does not exist in {data.__class__.__name__}")

        def __str__(self):
            return f'ID: {self.data_id} text: {self.text()}'

        @classmethod
        def generate_row(cls, data: SQLDataClass):
            fields = dataclasses.fields(data)
            row = list()
            for field_ in fields:
                row.append(cls(data, field_name=field_.name))

            return row

        @property
        def data_id(self):
            return self.__data_id

    def __init__(self):
        super(SQLGuiApp, self).__init__()
        self.setupUi(self)

        self.logger = Logger(None)

        """Set up statusbar"""
        self.statusbar_widget = SQLGuiApp.StatusBarWidget()
        self.statusbar.addPermanentWidget(self.statusbar_widget, stretch=1)

        """Schedule manager"""
        self.sql_manager = SQLManager(
            table=[
                (SQLTableNames.CELL1.value, self.CELL1DM),
                (SQLTableNames.CELL2.value, self.CELL2DM)
            ])
        # connect to database
        self.logger.info("Connecting to database...")
        self.db_connect_thread = WorkerThread(worker_function=self.connect_to_database,
                                              result_callback=self.connect_to_db_callback,
                                              loop=True
                                              )

        self.db_connect_thread.start()

        """Buttons"""
        self.button_add_c1.clicked.connect(self.add_c1_callback)
        self.button_add_c2.clicked.connect(self.add_c2_callback)

        """Table views"""
        # cell 1
        for i, _ in enumerate(self.CELL1DM.field_names()):
            self.table_c1.insertColumn(i)
        self.table_c1.setHorizontalHeaderLabels(self.CELL1DM.field_names())
        self.table_c1.horizontalHeader().resizeSections(QHeaderView.Fixed)

        # cell 2
        for i, _ in enumerate(self.CELL2DM.field_names()):
            self.table_c2.insertColumn(i)
        self.table_c2.setHorizontalHeaderLabels(self.CELL2DM.field_names())
        self.table_c2.horizontalHeader().resizeSections(QHeaderView.Fixed)

        # tab changed callback
        self.tabWidget.currentChanged.connect(self.tab_changed_callback)

        """Timer"""
        self.sql_timer = QTimer()
        self.sql_timer.timeout.connect(self.sql_timer_callback)
        self.sql_timer.start(self.SQL_UPDATE_INTERVAL)

    """ OVERRIDES ************************************************************************************************** """

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.resize_table_columns()

        super().resizeEvent(a0)

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == QtCore.Qt.Key_Delete:
            """Display confirmation message box"""
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setWindowTitle("Are you sure?")
            msg_box.setText("Are you sure want to delete the selected items?")
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            ret = msg_box.exec()

            if ret == QMessageBox.Cancel:
                return

            if self.tabWidget.currentWidget() == self.tab:
                selected_items = self.table_c1.selectedItems()
                table_name = SQLTableNames.CELL1.value
            elif self.tabWidget.currentWidget() == self.tab_2:
                selected_items = self.table_c2.selectedItems()
                table_name = SQLTableNames.CELL2.value
            else:
                raise ValueError()

            selected_ids = list()
            for item in selected_items:
                assert isinstance(item, SQLGuiApp.TableWidgetSQLItem)
                if item.data_id not in selected_ids:
                    selected_ids.append(item.data_id)

            self.sql_manager.delete_elements(selected_ids, table_name)
            self.load_data()

        super().keyPressEvent(a0)

    """ METHODS **************************************************************************************************** """

    def resize_table_columns(self):
        column_count = len(self.CELL1DM.field_names())
        for i in range(column_count):
            self.table_c1.setColumnWidth(i, int(self.table_c1.width() / column_count))

        column_count = len(self.CELL2DM.field_names())
        for i in range(column_count):
            self.table_c2.setColumnWidth(i, int(self.table_c2.width() / column_count))

    def connect_to_database(self, _: threading.Lock) -> Tuple[bool, str]:
        return self.sql_manager.connect_to_database()

    def load_data(self):
        # clear the view
        selected_widget = self.tabWidget.currentWidget()

        if selected_widget == self.tab:  # cell 1
            table = self.table_c1
            table_name = SQLTableNames.CELL1.value
            dm = self.CELL1DM
        elif selected_widget == self.tab_2:  # cell 2
            table = self.table_c2
            table_name = SQLTableNames.CELL2.value
            dm = self.CELL2DM
        else:
            raise ValueError("Invalid tab selected")

        table.setRowCount(0)

        # fetch the data in the db
        datas = self.sql_manager.get_all_elements(table_name)

        if datas is None:  # error result
            self.statusbar_widget.set_connection_label(False)
            self.show_db_disconnected_msg()
            return

        for i, data in enumerate(datas):
            table.insertRow(i)
            row = SQLGuiApp.TableWidgetSQLItem.generate_row(data)
            for j, item in enumerate(row):
                table.setItem(i, j, item)

        table.setHorizontalHeaderLabels(dm.field_names())
        self.resize_table_columns()

    # noinspection PyMethodMayBeStatic
    def show_db_disconnected_msg(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning")
        msg.setText("Database disconnected")

        msg.exec()

    def clear_inputs(self):
        self.line_edit_part_type.setText("")
        self.line_edit_inc_type.setText("")
        self.line_edit_type.setText("")

        self.spinbox_marker_count.setValue(0)
        self.spinbox_count.setValue(0)

    """ CALLBACKS ***************************************************************************************************"""

    def tab_changed_callback(self):
        self.resize_table_columns()
        if self.sql_manager.connected:
            self.load_data()

    def connect_to_db_callback(self, success: bool, msg: str):
        if success:
            self.logger.info(msg)
            self.statusbar_widget.set_connection_label(True)
            self.db_connect_thread.stop()  # stop the thread from running again
            self.load_data()

        else:
            self.logger.warn(msg)

    def add_c1_callback(self):
        """Callback method for the Add button in cell 1 tab"""
        bell = Bell()
        bell.type = self.line_edit_type.text()
        bell.count = self.spinbox_count.value()
        bell.remaining = bell.count

        self.sql_manager.insert_element(data=bell, table_name=SQLTableNames.CELL1.value)  # insert the new element
        self.load_data()  # reload the new data list
        self.clear_inputs()  # clear the input fields

    def add_c2_callback(self):
        """Callback method for the Add button in cell 2 tab"""
        # create the new data entry
        data = self.CELL2DM()
        data.inc_type = self.line_edit_inc_type.text()
        data.part_type = self.line_edit_part_type.text()
        data.marker_count = self.spinbox_marker_count.value()
        data.remaining = data.marker_count

        self.sql_manager.insert_element(data=data, table_name=SQLTableNames.CELL2.value)  # insert the new element
        self.load_data()  # reload the new data list
        self.clear_inputs()  # clear the input fields

    def sql_timer_callback(self):
        if self.sql_manager.connected:
            self.logger.debug("Loading view")
            self.load_data()


def main():
    app = QApplication(sys.argv)
    ui_main_window = SQLGuiApp()
    ui_main_window.show()
    app.exec()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    main()
    sys.excepthook = except_hook
