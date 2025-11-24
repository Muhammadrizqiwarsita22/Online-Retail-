import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Retail Analytics Dashboard",
    page_icon="🛍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. SIDEBAR LAYOUT (RAPI & MINIMALIS)
# ==========================================
with st.sidebar:
    st.markdown("## 🛍 Retail Dashboard")
    st.markdown("---")

    # Bagian 1: Input
    st.markdown("<p class='sidebar-category'>DATA INPUT</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload File CSV", type=["csv"], key="uploader_retail")
    
    # Bagian 2: Tema
    st.markdown("---")
    st.markdown("<p class='sidebar-category'>TEMA</p>", unsafe_allow_html=True)
    theme_selection = st.radio(
        "Pilih Tema", 
        ["Gelap", "Terang"], 
        index=0, 
        label_visibility="collapsed", 
        key="theme_selector"
    )
    
    # Bagian 3: Profile
    st.markdown("---") 
    st.markdown("<p class='sidebar-category'>PROFILE</p>", unsafe_allow_html=True)
    
    col_logo, col_text = st.columns([1, 3])
    with col_logo:
        st.image("https://muslimahnews.id/wp-content/uploads/2022/07/logo_usk.png", width=50)
    with col_text:
        st.markdown("**Kelompok AHAHAYY**")
        st.caption("Data Analytics")

    # --- BAGIAN 4: PROFILE (Opsional, dirapikan) ---
    st.markdown("---")
    st.caption("© 2025 Retail Analytics Project")


# ==========================================
# 3. LOGIKA WARNA (VARIABEL UNTUK CSS)
# ==========================================
if theme_selection == "Gelap":
    chart_template = "plotly_dark"
    main_bg_color = "#0E1117"
    sidebar_bg_color = "#262730"
    card_bg_color = "#1F2937"
    text_color = "#FAFAFA"
    divider_color = "rgba(255, 255, 255, 0.15)"
    
    metric_title_color = "#FAFAFA"
    metric_value_color = "#FAFAFA"
    border_color = "#374151"
    header_color = "#60A5FA"
    metric_shadow = "2px 2px 5px rgba(255,255,255,0.05)"
    delta_color = "lightgreen"
    input_bg_color = "#262730"
    input_hover_bg_color = "#374151" 
    uploader_shadow_hover = "0 0 8px rgba(255,255,255,0.15)"
    
else: # Mode Terang
    chart_template = "plotly_white"
    main_bg_color = "#FFFFFF"
    sidebar_bg_color = "#FFFFFF"
    card_bg_color = "#FFFFFF"
    text_color = "#000000"
    divider_color = "rgba(0, 0, 0, 0.15)"

    metric_title_color = "#000000"
    metric_value_color = "#000000"
    border_color = "#E5E7EB"
    header_color = "#1E3D59"
    metric_shadow = "0 4px 6px -1px rgba(0, 0, 0, 0.1)"
    delta_color = "green"
    input_bg_color = "#FFFFFF"
    input_hover_bg_color = "#F0F2F6" 
    uploader_shadow_hover = "0 0 12px rgba(0,0,0,0.15)"

# ==========================================
# 4. INJECT CSS (KODE BARU ANDA + FIX SIDEBAR)
# ==========================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

/* --- KODE CSS UTAMA DARI ANDA --- */
html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; color: {text_color} !important; }}
.stApp {{ background-color: {main_bg_color} !important; color: {text_color} !important; }}
section[data-testid="stSidebar"] {{ background-color: {sidebar_bg_color} !important; color: {text_color} !important; border-right: 1px solid {divider_color}; }}
header[data-testid="stHeader"] {{ background-color: {main_bg_color} !important; }}

div[data-testid="metric-container"] {{
    background-color: {card_bg_color} !important; border: 1px solid {border_color} !important;
    padding: 15px; border-radius: 10px; box-shadow: {metric_shadow};
}}
div[data-testid="metric-container"] > div > div:nth-child(1) p, div[data-testid="stMetricLabel"] {{
    color: {text_color} !important; font-weight: 600;
}}
div[data-testid="metric-container"] > div > div:nth-child(2) div, div[data-testid="stMetricValue"] {{
    color: {text_color} !important;
}}
div[data-testid="stMetricDelta"] svg {{ fill: {delta_color} !important; }}

