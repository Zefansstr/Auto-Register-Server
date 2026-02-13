"""
Script untuk membuat template Excel untuk register customer
"""
import pandas as pd

# Buat template Excel dengan kolom yang diperlukan
template_data = {
    'Username': ['customer1', 'customer2', 'customer3'],
    'Name': ['Customer One', 'Customer Two', 'Customer Three'],
    'Phone': ['123456789', '987654321', '555555555'],
    'Country': ['Malaysia', 'Malaysia', 'Malaysia'],
    'Traffic': ['Social Media', 'Organic', 'Recommend'],
    'Bank': ['Maybank', 'CIMB', 'Public Bank'],
    'Bank Account Name': ['CUSTOMER ONE', 'CUSTOMER TWO', 'CUSTOMER THREE'],
    'Account No': ['1234567890', '0987654321', '5555555555']
}

# Buat DataFrame
df = pd.DataFrame(template_data)

# Simpan ke Excel
output_file = 'customers.xlsx'
df.to_excel(output_file, index=False, sheet_name='Customers')

print(f"[OK] Template Excel berhasil dibuat: {output_file}")
print(f"\nKolom yang tersedia:")
for col in df.columns:
    print(f"  - {col}")

print(f"\nContoh data:")
print(df.head())

print(f"\n[INFO] Silakan edit file {output_file} dengan data customer Anda")
print("[INFO] Pastikan Traffic dan Bank sesuai dengan mapping di mappings.json")
