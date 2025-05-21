from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox

class BakiyeSorgulaFormu(QMainWindow):
    def __init__(self, hesaplar):
        super().__init__()
        self.setWindowTitle("Bakiye Sorgula")
        self.setGeometry(200, 200, 300, 200)

        self.hesaplar = hesaplar

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.hesap_no_label = QLabel("Hesap Numarası:", self)
        self.hesap_no_input = QLineEdit(self)

        self.sorgula_btn = QPushButton("Bakiye Sorgula", self)
        self.sorgula_btn.clicked.connect(self.bakiye_sorgula)

        layout.addWidget(self.hesap_no_label)
        layout.addWidget(self.hesap_no_input)
        layout.addWidget(self.sorgula_btn)

        central_widget.setLayout(layout)

    def bakiye_sorgula(self):
        hesap_no = self.hesap_no_input.text()

        if hesap_no in self.hesaplar:
            bakiye = self.hesaplar[hesap_no]["bakiye"]
            QMessageBox.information(self, "Bakiye", f"Hesap Bakiyesi: {bakiye} TL")
        else:
            QMessageBox.warning(self, "Hata", "Geçersiz hesap numarası!")