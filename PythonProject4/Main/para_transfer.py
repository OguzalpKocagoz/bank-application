import bildirim
import database
import stil
from islem_ekrani import IslemEkrani


class ParaTransferFormu(IslemEkrani):
    BASLIK = "Para Transfer"
    IKON = "💸"
    RENK = stil.TEAL
    BUTON_YAZISI = "Transfer Et"
    ALANLAR = [
        ("alici", "ALICI TC NO", "Alıcının TC kimlik numarası"),
        ("miktar", "TRANSFER MİKTARI (₺)", "Örn. 100"),
    ]

    def uygula(self):
        alici_tc = self.deger("alici")
        if not alici_tc:
            bildirim.uyari(self, "Lütfen alıcının TC kimlik numarasını girin.")
            return

        try:
            miktar = float(self.deger("miktar").replace(",", "."))
        except ValueError:
            bildirim.uyari(self, "Lütfen geçerli bir miktar girin.")
            return

        basarili, mesaj = database.para_transfer(
            self.kullanici_bilgileri[1], alici_tc, miktar
        )
        if basarili:
            self.temizle()
            self.bakiye_yenile()
            bildirim.basarili(self, mesaj, baslik="Transfer Tamamlandı")
        else:
            bildirim.hata(self, mesaj)
