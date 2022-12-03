import shutil
from rsa import generateKeys
import hashlib, sys, os.path, time, pathlib
import assets

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6 import uic

X = 12
z = 10
block = z * X

BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

def podpis(soubor, klic):

    sha3 = hashlib.sha3_512()
    with open(soubor, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha3.update(data)
    hash = sha3.hexdigest()

    with open(klic, "r") as f:
        klic = f.read()

    n = int(klic[0])
    d = int(klic[1])

    OTblocks = [ord(char) for char in hash]
    BINblocks = [bin(ch)[2:].zfill(X) for ch in OTblocks]
    BIN = "".join(BINblocks)
    BINs = [BIN[i:i + block] for i in range(0, len(BIN), block)]
    INTblocks = [int(ch, 2) for ch in BINs]
    c = [pow(ch, d, n) for ch in INTblocks]
    signature = "".join([str(ch) for ch in c])
    return signature


def overeni(soubor, klic, sign):
    sha3 = hashlib.sha3_512()
    with open(soubor, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha3.update(data)
    ohash = sha3.hexdigest()

    with open(klic, "r") as f:
        klic = f.read()

    n = int(klic[0])
    e = int(klic[1])

    with open(sign, "r") as f:
        signature = f.read()

    INTblocks = [int(ch) for ch in signature]
    m = [pow(c, e, n) for c in INTblocks]
    BINblocks = [bin(ch)[2:].zfill(block) for ch in m]
    BIN = "".join(BINblocks)
    BINs = [BIN[i:i + X] for i in range(0, len(BIN), X)]
    INTs = [int(ch, 2) for ch in BINs]
    output = [chr(ch) for ch in INTs]
    output = "".join(output)
    
    if ohash == output:
        msg = "Jsou shodné"
        return msg, soubor
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
        # archived = shutil.make_archive() zip file

        soubor, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getOpenFileName()", "","Privatni klic (*.sign);;All Files (*)")
        if soubor:
            with open(soubor, "w") as f:
                f.write(signature)
            
    
    def otevriPublicKey(self):
        global publicKey
        try:
            publicKey, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Public key (*.pub);;All Files (*)")
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
            overeniPodpis, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)")
            msg = "" + os.path.basename(overeniPodpis) + " byl nahrán"
            self.message.setText(msg)
        except:
            err = "Nepovedlo se načíst soubor"
            self.message.setText(err)
        msg, _ = overeni(overeniSouboru, publicKey, overeniPodpis)
        self.message.setText(msg)

    def keys(self):
        n, e, d = generateKeys()
        privateKey = (str(n) + ", " + str(d))
        publicKey = (str(n) + ", " + str(e))
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getOpenFileName()", "","Privatni klic (*.priv);;All Files (*)")
        if fileName:
            with open(fileName, "w") as f:
                f.write(privateKey)
        fileName1, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getOpenFileName()", "","Verejny klic (*.pub);;All Files (*)")
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
