from flask import Flask, render_template, request
from datetime import datetime
from bs4 import BeautifulSoup
import requests

# Function to scrape exchange rate from Mandiri
def scrape_mandiri():
    url = "https://www.bankmandiri.co.id/kurs"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')

        if not table:
            return None

        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) > 0 and 'MYR' in cells[0].text:
                nilai_beli = float(cells[3].text.strip().replace('.', '').replace(',', '.'))
                nilai_jual = float(cells[4].text.strip().replace('.', '').replace(',', '.'))
                rata_rata = (nilai_beli + nilai_jual) / 2
                return "{:,.2f}".format(rata_rata).replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return None

# Function to scrape exchange rate from BRI
def scrape_bri():
    url = "https://bri.co.id/kurs-detail"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.88 Safari/537.36'
    }
    try:
        # Tambahkan headers untuk menghindari 403 Forbidden
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Cari elemen <span> berdasarkan class MYR
        span = soup.find('span', class_='flagico flag-MYR_Malaysia')

        if not span:
            print("Elemen <span> untuk MYR tidak ditemukan.")
            return None

        # Cari tabel setelah elemen <span>
        row = span.find_parent('tr')

        if not row:
            print("Baris induk untuk MYR tidak ditemukan.")
            return None

        # Ambil semua kolom (td) dalam baris
        cells = row.find_all('td')

        if len(cells) >= 3:
            # Ambil nilai beli dan jual
            nilai_beli = float(cells[1].get_text().strip().replace('.', '').replace(',', '.'))
            nilai_jual = float(cells[2].get_text().strip().replace('.', '').replace(',', '.'))

            # Hitung rata-rata
            rata_rata = (nilai_beli + nilai_jual) / 2

            # Format hasil
            return "{:,.2f}".format(rata_rata).replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            print("Data nilai beli dan jual tidak lengkap.")
            return None

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None
    
# Function to scrape exchange rate from BCA
def scrape_bca():
    url = "https://www.bca.co.id/id/informasi/kurs"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')

        if not table:
            return None

        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) > 0 and 'MYR' in cells[0].text:
                nilai_beli = float(cells[3].text.strip().replace('.', '').replace(',', '.'))
                nilai_jual = float(cells[4].text.strip().replace('.', '').replace(',', '.'))
                rata_rata = (nilai_beli + nilai_jual) / 2
                return "{:,.2f}".format(rata_rata).replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return None

# Function to scrape exchange rate from BNI
def scrape_bni():
    url = "https://www.bni.co.id/id-id/beranda/informasi-valas"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Cari elemen <span> berdasarkan id
        span = soup.find('span', id='dnn_ctr6793_BNIValasInfoView_lblTitleBankNotes')

        if not span:
            print("Elemen <span> tidak ditemukan.")
            return None

        # Cari tabel setelah elemen <span> jika ada
        table = span.find_next('table', class_='table table-striped angrid-grid table_info_counter')

        if not table:
            print("Tabel tidak ditemukan setelah elemen <span>.")
            return None

        # Iterasi baris dalam tabel
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) > 0:
                # Cek apakah baris berisi MYR
                if 'MYR' in cells[0].get_text():
                    nilai_beli = float(cells[1].get_text().strip().replace('.', '').replace(',', '.'))
                    nilai_jual = float(cells[2].get_text().strip().replace('.', '').replace(',', '.'))
                    rata_rata = (nilai_beli + nilai_jual) / 2
                    return "{:,.2f}".format(rata_rata).replace(",", "X").replace(".", ",").replace("X", ".")
                    
        print("MYR tidak ditemukan dalam tabel.")
        return None

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None

# Function to scrape exchange rate from Maybank
def scrape_maybank():
    url = "https://www.maybank.co.id/Business/forexrate"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')

        if not table:
            return None

        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) > 0 and 'MYR' in cells[0].text:
                nilai_beli = float(cells[3].text.strip().replace('.', '').replace(',', '.'))
                nilai_jual = float(cells[4].text.strip().replace('.', '').replace(',', '.'))
                rata_rata = (nilai_beli + nilai_jual) / 2
                return "{:,.2f}".format(rata_rata).replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return None

