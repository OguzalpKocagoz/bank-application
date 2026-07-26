from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
                             QPushButton, QFrame, QTreeWidget, QTreeWidgetItem,
                             QHBoxLayout, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import database
import stil


# İşlem türü -> (etiket, bakiyeyi artırıyor mu)
ISLEM_ETIKETLERI = {
    'yatirma': ('⬆️  Para Yatırma', True),
    'cekme': ('⬇️  Para Çekme', False),
    'transfer_alma': ('⬅️  Transfer (Gelen)', True),
    'transfer_gonderme': ('➡️  Transfer (Giden)', False),
}


class IslemGecmisiFormu(QMainWindow):
    def __init__(self, kullanici_bilgileri):
        super().__init__()
        self.kullanici_bilgileri = kullanici_bilgileri
        self.setWindowTitle("📊 İşlem Geçmişi")
        self.setMinimumSize(680, 500)
        self.resize(860, 600)
        self.setStyleSheet(stil.pencere())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(18)
        central_widget.setLayout(layout)

        layout.addWidget(self._baslik_karti())
        layout.addWidget(self._liste_karti(), 1)

        self.islemleri_goster()

    def _baslik_karti(self):
        kart = QFrame()
        kart.setObjectName("baslikKarti")
        kart.setStyleSheet(stil.baslik_karti(stil.INDIGO))

        efekt = QGraphicsDropShadowEffect()
        efekt.setBlurRadius(32)
        efekt.setColor(QColor(0, 0, 0, 65))
        efekt.setOffset(0, 6)
        kart.setGraphicsEffect(efekt)

        kart_layout = QVBoxLayout()
        kart_layout.setContentsMargins(26, 22, 26, 24)
        kart_layout.setSpacing(4)
        kart.setLayout(kart_layout)

        baslik = QLabel("📊  İşlem Geçmişi")
        baslik.setStyleSheet(stil.baslik_yazisi(22))
        kart_layout.addWidget(baslik)

        self.ozet_label = QLabel()
        self.ozet_label.setStyleSheet(stil.alt_baslik())
        kart_layout.addWidget(self.ozet_label)

        return kart

    def _liste_karti(self):
        kart = QFrame()
        kart.setObjectName("kart")
        kart.setStyleSheet(stil.beyaz_kart())

        kart_layout = QVBoxLayout()
        kart_layout.setContentsMargins(20, 20, 20, 20)
        kart_layout.setSpacing(14)
        kart.setLayout(kart_layout)

        self.gecmis_tree = QTreeWidget()
        self.gecmis_tree.setHeaderLabels(
            ['Tarih', 'İşlem Türü', 'Miktar', 'Açıklama'])
        self.gecmis_tree.setAlternatingRowColors(False)
        self.gecmis_tree.setRootIsDecorated(False)
        self.gecmis_tree.setStyleSheet(stil.agac())
        kart_layout.addWidget(self.gecmis_tree)

        alt_satir = QHBoxLayout()
        alt_satir.addStretch()
        yenile_btn = QPushButton("🔄  Yenile")
        yenile_btn.setStyleSheet(stil.ikincil_buton())
        yenile_btn.setMinimumHeight(42)
        yenile_btn.clicked.connect(self.islemleri_goster)
        alt_satir.addWidget(yenile_btn)
        kart_layout.addLayout(alt_satir)

        return kart

    def islemleri_goster(self):
        self.gecmis_tree.clear()

        islemler = database.kullanici_islemleri_getir(self.kullanici_bilgileri[0])

        for islem in islemler:
            item = QTreeWidgetItem(self.gecmis_tree)

            item.setText(0, database.tarih_goster(islem[0]))

            etiket, artan = ISLEM_ETIKETLERI.get(islem[1], (islem[1], False))
            item.setText(1, etiket)

            if artan:
                item.setText(2, f"+ ₺{islem[2]:,.2f}")
                item.setForeground(2, QColor(stil.BASARI_RENGI))
            else:
                item.setText(2, f"− ₺{islem[2]:,.2f}")
                item.setForeground(2, QColor(stil.HATA_RENGI))

            item.setText(3, islem[3])

            item.setTextAlignment(2, Qt.AlignRight | Qt.AlignVCenter)

        self.ozet_label.setText(
            f"{len(islemler)} işlem listeleniyor" if islemler
            else "Henüz işlem yapılmamış")

        for i in range(4):
            self.gecmis_tree.resizeColumnToContents(i)

        if not islemler:
            bos_item = QTreeWidgetItem(self.gecmis_tree)
            bos_item.setText(1, "Henüz işlem geçmişi bulunmuyor")
            bos_item.setForeground(1, QColor(stil.SOLUK_YAZI))
