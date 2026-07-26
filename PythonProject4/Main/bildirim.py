"""Modern gorunumlu bildirim pencereleri.

QMessageBox'in isletim sistemi gorunumu yerine, uygulamanin geri kalaniyla
ayni dili konusan yuvarlak kosekli, golgeli bir diyalog kullanilir.

Kullanim:
    bildirim.basarili(self, "Hesabınız başarıyla oluşturuldu!")
    bildirim.hata(self, "Yetersiz bakiye!")
    if bildirim.onay(self, "Şifre sıfırlansın mı?"):
        ...
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QGraphicsDropShadowEffect,
                             QWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import stil


# tur -> (ikon, daire rengi, yazi rengi, varsayilan baslik, buton renkleri)
TURLER = {
    "basarili": ("✓", "#dcfce7", stil.BASARI_RENGI, "Başarılı", stil.YESIL),
    "hata": ("✕", "#fee2e2", stil.HATA_RENGI, "Hata", stil.KIRMIZI),
    "uyari": ("!", "#fef3c7", "#d97706", "Uyarı", stil.TURUNCU),
    "bilgi": ("i", "#e0e7ff", stil.INDIGO[0], "Bilgi", stil.INDIGO),
    "onay": ("?", "#e0e7ff", stil.INDIGO[0], "Onay", stil.INDIGO),
}


class Bildirim(QDialog):
    def __init__(self, parent, tur, mesaj, baslik=None, onay_mi=False):
        super().__init__(parent)
        ikon, daire_rengi, ikon_rengi, varsayilan_baslik, buton_renkleri = TURLER[tur]

        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)

        # Dis layout yalnizca golgeye yer acar.
        dis_layout = QVBoxLayout()
        dis_layout.setContentsMargins(24, 24, 24, 24)
        self.setLayout(dis_layout)

        kutu = QFrame()
        kutu.setObjectName("bildirimKutusu")
        kutu.setStyleSheet(f"""
            #bildirimKutusu {{
                background: {stil.KART_RENGI};
                border: 1px solid {stil.KENAR};
                border-radius: 18px;
            }}
        """)
        golge = QGraphicsDropShadowEffect()
        golge.setBlurRadius(40)
        golge.setColor(QColor(0, 0, 0, 60))
        golge.setOffset(0, 8)
        kutu.setGraphicsEffect(golge)
        dis_layout.addWidget(kutu)

        kutu_layout = QVBoxLayout()
        kutu_layout.setContentsMargins(28, 28, 28, 24)
        kutu_layout.setSpacing(14)
        kutu.setLayout(kutu_layout)

        # Renkli daire icinde ikon
        daire = QLabel(ikon)
        daire.setFixedSize(52, 52)
        daire.setAlignment(Qt.AlignCenter)
        daire.setStyleSheet(f"""
            background: {daire_rengi};
            color: {ikon_rengi};
            border-radius: 26px;
            font-size: 24px;
            font-weight: bold;
        """)
        daire_satiri = QHBoxLayout()
        daire_satiri.addStretch()
        daire_satiri.addWidget(daire)
        daire_satiri.addStretch()
        kutu_layout.addLayout(daire_satiri)

        baslik_etiketi = QLabel(baslik or varsayilan_baslik)
        baslik_etiketi.setAlignment(Qt.AlignCenter)
        baslik_etiketi.setStyleSheet(stil.bolum_basligi(17))
        kutu_layout.addWidget(baslik_etiketi)

        mesaj_etiketi = QLabel(mesaj)
        mesaj_etiketi.setAlignment(Qt.AlignCenter)
        mesaj_etiketi.setWordWrap(True)
        mesaj_etiketi.setStyleSheet(stil.soluk_yazi(13))
        kutu_layout.addWidget(mesaj_etiketi)

        kutu_layout.addSpacing(6)

        buton_satiri = QHBoxLayout()
        buton_satiri.setSpacing(10)

        if onay_mi:
            vazgec_btn = QPushButton("Vazgeç")
            vazgec_btn.setStyleSheet(stil.ikincil_buton())
            vazgec_btn.setMinimumHeight(40)
            vazgec_btn.clicked.connect(self.reject)
            buton_satiri.addWidget(vazgec_btn)

        tamam_btn = QPushButton("Devam Et" if onay_mi else "Tamam")
        tamam_btn.setStyleSheet(stil.buton(buton_renkleri))
        tamam_btn.setMinimumHeight(40)
        tamam_btn.setDefault(True)
        tamam_btn.clicked.connect(self.accept)
        buton_satiri.addWidget(tamam_btn)

        kutu_layout.addLayout(buton_satiri)

        self.setMinimumWidth(400)
        tamam_btn.setFocus()

    def showEvent(self, olay):
        """Diyalogu ana pencerenin ortasina yerlestir."""
        super().showEvent(olay)
        ebeveyn = self.parentWidget()
        if ebeveyn is not None:
            merkez = ebeveyn.geometry().center()
            self.move(merkez.x() - self.width() // 2,
                      merkez.y() - self.height() // 2)


class GirdiDiyalogu(QDialog):
    """Tek satirlik bir deger isteyen, bildirimle ayni gorunumde diyalog."""

    def __init__(self, parent, baslik, mesaj, ipucu="", gizli=False):
        super().__init__(parent)
        from PyQt5.QtWidgets import QLineEdit

        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)

        dis_layout = QVBoxLayout()
        dis_layout.setContentsMargins(24, 24, 24, 24)
        self.setLayout(dis_layout)

        kutu = QFrame()
        kutu.setObjectName("bildirimKutusu")
        kutu.setStyleSheet(f"""
            #bildirimKutusu {{
                background: {stil.KART_RENGI};
                border: 1px solid {stil.KENAR};
                border-radius: 18px;
            }}
        """)
        golge = QGraphicsDropShadowEffect()
        golge.setBlurRadius(40)
        golge.setColor(QColor(0, 0, 0, 60))
        golge.setOffset(0, 8)
        kutu.setGraphicsEffect(golge)
        dis_layout.addWidget(kutu)

        kutu_layout = QVBoxLayout()
        kutu_layout.setContentsMargins(28, 26, 28, 24)
        kutu_layout.setSpacing(8)
        kutu.setLayout(kutu_layout)

        baslik_etiketi = QLabel(baslik)
        baslik_etiketi.setStyleSheet(stil.bolum_basligi(17))
        kutu_layout.addWidget(baslik_etiketi)

        mesaj_etiketi = QLabel(mesaj)
        mesaj_etiketi.setWordWrap(True)
        mesaj_etiketi.setStyleSheet(stil.soluk_yazi(13))
        kutu_layout.addWidget(mesaj_etiketi)

        kutu_layout.addSpacing(8)

        self.giris = QLineEdit()
        self.giris.setStyleSheet(stil.giris_kutusu())
        self.giris.setPlaceholderText(ipucu)
        if gizli:
            self.giris.setEchoMode(QLineEdit.Password)
        self.giris.returnPressed.connect(self.accept)
        kutu_layout.addWidget(self.giris)

        kutu_layout.addSpacing(10)

        buton_satiri = QHBoxLayout()
        buton_satiri.setSpacing(10)
        buton_satiri.addStretch()

        vazgec_btn = QPushButton("Vazgeç")
        vazgec_btn.setStyleSheet(stil.ikincil_buton())
        vazgec_btn.setMinimumHeight(40)
        vazgec_btn.clicked.connect(self.reject)
        buton_satiri.addWidget(vazgec_btn)

        tamam_btn = QPushButton("Kaydet")
        tamam_btn.setStyleSheet(stil.buton(stil.INDIGO))
        tamam_btn.setMinimumHeight(40)
        tamam_btn.setDefault(True)
        tamam_btn.clicked.connect(self.accept)
        buton_satiri.addWidget(tamam_btn)

        kutu_layout.addLayout(buton_satiri)

        self.setMinimumWidth(420)
        self.giris.setFocus()

    def showEvent(self, olay):
        super().showEvent(olay)
        ebeveyn = self.parentWidget()
        if ebeveyn is not None:
            merkez = ebeveyn.geometry().center()
            self.move(merkez.x() - self.width() // 2,
                      merkez.y() - self.height() // 2)


def girdi_iste(parent, baslik, mesaj, ipucu="", gizli=False):
    """Kullanici 'Kaydet' derse girilen metni, aksi halde None doner."""
    diyalog = GirdiDiyalogu(parent, baslik, mesaj, ipucu, gizli)
    if diyalog.exec_() == QDialog.Accepted:
        return diyalog.giris.text().strip()
    return None


def _goster(parent, tur, mesaj, baslik=None):
    Bildirim(parent, tur, mesaj, baslik).exec_()


def basarili(parent, mesaj, baslik=None):
    _goster(parent, "basarili", mesaj, baslik)


def hata(parent, mesaj, baslik=None):
    _goster(parent, "hata", mesaj, baslik)


def uyari(parent, mesaj, baslik=None):
    _goster(parent, "uyari", mesaj, baslik)


def bilgi(parent, mesaj, baslik=None):
    _goster(parent, "bilgi", mesaj, baslik)


def onay(parent, mesaj, baslik=None):
    """Kullanici 'Devam Et' derse True doner."""
    return Bildirim(parent, "onay", mesaj, baslik, onay_mi=True).exec_() == QDialog.Accepted
