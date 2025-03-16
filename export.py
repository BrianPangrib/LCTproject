import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO
import os

# ==========================
# 🔵 BNI SETUP
# ==========================

# URL target BNI
BNI_URL = "https://www.bni.co.id/id-id/beranda/informasi-valas"

# Path untuk file Excel BNI
BNI_EXCEL_PATH = r"Z:\kerjaan magang\LCT_BNI.xlsx"

# Mapping elemen untuk masing-masing tabel BNI
BNI_TABLE_MAPPING = {
    "Special Rates": "dnn_ctr6793_BNIValasInfoView_lblTitleCounter",
    "TT Counter": "dnn_ctr6793_BNIValasInfoView_lblTitleBankNotes",
    "Bank Notes": "dnn_ctr6793_BNIValasInfoView_lblTitleSpecialRates"
}

def scrape_bni_tables():
    """Scrape ketiga tabel dari halaman BNI dan kembalikan sebagai dictionary DataFrames."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(BNI_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tables_data = {}

    for table_name, span_id in BNI_TABLE_MAPPING.items():
        # Cari elemen <span> berdasarkan ID untuk mendapatkan judul tabel
        span_element = soup.find("span", id=span_id)

        # Temukan tabel yang berdekatan
        table_element = span_element.find_next("table", class_="table table-striped angrid-grid table_info_counter")

        if table_element:
            table_io = StringIO(str(table_element))
            df = pd.read_html(table_io)[0]
            df["Tanggal Scraping"] = pd.Timestamp.now()  # Tambahkan kolom timestamp
            tables_data[table_name] = df
        else:
            print(f"Tabel '{table_name}' tidak ditemukan!")

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


def main_bni():
    """Fungsi utama untuk menjalankan scraping BNI dan menyimpan data."""
    scraped_tables = scrape_bni_tables()
    if scraped_tables:
        save_to_excel(scraped_tables, BNI_EXCEL_PATH)
    else:
        print("⚠️ Tidak ada data BNI yang berhasil di-scrape.")


# ==========================
# 🟢 MANDIRI SETUP
# ==========================

# URL target Mandiri
MANDIRI_URL = "https://www.bankmandiri.co.id/kurs"

# Path untuk file Excel Mandiri
MANDIRI_EXCEL_PATH = r"Z:\kerjaan magang\LCT_MANDIRI.xlsx"

# ID Tabel Mandiri
MANDIRI_TABLE_ID = "_Exchange_Rate_Portlet_INSTANCE_9070nSEKk62r_display"

def scrape_mandiri_tables():
    """Scrape tabel dari halaman Bank Mandiri."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(MANDIRI_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tables_data = {}

    # Cari tabel berdasarkan ID
    table_element = soup.find("table", id=MANDIRI_TABLE_ID)

    if table_element:
        table_io = StringIO(str(table_element))
        df = pd.read_html(table_io)[0]
        df["Tanggal Scraping"] = pd.Timestamp.now()  # Tambahkan kolom timestamp
        tables_data["Exchange Rates"] = df
    else:
        print("⚠️ Tabel Bank Mandiri tidak ditemukan!")

    return tables_data

def main_mandiri():
    """Fungsi utama untuk menjalankan scraping Mandiri dan menyimpan data."""
    scraped_tables = scrape_mandiri_tables()
    if scraped_tables:
        save_to_excel(scraped_tables, MANDIRI_EXCEL_PATH)
    else:
        print("⚠️ Tidak ada data Mandiri yang berhasil di-scrape.")


# ==========================
# 🔵 BRI SETUP
# ==========================

# URL target BRI
BRI_URL = "https://bri.co.id/kurs-detail"

# Path untuk file Excel BRI
BRI_EXCEL_PATH = r"Z:\kerjaan magang\LCT_BRI.xlsx"

# Mapping elemen untuk masing-masing tabel BRI
BRI_TABLE_MAPPING = {
    "E-Rate": "_bri_kurs_detail_portlet_display",
    "TT Counter": "_bri_kurs_detail_portlet_display2"
}

