# Auto Register BO Server

Script Python untuk auto register customer ke dashboard menggunakan mapping dari Excel.

## Fitur

- ✅ Login ke dashboard operator portal
- ✅ Auto register customer dari Excel
- ✅ Auto skip customer yang sudah pernah register
- ✅ Mapping Traffic dan Bank otomatis
- ✅ Generate report hasil register

## Instalasi

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Untuk menggunakan Selenium (jika form login memerlukan JavaScript):
```bash
pip install selenium
```
Download ChromeDriver dari: https://chromedriver.chromium.org/

## Penggunaan

### 1. Buat Template Excel

```bash
python create_excel_template.py
```

File `customers.xlsx` akan dibuat. Edit file ini dengan data customer Anda.

### 2. Edit File Excel

Buka `customers.xlsx` dan isi dengan data customer:
- Username
- Name
- Phone (tanpa country code)
- Country (Malaysia, Cambodia, dll)
- Traffic (Social Media, LVMY High Value, dll)
- Bank (Maybank, CIMB, dll)
- Bank Account Name
- Account No

**Pastikan Traffic dan Bank sesuai dengan mapping di `mappings.json`**

### 3. Jalankan Auto Register

```bash
python register_customer.py
```

Script akan:
1. Login ke dashboard
2. Register setiap customer dari Excel
3. Skip customer yang sudah pernah register
4. Generate report hasil di `customers_results.xlsx`

### 4. Cek Hasil

Buka file `customers_results.xlsx` untuk melihat hasil register setiap customer.

**Untuk panduan lengkap, lihat file `CARA_PENGGUNAAN.md`**

## Credentials

- **URL**: https://hwbo88v2.com/op/login
- **Username**: sbmycrmoperation
- **Password**: wvWNsyo8UmcX

## Catatan

- Script login menggunakan requests untuk HTTP requests
- Jika form login memerlukan JavaScript, gunakan versi Selenium
- Session/cookies akan disimpan untuk digunakan di request berikutnya
