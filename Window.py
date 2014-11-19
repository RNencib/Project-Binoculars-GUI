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
        #create the open file action
        openFile = QAction('Open', self)
        openFile.setShortcut('Ctrl+O') # Create shortcut
        openFile.setStatusTip('Open new File') # definition of the ation 
        openFile.triggered.connect(self.ShowFile)# use the ShowFile method
        # create the save file action
        saveFile = QAction('Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.Save)# use the Save method
        #Create new configuration
        Create = QAction('Create', self)
        Create.setStatusTip('Create new configuration')
        Create.triggered.connect(self.New_Config)
        # create menu
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')# add the file section on the menu
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        fileMenu = menubar.addMenu('&New Configuration')
        fileMenu.addAction(Create)
        # create window
        self.setGeometry(300, 300,500,500)# position and size of the window
        self.setWindowTitle('Binoculars')
        self.setWindowIcon(QIcon('binoculars.png'))# the icon of the app
        self.show() 
    # open file method  
    def ShowFile(self):
        #fname = QFileDialog.getOpenFileName(self, 'Open file','/home')
        #f = open(fname, 'r') # show the text file on the window
        # edit the text
        #with f:        
            #data = f.read()
            #self.textEdit.setText(data) 
        path = QFileDialog.getOpenFileName(
                self, 'Open File', '', 'CSV(*.csv)')
        if not path.isEmpty():
            with open(unicode(path), 'rb') as stream:
                self.table.setRowCount(0)
                self.table.setColumnCount(0)
                for rowdata in csv.reader(stream):
                    row = self.table.rowCount()
                    self.table.insertRow(row)
                    self.table.setColumnCount(len(rowdata))
                    for column, data in enumerate(rowdata):
                        item = QTableWidgetItem(data.decode('utf8'))
                        self.table.setItem(row, column, item)
    # save file method
    def Save(self):
        #fsave = QFileDialog.getSaveFileName(self,'Save file','/home')
        path = QFileDialog.getSaveFileName(
            self, 'Save File', '', 'CSV(*.csv)')
        if not path.isEmpty():
            with open(unicode(path), 'wb') as stream:
                writer = csv.writer(stream)
                for row in range(self.table.rowCount()):
                    rowdata = []
                    for column in range(self.table.columnCount()):
                        item = self.table.item(row, column)
                        if item is not None:
                            rowdata.append(
                                unicode(item.text()).encode('utf8'))
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)
    
    def New_Config(self):
        self.tab_widget.addTab(Conf_Tab(self),"Config")    
    

#----------------------------------------------------------------------------------------------------


        

#-----------------------------------------CREATE TABLE-----------------------------------------------       


class table(QWidget):

    
    def __init__(self, parent = None):
        super(table, self).__init__()
        
        
        # create a QTableWidget 
        
        self.table = QTableWidget(1, 2, self)
        self.table.setHorizontalHeaderLabels(['Parameter', 'Value'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        #create combobox
        combobox = QComboBox()
        list = []
        combobox.addItems(QStringList(self.list))
        #add items
        cell = QTableWidgetItem(QString("Types"))
        self.table.setItem(0, 0, cell)
        self.table.setCellWidget(0, 1, combobox)
        # create push button and add Types
        self.btn_add_types = QPushButton('Add Type', self)
        # create text edit
        self.TypeEdit = QLineEdit(self)
        #self.connect(self.btn_add_types, SIGNAL('clicked()'), self.add_types)
        # create push button and add it to a horizontal layout
        self.btn_add_row = QPushButton('+', self)
        # connect button clicked signal to our handler
        self.connect(self.btn_add_row, SIGNAL('clicked()'), self.add_row)
        # create push button and delete it to a horizontal layout
        self.btn_del_row = QPushButton('-', self)
        # connect button clicked signal to our handler
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

        
       

class Dispatcher(table):
    #label = QLabel('Dispatcher')#bug
    list = ['Local','OAR',]
    
class Input(table):
    #label = QLabel('Input')#bug
    list = []
    
class Projection(table):
    #label = QLabel('Projection')#bug
    list = []
    
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
