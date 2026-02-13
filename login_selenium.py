"""
Alternatif login menggunakan Selenium untuk form yang memerlukan JavaScript
Install: pip install selenium
Selenium 4.x akan auto-download ChromeDriver
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import sys
import os

# Fix encoding untuk Windows console (dengan error handling yang lebih aman)
if sys.platform == 'win32':
    try:
        # Set console code page ke UTF-8
        os.system('chcp 65001 >nul 2>&1')
    except:
        pass

class DashboardLoginSelenium:
    def __init__(self, base_url="https://hwbo88v2.com", headless=False):
        self.base_url = base_url
        self.login_url = f"{base_url}/op/login"
        self.headless = headless
        self.driver = None
        self.is_logged_in = False
    
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User agent untuk terlihat seperti browser normal
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        try:
            # Selenium 4.x akan auto-download ChromeDriver jika tidak ada
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()
            return True
        except Exception as e:
            print(f"[ERROR] Error setup ChromeDriver: {str(e)}")
            print("[INFO] Pastikan Chrome browser sudah terinstall")
            print("[INFO] Selenium 4.x akan auto-download ChromeDriver")
            return False
    
    def login(self, username, password):
        """
        Login ke dashboard menggunakan Selenium
        Returns: True jika berhasil, False jika gagal
        """
        if not self.driver:
            if not self.setup_driver():
                return False
        
        try:
            print(f"Mengakses halaman login: {self.login_url}")
            self.driver.get(self.login_url)
            
            # Tunggu form login muncul
            wait = WebDriverWait(self.driver, 10)
            
            # Cari input username
            print("Mencari field username...")
            username_input = wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            # Cari input password
            print("Mencari field password...")
            password_input = self.driver.find_element(By.NAME, "password")
            
            # Input username dan password
            username_input.clear()
            username_input.send_keys(username)
            print(f"[OK] Username diisi: {username}")
            
            password_input.clear()
            password_input.send_keys(password)
            print("[OK] Password diisi")
            
            # Cari dan klik button login
            print("Mencari button login...")
            login_button = self.driver.find_element(By.ID, "m_login_signin_submit")
            
            # Klik button login
            login_button.click()
            print("[OK] Button login diklik")
            
            # Tunggu redirect atau perubahan halaman (maksimal 10 detik)
            try:
                # Tunggu sampai URL berubah atau ada error message
                wait.until(
                    lambda driver: '/op/login' not in driver.current_url or 
                    len(driver.find_elements(By.CLASS_NAME, "alert")) > 0 or
                    len(driver.find_elements(By.CSS_SELECTOR, "[class*='error']")) > 0 or
                    len(driver.find_elements(By.CSS_SELECTOR, "[class*='danger']")) > 0
                )
            except:
                # Jika timeout, lanjutkan pengecekan
                pass
            
            # Tunggu sedikit untuk memastikan halaman sudah load
            time.sleep(2)
            
            # Cek apakah login berhasil
            current_url = self.driver.current_url
            print(f"URL setelah login: {current_url}")
            
            # Cek berbagai kemungkinan error message
            error_found = False
            error_text = ""
            
            # Cek alert messages
            try:
                error_elements = self.driver.find_elements(By.CSS_SELECTOR, ".alert, .alert-danger, .alert-error, [class*='error'], [class*='danger']")
                if error_elements:
                    for elem in error_elements:
                        text = elem.text.strip()
                        if text:
                            error_text = text
                            error_found = True
                            break
            except:
                pass
            
            # Cek apakah masih di halaman login
            if '/op/login' in current_url:
                if error_found:
                    print(f"[ERROR] Login gagal: {error_text}")
                else:
                    # Cek page source untuk error message
                    page_source = self.driver.page_source.lower()
                    if 'invalid' in page_source or 'incorrect' in page_source or 'wrong' in page_source:
                        print("[ERROR] Login gagal: Credentials tidak valid")
                    else:
                        print("[ERROR] Login gagal: Masih berada di halaman login")
                        print("[INFO] Cek apakah credentials benar atau ada validasi tambahan")
                return False
            else:
                # Berhasil redirect, login sukses
                self.is_logged_in = True
                print("[OK] Login berhasil!")
                return True
                
        except Exception as e:
            print(f"[ERROR] Error saat login: {str(e)}")
            return False
    
    def get_cookies(self):
        """Ambil cookies dari session untuk digunakan di requests"""
        if self.driver and self.is_logged_in:
            return self.driver.get_cookies()
        return None
    
    def get_session_cookies_dict(self):
        """Convert cookies ke dictionary format untuk requests.Session"""
        cookies = self.get_cookies()
        if cookies:
            return {cookie['name']: cookie['value'] for cookie in cookies}
        return {}
    
    def close(self):
        """Tutup browser"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            print("Browser ditutup")


if __name__ == "__main__":
    # Test login dengan Selenium
    dashboard = DashboardLoginSelenium(headless=False)  # Set True untuk headless mode
    
    username = "sbmycrmoperation"
    password = "wvWNsyo8UmcX"
    
    try:
        success = dashboard.login(username, password)
        
        if success:
            print("\n[OK] Login berhasil dengan Selenium!")
            cookies = dashboard.get_session_cookies_dict()
            print(f"[OK] Cookies tersimpan: {len(cookies)} cookies")
            print(f"Cookie names: {list(cookies.keys())}")
            
            # Tunggu sebelum close (untuk testing)
            print("\nBrowser akan tetap terbuka selama 10 detik untuk verifikasi...")
            time.sleep(10)
        else:
            print("\n[ERROR] Login gagal")
    finally:
        dashboard.close()
