# Banka Sistemi

Modern arayüzlü, SQLite veritabanı destekli basit bir banka sistemi uygulaması.

## Özellikler

- Kullanıcı kaydı ve girişi
- Admin paneli: kullanıcı listesi, işlem geçmişi, özet kutuları ve şifre sıfırlama
- Para yatırma, çekme ve hesaplar arası transfer işlemleri
- İşlem geçmişi takibi
- Modern ve kullanıcı dostu arayüz
- SQLite veritabanı desteği

## Çalıştırma

Üç yol var:

**1. Masaüstü kısayolu / .exe (en kolay)**

`dist/Banka Sistemi.exe` dosyasına çift tıklayın. Python kurulu olmasına gerek
yoktur, tek dosyadır; başka bilgisayara kopyalayarak da çalıştırabilirsiniz.

**2. Kaynak koddan, çift tıklayarak**

`calistir.bat` dosyasına çift tıklayın.

**3. Kaynak koddan, komut satırından**

1. Python 3.x sürümünün yüklü olduğundan emin olun
2. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. Uygulamayı çalıştırın:
   ```bash
   python Main/main.py
   ```

## .exe Derleme

`derle.bat` dosyasına çift tıklamanız yeterli (PyInstaller gerekir:
`pip install pyinstaller`). Sonuç `dist/Banka Sistemi.exe` olarak oluşur.

## Admin Girişi

- TC No: 11111111111
- Şifre: admin123

## Kullanım

1. Yeni hesap oluşturmak için "Yeni Hesap Oluştur" butonuna tıklayın
2. TC No ve şifrenizle giriş yapın
3. Ana menüden para yatırma, çekme ve işlem geçmişi gibi işlemleri gerçekleştirin

## Güvenlik

- Şifreler düz metin olarak değil, kullanıcıya özel salt ile PBKDF2-HMAC-SHA256
  kullanılarak hashlenmiş biçimde saklanır
- Hashleme öncesinde oluşturulmuş hesapların şifreleri uygulama ilk açıldığında
  otomatik olarak hashlenir; mevcut kullanıcılar aynı şifreyle giriş yapmaya devam eder
- Şifreler geri çevrilemez biçimde saklandığı için admin paneli dahil hiçbir
  ekran mevcut şifreyi gösteremez; admin ancak yeni bir şifre belirleyebilir
  ("Şifre Sıfırla"). "Şifre Bilgisi" düğmesi veritabanında gerçekte ne
  saklandığını (algoritma, tur sayısı, salt, özet) gösterir.
- TC No benzersiz olmalıdır
- Para işlemleri veritabanında kayıt altına alınır; transferde bakiye düşme,
  bakiye ekleme ve geçmiş kayıtları tek bir işlem (transaction) içinde yapılır

## Veritabanı

`banka.db` her zaman uygulamanın yanında tutulur, hangi dizinden çalıştırılırsa
çalıştırılsın aynı veritabanı kullanılır:

| Çalıştırma biçimi | Veritabanının yeri |
|---|---|
| Kaynak koddan (`main.py`, `calistir.bat`) | `Main/banka.db` |
| `.exe` ile | exe'nin yanındaki `banka.db` (`dist/banka.db`) |

Bu ikisi **ayrı** veritabanlarıdır. `.exe` sürümüne mevcut kayıtları taşımak
için `Main/banka.db` dosyasını `dist/` klasörüne kopyalayın.