def scrape_bri_tables():
    """Scrape tabel dari halaman BRI dan kembalikan sebagai dictionary DataFrames."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(BRI_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tables_data = {}

    for table_name, table_id in BRI_TABLE_MAPPING.items():
        # Temukan tabel berdasarkan ID
        table_element = soup.find("table", id=table_id)

        if table_element:
            table_io = StringIO(str(table_element))
            df = pd.read_html(table_io)[0]
            df["Tanggal Scraping"] = pd.Timestamp.now()  # Tambahkan kolom timestamp
            tables_data[table_name] = df
        else:
            print(f"⚠️ Tabel '{table_name}' tidak ditemukan di {BRI_URL}")

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

def main_bri():
    """Fungsi utama untuk menjalankan scraping BRI dan menyimpan data."""
    scraped_tables = scrape_bri_tables()
    if scraped_tables:
        save_to_excel(scraped_tables, BRI_EXCEL_PATH)
    else:
        print("⚠️ Tidak ada data BRI yang berhasil di-scrape.")


# ==========================
# 🔵 BCA SETUP
# ==========================

# URL target BCA
BCA_URL = "https://www.bca.co.id/id/informasi/kurs"

# Path untuk file Excel BCA
BCA_EXCEL_PATH = r"Z:\kerjaan magang\LCT_BCA.xlsx"

# Class tabel pada halaman BCA
BCA_TABLE_CLASS = "m-table-kurs m-table--sticky-first-coloumn m-table-kurs--pad"

def scrape_bca_table():
    """Scrape tabel kurs dari halaman BCA dan kembalikan sebagai DataFrame."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(BCA_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Temukan tabel berdasarkan class
    table_element = soup.find("table", class_=BCA_TABLE_CLASS)

    if table_element:
        table_io = StringIO(str(table_element))
        df = pd.read_html(table_io)[0]
        df["Tanggal Scraping"] = pd.Timestamp.now()  # Tambahkan kolom timestamp
        return df
    else:
        print(f"⚠️ Tabel tidak ditemukan di {BCA_URL}")
        return None

def save_to_excel_bca(new_data, file_path):
    """Simpan data dari tabel BCA ke file Excel, memperbarui data jika sudah ada."""

    # 🔴 Tangani jika file rusak atau tidak bisa dibaca
    if os.path.exists(file_path):
        try:
            existing_data = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")
        except Exception as e:
            print(f"⚠️ File Excel BCA rusak atau tidak valid: {e}")
            print(f"🗑️ Menghapus file rusak: {file_path}")
            os.remove(file_path)  # Hapus file rusak
            existing_data = {}  # Kosongkan data lama
    else:
        existing_data = {}

    # Jika sheet "Kurs BCA" sudah ada, gabungkan data lama dan baru
    if isinstance(existing_data, dict) and "Kurs BCA" in existing_data:
        existing_df = existing_data["Kurs BCA"]
        combined_data = pd.concat([existing_df, new_data], ignore_index=True)
    else:
        combined_data = new_data  # Jika file baru, buat data baru

    # 🔴 FLATTEN MultiIndex jika ada
    if isinstance(combined_data.columns, pd.MultiIndex):
        combined_data.columns = [' '.join(map(str, col)).strip() for col in combined_data.columns]

    with pd.ExcelWriter(file_path, engine="openpyxl", mode='w') as writer:
        if not combined_data.empty:  # Cegah penyimpanan workbook kosong
            combined_data.to_excel(writer, sheet_name="Kurs BCA", index=False)
        else:
            print("⚠️ Tidak ada data untuk disimpan, sheet tidak akan dibuat.")

    print(f"✅ Data BCA berhasil disimpan ke {file_path}")


