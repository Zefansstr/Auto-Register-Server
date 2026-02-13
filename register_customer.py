"""
Script untuk auto register customer dari Excel ke dashboard
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from login_selenium import DashboardLoginSelenium
import pandas as pd
import time
import json
import sys
import os

# Fix encoding untuk Windows console (dengan error handling yang lebih aman)
if sys.platform == 'win32':
    try:
        # Set console code page ke UTF-8
        os.system('chcp 65001 >nul 2>&1')
    except:
        pass


class CustomerRegister:
    def __init__(self, base_url="https://hwbo88v2.com"):
        self.base_url = base_url
        self.login_handler = DashboardLoginSelenium(headless=False)
        self.driver = None
        self.is_on_member_page = False  # Flag untuk track apakah sudah di halaman Member
        
    def load_mappings(self):
        """Load mapping untuk Traffic dan Bank dari file JSON"""
        try:
            with open('mappings.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("[WARNING] File mappings.json tidak ditemukan, menggunakan default mapping")
            return self.get_default_mappings()
    
    def get_default_mappings(self):
        """Default mapping jika file tidak ada"""
        return {
            "traffic": {
                "(PPC) CS Shooter": "35",
                "(PPC) Facebook (Collective)": "46",
                "(PPC) Facebook (Inbound)": "4",
                "(PPC) Facebook (Inno)": "60",
                "(PPC) Facebook (RS)": "61",
                "(PPC) Native Ads": "128",
                "(PPC) Pop Ads": "127",
                "(PPC) Push Ads": "125",
                "(PPC) SEO": "3",
                "(PPC) SEO (Telegram BOT)": "67",
                "(PPC) SEO (Telegram)": "72",
                "(PPC) Telegram Ads (inbound)": "59",
                "(PPC) Tiktok (Inbound)": "45",
                "(PPC) Tiktok (KENT)": "36",
                "(PPC) Website Ads (Clickadu)": "126",
                "LVMY High Value": "150",
                "LVMY Potential": "151",
                "Old Member": "2",
                "Organic": "32",
                "Others": "8",
                "Pornsite": "9",
                "Recommend": "7",
                "Shooter": "5",
                "Social Media": "1",
                "TMT": "6"
            },
            "bank": {
                "AmBank": "5",
                "BSN Bank": "6",
                "CIMB": "7",
                "Hong Leong": "8",
                "Maybank": "9",
                "RHB Bank": "10",
                "HSBC": "14",
                "Public Bank": "15",
                "Bank Rakyat": "16",
                "Bank Islam": "17",
                "Alliance Bank": "18",
                "Standard Chartered": "19",
                "Other Bank": "20",
                "Bank Muamalat": "21",
                "Affin Bank": "22",
                "UOB Bank": "23",
                "Citi Bank": "24",
                "Bank Of China": "25",
                "Agro Bank": "35",
                "Touch N Go": "43",
                "Telco": "44",
                "BSNEBIZ": "45",
                "OCBC": "46",
                "GX Bank": "50",
                "Merchantrade Bank": "51"
            },
            "country_code": {
                "Malaysia": "+60",
                "Cambodia": "+855",
                "Indonesia": "+62",
                "Thailand": "+66",
                "Singapore": "+65",
                "Vietnam": "+84",
                "Philippines": "+63"
            }
        }
    
    def login(self, username, password):
        """Login ke dashboard"""
        print("=" * 50)
        print("LOGIN KE DASHBOARD")
        print("=" * 50)
        success = self.login_handler.login(username, password)
        if success:
            self.driver = self.login_handler.driver
            return True
        return False
    
    def navigate_to_member_add(self):
        """Navigate ke halaman Member Add
        Jika sudah di halaman Member, langsung klik button Add saja
        """
        try:
            print("\n" + "=" * 50)
            print("NAVIGATE KE HALAMAN MEMBER ADD")
            print("=" * 50)
            
            wait = WebDriverWait(self.driver, 10)
            
            # Jika sudah di halaman Member, langsung klik button Add
            if self.is_on_member_page:
                print("[INFO] Sudah di halaman Member, langsung klik button Add Member...")
                return self.click_add_member_button()
            
            # Jika belum di halaman Member, navigate dulu
            # Klik menu Member
            print("Mencari menu Member...")
            
            # Cari menu Member (bisa dengan text atau href)
            member_menu = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'menu-link') and contains(., 'Member')]"))
            )
            member_menu.click()
            print("[OK] Menu Member diklik")
            time.sleep(1)
            
            # Klik submenu Member
            print("Mencari submenu Member...")
            member_submenu = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[@href='https://hwbo88v2.com/op/member']"))
            )
            member_submenu.click()
            print("[OK] Submenu Member diklik")
            time.sleep(2)
            
            # Set flag bahwa sudah di halaman Member
            self.is_on_member_page = True
            
            # Klik button "Member Add"
            return self.click_add_member_button()
            
        except Exception as e:
            print(f"[ERROR] Error navigate ke Member Add: {str(e)}")
            return False
    
    def click_add_member_button(self):
        """Klik button Member Add"""
        try:
            wait = WebDriverWait(self.driver, 10)
            
            print("Mencari button Member Add...")
            add_button = wait.until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/op/member/create')]"))
            )
            
            # Tunggu overlay hilang jika ada
            try:
                overlay = self.driver.find_element(By.CSS_SELECTOR, ".blockUI.blockOverlay")
                wait.until(EC.invisibility_of_element(overlay))
            except:
                pass
            
            # Scroll ke button jika perlu
            self.driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
            time.sleep(0.5)
            
            # Coba klik dengan JavaScript jika normal click gagal
            try:
                add_button.click()
            except:
                # Jika click gagal karena intercepted, gunakan JavaScript
                self.driver.execute_script("arguments[0].click();", add_button)
            
            print("[OK] Button Member Add diklik")
            
            # Tunggu modal muncul
            print("Menunggu modal form muncul...")
            time.sleep(3)
            
            # Tunggu form muncul di modal
            wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            print("[OK] Form register muncul")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error klik button Member Add: {str(e)}")
            return False
    
    def fill_register_form(self, customer_data, mappings):
        """Isi form register dengan data customer"""
        try:
            print("\n" + "=" * 50)
            print(f"MENGISI FORM REGISTER: {customer_data.get('Username', 'N/A')}")
            print("=" * 50)
            
            wait = WebDriverWait(self.driver, 10)
            
            # 1. Username
            print("Mengisi Username...")
            username_field = wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.clear()
            username_field.send_keys(str(customer_data.get('Username', '')))
            print(f"[OK] Username: {customer_data.get('Username', '')}")
            time.sleep(0.5)
            
            # 2. Name
            print("Mengisi Name...")
            name_field = self.driver.find_element(By.NAME, "name")
            name_field.clear()
            name_field.send_keys(str(customer_data.get('Name', '')))
            print(f"[OK] Name: {customer_data.get('Name', '')}")
            time.sleep(0.5)
            
            # 3. Phone dengan country code
            print("Mengisi Phone...")
            phone_field = wait.until(
                EC.presence_of_element_located((By.ID, "create_contact"))
            )
            
            # Handle country code: pakai kolom D "Country" di Excel untuk mapping prefix (60, 62, dll)
            country_name = None
            for col_name in ['Country', 'country', 'COUNTRY', 'Country Name', 'Negara']:
                if col_name in customer_data:
                    country_name = str(customer_data.get(col_name, '')).strip()
                    if country_name:
                        break
            if not country_name:
                country_name = 'Malaysia'
            country_code = mappings['country_code'].get(country_name, '+60')
            # Prefix nomor telepon akan dibuang sesuai kode negara ini (60, 62, dll)
            print(f"[DEBUG] Country dari Excel (kolom D): '{country_name}' -> kode {country_code}")
            
            # Klik country selector untuk memilih country
            try:
                # Scroll ke phone field jika perlu
                self.driver.execute_script("arguments[0].scrollIntoView(true);", phone_field)
                time.sleep(0.5)
                
                # Klik country selector dropdown
                country_selector = self.driver.find_element(By.CSS_SELECTOR, ".iti__selected-country-primary, .iti__selected-country")
                country_selector.click()
                time.sleep(1)
                
                # Cari country option berdasarkan country code atau country name
                # Coba beberapa cara untuk menemukan country option
                country_found = False
                try:
                    # Method 1: Cari berdasarkan data-dial-code
                    country_option = self.driver.find_element(By.XPATH, f"//li[@data-dial-code='{country_code.replace('+', '')}']")
                    country_option.click()
                    country_found = True
                except:
                    try:
                        # Method 2: Cari berdasarkan text yang mengandung country code
                        country_option = self.driver.find_element(By.XPATH, f"//li[contains(., '{country_code}')]")
                        country_option.click()
                        country_found = True
                    except:
                        # Method 3: Cari berdasarkan country name
                        country_option = self.driver.find_element(By.XPATH, f"//li[contains(., '{country_name}')]")
                        country_option.click()
                        country_found = True
                
                if country_found:
                    print(f"[OK] Country code dipilih: {country_name} ({country_code})")
                time.sleep(0.5)
            except Exception as e:
                print(f"[INFO] Country code selector tidak ditemukan atau sudah default: {str(e)}")
            
            # Input phone number: JANGAN ambil prefix kode negara (60, +60, 62, dll)
            # Excel sering format "60xxxxxxxx" -> yang diisi ke form hanya "xxxxxxxx" (setelah kode negara)
            raw_phone = customer_data.get('Phone', '')
            # Excel baca angka sebagai float -> 60139900566 jadi 60139900566.0; jangan sampai .0 ikut ke form
            if isinstance(raw_phone, (int, float)):
                raw_phone = str(int(raw_phone))
            else:
                raw_phone = str(raw_phone).strip()
            phone_number = raw_phone
            # Angka kode negara untuk negara customer ini (tanpa +), misal "60", "62"
            dial_digits = country_code.replace('+', '').strip()
            # Buang tanda + di depan jika ada
            if phone_number.startswith('+'):
                phone_number = phone_number[1:].strip()
            # Buang prefix kode negara di depan (60, 62, dll) — ambil hanya nomor setelahnya
            if phone_number.startswith(dial_digits):
                phone_number = phone_number[len(dial_digits):].strip()
            # Buang spasi/dash; buang juga .0 atau karakter non-digit sisa dari Excel float
            phone_number = phone_number.replace(' ', '').replace('-', '')
            phone_number = ''.join(c for c in phone_number if c.isdigit())
            
            phone_field.clear()
            phone_field.send_keys(phone_number)
            print(f"[OK] Phone: {phone_number} (Country: {country_name}, Code: {country_code})")
            time.sleep(0.5)
            
            # 4. Traffic (mapping dari kolom E "Traffic" di Excel)
            print("Mengisi Traffic...")
            # Prioritas: kolom header "Traffic" (biasanya kolom E di Excel)
            traffic_name = None
            for col_name in ['Traffic', 'traffic', 'TRAFFIC', 'Traffic Source', 'traffic_source']:
                if col_name in customer_data:
                    traffic_name = str(customer_data.get(col_name, '')).strip()
                    if traffic_name:
                        break
            
            if not traffic_name:
                print("[ERROR] Kolom Traffic tidak ditemukan di Excel atau kosong")
                print(f"[INFO] Kolom yang tersedia: {list(customer_data.keys())}")
            else:
                print(f"[DEBUG] Traffic dari Excel: '{traffic_name}'")
                
                # Cari traffic_id dengan case-insensitive dan handle whitespace
                traffic_id = None
                matched_key = None
                
                # Coba exact match dulu
                if traffic_name in mappings['traffic']:
                    traffic_id = mappings['traffic'][traffic_name]
                    matched_key = traffic_name
                else:
                    # Coba case-insensitive match
                    for key, value in mappings['traffic'].items():
                        if key.strip().lower() == traffic_name.lower():
                            traffic_id = value
                            matched_key = key
                            print(f"[INFO] Traffic ditemukan dengan case-insensitive: '{key}'")
                            break
                
                if traffic_id:
                    try:
                        # Selector seperti Playwright: #data-form select[name="traffic_id"]
                        traffic_selector = "#data-form select[name=\"traffic_id\"]"
                        traffic_select_element = wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, traffic_selector))
                        )
                        # Scroll ke dropdown box supaya terlihat dan bisa diklik
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", traffic_select_element)
                        time.sleep(0.5)
                        
                        # Klik mouse ke dropdown box Traffic (simulasi user klik)
                        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, traffic_selector)))
                        ActionChains(self.driver).move_to_element(traffic_select_element).click().perform()
                        time.sleep(0.5)
                        
                        # selectOption(value) seperti Playwright -> Selenium: select_by_value
                        traffic_select = Select(traffic_select_element)
                        traffic_select.select_by_value(str(traffic_id))
                        time.sleep(0.5)
                        
                        # Trigger change event agar form mendeteksi pilihan
                        self.driver.execute_script("""
                            var select = document.querySelector('#data-form select[name="traffic_id"]');
                            if (select) {
                                var ev = new Event('change', { bubbles: true });
                                select.dispatchEvent(ev);
                                if (typeof jQuery !== 'undefined') jQuery(select).trigger('change');
                            }
                        """)
                        time.sleep(0.3)
                        
                        # Cek apakah halaman pakai Select2 (kalau iya, sync UI)
                        is_select2 = self.driver.execute_script("""
                            var select = document.querySelector('#data-form select[name="traffic_id"]');
                            if (!select) return false;
                            // Cek apakah ada Select2 instance
                            if (typeof jQuery !== 'undefined') {
                                var $select = jQuery(select);
                                return $select.data('select2') !== undefined;
                            }
                            // Cek apakah ada span.select2-container di sekitar select
                            var parent = select.parentElement;
                            while (parent) {
                                if (parent.querySelector && parent.querySelector('.select2-container')) {
                                    return true;
                                }
                                parent = parent.parentElement;
                            }
                            return false;
                        """)
                        
                        if is_select2:
                            print(f"[DEBUG] Traffic menggunakan Select2, menggunakan method Select2...")
                            # Method untuk Select2
                            success = self.driver.execute_script(f"""
                                (function() {{
                                    var select = document.querySelector('#data-form select[name="traffic_id"]');
                                    if (!select) return false;
                                    
                                    // Set value di select asli
                                    select.value = '{traffic_id}';
                                    select.selectedIndex = Array.from(select.options).findIndex(opt => opt.value == '{traffic_id}');
                                    
                                    // Update Select2 via jQuery
                                    if (typeof jQuery !== 'undefined') {{
                                        var $select = jQuery(select);
                                        $select.val('{traffic_id}').trigger('change');
                                        
                                        // Jika ada Select2 instance, update juga
                                        var select2Instance = $select.data('select2');
                                        if (select2Instance) {{
                                            select2Instance.trigger('select', {{
                                                data: {{
                                                    id: '{traffic_id}',
                                                    text: select.options[select.selectedIndex].text
                                                }}
                                            }});
                                        }}
                                    }}
                                    
                                    // Trigger events
                                    ['change', 'input'].forEach(function(eventType) {{
                                        var event = new Event(eventType, {{ bubbles: true }});
                                        select.dispatchEvent(event);
                                    }});
                                    
                                    return select.value == '{traffic_id}';
                                }})();
                            """)
                            time.sleep(1)
                        else:
                            print(f"[DEBUG] Traffic menggunakan select biasa, menggunakan method standard...")
                            # Method untuk select biasa (sama seperti Bank yang berhasil)
                            traffic_select = Select(traffic_select_element)
                            traffic_select.select_by_value(traffic_id)
                            time.sleep(0.5)
                            
                            # Trigger events untuk memastikan
                            self.driver.execute_script(f"""
                                var select = document.querySelector('#data-form select[name="traffic_id"]');
                                if (select) {{
                                    var event = new Event('change', {{ bubbles: true }});
                                    select.dispatchEvent(event);
                                    if (typeof jQuery !== 'undefined') {{
                                        jQuery(select).trigger('change');
                                    }}
                                }}
                            """)
                            time.sleep(0.3)
                        
                        # Verifikasi
                        traffic_select = Select(traffic_select_element)
                        selected_option = traffic_select.first_selected_option
                        selected_value = selected_option.get_attribute('value')
                        
                        if selected_value == traffic_id:
                            print(f"[OK] Traffic: {traffic_name} -> {matched_key} (ID: {traffic_id})")
                            print(f"[OK] Traffic berhasil dipilih: {selected_option.text}")
                        else:
                            print(f"[WARNING] Traffic mungkin tidak terpilih dengan benar")
                            print(f"[DEBUG] Expected: {traffic_id}, Got: {selected_value}")
                            print(f"[INFO] Mencoba sekali lagi dengan JavaScript langsung...")
                            
                            # Last attempt: JavaScript langsung
                            self.driver.execute_script(f"""
                                var select = document.querySelector('#data-form select[name="traffic_id"]');
                                if (select) {{
                                    select.value = '{traffic_id}';
                                    select.selectedIndex = Array.from(select.options).findIndex(opt => opt.value == '{traffic_id}');
                                    
                                    // Set selected attribute
                                    for (var i = 0; i < select.options.length; i++) {{
                                        select.options[i].selected = (select.options[i].value == '{traffic_id}');
                                    }}
                                    
                                    // Trigger events
                                    var events = ['change', 'input', 'blur'];
                                    events.forEach(function(eventType) {{
                                        var event = new Event(eventType, {{ bubbles: true, cancelable: true }});
                                        select.dispatchEvent(event);
                                    }});
                                    
                                    // jQuery
                                    if (typeof jQuery !== 'undefined') {{
                                        jQuery(select).val('{traffic_id}').trigger('change');
                                    }}
                                }}
                            """)
                            time.sleep(0.8)
                            
                            # Final verification
                            traffic_select = Select(traffic_select_element)
                            final_selected = traffic_select.first_selected_option.get_attribute('value')
                            if final_selected == traffic_id:
                                print(f"[OK] Traffic akhirnya berhasil dipilih!")
                            else:
                                print(f"[ERROR] Traffic GAGAL dipilih setelah semua method")
                                print(f"[DEBUG] Final check - Expected: {traffic_id}, Got: {final_selected}")
                                print(f"[INFO] Value di select: {traffic_select_element.get_attribute('value')}")
                                print(f"[INFO] Selected index: {traffic_select_element.get_attribute('selectedIndex')}")
                    except Exception as e:
                        print(f"[ERROR] Error saat select Traffic: {str(e)}")
                        import traceback
                        traceback.print_exc()
                else:
                    print(f"[WARNING] Traffic '{traffic_name}' tidak ditemukan di mapping")
                    print(f"[INFO] Traffic yang tersedia di mapping:")
                    for key, value in sorted(mappings['traffic'].items()):
                        print(f"    - {key} (ID: {value})")
            time.sleep(0.5)
            
            # 5. Bank
            print("Mengisi Bank...")
            bank_name = str(customer_data.get('Bank', '')).strip()
            
            # Cari bank_id dengan case-insensitive dan handle whitespace
            bank_id = None
            # Coba exact match dulu
            if bank_name in mappings['bank']:
                bank_id = mappings['bank'][bank_name]
            else:
                # Coba case-insensitive match
                for key, value in mappings['bank'].items():
                    if key.strip().lower() == bank_name.lower():
                        bank_id = value
                        print(f"[INFO] Bank ditemukan dengan case-insensitive: '{key}'")
                        break
            
            if bank_id:
                try:
                    # Cari select element dan scroll ke element
                    bank_select_element = wait.until(
                        EC.presence_of_element_located((By.NAME, "bank_id"))
                    )
                    # Scroll ke element
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", bank_select_element)
                    time.sleep(0.3)
                    
                    # Method 1: Gunakan Selenium Select langsung
                    bank_select = Select(bank_select_element)
                    bank_select.select_by_value(bank_id)
                    time.sleep(0.5)
                    
                    # Verifikasi
                    selected_option = bank_select.first_selected_option
                    selected_value = selected_option.get_attribute('value')
                    
                    if selected_value == bank_id:
                        print(f"[OK] Bank: {bank_name} (ID: {bank_id})")
                        print(f"[OK] Bank berhasil dipilih: {selected_option.text}")
                    else:
                        # Method 2: JavaScript dengan selectedIndex
                        self.driver.execute_script(f"""
                            var select = document.querySelector('select[name="bank_id"]');
                            if (select) {{
                                for (var i = 0; i < select.options.length; i++) {{
                                    if (select.options[i].value == '{bank_id}') {{
                                        select.selectedIndex = i;
                                        select.value = '{bank_id}';
                                        break;
                                    }}
                                }}
                                var events = ['change', 'input', 'blur', 'focus'];
                                events.forEach(function(eventType) {{
                                    var event = new Event(eventType, {{ bubbles: true, cancelable: true }});
                                    select.dispatchEvent(event);
                                }});
                                if (typeof jQuery !== 'undefined') {{
                                    jQuery(select).val('{bank_id}').trigger('change');
                                }}
                            }}
                        """)
                        time.sleep(0.5)
                        
                        # Verifikasi lagi
                        bank_select = Select(bank_select_element)
                        selected_option = bank_select.first_selected_option
                        selected_value = selected_option.get_attribute('value')
                        if selected_value == bank_id:
                            print(f"[OK] Bank berhasil dipilih dengan JavaScript: {selected_option.text}")
                        else:
                            print(f"[WARNING] Bank mungkin tidak terpilih dengan benar")
                except Exception as e:
                    print(f"[ERROR] Error saat select Bank: {str(e)}")
            else:
                print(f"[WARNING] Bank '{bank_name}' tidak ditemukan di mapping")
                print(f"[INFO] Bank yang tersedia: {list(mappings['bank'].keys())}")
            time.sleep(0.5)
            
            # 6. Bank Account Name
            print("Mengisi Bank Account Name...")
            bank_account_name_field = self.driver.find_element(By.NAME, "bank_account")
            bank_account_name_field.clear()
            bank_account_name = customer_data.get('Bank Account Name', '')
            # Handle NaN dan nilai kosong - jika kosong/NaN, biarkan field kosong
            if pd.isna(bank_account_name) or (isinstance(bank_account_name, str) and bank_account_name.strip() == ''):
                bank_account_name_value = ''
                print(f"[OK] Bank Account Name: (kosong - tidak diisi)")
            else:
                bank_account_name_value = str(bank_account_name).strip()
                bank_account_name_field.send_keys(bank_account_name_value)
                print(f"[OK] Bank Account Name: {bank_account_name_value}")
            time.sleep(0.5)
            
            # 7. Bank Account Number
            print("Mengisi Bank Account Number...")
            bank_account_number_field = self.driver.find_element(By.NAME, "bank_account_number")
            bank_account_number_field.clear()
            bank_account_number = customer_data.get('Account No', '')
            # Handle NaN dan nilai kosong - jika kosong/NaN, biarkan field kosong
            if pd.isna(bank_account_number) or (isinstance(bank_account_number, str) and bank_account_number.strip() == ''):
                bank_account_number_value = ''
                print(f"[OK] Bank Account Number: (kosong - tidak diisi)")
            else:
                bank_account_number_value = str(bank_account_number).strip()
                bank_account_number_field.send_keys(bank_account_number_value)
                print(f"[OK] Bank Account Number: {bank_account_number_value}")
            time.sleep(0.5)
            
            print("[OK] Semua field berhasil diisi!")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error mengisi form: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def submit_form(self):
        """Submit form register
        Returns: 
            'success' - Register berhasil
            'duplicate' - Customer sudah pernah register (masih di popup)
            'failed' - Register gagal dengan error
        """
        try:
            print("\n" + "=" * 50)
            print("SUBMIT FORM")
            print("=" * 50)
            
            wait = WebDriverWait(self.driver, 10)
            
            # Cari button Submit
            submit_button = wait.until(
                EC.element_to_be_clickable((By.ID, "btn-submit"))
            )
            submit_button.click()
            print("[OK] Button Submit diklik")
            
            # Tunggu response (success atau error)
            time.sleep(3)
            
            # Cek apakah ada success message atau error
            try:
                # Cek alert success
                success_alerts = self.driver.find_elements(By.CSS_SELECTOR, ".alert-success, .alert.alert-success")
                if success_alerts:
                    success_text = success_alerts[0].text
                    print(f"[OK] Register berhasil: {success_text}")
                    return 'success'
                
                # Cek alert error
                error_alerts = self.driver.find_elements(By.CSS_SELECTOR, ".alert-danger, .alert-error, .alert.alert-danger")
                if error_alerts:
                    error_text = error_alerts[0].text
                    print(f"[ERROR] Register gagal: {error_text}")
                    return 'failed'
                
                # Cek apakah form masih terbuka (berarti mungkin duplicate atau error)
                try:
                    username_field = self.driver.find_element(By.NAME, "username")
                    # Jika form masih ada, kemungkinan customer sudah pernah register
                    print("[WARNING] Form masih terbuka setelah submit")
                    print("[INFO] Kemungkinan customer sudah pernah register")
                    return 'duplicate'
                except:
                    # Modal tertutup, kemungkinan berhasil
                    print("[OK] Modal tertutup, register kemungkinan berhasil")
                    return 'success'
                    
            except Exception as e:
                print(f"[INFO] Tidak dapat menentukan status: {str(e)}")
                # Cek apakah form masih ada
                try:
                    self.driver.find_element(By.NAME, "username")
                    return 'duplicate'
                except:
                    return 'success'
                
        except Exception as e:
            print(f"[ERROR] Error submit form: {str(e)}")
            return 'failed'
    
    def close_modal(self):
        """Tutup modal dengan klik Exit button (×)"""
        try:
            print("Menutup modal...")
            wait = WebDriverWait(self.driver, 5)
            
            # Cari button close/exit
            close_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close[data-dismiss='modal'], button.close.pull-right"))
            )
            
            # Coba klik normal dulu
            try:
                close_button.click()
            except:
                # Jika gagal, gunakan JavaScript
                self.driver.execute_script("arguments[0].click();", close_button)
            
            print("[OK] Modal ditutup")
            time.sleep(1)
            return True
            
        except Exception as e:
            print(f"[WARNING] Tidak dapat menutup modal: {str(e)}")
            # Coba cara lain - tekan ESC atau klik backdrop
            try:
                # Tekan ESC key
                from selenium.webdriver.common.keys import Keys
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                time.sleep(1)
                return True
            except:
                return False
    
    def register_customer(self, customer_data, mappings):
        """Register satu customer (full flow)
        Returns:
            'success' - Register berhasil
            'duplicate' - Customer sudah pernah register
            'failed' - Register gagal
        """
        # Navigate ke Member Add
        if not self.navigate_to_member_add():
            return 'failed'
        
        # Fill form
        if not self.fill_register_form(customer_data, mappings):
            return 'failed'
        
        # Submit
        submit_result = self.submit_form()
        
        # Handle duplicate (customer sudah pernah register)
        if submit_result == 'duplicate':
            # Tutup modal
            self.close_modal()
            # Set flag bahwa masih di halaman Member (tidak perlu navigate lagi)
            self.is_on_member_page = True
            return 'duplicate'
        
        # Jika success atau failed, tutup modal juga jika masih terbuka
        if submit_result == 'success':
            # Tunggu sebentar untuk memastikan modal tertutup
            time.sleep(1)
            try:
                # Cek apakah modal masih terbuka
                self.driver.find_element(By.NAME, "username")
                # Jika masih ada, tutup
                self.close_modal()
            except:
                # Modal sudah tertutup, tidak perlu tutup
                pass
            # Set flag bahwa masih di halaman Member (tidak perlu navigate lagi)
            self.is_on_member_page = True
        
        return submit_result
    
    def register_from_excel(self, excel_file, username, password, batch_size=15):
        """Register multiple customers dari Excel file. Setiap batch (10-15 record) disimpan ke customers_results.xlsx."""
        RESULTS_FILE = 'customers_results.xlsx'
        try:
            print("=" * 50)
            print("AUTO REGISTER CUSTOMER DARI EXCEL")
            print("=" * 50)
            print(f"[INFO] Per batch: {batch_size} record, simpan ke: {RESULTS_FILE}")
            
            # Load Excel
            print(f"\nMembaca file Excel: {excel_file}")
            df = pd.read_excel(excel_file)
            print(f"[OK] Excel loaded: {len(df)} rows")
            print(f"Columns: {list(df.columns)}")
            
            # Load mappings
            mappings = self.load_mappings()
            
            # Login
            if not self.login(username, password):
                print("[ERROR] Login gagal, tidak dapat melanjutkan")
                return
            
            # Register setiap customer
            results = []
            total = len(df)
            batch_num = 1
            
            for index, row in df.iterrows():
                print(f"\n{'='*50}")
                print(f"PROSES {index + 1}/{total}")
                print(f"{'='*50}")
                
                customer_data = row.to_dict()
                
                try:
                    result = self.register_customer(customer_data, mappings)
                    
                    # Tentukan status berdasarkan result
                    if result == 'success':
                        status = 'Success'
                        print(f"[OK] Customer {index + 1} berhasil diregister")
                    elif result == 'duplicate':
                        status = 'Duplicate (Already Registered)'
                        print(f"[WARNING] Customer {index + 1} sudah pernah register, di-skip")
                    else:
                        status = 'Failed'
                        print(f"[ERROR] Customer {index + 1} gagal diregister")
                    
                    results.append({
                        'Row': index + 1,
                        'Username': customer_data.get('Username', ''),
                        'Status': status
                    })
                    
                    # Setiap batch (10-15 record): save ke customers_results.xlsx lalu lanjut
                    if len(results) % batch_size == 0:
                        results_df = pd.DataFrame(results)
                        results_df.to_excel(RESULTS_FILE, index=False, engine='openpyxl')
                        print(f"\n[OK] Batch {batch_num} ({len(results)} record) disimpan ke: {RESULTS_FILE}")
                        batch_num += 1
                    
                    # Tunggu sebelum customer berikutnya
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"[ERROR] Error register customer {index + 1}: {str(e)}")
                    results.append({
                        'Row': index + 1,
                        'Username': customer_data.get('Username', ''),
                        'Status': f'Error: {str(e)}'
                    })
                    # Tetap save per batch meski error
                    if len(results) % batch_size == 0:
                        results_df = pd.DataFrame(results)
                        results_df.to_excel(RESULTS_FILE, index=False, engine='openpyxl')
                        print(f"\n[OK] Batch {batch_num} ({len(results)} record) disimpan ke: {RESULTS_FILE}")
                        batch_num += 1
            
            # Summary
            print("\n" + "=" * 50)
            print("SUMMARY REGISTRATION")
            print("=" * 50)
            success_count = sum(1 for r in results if r['Status'] == 'Success')
            duplicate_count = sum(1 for r in results if 'Duplicate' in r['Status'])
            failed_count = sum(1 for r in results if r['Status'] == 'Failed')
            
            print(f"Total: {total}")
            print(f"Success: {success_count}")
            print(f"Duplicate (Skipped): {duplicate_count}")
            print(f"Failed: {failed_count}")
            
            # Save results akhir (semua record) ke customers_results.xlsx
            if results:
                results_df = pd.DataFrame(results)
                results_df.to_excel(RESULTS_FILE, index=False, engine='openpyxl')
                print(f"\n[OK] Results final disimpan ke: {RESULTS_FILE}")
            
        except Exception as e:
            print(f"[ERROR] Error: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            if self.driver:
                print("\nBrowser akan ditutup dalam 5 detik...")
                time.sleep(5)
                self.login_handler.close()


if __name__ == "__main__":
    # Configuration
    EXCEL_FILE = "customers.xlsx"  # Ganti dengan nama file Excel Anda
    USERNAME = "sbmycrmoperation"
    PASSWORD = "wvWNsyo8UmcX"
    BATCH_SIZE = 15  # Setiap 10-15 record disimpan ke customers_results.xlsx, lalu lanjut

    register = CustomerRegister()
    register.register_from_excel(EXCEL_FILE, USERNAME, PASSWORD, batch_size=BATCH_SIZE)
