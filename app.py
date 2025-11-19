# app.py - Contoh Struktur Awal
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Dashboard Proyek Baru", layout="wide")

st.title("🌟 Dashboard Data Baru Anda")
st.write("Selamat datang! Mulai tambahkan kode visualisasi di sini.")

# Contoh sederhana (bisa diganti dengan data real)
data = {'kolom_a': np.random.rand(10), 'kolom_b': np.random.randint(1, 100, 10)}
df = pd.DataFrame(data)

st.subheader("Data Sampel")
st.dataframe(df)