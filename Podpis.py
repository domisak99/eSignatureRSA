import sys
import os, time
import hashlib
import rsa
import re
from zipfile import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import QtGui, uic
 
qtCreatorFile = "Podpis.ui" 
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

 
class Podpis(QMainWindow, Ui_MainWindow):

    def GenerateKey(self):
        n, pub, priv = rsa.generate_keys()
        options = QFileDialog.Options()
        privName, _ = QFileDialog.getSaveFileName(self,"Ulož privátní klíč", "","Privatni klic (*.priv)", options=options)
        if privName:    
            file_open=open(privName, "w+")
            ftext= "RSA " + str(priv) + " " + str(n)
            file_open.write(ftext)
            file_open.close()

            pubName, _ = QFileDialog.getSaveFileName(self,"Ulož veřejný klíč", "","Verejny klic (*.pub)", options=options)
            if pubName:     
                file_open=open(pubName, "w+")
                ftext= "RSA " + str(pub) + " " + str(n)
                file_open.write(ftext)
                file_open.close()
        
    def Create_Signature(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Vyber dokument", "","Textový soubor (*.txt);;Všechny soubory (*)", options=options)
        if fileName:
            self.Cesta.setText(fileName)
            file_size=os.path.getsize(fileName)
            file_name = os.path.basename(fileName)
            file_info=os.path.splitext(file_name)
            file_CreationTime=time.ctime(os.path.getctime(fileName))
            file_ChangeTime=time.ctime(os.path.getmtime(fileName))
            self.Datum.setText(str(file_CreationTime))
            self.Zmena.setText(str(file_ChangeTime))
            self.Velikost.setText(str(file_size))
            self.Nazev.setText(str(file_info[0]))
            self.Typ.setText(str(file_info[1]))
            hash2 = hashlib.sha3_512()

            with open(fileName, 'rb') as file2:
                q2 = file2.read()
                hash2.update(q2)
            hashdata = hash2.hexdigest()
            privFile , _ = QFileDialog.getOpenFileName(self,"Vyber privatni klic", "","Privatni klic (*.priv)", options=options)
            if privFile:
                f = open(privFile, "r+")
                privData=str(f.read())
                privData_arr=privData.split(" ")
                f.close()
                rsaData=rsa.encrypt(privData_arr[1], privData_arr[2], hashdata)

                fileD, _ = QFileDialog.getSaveFileName(self,"Ulož elektronický podpis", "","Elektronický podpis (*.sign)", options=options)
                if fileD:
                    f = open(fileD, "w+")
                    ftext= "SHA3-512 " + str(rsaData)
                    f.write(ftext)
                    f.close()
                    fileName2 = os.path.basename(fileName)
                    fileD2 = os.path.basename(fileD)
                    fileZip, _ = QFileDialog.getSaveFileName(self,"Ulož komprimovany soubor", "","Komprimovaný soubor (*.zip)", options=options)
                    if fileZip:
                        fileZip2= os.path.basename(fileZip)
                        with ZipFile(fileZip2, 'w') as zipObj2:
                           zipObj2.write(fileName2)
                           zipObj2.write(fileD2)
        
    def Check_Signature(self):
        options = QFileDialog.Options()
        fileZip, _ = QFileDialog.getOpenFileName(self,"Vyber komprimovaný soubor", "","Komprimovaný soubor (*.zip)", options=options)
        if fileZip:
            fileZip2= os.path.basename(fileZip)
            self.Cesta.setText(fileZip)
            file_size=os.path.getsize(fileZip)
            file_info=os.path.splitext(fileZip2)
            file_CreationTime=time.ctime(os.path.getctime(fileZip))
            file_ChangeTime=time.ctime(os.path.getmtime(fileZip))
            self.Datum.setText(str(file_CreationTime))
            self.Zmena.setText(str(file_ChangeTime))
            self.Velikost.setText(str(file_size))
            self.Nazev.setText(str(file_info[0]))
            self.Typ.setText(str(file_info[1]))
            archive = ZipFile(fileZip2, 'r')
            listZIP=archive.namelist()
            if(len(listZIP)>2):
                error5="Chybny pocet souboru v archivu " + str(len(listZIP)) + "/2"
                self.Stav.setText(error5)
                return 0
            
            for fileSign in listZIP:
                    if re.search('.+sign', fileSign): 
                           listZIP.remove(fileSign)

            fileDoc=listZIP[0]
            Doc = archive.read(fileDoc)
            DocHash=hashlib.sha3_512(Doc).hexdigest()
            Sign=archive.read(fileSign)
            Sign=Sign.decode("utf-8")
            Sign_arr=Sign.split()
            cipher=""
            for i in range(1, len(Sign_arr)):
                cipher=cipher+Sign_arr[i]+" "

            pubFile , _ = QFileDialog.getOpenFileName(self,"Vyber veřejný klíč", "","Verejny klic (*.pub)", options=options)
            if pubFile:
                f = open(pubFile, "r+")
                pubData=str(f.read())
                pubData_arr=pubData.split(" ")
                f.close()
                rsaData=rsa.decrypt(pubData_arr[1], pubData_arr[2], cipher)
                if(rsaData==DocHash):
                    self.Stav.setText("Hashe se rovnaji! Vše by mělo být v pořádku.")
                else:
                    self.Stav.setText("Hashe se nerovnaji! Pravděpodobně bylo se souborem manipulováno.")
                
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.otevriButton.clicked.connect(self.Create_Signature)
        self.ulozButton.clicked.connect(self.Check_Signature)
        self.generovat.clicked.connect(self.GenerateKey)
        self.Konec.clicked.connect(self.close)
     
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Podpis()
    window.show()
    sys.exit(app.exec_())
