# Cara Menggunakan Auto Register Customer

## Langkah-langkah Penggunaan

### 1. Siapkan File Excel

**A. Buat Template Excel (jika belum ada):**
```bash
python create_excel_template.py
```
File `customers.xlsx` akan dibuat dengan contoh data.

**B. Edit File Excel dengan Data Customer:**
- Buka file `customers.xlsx`
- Isi data customer yang akan diregister
- Pastikan semua kolom terisi dengan benar

**Kolom yang harus ada:**
- **Username** - Username untuk customer (contoh: customer1)
- **Name** - Nama lengkap customer (contoh: John Doe)
- **Phone** - Nomor telepon tanpa country code (contoh: 123456789)
- **Country** - Nama country (contoh: Malaysia, Cambodia, Indonesia, dll)
- **Traffic** - Nama traffic source (contoh: Social Media, LVMY High Value, Organic, dll)
- **Bank** - Nama bank (contoh: Maybank, CIMB, Public Bank, dll)
- **Bank Account Name** - Nama pemilik rekening (contoh: JOHN DOE)
- **Account No** - Nomor rekening bank (contoh: 1234567890)

**Catatan Penting:**
- Traffic harus sesuai persis dengan yang ada di `mappings.json` (case sensitive)
- Bank harus sesuai persis dengan yang ada di `mappings.json` (case sensitive)
- Phone hanya angka, tanpa country code (country code akan dipilih otomatis)

### 2. Edit Konfigurasi (Opsional)

Buka file `register_customer.py` dan edit bagian bawah jika perlu:

```python
if __name__ == "__main__":
    # Configuration
    EXCEL_FILE = "customers.xlsx"  # Ganti dengan nama file Excel Anda
    USERNAME = "sbmycrmoperation"   # Username login dashboard
    PASSWORD = "wvWNsyo8UmcX"      # Password login dashboard
    
    register = CustomerRegister()
    register.register_from_excel(EXCEL_FILE, USERNAME, PASSWORD)
```

**Atau** edit langsung di terminal saat menjalankan (akan dijelaskan di langkah 3).

### 3. Jalankan Script

**Cara 1: Langsung (menggunakan konfigurasi di script):**
```bash
python register_customer.py
```

**Cara 2: Dengan parameter (jika ingin ganti file Excel):**
Edit file `register_customer.py` bagian bawah, ganti `EXCEL_FILE` dengan nama file Excel Anda.

### 4. Proses yang Akan Terjadi

1. **Login** - Script akan login ke dashboard secara otomatis
2. **Navigate** - Script akan navigate ke halaman Member
3. **Register** - Untuk setiap customer di Excel:
   - Klik button "Member Add"
   - Isi form register dengan data dari Excel
   - Submit form
   - Jika customer sudah pernah register → Skip dan lanjut
   - Jika berhasil → Lanjut ke customer berikutnya
4. **Summary** - Script akan menampilkan summary hasil
5. **Results** - File `customers_results.xlsx` akan dibuat dengan hasil register

### 5. Hasil

Setelah selesai, akan ada file `customers_results.xlsx` yang berisi:
- **Row** - Nomor baris di Excel
- **Username** - Username customer
- **Status** - Status register:
  - `Success` - Register berhasil
  - `Duplicate (Already Registered)` - Customer sudah pernah register, di-skip
  - `Failed` - Register gagal

## Contoh Penggunaan

### Contoh 1: Register 3 Customer

**File Excel (customers.xlsx):**
```
Username    | Name          | Phone      | Country  | Traffic          | Bank      | Bank Account Name | Account No
customer1   | John Doe      | 123456789  | Malaysia | Social Media     | Maybank   | JOHN DOE          | 1234567890
customer2   | Jane Smith    | 987654321  | Malaysia | LVMY High Value | CIMB      | JANE SMITH        | 0987654321
customer3   | Bob Johnson   | 555555555  | Malaysia | Organic          | Public Bank | BOB JOHNSON    | 5555555555
```

**Jalankan:**
```bash
python register_customer.py
```

**Output yang akan muncul:**
```
==================================================
AUTO REGISTER CUSTOMER DARI EXCEL
==================================================

Membaca file Excel: customers.xlsx
[OK] Excel loaded: 3 rows
Columns: ['Username', 'Name', 'Phone', 'Country', 'Traffic', 'Bank', 'Bank Account Name', 'Account No']

==================================================
LOGIN KE DASHBOARD
==================================================
...
[OK] Login berhasil!

==================================================
PROSES 1/3
==================================================
...
[OK] Customer 1 berhasil diregister

==================================================
PROSES 2/3
==================================================
...
[OK] Customer 2 berhasil diregister

==================================================
PROSES 3/3
==================================================
...
[OK] Customer 3 berhasil diregister

==================================================
SUMMARY REGISTRATION
==================================================
Total: 3
Success: 3
Duplicate (Skipped): 0
Failed: 0

[OK] Results saved to: customers_results.xlsx
```

## Troubleshooting

### Error: "File Excel tidak ditemukan"
- Pastikan file Excel ada di folder yang sama dengan script
- Cek nama file sesuai dengan yang di konfigurasi

### Error: "Traffic tidak ditemukan di mapping"
- Pastikan nama Traffic di Excel sesuai persis dengan yang ada di `mappings.json`
- Case sensitive (huruf besar/kecil harus sama)
- Contoh: "Social Media" bukan "social media"

### Error: "Bank tidak ditemukan di mapping"
- Pastikan nama Bank di Excel sesuai persis dengan yang ada di `mappings.json`
- Case sensitive
- Contoh: "Maybank" bukan "maybank"

### Error: "Login gagal"
- Cek username dan password di script
- Pastikan koneksi internet stabil
- Pastikan dashboard bisa diakses manual

### Browser tidak terbuka
- Pastikan Chrome browser sudah terinstall
- Selenium akan auto-download ChromeDriver jika belum ada

## Tips

1. **Test dengan 1-2 customer dulu** sebelum register banyak customer
2. **Backup file Excel** sebelum menjalankan script
3. **Cek hasil di `customers_results.xlsx`** setelah selesai
4. **Pastikan Traffic dan Bank sesuai** dengan mapping untuk menghindari error
5. **Jangan tutup browser** saat script sedang berjalan (script akan tutup sendiri setelah selesai)

## Daftar Traffic yang Tersedia

Lihat file `mappings.json` untuk daftar lengkap, atau gunakan:
- Social Media
- LVMY High Value
- LVMY Potential
- Organic
- Old Member
- Recommend
- Others
- Dan lainnya (lihat mappings.json)

## Daftar Bank yang Tersedia

Lihat file `mappings.json` untuk daftar lengkap, atau gunakan:
- Maybank
- CIMB
- Public Bank
- Hong Leong
- AmBank
- Dan lainnya (lihat mappings.json)
