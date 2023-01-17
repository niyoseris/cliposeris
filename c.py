import pyperclip
import time
from PyQt5 import QtWidgets, QtGui, QtCore

class ClipboardHistory(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the clipboard history list
        self.clipboard_history = []
        self.current_clipboard = ""
        self.current_selected = None

        # Create the UI elements
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setStyleSheet("padding: 5px;")
        self.set_clipboard_button = QtWidgets.QPushButton("Set clipboard")
        self.remove_button = QtWidgets.QPushButton("Remove")

        # Set up the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.list_widget)
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.set_clipboard_button)
        button_layout.addWidget(self.remove_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Connect the buttons to their respective functions
        self.set_clipboard_button.clicked.connect(self.set_clipboard_data)
        self.remove_button.clicked.connect(self.remove_item)

        # Main loop that checks the clipboard data every 500 milliseconds
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.save_to_clipboard_history)
        self.timer.start(500)

    # Function to save the current clipboard data to the history list
    def save_to_clipboard_history(self):
        new_clipboard = pyperclip.paste()
        if new_clipboard != self.current_clipboard:
            if new_clipboard not in self.clipboard_history:
                self.current_clipboard = new_clipboard
                self.clipboard_history.append(self.current_clipboard)
                item = QtWidgets.QListWidgetItem(new_clipboard)
                item.setToolTip(new_clipboard)
                if self.list_widget.count() > 0:
                    last_item = self.list_widget.item(self.list_widget.count()-1)
                    if last_item.background().color() == QtGui.QColor("yellow"):
                        item.setBackground(QtGui.QColor("white"))
                    else:
                        item.setBackground(QtGui.QColor("yellow"))
                else:
                    item.setBackground(QtGui.QColor("yellow"))
                self.list_widget.addItem(item)
            else:
                self.current_clipboard = new_clipboard
                items = self.list_widget.findItems(new_clipboard, QtCore.Qt.MatchExactly)
                for item in items:
                    item.setBackground(QtGui.QColor("white"))
                self.list_widget.scrollToItem(items[0])

    # Function to set the clipboard data to a specific item in the history list
    def set_clipboard_data(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            pyperclip.copy(selected_item.text())
            for i in range(self.list_widget.count()):
                item = self.list_widget.item(i)
                item.setBackground(QtGui.QColor("white"))
            selected_item.setBackground(QtGui.QColor("yellow"))

    # Function to remove the selected item from the history list
    def remove_item(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            row = self.list_widget.row(selected_item)
            self.list_widget.takeItem(row)
            self.clipboard_history.remove(selected_item.text())
            if self.current_selected == selected_item:
                self.current_selected = None
            if self.list_widget.count() > 0:
                for i in range(self.list_widget.count()):
                    item = self.list_widget.item(i)
                    if i % 2 == 0:
                        item.setBackground(QtGui.QColor("white"))
                    else:
                        item.setBackground(QtGui.QColor("yellow"))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = ClipboardHistory()
    window.setWindowTitle("Cliposeris")
    window.show()
    app.exec_()