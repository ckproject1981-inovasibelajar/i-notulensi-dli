import streamlit as st
import google.generativeai as genai

# --- Konfigurasi Halaman (Harus dipanggil pertama kali) ---
st.set_page_config(page_title="AI Meeting Scribe Pro", page_icon="🎙️", layout="wide")

# --- Konfigurasi API (Menggunakan Secrets) ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("API Key belum diset di Streamlit Secrets. Silakan tambahkan GEMINI_API_KEY di dashboard Streamlit.")
    st.stop()

# --- CSS Custom (Tabel & UI) ---
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
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_models = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-1.5-pro']
    model_to_use = next((m for m in target_models if m in models), models[0])
    model = genai.GenerativeModel(model_to_use)
    
    prompt = f"""
    Anda adalah sekretaris profesional.Anda menguasai manajemen perguruan tinggi, kurikulum perguruan tinggi dan memahami struktur tapat di perguruan tinggi. Susun notulensi rapat berdasarkan data berikut:
    DETAIL RAPAT: {metadata}
    TRANSKRIP RAPAT: {transcript}
    
    Susun dalam format Markdown dengan tabel formal. Pastikan setiap poin pembahasan dan aksi tertulis dengan jelas.
    """
    response = model.generate_content(prompt)
    return response.text

# --- Antarmuka Utama ---
st.title("🎙️ AI Meeting Scribe Pro")

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
            
            st.divider()
            if st.button("📋 Salin Teks ke Clipboard"):
                st.write(f'<script>navigator.clipboard.writeText(`{hasil}`)</script>', unsafe_allow_html=True)
                st.toast("Teks berhasil disalin ke clipboard!")
                
            with st.expander("Lihat Format Mentah (Markdown)"):
                st.code(hasil, language="markdown")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")