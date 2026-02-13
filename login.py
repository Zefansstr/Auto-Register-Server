import requests
from bs4 import BeautifulSoup
# BeautifulSoup akan menggunakan html.parser (built-in, tidak perlu lxml)
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

class DashboardLogin:
    def __init__(self, base_url="https://hwbo88v2.com"):
        self.base_url = base_url
        self.login_url = f"{base_url}/op/login"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.is_logged_in = False
    
    def login(self, username, password):
        """
        Login ke dashboard dengan username dan password
        Returns: True jika berhasil, False jika gagal
        """
        try:
            # Step 1: Ambil halaman login untuk mendapatkan CSRF token atau session cookies
            print(f"Mengakses halaman login: {self.login_url}")
            response = self.session.get(self.login_url)
            response.raise_for_status()
            
            # Parse HTML untuk mendapatkan form data dan CSRF token jika ada
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Cari CSRF token jika ada
            csrf_token = None
            csrf_input = soup.find('input', {'name': ['_token', 'csrf_token', 'csrf-token']})
            if csrf_input:
                csrf_token = csrf_input.get('value')
            
            # Step 2: Siapkan data untuk login
            login_data = {
                'username': username,
                'password': password
            }
            
            # Tambahkan CSRF token jika ada
            if csrf_token:
                login_data['_token'] = csrf_token
            
            # Step 3: Coba beberapa kemungkinan endpoint login
            # Beberapa website menggunakan endpoint berbeda untuk login
            possible_endpoints = [
                self.login_url,
                f"{self.base_url}/op/login/submit",
                f"{self.base_url}/op/auth/login",
                f"{self.base_url}/api/login",
            ]
            
            print(f"Melakukan login dengan username: {username}")
            
            for endpoint in possible_endpoints:
                try:
                    print(f"  Mencoba endpoint: {endpoint}")
                    # Coba dengan POST data
                    login_response = self.session.post(
                        endpoint,
                        data=login_data,
                        allow_redirects=True,
                        timeout=10
                    )
                    
                    print(f"  Status code: {login_response.status_code}")
                    print(f"  Final URL: {login_response.url}")
                    
                    # Cek response
                    if login_response.status_code in [200, 302]:
                        # Cek apakah redirect atau masih di login page
                        final_url = login_response.url
                        
                        # Jika redirect ke halaman selain login, kemungkinan berhasil
                        if '/op/login' not in final_url:
                            self.is_logged_in = True
                            print(f"[OK] Login berhasil! Redirect ke: {final_url}")
                            return True
                        
                        # Jika masih di login page, cek apakah ada error
                        if '/op/login' in final_url:
                            soup_check = BeautifulSoup(login_response.text, 'html.parser')
                            # Cari berbagai kemungkinan error message
                            error_selectors = [
                                {'class': ['alert', 'alert-danger', 'alert-error']},
                                {'class': ['error', 'error-message']},
                                {'id': ['error', 'error-message']},
                            ]
                            
                            for selector in error_selectors:
                                error_elem = soup_check.find(**selector)
                                if error_elem:
                                    error_text = error_elem.get_text(strip=True)
                                    if error_text:
                                        print(f"[ERROR] Login gagal: {error_text}")
                                        return False
                            
                            # Jika endpoint pertama gagal, coba endpoint berikutnya
                            if endpoint != possible_endpoints[-1]:
                                print("  Endpoint ini gagal, mencoba endpoint berikutnya...")
                                continue
                            else:
                                print("[ERROR] Login gagal: Masih berada di halaman login")
                                print("[INFO] Form login mungkin memerlukan JavaScript. Coba gunakan login_selenium.py")
                                return False
                
                except requests.exceptions.RequestException as e:
                    # Jika endpoint ini error, coba endpoint berikutnya
                    print(f"  Endpoint error: {str(e)}")
                    if endpoint != possible_endpoints[-1]:
                        continue
            
            # Jika semua endpoint gagal
            print("[ERROR] Login gagal: Tidak dapat mengakses endpoint login")
            return False
                
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Error saat login: {str(e)}")
            return False
    
    def check_login_status(self):
        """
        Cek apakah masih login dengan mengakses halaman yang memerlukan authentication
        """
        try:
            # Coba akses halaman dashboard atau protected page
            dashboard_url = f"{self.base_url}/op/dashboard"  # Adjust sesuai endpoint dashboard
            response = self.session.get(dashboard_url)
            
            if response.status_code == 200 and '/op/login' not in response.url:
                return True
            return False
        except:
            return False
    
    def get_session(self):
        """
        Return session object untuk digunakan di request berikutnya
        """
        return self.session if self.is_logged_in else None
    
    def logout(self):
        """
        Logout dari dashboard
        """
        try:
            logout_url = f"{self.base_url}/op/logout"
            self.session.get(logout_url)
            self.is_logged_in = False
            print("Logout berhasil")
        except:
            pass


if __name__ == "__main__":
    # Test login
    dashboard = DashboardLogin()
    
    username = "sbmycrmoperation"
    password = "wvWNsyo8UmcX"
    
    success = dashboard.login(username, password)
    
    if success:
        print("\n[OK] Session login berhasil dibuat!")
        print(f"Cookies: {len(dashboard.session.cookies)} cookies tersimpan")
        
        # Test check login status
        if dashboard.check_login_status():
            print("[OK] Status login: Masih aktif")
        else:
            print("[WARNING] Status login: Perlu verifikasi manual")
    else:
        print("\n[ERROR] Login gagal, silakan cek credentials atau network connection")
