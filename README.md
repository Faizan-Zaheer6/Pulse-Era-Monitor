# ⚡ PULSE ERA | Global Grid Monitor

A futuristic, real-time website monitoring dashboard built with FastAPI and Streamlit.

## 🚀 Features
- Real-time Asynchronous Probing
- Animated Neon UI with Glassmorphism
- PDF & CSV Intelligence Reports
- Live Latency Waveforms

## 🛠️ Setup
1. `pip install -r requirements.txt`
2. Run Backend: `python -m uvicorn main:app --reload`
3. Run Frontend: `streamlit run app.py`

4. ## 🐳 Docker Support
This project is fully containerized. You can pull the image directly from Docker Hub:
```bash
docker pull fzd6/pulse-era-app:latest
docker run -p 8000:8000 fzd6/pulse-era-app:latest
