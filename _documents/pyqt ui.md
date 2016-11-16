1. use Qt Designer to create basic UI

2. make sure `pyui4.bat` is in the System PATH

3. change ui to py file
   ```
   pyuic4.bat demo.ui > demo.py
   ```
   OR generate file included excutable code
   ```
   pyuic4.bat -x -o demo.py demo.ui
   ```

4. create a new py file. input something like:
```
import sys
from PyQt4 import QtGui
from first import Ui_MainWindow # from xxx.py


class MyForm(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()  # from xxx.py
        self.ui.setupUi(self) 

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
```

5. generate `.exe` file in windows
- install pyinstaller. 
  `pip install pyinstaller`
- generate excutable file. 
  `pyinstaller.exe --windowed gui_action.py`