[data-testid="stFileUploader"] section {{
    background-color: {input_bg_color} !important;
    border: 1px dashed {border_color} !important;
    transition: all 0.3s ease;
}}
[data-testid="stFileUploader"] section:hover,
[data-testid="stFileUploader"] section:active {{
    background-color: {input_hover_bg_color} !important;
    border-color: {header_color} !important;
    box-shadow: {uploader_shadow_hover} !important;
    cursor: pointer;
}}

hr {{ border-top: 1px solid {divider_color} !important; opacity:1 !important; margin:1.5rem 0; }}
h1,h2,h3,h4,h5,h6 {{ color: {header_color} !important; }}
.stDataFrame, .stTable {{ color: {text_color} !important; }}
button[data-baseweb="tab"] div p {{ font-family: 'Poppins', sans-serif !important; font-weight: 600; color: {text_color} !important; }}

/* FIX SEMUA TEKS ABU PADA PLOTLY / TAB / DATAFRAME */
* {{ color: inherit !important; }}
g.xtick text, g.ytick text {{ fill: {text_color} !important; }}
g.legend text {{ fill: {text_color} !important; }}
.dataframe th, .dataframe td {{ color: {text_color} !important; }}
label, span, p {{ color: {text_color} !important; }}

/* --- TAMBAHAN: AGAR SIDEBAR TETAP RAPI (Meniru Referensi) --- */
.sidebar-category {{
    font-size: 12px;
    font-weight: 700 !important;
    color: #888888 !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 5px;
    margin-top: 20px;
}}
div[role="radiogroup"] label > div:first-child {{
    background-color: transparent;
    border: 2px solid {text_color};
}}
div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child {{
    background-color: #FF4B4B !important;
    border-color: #FF4B4B !important;
}}
/* ------------------------------------------------------- */

