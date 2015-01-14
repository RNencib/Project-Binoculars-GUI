import sys, csv
import itertools
from PyQt4.QtGui import *
from PyQt4.QtCore import *
#--------------------------------------------CREATE MAIN WINDOW----------------------------------------
class SimpleGUI(QMainWindow):

    def __init__(self):
        super(SimpleGUI, self).__init__()
        self.initUI()
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

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

        palette = QPalette()
        palette.setColor(QPalette.Background,Qt.gray)
        self.setPalette(palette)
        self.setGeometry(300, 300,500,500)
        self.setWindowTitle('Binoculars')
        self.setWindowIcon(QIcon('binoculars.png'))
        self.show()

    def ShowFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '', '*.txt')
        self.tab_widget.addTab(Conf_Tab(self),filename)
        widget = self.tab_widget.currentWidget()
        widget.read_data(filename)
                
        
        d = widget.read_data(filename)
        for k in d.keys():
            print "%s:" % k 
            for i in d[k]:
                print "    %s" % str(i)    
                    
 


    def Save(self):
        filename = QFileDialog().getSaveFileName(self, 'Enregistrer', '', '*.txt')
        widget = self.tab_widget.currentWidget() 
        widget.save(filename) 

    def New_Config(self):
        self.tab_widget.addTab(Conf_Tab(self),'New configuration')
#----------------------------------------------------------------------------------------------------
#-----------------------------------------CREATE TABLE-----------------------------------------------
class Table(QWidget):
    def __init__(self, choice = [], parent = None):
        super(Table, self).__init__()
       
        # create a QTableWidget
        self.table = QTableWidget(1, 3, self)
        self.table.setHorizontalHeaderLabels(['Parameter', 'Value','Comment'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        
        #create combobox
        combobox = QComboBox()
        combobox.addItems(QStringList(choice))
        
        #add items
        cell = QTableWidgetItem(QString("Types"))
        cell2 = QTableWidgetItem(QString(""))
        self.table.setItem(0, 0, cell)
        self.table.setCellWidget(0, 1, combobox)
        self.table.setItem(0, 2,cell2)
        self.btn_add_types = QPushButton('Add Type', self)
        self.TypeEdit = QLineEdit(self)
        
        #self.connect(self.btn_add_types, SIGNAL('clicked()'), self.add_types)
        self.btn_add_row = QPushButton('+', self)
        self.connect(self.btn_add_row, SIGNAL('clicked()'), self.add_row)
        self.btn_del_row = QPushButton('-', self)
        self.connect(self.btn_del_row, SIGNAL('clicked()'), self.del_row)
        
        layout =QGridLayout()
        #layout.addWidget(self.label,0,0)
        layout.addWidget(self.table,1,0,2,2)
        layout.addWidget(self.btn_add_types,3,0)
        layout.addWidget(self.btn_add_row,1,2)
        layout.addWidget(self.btn_del_row,2,2)
        layout.addWidget(self.TypeEdit,3,1)
        self.setLayout(layout)

    def add_row(self):
        self.table.insertRow(self.table.rowCount())

    def del_row(self):
        if self.table.rowCount() > 1 :
            self.table.removeRow(self.table.rowCount())

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
        
            



class Dispatcher(Table):
    def __init__(self, parent = None):
        choice = ['Local','OAR',]
        super(Dispatcher, self).__init__(choice)
        label = QLabel('Dispatcher')

class Input(Table):
    def __init__(self, parent = None):
        choice = ['test', 'test1']
        super(Input, self).__init__(choice)
        label = QLabel('Input')

class Projection(Table):
    def __init__(self, parent = None):
        choice = ['test', 'test1']
        super(Projection, self).__init__(choice)
        label = QLabel('Projection')

#----------------------------------------------------------------------------------------------------
#-----------------------------------------CREATE CONFIG----------------------------------------------
class Conf_Tab(QWidget):
    def __init__(self, parent = None):

        super(Conf_Tab,self).__init__()
        self.Dis = Dispatcher()
        self.Inp = Input()
        self.Pro = Projection()

        Layout = QVBoxLayout()
        Layout.addWidget(self.Dis)
        Layout.addWidget(self.Inp)
        Layout.addWidget(self.Pro)
        self.setLayout(Layout)

    def save(self, filename):
        with open(filename, 'w') as fp:
            fp.write('[dispatcher]\n')
            for key, value, comment in self.Dis.getParam():# cycles over the iterator object
                fp.write('{0} = {1} #{2}\n'.format(key, value, comment))
            fp.write('[input]\n')
            for key, value, comment in self.Inp.getParam():
                fp.write('{0} = {1} #{2}\n'.format(key, value, comment))
            fp.write('[projection]\n')
            for key, value, comment in self.Pro.getParam():
                fp.write('{0} = {1} #{2}\n'.format(key, value, comment))
           







    def read_data(self,filename):
        with open(filename, 'r') as inf:
            lines = inf.readlines()
 
        data = {'dispatcher': [], 'input': [], 'projection': []}
        for line in lines:
            if 'dispatcher' in line:
                key = 'dispatcher'
            elif 'input' in line:
                key = 'input'
            elif 'projection' in line: 
                key = 'projection'
            else:
                try:
                    caput, cauda = line.split('#')
                except ValueError:
                # no # in line
                    continue
                try:
                    name, value = caput.split('=')
                except ValueError:
                # ligne mal formee
                    continue
                data[key].append([name, value, cauda])
                 
        for n, key in enumerate(data):
            for m, item in enumerate(data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
    








