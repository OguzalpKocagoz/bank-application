import sqlite3
from datetime import datetime

def create_database():
    conn = sqlite3.connect('banka.db')
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
    
    # Admin kullanıcısını ekle
    try:
        cursor.execute('''
        INSERT INTO kullanicilar (tc_no, ad, soyad, telefon, sifre, hesap_turu)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', ('11111111111', 'Admin', 'User', '5555555555', 'admin123', 'admin'))
    except sqlite3.IntegrityError:
        pass  # Admin zaten varsa ekleme
    
    conn.commit()
    conn.close()

def kayit_ekle(tc_no, ad, soyad, telefon, sifre):
    conn = sqlite3.connect('banka.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO kullanicilar (tc_no, ad, soyad, telefon, sifre)
        VALUES (?, ?, ?, ?, ?)
        ''', (tc_no, ad, soyad, telefon, sifre))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def giris_kontrol(tc_no, sifre):
    conn = sqlite3.connect('banka.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, tc_no, ad, soyad, telefon, bakiye, hesap_turu 
        FROM kullanicilar 
        WHERE tc_no = ? AND sifre = ?
    ''', (tc_no, sifre))
    kullanici = cursor.fetchone()
    conn.close()
    return kullanici

def bakiye_guncelle(tc_no, miktar, islem_turu):
    conn = sqlite3.connect('banka.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, bakiye FROM kullanicilar WHERE tc_no = ?', (tc_no,))
    kullanici = cursor.fetchone()
    if not kullanici:
        conn.close()
        return False
    
    kullanici_id, mevcut_bakiye = kullanici
    yeni_bakiye = mevcut_bakiye + miktar if islem_turu == 'yatirma' else mevcut_bakiye - miktar
    
    if yeni_bakiye < 0:
        conn.close()
        return False
    
    cursor.execute('UPDATE kullanicilar SET bakiye = ? WHERE tc_no = ?', (yeni_bakiye, tc_no))
    
    # İşlem geçmişine kaydet
    aciklama = f"{'Para yatırma' if islem_turu == 'yatirma' else 'Para çekme'} işlemi"
    cursor.execute('''
    INSERT INTO islem_gecmisi (kullanici_id, islem_turu, miktar, tarih, aciklama)
    VALUES (?, ?, ?, ?, ?)
    ''', (kullanici_id, islem_turu, miktar, datetime.now(), aciklama))
    
    conn.commit()
    conn.close()
    return True

def islem_gecmisi_getir(tc_no):
    conn = sqlite3.connect('banka.db')
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