# Function to scrape exchange rate from CIMB Niaga
def scrape_cimb():
    url = "https://www.cimbniaga.co.id/id/personal/index"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Cari elemen <td> untuk MYR
        myr_cell = soup.find(lambda tag: tag.name == 'td' and 'MYR' in tag.get_text())


        if not myr_cell:
            return None

        # Temukan parent <tr> untuk mengambil data terkait
        row = myr_cell.find_parent('tr')

        # Cari elemen td2 (nilai beli) dan td3 (nilai jual) di dalam baris yang sama
        nilai_beli_cell = row.find('td', class_='td2')
        nilai_jual_cell = row.find('td', class_='td3')

        if not nilai_beli_cell or not nilai_jual_cell:
            print("Nilai beli atau jual tidak ditemukan.")
            return None

        # Konversi format angka dari pemisah ribuan dan desimal
        nilai_beli_str = nilai_beli_cell.get_text().strip().replace(',', 'X').replace('.', ',').replace('X', '.')
        nilai_jual_str = nilai_jual_cell.get_text().strip().replace(',', 'X').replace('.', ',').replace('X', '.')

        # Konversi string ke float
        nilai_beli = float(nilai_beli_str.replace('.', '').replace(',', '.'))
        nilai_jual = float(nilai_jual_str.replace('.', '').replace(',', '.'))

        # Hitung rata-rata
        rata_rata = (nilai_beli + nilai_jual) / 2

        # Format hasil kembali ke pemisah ribuan (.) dan desimal (,)
        return "{:,.2f}".format(rata_rata).replace(",", "X").replace(".", ",").replace("X", ".")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None
    
# Function to scrape exchange rate from MUFG
def scrape_mufg():
    url = "https://www.mufg.co.id/charges/today-exchange-rates"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')

        if not table:
            return None

        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) > 0 and 'MYR' in cells[0].text:
                # Konversi format angka dari pemisah ribuan (,) ke (.) dan pemisah desimal (.) ke (,)
                nilai_beli_str = cells[1].text.strip().replace(',', 'X').replace('.', ',').replace('X', '.')
                nilai_jual_str = cells[2].text.strip().replace(',', 'X').replace('.', ',').replace('X', '.')

                # Konversi string ke float
                nilai_beli = float(nilai_beli_str.replace('.', '').replace(',', '.'))
                nilai_jual = float(nilai_jual_str.replace('.', '').replace(',', '.'))
                
                # Menghitung rata-rata
                rata_rata = (nilai_beli + nilai_jual) / 2

                # Format kembali ke pemisah ribuan (.) dan desimal (,)
                return "{:,.2f}".format(rata_rata).replace(",", "X").replace(".", ",").replace("X", ".")

    except Exception as e:
        return None

# Function to scrape exchange rate from HSBC
def scrape_hsbc():
    url = "https://www.hsbc.co.id/1/2/id/personal/foreign-exchange/real-time-fx-rates#banknote-rates"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')

        if not table:
            return None

        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) > 0 and 'MYR' in cells[0].text:
                nilai_beli = float(cells[3].text.strip().replace('.', '').replace(',', '.'))
                nilai_jual = float(cells[4].text.strip().replace('.', '').replace(',', '.'))
                rata_rata = (nilai_beli + nilai_jual) / 2
                return "{:,.2f}".format(rata_rata).replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return None   

def get_exchange_rates():
    return {
        "Mandiri": scrape_mandiri() or 'NONE',
        "BRI": scrape_bri() or 'NONE',
        "BCA": scrape_bca() or 'NONE',
        "BNI": scrape_bni() or 'NONE',
        "Maybank": scrape_maybank() or 'NONE',
        "CIMB Niaga": scrape_cimb() or 'NONE',
        "MUFG": scrape_mufg() or 'NONE',
        "HSBC": scrape_hsbc() or 'NONE'
    }

# Running each function separately
print(f"Mandiri: {scrape_mandiri() or 'NONE'}")
print(f"BRI: {scrape_bri() or 'NONE'}")
print(f"BCA: {scrape_bca() or 'NONE'}")
print(f"BNI: {scrape_bni() or 'NONE'}")
print(f"Maybank: {scrape_maybank() or 'NONE'}")
print(f"CIMB Niaga: {scrape_cimb() or 'NONE'}")
print(f"MUFG: {scrape_mufg() or 'NONE'}")
print(f"HSBC: {scrape_hsbc() or 'NONE'}")
