from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, 
                             QPushButton, QMessageBox, QFrame, QTreeWidget,
                             QTreeWidgetItem, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import sqlite3
from datetime import datetime

class IslemGecmisiFormu(QMainWindow):
    def __init__(self, kullanici_bilgileri):
        super().__init__()
        self.kullanici_bilgileri = kullanici_bilgileri
        self.setWindowTitle("📊 İşlem Geçmişi")
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
        
        baslik_frame = QFrame()
        baslik_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4361ee, stop:1 #3a0ca3);
                border-radius: 10px;
                margin: 10px;
                padding: 20px;
            }
        """)
        baslik_layout = QVBoxLayout()
        baslik_layout.setSpacing(10)
        baslik_layout.setContentsMargins(10, 10, 10, 10)
        baslik_frame.setLayout(baslik_layout)
        
        baslik = QLabel("📊 İşlem Geçmişi")
        baslik.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
            margin: 5px;
        """)
        baslik.setAlignment(Qt.AlignCenter)
        baslik_layout.addWidget(baslik)
        
        layout.addWidget(baslik_frame)
        
        self.gecmis_tree = QTreeWidget()
        self.gecmis_tree.setHeaderLabels(['📅 Tarih', '💫 İşlem Türü', '💰 Miktar', '📝 Açıklama'])
        self.gecmis_tree.setAlternatingRowColors(True)
        self.gecmis_tree.setStyleSheet("""
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
        
        layout.addWidget(self.gecmis_tree)
        
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
        
        yenile_btn = QPushButton("🔄 İşlem Geçmişini Yenile")
        yenile_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4361ee, stop:1 #3a0ca3);
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-height: 35px;
                margin: 5px;
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
        
        self.islemleri_goster()
    
    def islemleri_goster(self):
        self.gecmis_tree.clear()
        
        conn = sqlite3.connect('banka.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT tarih, islem_turu, miktar, aciklama
        FROM islem_gecmisi
        WHERE kullanici_id = ?
        ORDER BY tarih DESC
        ''', (self.kullanici_bilgileri[0],))
        
        for islem in cursor.fetchall():
            item = QTreeWidgetItem(self.gecmis_tree)
            
            tarih = datetime.strptime(islem[0], '%Y-%m-%d %H:%M:%S.%f')
            formatli_tarih = tarih.strftime('%d.%m.%Y %H:%M')
            item.setText(0, formatli_tarih)
            
            if islem[1] == 'yatirma':
                item.setText(1, '⬆️ Para Yatırma')
                item.setText(2, f"+₺{islem[2]:.2f}")
                item.setForeground(2, QColor('#28a745'))
            elif islem[1] == 'cekme':
                item.setText(1, '⬇️ Para Çekme')
                item.setText(2, f"-₺{islem[2]:.2f}")
                item.setForeground(2, QColor('#dc3545'))
            elif islem[1] == 'transfer_gonderme':
                item.setText(1, '➡️ Para Transferi (Gönderen)')
                item.setText(2, f"-₺{islem[2]:.2f}")
                item.setForeground(2, QColor('#dc3545'))
            elif islem[1] == 'transfer_alma':
                item.setText(1, '⬅️ Para Transferi (Alıcı)')
                item.setText(2, f"+₺{islem[2]:.2f}")
                item.setForeground(2, QColor('#28a745'))
            
            item.setText(3, islem[3])
            
            for i in range(4):
                item.setTextAlignment(i, Qt.AlignCenter)
        
        conn.close()
        
        for i in range(4):
            self.gecmis_tree.resizeColumnToContents(i)
        
        if self.gecmis_tree.topLevelItemCount() == 0:
            bos_item = QTreeWidgetItem(self.gecmis_tree)
            bos_item.setText(0, "")
            bos_item.setText(1, "Henüz işlem geçmişi bulunmuyor")
            bos_item.setText(2, "")
            bos_item.setText(3, "")
            for i in range(4):
                bos_item.setTextAlignment(i, Qt.AlignCenter)
            bos_item.setForeground(1, QColor('#6c757d')) 