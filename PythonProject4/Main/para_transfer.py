from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import Qt
import sqlite3
from datetime import datetime

class ParaTransferFormu(QMainWindow):
    def __init__(self, kullanici_bilgileri):
        super().__init__()
        self.kullanici_bilgileri = kullanici_bilgileri
        self.setWindowTitle("💸 Para Transfer")
        self.setGeometry(100, 100, 500, 400)
        self.setMinimumSize(400, 300)
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
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5bc0de, stop:1 #46b8da);
                border-radius: 10px;
                margin: 10px;
                padding: 20px;
            }
        """)
        baslik_layout = QVBoxLayout()
        baslik_layout.setSpacing(10)
        baslik_layout.setContentsMargins(10, 10, 10, 10)
        baslik_frame.setLayout(baslik_layout)
        
        baslik = QLabel("💸 Para Transfer")
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
        
        alici_label = QLabel("Alıcı TC No:")
        alici_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.alici_tc = QLineEdit()
        self.alici_tc.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                min-height: 35px;
            }
            QLineEdit:focus {
                border: 1px solid #5bc0de;
            }
        """)
        self.alici_tc.setPlaceholderText("Alıcının TC kimlik numarası")
        
        miktar_label = QLabel("Transfer Miktarı (₺):")
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
                border: 1px solid #5bc0de;
            }
        """)
        self.miktar_entry.setPlaceholderText("Transfer edilecek miktar")
        
        transfer_btn = QPushButton("Para Transfer Et")
        transfer_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5bc0de, stop:1 #46b8da);
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-height: 35px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #46b8da, stop:1 #5bc0de);
            }
            QPushButton:pressed {
                background: #46b8da;
            }
        """)
        transfer_btn.clicked.connect(self.para_transfer)
        
        form_layout.addWidget(alici_label)
        form_layout.addWidget(self.alici_tc)
        form_layout.addWidget(miktar_label)
        form_layout.addWidget(self.miktar_entry)
        form_layout.addWidget(transfer_btn)
        
        layout.addWidget(form_frame)
    
    def para_transfer(self):
        try:
            alici_tc = self.alici_tc.text().strip()
            miktar = float(self.miktar_entry.text().strip())
            
            if miktar <= 0:
                raise ValueError
            
            conn = sqlite3.connect('banka.db')
            cursor = conn.cursor()
            
            cursor.execute('SELECT bakiye FROM kullanicilar WHERE tc_no = ?', 
                         (self.kullanici_bilgileri[1],))
            gonderen_bakiye = cursor.fetchone()[0]
            
            if miktar > gonderen_bakiye:
                QMessageBox.warning(self, "Hata", "Yetersiz bakiye!")
                return
            
            cursor.execute('SELECT id FROM kullanicilar WHERE tc_no = ?', (alici_tc,))
            alici = cursor.fetchone()
            
            if not alici:
                QMessageBox.warning(self, "Hata", "Alıcı bulunamadı!")
                return
            
            alici_id = alici[0]
            
            cursor.execute('''
            UPDATE kullanicilar 
            SET bakiye = bakiye - ? 
            WHERE tc_no = ?
            ''', (miktar, self.kullanici_bilgileri[1]))
            
            cursor.execute('''
            UPDATE kullanicilar 
            SET bakiye = bakiye + ? 
            WHERE tc_no = ?
            ''', (miktar, alici_tc))
            
            cursor.execute('''
            INSERT INTO islem_gecmisi (kullanici_id, islem_turu, miktar, tarih, aciklama)
            VALUES (?, ?, ?, ?, ?)
            ''', (self.kullanici_bilgileri[0], 'transfer_gonderme', miktar, 
                 datetime.now(), f'Para transferi - Alıcı TC: {alici_tc}'))
            
            cursor.execute('''
            INSERT INTO islem_gecmisi (kullanici_id, islem_turu, miktar, tarih, aciklama)
            VALUES (?, ?, ?, ?, ?)
            ''', (alici_id, 'transfer_alma', miktar, 
                 datetime.now(), f'Para transferi - Gönderen TC: {self.kullanici_bilgileri[1]}'))
            
            conn.commit()
            conn.close()
            
            self.alici_tc.clear()
            self.miktar_entry.clear()
            QMessageBox.information(self, "Başarılı", f"₺{miktar:.2f} transfer edildi!")
            
        except ValueError:
            QMessageBox.warning(self, "Hata", "Geçerli bir miktar girin!") 