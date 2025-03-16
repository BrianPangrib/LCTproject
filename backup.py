import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO
import os

# ==========================
# 🔵 HSBC SETUP
# ==========================

# URL target HSBC
HSBC_URL = "https://www.hsbc.co.id/1/2/id/personal/foreign-exchange/real-time-fx-rates#banknote-rates"

# Path untuk file Excel HSBC
HSBC_EXCEL_PATH = r"Z:\kerjaan magang\LCT_HSBC.xlsx"

# Class tabel pada halaman HSBC
HSBC_TABLE_CLASS = "tdnaMob"

def scrape_hsbc_table():
    """Scrape tabel kurs dari halaman HSBC dan kembalikan sebagai DataFrame."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(HSBC_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Temukan tabel berdasarkan class
    table_element = soup.find("table", class_=HSBC_TABLE_CLASS)

    if table_element:
        table_io = StringIO(str(table_element))
        df = pd.read_html(table_io)[0]
        df["Tanggal Scraping"] = pd.Timestamp.now()  # Tambahkan kolom timestamp
        return df
    else:
        print(f"⚠️ Tabel tidak ditemukan di {HSBC_URL}")
        return None

def save_to_excel_hsbc(new_data, file_path):
    """Simpan data dari tabel HSBC ke file Excel, memperbarui data jika sudah ada."""
    if os.path.exists(file_path):
        existing_data = pd.read_excel(file_path, sheet_name="Kurs HSBC", engine="openpyxl")
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        combined_data = new_data

    with pd.ExcelWriter(file_path, engine="openpyxl", mode='w') as writer:
        # Flatten MultiIndex jika ada
        if isinstance(combined_data.columns, pd.MultiIndex):
            combined_data.columns = [' '.join(map(str, col)).strip() for col in combined_data.columns]

        # Bersihkan kolom kosong
        combined_data.dropna(axis=1, how='all', inplace=True)

        # Format kolom 'Tanggal Scraping'
        if 'Tanggal Scraping' in combined_data.columns:
            combined_data['Tanggal Scraping'] = pd.to_datetime(combined_data['Tanggal Scraping'])
        
        # Reset index agar tidak berantakan
        combined_data.reset_index(drop=True, inplace=True)

        # Simpan ke Excel
        combined_data.to_excel(writer, sheet_name="Kurs HSBC", index=False)

    print(f"✅ Data berhasil disimpan ke {file_path}")

def main_hsbc():
    """Fungsi utama untuk menjalankan scraping HSBC dan menyimpan data."""
    scraped_data = scrape_hsbc_table()
    if scraped_data is not None:
        save_to_excel_hsbc(scraped_data, HSBC_EXCEL_PATH)
    else:
        print("⚠️ Tidak ada data HSBC yang berhasil di-scrape.")

# ==========================
# 🟡 MAIN PROGRAM
# ==========================

if __name__ == "__main__":
    main_hsbc()
