pd = QtGui.QProgressDialog('running', 'Cancel', 0, 0, self)
        pd.setWindowModality(QtCore.Qt.WindowModal)
        pd.show()
        def progress(cfg, command):
            pd.setValue(0)
            if pd.wasCanceled():
                raise KeyboardInterrupt
            QtGui.QApplication.processEvents()
            return BINoculars.main.Main.from_object(cfg, command)
        try:
            for index in range(self.ListCommand.rowCount()-1):
                cfg = self.ListCommand.item(index,1).cfg
                command = self.ListCommand.item(index,0).command
                progress(cfg, command)
                self.ListCommand.setRowCount(1)
        except BaseException, e:
            tb=traceback.format_exc()
            QtGui.QMessageBox.about(self,"Error Message",QtCore.QString(tb))
        finally:
                pd.close()
