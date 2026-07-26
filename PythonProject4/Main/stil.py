"""Ekranlarin ortak gorunum tanimlari.

Iki kurala uyulur:

1. Kap (QFrame) bicimlendirilirken `QFrame { ... }` yerine `#nesneAdi { ... }`
   secicisi kullanilir. QLabel, QFrame'in alt sinifi oldugu icin `QFrame`
   secicisi kartin icindeki butun etiketlere de carpar; etiketler kartin
   arkaplanini ve padding'ini devralip yazilari gorunmez olur.

2. QSS'te `margin` kullanilmaz. Margin widget'in cizim alanini daraltir ama
   layout bunu hesaba katmadigi icin kutular ust uste biner. Bosluk her zaman
   layout uzerinden (setSpacing / setContentsMargins) verilir.
"""

# --- Temel renkler --------------------------------------------------------
ARKA_PLAN = "#f3f4f6"
KART_RENGI = "#ffffff"
KENAR = "#e5e7eb"
YAZI_RENGI = "#111827"
SOLUK_YAZI = "#6b7280"

# --- Vurgu renkleri: (normal, uzerine gelince, basiliyken) ---------------
INDIGO = ("#4f46e5", "#4338ca", "#3730a3")
MAVI = ("#2563eb", "#1d4ed8", "#1e40af")
YESIL = ("#059669", "#047857", "#065f46")
TURUNCU = ("#d97706", "#b45309", "#92400e")
TEAL = ("#0891b2", "#0e7490", "#155e75")
MOR = ("#7c3aed", "#6d28d9", "#5b21b6")
KIRMIZI = ("#dc2626", "#b91c1c", "#991b1b")
GRI = ("#6b7280", "#4b5563", "#374151")

# Basari / hata gostergeleri
BASARI_RENGI = "#059669"
HATA_RENGI = "#dc2626"

YAZI_TIPI = '"Segoe UI Variable Text", "Segoe UI", "Inter", sans-serif'


def gradyan(renkler):
    """Baslik kartlari icin yumusak, capraz gecis."""
    bas, son = renkler[0], renkler[2]
    return (f"qlineargradient(x1:0, y1:0, x2:1, y2:1, "
            f"stop:0 {bas}, stop:1 {son})")


def pencere():
    """QMainWindow'un tabani. Burada QLabel/QPushButton'a margin verilmez."""
    return f"""
        QMainWindow, QDialog {{
            background: {ARKA_PLAN};
        }}
        QLabel {{
            color: {YAZI_RENGI};
            font-family: {YAZI_TIPI};
            font-size: 13px;
            background: transparent;
        }}
        QToolTip {{
            background: {YAZI_RENGI};
            color: white;
            border: none;
            padding: 6px 8px;
        }}
    """


def baslik_karti(renkler=INDIGO):
    """Ustteki renkli baslik kartinin bicimi (#baslikKarti)."""
    return f"""
        #baslikKarti {{
            background: {gradyan(renkler)};
            border-radius: 18px;
        }}
        #baslikKarti QLabel {{
            color: white;
            background: transparent;
        }}
    """


def beyaz_kart(nesne_adi="kart"):
    """Yumusak kenarli, ince cerceveli beyaz panel."""
    return f"""
        #{nesne_adi} {{
            background: {KART_RENGI};
            border: 1px solid {KENAR};
            border-radius: 18px;
        }}
    """


def baslik_yazisi(boyut=22):
    return (f"color: white; font-family: {YAZI_TIPI}; font-size: {boyut}px; "
            f"font-weight: 600; letter-spacing: 0.2px;")


def ikon_yazisi(boyut=40):
    return f"color: white; font-size: {boyut}px;"


def alt_baslik():
    """Baslik kartindaki ikincil satir (ornegin bakiye)."""
    return (f"color: rgba(255, 255, 255, 0.88); font-family: {YAZI_TIPI}; "
            f"font-size: 14px;")


def bolum_basligi(boyut=15):
    return (f"color: {YAZI_RENGI}; font-family: {YAZI_TIPI}; "
            f"font-size: {boyut}px; font-weight: 600;")


def alan_etiketi():
    return (f"color: {SOLUK_YAZI}; font-family: {YAZI_TIPI}; font-size: 12px; "
            f"font-weight: 600; letter-spacing: 0.3px;")