def main_bca():
    """Fungsi utama untuk menjalankan scraping BCA dan menyimpan data."""
    scraped_data = scrape_bca_table()
    if scraped_data is not None:
        save_to_excel_bca(scraped_data, BCA_EXCEL_PATH)  # ⬅️ Menggunakan fungsi khusus BCA
    else:
        print("⚠️ Tidak ada data BCA yang berhasil di-scrape.")

# ==========================
# 🔵 MAYBANK SETUP
# ==========================

# URL target Maybank
MAYBANK_URL = "https://www.maybank.co.id/Business/forexrate"

# Path untuk file Excel Maybank
MAYBANK_EXCEL_PATH = r"Z:\kerjaan magang\LCT_MAYBANK.xlsx"

# Class tabel pada halaman Maybank
MAYBANK_TABLE_CLASS = "table-custom full-table-width"

def scrape_maybank_table():
    """Scrape tabel kurs dari halaman Maybank dan kembalikan sebagai DataFrame."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(MAYBANK_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Temukan tabel berdasarkan class
    table_element = soup.find("table", class_=MAYBANK_TABLE_CLASS)

    if table_element:
        table_io = StringIO(str(table_element))
        df = pd.read_html(table_io)[0]
        df["Tanggal Scraping"] = pd.Timestamp.now()  # Tambahkan kolom timestamp
        return df
    else:
        print(f"⚠️ Tabel tidak ditemukan di {MAYBANK_URL}")
        return None

def save_to_excel_maybank(new_data, file_path):
    """Simpan data dari tabel ke file Excel, memperbarui data jika sudah ada."""
    if os.path.exists(file_path):
        existing_data = pd.read_excel(file_path, sheet_name="Kurs Maybank", engine="openpyxl")
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
        combined_data.to_excel(writer, sheet_name="Kurs Maybank", index=False)

    print(f"✅ Data berhasil disimpan ke {file_path}")

def main_maybank():
    """Fungsi utama untuk menjalankan scraping Maybank dan menyimpan data."""
    scraped_data = scrape_maybank_table()
    if scraped_data is not None:
        save_to_excel_maybank(scraped_data, MAYBANK_EXCEL_PATH)
    else:
        print("⚠️ Tidak ada data Maybank yang berhasil di-scrape.")

# ==========================
# 🔵 CIMB Niaga SETUP
# ==========================

# URL target CIMB Niaga
CIMB_URL = "https://www.cimbniaga.co.id/id/personal/index"

# Path untuk file Excel CIMB Niaga
CIMB_EXCEL_PATH = r"Z:\kerjaan magang\LCT_CIMB.xlsx"

# Class tabel pada halaman CIMB Niaga
CIMB_TABLE_CLASS = "table mb-0 cimb-table table-borderless table-hover"

def scrape_cimb_table():
    """Scrape tabel kurs dari halaman CIMB Niaga dan kembalikan sebagai DataFrame."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(CIMB_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # 🔍 Periksa semua tabel di halaman
    tables = soup.find_all("table")
    print(f"✅ Jumlah tabel ditemukan di CIMB Niaga: {len(tables)}")

    # Temukan tabel berdasarkan class
    table_element = soup.find("table", class_=CIMB_TABLE_CLASS)

    if table_element:
        table_io = StringIO(str(table_element))
        df = pd.read_html(table_io)[0]
        df["Tanggal Scraping"] = pd.Timestamp.now()  # Tambahkan kolom timestamp
        return df
    else:
        print(f"⚠️ Tabel tidak ditemukan di {CIMB_URL}. Coba periksa class-nya lagi.")
        return None

