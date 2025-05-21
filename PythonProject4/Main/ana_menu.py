from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, 
                             QLineEdit, QMessageBox, QTabWidget, QTreeWidget, QTreeWidgetItem,
                             QHBoxLayout, QFrame, QSizePolicy, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import sqlite3
from datetime import datetime
from para_yatir import ParaYatirFormu
from para_cek import ParaCekFormu
from para_transfer import ParaTransferFormu
from islem_gecmisi import IslemGecmisiFormu

class AnaMenu(QMainWindow):
    def __init__(self, kullanici_bilgileri):
        super().__init__()
        self.kullanici_bilgileri = kullanici_bilgileri
        self.setWindowTitle("🏦 Banka Uygulaması")
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
                margin: 3px;
            }
            QTabWidget::pane {
                border: none;
                background: white;
                border-radius: 10px;
            }
            QTabBar::tab {
                background: #f8f9fa;
                border: none;
                padding: 10px 20px;
                margin: 5px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4361ee, stop:1 #3a0ca3);
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background: #e9ecef;
            }
            QTreeWidget {
                font-size: 14px;
                margin: 3px;
            }
            QTreeWidget::item {
                height: 35px;
                margin: 3px;
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
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        central_widget.setLayout(layout)
        
        baslik_frame = QFrame()
        baslik_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4361ee, stop:1 #3a0ca3);
                border-radius: 10px;
                margin: 5px;
                padding: 10px;
            }
        """)
        baslik_layout = QVBoxLayout()
        baslik_layout.setSpacing(5)
        baslik_layout.setContentsMargins(5, 5, 5, 5)
        baslik_frame.setLayout(baslik_layout)
        
        hosgeldin_label = QLabel(f"👋 Hoş Geldiniz, {self.kullanici_bilgileri[2]} {self.kullanici_bilgileri[3]}")
        hosgeldin_label.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: bold;
            margin: 5px;
        """)
        hosgeldin_label.setAlignment(Qt.AlignCenter)
        
        bakiye_label = QLabel(f"💰 Bakiye: ₺{self.kullanici_bilgileri[5]:.2f}")
        bakiye_label.setStyleSheet("""
            color: white;
            font-size: 16px;
            margin: 5px;
        """)
        bakiye_label.setAlignment(Qt.AlignCenter)
        
        baslik_layout.addWidget(hosgeldin_label)
        baslik_layout.addWidget(bakiye_label)
        
        layout.addWidget(baslik_frame)
        
        self.tab_widget = QTabWidget()
        
        # Para İşlemleri Sekmesi
        islemler_tab = QWidget()
        islemler_layout = QVBoxLayout()
        islemler_layout.setSpacing(10)
        islemler_layout.setContentsMargins(10, 10, 10, 10)
        islemler_tab.setLayout(islemler_layout)
        
        yatir_btn = QPushButton("💰 Para Yatır")
        yatir_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #059669);
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
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #059669, stop:1 #10b981);
            }
            QPushButton:pressed {
                background: #059669;
            }
        """)
        yatir_btn.clicked.connect(self.para_yatir_penceresi_ac)
        
        transfer_btn = QPushButton("💸 Para Transfer")
        transfer_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5bc0de, stop:1 #46b8da);
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
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #46b8da, stop:1 #5bc0de);
            }
            QPushButton:pressed {
                background: #46b8da;
            }
        """)
        transfer_btn.clicked.connect(self.para_transfer_penceresi_ac)
        
        cek_btn = QPushButton("💸 Para Çek")
        cek_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f0ad4e, stop:1 #ec971f);
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
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ec971f, stop:1 #f0ad4e);
            }
            QPushButton:pressed {
                background: #ec971f;
            }
        """)
        cek_btn.clicked.connect(self.para_cek_penceresi_ac)
        
        gecmis_btn = QPushButton("📊 İşlem Geçmişi")
        gecmis_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4361ee, stop:1 #3a0ca3);
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
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3a0ca3, stop:1 #4361ee);
            }
            QPushButton:pressed {
                background: #3a0ca3;
            }
        """)
        gecmis_btn.clicked.connect(self.islem_gecmisi_penceresi_ac)
        
        islemler_layout.addWidget(yatir_btn)
        islemler_layout.addWidget(transfer_btn)
        islemler_layout.addWidget(cek_btn)
        islemler_layout.addWidget(gecmis_btn)
        
        self.tab_widget.addTab(islemler_tab, "💰 Para İşlemleri")
        
        layout.addWidget(self.tab_widget)
    
    def para_yatir_penceresi_ac(self):
        self.para_yatir = ParaYatirFormu(self.kullanici_bilgileri)
        self.para_yatir.show()
    
    def para_cek_penceresi_ac(self):
        self.para_cek = ParaCekFormu(self.kullanici_bilgileri)
        self.para_cek.show()
    
    def para_transfer_penceresi_ac(self):
        self.para_transfer = ParaTransferFormu(self.kullanici_bilgileri)
        self.para_transfer.show()
    
    def islem_gecmisi_penceresi_ac(self):
        self.islem_gecmisi = IslemGecmisiFormu(self.kullanici_bilgileri)
        self.islem_gecmisi.show()