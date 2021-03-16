from PyQt5 import QtCore, QtWidgets
from client import Ui_MainWindow
from datetime import datetime
import requests

#Наслідую для класа Messendger графічний інтерфейс
class Messenger(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, host='127.0.0.1:5000'):
        super().__init__()
        self.setupUi(self)

        self.host = host
        #Призначаю для pushButton метод send_message
        self.pushButton.pressed.connect(self.send_message)

        self.after = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(1000)

    def print_messages(self, message):
        #Метод для виведення повідомленнь
        dt = datetime.fromtimestamp(message['time'])
        dt_str = dt.strftime('%d %b %H:%M:%S')
        self.textBrowser.append(dt_str + ' ' + message['name'])
        self.textBrowser.append(message['text'])
        self.textBrowser.append("")

    def get_messages(self):
        #метод для запиту повідомлень з серверу
        try:
            response = requests.get('http://' + self.host + '/messages', params={'after': self.after})
        except:
            return

        messages = response.json()['messages']
        for message in messages:
            self.print_messages(message)
            self.after = message['time']

    def send_message(self):
        #метод для надсилання повідомлень на сервер
        name = self.lineEdit.text()
        text = self.textEdit.toPlainText()

        #обробка виключень і демонстрація помилок безпосередньо користувачу
        try:
            response = requests.post('http://' + self.host + '/send', json={'name': name, 'text': text})

        except:
            self.textBrowser.append("Сервер тимчасово недоступний")
            self.textBrowser.append("Надішліть повідомлення пізніше....")
            self.textBrowser.append('')
            return

        if response.status_code != 200:
            self.textBrowser.append("Обов'язково вкажіть ім'я")
            self.textBrowser.append("Текст не має перевищувати 1000 символів")
            self.textBrowser.append('')
            return

        self.textEdit.clear()


app = QtWidgets.QApplication([])
#тут вказано локальний сервер, для нормального функціонування месенджера треба вказати дійсний хост
window = Messenger('127.0.0.1:5000')
window.show()
app.exec()
