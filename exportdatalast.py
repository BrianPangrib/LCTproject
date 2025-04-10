import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO
import os


# LIST BANK PADA CODE INI:
# ICBC
# BOC
# CCB
# OCBC
# SINARMAS
# DBS

# ==========================
# 🟢 ICBC BANK SETUP
# ==========================

# URL target ICBC Bank
ICBC_URL = "https://www.icbc.co.id/it/column/1438058489762431129.html"

# Path untuk file Excel ICBC Bank (Sesuaikan Direktori)
ICBC_EXCEL_PATH = r"Z:\kerjaan magang\LCT_ICBC.xlsx"

# Class Tabel ICBC Bank
ICBC_TABLE_CLASS = "forex-table"

def scrape_icbc_tables():
    """Scrape tabel dari halaman ICBC Bank dan konversi nilai kurs ke float."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(ICBC_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tables_data = {}

    # Cari tabel berdasarkan class
    table_element = soup.find("table", class_=ICBC_TABLE_CLASS)

    if table_element:
        table_io = StringIO(str(table_element))
        df = pd.read_html(table_io)[0]

        # 🧹 Bersihkan koma & konversi ke float (kecuali kolom pertama: 'Mata Uang')
        for col in df.columns[1:]:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .astype(float)
            )

        # 🕒 Tambahkan kolom timestamp
        df["Tanggal Scraping"] = pd.Timestamp.now()

        tables_data["Exchange Rates"] = df
    else:
        print("⚠️ Tabel Bank ICBC tidak ditemukan!")

    return tables_data


def save_to_excel_icbc(tables_data, file_path):
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

def main_icbc():
    """Fungsi utama untuk menjalankan scraping ICBC Bank dan menyimpan data."""
    scraped_tables = scrape_icbc_tables()
    if scraped_tables:
        save_to_excel_icbc(scraped_tables, ICBC_EXCEL_PATH)
    else:
        print("⚠️ Tidak ada data ICBC Bank yang berhasil di-scrape.")


# ==========================
# 🔵 BOC BANK SETUP
# ==========================

# URL target Bank of China
BOC_URL = "https://www.bankofchina.com/sourcedb/idr/"

# Path untuk file Excel BoC (diubah sesuai direktori masing-masing)
BOC_EXCEL_PATH = r"Z:\kerjaan magang\LCT_BOC.xlsx"

# Class Tabel Bank of China
BOC_TABLE_CLASS = "data2"

def scrape_boc_tables():
    """Scrape tabel dari halaman Bank of China."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(BOC_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tables_data = {}

    # Cari tabel berdasarkan class
    table_element = soup.find("table", class_=BOC_TABLE_CLASS)

    if table_element:
        table_io = StringIO(str(table_element))
        df = pd.read_html(table_io, header=0)[0]

        # Tambahkan kolom timestamp
        df["Tanggal Scraping"] = pd.Timestamp.now()
        tables_data["Exchange Rates"] = df
    else:
        print("⚠️ Tabel Bank of China tidak ditemukan!")

    return tables_data


def save_to_excel(tables_data, file_path):
    """Simpan data dari semua tabel ke file Excel, memperbarui data jika sudah ada."""
    if os.path.exists(file_path):
        # Baca file Excel yang sudah ada
        existing_data = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")
    else:
        existing_data = {}

    with pd.ExcelWriter(file_path, engine="openpyxl", mode='w') as writer:
        for table_name, new_df in tables_data.items():
            # Gabungkan data lama dan baru jika ada
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

def main_boc():
    """Fungsi utama untuk menjalankan scraping Bank of China dan menyimpan data."""
    scraped_tables = scrape_boc_tables()
    if scraped_tables:
        save_to_excel(scraped_tables, BOC_EXCEL_PATH)
    else:
        print("⚠️ Tidak ada data BoC yang berhasil di-scrape.")

# ==========================
# 🔵 CCB INDONESIA SETUP
# ==========================

CCB_URL = "https://idn.ccb.com/en/rupiah-forex-deposit"
CCB_EXCEL_PATH = r"Z:\kerjaan magang\LCT_CCB.xlsx"
CCB_TABLE_CLASS = "table table-bordered my-0"

def scrape_ccb_tables():
    """Scrape tabel dari halaman CCB Indonesia."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(CCB_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tables_data = {}

    # Temukan tabel sesuai class CCB
    table_element = soup.find("table", class_=CCB_TABLE_CLASS)

    if table_element:
        table_io = StringIO(str(table_element))
        df = pd.read_html(table_io, header=0)[0]

        # Tambahkan timestamp scraping
        df["Tanggal Scraping"] = pd.Timestamp.now()
        tables_data["CCB Exchange Rates"] = df
    else:
        print("⚠️ Tabel CCB Indonesia tidak ditemukan!")

    return tables_data

def save_to_excel(tables_data, file_path):
    """Simpan data dari semua tabel ke file Excel, memperbarui data jika sudah ada."""
    if os.path.exists(file_path):
        # Baca file Excel yang sudah ada
        existing_data = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")
    else:
        existing_data = {}

    with pd.ExcelWriter(file_path, engine="openpyxl", mode='w') as writer:
        for table_name, new_df in tables_data.items():
            # Gabungkan data lama dan baru jika ada
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

def main_ccb():
    """Fungsi utama untuk menjalankan scraping CCB Indonesia dan menyimpan data."""
    scraped_tables = scrape_ccb_tables()
    if scraped_tables:
        save_to_excel(scraped_tables, CCB_EXCEL_PATH)
    else:
        print("⚠️ Tidak ada data CCB yang berhasil di-scrape.")


# ==========================
# 🔵 OCBC NISP SETUP
# ==========================

OCBC_URL = "https://www.ocbc.id/nilai-tukar-mata-uang-asing"
OCBC_EXCEL_PATH = r"Z:\kerjaan magang\LCT_OCBC.xlsx"
OCBC_TABLE_CLASS = "ocbc-widget-xr-tbl"

def scrape_ocbc_tables():
    """Scrape tabel dari halaman OCBC NISP."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(OCBC_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tables_data = {}

    table_element = soup.find("table", class_=OCBC_TABLE_CLASS)

    if table_element:
        table_io = StringIO(str(table_element))
        df = pd.read_html(table_io, header=0)[0]

        df["Tanggal Scraping"] = pd.Timestamp.now()
        tables_data["OCBC Exchange Rates"] = df
    else:
        print("⚠️ Tabel OCBC NISP tidak ditemukan!")

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

            if isinstance(combined_df.columns, pd.MultiIndex):
                combined_df.columns = [' '.join(map(str, col)).strip() for col in combined_df.columns]

            combined_df.dropna(axis=1, how='all', inplace=True)

            if 'Tanggal Scraping' in combined_df.columns:
                combined_df['Tanggal Scraping'] = pd.to_datetime(combined_df['Tanggal Scraping'])

            combined_df.reset_index(drop=True, inplace=True)
            combined_df.to_excel(writer, sheet_name=table_name, index=False)

    print(f"✅ Data berhasil disimpan ke {file_path}")

