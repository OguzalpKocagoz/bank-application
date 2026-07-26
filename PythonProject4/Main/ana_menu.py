from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel,
                             QHBoxLayout, QFrame, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QColor
import database
import stil
from para_yatir import ParaYatirFormu
from para_cek import ParaCekFormu
from para_transfer import ParaTransferFormu
from islem_gecmisi import IslemGecmisiFormu


class AnaMenu(QMainWindow):
    def __init__(self, kullanici_bilgileri):
        super().__init__()
        self.kullanici_bilgileri = kullanici_bilgileri
        self.setWindowTitle("🏦 Banka Uygulaması")
        self.setMinimumSize(600, 560)
        self.resize(680, 620)
        self.setStyleSheet(stil.pencere())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(18)
        central_widget.setLayout(layout)

        layout.addWidget(self._bakiye_karti())
        layout.addWidget(self._islemler_karti())
        layout.addStretch()

    def _bakiye_karti(self):
        """Ust kart: kullanici adi ve guncel bakiye."""
        kart = QFrame()
        kart.setObjectName("baslikKarti")
        kart.setStyleSheet(stil.baslik_karti(stil.INDIGO))
        kart.setGraphicsEffect(_golge(34, 70))

        kart_layout = QVBoxLayout()
        kart_layout.setContentsMargins(28, 26, 28, 28)
        kart_layout.setSpacing(4)
        kart.setLayout(kart_layout)

        hosgeldin_label = QLabel(
            f"Hoş geldiniz, {self.kullanici_bilgileri[2]} {self.kullanici_bilgileri[3]}"
        )
        hosgeldin_label.setStyleSheet(stil.alt_baslik())
        kart_layout.addWidget(hosgeldin_label)

        kart_layout.addSpacing(6)

        bakiye_basligi = QLabel("TOPLAM BAKİYE")
        bakiye_basligi.setStyleSheet(
            "color: rgba(255,255,255,0.7); font-size: 11px; "
            "font-weight: 600; letter-spacing: 1px;")
        kart_layout.addWidget(bakiye_basligi)

        self.bakiye_label = QLabel(f"₺{self.kullanici_bilgileri[5]:,.2f}")
        self.bakiye_label.setStyleSheet(
            "color: white; font-size: 34px; font-weight: 600;")
        kart_layout.addWidget(self.bakiye_label)

        kart_layout.addSpacing(8)

        tc_label = QLabel(f"TC  ·  {self.kullanici_bilgileri[1]}")
        tc_label.setStyleSheet(
            "color: rgba(255,255,255,0.7); font-size: 12px; letter-spacing: 0.5px;")
        kart_layout.addWidget(tc_label)

        return kart

    def _islemler_karti(self):
        kart = QFrame()
        kart.setObjectName("kart")
        kart.setStyleSheet(stil.beyaz_kart())
        kart.setGraphicsEffect(_golge(26, 35))

        kart_layout = QVBoxLayout()
        kart_layout.setContentsMargins(24, 22, 24, 24)
        kart_layout.setSpacing(12)
        kart.setLayout(kart_layout)

        baslik = QLabel("Para İşlemleri")
        baslik.setStyleSheet(stil.bolum_basligi(16))
        kart_layout.addWidget(baslik)

        butonlar = [
            ("💰", "Para Yatır", "Hesabınıza para ekleyin",
             stil.YESIL, self.para_yatir_penceresi_ac),
            ("💸", "Para Transfer", "Başka bir hesaba gönderin",
             stil.TEAL, self.para_transfer_penceresi_ac),
            ("🏧", "Para Çek", "Hesabınızdan para çekin",
             stil.TURUNCU, self.para_cek_penceresi_ac),
            ("📊", "İşlem Geçmişi", "Geçmiş hareketlerinizi görün",
             stil.INDIGO, self.islem_gecmisi_penceresi_ac),
        ]
        for ikon, yazi, aciklama, renk, islev in butonlar:
            kart_layout.addWidget(
                self._islem_satiri(ikon, yazi, aciklama, renk, islev))

        return kart

    def _islem_satiri(self, ikon, yazi, aciklama, renk, islev):
        """Ikon + baslik + aciklamadan olusan tiklanabilir satir."""
        btn = QPushButton()
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumHeight(66)
        btn.clicked.connect(islev)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: #fbfbfc;
                border: 1px solid {stil.KENAR};
                border-radius: 12px;
                text-align: left;
            }}
            QPushButton:hover {{
                background: #f5f6f8;
                border: 1px solid {renk[0]};
            }}
            QPushButton:pressed {{
                background: #eef0f3;
            }}
        """)

        satir = QHBoxLayout()
        satir.setContentsMargins(14, 10, 16, 10)
        satir.setSpacing(14)
        btn.setLayout(satir)

        ikon_etiketi = QLabel(ikon)
        ikon_etiketi.setFixedSize(42, 42)
        ikon_etiketi.setAlignment(Qt.AlignCenter)
        ikon_etiketi.setStyleSheet(f"""
            background: {renk[0]};
            border-radius: 12px;
            font-size: 19px;
        """)
        satir.addWidget(ikon_etiketi)

        yazi_kutusu = QVBoxLayout()
        yazi_kutusu.setSpacing(2)

        ust = QLabel(yazi)
        ust.setStyleSheet(
            f"color: {stil.YAZI_RENGI}; font-size: 14px; font-weight: 600; "
            f"background: transparent;")
        yazi_kutusu.addWidget(ust)

        alt = QLabel(aciklama)
        alt.setStyleSheet(
            f"color: {stil.SOLUK_YAZI}; font-size: 12px; background: transparent;")
        yazi_kutusu.addWidget(alt)

        satir.addLayout(yazi_kutusu)
        satir.addStretch()

        ok = QLabel("›")
        ok.setStyleSheet(
            f"color: {stil.SOLUK_YAZI}; font-size: 20px; background: transparent;")
        satir.addWidget(ok)

        return btn

    def event(self, olay):
        # İşlem penceresi kapanınca ana menü tekrar öne gelir; bakiyeyi o anda
        # veritabanından tazeleyerek eski değeri göstermesini engelliyoruz.
        if olay.type() == QEvent.WindowActivate:
            self.bakiye_yenile()
        return super().event(olay)

    def bakiye_yenile(self):
        bakiye = database.bakiye_getir(self.kullanici_bilgileri[1])
        if bakiye is None:
            return
        self.kullanici_bilgileri = self.kullanici_bilgileri[:5] + (bakiye,) + \
            tuple(self.kullanici_bilgileri[6:])
        self.bakiye_label.setText(f"₺{bakiye:,.2f}")

    def para_yatir_penceresi_ac(self):
        self.para_yatir = ParaYatirFormu(self.kullanici_bilgileri)
        self.para_yatir.show()

    def para_cek_penceresi_ac(self):
        self.para_cek = ParaCekFormu(self.kullanici_bilgileri)
        self.para_cek.show()

    def para_transfer_penceresi_ac(self):
        self.para_transfer = ParaTransferFormu(self.kullanici_bilgileri)
        self.para_transfer.show()

    def islem_gecmisi_penceresi_ac(self):
        self.islem_gecmisi = IslemGecmisiFormu(self.kullanici_bilgileri)
        self.islem_gecmisi.show()


def _golge(bulanik, saydamlik):
    efekt = QGraphicsDropShadowEffect()
    efekt.setBlurRadius(bulanik)
    efekt.setColor(QColor(0, 0, 0, saydamlik))
    efekt.setOffset(0, 6)
    return efekt
