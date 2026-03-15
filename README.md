# 🌍 PyClimaExplorer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pyclimaexplorer-squirtlesquad.streamlit.app/)

**Live Demo URL:** [https://pyclimaexplorer-squirtlesquad.streamlit.app/](https://pyclimaexplorer-squirtlesquad.streamlit.app/)

PyClimaExplorer is a high-performance, interactive climate data visualization dashboard built for the Technex IIT BHU Hackathon. It turns raw NetCDF telemetry into a compelling, cinematic story using 3D spatial mapping and AI-generated narratives.

## 🚀 Key Features

* **3D Spatial Telemetry (XR Ready):** Global hex-bin mapping using PyDeck, layered over a custom Polygon landmask.
* **Universal NetCDF Ingestion:** Upload any `.nc` climate dataset. Our pipeline auto-detects variables, normalizes coordinates (0-360 to -180-180), and handles NaNs.
* **AI Narration Engine:** Powered by Google Gemini 1.5 Pro. It reads the current telemetry and streams highly technical, cinematic climate warnings character-by-character.
* **Responsive UI:** A "Command Center" glassmorphism aesthetic built with Streamlit.

## 🛠️ Tech Stack

* **Frontend & Backend UI:** Streamlit
* **Data Processing:** Xarray, Pandas, NumPy, NetCDF4
* **Visualization:** PyDeck (Deck.GL), Plotly
* **AI Storytelling:** Google Gemini (google-generativeai)

## 💻 Local Setup

1. **Clone the repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up Gemini API Key:**
   Create a `.env` file in the root directory or `.streamlit/secrets.toml` with:
   ```env
   GEMINI_API_KEY="your_api_key_here"
   ```
4. **Run the application:**
   ```bash
   streamlit run app.py
   ```
