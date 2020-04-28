import sgtk
import os, sys, threading

from sgtk.platform.qt import QtCore, QtGui
logger = sgtk.platform.get_logger(__name__)

def show_dialog(app_instance):
    app_instance.engine.show_dialog("Asset Rename Filter...", app_instance, AppDialog)

class AppDialog(QtGui.QWidget):
    aim_project_base_path = u'B:/project/s4_chinatravelogues/assets'
    def __init__(self):
        super(AppDialog, self).__init__()
        self.resize(800,800)
        logger.info('Launching Asset Rename Filter...')
        self.worker = Worker()
        self.worker.trigger.connect(self.queryAssets)
        self.setWindowFlags(QtCore.Qt.Window)
        self.mainLayout = QtGui.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(20,5,20,20)
        self.mainLayout.setSpacing(0)
        self.listwidget = QtGui.QListWidget()
        self.listwidget.setObjectName(u'listWidget')
        self.listwidget.setSpacing(4)
        self.queryButton = QtGui.QPushButton('Query')
        self.queryButton.clicked.connect(self.startWorker)
        self.mainLayout.addWidget(self.queryButton)
        self.mainLayout.addWidget(self.listwidget)

    def startWorker(self):
        self.worker.start()

    @QtCore.Slot() 
    def queryAssets(self):
        logger.info('aaaaaaaaaaaaaaaaaaaaa')
        self.runCreate()
    
    def createItem(self, asset_name, path, current_name):
        listWidgetItem = QtGui.QListWidgetItem()
        listWidgetItem.setSizeHint(QtCore.QSize(200,80))
        itemWidget = QtGui.QWidget()
        vLayout = QtGui.QVBoxLayout(itemWidget)
        vLayout.setSpacing(3)
        hLayout = QtGui.QHBoxLayout()
        hLayout.setSpacing(25)
        asset_name_label = QtGui.QLabel()
        asset_name_label.setText(asset_name)
        asset_name_label.setObjectName('asset_name')
        asset_name_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        asset_name_label.setMinimumWidth(260)
        current_name_le = QtGui.QLineEdit()
        current_name_le.setFixedHeight(23)
        current_name_le.setText(current_name)
        path_label = QtGui.QLabel()
        path_label.setText(path)
        path_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        hLayout.addWidget(asset_name_label)
        hLayout.addWidget(current_name_le)
        vLayout.addLayout(hLayout)
        vLayout.addWidget(path_label)
        self.listwidget.addItem(listWidgetItem)
        self.listwidget.setItemWidget(listWidgetItem, itemWidget)
        widgets = {'asset_name': asset_name_label, 'current_name':current_name_le, 'path':path_label}
        listWidgetItem.setData(QtCore.Qt.UserRole, widgets)
        current_name_le.textChanged.connect(lambda * args:self._update_path(listWidgetItem))
    
    def runCreate(self):
        for x in self.get_assets():
            asset_name, current_name, path = x
            self.createItem(asset_name, path, current_name)
            
    def get_assets(self):
        assets = []
        for root, dirs, files in os.walk(self.aim_project_base_path):
            for i in files:
                if '.mb' in i:
                    ttmp = root.replace('\\', '/').split('/')
                    if 'Mod' in root:
                        asset_name = ttmp[ttmp.index('Mod') - 2]
                        base_path = os.path.join(root, i).replace('\\', '/')
                        assets.append([asset_name, i, base_path])
                    if 'Rig' in root:
                        asset_name = ttmp[ttmp.index('Rig') - 2]
                        base_path = os.path.join(root, i).replace('\\', '/')
                        assets.append([asset_name, i, base_path])
        return assets

    def _update_path(self, item):
        data = item.data(QtCore.Qt.UserRole)
        path = data['path'].text()
        new_name = data['current_name'].text()
        new_path = os.path.dirname(path) + '/' + new_name
        data['path'].setText(new_path)
        data['path'].setStyleSheet('color:#00FF7F;')

        os.rename(path, new_path)


class Worker(QtCore.QThread):
    trigger = QtCore.Signal()
    def __init__(self):
        super(Worker, self).__init__()

    def run(self):
        self.trigger.emit()
        logger.info('Emit done!!!')
        