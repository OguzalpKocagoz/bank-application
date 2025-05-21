from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame,
                             QTreeWidget, QTreeWidgetItem, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import sqlite3
from datetime import datetime
import database

class AdminGirisFormu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("👑 Admin Girişi")
        self.setGeometry(100, 100, 400, 500)
        self.setMinimumSize(400, 500)
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
        
        # Başlık çerçevesi
        baslik_frame = QFrame()
        baslik_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6f42c1, stop:1 #563d7c);
                border-radius: 10px;
                margin: 10px;
                padding: 20px;
            }
        """)
        baslik_layout = QVBoxLayout()
        baslik_layout.setSpacing(10)
        baslik_layout.setContentsMargins(10, 10, 10, 10)
        baslik_frame.setLayout(baslik_layout)
        
        # Admin ikonu
        icon_label = QLabel("👑")
        icon_label.setStyleSheet("""
            font-size: 48px;
            color: white;
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        baslik_layout.addWidget(icon_label)
        
        # Başlık
        baslik = QLabel("Admin Girişi")
        baslik.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
            margin: 10px;
        """)
        baslik.setAlignment(Qt.AlignCenter)
        baslik_layout.addWidget(baslik)
        
        layout.addWidget(baslik_frame)
        
        # Giriş formu çerçevesi
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
        
        # Kullanıcı adı
        kullanici_label = QLabel("👤 Kullanıcı Adı")
        kullanici_label.setStyleSheet("""
            color: #495057;
            font-size: 14px;
            font-weight: bold;
            margin-top: 10px;
        """)
        form_layout.addWidget(kullanici_label)
        
        self.kullanici_entry = QLineEdit()
        self.kullanici_entry.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #e9ecef;
                border-radius: 5px;
                font-size: 14px;
                margin-bottom: 15px;
            }
            QLineEdit:focus {
                border: 2px solid #6f42c1;
            }
        """)
        self.kullanici_entry.setPlaceholderText("Admin kullanıcı adınızı giriniz")
        form_layout.addWidget(self.kullanici_entry)
        
        # Şifre
        sifre_label = QLabel("🔒 Şifre")
        sifre_label.setStyleSheet("""
            color: #495057;
            font-size: 14px;
            font-weight: bold;
            margin-top: 10px;
        """)
        form_layout.addWidget(sifre_label)
        
        self.sifre_entry = QLineEdit()
        self.sifre_entry.setEchoMode(QLineEdit.Password)
        self.sifre_entry.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #e9ecef;
                border-radius: 5px;
                font-size: 14px;
                margin-bottom: 20px;
            }
            QLineEdit:focus {
                border: 2px solid #6f42c1;
            }
        """)
        self.sifre_entry.setPlaceholderText("Admin şifrenizi giriniz")
        form_layout.addWidget(self.sifre_entry)
        
        # Giriş butonu
        self.giris_btn = QPushButton("🚀 Giriş Yap")
        self.giris_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6f42c1, stop:1 #563d7c);
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-height: 40px;
                margin: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #563d7c, stop:1 #6f42c1);
            }
            QPushButton:pressed {
                background: #563d7c;
            }
        """)
        self.giris_btn.clicked.connect(self.admin_giris)
        form_layout.addWidget(self.giris_btn)
        
        # Geri dön butonu
        self.geri_btn = QPushButton("⬅️ Geri Dön")
        self.geri_btn.setStyleSheet("""
            QPushButton {
                background: #6c757d;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-height: 40px;
                margin: 5px;
            }
            QPushButton:hover {
                background: #5a6268;
            }
            QPushButton:pressed {
                background: #545b62;
            }
        """)
        self.geri_btn.clicked.connect(self.geri_don)
        form_layout.addWidget(self.geri_btn)
        
        layout.addWidget(form_frame)
    
    def admin_giris(self):
        kullanici = self.kullanici_entry.text().strip()
        sifre = self.sifre_entry.text().strip()
        
        if not kullanici or not sifre:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
            return
        
        kullanici = database.giris_kontrol(kullanici, sifre)
        if kullanici and kullanici[6] == 'admin':
            from admin_panel import AdminPanel
            self.admin_panel = AdminPanel(kullanici)
            self.admin_panel.show()
            self.close()
        else:
            QMessageBox.warning(self, "Hata", "Geçersiz kullanıcı adı veya şifre!")
    
    def geri_don(self):
        from kullanici_giris import KullaniciGiris
        self.giris = KullaniciGiris()
        self.giris.show()
        self.close()

