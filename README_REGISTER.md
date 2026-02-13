# Auto Register Customer - Panduan Penggunaan

## Overview
Script ini digunakan untuk auto register customer dari Excel ke dashboard menggunakan Selenium automation.

## File yang Dibutuhkan

1. **register_customer.py** - Script utama untuk auto register
2. **login_selenium.py** - Script untuk login (sudah dibuat sebelumnya)
3. **mappings.json** - File mapping untuk Traffic ID, Bank ID, dan Country Code
4. **customers.xlsx** - File Excel berisi data customer yang akan diregister

## Struktur Excel (customers.xlsx)

File Excel harus memiliki kolom berikut:

| Kolom | Deskripsi | Contoh |
|-------|-----------|--------|
| Username | Username untuk customer | customer1 |
| Name | Nama lengkap customer | John Doe |
| Phone | Nomor telepon (tanpa country code) | 123456789 |
| Country | Nama country | Malaysia |
| Traffic | Nama traffic source | Social Media |
| Bank | Nama bank | Maybank |
| Bank Account Name | Nama pemilik rekening | JOHN DOE |
| Account No | Nomor rekening bank | 1234567890 |

### Catatan Penting:
- **Traffic**: Harus sesuai dengan nama di `mappings.json` (case sensitive)
- **Bank**: Harus sesuai dengan nama di `mappings.json` (case sensitive)
- **Country**: Pilihan: Malaysia, Cambodia, Indonesia, Thailand, Singapore, Vietnam, Philippines
- **Phone**: Hanya angka, tanpa country code (country code akan dipilih otomatis)

## Cara Menggunakan

### 1. Buat Template Excel
```bash
python create_excel_template.py
```
File `customers.xlsx` akan dibuat dengan contoh data.

### 2. Edit Excel dengan Data Customer
Buka `customers.xlsx` dan isi dengan data customer yang akan diregister.

**Pastikan:**
- Traffic sesuai dengan mapping (lihat `mappings.json`)
- Bank sesuai dengan mapping (lihat `mappings.json`)
- Semua field terisi (tidak boleh kosong)

### 3. Jalankan Auto Register
```bash
python register_customer.py
```

Atau edit file `register_customer.py` di bagian bawah untuk mengubah:
- `EXCEL_FILE` - nama file Excel Anda
- `USERNAME` - username login dashboard
- `PASSWORD` - password login dashboard

## Mapping Traffic

Traffic yang tersedia (lihat `mappings.json` untuk lengkapnya):
- Social Media (ID: 1)
- Old Member (ID: 2)
- (PPC) SEO (ID: 3)
- (PPC) Facebook (Inbound) (ID: 4)
- Shooter (ID: 5)
- TMT (ID: 6)
- Recommend (ID: 7)
- Others (ID: 8)
- Pornsite (ID: 9)
- Organic (ID: 32)
- Dan lainnya...

## Mapping Bank

Bank yang tersedia (lihat `mappings.json` untuk lengkapnya):
- Maybank (ID: 9)
- CIMB (ID: 7)
- Public Bank (ID: 15)
- Hong Leong (ID: 8)
- AmBank (ID: 5)
- Dan lainnya...

## Output

Setelah selesai, script akan membuat file `customers_results.xlsx` yang berisi:
- Row number
- Username
- Status (Success/Failed/Error message)

## Troubleshooting

### Error: "Traffic tidak ditemukan di mapping"
- Pastikan nama Traffic di Excel sesuai persis dengan yang ada di `mappings.json`
- Case sensitive, jadi "Social Media" bukan "social media"

### Error: "Bank tidak ditemukan di mapping"
- Pastikan nama Bank di Excel sesuai persis dengan yang ada di `mappings.json`
- Case sensitive

### Error: "Form tidak muncul"
- Pastikan koneksi internet stabil
- Cek apakah dashboard masih bisa diakses manual
- Coba jalankan ulang script

### Error: "Login gagal"
- Cek username dan password di script
- Pastikan credentials masih valid

## Catatan

- Script akan membuka browser Chrome (tidak headless) untuk memudahkan monitoring
- Setiap customer akan diregister satu per satu dengan delay 2 detik
- Jika ada error pada satu customer, script akan lanjut ke customer berikutnya
- Browser akan tetap terbuka 5 detik setelah selesai untuk verifikasi
