import json
import os
import sys
from subprocess import CalledProcessError

from PyQt5 import QtCore, QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QGridLayout, QLabel, QFormLayout, \
    QProgressBar
from PyQt5.QtWidgets import QFileDialog
from geojson import FeatureCollection

sys.path.append('/home/azamat/projects/labaratory/osm_synchronization_tool/')
from synchronize import initial_data
from synchronize import syncronize


class Window(QMainWindow):
    def exit(self):
        sys.exit()

    def __init__(self):
        super(Window, self).__init__()

        self.first_widget = QWidget()
        self.first_widget.setGeometry(500, 1000, 400, 120)
        self.first_widget.setWindowTitle('Synchronization')

        # first_widget
        first_layout = QFormLayout()
        self.first_widget.setLayout(first_layout)
        btn = QPushButton('Diff file', self)
        btn.clicked.connect(self.file_open)
        btn.resize(btn.sizeHint())
        conf_btn = QPushButton('Conf file', self)
        conf_btn.clicked.connect(self.conf_file_open)
        conf_btn.resize(conf_btn.sizeHint())
        self.apply_btn = QPushButton('Apply changes', self)
        self.apply_btn.clicked.connect(self.change_widget)
        self.apply_btn.resize(self.apply_btn.sizeHint())
        self.apply_btn.setEnabled(False)
        self.progress = QProgressBar(self)
        self.progress.setVisible(False)

        self.text = QLabel(self)
        self.text.setVisible(False)
        self.s_text = QLabel(self)
        self.s_text.setVisible(False)
        first_layout.addRow(btn)
        first_layout.addRow(self.text)
        first_layout.addRow(conf_btn)
        first_layout.addRow(self.s_text)
        first_layout.addRow(self.progress)
        first_layout.addRow(self.apply_btn)

        self.first_widget.show()

        # second_widget
        self.widget = QWidget()
        self.widget.setGeometry(500, 1000, 1000, 400)
        self.widget.setWindowTitle('Synchronization')
        grid = QGridLayout()
        self.view = QtWebEngineWidgets.QWebEngineView()
        self.view.setMinimumHeight(600)
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "html/map.html"))
        self.view.load(QtCore.QUrl().fromLocalFile(file_path))
        self.first = QLabel(self)
        self.second = QLabel(self)
        self.third = QLabel(self)
        self.exit_btn = QPushButton('Quit', self)
        self.exit_btn.setMaximumWidth(50)
        self.exit_btn.clicked.connect(self.exit)
        grid.addWidget(self.view, 1, 0, 8, 2)
        grid.addWidget(self.first, 9, 0, QtCore.Qt.AlignCenter)
        grid.addWidget(self.second, 10, 0, QtCore.Qt.AlignCenter)
        grid.addWidget(self.third, 11, 0, QtCore.Qt.AlignCenter)
        grid.addWidget(self.exit_btn, 12, 1)
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

        self.progress.setVisible(True)
        self.progress.setValue(30)

        initial = initial_data(self.name)

        initial_feature_collection = FeatureCollection(
            initial['b_deleted'] + initial['road_deleted'] + initial['river_deleted']
            + initial['b_edited'] + initial['road_edited'] + initial['river_edited'])

        initial_json = json.dumps(initial_feature_collection)

        self.view.page().runJavaScript(
            'var features = (new ol.format.GeoJSON()).readFeatures({:s});'.format(initial_json) +
            'initialVectorFeaturesSource.clear();' +
            'initialVectorFeaturesSource.addFeatures(features);'
        )

        self.progress.setValue(70)

        try:

            data = syncronize(self.name)

            '''e = xml.etree.ElementTree.parse(name).getroot()

            left = e.findall('Box')[0].find('left').text
            right = e.findall('Box')[0].find('right').text
            top = e.findall('Box')[0].find('top').text
            bottom = e.findall('Box')[0].find('bottom').text'''

            feature_collection = FeatureCollection(
                data['b_added'] + data[
                    'road_added'] +
                data['river_added']
                + data['b_edited'] + data['road_edited'] + data['river_edited'])

            j = json.dumps(feature_collection)

            self.view.page().runJavaScript(
                'var features = (new ol.format.GeoJSON()).readFeatures({:s});'.format(j) +
                'vectorFeaturesSource.clear();' +
                'vectorFeaturesSource.addFeatures(features);'
            )

            self.first.setText(
                'Deleted features: {:d} buildings, {:d} roads, {:d} rivers'.format(
                    len(initial['b_deleted']),
                    len(initial['road_deleted']),
                    len(initial[
                            'river_deleted'])))
            self.second.setText(
                'Added features: {:d} buildings, {:d} roads, {:d} rivers'.format(
                    len(data['b_added']),
                    len(data['road_added']),
                    len(data['river_added'])))
            self.third.setText(
                'Modified features: {:d} buildings, {:d} roads, {:d} rivers'.format(
                    len(data['b_edited']),
                    len(data['road_edited']),
                    len(data[
                            'river_edited'])))

        except CalledProcessError:
            print("Error during update")

        self.progress.setValue(100)

        self.first_widget.hide()
        self.widget.show()


if __name__ == "__main__":
    def run():
        app = QApplication(sys.argv)
        Gui = Window()
        sys.exit(app.exec_())

run()
