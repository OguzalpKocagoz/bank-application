# Banka Sistemi

Modern arayüzlü, SQLite veritabanı destekli basit bir banka sistemi uygulaması.

## Özellikler

- Kullanıcı kaydı ve girişi
- Admin paneli
- Para yatırma ve çekme işlemleri
- İşlem geçmişi takibi
- Modern ve kullanıcı dostu arayüz
- SQLite veritabanı desteği

## Kurulum

1. Python 3.x sürümünün yüklü olduğundan emin olun
2. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. Uygulamayı çalıştırın:
   ```bash
   python Main/main.py
   ```

## Admin Girişi

- TC No: 11111111111
- Şifre: admin123

## Kullanım

1. Yeni hesap oluşturmak için "Yeni Hesap Oluştur" butonuna tıklayın
2. TC No ve şifrenizle giriş yapın
3. Ana menüden para yatırma, çekme ve işlem geçmişi gibi işlemleri gerçekleştirin

## Güvenlik

- Şifreler veritabanında saklanır
- TC No ve email adresi benzersiz olmalıdır
- Para işlemleri veritabanında kayıt altına alınır 