# Panduan Instalasi Python

## Masalah: 'pip' is not recognized

Ini berarti Python belum terinstall atau tidak ada di PATH system.

## Solusi 1: Install Python (Recommended)

1. **Download Python:**
   - Kunjungi: https://www.python.org/downloads/
   - Download Python 3.11 atau 3.12 (versi terbaru)

2. **Install Python:**
   - Jalankan installer yang sudah didownload
   - **PENTING:** Centang checkbox "Add Python to PATH" saat instalasi
   - Klik "Install Now"

3. **Verifikasi instalasi:**
   - Buka Command Prompt baru (atau restart terminal)
   - Ketik: `python --version`
   - Ketik: `pip --version`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Solusi 2: Gunakan Python Launcher (jika sudah terinstall)

Jika Python sudah terinstall tapi tidak di PATH, coba:

```bash
python -m pip install -r requirements.txt
```

atau

```bash
py -m pip install -r requirements.txt
```

## Solusi 3: Install Manual (tanpa pip)

Jika tidak bisa menggunakan pip, download package manual:

1. **Download packages:**
   - requests: https://pypi.org/project/requests/#files
   - beautifulsoup4: https://pypi.org/project/beautifulsoup4/#files
   - lxml: https://pypi.org/project/lxml/#files

2. **Extract dan install manual** (tidak disarankan, lebih sulit)

## Setelah Python Terinstall

Setelah Python terinstall dengan benar, jalankan:

```bash
pip install -r requirements.txt
```

Kemudian test login:
```bash
python login.py
```
