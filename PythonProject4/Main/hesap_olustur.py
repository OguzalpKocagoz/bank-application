from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame, 
                             QHBoxLayout, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import re
import database

class HesapOlusturFormu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("✨ Yeni Hesap Oluştur")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(600, 400)
        self.setStyleSheet("""
            QMainWindow {
                background: #f8f9fa;
            }
            QLabel {
                font-size: 14px;
                margin: 5px;
            }
            QPushButton {
                font-size: 14px;
                padding: 10px;
                min-height: 35px;
                margin: 5px;
            }
            QLineEdit {
                font-size: 14px;
                padding: 10px;
                min-height: 35px;
                margin: 5px;
            }
            QFrame {
                margin: 5px;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        central_widget.setLayout(layout)
        
        baslik_frame = QFrame()
        baslik_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #059669);
                border-radius: 10px;
                margin: 10px;
                padding: 20px;
            }
        """)
        baslik_layout = QVBoxLayout()
        baslik_layout.setSpacing(10)
        baslik_layout.setContentsMargins(10, 10, 10, 10)
        baslik_frame.setLayout(baslik_layout)
        
        icon_label = QLabel("✨")
        icon_label.setStyleSheet("""
            font-size: 32px;
            color: white;
            margin: 5px;
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        baslik_layout.addWidget(icon_label)
        
        baslik = QLabel("Yeni Hesap Oluştur")
        baslik.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
            margin: 5px;
        """)
        baslik.setAlignment(Qt.AlignCenter)
        baslik_layout.addWidget(baslik)
        
        layout.addWidget(baslik_frame)
        
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 10px;
                margin: 10px;
                padding: 20px;
            }
        """)
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_frame.setLayout(form_layout)
        
        self.form_alanlari = {}
        self.form_alani_ekle(form_layout, "👤 TC Kimlik No", "tc_entry", "11 haneli TC kimlik numaranız")
        self.form_alani_ekle(form_layout, "📝 Ad", "ad_entry", "Adınız")
        self.form_alani_ekle(form_layout, "📝 Soyad", "soyad_entry", "Soyadınız")
        self.form_alani_ekle(form_layout, "📱 Telefon", "telefon_entry", "10 haneli telefon numaranız")
        self.form_alani_ekle(form_layout, "🔒 Şifre", "sifre_entry", "En az 6 karakterli şifreniz", True)
        self.form_alani_ekle(form_layout, "🔒 Şifre Tekrar", "sifre_tekrar_entry", "Şifrenizi tekrar girin", True)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        buttons_layout.setContentsMargins(20, 20, 20, 20)
        
        self.kayit_btn = QPushButton("✨ Hesap Oluştur")
        self.kayit_btn.setFixedWidth(200)
        self.kayit_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #059669);
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-height: 35px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #059669, stop:1 #10b981);
            }
            QPushButton:pressed {
                background: #059669;
            }
        """)
        self.kayit_btn.clicked.connect(self.hesap_olustur)
        buttons_layout.addWidget(self.kayit_btn)
        
        self.geri_btn = QPushButton("🔙 Giriş Sayfasına Dön")
        self.geri_btn.setFixedWidth(200)
        self.geri_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4361ee, stop:1 #3a0ca3);
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-height: 35px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3a0ca3, stop:1 #4361ee);
            }
            QPushButton:pressed {
                background: #3a0ca3;
            }
        """)
        self.geri_btn.clicked.connect(self.giris_sayfasina_don)
        buttons_layout.addWidget(self.geri_btn)
        
        form_layout.addLayout(buttons_layout)
        layout.addWidget(form_frame)
    
    def form_alani_ekle(self, layout, etiket_text, entry_name, placeholder_text="", sifre_mi=False):
        etiket = QLabel(etiket_text)
        etiket.setStyleSheet("""
            color: #495057;
            font-size: 14px;
            font-weight: bold;
            margin: 5px;
        """)
        layout.addWidget(etiket)
        
        entry = QLineEdit()
        if sifre_mi:
            entry.setEchoMode(QLineEdit.Password)
        entry.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #e9ecef;
                border-radius: 5px;
                font-size: 14px;
                min-height: 35px;
                margin: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #10b981;
            }
        """)
        entry.setPlaceholderText(placeholder_text)
        entry.setFixedWidth(300)
        layout.addWidget(entry, alignment=Qt.AlignCenter)
        self.form_alanlari[entry_name] = entry
    
    def hesap_olustur(self):
        # Form verilerini al
        tc_no = self.form_alanlari["tc_entry"].text().strip()
        ad = self.form_alanlari["ad_entry"].text().strip()
        soyad = self.form_alanlari["soyad_entry"].text().strip()
        telefon = self.form_alanlari["telefon_entry"].text().strip()
        sifre = self.form_alanlari["sifre_entry"].text().strip()
        sifre_tekrar = self.form_alanlari["sifre_tekrar_entry"].text().strip()
        
        # Boş alan kontrolü
        if not all([tc_no, ad, soyad, telefon, sifre, sifre_tekrar]):
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
            return
        
        # TC No kontrolü
        if not tc_no.isdigit() or len(tc_no) != 11:
            QMessageBox.warning(self, "Hata", "TC Kimlik No 11 haneli sayı olmalıdır!")
            return
        
        # Telefon format kontrolü
        telefon = telefon.replace(" ", "")
        if not telefon.isdigit() or len(telefon) != 10:
            QMessageBox.warning(self, "Hata", "Telefon numarası 10 haneli olmalıdır!")
            return
        
        # Şifre kontrolü
        if sifre != sifre_tekrar:
            QMessageBox.warning(self, "Hata", "Şifreler eşleşmiyor!")
            return
        
        if len(sifre) < 6:
            QMessageBox.warning(self, "Hata", "Şifre en az 6 karakter olmalıdır!")
            return
        
        # Veritabanına kaydet
        if database.kayit_ekle(tc_no, ad, soyad, telefon, sifre):
            QMessageBox.information(self, "Başarılı", "Hesabınız başarıyla oluşturuldu!")
            self.giris_sayfasina_don()
        else:
            QMessageBox.warning(self, "Hata", "Bu TC No zaten kayıtlı!")
    
    def giris_sayfasina_don(self):
        from kullanici_giris import KullaniciGiris
        self.close()
        self.giris = KullaniciGiris()
        self.giris.show()