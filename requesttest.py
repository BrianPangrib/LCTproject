import requests
from bs4 import BeautifulSoup

# URLs untuk login dan scraping
login_url = 'https://login.bloomberg.com/api/login/bconnect'
secure_url = 'https://login.bloomberg.com/api/account/current-user'
scrape_url = 'https://www.bloomberg.com/quote/MYRIDR:CUR'

# Data login
payload = {
    'username': 'syafira_a@bi.go.id',
    'password': 'Perpus123*#'
}

# Headers untuk meniru browser asli
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.88 Safari/537.36',
    'Referer': 'https://www.bloomberg.com/',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

# Mulai session
with requests.Session() as session:
    try:
        
        login_response = session.post(login_url, data=payload, headers=headers)

        if login_response.status_code != 200:
            print(f"Login gagal. Status code: {login_response.status_code}")
        else:
            print("Login berhasil!")

            
            secure_response = session.get(secure_url, headers=headers)
            if secure_response.status_code == 200:
                print("Autentikasi berhasil, melanjutkan scraping...")

                
                scrape_response = session.get(scrape_url, headers=headers)
                soup = BeautifulSoup(scrape_response.text, 'html.parser')

                
                price_div = soup.find('div', {'data-component': 'sized-price'})

                if price_div:
                    price = price_div.get_text().strip()
                    print(f"Harga MYR/IDR: {price}")
                else:
                    print("Data harga tidak ditemukan di halaman.")

            else:
                print(f"Autentikasi gagal. Status code: {secure_response.status_code}")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
