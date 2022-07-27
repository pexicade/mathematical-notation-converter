from PyQt6.QtWidgets import QDialog, QMainWindow, QStackedLayout,QWidget,QApplication
from PyQt6.QtGui import QBrush, QIcon,QFont, QPixmap, QFontDatabase
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QPushButton, QLineEdit, QMessageBox, QVBoxLayout

import sys
import converters

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setFixedSize(655,550)
        self.setWindowTitle('Converter')
        self.setStyleSheet("background-color:white")
        self.add_widgets()
        self.create_meun()

    def add_widgets(self):
        font = QFont('Bebas Neue',27)
        #the title at the top
        title = QLabel('Notation Converter',self)
        title.setFont(font)
        title.setStyleSheet("background-color:transparent;color:black;QLabel{font-size:28px;font-weight:bold}")
        title.setFixedSize(325,40)
        title.move(320,15)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #the info icon at the bttom right corner
        self.info = QLabel(self)
        info_icon = QPixmap('src\\outline_info_black_24dp.png')
        info_icon.scaled(24,24)
        self.info.setPixmap(info_icon)
        self.info.setScaledContents(True)
        self.info.setFixedSize(24,24)
        self.info.move(655-24-15,550-24-15)
        self.info.mousePressEvent = self.info_clicked
        # the picture on the left
        pic = QPixmap('src\\mountain.jpg')
        pic.scaledToHeight(550)
        pic.scaledToWidth(320)
        self.picture = QLabel(self)
        self.picture.setPixmap(pic)
        self.picture.setScaledContents(True)
        self.picture.setFixedSize(320,550)
        self.picture.move(0,0)

    def create_meun(self):
        self.menu = QWidget(self)
        self.menu.setFixedSize(325,450)
        self.menu.move(320,60)
        self.menu.setStyleSheet("background-color:transparent")
        vbox = QVBoxLayout()
        self.menu.setLayout(vbox)
        self.menu_options = ['Infix to Postfix','Postfix to Infix','Infix to Prefix','Prefix to Infix','Prefix to Postfix','Postfix to Prefix','History']
        # ('#E79915','#E9451F')
        colors = [("#37CCE3","#236BE2"),('#13DB8C','#0772D5'),('#4ABEFC','#C32DBF'),('#E96567','#B011CA')]#,('#702CEA','#DF3872')]
        for i in range(len(self.menu_options)):
            button = QPushButton(self.menu_options[i],self.menu)
            button.setFixedSize(260,50)
            button.move(100,70+i*50)
            button.setStyleSheet(f"color:white;font-size:22px;font-weight:400;text-align:center;border:2px solid white;border-radius:10px;\
                                    background: QLinearGradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 {colors[i%4][0]}, stop: 1 {colors[i%4][1]});")
            button.clicked.connect(self.menu_clicked)
            vbox.setAlignment(Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignTop)
            vbox.addWidget(button)
        vbox.setSpacing(18)
    
    def menu_clicked(self):
        sender = self.sender()
        if sender.text() == 'History':
            self.show_history()
        else:
            convertionWidget.setWindowTitle(self.sender().text())
            function_name = sender.text().lower().replace(' ','_')
            convertionWidget.function_name = function_name
            convertionWidget.convertion_from , convertionWidget.convertion_to = function_name.split('_to_')
            convertionWidget.set_things_up()
            widgets.setCurrentIndex(1)

    def show_history(self):
        self.dialog = QDialog(self)
        self.dialog.setFixedSize(350,110)
        self.dialog.setWindowTitle('History')
        self.dialog.setStyleSheet("background-color:white")
        self.vbox = QVBoxLayout()
        self.history_order = 0 # descending
        self.dialog.setLayout(self.vbox)
        if len(history) == 0:
            self.vbox.addWidget(self.make_label('No history yet',300,30))
        else:
            history_label = self.make_label('History:',300,30)
            history_label.mousePressEvent = self.history_clicked
            self.vbox.addWidget(history_label)
            for i in range(len(history)):
                self.vbox.addWidget(self.make_label(f'\t{history[i][0]} : {history[i][1]}',300,30))
        self.dialog.show()

    def info_clicked(self,mouse_event):
        dialog = QDialog(self)
        dialog.setFixedSize(250,150)
        dialog.setWindowTitle('About')
        dialog.setStyleSheet("background-color:white")
        vbox = QVBoxLayout()
        dialog.setLayout(vbox)
        labels=[QLabel('Programmer: Mhmd Sadeghi')]
        labels.append(QLabel('Date: 2021/01/02'))
        labels.append(QLabel('Version: 1.0'))
        for label in labels:
            label.setStyleSheet("background-color:white;color:black;font-size:18px;font-weight:400")
            label.setFixedSize(250,40)
            label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            vbox.addWidget(label)
        dialog.show()

    def history_clicked(self,mouse_event):
        #change the order (ascending to descending and vice versa)
        print(f'{self.history_order=}')
        print(f'{self.dialog.layout().count()=}')
        for i in range(1,self.dialog.layout().count()):
            self.dialog.layout().itemAt(i).widget().setParent(None)
        if self.history_order == 0:
            start = 0
            end = len(history)
            step = 1
            self.history_order = 1
        else:
            start = len(history)-1
            end = -1
            step = -1
            self.history_order = 0
        for i in range(start,end,step):
            self.dialog.layout().addWidget(self.make_label(f'\t{history[i][0]} : {history[i][1]}',300,30))

    def make_label(self,text,weight,height):
        label = QLabel(text)
        label.setStyleSheet("background-color:white;color:black;font-size:17px;font-weight:400")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setFixedSize(weight,height)
        return label

class ConvertionWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.font = QFont('Overpass')
        self.font1 = QFont('Allerta')
        self.setFixedSize(465,285)
        self.setStyleSheet("background-color:white")
        layout = QVBoxLayout()
        self.setLayout(layout)
        back_icon = QPixmap('src\\outline_arrow_back_ios_black_24dp.png')
        back_icon.scaled(24,24)
        self.back = QLabel(self)
        self.back.setPixmap(back_icon)
        self.back.setFixedSize(24,24)
        self.back.setScaledContents(True)
        self.back.move(15,15)
        self.back_label = QLabel('Back',self)
        self.back_label.setFont(self.font)
        self.back_label.setStyleSheet("background-color:transparent;color:black;font-size:16px;text-align:left")
        self.back_label.setFixedSize(50,24)
        self.back_label.move(15+24+2,15)
        self.back.mousePressEvent = self.back_clicked
        self.label = QLabel(self)
        self.label.move(25,50)
        self.label.setFixedSize(350,40)
        self.label.setFont(self.font1)
        self.label.setStyleSheet("background-color:white;color:black;font-size:22px;text-align:left")
        self.text_box = QLineEdit(self)
        self.text_box.move(25,105)
        self.text_box.setFixedSize(290,50)
        self.text_box.setStyleSheet("background-color:white;color:black;font-size:17px;text-align:left")
        self.font1.setWeight(QFont.Weight.Light)
        self.text_box.setFont(self.font1)
        self.convert = QPushButton("Convert",self)
        self.convert.setFixedSize(130,45)
        self.convert.move(212-65,175)
        self.convert.setStyleSheet("color:white;font-size:19px;text-align:center;border:1px solid white;border-radius:10px;\
                                    background: QLinearGradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #E96567, stop: 1 #B011CA);")
        self.convert.setFont(self.font)
        self.convert.clicked.connect(self.convert_clicked)
        self.result = QLabel(self)
        self.result.setFixedSize(400,40)
        self.result.move(25,230)
        self.result.setFont(self.font)
        self.result.setStyleSheet("background-color:white;color:black;font-size:22px;text-align:left")
        self.function_name = self.convertion_from = self.convertion_to = ''

    def set_things_up(self):
        a = self.convertion_from
        self.label.setText(f'Enter {"an" if a=="infix" else "a"} {a} expression')
        hints = {'prefix':'/ + A B - C D','infix':'( A + B ) / ( C - D )','postfix':'A B + C D - /'}
        self.text_box.setPlaceholderText('Example: '+hints[self.convertion_from])
        self.result.setText(f'{self.convertion_to}:')

    def convert_clicked(self):
        res = ''
        try:
            res = converters.converters[self.function_name](converters.extract_tokens(self.text_box.text(),self.convertion_from))
            self.result.setText(f'{self.convertion_to}: {res}')
            print('res:',res)
            self.add_to_history(self.function_name.replace('_to_',' to ').title())
        except Exception as e:
            self.result.setText(f'{self.convertion_to}:')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            if type(e)==IndexError:#stack is empty
                msg.setText("the order of the operators and operands is wrong")
                msg.setInformativeText(f'Error: {e}')
            else:
                msg.setText(str(e))
            msg.exec()

    def back_clicked(self,mouse_event):
        self.text_box.clear()
        widgets.setCurrentIndex(0)

    def add_to_history(self,convertion):
        # example: [('Prefix to Postfix',5),('Prefix to Infix',3),('Infix to Postifx',2),('Infix to Prefix',2)]
        # if the user uses the same conversion more than once, the number of uses gets increased
        # if not, we need to insert the new element in the right place and not sort the whole list
        for i in range(len(history)):
            if history[i][0]==convertion:
                count = history[i][1]+1
                history[i] = (convertion,count)
                while i>=1 and history[i-1][1] < count: #swap until the right place is found
                    history[i], history[i-1] = history[i-1], history[i]
                    i-=1
                break
        else: # if the convertion wasn't already in history we just append it
            history.append((convertion,1))
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont('fonts/BebasNeue-Regular.ttf')
    QFontDatabase.addApplicationFont('fonts/SIMPLIFICA.ttf')
    QFontDatabase.addApplicationFont('fonts/overpass-regular.otf')
    QFontDatabase.addApplicationFont('fonts/allerta_medium.ttf')
    widgets = QStackedLayout()
    mainWindow = MainWindow()
    convertionWidget = ConvertionWidget()
    widgets.addWidget(mainWindow)
    widgets.addWidget(convertionWidget)
    history = []
    app.exec()