from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QFrame, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import bildirim
import database
import stil


class KullaniciGiris(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏦 Banka Sistemi")
        self.setMinimumSize(440, 640)
        self.resize(440, 660)
        self.setStyleSheet(stil.pencere())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(18)
        central_widget.setLayout(layout)

        layout.addWidget(self._logo_karti())
        layout.addWidget(self._giris_formu())
        layout.addStretch()

        # Veritabanını oluştur
        database.create_database()

    def _logo_karti(self):
        kart = QFrame()
        kart.setObjectName("baslikKarti")
        kart.setStyleSheet(stil.baslik_karti(stil.INDIGO))
        kart.setGraphicsEffect(golge(34, 70))

        kart_layout = QVBoxLayout()
        kart_layout.setContentsMargins(26, 30, 26, 30)
        kart_layout.setSpacing(10)
        kart.setLayout(kart_layout)

        logo = QLabel("🏦")
        logo.setStyleSheet(stil.ikon_yazisi(46))
        logo.setAlignment(Qt.AlignCenter)
        kart_layout.addWidget(logo)

        baslik = QLabel("Banka Sistemine\nHoş Geldiniz")
        baslik.setStyleSheet(stil.baslik_yazisi(24))
        baslik.setAlignment(Qt.AlignCenter)
        kart_layout.addWidget(baslik)

        return kart

    def _giris_formu(self):
        kart = QFrame()
        kart.setObjectName("kart")
        kart.setStyleSheet(stil.beyaz_kart())
        kart.setGraphicsEffect(golge(26, 35))

        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(26, 26, 26, 26)
        form_layout.setSpacing(7)
        kart.setLayout(form_layout)

        tc_label = QLabel("TC KİMLİK NO")
        tc_label.setStyleSheet(stil.alan_etiketi())
        form_layout.addWidget(tc_label)

        self.tc_entry = QLineEdit()
        self.tc_entry.setStyleSheet(stil.giris_kutusu())
        self.tc_entry.setPlaceholderText("TC Kimlik numaranızı giriniz")
        self.tc_entry.returnPressed.connect(self.giris_yap)
        form_layout.addWidget(self.tc_entry)

        form_layout.addSpacing(10)

        sifre_label = QLabel("ŞİFRE")
        sifre_label.setStyleSheet(stil.alan_etiketi())
        form_layout.addWidget(sifre_label)

        self.sifre_entry = QLineEdit()
        self.sifre_entry.setEchoMode(QLineEdit.Password)
        self.sifre_entry.setStyleSheet(stil.giris_kutusu())
        self.sifre_entry.setPlaceholderText("Şifrenizi giriniz")
        self.sifre_entry.returnPressed.connect(self.giris_yap)
        form_layout.addWidget(self.sifre_entry)

        form_layout.addSpacing(18)

        self.giris_btn = QPushButton("Giriş Yap")
        self.giris_btn.setStyleSheet(stil.buton(stil.INDIGO))
        self.giris_btn.setMinimumHeight(44)
        self.giris_btn.clicked.connect(self.giris_yap)
        form_layout.addWidget(self.giris_btn)

        form_layout.addSpacing(2)

        self.kayit_btn = QPushButton("Yeni Hesap Oluştur")
        self.kayit_btn.setStyleSheet(stil.ikincil_buton())
        self.kayit_btn.setMinimumHeight(44)
        self.kayit_btn.clicked.connect(self.kayit_sayfasina_git)
        form_layout.addWidget(self.kayit_btn)

        self.admin_btn = QPushButton("👑  Admin Girişi")
        self.admin_btn.setStyleSheet(stil.ikincil_buton())
        self.admin_btn.setMinimumHeight(44)
        self.admin_btn.clicked.connect(self.admin_giris_sayfasina_git)
        form_layout.addWidget(self.admin_btn)

        return kart

    def giris_yap(self):
        tc_no = self.tc_entry.text().strip()
        sifre = self.sifre_entry.text().strip()

        if not tc_no or not sifre:
            bildirim.uyari(self, "Lütfen tüm alanları doldurun.")
            return

        kullanici = database.giris_kontrol(tc_no, sifre)
        if kullanici:
            if kullanici[6] == 'admin':  # hesap_turu kontrolü
                from admin_panel import AdminPanel
                self.admin_panel = AdminPanel(kullanici)
                self.admin_panel.show()
            else:
                from ana_menu import AnaMenu
                self.ana_menu = AnaMenu(kullanici)
                self.ana_menu.show()
            self.close()
        else:
            bildirim.hata(self, "TC No veya şifre hatalı.")

    def kayit_sayfasina_git(self):
        from hesap_olustur import HesapOlusturFormu
        self.hesap_olustur = HesapOlusturFormu()
        self.hesap_olustur.show()
        self.close()

    def admin_giris_sayfasina_git(self):
        from admin_giris import AdminGirisFormu
        self.admin_giris = AdminGirisFormu()
        self.admin_giris.show()
        self.close()


def golge(bulanik, saydamlik):
    efekt = QGraphicsDropShadowEffect()
    efekt.setBlurRadius(bulanik)
    efekt.setColor(QColor(0, 0, 0, saydamlik))
    efekt.setOffset(0, 6)
    return efekt
