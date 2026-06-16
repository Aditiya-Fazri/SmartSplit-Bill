import streamlit as st

from modules import reader, splitter, views

st.set_page_config(page_title="SmartSplit Bill", page_icon="🧾")

if "data_struk" not in st.session_state:
    st.session_state["data_struk"] = None
if "peserta" not in st.session_state:
    st.session_state["peserta"] = []
if "assign" not in st.session_state:
    st.session_state["assign"] = {}

st.title("🧾 SmartSplit Bill")
st.caption("Upload struk, AI baca isinya, terus bagi tagihan ke temen-temen.")

# sidebar: ambil api key
api_key = views.sidebar_pengaturan()

# STEP 1: upload + baca struk
gambar = views.upload_struk()
if gambar is not None:
    if st.button("Baca struk pakai AI"):
        if api_key == "":
            st.error("Isi dulu Google API Key di sidebar.")
            st.stop()
        with st.spinner("Lagi baca struk..."):
            st.session_state["data_struk"] = reader.baca_struk(gambar, api_key)
        st.success("Struk selesai dibaca.")

if st.session_state["data_struk"] is None:
    st.stop()

# STEP 2: cek & edit data
items, subtotal, total = views.edit_data(st.session_state["data_struk"])

# STEP 3: tambah/hapus peserta
nama_baru, tambah, hapus = views.input_peserta(st.session_state["peserta"])
if tambah and nama_baru != "" and nama_baru not in st.session_state["peserta"]:
    st.session_state["peserta"].append(nama_baru)
    st.rerun()
if hapus is not None:
    st.session_state["peserta"].remove(hapus)
    st.rerun()

if len(st.session_state["peserta"]) == 0:
    st.stop()

# STEP 4: assign item ke orang
st.session_state["assign"] = views.assign_items(items, st.session_state["peserta"])

# STEP 5: hitung & tampilan hasil
if st.button("Hitung pembagian"):
    hasil = splitter.hitung_pembagian(
        items,
        st.session_state["assign"],
        st.session_state["peserta"],
        subtotal,
        total,
    )
    views.tampilkan_hasil(hasil, total)