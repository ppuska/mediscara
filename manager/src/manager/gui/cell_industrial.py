"""Module for the industrial cell code"""

from PyQt5.QtWidgets import QMainWindow, QWidget, QListWidgetItem

from .layout.industrial import Ui_industrialWindow
from .layout.industrial_item import Ui_ListItem

from ..production.interface import Production
from ..production.model import Container, IndustialOrder


class IndustrialCell(QMainWindow, Ui_industrialWindow):
    class IndustrialListItem(QWidget, Ui_ListItem):
        def __init__(self, incubator_type: str, production_count: int, parent: None):

            super().__init__(parent)

            self.setupUi(self)

            self.label_inc_type.setText(f"Incubator type: {incubator_type}")
            self.label_count.setText(f"Production count: {production_count}")
            self.label_remaining.setText(f"Remaining: {production_count}")

    def __init__(self, server_address: str, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)

        self.__production_manager = Production(server_address=server_address)

        # connect signals and slots
        self.button_publish.clicked.connect(self._publish)

        self._load_page()

    def _load_page(self):
        container = self.__production_manager.load_production_orders(container_id=Container.get_industrial_id())
        print(container)

        for order in container.order_list:
            assert isinstance(order, IndustialOrder)
            widget = IndustrialCell.IndustrialListItem(
                incubator_type=order.incubator_type, production_count=order.count, parent=self
            )
            list_widget_item = QListWidgetItem(self.list_widget)
            list_widget_item.setSizeHint(widget.sizeHint())

            self.list_widget.addItem(list_widget_item)
            self.list_widget.setItemWidget(list_widget_item, widget)

    def _publish(self):
        order = IndustialOrder()
        order.count = self.spinbox_count.value()
        order.incubator_type = self.line_edit_inc_type.text()

        self.__production_manager.new_production_order(order)
