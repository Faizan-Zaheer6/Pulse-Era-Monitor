import streamlit as st
import pandas as pd
import time
import requests
from datetime import datetime
from fpdf import FPDF
import io
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIG ---
st.set_page_config(page_title="PULSE ERA", layout="wide")
st_autorefresh(interval=10000, key="pulse_sync") 

# --- 2. ANIMATED NEON UI CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #0b0d17, #1a1c2c, #051937, #0b0d17);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 251, 255, 0.3);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    .stButton>button, .stDownloadButton>button {
        background: linear-gradient(90deg, #00FBFF, #0080FF) !important;
        color: black !important;
        font-weight: 900 !important;
        border: none !important;
        border-radius: 10px !important;
        transition: 0.3s;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px #00FBFF;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PDF GENERATOR ---
def generate_pdf(node, history):
    node_data = history[history['URL'] == node]
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, f"PULSE ERA | NODE REPORT", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(100, 10, f"Target: {node}", ln=True)
    pdf.cell(100, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(5)
    
    pdf.set_fill_color(0, 251, 255)
    pdf.cell(90, 10, "Timestamp", border=1, fill=True)
    pdf.cell(90, 10, "Latency (ms)", border=1, fill=True)
    pdf.ln()
    
    for _, row in node_data.tail(10).iterrows():
        pdf.cell(90, 10, str(row['Time']), border=1)
        pdf.cell(90, 10, str(row['Latency']), border=1)
        pdf.ln()
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- 4. PERSISTENT STATE ---
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Time', 'URL', 'Latency'])

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("⚡ PULSE ERA")
    new_url = st.text_input("Deploy New Probe", placeholder="example.com")
    if st.button("INITIALIZE"):
        if new_url:
            try:
                requests.post("http://127.0.0.1:8000/add-website", json={"url": new_url}, timeout=2)
                st.success("Syncing...")
                time.sleep(1)
                st.rerun()
            except: 
                st.error("Backend Offline")

# --- 6. MAIN DASHBOARD ---
st.title("⚡ Global Grid Monitor")

try:
    res = requests.get("http://127.0.0.1:8000/status", timeout=8)
    if res.status_code == 200:
        raw_data = res.json()
        if raw_data:
            # Create DataFrame
            df = pd.DataFrame(raw_data)
            
            # 🔥 Fix: Rename columns to match the Frontend logic
            df = df.rename(columns={
                'Latency_ms': 'Latency (ms)', 
                'HTTP_Code': 'HTTP Code',
                'Last_Check': 'Time'
            })
            
            # Data Cleanup
            df['HTTP Code'] = df['HTTP Code'].astype(str)

            # Metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("Live Nodes", len(df))
            # Calculate Avg Latency safely
            avg_lat = round(df['Latency (ms)'].mean(), 2) if 'Latency (ms)' in df.columns else 0
            c2.metric("Avg Latency", f"{avg_lat} ms")
            c3.metric("Grid Status", "ACTIVE")

            # Graph logic
            st.subheader("📈 Signal Stability Waveforms")
            now = datetime.now().strftime("%H:%M:%S")
            
            # Update Persistent History
            new_recs = [{'Time': now, 'URL': r['URL'], 'Latency': r['Latency (ms)']} for _, r in df.iterrows()]
            st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame(new_recs)], ignore_index=True).tail(200)
            
            if not st.session_state.history.empty:
                chart_pivoted = st.session_state.history.pivot_table(index='Time', columns='URL', values='Latency', aggfunc='mean')
                st.line_chart(chart_pivoted)

            # Table display
            st.subheader("🌐 Grid Nodes Status")
            
            # Naya Tareeka (Warning khatam ho jayegi)
            st.dataframe(df, width="stretch", hide_index=True)

            # Export Intelligence
            st.markdown("---")
            st.subheader("📥 Export Intelligence")
            target = st.selectbox("Select Node", df['URL'].unique())
            col_csv, col_pdf = st.columns(2)
            
            with col_csv:
                csv_data = st.session_state.history[st.session_state.history['URL'] == target].to_csv(index=False).encode('utf-8')
                st.download_button("📊 Download CSV", csv_data, f"{target}.csv", "text/csv")
            
            with col_pdf:
                pdf_data = generate_pdf(target, st.session_state.history)
                st.download_button("📩 Download PDF", pdf_data, f"{target}.pdf", "application/pdf")
        else:
            st.warning("🔄 Waiting for Grid Data...")
    else:
        st.error(f"Backend Error: {res.status_code}")
except Exception as e:
    st.info("📡 Scanning for Grid Signals...")