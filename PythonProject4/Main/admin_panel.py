from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
                             QTabWidget, QTreeWidget, QTreeWidgetItem, QPushButton,
                             QFrame, QHBoxLayout, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import bildirim
import database
import stil


# İşlem türü -> (etiket, bakiyeyi artırıyor mu)
ISLEM_ETIKETLERI = {
    'yatirma': ('⬆️  Para Yatırma', True),
    'cekme': ('⬇️  Para Çekme', False),
    'transfer_alma': ('⬅️  Transfer (Gelen)', True),
    'transfer_gonderme': ('➡️  Transfer (Giden)', False),
}


class AdminPanel(QMainWindow):
    def __init__(self, admin_bilgileri):
        super().__init__()
        self.admin_bilgileri = admin_bilgileri
        self.setWindowTitle("👑 Admin Paneli")
        self.setMinimumSize(860, 620)
        self.resize(980, 700)
        self.setStyleSheet(stil.pencere())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)
        central_widget.setLayout(layout)

        layout.addWidget(self._baslik_karti())
        layout.addLayout(self._ozet_satiri())

        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(stil.sekme())
        self.tab_widget.addTab(self._kullanicilar_sekmesi(), "👥  Kullanıcılar")
        self.tab_widget.addTab(self._islemler_sekmesi(), "📊  İşlem Geçmişi")
        layout.addWidget(self.tab_widget, 1)

        self.verileri_yenile()

    # --- ust bolum --------------------------------------------------------

    def _baslik_karti(self):
        kart = QFrame()
        kart.setObjectName("baslikKarti")
        kart.setStyleSheet(stil.baslik_karti(stil.MOR))
        kart.setGraphicsEffect(_golge(32, 65))

        kart_layout = QHBoxLayout()
        kart_layout.setContentsMargins(26, 22, 26, 22)
        kart_layout.setSpacing(16)
        kart.setLayout(kart_layout)

        ikon = QLabel("👑")
        ikon.setStyleSheet(stil.ikon_yazisi(34))
        kart_layout.addWidget(ikon)

        yazi_kutusu = QVBoxLayout()
        yazi_kutusu.setSpacing(2)

        baslik = QLabel("Admin Paneli")
        baslik.setStyleSheet(stil.baslik_yazisi(22))
        yazi_kutusu.addWidget(baslik)

        alt = QLabel(f"{self.admin_bilgileri[2]} {self.admin_bilgileri[3]} "
                     f"·  TC {self.admin_bilgileri[1]}")
        alt.setStyleSheet(stil.alt_baslik())
        yazi_kutusu.addWidget(alt)

        kart_layout.addLayout(yazi_kutusu)
        kart_layout.addStretch()

        cikis_btn = QPushButton("Çıkış Yap")
        cikis_btn.setStyleSheet(f"""
            QPushButton {{
                background: rgba(255,255,255,0.18);
                color: white;
                padding: 10px 20px;
                border: 1px solid rgba(255,255,255,0.35);
                border-radius: 10px;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{ background: rgba(255,255,255,0.28); }}
            QPushButton:pressed {{ background: rgba(255,255,255,0.14); }}
        """)
        cikis_btn.setMinimumHeight(40)
        cikis_btn.setCursor(Qt.PointingHandCursor)
        cikis_btn.clicked.connect(self.cikis_yap)
        kart_layout.addWidget(cikis_btn)

        return kart

    def _ozet_satiri(self):
        """Ust uste degil, yan yana duran uc ozet kutusu."""
        satir = QHBoxLayout()
        satir.setSpacing(14)

        self.ozet_kutulari = {}
        for anahtar, etiket, renk in [
            ("kullanici", "TOPLAM KULLANICI", stil.INDIGO),
            ("bakiye", "TOPLAM BAKİYE", stil.YESIL),
            ("islem", "TOPLAM İŞLEM", stil.TEAL),
        ]:
            kutu = QFrame()
            kutu.setObjectName("ozetKutusu")
            kutu.setStyleSheet(f"""
                #ozetKutusu {{
                    background: {stil.KART_RENGI};
                    border: 1px solid {stil.KENAR};
                    border-radius: 14px;
                }}
            """)
            kutu_layout = QVBoxLayout()
            kutu_layout.setContentsMargins(18, 14, 18, 16)
            kutu_layout.setSpacing(4)
            kutu.setLayout(kutu_layout)

            baslik = QLabel(etiket)
            baslik.setStyleSheet(stil.alan_etiketi())
            kutu_layout.addWidget(baslik)

            deger = QLabel("—")
            deger.setStyleSheet(
                f"color: {renk[0]}; font-size: 24px; font-weight: 600;")
            kutu_layout.addWidget(deger)

            self.ozet_kutulari[anahtar] = deger
            satir.addWidget(kutu)

        return satir

    # --- sekmeler ---------------------------------------------------------

    def _sekme_govdesi(self, agac, dugmeler):
        sekme = QWidget()
        sekme_layout = QVBoxLayout()
        sekme_layout.setContentsMargins(18, 18, 18, 18)
        sekme_layout.setSpacing(12)
        sekme.setLayout(sekme_layout)

        sekme_layout.addWidget(agac)

        alt_satir = QHBoxLayout()
        alt_satir.setSpacing(10)
        alt_satir.addStretch()
        for yazi, bicim, islev in dugmeler:
            btn = QPushButton(yazi)
            btn.setStyleSheet(bicim)
            btn.setMinimumHeight(42)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(islev)
            alt_satir.addWidget(btn)
        sekme_layout.addLayout(alt_satir)

        return sekme

    def _kullanicilar_sekmesi(self):
        self.kullanici_tree = QTreeWidget()
        self.kullanici_tree.setHeaderLabels(
            ['TC No', 'Ad', 'Soyad', 'Telefon', 'Bakiye', 'Şifre'])
        self.kullanici_tree.setRootIsDecorated(False)
        self.kullanici_tree.setStyleSheet(stil.agac())
        self.kullanici_tree.itemDoubleClicked.connect(
            lambda *_: self.sifre_bilgisi_goster())

        return self._sekme_govdesi(self.kullanici_tree, [
            ("🔍  Şifre Bilgisi", stil.ikincil_buton(), self.sifre_bilgisi_goster),
            ("🔑  Şifre Sıfırla", stil.buton(stil.TURUNCU), self.sifre_sifirla),
            ("🔄  Yenile", stil.ikincil_buton(), self.verileri_yenile),
        ])

    def _islemler_sekmesi(self):
        self.islem_tree = QTreeWidget()
        self.islem_tree.setHeaderLabels(
            ['Tarih', 'TC No', 'Ad Soyad', 'İşlem Türü', 'Miktar', 'Açıklama'])
        self.islem_tree.setRootIsDecorated(False)
        self.islem_tree.setStyleSheet(stil.agac())

        return self._sekme_govdesi(self.islem_tree, [
            ("🔄  Yenile", stil.ikincil_buton(), self.verileri_yenile),
        ])

    # --- veri -------------------------------------------------------------

    def verileri_yenile(self):
        self.kullanicilari_goster()
        self.islemleri_goster()

    def kullanicilari_goster(self):
        self.kullanici_tree.clear()

        kullanicilar = database.tum_kullanicilari_getir()
        toplam_bakiye = 0.0

        for kullanici in kullanicilar:
            item = QTreeWidgetItem(self.kullanici_tree)

            item.setText(0, kullanici[0])  # TC No
            item.setText(1, kullanici[1])  # Ad
            item.setText(2, kullanici[2])  # Soyad
            item.setText(3, kullanici[3])  # Telefon
            item.setText(4, f"₺{kullanici[4]:,.2f}")  # Bakiye
            # Şifreler geri çevrilemez biçimde saklandığı için gösterilemez.
            item.setText(5, "•••••••• (hashli)")

            item.setForeground(4, QColor(stil.BASARI_RENGI if kullanici[4] > 0
                                         else stil.SOLUK_YAZI))
            item.setForeground(5, QColor(stil.SOLUK_YAZI))
            item.setTextAlignment(4, Qt.AlignRight | Qt.AlignVCenter)

            toplam_bakiye += kullanici[4]

        for i in range(6):
            self.kullanici_tree.resizeColumnToContents(i)

        self.ozet_kutulari["kullanici"].setText(str(len(kullanicilar)))
        self.ozet_kutulari["bakiye"].setText(f"₺{toplam_bakiye:,.2f}")

        if not kullanicilar:
            bos_item = QTreeWidgetItem(self.kullanici_tree)
            bos_item.setText(1, "Henüz kullanıcı bulunmuyor")
            bos_item.setForeground(1, QColor(stil.SOLUK_YAZI))

    def islemleri_goster(self):
        self.islem_tree.clear()

        islemler = database.tum_islemleri_getir()

        for islem in islemler:
            item = QTreeWidgetItem(self.islem_tree)

            item.setText(0, database.tarih_goster(islem[0]))
            item.setText(1, islem[1])  # TC No
            item.setText(2, islem[2])  # Ad Soyad

            etiket, artan = ISLEM_ETIKETLERI.get(islem[3], (islem[3], False))
            item.setText(3, etiket)
            if artan:
                item.setText(4, f"+ ₺{islem[4]:,.2f}")
                item.setForeground(4, QColor(stil.BASARI_RENGI))
            else:
                item.setText(4, f"− ₺{islem[4]:,.2f}")
                item.setForeground(4, QColor(stil.HATA_RENGI))

            item.setText(5, islem[5])  # Açıklama
            item.setTextAlignment(4, Qt.AlignRight | Qt.AlignVCenter)

        for i in range(6):
            self.islem_tree.resizeColumnToContents(i)

        self.ozet_kutulari["islem"].setText(str(len(islemler)))

        if not islemler:
            bos_item = QTreeWidgetItem(self.islem_tree)
            bos_item.setText(2, "Henüz işlem bulunmuyor")
            bos_item.setForeground(2, QColor(stil.SOLUK_YAZI))

    # --- sifre islemleri --------------------------------------------------

    def _secili_kullanici(self):
        """Listede secili satirin (tc_no, ad_soyad) bilgisi."""
        secili = self.kullanici_tree.selectedItems()
        if not secili or not secili[0].text(0):
            bildirim.uyari(self, "Önce listeden bir kullanıcı seçin.")
            return None
        item = secili[0]
        return item.text(0), f"{item.text(1)} {item.text(2)}"

    def sifre_bilgisi_goster(self):
        """Veritabaninda o hesap icin gercekte ne saklandigini gosterir."""
        secim = self._secili_kullanici()
        if not secim:
            return
        tc_no, ad_soyad = secim

        kayit = database.sifre_kaydi_getir(tc_no)
        if not kayit:
            bildirim.hata(self, "Kullanıcı bulunamadı.")
            return

        parcalar = kayit.split("$")
        if len(parcalar) == 4:
            algoritma, iterasyon, salt, ozet = parcalar
            detay = (f"{ad_soyad} ({tc_no})\n\n"
                     f"Algoritma:  {algoritma}\n"
                     f"Tur sayısı:  {int(iterasyon):,}\n"
                     f"Salt:  {salt}\n"
                     f"Özet:  {ozet[:32]}…\n\n"
                     f"Şifrenin kendisi hiçbir yerde saklanmıyor. Buradaki özet "
                     f"tek yönlüdür; şifreye geri çevrilemez. Şifreyi öğrenmek "
                     f"yerine yenisini belirleyebilirsiniz.")
        else:
            detay = (f"{ad_soyad} ({tc_no})\n\n"
                     f"Bu hesabın şifresi henüz hashlenmemiş görünüyor.")

        bildirim.bilgi(self, detay, baslik="Şifre Nasıl Saklanıyor?")

    def sifre_sifirla(self):
        secim = self._secili_kullanici()
        if not secim:
            return
        tc_no, ad_soyad = secim

        yeni_sifre = bildirim.girdi_iste(
            self,
            "Şifre Sıfırla",
            f"{ad_soyad} ({tc_no}) için yeni bir şifre belirleyin. "
            f"Kullanıcı bundan sonra bu şifreyle giriş yapar.",
            ipucu="En az 6 karakter",
            gizli=True)

        if yeni_sifre is None:
            return

        basarili, mesaj = database.sifre_degistir(tc_no, yeni_sifre)
        if basarili:
            bildirim.basarili(
                self, f"{ad_soyad} için yeni şifre belirlendi.",
                baslik="Şifre Güncellendi")
        else:
            bildirim.hata(self, mesaj)

    def cikis_yap(self):
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
