from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, 
                           QVBoxLayout, QMessageBox, QFrame, QHBoxLayout, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
import database

class KullaniciGiris(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏦 Banka Sistemi")
        self.setGeometry(100, 100, 400, 450)
        self.setMinimumSize(400, 600)
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
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Logo ve başlık çerçevesi
        logo_frame = QFrame()
        logo_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4361ee, stop:1 #3a0ca3);
                border-radius: 20px;
                margin: 20px;
                padding: 30px;
            }
        """)
        logo_layout = QVBoxLayout()
        logo_frame.setLayout(logo_layout)
        
        # Logo
        logo_label = QLabel("🏦")
        logo_label.setStyleSheet("""
            font-size: 64px;
            color: white;
        """)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_label)
        
        # Başlık
        baslik = QLabel("Banka Sistemine\nHoş Geldiniz")
        baslik.setStyleSheet("""
            color: white;
            font-size: 28px;
            font-weight: bold;
            margin: 10px;
        """)
        baslik.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(baslik)
        
        # Logo frame gölge efekti
        logo_shadow = QGraphicsDropShadowEffect()
        logo_shadow.setBlurRadius(30)
        logo_shadow.setColor(QColor(0, 0, 0, 80))
        logo_shadow.setOffset(0, 5)
        logo_frame.setGraphicsEffect(logo_shadow)
        
        layout.addWidget(logo_frame)
        
        # Giriş formu çerçevesi
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 20px;
                margin: 20px;
                padding: 30px;
            }
        """)
        form_layout = QVBoxLayout()
        form_frame.setLayout(form_layout)
        
        # Form frame gölge efekti
        form_shadow = QGraphicsDropShadowEffect()
        form_shadow.setBlurRadius(30)
        form_shadow.setColor(QColor(0, 0, 0, 50))
        form_shadow.setOffset(0, 5)
        form_frame.setGraphicsEffect(form_shadow)
        
        # TC No
        tc_label = QLabel("👤 TC Kimlik No")
        tc_label.setStyleSheet("""
            color: #495057;
            font-size: 14px;
            font-weight: bold;
            margin-top: 5px;
        """)
        form_layout.addWidget(tc_label)
        
        self.tc_entry = QLineEdit()
        self.tc_entry.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                font-size: 13px;
                margin-bottom: 10px;
                min-height: 25px;
            }
            QLineEdit:focus {
                border: 2px solid #4361ee;
            }
        """)
        self.tc_entry.setPlaceholderText("TC Kimlik numaranızı giriniz")
        form_layout.addWidget(self.tc_entry)
        
        # Şifre
        sifre_label = QLabel("🔒 Şifre")
        sifre_label.setStyleSheet("""
            color: #495057;
            font-size: 14px;
            font-weight: bold;
            margin-top: 5px;
        """)
        form_layout.addWidget(sifre_label)
        
        self.sifre_entry = QLineEdit()
        self.sifre_entry.setEchoMode(QLineEdit.Password)
        self.sifre_entry.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                font-size: 13px;
                margin-bottom: 15px;
                min-height: 25px;
            }
            QLineEdit:focus {
                border: 2px solid #4361ee;
            }
        """)
        self.sifre_entry.setPlaceholderText("Şifrenizi giriniz")
        form_layout.addWidget(self.sifre_entry)
        
        # Butonlar için container
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(5)
        
        # Giriş butonu
        self.giris_btn = QPushButton("🚀 Giriş Yap")
        self.giris_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4361ee, stop:1 #3a0ca3);
                color: white;
                padding: 5px;
                border: none;
                border-radius: 5px;
                font-size: 13px;
                font-weight: bold;
                min-height: 25px;
                margin: 2px 0;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3a0ca3, stop:1 #4361ee);
            }
            QPushButton:pressed {
                background: #3a0ca3;
            }
        """)
        self.giris_btn.clicked.connect(self.giris_yap)
        buttons_layout.addWidget(self.giris_btn)
        
        # Kayıt ol butonu
        self.kayit_btn = QPushButton("✨ Yeni Hesap Oluştur")
        self.kayit_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #059669);
                color: white;
                padding: 5px;
                border: none;
                border-radius: 5px;
                font-size: 13px;
                font-weight: bold;
                min-height: 25px;
                margin: 2px 0;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #059669, stop:1 #10b981);
            }
            QPushButton:pressed {
                background: #059669;
            }
        """)
        self.kayit_btn.clicked.connect(self.kayit_sayfasina_git)
        buttons_layout.addWidget(self.kayit_btn)
        
        # Admin girişi butonu
        self.admin_btn = QPushButton("👑 Admin Girişi")
        self.admin_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6f42c1, stop:1 #563d7c);
                color: white;
                padding: 5px;
                border: none;
                border-radius: 5px;
                font-size: 13px;
                font-weight: bold;
                min-height: 25px;
                margin: 2px 0;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #563d7c, stop:1 #6f42c1);
            }
            QPushButton:pressed {
                background: #563d7c;
            }
        """)
        self.admin_btn.clicked.connect(self.admin_giris_sayfasina_git)
        buttons_layout.addWidget(self.admin_btn)
        
        form_layout.addLayout(buttons_layout)
        layout.addWidget(form_frame)
        
        # Veritabanını oluştur
        database.create_database()
    
    def giris_yap(self):
        tc_no = self.tc_entry.text().strip()
        sifre = self.sifre_entry.text().strip()
        
        if not tc_no or not sifre:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
            return
        
        kullanici = database.giris_kontrol(tc_no, sifre)
        if kullanici:
            if kullanici[6] == 'admin':  # hesap_turu kontrolü
                from admin_panel import AdminPanel
                self.admin_panel = AdminPanel(kullanici)
                self.admin_panel.show()
            else:
                from ana_menu import AnaMenu
                self.ana_menu = AnaMenu(kullanici)
                self.ana_menu.show()
            self.close()
        else:
            QMessageBox.warning(self, "Hata", "TC No veya şifre hatalı!")
    
    def kayit_sayfasina_git(self):
        from hesap_olustur import HesapOlusturFormu
        self.hesap_olustur = HesapOlusturFormu()
        self.hesap_olustur.show()
        self.close()
    
    def admin_giris_sayfasina_git(self):
        from admin_giris import AdminGirisFormu
        self.admin_giris = AdminGirisFormu()
        self.admin_giris.show()
        self.close()