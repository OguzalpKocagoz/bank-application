from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, 
                             QTabWidget, QTreeWidget, QTreeWidgetItem, QPushButton,
                             QFrame, QHBoxLayout, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from datetime import datetime
import sqlite3

class AdminPanel(QMainWindow):
    def __init__(self, admin_bilgileri):
        super().__init__()
        self.admin_bilgileri = admin_bilgileri
        self.setWindowTitle("👑 Admin Paneli")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background: #f8f9fa;
            }
        """)
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Başlık çerçevesi
        baslik_frame = QFrame()
        baslik_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4361ee, stop:1 #3a0ca3);
                border-radius: 20px;
                margin: 20px;
                padding: 30px;
            }
        """)
        baslik_layout = QVBoxLayout()
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
        baslik = QLabel(f"Admin Paneli - {admin_bilgileri[2]} {admin_bilgileri[3]}")
        baslik.setStyleSheet("""
            color: white;
            font-size: 28px;
            font-weight: bold;
            margin: 10px;
        """)
        baslik.setAlignment(Qt.AlignCenter)
        baslik_layout.addWidget(baslik)
        
        # Başlık frame gölge efekti
        baslik_shadow = QGraphicsDropShadowEffect()
        baslik_shadow.setBlurRadius(30)
        baslik_shadow.setColor(QColor(0, 0, 0, 80))
        baslik_shadow.setOffset(0, 5)
        baslik_frame.setGraphicsEffect(baslik_shadow)
        
        layout.addWidget(baslik_frame)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: white;
                border-radius: 15px;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f8f9fa, stop:1 #e9ecef);
                color: #495057;
                min-width: 150px;
                max-width: 200px;
                min-height: 50px;
                padding: 8px 15px;
                margin: 8px 4px;
                border-radius: 25px;
                font-size: 15px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4361ee, stop:1 #3a0ca3);
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e9ecef, stop:1 #dee2e6);
            }
        """)
        
        # Tab widget gölge efekti
        tab_shadow = QGraphicsDropShadowEffect()
        tab_shadow.setBlurRadius(30)
        tab_shadow.setColor(QColor(0, 0, 0, 50))
        tab_shadow.setOffset(0, 5)
        self.tab_widget.setGraphicsEffect(tab_shadow)
        
        layout.addWidget(self.tab_widget)
        
        # Kullanıcılar sekmesi
        self.kullanicilar_tab = QWidget()
        self.tab_widget.addTab(self.kullanicilar_tab, "👥 Kullanıcılar")
        self.kullanicilar_tab_olustur()
        
        # İşlem Geçmişi sekmesi
        self.islemler_tab = QWidget()
        self.tab_widget.addTab(self.islemler_tab, "📊 İşlem Geçmişi")
        self.islemler_tab_olustur()
        
        # Alt panel
        alt_panel = QFrame()
        alt_panel.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
                margin: 20px;
                padding: 15px;
            }
        """)
        alt_layout = QHBoxLayout()
        alt_panel.setLayout(alt_layout)
        
        # Alt panel gölge efekti
        alt_shadow = QGraphicsDropShadowEffect()
        alt_shadow.setBlurRadius(20)
        alt_shadow.setColor(QColor(0, 0, 0, 30))
        alt_shadow.setOffset(0, 3)
        alt_panel.setGraphicsEffect(alt_shadow)
        
        # Çıkış butonu
        self.cikis_btn = QPushButton("🚪 Çıkış Yap")
        self.cikis_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #dc3545, stop:1 #c82333);
                color: white;
                padding: 15px 40px;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #c82333, stop:1 #dc3545);
            }
            QPushButton:pressed {
                background: #bd2130;
            }
        """)
        self.cikis_btn.clicked.connect(self.cikis_yap)
        
        alt_layout.addStretch()
        alt_layout.addWidget(self.cikis_btn)
        alt_layout.addStretch()
        
        layout.addWidget(alt_panel)
    
    def kullanicilar_tab_olustur(self):
        layout = QVBoxLayout()
        self.kullanicilar_tab.setLayout(layout)
        
        # TreeWidget
        self.kullanici_tree = QTreeWidget()
        self.kullanici_tree.setHeaderLabels(['👤 TC No', '📝 Ad', '📝 Soyad', '📧 Email', '📱 Telefon', '💰 Bakiye'])
        self.kullanici_tree.setAlternatingRowColors(True)
        self.kullanici_tree.setStyleSheet("""
            QTreeWidget {
                background-color: white;
                border: none;
                border-radius: 15px;
                padding: 15px;
                font-size: 14px;
                margin: 10px;
            }
            QTreeWidget::item {
                height: 40px;
                border-bottom: 1px solid #f0f0f0;
            }
            QTreeWidget::item:selected {
                background: #e7f5ff;
                color: #1a73e8;
                border-radius: 8px;
            }
            QTreeWidget::item:hover {
                background: #f8f9fa;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 14px;
                color: #495057;
            }
            QTreeWidget::item:alternate {
                background-color: #f8f9fa;
            }
        """)
        
        # TreeWidget gölge efekti
        tree_shadow = QGraphicsDropShadowEffect()
        tree_shadow.setBlurRadius(20)
        tree_shadow.setColor(QColor(0, 0, 0, 30))
        tree_shadow.setOffset(0, 3)
        self.kullanici_tree.setGraphicsEffect(tree_shadow)
        
        layout.addWidget(self.kullanici_tree)
        
        # Alt panel
        alt_panel = QFrame()
        alt_panel.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
                margin: 10px;
                padding: 15px;
            }
        """)
        alt_layout = QHBoxLayout()
        alt_panel.setLayout(alt_layout)
        
        # Yenile butonu
        yenile_btn = QPushButton("🔄 Listeyi Yenile")
        yenile_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4361ee, stop:1 #3a0ca3);
                color: white;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3a0ca3, stop:1 #4361ee);
            }
            QPushButton:pressed {
                background: #3a0ca3;
            }
        """)
        yenile_btn.clicked.connect(self.kullanicilari_goster)
        
        alt_layout.addStretch()
        alt_layout.addWidget(yenile_btn)
        alt_layout.addStretch()
        
        layout.addWidget(alt_panel)
        
        # Kullanıcıları listele
        self.kullanicilari_goster()
    
    def islemler_tab_olustur(self):
        layout = QVBoxLayout()
        self.islemler_tab.setLayout(layout)
        
        # TreeWidget
        self.islem_tree = QTreeWidget()
        self.islem_tree.setHeaderLabels(['📅 Tarih', '👤 TC No', '📝 Ad Soyad', '💫 İşlem Türü', '💰 Miktar', '📝 Açıklama'])
        self.islem_tree.setAlternatingRowColors(True)
        self.islem_tree.setStyleSheet("""
            QTreeWidget {
                background-color: white;
                border: none;
                border-radius: 15px;
                padding: 15px;
                font-size: 14px;
                margin: 10px;
            }
            QTreeWidget::item {
                height: 40px;
                border-bottom: 1px solid #f0f0f0;
            }
            QTreeWidget::item:selected {
                background: #e7f5ff;
                color: #1a73e8;
                border-radius: 8px;
            }
            QTreeWidget::item:hover {
                background: #f8f9fa;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 14px;
                color: #495057;
            }
            QTreeWidget::item:alternate {
                background-color: #f8f9fa;
            }
        """)
        
        # TreeWidget gölge efekti
        tree_shadow = QGraphicsDropShadowEffect()
        tree_shadow.setBlurRadius(20)
        tree_shadow.setColor(QColor(0, 0, 0, 30))
        tree_shadow.setOffset(0, 3)
        self.islem_tree.setGraphicsEffect(tree_shadow)
        
        layout.addWidget(self.islem_tree)
        
        # Alt panel
        alt_panel = QFrame()
        alt_panel.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
                margin: 10px;
                padding: 15px;
            }
        """)
        alt_layout = QHBoxLayout()
        alt_panel.setLayout(alt_layout)
        
        # Yenile butonu
        yenile_btn = QPushButton("🔄 Listeyi Yenile")
        yenile_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4361ee, stop:1 #3a0ca3);
                color: white;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3a0ca3, stop:1 #4361ee);
            }
            QPushButton:pressed {
                background: #3a0ca3;
            }
        """)
        yenile_btn.clicked.connect(self.islemleri_goster)
        
        alt_layout.addStretch()
        alt_layout.addWidget(yenile_btn)
        alt_layout.addStretch()
        
        layout.addWidget(alt_panel)
        
        # İşlemleri listele
        self.islemleri_goster()
    
    def kullanicilari_goster(self):
        # Mevcut listeyi temizle
        self.kullanici_tree.clear()
        
        # Veritabanından kullanıcıları çek
        conn = sqlite3.connect('banka.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT tc_no, ad, soyad, email, telefon, bakiye 
        FROM kullanicilar 
        WHERE hesap_turu != 'admin'
        ORDER BY ad, soyad
        ''')
        
        for kullanici in cursor.fetchall():
            item = QTreeWidgetItem(self.kullanici_tree)
            for i in range(6):
                item.setTextAlignment(i, Qt.AlignCenter)
            
            item.setText(0, kullanici[0])  # TC No
            item.setText(1, kullanici[1])  # Ad
            item.setText(2, kullanici[2])  # Soyad
            item.setText(3, kullanici[3])  # Email
            item.setText(4, kullanici[4])  # Telefon
            item.setText(5, f"₺{kullanici[5]:.2f}")  # Bakiye
            
            # Bakiye rengini ayarla
            if kullanici[5] > 0:
                item.setForeground(5, QColor('#28a745'))  # Yeşil
            else:
                item.setForeground(5, QColor('#dc3545'))  # Kırmızı
        
        conn.close()
        
        # Sütun genişliklerini otomatik ayarla
        for i in range(6):
            self.kullanici_tree.resizeColumnToContents(i)
    
    def islemleri_goster(self):
        # Mevcut listeyi temizle
        self.islem_tree.clear()
        
        # Veritabanından işlemleri çek
        conn = sqlite3.connect('banka.db')
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
        
        for islem in cursor.fetchall():
            item = QTreeWidgetItem(self.islem_tree)
            for i in range(6):
                item.setTextAlignment(i, Qt.AlignCenter)
            
            # Tarih formatını düzenle
            tarih = datetime.strptime(islem[0], '%Y-%m-%d %H:%M:%S.%f')
            formatli_tarih = tarih.strftime('%d.%m.%Y %H:%M')
            item.setText(0, formatli_tarih)
            
            item.setText(1, islem[1])  # TC No
            item.setText(2, islem[2])  # Ad Soyad
            
            # İşlem türüne göre emoji ve stil
            if islem[3] == 'yatirma':
                item.setText(3, '⬆️ Para Yatırma')
                item.setText(4, f"+₺{islem[4]:.2f}")
                item.setForeground(4, QColor('#28a745'))  # Yeşil
            else:
                item.setText(3, '⬇️ Para Çekme')
                item.setText(4, f"-₺{islem[4]:.2f}")
                item.setForeground(4, QColor('#dc3545'))  # Kırmızı
            
            item.setText(5, islem[5])  # Açıklama
        
        conn.close()
        
        # Sütun genişliklerini otomatik ayarla
        for i in range(6):
            self.islem_tree.resizeColumnToContents(i)
    
    def cikis_yap(self):
        from kullanici_giris import KullaniciGiris
        self.close()
        self.giris = KullaniciGiris()
        self.giris.show() 