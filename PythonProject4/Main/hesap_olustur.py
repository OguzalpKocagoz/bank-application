from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFrame, QHBoxLayout,
                             QGraphicsDropShadowEffect, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import bildirim
import database
import stil


class HesapOlusturFormu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("✨ Yeni Hesap Oluştur")
        self.setMinimumSize(540, 640)
        self.resize(560, 780)
        self.setStyleSheet(stil.pencere())

        # Pencere kucultuldugunde alanlar sikismasin diye form kaydirilabilir.
        kaydirma = QScrollArea()
        kaydirma.setWidgetResizable(True)
        kaydirma.setFrameShape(QFrame.NoFrame)
        kaydirma.setStyleSheet(
            f"QScrollArea, QScrollArea > QWidget > QWidget "
            f"{{ background: {stil.ARKA_PLAN}; }}")
        self.setCentralWidget(kaydirma)

        govde = QWidget()
        kaydirma.setWidget(govde)

        layout = QVBoxLayout()
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(18)
        govde.setLayout(layout)

        layout.addWidget(self._baslik_karti())
        layout.addWidget(self._form_karti())
        layout.addStretch()

    def _baslik_karti(self):
        kart = QFrame()
        kart.setObjectName("baslikKarti")
        kart.setStyleSheet(stil.baslik_karti(stil.YESIL))
        kart.setGraphicsEffect(_golge(32, 65))

        kart_layout = QVBoxLayout()
        kart_layout.setContentsMargins(26, 26, 26, 26)
        kart_layout.setSpacing(8)
        kart.setLayout(kart_layout)

        ikon = QLabel("✨")
        ikon.setStyleSheet(stil.ikon_yazisi(38))
        ikon.setAlignment(Qt.AlignCenter)
        kart_layout.addWidget(ikon)

        baslik = QLabel("Yeni Hesap Oluştur")
        baslik.setStyleSheet(stil.baslik_yazisi(22))
        baslik.setAlignment(Qt.AlignCenter)
        kart_layout.addWidget(baslik)

        alt = QLabel("Bilgilerinizi girerek hesabınızı oluşturun")
        alt.setStyleSheet(stil.alt_baslik())
        alt.setAlignment(Qt.AlignCenter)
        kart_layout.addWidget(alt)

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

        self.form_alanlari = {}
        alanlar = [
            ("TC KİMLİK NO", "tc_entry", "11 haneli TC kimlik numaranız", False),
            ("AD", "ad_entry", "Adınız", False),
            ("SOYAD", "soyad_entry", "Soyadınız", False),
            ("TELEFON", "telefon_entry", "10 haneli telefon numaranız", False),
            ("ŞİFRE", "sifre_entry", "En az 6 karakterli şifreniz", True),
            ("ŞİFRE TEKRAR", "sifre_tekrar_entry", "Şifrenizi tekrar girin", True),
        ]
        for etiket, ad, ipucu, sifre_mi in alanlar:
            self.form_alani_ekle(form_layout, etiket, ad, ipucu, sifre_mi)

        form_layout.addSpacing(16)

        buton_satiri = QHBoxLayout()
        buton_satiri.setSpacing(10)

        self.geri_btn = QPushButton("Geri Dön")
        self.geri_btn.setStyleSheet(stil.ikincil_buton())
        self.geri_btn.setMinimumHeight(44)
        self.geri_btn.clicked.connect(self.giris_sayfasina_don)
        buton_satiri.addWidget(self.geri_btn)

        self.kayit_btn = QPushButton("Hesap Oluştur")
        self.kayit_btn.setStyleSheet(stil.buton(stil.YESIL))
        self.kayit_btn.setMinimumHeight(44)
        self.kayit_btn.clicked.connect(self.hesap_olustur)
        buton_satiri.addWidget(self.kayit_btn, 1)

        form_layout.addLayout(buton_satiri)
        return kart

    def form_alani_ekle(self, layout, etiket_text, entry_name,
                        placeholder_text="", sifre_mi=False):
        if layout.count():
            layout.addSpacing(10)

        etiket = QLabel(etiket_text)
        etiket.setStyleSheet(stil.alan_etiketi())
        layout.addWidget(etiket)

        entry = QLineEdit()
        if sifre_mi:
            entry.setEchoMode(QLineEdit.Password)
        entry.setStyleSheet(stil.giris_kutusu(stil.YESIL))
        entry.setPlaceholderText(placeholder_text)
        entry.returnPressed.connect(self.hesap_olustur)
        layout.addWidget(entry)

        self.form_alanlari[entry_name] = entry

    def hesap_olustur(self):
        # Form verilerini al
        tc_no = self.form_alanlari["tc_entry"].text().strip()
        ad = self.form_alanlari["ad_entry"].text().strip()
        soyad = self.form_alanlari["soyad_entry"].text().strip()
        telefon = self.form_alanlari["telefon_entry"].text().strip()
        sifre = self.form_alanlari["sifre_entry"].text().strip()
        sifre_tekrar = self.form_alanlari["sifre_tekrar_entry"].text().strip()

        # Boş alan kontrolü
        if not all([tc_no, ad, soyad, telefon, sifre, sifre_tekrar]):
            bildirim.uyari(self, "Lütfen tüm alanları doldurun.")
            return

        # TC No kontrolü
        if not tc_no.isdigit() or len(tc_no) != 11:
            bildirim.uyari(self, "TC Kimlik No 11 haneli bir sayı olmalıdır.")
            return

        # Telefon format kontrolü
        telefon = telefon.replace(" ", "")
        if not telefon.isdigit() or len(telefon) != 10:
            bildirim.uyari(self, "Telefon numarası 10 haneli olmalıdır.")
            return

        # Şifre kontrolü
        if sifre != sifre_tekrar:
            bildirim.uyari(self, "Girdiğiniz iki şifre birbiriyle eşleşmiyor.")
            return

        if len(sifre) < 6:
            bildirim.uyari(self, "Şifreniz en az 6 karakter olmalıdır.")
            return

        # Veritabanına kaydet
        if database.kayit_ekle(tc_no, ad, soyad, telefon, sifre):
            bildirim.basarili(
                self,
                f"Sayın {ad} {soyad}, hesabınız oluşturuldu.\n"
                f"TC kimlik numaranız ve şifrenizle giriş yapabilirsiniz.",
                baslik="Hesabınız Hazır")
            self.giris_sayfasina_don()
        else:
            bildirim.hata(self, "Bu TC No ile kayıtlı bir hesap zaten var.")

    def giris_sayfasina_don(self):
        from kullanici_giris import KullaniciGiris
        self.giris = KullaniciGiris()
        self.giris.show()
        self.close()


def _golge(bulanik, saydamlik):
    efekt = QGraphicsDropShadowEffect()
    efekt.setBlurRadius(bulanik)
    efekt.setColor(QColor(0, 0, 0, saydamlik))
    efekt.setOffset(0, 6)
    return efekt
