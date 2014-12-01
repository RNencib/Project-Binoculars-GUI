import sys, csv
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

        self.setGeometry(300, 300,500,500)
        self.setWindowTitle('Binoculars')
        self.setWindowIcon(QIcon('binoculars.png'))
        self.show() 

    def ShowFile(self):
        path = QFileDialog.getOpenFileName(self, 'Open File', '', '*.txt')
       #if not path.isEmpty():
                #self.table.setRowCount(1)
                #self.table.setColumnCount(3)
                #for rowdata in data.readlines():
                 #   row = self.table.rowCount()
                  #  self.table.insertRow(row)
                   # self.table.setColumnCount(len(rowdata))
                    #for column, data in enumerate(rowdata):
                     #   item = QTableWidgetItem(data.decode('utf8'))
                      #  self.table.setItem(row, column, item)

    def Save(self):
        fsave = QFileDialog.getSaveFileName(self, 'Save File', '', '*.txt')
        widget = current.widget #Conf_Tab
        widget.Save()

        Conf_Tab.Save(fsave)
        file = open(fsave)
        file.write()

        Conf_tab.getParams()

    def New_Config(self):
        self.tab_widget.addTab(Conf_Tab(self),"Config")    
    

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
        combobox = QComboBox()
        self.choise = []
        combobox.addItems(QStringList(self.choise))

        
        #add items
        cell = QTableWidgetItem(QString("Types"))
        self.table.setItem(0, 0, cell)
        self.table.setCellWidget(0, 1, combobox)

        self.btn_add_types = QPushButton('Add Type', self)
        self.TypeEdit = QLineEdit(self)
        #self.connect(self.btn_add_types, SIGNAL('clicked()'), self.add_types)

        self.btn_add_row = QPushButton('+', self)
        self.connect(self.btn_add_row, SIGNAL('clicked()'), self.add_row)

        self.btn_del_row = QPushButton('-', self)
        self.connect(self.btn_del_row, SIGNAL('clicked()'), self.del_row)
          

        layout =QGridLayout()
        #layout.addWidget(self.label,0,0)#bug
        layout.addWidget(self.table,1,0,2,2)
        layout.addWidget(self.btn_add_types,3,0)
        layout.addWidget(self.btn_add_row,1,2)
        layout.addWidget(self.btn_del_row,2,2)
        layout.addWidget(self.TypeEdit,3,1)
        self.setLayout(layout)


 


    #def add_types(self):
        #self.list1 = [self.TypeEdit]
        #self.list.append(self.list1)
    def add_row(self):
        self.table.setRowCount(self.table.rowCount() + 1)

    def del_row(self):
        if self.table.rowCount() > 1 :
            self.table.setRowCount(self.table.rowCount() - 1) 

    def getParams(self):
        for index in range (self.table.rowCount):
            yield self.table.item(index,0),self.table.item(index,1)
        

        
       

class Dispatcher(Table):
    #label = QLabel('Dispatcher')#bug
    choise = ['Local','OAR',]
    
class Input(Table):
    #label = QLabel('Input')#bug
    choise = []
    
class Projection(Table):
    #label = QLabel('Projection')#bug
    choise = []
    
#----------------------------------------------------------------------------------------------------
        
#-----------------------------------------CREATE CONFIG----------------------------------------------
class Conf_Tab(QWidget):

    
    def __init__(self, parent = None):
        super(Conf_Tab,self).__init__()

        Dis = Dispatcher()
        Inp = Input()
        Pro = Projection()

        Layout = QVBoxLayout()
        Layout.addWidget(Dis)
        Layout.addWidget(Inp)
        Layout.addWidget(Pro)
        self.setLayout(Layout)

    def getParams(self):
        for param in itertools.chain(Dispatcher.getParams(),Input.getParams(),Projection.getParams):
            yield param
        
        
