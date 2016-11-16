# coding=utf-8

import sys
import logging
import cgi
import gui
import ble
import time
import datetime
import Queue
import serial.tools.list_ports
from PyQt4.QtGui import QApplication, QMainWindow, QTextCursor
from PyQt4.QtCore import QThread, SIGNAL


class GuiAction(QMainWindow, gui.Ui_MainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.mode = None
        self.rx = ""
        self.com = serial.Serial()
        self.queue_com = Queue.Queue()
        self.thread_com = ThreadComServer(self.queue_com, self.com)
        self.queue_ble = Queue.Queue()
        self.thread_ble = ThreadBleServer(self.queue_ble)
        # Tx Area
        self.comboBoxCom.currentIndexChanged.connect(self.com_changed)
        self.comboBoxCom.addItem("Choose COM Port")
        self.comboBoxCom.setCurrentIndex(0)
        self.pushButtonSend.clicked.connect(self.cmd_send)
        # Rx Area
        self.pushButtonClr.clicked.connect(self.data_clean)
        # COM list
        com_list = serial.tools.list_ports.comports()
        for clist in com_list:
            desc = clist.description.split('(')
            try:
                self.comboBoxCom.addItem(clist.device + " " + desc[0])
            except:
                self.comboBoxCom.addItem(clist.device + " Unknow")

    def closeEvent(self, event):
        self.com_stop()
        self.ble_stop()
        self.com.close()
        self.thread_com.wait()
        self.thread_ble.wait()

    def com_changed(self, com_port):
        try:
            self.com_stop()
            self.ble_stop()
            self.mode = None
            self.com.close()
            com_str = str(self.comboBoxCom.currentText()).split(' ')
            if "COM" in com_str[0].upper():
                self.com.port = com_str[0]
            else:
                self.com.port = None
            if "Bluegiga" in com_str[1]:
                self.comboBoxCom.setStyleSheet("color:blue;")
                self.ble_handle("ble_start")
                self.ble_start()
                '''set self.mode = "ble" at ble_handle'''
            else:
                self.com.baudrate = 9600
                self.com.timeout = 1
                self.com.writeTimeout = 1
                self.com.open()
                self.comboBoxCom.setStyleSheet("color:green;")
                self.txt_append("com connected!", type='progress')
                self.mode = "com"
                self.com_start()
        except Exception as e:
            logging.debug(e)
            self.com_stop()
            self.ble_stop()
            self.comboBoxCom.setStyleSheet("color:red;")

    def cmd_send(self):
        cmd = self.lineEdit.text()
        if "com" == self.mode:
            self.txt_append("\r\n%s\r\n" % cmd, type='tx_com')
            self.queue_com.put(cmd)
        elif "ble" == self.mode:
            self.txt_append("\r\n%s\r\n" % cmd, type='tx_ble')
            self.queue_ble.put(cmd)

    def data_clean(self):
        self.textBrowser.setText("")

    def txt_append(self, val, type='rx'):
        colors = {'progress': 'grey', 'error': 'red',
                  'rx': 'black', 'tx_com': 'green', 'tx_ble': 'blue'}
        val = "<font color=%s>%s</font>" % (colors[type], cgi.escape(val))
        self.textBrowser.moveCursor(QTextCursor.End)
        self.textBrowser.append(val)

    def com_start(self):
        self.queue_com.queue.clear()
        self.connect(self.thread_com, SIGNAL(
            "com_handle(PyQt_PyObject, PyQt_PyObject)"), self.com_handle)
        self.thread_com.start()

    def com_stop(self):
        self.thread_com.stop_com()
        self.disconnect(self.thread_com, SIGNAL(
            "com_handle(PyQt_PyObject, PyQt_PyObject)"), self.com_handle)

    def com_handle(self, step, val=""):
        if (step == "com_error"):
            self.comboBoxCom.setEnabled(True)
            self.comboBoxCom.setStyleSheet("color:red;")
            self.txt_append("com error: %s\r\n" % val, type='progress')
        elif (step == "com_data"):
            self.txt_append(val, type='rx')

    def ble_start(self):
        self.queue_ble.queue.clear()
        self.connect(self.thread_ble, SIGNAL(
            "ble_handle(PyQt_PyObject, PyQt_PyObject)"), self.ble_handle)
        self.thread_ble.start()

    def ble_stop(self):
        self.thread_ble.stop_ble()
        self.disconnect(self.thread_ble, SIGNAL(
            "ble_handle(PyQt_PyObject, PyQt_PyObject)"), self.ble_handle)

    def ble_handle(self, step, val=""):
        # print step + " " + val
        if (step == "ble_start"):
            self.comboBoxCom.setEnabled(False)
            self.txt_append("ble connecting ...\r\n", type='progress')
        elif (step == "ble_connect"):
            self.comboBoxCom.setEnabled(True)
            self.txt_append("ble connect to %s !\r\n" % val, type='progress')
            self.mode = "ble"
        elif (step == "ble_error"):
            self.comboBoxCom.setEnabled(True)
            self.comboBoxCom.setCurrentIndex(0)
            self.txt_append("ble error: %s\r\n" % val, type='progress')
        elif (step == "ble_data"):
            self.rx += val
            if "\r\n" in self.rx or len(self.rx) > 100:
                self.txt_append(self.rx, type='rx')
                self.rx = ""
        elif (step == "ble_rx_timeout"):
            if self.rx.strip() != "":
                self.txt_append(self.rx, type='rx')
            self.txt_append("receive finished!", type='progress')
            self.txt_append("", type='progress')
            self.rx = ""


class ThreadComServer(QThread):

    def __init__(self, queue, com):
        QThread.__init__(self)
        self.stop = False
        self.queue = queue
        self.com = com

    def __del__(self):
        self.wait()

    def stop_com(self):
        self.stop = True

    def run(self):
        self.stop = False
        self.queue.queue.clear()

        while not self.stop:
            time.sleep(0.1)
            try:
                value = self.com.readline(100)
                # print val,
                if len(value) > 0:
                    self.emit(
                        SIGNAL("com_handle(PyQt_PyObject, PyQt_PyObject)"), "com_data", value)
                command = str(self.queue.get(False))
                if '~' not in command:
                    command += "\r\n"
                self.com.write(command)
            except Exception as e:
                if str(e).strip() != "":
                    logging.error(e)
                    self.emit(
                        SIGNAL("com_handle(PyQt_PyObject, PyQt_PyObject)"), "com_error", str(e))


class ThreadBleServer(QThread):
    HANDLE_CRP = 8  # from cable_replacement example, xgatt_data 8
    SERVER_CRP = "0x0B:D5:16:66:E7:CB:46:9B:8E:4D:27:42:F1:BA:77:CC"

    def __init__(self, queue):
        QThread.__init__(self)
        self.stop = False
        self.rx_busy = False
        self.queue = queue
        self.timeout = 0

    def __del__(self):
        self.wait()

    def stop_ble(self):
        self.stop = True

    def indication_callback(self, handle, value):
        # print "indication, handle %d: %s " % (handle, value)
        if (handle == self.HANDLE_CRP):
            self.rx_busy = True
            self.timeout = datetime.datetime.now() + datetime.timedelta(0, 3, 0)
            self.emit(
                SIGNAL("ble_handle(PyQt_PyObject, PyQt_PyObject)"), "ble_data", value)

    def run(self):
        try:
            self.stop = False
            self.rx_busy = False
            self.queue.queue.clear()
            flag = False
            ble_device = ble.BleDevice()
            devices = ble_device.scan()
            for dev in devices:
                # print dev
                try:
                    '''can not promise every ble device have 'packet_data' message'''
                    service = dev['packet_data']['connectable_advertisement_packet'][
                        'complete_list_128-bit_service_class_uuids']
                except:
                    continue

                if self.SERVER_CRP in service:
                    ble_device.connect(dev['address'])
                    ble_device.set_indication(
                        "e7add780-b042-4876-aae1-112855353cc1", callback=self.indication_callback)
                    self.emit(SIGNAL("ble_handle(PyQt_PyObject, PyQt_PyObject)"),
                              "ble_connect", dev['name'])
                    flag = True
                    break
            if flag is False:
                raise Exception("not find usable device")
        except Exception as e:
            logging.error(e)
            ble_device.stop()
            self.emit(SIGNAL("ble_handle(PyQt_PyObject, PyQt_PyObject)"),
                      "ble_error", str(e))
            return

        while not self.stop:
            time.sleep(0.1)
            try:
                command = str(self.queue.get(False))
                if '~' not in command:
                    command += "\r\n"
                if not self.rx_busy:
                    ble_device.write_characteristics_handle(
                        str(command) + "\r\n", self.HANDLE_CRP)
                    self.timeout = datetime.datetime.now() + datetime.timedelta(0, 3, 0)
                    self.rx_busy = True
            except Exception as e:
                if str(e).strip() != "":
                    ble_device.stop()
                    logging.error(e)
                    self.emit(
                        SIGNAL("ble_handle(PyQt_PyObject, PyQt_PyObject)"), "ble_error", str(e))
            finally:
                if self.rx_busy:
                    cur_time = datetime.datetime.now()
                    if cur_time > self.timeout:
                        self.emit(
                            SIGNAL("ble_handle(PyQt_PyObject, PyQt_PyObject)"), "ble_rx_timeout", "")
                        self.rx_busy = False

        ble_device.stop()


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)

    app = QApplication(sys.argv)
    gui_action = GuiAction()
    gui_action.show()
    sys.exit(app.exec_())
