import bildirim
import database
import stil
from islem_ekrani import IslemEkrani


class ParaYatirFormu(IslemEkrani):
    BASLIK = "Para Yatır"
    IKON = "💰"
    RENK = stil.YESIL
    BUTON_YAZISI = "Para Yatır"
    ALANLAR = [("miktar", "YATIRILACAK MİKTAR (₺)", "Örn. 500")]

    def uygula(self):
        try:
            miktar = float(self.deger("miktar").replace(",", "."))
        except ValueError:
            bildirim.uyari(self, "Lütfen geçerli bir miktar girin.")
            return

        basarili, mesaj = database.para_yatir(self.kullanici_bilgileri[1], miktar)
        if basarili:
            self.temizle()
            self.bakiye_yenile()
            bildirim.basarili(self, mesaj, baslik="Para Yatırıldı")
        else:
            bildirim.hata(self, mesaj)
