import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt5.QtWidgets import QTextEdit, QFileDialog


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 800, 500)
        self.setWindowTitle('Synchronization')
        self.win = QWidget()

        btn = QPushButton('File', self)
        btn.clicked.connect(self.file_open)

        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        self.text.setLineWrapMode(QTextEdit.NoWrap)
        self.text.setVisible(False)

        btn.resize(btn.sizeHint())
        btn.move(0, 100)

        self.show()

    def file_open(self):
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog)
        file = open(name, 'r')

        with file:
            data = file.read()
            self.text.setVisible(True)
            self.text.insertPlainText("Processed")
            print(data)


if __name__ == "__main__":  # had to add this otherwise app crashed

    def run():
        app = QApplication(sys.argv)
        Gui = Window()
        sys.exit(app.exec_())

run()
