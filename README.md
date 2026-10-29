# Automated Invoice Generator (Aplikasi Generator Faktur & Nota Otomatis)

Aplikasi web berbasis Python Flask untuk pembuatan faktur, nota, dan manajemen penagihan bisnis secara otomatis dengan penyimpanan database SQLite lokal.

## 🚀 Fitur
- Pembuatan faktur/nota instan dengan kalkulasi total otomatis.
- Daftar faktur, lihat detail, dan cetak via `@media print`.
- Hapus faktur yang tidak diperlukan.

## 🛠️ Tech Stack
- **Backend:** Python, Flask (Application Factory + Blueprint), SQLite
- **Frontend:** HTML5, CSS3 (Responsive Design)

## 📁 Struktur Proyek
```
invoice_app/
├── app/                      # Package aplikasi
│   ├── __init__.py           # Application factory (create_app)
│   ├── routes/               # Blueprint route (invoice_routes.py)
│   ├── services/             # Logika bisnis & akses database (invoice_service.py)
│   ├── templates/            # Template HTML (Jinja2)
│   └── static/               # Asset CSS
├── config.py                 # Konfigurasi terpusat
├── requirements.txt          # Dependensi ter-pin
├── run.py                    # Entry point development
├── wsgi.py                   # Entry point production (gunicorn)
└── README.md
```

## ⚙️ Cara Menjalankan
1. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
2. Jalankan aplikasi:
   ```bash
   python run.py
   ```
3. Buka di browser: `http://127.0.0.1:5000`
4. (Production) jalankan dengan gunicorn:
   ```bash
   gunicorn wsgi:app
   ```

## 📋 Catatan
- Database SQLite dibuat otomatis di folder `instance/` saat pertama dijalankan.
- Folder `instance/` dan file `*.db` tidak ikut ter-commit (lihat `.gitignore`).
