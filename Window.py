import sys, csv, os
import itertools
import inspect
import glob
import BINoculars.util, BINoculars.main
from PyQt4.QtGui import *
from PyQt4.QtCore import *

#--------------------------------------------CREATE MAIN WINDOW----------------------------------------
class SimpleGUI(QMainWindow):

    def __init__(self):
        super(SimpleGUI, self).__init__()
        self.initUI()
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        close = self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

    def close_tab(self, tab):
        self.tab_widget.removeTab(tab)

    def initUI(self):
        openFile = QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.ShowFile)

        saveFile = QAction('Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.Save)

        Create = QAction('Create', self)
        Create.setStatusTip('Create new configuration')
        Create.triggered.connect(self.New_Config)
         
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        fileMenu = menubar.addMenu('&New Configuration')
        fileMenu.addAction(Create)
        fileMenu = menubar.addMenu('&HELP')

        palette = QPalette()
        palette.setColor(QPalette.Background,Qt.gray)
        self.setPalette(palette)
        self.setGeometry(250, 200,500,500)
        self.setWindowTitle('Binoculars')
        self.setWindowIcon(QIcon('binoculars.png'))
        self.show()

    def ShowFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '')
        for F in filename.split('/') :
            NameFile = []
            NameFile.append(F)
        NameFile.reverse()
        self.tab_widget.addTab(Conf_Tab(self),NameFile[0])
        widget = self.tab_widget.currentWidget()
        widget.read_data(filename)


    def Save(self):
        filename = QFileDialog().getSaveFileName(self, 'Enregistrer', '', '*.txt')
        widget = self.tab_widget.currentWidget() 
        widget.save(filename) 
        
    def New_Config(self):
        self.tab_widget.addTab(Conf_Tab(self),'New configuration')

