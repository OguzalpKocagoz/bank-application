from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import Qt
import sqlite3
from datetime import datetime

class ParaYatirFormu(QMainWindow):
    def __init__(self, kullanici_bilgileri):
        super().__init__()
        self.kullanici_bilgileri = kullanici_bilgileri
        self.setWindowTitle("💰 Para Yatır")
        self.setGeometry(100, 100, 500, 300)
        self.setMinimumSize(400, 250)
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
        layout.setSpacing(15)
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
        
        baslik = QLabel("💰 Para Yatır")
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
        
        miktar_label = QLabel("Yatırılacak Miktar (₺):")
        miktar_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.miktar_entry = QLineEdit()
        self.miktar_entry.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                min-height: 35px;
            }
            QLineEdit:focus {
                border: 1px solid #10b981;
            }
        """)
        self.miktar_entry.setPlaceholderText("Miktar giriniz")
        
        yatir_btn = QPushButton("Para Yatır")
        yatir_btn.setStyleSheet("""
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
        yatir_btn.clicked.connect(self.para_yatir)
        
        form_layout.addWidget(miktar_label)
        form_layout.addWidget(self.miktar_entry)
        form_layout.addWidget(yatir_btn)
        
        layout.addWidget(form_frame)
    
    def para_yatir(self):
        try:
            miktar = float(self.miktar_entry.text().strip())
            if miktar <= 0:
                raise ValueError
            
            conn = sqlite3.connect('banka.db')
            cursor = conn.cursor()
            
            cursor.execute('''
            UPDATE kullanicilar 
            SET bakiye = bakiye + ? 
            WHERE tc_no = ?
            ''', (miktar, self.kullanici_bilgileri[1]))
            
            cursor.execute('''
            INSERT INTO islem_gecmisi (kullanici_id, islem_turu, miktar, tarih, aciklama)
            VALUES (?, ?, ?, ?, ?)
            ''', (self.kullanici_bilgileri[0], 'yatirma', miktar, 
                 datetime.now(), 'Para yatırma işlemi'))
            
            conn.commit()
            conn.close()
            
            self.miktar_entry.clear()
            QMessageBox.information(self, "Başarılı", f"₺{miktar:.2f} yatırıldı!")
            
        except ValueError:
            QMessageBox.warning(self, "Hata", "Geçerli bir miktar girin!") 