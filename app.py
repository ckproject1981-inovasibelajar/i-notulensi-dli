import streamlit as st
import google.generativeai as genai

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="iNotulensi DLI UM ver 1.0", page_icon="🎙️", layout="wide")

# --- Konfigurasi API ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("API Key belum diset di Streamlit Secrets.")
    st.stop()

# --- CSS Custom ---
st.markdown("""
    <style>
    table { width: 100% !important; border-collapse: collapse; }
    th, td { padding: 12px !important; text-align: left !important; border: 1px solid #ddd !important; }
    th { background-color: #f2f2f2 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- Fungsi Logika AI ---
def generate_minutes(transcript, metadata):
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Anda adalah sekretaris profesional. Susun notulensi rapat berdasarkan data berikut:
    DETAIL RAPAT: {metadata}
    TRANSKRIP RAPAT: {transcript}
    
    Susun dalam format Markdown dengan tabel formal untuk poin pembahasan dan aksi.
    """
    response = model.generate_content(prompt)
    return response.text

# --- Antarmuka Utama ---
# Menambahkan Logo
st.image("https://i.ibb.co.com/23N3kpBY/Logo-DLI.png", width=150)
st.title("iNotulensi DLI UM ver 1.0")

with st.expander("📝 Detail Undangan", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        hari_tanggal = st.text_input("Hari, Tanggal:")
        waktu = st.text_input("Pukul:")
    with col2:
        tempat = st.text_input("Tempat:")
        acara = st.text_input("Acara:")
    pimpinan = st.text_input("Pimpinan Rapat:")
    peserta = st.text_area("Peserta:")

transkrip = st.text_area("Masukkan Transkrip Rapat:", height=300)

if st.button("Generate Notulensi", type="primary"):
    if not transkrip:
        st.error("Mohon isi Transkrip.")
    else:
        metadata = f"Acara: {acara}\nHari/Tanggal: {hari_tanggal}\nWaktu: {waktu}\nTempat: {tempat}\nPimpinan: {pimpinan}\nPeserta: {peserta}"
        try:
            with st.spinner("Memproses notulensi..."):
                hasil = generate_minutes(transkrip, metadata)
            
            st.success("Notulensi berhasil disusun!")
            st.subheader("Hasil Notulensi:")
            st.markdown(hasil)
            
            # --- Fitur Salin ---
            # Catatan: Tombol salin standar Streamlit tidak mendukung copy teks dari variabel Python langsung.
            # Cara terbaik adalah menampilkan code block yang bisa dikopi user dengan mudah.
            st.divider()
            with st.expander("Lihat & Salin Markdown"):
                st.code(hasil, language="markdown")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")