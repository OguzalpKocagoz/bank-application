"""Para yatirma / cekme / transfer ekranlarinin ortak iskeleti.

Ucu de ayni duzeni kullanir: renkli baslik karti, guncel bakiye, bir veya iki
giris alani ve tek bir eylem butonu. Fark eden kisimlar alt siniftan gelir.
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFrame,
                             QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import database
import stil


class IslemEkrani(QMainWindow):
    # Alt siniflar doldurur
    BASLIK = ""
    IKON = ""
    RENK = stil.INDIGO
    BUTON_YAZISI = ""
    ALANLAR = []  # [(anahtar, etiket, ipucu)]

    def __init__(self, kullanici_bilgileri):
        super().__init__()
        self.kullanici_bilgileri = kullanici_bilgileri
        self.setWindowTitle(f"{self.IKON} {self.BASLIK}")
        yukseklik = 400 + 76 * (len(self.ALANLAR) - 1)
        self.setMinimumSize(460, yukseklik)
        self.resize(480, yukseklik + 20)
        self.setStyleSheet(stil.pencere())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(18)
        central_widget.setLayout(layout)

        layout.addWidget(self._baslik_karti())
        layout.addWidget(self._form_karti())
        layout.addStretch()

    def _baslik_karti(self):
        kart = QFrame()
        kart.setObjectName("baslikKarti")
        kart.setStyleSheet(stil.baslik_karti(self.RENK))
        kart.setGraphicsEffect(_golge(32, 65))

        kart_layout = QVBoxLayout()
        kart_layout.setContentsMargins(26, 22, 26, 24)
        kart_layout.setSpacing(4)
        kart.setLayout(kart_layout)

        ikon = QLabel(self.IKON)
        ikon.setStyleSheet(stil.ikon_yazisi(30))
        kart_layout.addWidget(ikon)

        baslik = QLabel(self.BASLIK)
        baslik.setStyleSheet(stil.baslik_yazisi(22))
        kart_layout.addWidget(baslik)

        kart_layout.addSpacing(8)

        self.bakiye_label = QLabel()
        self.bakiye_label.setStyleSheet(stil.alt_baslik())
        kart_layout.addWidget(self.bakiye_label)
        self.bakiye_yenile()

        return kart

    def _form_karti(self):
        kart = QFrame()
        kart.setObjectName("kart")
        kart.setStyleSheet(stil.beyaz_kart())
        kart.setGraphicsEffect(_golge(26, 35))

        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(26, 26, 26, 26)
        form_layout.setSpacing(7)
        kart.setLayout(form_layout)

        self.alanlar = {}
        for sira, (anahtar, etiket_yazisi, ipucu) in enumerate(self.ALANLAR):
            if sira:
                form_layout.addSpacing(10)

            etiket = QLabel(etiket_yazisi)
            etiket.setStyleSheet(stil.alan_etiketi())
            form_layout.addWidget(etiket)

            giris = QLineEdit()
            giris.setStyleSheet(stil.giris_kutusu(self.RENK))
            giris.setPlaceholderText(ipucu)
            giris.returnPressed.connect(self.uygula)
            form_layout.addWidget(giris)

            self.alanlar[anahtar] = giris

        form_layout.addSpacing(18)

        btn = QPushButton(self.BUTON_YAZISI)
        btn.setStyleSheet(stil.buton(self.RENK))
        btn.setMinimumHeight(46)
        btn.clicked.connect(self.uygula)
        form_layout.addWidget(btn)

        return kart

    # --- yardimcilar ------------------------------------------------------

    def deger(self, anahtar):
        return self.alanlar[anahtar].text().strip()

    def temizle(self):
        for giris in self.alanlar.values():
            giris.clear()

    def bakiye_yenile(self):
        bakiye = database.bakiye_getir(self.kullanici_bilgileri[1])
        if bakiye is not None:
            self.bakiye_label.setText(f"Güncel bakiye:  ₺{bakiye:,.2f}")

    def uygula(self):
        """Alt sinif doldurur."""
        raise NotImplementedError


def _golge(bulanik, saydamlik):
    efekt = QGraphicsDropShadowEffect()
    efekt.setBlurRadius(bulanik)
    efekt.setColor(QColor(0, 0, 0, saydamlik))
    efekt.setOffset(0, 6)
    return efekt
