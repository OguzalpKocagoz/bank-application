import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QIcon
from kullanici_giris import KullaniciGiris


def kaynak_yolu(ad):
    """Paket icine gomulen dosyalarin yolu.

    .exe olarak calisirken PyInstaller gomulu dosyalari sys._MEIPASS altindaki
    gecici klasore acar; normal calistirmada dosya bu klasorde durur.
    """
    temel = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(temel, ad)


def main():
    app = QApplication(sys.argv)

    # Uygulama stili
    app.setStyle('Fusion')
    app.setFont(QFont("Segoe UI", 9))

    simge = kaynak_yolu("banka.ico")
    if os.path.exists(simge):
        app.setWindowIcon(QIcon(simge))

    # Giriş ekranını başlat
    giris = KullaniciGiris()
    giris.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
