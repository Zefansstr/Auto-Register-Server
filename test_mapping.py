"""
Script untuk test mapping Traffic dan Bank
"""
import json

# Load mappings
with open('mappings.json', 'r', encoding='utf-8') as f:
    mappings = json.load(f)

print("=" * 50)
print("TEST MAPPING TRAFFIC")
print("=" * 50)

# Test LVMY High Value dan LVMY Potential
test_traffics = [
    "LVMY High Value",
    "LVMY Potential",
    "lvmy high value",  # lowercase
    "LVMY HIGH VALUE",  # uppercase
    "LVMY High Value ",  # dengan spasi
    " Social Media",
    "Social Media"
]

for traffic in test_traffics:
    traffic_stripped = traffic.strip()
    # Exact match
    if traffic_stripped in mappings['traffic']:
        print(f"[OK] '{traffic}' -> {mappings['traffic'][traffic_stripped]}")
    else:
        # Case-insensitive match
        found = False
        for key, value in mappings['traffic'].items():
            if key.strip().lower() == traffic_stripped.lower():
                print(f"[OK] '{traffic}' -> {value} (case-insensitive match dengan '{key}')")
                found = True
                break
        if not found:
            print(f"[ERROR] '{traffic}' -> TIDAK DITEMUKAN")

print("\n" + "=" * 50)
print("DAFTAR TRAFFIC YANG TERSEDIA")
print("=" * 50)
for key, value in sorted(mappings['traffic'].items()):
    print(f"  {key} -> {value}")

print("\n" + "=" * 50)
print("DAFTAR BANK YANG TERSEDIA")
print("=" * 50)
for key, value in sorted(mappings['bank'].items()):
    print(f"  {key} -> {value}")