def save_to_excel_cimb(new_data, file_path):
    """Simpan data dari tabel CIMB Niaga ke file Excel, memperbarui data jika sudah ada."""

    # 🔴 Tangani jika file rusak atau tidak bisa dibaca
    if os.path.exists(file_path):
        try:
            existing_data = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")
        except Exception as e:
            print(f"⚠️ File Excel CIMB Niaga rusak atau tidak valid: {e}")
            print(f"🗑️ Menghapus file rusak: {file_path}")
            os.remove(file_path)  # Hapus file rusak
            existing_data = {}  # Kosongkan data lama
    else:
        existing_data = {}

    # Jika sheet "Kurs CIMB Niaga" sudah ada, gabungkan data lama dan baru
    if isinstance(existing_data, dict) and "Kurs CIMB Niaga" in existing_data:
        existing_df = existing_data["Kurs CIMB Niaga"]
        combined_data = pd.concat([existing_df, new_data], ignore_index=True)
    else:
        combined_data = new_data  # Jika file baru, buat data baru

    # 🔴 FLATTEN MultiIndex jika ada
    if isinstance(combined_data.columns, pd.MultiIndex):
        combined_data.columns = [' '.join(map(str, col)).strip() for col in combined_data.columns]

    with pd.ExcelWriter(file_path, engine="openpyxl", mode='w') as writer:
        if not combined_data.empty:  # Cegah penyimpanan workbook kosong
            combined_data.to_excel(writer, sheet_name="Kurs CIMB Niaga", index=False)
        else:
            print("⚠️ Tidak ada data untuk disimpan, sheet tidak akan dibuat.")

    print(f"✅ Data CIMB Niaga berhasil disimpan ke {file_path}")

def main_cimb():
    """Fungsi utama untuk menjalankan scraping CIMB Niaga dan menyimpan data."""
    scraped_data = scrape_cimb_table()
    if scraped_data is not None:
        save_to_excel_cimb(scraped_data, CIMB_EXCEL_PATH)  # ⬅️ Menggunakan fungsi khusus CIMB Niaga
    else:
        print("⚠️ Tidak ada data CIMB Niaga yang berhasil di-scrape.")

# ==========================
# 🔵 MUFG SETUP
# ==========================

# URL target MUFG
MUFG_URL = "https://www.mufg.co.id/charges/today-exchange-rates"

# Path untuk file Excel MUFG
MUFG_EXCEL_PATH = r"Z:\kerjaan magang\LCT_MUFG.xlsx"

# Class tabel pada halaman MUFG
MUFG_TABLE_CLASS = "table table-bordered"

def scrape_mufg_table():
    """Scrape tabel kurs dari halaman MUFG dan kembalikan sebagai DataFrame."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(MUFG_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Temukan tabel berdasarkan class
    table_element = soup.find("table", class_=MUFG_TABLE_CLASS)

    if table_element:
        table_io = StringIO(str(table_element))
        df = pd.read_html(table_io)[0]
        df["Tanggal Scraping"] = pd.Timestamp.now()  # Tambahkan kolom timestamp
        return df
    else:
        print(f"⚠️ Tabel tidak ditemukan di {MUFG_URL}")
        return None

def save_to_excel_mufg(new_data, file_path):
    """Simpan data dari tabel ke file Excel, memperbarui data jika sudah ada."""
    if os.path.exists(file_path):
        existing_data = pd.read_excel(file_path, sheet_name="Kurs MUFG", engine="openpyxl")
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
        combined_data.to_excel(writer, sheet_name="Kurs MUFG", index=False)

    print(f"✅ Data berhasil disimpan ke {file_path}")

def main_mufg():
    """Fungsi utama untuk menjalankan scraping MUFG dan menyimpan data."""
    scraped_data = scrape_mufg_table()
    if scraped_data is not None:
        save_to_excel_mufg(scraped_data, MUFG_EXCEL_PATH)
    else:
        print("⚠️ Tidak ada data MUFG yang berhasil di-scrape.")


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
    # Jalankan scraping untuk BNI
    main_bni()

    # Jalankan scraping untuk Mandiri
    main_mandiri()

    # Jalankan scraping untuk BRI
    main_bri()

    # Jalankan scraping untuk BCA
    main_bca()

    # Jalankan scraping untuk Maybank
    main_maybank()

    # Jalankan scraping untuk CIMB Niaga
    main_cimb()

    # Jalankan scraping untuk MUFG
    main_mufg()
    
    # Jalankan scraping untuk HSBC
    main_hsbc()