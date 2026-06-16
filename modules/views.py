import streamlit as st
import pandas as pd
from PIL import Image

from modules import splitter, formatter


def ambil_jumlah(nilai):
    if not nilai or pd.isna(nilai):
        return 1
    return int(nilai)


def sidebar_pengaturan():
    # bagian sidebar: input api key gemini
    st.sidebar.header("Pengaturan")
    st.sidebar.markdown("**Model AI:** Gemini")
    api_key = st.sidebar.text_input("Google API Key", type="password")
    st.sidebar.caption("Gemini butuh API key dari Google AI Studio.")
    return api_key


def upload_struk():
    st.header("1. Upload Struk")
    file_struk = st.file_uploader("Pilih gambar struk", type=["jpg", "jpeg", "png"])
    if file_struk is None:
        return None
    gambar = Image.open(file_struk).convert("RGB")
    st.image(gambar, width=350)
    return gambar


def edit_data(data_struk):
    st.header("2. Cek & Edit Data")
    st.write("Cek hasil bacaan AI. Kalau ada yang salah/kurang, bisa diedit di tabel:")

    df = pd.DataFrame(data_struk["items"])
    df_edit = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="editor")
    items = df_edit.to_dict("records")

    items_valid = []
    for it in items:
        nama = it.get("name")
        harga = it.get("total_price")
        if nama is None or str(nama).strip() == "":
            continue
        if harga is None or pd.isna(harga):
            continue
        items_valid.append(it)
    items = items_valid     
    
    rincian = []
    for it in items:
        jumlah = ambil_jumlah(it["count"])
        harga_total = float(it["total_price"])
        harga_satuan = harga_total / jumlah if jumlah > 0 else harga_total
        rincian.append({
            "Item": it["name"],
            "Jumlah": jumlah,
            "Harga Satuan": formatter.rupiah(harga_satuan),
            "Total": formatter.rupiah(harga_total),
        })
    st.caption("Rincian (harga satuan dihitung otomatis):")
    st.table(pd.DataFrame(rincian))

    total = st.number_input(
        "Total tagihan (sudah termasuk pajak/service)",
        value=float(data_struk["total"]),
        step=1000.0,
    )

    subtotal = splitter.hitung_subtotal(items)

    c1, c2, c3 = st.columns(3)
    c1.metric("Subtotal", formatter.rupiah(subtotal))
    c2.metric("Pajak/Service", formatter.rupiah(total - subtotal))
    c3.metric("Total", formatter.rupiah(total))

    return items, subtotal, total


def input_peserta(peserta):
    st.header("3. Siapa saja yang Bayar?")
    nama_baru = st.text_input("Nama orang")
    tambah = st.button("Tambah orang")

    hapus = None
    if len(peserta) > 0:
        st.write("Peserta:")
        for nama in peserta:
            kolom_nama, kolom_tombol = st.columns([4, 1])
            kolom_nama.write("- " + nama)
            if kolom_tombol.button("Hapus", key="hapus_" + nama):
                hapus = nama

    return nama_baru, tambah, hapus


def assign_items(items, peserta):
    st.header("4. Item Ini Siapa yang Bayar?")
    assign = {}
    for i in range(len(items)):
        item = items[i]
        jumlah = ambil_jumlah(item["count"])
        harga_total = float(item["total_price"])
        harga_satuan = harga_total / jumlah if jumlah > 0 else harga_total

        st.write(
            "**" + str(item["name"]) + "**  "
            + str(jumlah) + " x " + formatter.rupiah(harga_satuan)
            + " = " + formatter.rupiah(harga_total)
        )
        pilih = st.multiselect(
            "Yang bayar " + str(item["name"]),
            peserta,
            key="assign_" + str(i),
            label_visibility="collapsed",
        )
        assign[i] = pilih

    # kasih warning kalau ada item yang belum dipilih siapa yang bayar
    belum = []
    for i in range(len(items)):
        if len(assign[i]) == 0:
            belum.append(str(items[i]["name"]))
    if len(belum) > 0:
        st.warning("Item ini belum ada yang bayar: " + ", ".join(belum))

    return assign


def tampilkan_hasil(hasil, total):
    # tampilan rincian bayaran tiap orang + tombol download 
    st.header("5. Hasil Pembagian")
    for nama in hasil:
        detail = hasil[nama]
        with st.container(border=True):
            kiri, kanan = st.columns([3, 2])
            kiri.subheader(nama)
            kanan.markdown("#### Total: " + formatter.rupiah(detail["total"]))

            rincian = []
            for it in detail["items"]:
                rincian.append({"Item": it["name"], "Harga": formatter.rupiah(it["harga"])})
            if len(rincian) > 0:
                st.table(pd.DataFrame(rincian))

            st.write("Subtotal: " + formatter.rupiah(detail["subtotal"]))
            st.write("Pajak & Service: " + formatter.rupiah(detail["extra"]))

    ringkasan = formatter.buat_ringkasan(hasil, total)
    st.download_button("Download ringkasan (.txt)", ringkasan, "split_bill.txt")