import rsa
import hashlib, sys, os.path, time, pathlib
import assets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6 import uic


def podpis(soubor, klic):
    with open(soubor, "rb") as f:
        novyHash = hashlib.sha3_512(f.read()).hexdigest()

    with open(klic, "r") as f:
        klicek = f.read()

    n, d = rsa.decodeKeyBase64(klicek)

    signature = rsa.encode(novyHash, n, d)
    s = rsa.encodeBase64(signature)
    return s


def overeni(soubor, klic, sign):
    with open(soubor, "rb") as f:
        novyHash = hashlib.sha3_512(f.read()).hexdigest()

    with open(klic, "r") as f:
        klicek = f.read()

    n, e = rsa.decodeKeyBase64(klicek)

    with open(sign, "r") as f:
        signature = f.read()

    decSignature = rsa.decodeBase64(signature)
    druhy = rsa.decode(decSignature, n, e)

    print("hash1: ", novyHash)
    print("hash2: ", druhy)

    if druhy == novyHash:
        msg = "Jsou shodné"
    else:
        msg = "Nejsou shodné"
    return msg, soubor


def properties(fileName):
    fileInfo = {
        "Name: ": os.path.basename(fileName),
        "Type: ": pathlib.Path(fileName).suffix,
        "Created: ": time.ctime(os.path.getctime(fileName)),
        "Modified: ": time.ctime(os.path.getmtime(fileName)),
        "Path: ": os.path.dirname(fileName)
    }
    fileInfoP = ""
    fileInfoD = ""
    for item in fileInfo:
        fileInfoP += item
        fileInfoP +=  "\n"
        fileInfoD += fileInfo[item]
        fileInfoD += "\n"

    return fileInfoP, fileInfoD

 
Ui_MainWindow, QtBaseClass = uic.loadUiType("gui.ui")

class MyApp(QMainWindow, Ui_MainWindow):
    

    def otevriPrivateKey(self):
        global privateKey
        try:
            privateKey, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Private key (*.priv);;All Files (*)")
            msg = "" + os.path.basename(privateKey) + " byl nahrán"
            self.message.setText(msg)

        except:
            err = "Nepovedlo se načíst soubor"
            self.message.setText(err)


    def podpisOtevriSoubor(self):
        global podpisSoubor
        try:
            podpisSoubor, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)")
            msg = "" + os.path.basename(podpisSoubor) + " byl nahrán"
            self.message.setText(msg)
            if podpisSoubor:
                fileInfoP, fileInfoD = properties(podpisSoubor)                
                self.podpisFileInfoP.setText(fileInfoP)
                self.podpisFileInfoD.setText(fileInfoD)

        except:
            err = "Nepovedlo se načíst soubor"
            self.message.setText(err)


    def podpisSave(self):
        signature = podpis(podpisSoubor, privateKey)

        soubor, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getOpenFileName()", "RSA_SHA3-512 PODPIS_V_BASE64.sign","Signature (*.sign);;All Files (*)")
        if soubor:
            with open(soubor, "w") as f:
                f.write(signature)
            
    
    def otevriPublicKey(self):
        global publicKey
        try:
            publicKey, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","(*.pub);;All Files (*)")
            msg = "" + os.path.basename(publicKey) + " byl nahrán"
            self.message.setText(msg)

        except:
            err = "Nepovedlo se načíst soubor"
            self.message.setText(err)


    def overeniOtevriSoubor(self):
        global overeniSouboru
        try:
            overeniSouboru, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)")
            msg = "" + os.path.basename(overeniSouboru) + " byl nahrán"
            self.message.setText(msg)
            if overeniSouboru:
                fileInfoP, fileInfoD = properties(overeniSouboru)
                self.overeniFileInfoP.setText(fileInfoP)
                self.overeniFileInfoD.setText(fileInfoD)
        except:
            err = "Nepovedlo se načíst soubor"
            self.message.setText(err)


    def overeniOtevriPodpis(self):
        global overeniPodpis
        try:
            overeniPodpis, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","(*.sign);;All Files (*)")
            msg = "" + os.path.basename(overeniPodpis) + " byl nahrán"
            self.message.setText(msg)
        except:
            err = "Nepovedlo se načíst soubor"
            self.message.setText(err)
        msg, _ = overeni(overeniSouboru, publicKey, overeniPodpis)
        self.message.setText(msg)


    def keys(self):
        n, e, d = rsa.generateKeys()
        privateKey = rsa.encodeKeyBase64(n, d)
        publicKey = rsa.encodeKeyBase64(n, e)
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getOpenFileName()", "RSA SOUKROMÝ_KLÍČ_V_BASE64.priv","(*.priv);;All Files (*)")
        if fileName:
            with open(fileName, "w") as f:
                f.write(privateKey)
        fileName1, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getOpenFileName()", "RSA VEŘEJNÝ_KLÍČ_V_BASE64.pub","(*.pub);;All Files (*)")
        if fileName1:
            with open(fileName1, "w") as f:
                f.write(publicKey)
            

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.saveKeys.clicked.connect(self.keys)
        self.podpisOpenPrivateKey.clicked.connect(self.otevriPrivateKey)
        self.podpisOpenFile.clicked.connect(self.podpisOtevriSoubor)
        self.podpisSaveFile.clicked.connect(self.podpisSave)
        self.overeniOpenPublicKey.clicked.connect(self.otevriPublicKey)
        self.overeniOpenFile.clicked.connect(self.overeniOtevriSoubor)
        self.overeniOpenSignature.clicked.connect(self.overeniOtevriPodpis)
     
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
