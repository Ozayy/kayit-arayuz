from PyQt5.QtWidgets import QMainWindow,QMessageBox
from PyQt5 import QtWidgets
from untitled import  Ui_MainWindow
import sqlite3
from PyQt5.QtWidgets import QApplication




class kullanicilarr(QMainWindow):
    def __init__(self):
        super(kullanicilarr, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.connect = sqlite3.connect("C:/veri/veritabani.db")
        self.im = self.connect.cursor()

        kullanici = """CREATE TABLE IF NOT EXISTS Girisler(id INTEGER PRIMARY KEY AUTOINCREMENT,Kullanici TEXT,Sifre TEXT,EPosta TEXT)"""
        self.im.execute(kullanici)
        self.connect.commit()


        self.ekran_ilk= 0
        self.ekran_iki = 1


        self.ui.pushButton_2.clicked.connect(self.kayit_baglan)
        self.ui.pushButton_4.clicked.connect(self.geri_git)
        self.ui.pushButton_3.clicked.connect(self.kod_yaz)
        self.ui.pushButton.clicked.connect(self.giris_login)

    def giris_login(self):
        self.kullanici_giris = self.ui.lineEdit.text()
        self.sifre_giris = self.ui.lineEdit_2.text()


        if self.kullanici_giris == "" or self.sifre_giris == "":
            messagebox = QMessageBox()
            messagebox.setIcon(QMessageBox.Warning)
            messagebox.setWindowTitle("Boş alan")
            messagebox.setText("Boş alan bırakma lütfen")
            messagebox.setStandardButtons(QMessageBox.Ok)
            buton_ok = messagebox.button(QMessageBox.Ok)
            buton_ok.setText("Tamam")
            messagebox.exec_()

        else:
            self.im.execute("""SELECT * FROM Girisler WHERE Kullanici=? and Sifre=?""", (self.kullanici_giris,self.sifre_giris))

            test= self.im.fetchall()

            if len(test)<1:
                messagebox = QMessageBox()
                messagebox.setIcon(QMessageBox.Warning)
                messagebox.setWindowTitle("Hatalı Giriş")
                messagebox.setText("Böyle bir kayıt bulunamadı")
                messagebox.setStandardButtons(QMessageBox.Ok)
                buton_ok = messagebox.button(QMessageBox.Ok)
                buton_ok.setText("Tamam")
                messagebox.exec_()

            else:
                self.ui.statusbar.showMessage("Giriş Başarılı", 3000)
                self.ui.statusbar.setStyleSheet("background-color : white")




    def kullanici_kontrol(self,isim):
        for kontrol in isim:
            x = kontrol.isdigit()
            if x == True:
                return x

    def kod_yaz(self):
        self.kullanici_kayit = self.ui.lineEdit_3.text()
        self.sifre_kayit = self.ui.lineEdit_4.text()
        self.eposta_kayit = self.ui.lineEdit_5.text()

        karsilastir = self.im.execute("SELECT * FROM Girisler WHERE Kullanici='"+self.kullanici_kayit+"'")
        karsilastir_kullanici = karsilastir.fetchall()
        karsilastir_iki = self.im.execute("SELECT * FROM Girisler WHERE Eposta='"+self.eposta_kayit+"'")
        karsilastir_eposta = karsilastir_iki.fetchall()




        if self.kullanici_kayit == "" or self.sifre_kayit == "" or self.eposta_kayit == "":
            messagebox = QMessageBox()
            messagebox.setIcon(QMessageBox.Warning)
            messagebox.setWindowTitle("Boş olmamalı")
            messagebox.setText(
                "Kullanıcı adı,şifre veya eposta boş bırakılmamalı")
            messagebox.setStandardButtons(QMessageBox.Ok)
            buton_ok = messagebox.button(QMessageBox.Ok)
            buton_ok.setText("Tamam")
            messagebox.exec_()

        elif karsilastir_eposta:
            messagebox = QMessageBox()
            messagebox.setIcon(QMessageBox.Warning)
            messagebox.setWindowTitle("Kayıt zaten var")
            messagebox.setText(
                "Eposta sistemde zaten mevcut")
            messagebox.setStandardButtons(QMessageBox.Ok)
            buton_ok = messagebox.button(QMessageBox.Ok)
            buton_ok.setText("Tamam")
            messagebox.exec_()



        elif karsilastir_kullanici:
            messagebox = QMessageBox()
            messagebox.setIcon(QMessageBox.Warning)
            messagebox.setWindowTitle("Kayıt zaten var")
            messagebox.setText(
                "Bu kayıt sistemde mevcut")
            messagebox.setStandardButtons(QMessageBox.Ok)
            buton_ok = messagebox.button(QMessageBox.Ok)
            buton_ok.setText("Tamam")
            messagebox.exec_()


        elif self.kullanici_kontrol(self.kullanici_kayit):
            messagebox = QMessageBox()
            messagebox.setIcon(QMessageBox.Warning)
            messagebox.setWindowTitle("Rakam giremezsin")
            messagebox.setText(
                "Kullanıcı adını rakam giremezsin")
            messagebox.setStandardButtons(QMessageBox.Ok)
            buton_ok = messagebox.button(QMessageBox.Ok)
            buton_ok.setText("Tamam")
            messagebox.exec_()
        else:
            self.im.execute("""INSERT INTO Girisler(Kullanici,Sifre,Eposta) VALUES(?,?,?)""",[self.kullanici_kayit,self.sifre_kayit,self.eposta_kayit])
            self.connect.commit()
            self.ui.statusbar.showMessage("KAYIT BAŞARILI",2000)
            self.ui.statusbar.setStyleSheet("background-color : white")
            self.ui.lineEdit_3.clear()
            self.ui.lineEdit_4.clear()
            self.ui.lineEdit_5.clear()

















    def geri_git(self):
        self.ui.stackedWidget.setCurrentIndex(self.ekran_ilk)



    def kayit_baglan(self):
        self.ui.stackedWidget.setCurrentIndex(self.ekran_iki)




















app=QApplication([])

kullanicilar=kullanicilarr()
kullanicilar.show()

app.exec_()
