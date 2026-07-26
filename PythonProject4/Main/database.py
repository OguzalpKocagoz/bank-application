import hashlib
import os
import secrets
import sqlite3
import sys
from datetime import datetime


def _temel_dizin():
    """Veritabaninin durdugu klasor.

    .exe olarak paketlendiginde PyInstaller kodu gecici bir klasore acar;
    oradaki bir yol her calistirmada silinecegi icin veritabani exe'nin
    yanina yazilir. Normal calistirmada bu dosyanin klasoru kullanilir.
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


# Veritabanı her zaman aynı yerde durur; uygulama hangi dizinden
# çalıştırılırsa çalıştırılsın aynı banka.db kullanılır.
DB_PATH = os.path.join(_temel_dizin(), 'banka.db')

TARIH_FORMATI = '%Y-%m-%d %H:%M:%S'

_PBKDF2_ITERASYON = 200_000
_HASH_ONEKI = 'pbkdf2_sha256'


def baglan():
    """Uygulamadaki tüm sorgular için ortak bağlantı."""
    return sqlite3.connect(DB_PATH)


def simdi():
    """İşlem geçmişine yazılacak tarih (mikrosaniyesiz, tek format)."""
    return datetime.now().strftime(TARIH_FORMATI)


def tarih_ayristir(tarih_metni):
    """Veritabanındaki tarihi datetime'a çevirir.

    Eski kayıtlar mikrosaniyeli (datetime.now() doğrudan yazılmış) ya da
    CURRENT_TIMESTAMP kaynaklı olabildiği için birden fazla format denenir.
    """
    if isinstance(tarih_metni, datetime):
        return tarih_metni
    for bicim in (TARIH_FORMATI, '%Y-%m-%d %H:%M:%S.%f'):
        try:
            return datetime.strptime(tarih_metni, bicim)
        except (ValueError, TypeError):
            continue
    return None


def tarih_goster(tarih_metni):
    """İşlem tarihini arayüzde gösterilecek biçime çevirir."""
    tarih = tarih_ayristir(tarih_metni)
    return tarih.strftime('%d.%m.%Y %H:%M') if tarih else str(tarih_metni)


def sifre_hashle(sifre, salt=None):
    """Şifreyi PBKDF2-HMAC-SHA256 ile, kullanıcıya özel salt ile hashler."""
    salt = salt or secrets.token_hex(16)
    ozet = hashlib.pbkdf2_hmac(
        'sha256', sifre.encode('utf-8'), salt.encode('utf-8'), _PBKDF2_ITERASYON
    ).hex()
    return f'{_HASH_ONEKI}${_PBKDF2_ITERASYON}${salt}${ozet}'


def sifre_dogrula(sifre, kayitli_deger):
    """Girilen şifre kayıtlı hash ile eşleşiyor mu?

    Hash öneki taşımayan kayıtlar hashlemeden önce oluşturulmuş düz metin
    şifrelerdir; bunlar da karşılaştırılır ki eski hesaplar giriş yapabilsin.
    """
    if not kayitli_deger:
        return False
    if not kayitli_deger.startswith(_HASH_ONEKI + '$'):
        return secrets.compare_digest(sifre, kayitli_deger)
    try:
        _, iterasyon, salt, ozet = kayitli_deger.split('$')
        beklenen = hashlib.pbkdf2_hmac(
            'sha256', sifre.encode('utf-8'), salt.encode('utf-8'), int(iterasyon)
        ).hex()
    except (ValueError, TypeError):
        return False
    return secrets.compare_digest(beklenen, ozet)


def create_database():
    conn = baglan()
    cursor = conn.cursor()

    # Kullanıcılar tablosu
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS kullanicilar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tc_no TEXT UNIQUE,
        ad TEXT,
        soyad TEXT,
        telefon TEXT,
        sifre TEXT,
        bakiye REAL DEFAULT 0,
        hesap_turu TEXT DEFAULT 'normal'
    )
    ''')

    # İşlem geçmişi tablosu
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS islem_gecmisi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kullanici_id INTEGER,
        islem_turu TEXT,
        miktar REAL,
        aciklama TEXT,
        tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (kullanici_id) REFERENCES kullanicilar (id)
    )
    ''')

    # Admin kullanıcısını ekle (zaten varsa dokunma)
    cursor.execute('''
    INSERT OR IGNORE INTO kullanicilar (tc_no, ad, soyad, telefon, sifre, hesap_turu)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', ('11111111111', 'Admin', 'User', '5555555555',
          sifre_hashle('admin123'), 'admin'))

    conn.commit()
    conn.close()

    _duz_metin_sifreleri_hashle()


def _duz_metin_sifreleri_hashle():
    """Hashleme öncesinde açılmış hesapların şifrelerini tek seferde hashler."""
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('SELECT id, sifre FROM kullanicilar')
    eski_kayitlar = [
        (kayit_id, sifre) for kayit_id, sifre in cursor.fetchall()
        if sifre and not sifre.startswith(_HASH_ONEKI + '$')
    ]
    for kayit_id, duz_sifre in eski_kayitlar:
        cursor.execute('UPDATE kullanicilar SET sifre = ? WHERE id = ?',
                       (sifre_hashle(duz_sifre), kayit_id))
    conn.commit()
    conn.close()


def kayit_ekle(tc_no, ad, soyad, telefon, sifre):
    conn = baglan()
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO kullanicilar (tc_no, ad, soyad, telefon, sifre)
        VALUES (?, ?, ?, ?, ?)
        ''', (tc_no, ad, soyad, telefon, sifre_hashle(sifre)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def sifre_degistir(tc_no, yeni_sifre):
    """Bir hesaba yeni sifre atar. (basarili, mesaj) doner.

    Kayitli sifreler geri cevrilemez bicimde hashlendigi icin mevcut sifre
    okunamaz; admin ancak yenisini belirleyebilir.
    """
    if len(yeni_sifre) < 6:
        return False, "Şifre en az 6 karakter olmalıdır!"

    conn = baglan()
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE kullanicilar SET sifre = ? WHERE tc_no = ?',
                       (sifre_hashle(yeni_sifre), tc_no))
        if cursor.rowcount == 0:
            return False, "Kullanıcı bulunamadı!"
        conn.commit()
        return True, "Şifre güncellendi."
    except sqlite3.Error:
        conn.rollback()
        return False, "Şifre güncellenirken bir hata oluştu!"
    finally:
        conn.close()


def sifre_kaydi_getir(tc_no):
    """Veritabaninda o hesap icin ne saklandigini doner.

    Donen deger sifrenin kendisi degil, PBKDF2 ozetidir; sifreye geri
    cevrilemez. Admin panelinde 'ne saklaniyor' sorusunu yanitlamak icin var.
    """
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('SELECT sifre FROM kullanicilar WHERE tc_no = ?', (tc_no,))
    kayit = cursor.fetchone()
    conn.close()
    return kayit[0] if kayit else None


def giris_kontrol(tc_no, sifre):
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, tc_no, ad, soyad, telefon, bakiye, hesap_turu, sifre
        FROM kullanicilar
        WHERE tc_no = ?
    ''', (tc_no,))
    kayit = cursor.fetchone()
    conn.close()

    if not kayit or not sifre_dogrula(sifre, kayit[7]):
        return None
    # Şifre sütununu çağırana döndürme.
    return kayit[:7]


def kullanici_getir(tc_no):
    """Giriş sonrası bakiyeyi tazelemek için kullanıcıyı yeniden okur."""
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, tc_no, ad, soyad, telefon, bakiye, hesap_turu
        FROM kullanicilar
        WHERE tc_no = ?
    ''', (tc_no,))
    kullanici = cursor.fetchone()
    conn.close()
    return kullanici


def bakiye_getir(tc_no):
    kullanici = kullanici_getir(tc_no)
    return kullanici[5] if kullanici else None


def para_yatir(tc_no, miktar):
    """Para yatırır. (basarili, mesaj) döndürür."""
    if miktar <= 0:
        return False, "Geçerli bir miktar girin!"

    conn = baglan()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM kullanicilar WHERE tc_no = ?', (tc_no,))
        kullanici = cursor.fetchone()
        if not kullanici:
            return False, "Kullanıcı bulunamadı!"

        cursor.execute('UPDATE kullanicilar SET bakiye = bakiye + ? WHERE tc_no = ?',
                       (miktar, tc_no))
        cursor.execute('''
        INSERT INTO islem_gecmisi (kullanici_id, islem_turu, miktar, tarih, aciklama)
        VALUES (?, ?, ?, ?, ?)
        ''', (kullanici[0], 'yatirma', miktar, simdi(), 'Para yatırma işlemi'))
        conn.commit()
        return True, f"₺{miktar:.2f} yatırıldı!"
    except sqlite3.Error:
        conn.rollback()
        return False, "İşlem sırasında bir hata oluştu!"
    finally:
        conn.close()


def para_cek(tc_no, miktar):
    """Para çeker. (basarili, mesaj) döndürür."""
    if miktar <= 0:
        return False, "Geçerli bir miktar girin!"

    conn = baglan()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, bakiye FROM kullanicilar WHERE tc_no = ?', (tc_no,))
        kullanici = cursor.fetchone()
        if not kullanici:
            return False, "Kullanıcı bulunamadı!"
        if miktar > kullanici[1]:
            return False, "Yetersiz bakiye!"

        cursor.execute('UPDATE kullanicilar SET bakiye = bakiye - ? WHERE tc_no = ?',
                       (miktar, tc_no))
        cursor.execute('''
        INSERT INTO islem_gecmisi (kullanici_id, islem_turu, miktar, tarih, aciklama)
        VALUES (?, ?, ?, ?, ?)
        ''', (kullanici[0], 'cekme', miktar, simdi(), 'Para çekme işlemi'))
        conn.commit()
        return True, f"₺{miktar:.2f} çekildi!"
    except sqlite3.Error:
        conn.rollback()
        return False, "İşlem sırasında bir hata oluştu!"
    finally:
        conn.close()


def para_transfer(gonderen_tc, alici_tc, miktar):
    """İki hesap arasında para aktarır. (basarili, mesaj) döndürür.

    Bakiye düşme, bakiye ekleme ve iki geçmiş kaydı tek işlem içinde yapılır;
    ortada bir hata olursa hiçbiri kalıcı olmaz.
    """
    if miktar <= 0:
        return False, "Geçerli bir miktar girin!"
    if gonderen_tc == alici_tc:
        return False, "Kendi hesabınıza transfer yapamazsınız!"

    conn = baglan()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, bakiye FROM kullanicilar WHERE tc_no = ?', (gonderen_tc,))
        gonderen = cursor.fetchone()
        if not gonderen:
            return False, "Gönderen hesap bulunamadı!"

        cursor.execute('SELECT id FROM kullanicilar WHERE tc_no = ?', (alici_tc,))
        alici = cursor.fetchone()
        if not alici:
            return False, "Alıcı bulunamadı!"

        if miktar > gonderen[1]:
            return False, "Yetersiz bakiye!"

        zaman = simdi()
        cursor.execute('UPDATE kullanicilar SET bakiye = bakiye - ? WHERE tc_no = ?',
                       (miktar, gonderen_tc))
        cursor.execute('UPDATE kullanicilar SET bakiye = bakiye + ? WHERE tc_no = ?',
                       (miktar, alici_tc))
        cursor.execute('''
        INSERT INTO islem_gecmisi (kullanici_id, islem_turu, miktar, tarih, aciklama)
        VALUES (?, ?, ?, ?, ?)
        ''', (gonderen[0], 'transfer_gonderme', miktar, zaman,
              f'Para transferi - Alıcı TC: {alici_tc}'))
        cursor.execute('''
        INSERT INTO islem_gecmisi (kullanici_id, islem_turu, miktar, tarih, aciklama)
        VALUES (?, ?, ?, ?, ?)
        ''', (alici[0], 'transfer_alma', miktar, zaman,
              f'Para transferi - Gönderen TC: {gonderen_tc}'))
        conn.commit()
        return True, f"₺{miktar:.2f} transfer edildi!"
    except sqlite3.Error:
        conn.rollback()
        return False, "Transfer sırasında bir hata oluştu!"
    finally:
        conn.close()


def islem_gecmisi_getir(tc_no):
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT ig.islem_turu, ig.miktar, ig.tarih, ig.aciklama
    FROM islem_gecmisi ig
    JOIN kullanicilar k ON k.id = ig.kullanici_id
    WHERE k.tc_no = ?
    ORDER BY ig.tarih DESC
    ''', (tc_no,))
    islemler = cursor.fetchall()
    conn.close()
    return islemler


def kullanici_islemleri_getir(kullanici_id):
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT tarih, islem_turu, miktar, aciklama
    FROM islem_gecmisi
    WHERE kullanici_id = ?
    ORDER BY tarih DESC
    ''', (kullanici_id,))
    islemler = cursor.fetchall()
    conn.close()
    return islemler


def tum_kullanicilari_getir():
    """Admin paneli için admin dışındaki tüm kullanıcılar."""
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT tc_no, ad, soyad, telefon, bakiye
    FROM kullanicilar
    WHERE hesap_turu != 'admin'
    ORDER BY ad, soyad
    ''')
    kullanicilar = cursor.fetchall()
    conn.close()
    return kullanicilar


def tum_islemleri_getir():
    """Admin paneli için tüm kullanıcıların işlem geçmişi."""
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT
        ig.tarih,
        k.tc_no,
        k.ad || ' ' || k.soyad as ad_soyad,
        ig.islem_turu,
        ig.miktar,
        ig.aciklama
    FROM islem_gecmisi ig
    JOIN kullanicilar k ON k.id = ig.kullanici_id
    ORDER BY ig.tarih DESC
    ''')
    islemler = cursor.fetchall()
    conn.close()
    return islemler