</style>
""", unsafe_allow_html=True)

# ==========================================
# 5. FUNGSI DATA PROCESSING
# ==========================================
@st.cache_data
def load_and_clean_data(file):
    df = pd.read_csv(file)
    df['Customer ID'].fillna('Unknown', inplace=True)
    df['Description'] = df.groupby('StockCode')['Description'] \
        .transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else 'Unknown'))
    df = df.drop_duplicates()
    Q1 = df['Quantity'].quantile(0.25)
    Q3 = df['Quantity'].quantile(0.75)
    IQR = Q3 - Q1
    fence_low = Q1 - 1.5 * IQR
    fence_high = Q3 + 1.5 * IQR
    df = df.loc[(df['Quantity'] >= fence_low) & (df['Quantity'] <= fence_high)]
    Q1_p = df['Price'].quantile(0.25)
    Q3_p = df['Price'].quantile(0.75)
    IQR_p = Q3_p - Q1_p
    fence_low_p = Q1_p - 1.5 * IQR_p
    fence_high_p = Q3_p + 1.5 * IQR_p
    df = df.loc[(df['Price'] >= fence_low_p) & (df['Price'] <= fence_high_p)]
    df = df[(df['Price'] > 0) & (df['Quantity'] > 0)]
    df = df[df['Invoice'].str[0] != 'C']
    df = df[df['Customer ID'] != '-1']   
    df['Sales'] = df['Quantity'] * df['Price']
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    return df

# ==========================================
# 6. DASHBOARD CONTENT
# ==========================================

st.title("📊 Executive Retail Overview")
st.markdown("Dashboard interaktif KPI penjualan ritel online.")

if uploaded_file is not None:
    try:
        with st.spinner('Sedang memproses data sesuai algoritma...'):
            df_cleaned = load_and_clean_data(uploaded_file)
        
        # --- SECTION A: KEY METRICS ---
        st.markdown("### 🚀 Performance Highlights")
        m1, m2, m3, m4 = st.columns(4)
        
        total_sales = df_cleaned['Sales'].sum()
        total_trx = df_cleaned['Invoice'].nunique()
        avg_sales = df_cleaned['Sales'].mean()
        total_cust = df_cleaned['Customer ID'].nunique()

        m1.metric("Total Pendapatan", f"£ {total_sales:,.0f}", delta="Revenue")
        m2.metric("Total Transaksi", f"{total_trx:,}", delta="Invoices")
        m3.metric("Rata-rata Basket Size", f"£ {avg_sales:.2f}")
        m4.metric("Total Pelanggan", f"{total_cust:,}", delta="Active Users")
        
        st.markdown("---")

        # --- SECTION B: TABS ANALISIS ---
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📄 Data Source", 
            "📈 Tren Penjualan", 
            "🌍 Geografi", 
            "📦 Produk", 
            "👥 Segmentasi RFM",
            "💡 Rekomendasi"
        ])

        # === TAB 1: DATA SOURCE ===
        with tab1:
            st.markdown("### 📋 Tinjauan Data Transaksi (Dataset Preview)")
            st.caption(f"Dataset yang telah dibersihkan berisi *{df_cleaned.shape[0]:,} baris* data transaksi.")
            
            search_query = st.text_input(
                "🔍 Cari Data (Invoice, Nama Produk, Negara, atau ID):", 
                placeholder="Ketik kata kunci pencarian di sini..."
            )
            
            if search_query:
                mask = df_cleaned.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
                df_display = df_cleaned[mask]
                st.write(f"Menampilkan **{df_display.shape[0]}** hasil pencarian untuk: *'{search_query}'*")
            else:
                df_display = df_cleaned.head(10)
            
            st.dataframe(df_display, use_container_width=True)
            
            st.divider()
            with st.expander("📚 Kamus Data & Penjelasan Variabel"):
                st.markdown("Tabel berikut menjelaskan atribut-atribut yang digunakan dalam analisis ini:")
                data_dict = {
                    "Nama Variabel": ["Invoice", "StockCode", "Description", "Quantity", "InvoiceDate", "Price", "Customer ID", "Country", "Sales"],
                    "Definisi & Tipe Data": [
                        "Kode unik faktur. (Object)", "Kode identitas produk. (Object)", "Nama produk. (Object)", 
                        "Volume beli. (Int64)", "Waktu transaksi. (Datetime)", "Harga satuan. (Float64)", 
                        "ID pelanggan. (Object)", "Negara. (Object)", "Total nilai (Qty x Price). (Float64)"
                    ]
                }
                df_dict = pd.DataFrame(data_dict)
                st.dataframe(df_dict, hide_index=True, use_container_width=True)

        # === TAB 2: TREN PENJUALAN ===
        with tab2:
            st.subheader("Analisis Tren Penjualan Bulanan")
            st.markdown("""
            Grafik di bawah ini memvisualisasikan **fluktuasi pendapatan bulanan** (Revenue) sepanjang periode data. 
            Analisis ini penting untuk memahami *pola musiman (seasonality)*, mengukur pertumbuhan bisnis, 
            serta mengevaluasi efektivitas strategi pemasaran pada bulan-bulan tertentu.
            """)
            
            df_trend = df_cleaned.set_index('InvoiceDate').resample('M').agg({'Sales': 'sum'}).reset_index()
            best_month_row = df_trend.loc[df_trend['Sales'].idxmax()]
            best_month_name = best_month_row['InvoiceDate'].strftime('%B %Y') 
            best_month_val = best_month_row['Sales']
            
            st.markdown(f"""
            > 📈 **Highlight Performa:** > Puncak penjualan tertinggi tercatat pada bulan **{best_month_name}**, 
            > di mana total pendapatan mencapai **£ {best_month_val:,.0f}**.
            """)
            
            fig_trend = px.line(
                df_trend,
                x='InvoiceDate', y='Sales',
                title='Tren Penjualan Bulanan (Total Revenue)',
                markers=True,
                color_discrete_sequence=['#1f77b4'],
                template=chart_template
            )
            
            fig_trend.update_layout(
                xaxis_title='Bulan Transaksi',
                yaxis_title='Total Penjualan (dalam £)',
                xaxis_tickformat='%b %Y',
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Poppins", color=text_color),
                title_font=dict(color=text_color, size=18),
                xaxis=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color), gridcolor=divider_color),
                yaxis=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color), gridcolor=divider_color)
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            st.info("💡 *INSIGHT:* Tren penjualan menunjukkan pola musiman dengan peningkatan signifikan menjelang akhir tahun.")

        # === TAB 3: GEOGRAFI ===
        with tab3:
            st.subheader("Analisis Geografi") 
            st.markdown("""
            Visualisasi ini memetakan distribusi penjualan berdasarkan negara asal pelanggan. 
            Data ini krusial untuk menentukan strategi **ekspansi pasar internasional** dan **logistik pengiriman**.
            """)
            
            country_sales = df_cleaned.groupby('Country')['Sales'].sum().sort_values(ascending=False)
            country_sales_top10 = country_sales.drop('United Kingdom', errors='ignore').head(10).reset_index()
            country_sales_top10['Sales'] = country_sales_top10['Sales'].round(0).astype(int)
            
            if not country_sales_top10.empty:
                top_c_name = country_sales_top10.iloc[0]['Country']
                top_c_val = country_sales_top10.iloc[0]['Sales']
                
                st.markdown(f"""
                > 🌍 **Market Leader Internasional:** > Di luar Inggris (UK), pasar terbesar Anda adalah **{top_c_name}** dengan total kontribusi pendapatan sebesar **£ {top_c_val:,.0f}**.
                """)

            fig_country = px.bar(
                country_sales_top10,
                x='Country', y='Sales',
                title='Top 10 Negara (Selain UK) Berdasarkan Total Penjualan',
                labels={'Country':'Negara', 'Sales':'Total Penjualan (dalam £)'},
                text='Sales',
                color_discrete_sequence=['#1f77b4'],
                template=chart_template
            )
            fig_country.update_traces(texttemplate='%{text:,}', textposition='outside')
            
            fig_country.update_layout(
                xaxis_tickangle=-45,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Poppins", color=text_color),
                title_font=dict(color=text_color, size=18),
                xaxis=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color), gridcolor=divider_color),
                yaxis=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color), gridcolor=divider_color)
            )
            st.plotly_chart(fig_country, use_container_width=True)
            st.info("💡 *INSIGHT:* Fokuskan kampanye pemasaran lokal (bahasa & mata uang) pada 3 negara teratas untuk ROI yang lebih baik.")

        # === TAB 4: PRODUK ===
        with tab4:
            st.subheader("Analisis Produk")
            st.markdown("""
            Analisis ini membantu Anda mengidentifikasi **Pareto Product**: barang mana yang paling laku (secara volume) 
            dan barang mana yang paling menguntungkan (secara revenue).
            """)
            
            top_qty_df = df_cleaned.groupby('Description')['Quantity'].sum().nlargest(1).reset_index()
            top_rev_df = df_cleaned.groupby('Description')['Sales'].sum().nlargest(1).reset_index()
            best_qty_name = top_qty_df.iloc[0]['Description']
            best_rev_name = top_rev_df.iloc[0]['Description']
            
            st.markdown(f"""
            > 📦 **Produk Jagoan:**
            > * **Paling Laris (Qty):** *{best_qty_name}* (Traffic Maker).
            > * **Paling Menguntungkan (Rev):** *{best_rev_name}* (Revenue Generator).
            """)
            
            col_prod1, col_prod2 = st.columns(2)
            
            with col_prod1:
                top_quantity = df_cleaned.groupby('Description')['Quantity'].sum().nlargest(10).sort_values(ascending=True).reset_index()
                fig_qty = px.bar(
                    top_quantity,
                    x='Quantity', y='Description',
                    orientation='h',
                    title='Top 10 Produk Berdasarkan Total Kuantitas',
                    labels={'Description':'Deskripsi', 'Quantity':'Total Kuantitas'},
                    text='Quantity',
                    color_discrete_sequence=['#1f77b4'],
                    template=chart_template
                )
                fig_qty.update_traces(texttemplate='%{text:,}', textposition='outside')
                
                fig_qty.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Poppins", color=text_color),
                    title_font=dict(color=text_color, size=16),
                    xaxis=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color), gridcolor=divider_color),
                    yaxis=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color))
                )
                st.plotly_chart(fig_qty, use_container_width=True)
                
            with col_prod2:
                top_revenue = df_cleaned.groupby('Description')['Sales'].sum().nlargest(10).sort_values(ascending=True).reset_index()
                top_revenue['Sales'] = top_revenue['Sales'].round(0).astype(int)
                fig_rev = px.bar(
                    top_revenue,
                    x='Sales', y='Description',
                    orientation='h',
                    title='Top 10 Produk Berdasarkan Total Pendapatan',
                    labels={'Description':'Deskripsi', 'Sales':'Total Pendapatan (£)'},
                    text='Sales',
                    color_discrete_sequence=['#1f77b4'],
                    template=chart_template
                )
                fig_rev.update_traces(texttemplate='%{text:,}', textposition='outside')
                
                fig_rev.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Poppins", color=text_color),
                    title_font=dict(color=text_color, size=16),
                    xaxis=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color), gridcolor=divider_color),
                    yaxis=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color))
                )
                st.plotly_chart(fig_rev, use_container_width=True)

            st.info("💡 *INSIGHT STRATEGI:* Gunakan produk 'Traffic Maker' (High Qty) sebagai pancingan promosi untuk mendorong penjualan produk 'Revenue Generator' (High Sales) melalui teknik bundling.")

        # === TAB 5: SEGMENTASI RFM ===
        with tab5:
            st.subheader("Segmentasi Pelanggan (RFM Analysis)")
            st.markdown("""
            Metode **RFM (Recency, Frequency, Monetary)** digunakan untuk mengelompokkan perilaku pelanggan. 
            Ini membantu Anda membedakan antara pelanggan VIP, pelanggan baru, dan pelanggan yang berpotensi pergi (Churn).
            """)
            
            max_date = df_cleaned['InvoiceDate'].max()
            reference_date = max_date + pd.Timedelta(days=1)
            rfm_df = df_cleaned.groupby('Customer ID').agg(
                Recency=('InvoiceDate', lambda x: (reference_date - x.max()).days),
                Frequency=('Invoice', 'nunique'),
                Monetary=('Sales', 'sum')
            ).reset_index()

            rfm_df['R_Rank'] = rfm_df['Recency'].rank(pct=True, method='first')
            rfm_df['F_Rank'] = rfm_df['Frequency'].rank(pct=True, method='first')
            rfm_df['M_Rank'] = rfm_df['Monetary'].rank(pct=True, method='first')
            rfm_df['R_Score'] = pd.cut(rfm_df['R_Rank'], bins=5, labels=[5, 4, 3, 2, 1], include_lowest=True).astype(int)
            rfm_df['F_Score'] = pd.cut(rfm_df['F_Rank'], bins=5, labels=[1, 2, 3, 4, 5], include_lowest=True).astype(int)
            rfm_df['M_Score'] = pd.cut(rfm_df['M_Rank'], bins=5, labels=[1, 2, 3, 4, 5], include_lowest=True).astype(int)

            def rfm_segment(row):
                r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
                if r == 5 and f == 5 and m == 5: return 'Champions (Terbaik)'
                elif r >= 4 and f >= 4 and m >= 4: return 'Loyal Customers (Setia)'
                elif r <= 2 and f <= 2 and m <= 2: return 'At Risk (Berisiko Hilang)'
                elif r >= 4 and f <= 2 and m <= 2: return 'New Customers (Baru)'
                elif r <= 2 and f >= 4 and m >= 4: return 'Can\'t Lose Them (Berharga)'
                else: return 'Standard (Rata-rata)'

            rfm_df['Segment'] = rfm_df.apply(rfm_segment, axis=1)
            champions_count = rfm_df[rfm_df['Segment'] == 'Champions (Terbaik)'].shape[0]
            
            st.markdown(f"""
            > 🏆 **Status Pelanggan VIP:** > Saat ini terdapat **{champions_count} pelanggan** dalam kategori *Champions*. 
            > Mereka membeli baru-baru ini, sangat sering, dan dengan nominal besar. Pertahankan mereka!
            """)
            
            col_rfm1, col_rfm2 = st.columns(2)
            
            with col_rfm1:
                segment_counts = rfm_df['Segment'].value_counts().reset_index()
                segment_counts.columns = ['Segment', 'Count']
                fig_seg = px.bar(
                    segment_counts,
                    x='Segment', y='Count',
                    title='Distribusi Segmen Pelanggan RFM',
                    labels={'Segment':'Segmen Pelanggan', 'Count':'Jumlah Pelanggan'},
                    text='Count',
                    color_discrete_sequence=['#1f77b4'],
                    template=chart_template
                )
                fig_seg.update_traces(texttemplate='%{text:,}', textposition='outside')
                
                fig_seg.update_layout(
                    xaxis_tickangle=-45, 
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Poppins", color=text_color),
                    title_font=dict(color=text_color, size=16),
                    xaxis=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color), gridcolor=divider_color),
                    yaxis=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color), gridcolor=divider_color)
                )
                st.plotly_chart(fig_seg, use_container_width=True)
            
            with col_rfm2:
                segment_monetary = rfm_df.groupby('Segment')['Monetary'].mean().round(0).astype(int).sort_values(ascending=False).reset_index()
                segment_monetary.columns = ['Segment', 'MeanMonetary']
                fig_mon = px.bar(
                    segment_monetary,
                    x='Segment', y='MeanMonetary',
                    title='Rata-rata Pengeluaran (Monetary) per Segmen',
                    labels={'Segment':'Segmen Pelanggan', 'MeanMonetary':'Rata-rata Pengeluaran (£)'},
                    text='MeanMonetary',
                    color_discrete_sequence=['#1f77b4'],
                    template=chart_template
                )
                fig_mon.update_traces(texttemplate='%{text:,}', textposition='outside')
                
                fig_mon.update_layout(
                    xaxis_tickangle=-45, 
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Poppins", color=text_color),
                    title_font=dict(color=text_color, size=16),
                    xaxis=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color), gridcolor=divider_color),
                    yaxis=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color), gridcolor=divider_color)
                )
                st.plotly_chart(fig_mon, use_container_width=True)
            st.success("Strategi: Fokus pada *Champions (Terbaik)* dan *Loyal Customers (Setia)* untuk menjaga stabilitas pendapatan.")

        # === TAB 6: REKOMENDASI BISNIS ===
        with tab6:
            st.subheader("Kesimpulan & Rekomendasi Strategis")
            
            top_country_name = df_cleaned[df_cleaned['Country'] != 'United Kingdom']['Sales'].sum()
            top_country_idx = df_cleaned.groupby('Country')['Sales'].sum().drop('United Kingdom', errors='ignore').idxmax()
            top_product_name = df_cleaned.groupby('Description')['Quantity'].sum().idxmax()
            rfm_check = df_cleaned.groupby('Customer ID').agg({
                'InvoiceDate': lambda x: (reference_date - x.max()).days,
                'Invoice': 'nunique',
                'Sales': 'sum'
            })
            avg_recency = rfm_check['InvoiceDate'].mean()
            
            with st.container():
                st.markdown("#### 🔍 Temuan Utama (Key Findings)")
                col_findings1, col_findings2 = st.columns(2)
                with col_findings1:
                    st.info(f"""
                    **1. Produk Paling Diminati**
                    \nProduk **"{top_product_name}"** adalah item dengan volume penjualan tertinggi. Ini adalah 'Traffic Maker' utama toko Anda.
                    """)
                with col_findings2:
                    st.warning(f"""
                    **2. Pasar Internasional Potensial**
                    \nDi luar UK, negara **{top_country_idx}** menunjukkan kontribusi pendapatan terbesar. Ini menandakan adanya basis pelanggan setia di wilayah tersebut.
                    """)

            st.markdown("---")
            st.markdown("#### 🚀 Rekomendasi Prioritas Aksi")
            col_rec1, col_rec2 = st.columns(2)
            
            with col_rec1:
                st.markdown("##### 🛒 Strategi Produk & Stok")
                st.markdown(f"""
                * **Amankan Stok Utama:** Pastikan stok *{top_product_name}* tidak pernah kosong (Out of Stock), karena produk ini memancing pembelian produk lain.
                * **Bundling Strategy:** Buat paket bundling produk terlaris dengan produk yang kurang laku (slow-moving) untuk meningkatkan perputaran inventaris.
                * **Analisis Musiman:** Berdasarkan grafik tren, siapkan stok 2x lipat menjelang akhir tahun (Q4) untuk mengantisipasi lonjakan permintaan.
                """)
            with col_rec2:
                st.markdown("##### 📢 Strategi Pemasaran & Pelanggan")
                st.markdown(f"""
                * **Program Loyalitas:** Fokuskan budget marketing pada segmen *'Champions'* & *'Loyal'* (RFM). Berikan mereka akses *early-bird* untuk produk baru.
                * **Ekspansi Wilayah:** Tingkatkan iklan digital yang ditargetkan khusus ke wilayah **{top_country_idx}** untuk memaksimalkan penetrasi pasar global.
                * **Win-Back Campaign:** Untuk pelanggan yang sudah lama tidak belanja (> {int(avg_recency)} hari), kirimkan email 'We Miss You' dengan voucher diskon khusus.
                """)

            st.markdown("---")
            st.markdown("#### 🤖 Automated Recommendation System")
            rec_data = {
                "Kategori": ["Inventory", "Customer Retention", "Pricing", "Expansion"],
                "Status": ["Aman", "Perlu Perhatian", "Stabil", "Peluang Tinggi"],
                "Rekomendasi AI": [
                    f"Pertahankan level stok untuk {top_product_name}.",
                    "Segmen 'At Risk' meningkat, segera aktifkan email marketing.",
                    "Harga rata-rata stabil, tidak perlu diskon besar-besaran.",
                    f"Fokus promosi bahasa lokal untuk negara {top_country_idx}."
                ]
            }
            rec_df = pd.DataFrame(rec_data)
            st.dataframe(
                rec_df, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "Status": st.column_config.TextColumn(
                        "Status Indikator",
                        help="Status kesehatan metrik saat ini",
                        validate="^[A-Za-z0-9 ]+$"
                    )
                }
            )

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses data: {e}")

else:
    st.info("Silakan upload file CSV retail untuk menampilkan dashboard.")