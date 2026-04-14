"""
Konversi file .xlsx dari folder data_ref ke CSV di data_ref/csv/
Mendukung format: Pagu Dana Desa dan Penyerapan Dana Desa (Provinsi Jambi)
"""

import os
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data_ref"))
CSV_DIR = os.path.join(BASE_DIR, "csv")
os.makedirs(CSV_DIR, exist_ok=True)

PAGU_COLS = [
    "No", "Kode_Provinsi", "Provinsi", "Kode_Lokasi",
    "Kabupaten_Kota", "Kode_Desa", "Nama_Desa", "Pagu",
]

PENYERAPAN_COLS = [
    "No", "Kode_Provinsi", "Provinsi", "Kode_Lokasi",
    "Kabupaten_Kota", "Kode_Desa", "Nama_Desa",
    "Kode_Output", "Uraian_Output", "Volume", "Satuan",
    "Cara_Pengadaan", "Keterangan",
    "Real_T1", "Real_T2", "Real_T3",
    "Pct_T1", "Pct_T2", "Pct_T3",
]


def read_dana_desa_xlsx(filepath: str, file_type: str) -> pd.DataFrame:
    """
    Baca file xlsx Dana Desa dengan format standar:
      Baris 0-1 : judul & tahun
      Baris 2   : kosong
      Baris 3   : header kolom
      Baris 4+  : data
    """
    expected_cols = PAGU_COLS if file_type == "pagu" else PENYERAPAN_COLS
    num_cols = len(expected_cols)

    df = pd.read_excel(filepath, header=3, usecols=range(num_cols))
    df.columns = expected_cols

    # Buang baris yang bukan data (header ganda / footer / total)
    df = df[pd.to_numeric(df["No"], errors="coerce").notna()].copy()
    df["No"] = df["No"].astype(int)
    df = df.reset_index(drop=True)
    return df


def convert_all():
    xlsx_files = [f for f in os.listdir(BASE_DIR) if f.lower().endswith(".xlsx")]

    if not xlsx_files:
        print("Tidak ada file .xlsx ditemukan di:", BASE_DIR)
        return

    for filename in sorted(xlsx_files):
        name_lower = filename.lower()
        if "pagu" in name_lower:
            file_type = "pagu"
        elif "penyerapan" in name_lower:
            file_type = "penyerapan"
        else:
            print(f"[SKIP] Format tidak dikenal: {filename}")
            continue

        src_path = os.path.join(BASE_DIR, filename)
        csv_name = os.path.splitext(filename)[0].replace(" ", "_") + ".csv"
        dst_path = os.path.join(CSV_DIR, csv_name)

        try:
            df = read_dana_desa_xlsx(src_path, file_type)
            df.to_csv(dst_path, index=False, encoding="utf-8-sig")
            print(f"[OK] {filename} -> csv/{csv_name}  ({len(df):,} baris)")
        except Exception as e:
            print(f"[ERROR] {filename}: {e}")


if __name__ == "__main__":
    convert_all()