#----------------------------------------------------------------------------------------------------
#-----------------------------------------CREATE TABLE-----------------------------------------------
class Table(QWidget):
    def __init__(self, parent = None):
        super(Table, self).__init__()
        
        # create a QTableWidget
        self.table = QTableWidget(1, 3, self)
        self.table.setHorizontalHeaderLabels(['Parameter', 'Value','Comment'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        
        #create combobox
        self.combobox = QComboBox()
        #add items
        cell = QTableWidgetItem(QString("type"))
        cell2 = QTableWidgetItem(QString(""))
        self.table.setItem(0, 0, cell)
        self.table.setCellWidget(0, 1, self.combobox)
        self.table.setItem(0, 2,cell2)

        self.btn_add_row = QPushButton('+', self)
        self.connect(self.btn_add_row, SIGNAL('clicked()'), self.add_row)
        self.buttonRemove = QPushButton('-',self)
        self.connect(self.buttonRemove, SIGNAL("clicked()"), self.remove) 

        layout =QGridLayout()
        layout.addWidget(self.table,0,0,3,10)
        layout.addWidget(self.btn_add_row,0,11)
        layout.addWidget(self.buttonRemove,1,11)
        self.setLayout(layout)

    def add_row(self):
        self.table.insertRow(self.table.rowCount())
    
    def remove(self):
        self.table.removeRow(self.table.currentRow()) 

    def get_keys(self):
        return list(self.table.item(index,0).text() for index in range(self.table.rowCount())) 


    def getParam(self):
        for index in range(self.table.rowCount()):
            key = self.table.item(index,0).text() 
            comment = self.table.item(index, 2).text()
            if self.table.item(index,1):
                value = self.table.item(index, 1).text()
            else:
                value = self.table.cellWidget(index, 1).currentText()
            if self.table.item == None:
                value = self.table.item(index,1).text("")
            yield key, value, comment
        
    def addData(self, data):
        for item in data:
            if item[0] == 'type':
                box = self.table.cellWidget(0,1)
                box.setCurrentIndex(box.findText(item[1], Qt.MatchFixedString))
                newitem = QTableWidgetItem(item[2])
                self.table.setItem(0, 2, newitem)
            else: 
                self.add_row()
                row = self.table.rowCount()
                for col in range(self.table.columnCount()):
                    newitem = QTableWidgetItem(item[col])
                    self.table.setItem(row -1, col, newitem)

    def addDataConf(self, items):
        keys = self.get_keys()
        newconfigs = list([item[0], '', item[1]] for item in items if item[0] not in keys)
        self.addData(newconfigs)
                
    def add_to_combo(self, items):
        self.combobox.clear()
        self.combobox.addItems(items)
    

#----------------------------------------------------------------------------------------------------
#-----------------------------------------CREATE CONFIG----------------------------------------------
class Conf_Tab(QWidget):
    def __init__(self, parent = None):

        super(Conf_Tab,self).__init__()
        self.Dis = Table()
        self.Inp = Table()
        self.Pro = Table()

        label1 = QLabel('<strong>Dispatcher</strong>')
        label2 = QLabel('<strong>Input</strong>')
        label3 = QLabel('<strong>Projection<strong>')

        self.select = QComboBox()
        backends = list(backend.lower() for backend in BINoculars.util.get_backends())
        self.select.addItems(QStringList(backends))
        self.start = QPushButton('run')
        self.connect(self.start, SIGNAL("clicked()"), self.run)
        self.scan = QLineEdit()
        self.start.setStyleSheet("background-color: darkred")

        Layout = QGridLayout()
        Layout.addWidget(self.select,0,1)
        Layout.addWidget(label1,1,1)
        Layout.addWidget(self.Dis,2,1)
        Layout.addWidget(label2,3,1)
        Layout.addWidget(self.Inp,4,1)
        Layout.addWidget(label3,5,1)
        Layout.addWidget(self.Pro,6,1)
        Layout.addWidget(self.start,7,0)
        Layout.addWidget(self.scan,7,1)
        self.setLayout(Layout)
 
        self.Dis.add_to_combo(QStringList(BINoculars.util.get_dispatchers()))
        self.select.activated['QString'].connect(self.DataCombo)
        self.Inp.combobox.activated['QString'].connect(self.DataTableInp)
        self.Pro.combobox.activated['QString'].connect(self.DataTableInpPro)
        self.Dis.combobox.activated['QString'].connect(self.DataTableInpDis)
        

    def DataCombo(self,text):
        self.Inp.add_to_combo(QStringList(BINoculars.util.get_inputs(str(text))))
        self.Pro.add_to_combo(QStringList(BINoculars.util.get_projections(str(text))))

    def DataTableInp (self,text):
        backend = str(self.select.currentText())
        inp = BINoculars.util.get_input_configkeys(backend, str(self.Inp.combobox.currentText()))
        self.Inp.addDataConf(inp)

    def DataTableInpPro (self,text):
        backend = str(self.select.currentText())
        proj = BINoculars.util.get_projection_configkeys(backend, str(self.Pro.combobox.currentText()))
        self.Pro.addDataConf(proj)

    def DataTableInpDis (self,text):
        backend = str(self.select.currentText())
        disp = BINoculars.util.get_dispatcher_configkeys(str(self.Dis.combobox.currentText()))
        self.Dis.addDataConf(disp)

 
    def save(self, filename): 
        with open(filename, 'w') as fp:
            fp.write('[dispatcher]\n')
            for key, value, comment in self.Dis.getParam():# cycles over the iterator object
                fp.write('{0} = {1} #{2}\n'.format(key, value, comment))
            fp.write('[input]\n')
            for key, value, comment in self.Inp.getParam():
                if key == 'type':
                    value = '{0}:{1}'.format(self.select.currentText(),value)
                fp.write('{0} = {1} #{2}\n'.format(key, value, comment))
            fp.write('[projection]\n')
            for key, value, comment in self.Pro.getParam():
                if key == 'type':
                    value = '{0}:{1}'.format(self.select.currentText(),value)
                fp.write('{0} = {1} #{2}\n'.format(key, value, comment))

    def get_configobj(self, filename):
        indict = {}
        for key, value, comment in self.Inp.getParam():
            if key == 'type':
                value = '{0}:{1}'.format(self.select.currentText(),value)
                indict[key] = value
            

        for key, value, comment in self.Dis.getParam():
            if key == 'type':
                value = '{0}:{1}'.format(self.select.currentText(),value)
                indict[key] = value
            

        for key, value, comment in self.Pro.getParam():
            if key == 'type':
                value = '{0}:{1}'.format(self.select.currentText(),value)
                indict[key] = value
            

        cfg = BINoculars.util.Configfile()
        setattr(cfg, 'input', indict)
        setattr(cfg, 'dispatcher', indict)
        setattr(cfg, 'projection', indict)
        return cfg

    def read_data(self,filename):
        with open(filename, 'r') as inf:
            lines = inf.readlines()
 
        data = {'dispatcher': [], 'input': [], 'projection': []}
        for line in lines:
            line = line.strip('\n')
            if '[dispatcher]' in line:
                key = 'dispatcher'
            elif '[input]' in line:
                key = 'input'
            elif '[projection]' in line: 
                key = 'projection'
            else:
                if '#' in line:
                    index = line.index('#')
                    caput = line[:index]
                    cauda = line[index:]
                else:
                    caput = line
                    cauda = ''
                if '=' in caput:
                    name, value = caput.split('=')
                    if name.strip(' ') == 'type' and ':' in value:
                        backend, value = value.strip(' ').split(':')
                    data[key].append([name.strip(' '), value.strip(' '), cauda.strip(' ')])

        self.select.setCurrentIndex(self.select.findText(backend, Qt.MatchFixedString))
        self.DataCombo(backend)

        for key in data:
            if key == 'dispatcher':
                self.Dis.addData(data[key])
            elif key == 'input':
                self.Inp.addData(data[key])
            elif key == 'projection':
                self.Pro.addData(data[key])

                
    def run(self,cfg):
        command = self.scan.text()
        BINoculars.main.Main.from_object(cfg, command)
        
    



