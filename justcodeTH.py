from flask import Flask, render_template, request
from datetime import datetime
from bs4 import BeautifulSoup
import requests

# Function to scrape exchange rate from Mandiri
def scrape_mandiriTH():
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
            if len(cells) > 0 and 'THB' in cells[0].text:
                nilai_beli = float(cells[3].text.strip().replace('.', '').replace(',', '.'))
                nilai_jual = float(cells[4].text.strip().replace('.', '').replace(',', '.'))
                rata_rata = (nilai_beli + nilai_jual) / 2
                return "{:,.2f}".format(rata_rata).replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return None

# Function to scrape exchange rate from BRI
def scrape_briTH():
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
        span = soup.find('span', class_='flagico flag-THB_Thailand')

        if not span:
            print("Elemen <span> untuk THB tidak ditemukan.")
            return None

        # Cari tabel setelah elemen <span>
        row = span.find_parent('tr')

        if not row:
            print("Baris induk untuk THB tidak ditemukan.")
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

# Running each function separately
print(f"Mandiri: {scrape_mandiriTH() or 'NONE'}")
print(f"BRI: {scrape_briTH() or 'NONE'}")
