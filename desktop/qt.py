import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QGridLayout, QLabel, QFormLayout, \
    QVBoxLayout
from PyQt5.QtWidgets import QTextEdit, QFileDialog
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
import os
from synchronize import syncronize
import xml.etree.ElementTree
from geojson import FeatureCollection
import json


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.first_widget = QWidget()
        self.first_widget.setGeometry(500, 1000, 400, 100)
        self.first_widget.setWindowTitle('Synchronization')

        # first_widget
        first_layout = QFormLayout()
        self.first_widget.setLayout(first_layout)
        btn = QPushButton('File', self)
        btn.clicked.connect(self.file_open)
        btn.resize(btn.sizeHint())
        conf_btn = QPushButton('Conf file', self)
        conf_btn.clicked.connect(self.conf_file_open)
        conf_btn.resize(conf_btn.sizeHint())
        self.apply_btn = QPushButton('Apply changes', self)
        self.apply_btn.clicked.connect(self.change_widget)
        self.apply_btn.resize(self.apply_btn.sizeHint())
        self.apply_btn.setEnabled(False)

        self.text = QLabel(self)
        self.text.setVisible(False)
        self.s_text = QLabel(self)
        self.s_text.setVisible(False)
        first_layout.addRow(btn)
        first_layout.addRow(self.text)
        first_layout.addRow(conf_btn)
        first_layout.addRow(self.s_text)
        first_layout.addRow(self.apply_btn)

        self.first_widget.show()

        # second_widget
        self.widget = QWidget()
        self.widget.setGeometry(500, 1000, 200, 400)
        self.widget.setWindowTitle('Synchronization')
        grid = QGridLayout()
        grid.setSpacing(10)
        self.view = QtWebEngineWidgets.QWebEngineView()
        self.view.setMaximumHeight(300)
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "html/map.html"))
        self.view.load(QtCore.QUrl().fromLocalFile(file_path))
        self.first = QLabel('Deleted features: {:d} buildings, {:d} roads, {:d} rivers', self)
        self.second = QLabel('Added features: {:d} buildings, {:d} roads, {:d} rivers', self)
        self.third = QLabel('Modified features: {:d} buildings, {:d} roads, {:d} rivers', self)
        grid.addWidget(self.view, 1, 0)
        grid.addWidget(self.first, 2, 0)
        grid.addWidget(self.second, 3, 0)
        grid.addWidget(self.third, 4, 0)
        self.view.loadFinished.connect(self.fillForm)
        self.widget.setLayout(grid)

    def file_open(self):
        self.name, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog)

        if self.name != '':
            self.text.setText(self.name)
            self.text.setVisible(True)
            self.enable_apply()

    def conf_file_open(self):
        self.conf_name, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog)

        if self.conf_name != '':
            self.s_text.setText(self.conf_name)
            self.s_text.setVisible(True)
            self.enable_apply()

    def enable_apply(self):
        if hasattr(self, 'name') and hasattr(self, 'conf_name'):
            if self.name != '' and self.conf_name != '':
                self.apply_btn.setEnabled(True)

    def change_widget(self):

        data = syncronize(self.name)

        '''e = xml.etree.ElementTree.parse(name).getroot()

        left = e.findall('Box')[0].find('left').text
        right = e.findall('Box')[0].find('right').text
        top = e.findall('Box')[0].find('top').text
        bottom = e.findall('Box')[0].find('bottom').text'''

        feature_collection = FeatureCollection(
            data['b_deleted'] + data['road_deleted'] + data['river_deleted'] + data['b_added'] + data['road_added'] +
            data['river_added']
            + data['b_edited'] + data['road_edited'] + data['river_edited'])

        j = json.dumps(feature_collection)

        self.view.page().runJavaScript(
            'var features = (new ol.format.GeoJSON()).readFeatures({:s});'.format(j) +
            'vectorFeaturesSource.clear();' +
            'vectorFeaturesSource.addFeatures(features);'
        )

        self.first.setText('Deleted features: {:d} buildings, {:d} roads, {:d} rivers'.format(len(data['b_deleted']),
                                                                                              len(data['road_deleted']),
                                                                                              len(data[
                                                                                                      'river_deleted'])))
        self.second.setText(
            'Added features: {:d} buildings, {:d} roads, {:d} rivers'.format(len(data['b_added']),
                                                                             len(data['road_added']),
                                                                             len(data['river_added'])))
        self.third.setText('Modified features: {:d} buildings, {:d} roads, {:d} rivers'.format(len(data['b_edited']),
                                                                                               len(data['road_edited']),
                                                                                               len(data[
                                                                                                       'river_edited'])))
        self.first_widget.hide()
        self.widget.show()


if __name__ == "__main__":
    def run():
        app = QApplication(sys.argv)
        Gui = Window()
        sys.exit(app.exec_())

run()