class AdminPanelFormu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("👑 Admin Paneli")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(800, 600)
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
            QFrame {
                margin: 5px;
            }
            QTreeWidget {
                font-size: 14px;
                margin: 5px;
            }
            QTreeWidget::item {
                height: 35px;
                margin: 5px;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        central_widget.setLayout(layout)
        
        # Başlık çerçevesi
        baslik_frame = QFrame()
        baslik_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6f42c1, stop:1 #563d7c);
                border-radius: 10px;
                margin: 10px;
                padding: 20px;
            }
        """)
        baslik_layout = QVBoxLayout()
        baslik_layout.setSpacing(10)
        baslik_layout.setContentsMargins(10, 10, 10, 10)
        baslik_frame.setLayout(baslik_layout)
        
        # Admin ikonu
        icon_label = QLabel("👑")
        icon_label.setStyleSheet("""
            font-size: 48px;
            color: white;
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        baslik_layout.addWidget(icon_label)
        
        # Başlık
        baslik = QLabel("Admin Paneli")
        baslik.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
            margin: 10px;
        """)
        baslik.setAlignment(Qt.AlignCenter)
        baslik_layout.addWidget(baslik)
        
        layout.addWidget(baslik_frame)
        
        # Kullanıcılar tablosu
        self.kullanicilar_tree = QTreeWidget()
        self.kullanicilar_tree.setHeaderLabels(['👤 TC No', '👤 Ad', '👤 Soyad', '📱 Telefon', '💰 Bakiye'])
        self.kullanicilar_tree.setAlternatingRowColors(True)
        self.kullanicilar_tree.setStyleSheet("""
            QTreeWidget {
                background-color: white;
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                margin: 5px;
            }
            QTreeWidget::item {
                height: 35px;
                border-bottom: 1px solid #f0f0f0;
                margin: 5px;
            }
            QTreeWidget::item:selected {
                background: #e7f5ff;
                color: #1a73e8;
                border-radius: 5px;
            }
            QTreeWidget::item:hover {
                background: #f8f9fa;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 14px;
                color: #495057;
            }
            QTreeWidget::item:alternate {
                background-color: #f8f9fa;
            }
        """)
        
        layout.addWidget(self.kullanicilar_tree)
        
        # Alt panel
        alt_panel = QFrame()
        alt_panel.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 10px;
                margin: 10px;
                padding: 20px;
            }
        """)
        alt_layout = QHBoxLayout()
        alt_layout.setSpacing(10)
        alt_layout.setContentsMargins(10, 10, 10, 10)
        alt_panel.setLayout(alt_layout)
        
        # Yenile butonu
        yenile_btn = QPushButton("🔄 Kullanıcıları Yenile")
        yenile_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6f42c1, stop:1 #563d7c);
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-height: 35px;
                margin: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #563d7c, stop:1 #6f42c1);
            }
            QPushButton:pressed {
                background: #563d7c;
            }
        """)
        yenile_btn.clicked.connect(self.kullanicilari_goster)
        
        # Geri dön butonu
        geri_btn = QPushButton("⬅️ Geri Dön")
        geri_btn.setStyleSheet("""
            QPushButton {
                background: #6c757d;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-height: 35px;
                margin: 5px;
            }
            QPushButton:hover {
                background: #5a6268;
            }
            QPushButton:pressed {
                background: #545b62;
            }
        """)
        geri_btn.clicked.connect(self.geri_don)
        
        alt_layout.addStretch()
        alt_layout.addWidget(yenile_btn)
        alt_layout.addWidget(geri_btn)
        alt_layout.addStretch()
        
        layout.addWidget(alt_panel)
        
        self.kullanicilari_goster()
    
    def kullanicilari_goster(self):
        self.kullanicilar_tree.clear()
        
        conn = sqlite3.connect('banka.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT tc_no, ad, soyad, telefon, bakiye
        FROM kullanicilar
        WHERE hesap_turu != 'admin'
        ORDER BY id DESC
        ''')
        
        for kullanici in cursor.fetchall():
            item = QTreeWidgetItem(self.kullanicilar_tree)
            
            item.setText(0, kullanici[0])
            item.setText(1, kullanici[1])
            item.setText(2, kullanici[2])
            item.setText(3, kullanici[3])
            item.setText(4, f"₺{kullanici[4]:.2f}")
            
            for i in range(5):
                item.setTextAlignment(i, Qt.AlignCenter)
        
        conn.close()
        
        for i in range(5):
            self.kullanicilar_tree.resizeColumnToContents(i)
        
        if self.kullanicilar_tree.topLevelItemCount() == 0:
            bos_item = QTreeWidgetItem(self.kullanicilar_tree)
            bos_item.setText(0, "")
            bos_item.setText(1, "Henüz kullanıcı bulunmuyor")
            bos_item.setText(2, "")
            bos_item.setText(3, "")
            bos_item.setText(4, "")
            for i in range(5):
                bos_item.setTextAlignment(i, Qt.AlignCenter)
            bos_item.setForeground(1, QColor('#6c757d'))
    
    def geri_don(self):
        from kullanici_giris import KullaniciGiris
        self.giris = KullaniciGiris()
        self.giris.show()
        self.close() 