def soluk_yazi(boyut=12):
    return f"color: {SOLUK_YAZI}; font-family: {YAZI_TIPI}; font-size: {boyut}px;"


def giris_kutusu(renkler=INDIGO):
    """QLineEdit. Padding yalniz yaprak kontrollerde guvenli: Qt padding'i
    sizeHint'e ekler, dolayisiyla layout dogru yer ayirir."""
    odak = renkler[0]
    return f"""
        QLineEdit {{
            padding: 10px 12px;
            border: 1px solid {KENAR};
            border-radius: 10px;
            font-family: {YAZI_TIPI};
            font-size: 13px;
            background: #fbfbfc;
            color: {YAZI_RENGI};
            min-height: 20px;
            selection-background-color: {odak};
        }}
        QLineEdit:hover {{
            border: 1px solid #d1d5db;
            background: white;
        }}
        QLineEdit:focus {{
            border: 1px solid {odak};
            background: white;
        }}
    """


def buton(renkler=INDIGO):
    normal, uzerinde, basili = renkler
    return f"""
        QPushButton {{
            background: {normal};
            color: white;
            padding: 11px 18px;
            border: none;
            border-radius: 10px;
            font-family: {YAZI_TIPI};
            font-size: 13px;
            font-weight: 600;
            min-height: 20px;
        }}
        QPushButton:hover {{
            background: {uzerinde};
        }}
        QPushButton:pressed {{
            background: {basili};
        }}
        QPushButton:disabled {{
            background: #d1d5db;
            color: #f9fafb;
        }}
    """


def ikincil_buton():
    """Cerceveli, notr buton: ikincil eylemler icin."""
    return f"""
        QPushButton {{
            background: white;
            color: {YAZI_RENGI};
            padding: 11px 18px;
            border: 1px solid {KENAR};
            border-radius: 10px;
            font-family: {YAZI_TIPI};
            font-size: 13px;
            font-weight: 600;
            min-height: 20px;
        }}
        QPushButton:hover {{
            background: #f9fafb;
            border: 1px solid #d1d5db;
        }}
        QPushButton:pressed {{
            background: #f3f4f6;
        }}
    """


def agac():
    """QTreeWidget (listeler). Item'lara margin verilmez."""
    return f"""
        QTreeWidget {{
            background-color: {KART_RENGI};
            border: 1px solid {KENAR};
            border-radius: 14px;
            padding: 6px;
            font-family: {YAZI_TIPI};
            font-size: 13px;
            color: {YAZI_RENGI};
            outline: none;
        }}
        QTreeWidget::item {{
            height: 38px;
            border-bottom: 1px solid #f3f4f6;
        }}
        QTreeWidget::item:selected {{
            background: #eef2ff;
            color: {INDIGO[0]};
        }}
        QTreeWidget::item:hover {{
            background: #f9fafb;
        }}
        QHeaderView::section {{
            background-color: {KART_RENGI};
            padding: 12px 8px;
            border: none;
            border-bottom: 1px solid {KENAR};
            font-family: {YAZI_TIPI};
            font-weight: 600;
            font-size: 12px;
            color: {SOLUK_YAZI};
        }}
        QScrollBar:vertical {{
            background: transparent;
            width: 10px;
        }}
        QScrollBar::handle:vertical {{
            background: #d1d5db;
            border-radius: 5px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: #9ca3af;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}
    """


def sekme():
    return f"""
        QTabWidget::pane {{
            border: 1px solid {KENAR};
            background: {KART_RENGI};
            border-radius: 16px;
            top: -1px;
        }}
        QTabBar::tab {{
            background: transparent;
            color: {SOLUK_YAZI};
            min-width: 120px;
            padding: 10px 18px;
            margin-right: 6px;
            border: 1px solid transparent;
            border-radius: 10px;
            font-family: {YAZI_TIPI};
            font-size: 13px;
            font-weight: 600;
        }}
        QTabBar::tab:selected {{
            background: {KART_RENGI};
            color: {INDIGO[0]};
            border: 1px solid {KENAR};
        }}
        QTabBar::tab:hover:!selected {{
            background: #e9eaee;
            color: {YAZI_RENGI};
        }}
    """
