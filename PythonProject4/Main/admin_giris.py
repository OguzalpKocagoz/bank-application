from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFrame,
                             QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import bildirim
import database
import stil


class AdminGirisFormu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("👑 Admin Girişi")
        self.setMinimumSize(440, 540)
        self.resize(440, 560)
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
        kart.setStyleSheet(stil.baslik_karti(stil.MOR))
        kart.setGraphicsEffect(_golge(32, 65))

        kart_layout = QVBoxLayout()
        kart_layout.setContentsMargins(26, 28, 26, 28)
        kart_layout.setSpacing(8)
        kart.setLayout(kart_layout)

        ikon = QLabel("👑")
        ikon.setStyleSheet(stil.ikon_yazisi(40))
        ikon.setAlignment(Qt.AlignCenter)
        kart_layout.addWidget(ikon)

        baslik = QLabel("Admin Girişi")
        baslik.setStyleSheet(stil.baslik_yazisi(22))
        baslik.setAlignment(Qt.AlignCenter)
        kart_layout.addWidget(baslik)

        alt = QLabel("Yönetim paneline erişmek için giriş yapın")
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

        # Giriş TC No ile yapılıyor; etiket de bunu söylesin.
        kullanici_label = QLabel("TC KİMLİK NO")
        kullanici_label.setStyleSheet(stil.alan_etiketi())
        form_layout.addWidget(kullanici_label)

        self.kullanici_entry = QLineEdit()
        self.kullanici_entry.setStyleSheet(stil.giris_kutusu(stil.MOR))
        self.kullanici_entry.setPlaceholderText("Admin TC kimlik numarası")
        self.kullanici_entry.returnPressed.connect(self.admin_giris)
        form_layout.addWidget(self.kullanici_entry)

        form_layout.addSpacing(10)

        sifre_label = QLabel("ŞİFRE")
        sifre_label.setStyleSheet(stil.alan_etiketi())
        form_layout.addWidget(sifre_label)

        self.sifre_entry = QLineEdit()
        self.sifre_entry.setEchoMode(QLineEdit.Password)
        self.sifre_entry.setStyleSheet(stil.giris_kutusu(stil.MOR))
        self.sifre_entry.setPlaceholderText("Admin şifrenizi giriniz")
        self.sifre_entry.returnPressed.connect(self.admin_giris)
        form_layout.addWidget(self.sifre_entry)

        form_layout.addSpacing(18)

        self.giris_btn = QPushButton("Giriş Yap")
        self.giris_btn.setStyleSheet(stil.buton(stil.MOR))
        self.giris_btn.setMinimumHeight(44)
        self.giris_btn.clicked.connect(self.admin_giris)
        form_layout.addWidget(self.giris_btn)

        form_layout.addSpacing(2)

        self.geri_btn = QPushButton("Geri Dön")
        self.geri_btn.setStyleSheet(stil.ikincil_buton())
        self.geri_btn.setMinimumHeight(44)
        self.geri_btn.clicked.connect(self.geri_don)
        form_layout.addWidget(self.geri_btn)

        return kart

    def admin_giris(self):
        tc_no = self.kullanici_entry.text().strip()
        sifre = self.sifre_entry.text().strip()

        if not tc_no or not sifre:
            bildirim.uyari(self, "Lütfen tüm alanları doldurun.")
            return

        kullanici = database.giris_kontrol(tc_no, sifre)
        if kullanici and kullanici[6] == 'admin':
            from admin_panel import AdminPanel
            self.admin_panel = AdminPanel(kullanici)
            self.admin_panel.show()
            self.close()
        else:
            bildirim.hata(self, "Admin bilgileri hatalı.")

    def geri_don(self):
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
