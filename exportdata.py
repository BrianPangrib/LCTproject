import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO
import os

# ==========================
# 🟢 PERMATA BANK SETUP
# ==========================

# URL target Permata Bank
PERMATA_URL = "https://www.permatabank.com/en/kurs/nilai-tukar-mata-uang"

# Path untuk file Excel Permata Bank (Sesuaikan Direktori)
PERMATA_EXCEL_PATH = r"Z:\kerjaan magang\LCT_PERMATA.xlsx"

# ID Tabel Permata Bank
PERMATA_TABLE_ID = "forex"

def scrape_permata_tables():
    """Scrape tabel dari halaman Permata Bank."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(PERMATA_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tables_data = {}

    # Cari tabel berdasarkan ID
    table_element = soup.find("table", id=PERMATA_TABLE_ID)

    if table_element:
        table_io = StringIO(str(table_element))
        df = pd.read_html(table_io)[0]
        df["Tanggal Scraping"] = pd.Timestamp.now()  # Tambahkan kolom timestamp
        tables_data["Exchange Rates"] = df
    else:
        print("⚠️ Tabel Bank Permata tidak ditemukan!")

    return tables_data

def save_to_excel(tables_data, file_path):
    """Simpan data dari semua tabel ke file Excel, memperbarui data jika sudah ada."""
    if os.path.exists(file_path):
        existing_data = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")
    else:
        existing_data = {}

    with pd.ExcelWriter(file_path, engine="openpyxl", mode='w') as writer:
        for table_name, new_df in tables_data.items():
            if table_name in existing_data:
                combined_df = pd.concat([existing_data[table_name], new_df], ignore_index=True)
            else:
                combined_df = new_df

            # 🔴 FLATTEN MultiIndex jika ada
            if isinstance(combined_df.columns, pd.MultiIndex):
                combined_df.columns = [' '.join(map(str, col)).strip() for col in combined_df.columns]

            # ✅ Bersihkan kolom kosong
            combined_df.dropna(axis=1, how='all', inplace=True)

            # ✅ Format kolom 'Tanggal Scraping'
            if 'Tanggal Scraping' in combined_df.columns:
                combined_df['Tanggal Scraping'] = pd.to_datetime(combined_df['Tanggal Scraping'])
            
            # ✅ Reset index agar tidak berantakan
            combined_df.reset_index(drop=True, inplace=True)

            # ✅ Simpan ke Excel
            combined_df.to_excel(writer, sheet_name=table_name, index=False)

    print(f"✅ Data berhasil disimpan ke {file_path}")

def main_permata():
    """Fungsi utama untuk menjalankan scraping Permata Bank dan menyimpan data."""
    scraped_tables = scrape_permata_tables()
    if scraped_tables:
        save_to_excel(scraped_tables, PERMATA_EXCEL_PATH)
    else:
        print("⚠️ Tidak ada data Permata Bank yang berhasil di-scrape.")

# ==========================
# 🟢 DANAMON BANK SETUP
# ==========================

# URL target Bank Danamon
DANAMON_URL = "https://www.danamon.co.id/id/Kurs-Details"

# Path untuk file Excel Bank Danamon (Sesuai Direktori)
DANAMON_EXCEL_PATH = r"Z:\kerjaan magang\LCT_DANAMON.xlsx"

# Class tabel pada halaman Danamon
DANAMON_TABLE_CLASS = "clone cf hidden-md hidden-lg"

def scrape_danamon_tables():
    """Scrape tabel dari halaman Bank Danamon."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(DANAMON_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tables_data = {}

    # Cari tabel berdasarkan class
    table_element = soup.find("table", class_=DANAMON_TABLE_CLASS)

    if table_element:
        table_io = StringIO(str(table_element))
        df = pd.read_html(table_io)[0]
        df["Tanggal Scraping"] = pd.Timestamp.now()  # Tambahkan kolom timestamp
        tables_data["Exchange Rates"] = df
    else:
        print("⚠️ Tabel Bank Danamon tidak ditemukan!")

    return tables_data

