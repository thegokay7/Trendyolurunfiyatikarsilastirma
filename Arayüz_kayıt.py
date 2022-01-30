from PyQt5 import QtCore, QtWidgets
import sqlite3
import requests
from bs4 import BeautifulSoup 
from wsgiref import headers
conn = sqlite3.connect('liste.db')

c = conn.cursor()


c.execute("""CREATE TABLE if not exists todo_list(
    "list_item"	TEXT,
	"Fiyat"	INTEGER,
	"url"	TEXT)
    """)


conn.commit()


conn.close()



class Pncr1(object):
    def habura(self, kontrolsyf):
        kontrolsyf.setObjectName("Yapılacaklar_listesi")
        kontrolsyf.setFixedWidth(520)
        kontrolsyf.setFixedHeight(600)
        self.centralwidget = QtWidgets.QWidget(kontrolsyf)
        self.centralwidget.setObjectName("centralwidget")
        self.ekleme = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.ekle())
        self.ekleme.setGeometry(QtCore.QRect(10, 50, 120, 30))
        self.ekleme.setObjectName("ekleme")
        self.teksil = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.kaldır())
        self.teksil.setGeometry(QtCore.QRect(140, 50, 140, 30))
        self.teksil.setObjectName("teksil")
        self.toplusil = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.sil())
        self.toplusil.setGeometry(QtCore.QRect(290, 50, 100, 30))
        self.toplusil.setObjectName("toplusil")
        self.ekleme_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.ekleme_edit.setGeometry(QtCore.QRect(10, 10, 500, 30))
        self.ekleme_edit.setObjectName("ekleme_edit")
        self.liste = QtWidgets.QListWidget(self.centralwidget)
        self.liste.setGeometry(QtCore.QRect(10, 90, 500, 450))
        self.liste.setObjectName("liste")
        self.savedb = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.kayıt())
        self.savedb.setGeometry(QtCore.QRect(400, 50, 111, 31))
        self.savedb.setObjectName("savedb")
        self.kontrol = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.kayıt())
        self.kontrol.setGeometry(QtCore.QRect(10, 550, 500, 31))
        self.kontrol.setObjectName("kontrol")
        kontrolsyf.setCentralWidget(self.centralwidget)
        self.menu = QtWidgets.QMenuBar(kontrolsyf)
        self.menu.setGeometry(QtCore.QRect(0, 0, 405, 20))

        kontrolsyf.setMenuBar(self.menu)
        self.statusbar = QtWidgets.QStatusBar(kontrolsyf)
        self.statusbar.setObjectName("statusbar")
        kontrolsyf.setStatusBar(self.statusbar)

        self.retranslateUi(kontrolsyf)
        QtCore.QMetaObject.connectSlotsByName(kontrolsyf)
        self.k()
        
    def k(self):
        
        conn = sqlite3.connect('liste.db')
        
        c = conn.cursor()

        c.execute("SELECT * FROM todo_list")
        records = c.fetchall()


        
        conn.commit()

        
        conn.close()

        
        for record in records:
            self.liste.addItem(str(record[0]))
    
   
    def ekle(self):
        global convertedPrice
        global itemurl
        itemurl = self.ekleme_edit.text()
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        }
        page = requests.get(url= itemurl , headers=headers)

        sayfa = BeautifulSoup(page.content,'html.parser')
        productTitle = sayfa.find("h1", class_="pr-new-br").getText()

        price = sayfa.find("span", class_="prc-slg").getText()

        #image = item.sayfa.find("img",class_="js-image-zoom__zoomed-area")

        convertedPrice = float(price.replace(",",".").replace("TL",""))
        
        self.liste.addItem(productTitle)
        self.ekleme_edit.setText("")
        conn = sqlite3.connect('liste.db')
        c = conn.cursor()
        c.execute("INSERT INTO todo_list VALUES (:item,:price,:url)",
                {
                    "item": productTitle, 'price': convertedPrice, "url" : itemurl
                })
        conn.commit()
        conn.close()
        
    
    def kaldır(self):
        
        clicked = self.liste.currentRow()
        self.liste.takeItem(clicked)

    
    def sil(self):
        self.liste.clear()
    def kayıt(self):
        conn = sqlite3.connect('liste.db')
        c = conn.cursor()
        c.execute('DELETE FROM todo_list;',)
        items = []
        for index in range(self.liste.count()):
            items.append(self.liste.item(index))

        for item in items:
            c.execute("INSERT INTO todo_list VALUES (:item,:price,:url)",
                {
                    'item': item.text(),'price': convertedPrice, "url" : itemurl
                })
          
        conn.commit()
        conn.close()   
    def retranslateUi(self, kontrolsyf):
        ceviri = QtCore.QCoreApplication.translate
        kontrolsyf.setWindowTitle(ceviri("Ana Ekran", "Alınacaklar listesi"))
        self.ekleme.setText(ceviri("Ana Ekran", "Ekle"))
        self.teksil.setText(ceviri("Ana Ekran", "Çıkar"))
        self.toplusil.setText(ceviri("Ana Ekran", "Temizle"))
        self.savedb.setText(ceviri("Ama Ekram", "Kaydet"))
        self.kontrol.setText(ceviri("Ana Ekran","Fiyat Kontrol Et"))

        
       
      

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    kontrolsyf = QtWidgets.QMainWindow()
    ui = Pncr1()
    ui.habura(kontrolsyf)
    kontrolsyf.show()
    sys.exit(app.exec_())