def main_ocbc():
    """Fungsi utama untuk menjalankan scraping OCBC NISP dan menyimpan data."""
    scraped_tables = scrape_ocbc_tables()
    if scraped_tables:
        save_to_excel(scraped_tables, OCBC_EXCEL_PATH)
    else:
        print("⚠️ Tidak ada data OCBC yang berhasil di-scrape.")

# ==========================
# 🔵 SINARMAS BANK SETUP
# ==========================

SINARMAS_URL = "https://www.banksinarmas.com/id/kurs#"
SINARMAS_EXCEL_PATH = r"Z:\kerjaan magang\LCT_SINARMAS.xlsx"
SINARMAS_TABLE_CLASS = "tbl2"

def scrape_sinarmas_tables():
    """Scrape tabel dari halaman Bank Sinarmas."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(SINARMAS_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tables_data = {}

    table_element = soup.find("table", class_=SINARMAS_TABLE_CLASS)

    if table_element:
        table_io = StringIO(str(table_element))
        df = pd.read_html(table_io, header=0)[0]

        df["Tanggal Scraping"] = pd.Timestamp.now()
        tables_data["Sinarmas Exchange Rates"] = df
    else:
        print("⚠️ Tabel Bank Sinarmas tidak ditemukan!")

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

            if isinstance(combined_df.columns, pd.MultiIndex):
                combined_df.columns = [' '.join(map(str, col)).strip() for col in combined_df.columns]

            combined_df.dropna(axis=1, how='all', inplace=True)

            if 'Tanggal Scraping' in combined_df.columns:
                combined_df['Tanggal Scraping'] = pd.to_datetime(combined_df['Tanggal Scraping'])

            combined_df.reset_index(drop=True, inplace=True)
            combined_df.to_excel(writer, sheet_name=table_name, index=False)

    print(f"✅ Data berhasil disimpan ke {file_path}")

def main_sinarmas():
    """Fungsi utama untuk menjalankan scraping Bank Sinarmas dan menyimpan data."""
    scraped_tables = scrape_sinarmas_tables()
    if scraped_tables:
        save_to_excel(scraped_tables, SINARMAS_EXCEL_PATH)
    else:
        print("⚠️ Tidak ada data Sinarmas yang berhasil di-scrape.")

# ==========================
# 🔵 DBS INDONESIA SETUP
# ==========================

DBS_URL = "https://www.dbs.id/id/treasures-id/forex.page"
DBS_EXCEL_PATH = r"Z:\kerjaan magang\LCT_DBS.xlsx"
DBS_TABLE_CLASS = "tbl-primary mBot-8"

def scrape_dbs_tables():
    """Scrape tabel dari halaman DBS Indonesia."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(DBS_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tables_data = {}

    table_element = soup.find("table", class_=DBS_TABLE_CLASS)

    if table_element:
        table_io = StringIO(str(table_element))
        df = pd.read_html(table_io, header=0)[0]

        df["Tanggal Scraping"] = pd.Timestamp.now()
        tables_data["DBS Exchange Rates"] = df
    else:
        print("⚠️ Tabel DBS Indonesia tidak ditemukan!")

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

            if isinstance(combined_df.columns, pd.MultiIndex):
                combined_df.columns = [' '.join(map(str, col)).strip() for col in combined_df.columns]

            combined_df.dropna(axis=1, how='all', inplace=True)

            if 'Tanggal Scraping' in combined_df.columns:
                combined_df['Tanggal Scraping'] = pd.to_datetime(combined_df['Tanggal Scraping'])

            combined_df.reset_index(drop=True, inplace=True)
            combined_df.to_excel(writer, sheet_name=table_name, index=False)

    print(f"✅ Data berhasil disimpan ke {file_path}")

def main_dbs():
    """Fungsi utama untuk menjalankan scraping DBS Indonesia dan menyimpan data."""
    scraped_tables = scrape_dbs_tables()
    if scraped_tables:
        save_to_excel(scraped_tables, DBS_EXCEL_PATH)
    else:
        print("⚠️ Tidak ada data DBS yang berhasil di-scrape.")


if __name__ == "__main__":
    main_icbc()
    main_boc()
    main_ccb()
    main_ocbc()
    main_sinarmas()
    main_dbs()