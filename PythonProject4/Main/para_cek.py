import bildirim
import database
import stil
from islem_ekrani import IslemEkrani


class ParaCekFormu(IslemEkrani):
    BASLIK = "Para Çek"
    IKON = "🏧"
    RENK = stil.TURUNCU
    BUTON_YAZISI = "Para Çek"
    ALANLAR = [("miktar", "ÇEKİLECEK MİKTAR (₺)", "Örn. 250")]

    def uygula(self):
        try:
            miktar = float(self.deger("miktar").replace(",", "."))
        except ValueError:
            bildirim.uyari(self, "Lütfen geçerli bir miktar girin.")
            return

        basarili, mesaj = database.para_cek(self.kullanici_bilgileri[1], miktar)
        if basarili:
            self.temizle()
            self.bakiye_yenile()
            bildirim.basarili(self, mesaj, baslik="Para Çekildi")
        else:
            bildirim.hata(self, mesaj)
