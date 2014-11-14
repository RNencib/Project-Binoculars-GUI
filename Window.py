import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

#--------------------------------------------CREATE MAIN WINDOW----------------------------------------
class SimpleGUI(QMainWindow):
    
    def __init__(self):
        super(SimpleGUI, self).__init__()
        self.initUI()

    def initUI(self):      
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.tab_widget.addTab(Dispatcher(self),"Dispatcher")
        self.tab_widget.addTab(Input(self),"Input")
        self.tab_widget.addTab(Projection(self),"Projection")
        # create the open file action
        openFile = QAction('Open', self)
        openFile.setShortcut('Ctrl+O') # Create shortcut
        openFile.setStatusTip('Open new File') # definition of the ation 
        openFile.triggered.connect(self.ShowFile)# use the ShowFile method
        # create the save file action
        saveFile = QAction('Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.Save)# use the Save method
        # create menu
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')# add the file section on the menu
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        # create window
        self.setGeometry(300, 300, 600, 450)# position and size of the window
        self.setWindowTitle('Binoculars')
        self.setWindowIcon(QIcon('binoculars.png'))# the icon of the app
        self.show() 
    # open file method  
    def ShowFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file','/home')
        f = open(fname, 'r') # show the text file on the window
        # edit the text
        with f:        
            data = f.read()
            self.textEdit.setText(data) 
    # save file method
    def Save(self):
        fsave = QFileDialog.getSaveFileName(self,'Save file','/home')
    

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
        combobox.addItems(QStringList(self.list))
        #add items
        cell = QTableWidgetItem(QString("Types"))
        self.table.setItem(0, 0, cell)
        self.table.setCellWidget(0, 1, combobox)
        # create push button and add Types
        self.btn_add_types = QPushButton('Add Type', self)
        self.btn_add_types.resize(100,20)
        self.btn_add_types.move(0,192)
        # create text edit
        self.TypeEdit = QLineEdit(self)
        self.TypeEdit.move(101,192)
        # create push button and add it to a horizontal layout
        self.btn_add_row = QPushButton('+', self)
        self.btn_add_row.resize(20,20)
        self.btn_add_row.move(255,0)
        # connect button clicked signal to our handler
        self.connect(self.btn_add_row, SIGNAL('clicked()'), self.add_row)
        # create push button and delete it to a horizontal layout
        self.btn_del_row = QPushButton('-', self)
        self.btn_del_row.resize(20,20)
        self.btn_del_row.move(255,20)
        # connect button clicked signal to our handler
        self.connect(self.btn_del_row, SIGNAL('clicked()'), self.del_row)

    def add_row(self):
        self.table.setRowCount(self.table.rowCount() + 1)
    def del_row(self):
        if self.table.rowCount() > 1 :
            self.table.setRowCount(self.table.rowCount() - 1)    

class Dispatcher(table):
    list = ['Local','OAR',]
    
class Input(table):
    list = ['','',]
  
class Projection(table):
    list = ['','',]

#----------------------------------------------------------------------------------------------------
        
        