def save_to_excel(tables_data, file_path):
    """Simpan data dari semua tabel ke file Excel, memperbarui data jika sudah ada."""
    if os.path.exists(file_path):
        existing_data = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")
    else:
        existing_data = {}

    with pd.ExcelWriter(file_path, engine="openpyxl", mode='w') as writer:
        for table_name, new_df in tables_data.items():
            if table_name in existing_data:
                combined_df = pd.concat([existing_data[table_name], new_df], ignore_index=True)
            else:
                combined_df = new_df

            # 🔴 FLATTEN MultiIndex jika ada
            if isinstance(combined_df.columns, pd.MultiIndex):
                combined_df.columns = [' '.join(map(str, col)).strip() for col in combined_df.columns]

            # ✅ Bersihkan kolom kosong
            combined_df.dropna(axis=1, how='all', inplace=True)

            # ✅ Format kolom 'Tanggal Scraping'
            if 'Tanggal Scraping' in combined_df.columns:
                combined_df['Tanggal Scraping'] = pd.to_datetime(combined_df['Tanggal Scraping'])
            
            # ✅ Reset index agar tidak berantakan
            combined_df.reset_index(drop=True, inplace=True)

            # ✅ Simpan ke Excel
            combined_df.to_excel(writer, sheet_name=table_name, index=False)

    print(f"✅ Data berhasil disimpan ke {file_path}")

def main_danamon():
    """Fungsi utama untuk menjalankan scraping Bank Danamon dan menyimpan data."""
    scraped_tables = scrape_danamon_tables()
    if scraped_tables:
        save_to_excel(scraped_tables, DANAMON_EXCEL_PATH)
    else:
        print("⚠️ Tidak ada data Bank Danamon yang berhasil di-scrape.")


# ==========================
# 🟢 BTPN BANK SETUP
# ==========================

# URL target Bank BTPN
BTPN_URL = "https://www.smbci.com/en/prime-lending-rate/kurs"

# Path untuk file Excel Bank BTPN (Sesuai Direktori)
BTPN_EXCEL_PATH = r"Z:\kerjaan magang\LCT_BTPN.xlsx"

# Class tabel pada halaman BTPN
BTPN_TABLE_CLASS = "table-custom"

def scrape_btpn_tables():
    """Scrape tabel dari halaman Bank BTPN."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(BTPN_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tables_data = {}

    # Cari tabel berdasarkan class
    table_element = soup.find("table", class_=BTPN_TABLE_CLASS)

    if table_element:
        table_io = StringIO(str(table_element))
        df = pd.read_html(table_io)[0]
        df["Tanggal Scraping"] = pd.Timestamp.now()  # Tambahkan kolom timestamp
        tables_data["Exchange Rates"] = df
    else:
        print("⚠️ Tabel Bank BTPN tidak ditemukan!")

    return tables_data

def save_to_excel(tables_data, file_path):
    """Simpan data dari semua tabel ke file Excel, memperbarui data jika sudah ada."""
    if os.path.exists(file_path):
        existing_data = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")
    else:
        existing_data = {}

    with pd.ExcelWriter(file_path, engine="openpyxl", mode='w') as writer:
        for table_name, new_df in tables_data.items():
            if table_name in existing_data:
                combined_df = pd.concat([existing_data[table_name], new_df], ignore_index=True)
            else:
                combined_df = new_df

            # 🔴 FLATTEN MultiIndex jika ada
            if isinstance(combined_df.columns, pd.MultiIndex):
                combined_df.columns = [' '.join(map(str, col)).strip() for col in combined_df.columns]

            # ✅ Bersihkan kolom kosong
            combined_df.dropna(axis=1, how='all', inplace=True)

            # ✅ Format kolom 'Tanggal Scraping'
            if 'Tanggal Scraping' in combined_df.columns:
                combined_df['Tanggal Scraping'] = pd.to_datetime(combined_df['Tanggal Scraping'])
            
            # ✅ Reset index agar tidak berantakan
            combined_df.reset_index(drop=True, inplace=True)

            # ✅ Simpan ke Excel
            combined_df.to_excel(writer, sheet_name=table_name, index=False)

    print(f"✅ Data berhasil disimpan ke {file_path}")

def main_btpn():
    """Fungsi utama untuk menjalankan scraping Bank BTPN dan menyimpan data."""
    scraped_tables = scrape_btpn_tables()
    if scraped_tables:
        save_to_excel(scraped_tables, BTPN_EXCEL_PATH)
    else:
        print("⚠️ Tidak ada data Bank BTPN yang berhasil di-scrape.")

if __name__ == "__main__":
    main_permata()
    main_danamon()
    main_btpn()