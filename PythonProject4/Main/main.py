import sys
from PyQt5.QtWidgets import QApplication
from kullanici_giris import KullaniciGiris

def main():
    app = QApplication(sys.argv)
    
    # Uygulama stili
    app.setStyle('Fusion')
    
    # Giriş ekranını başlat
    giris = KullaniciGiris()
    giris.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()