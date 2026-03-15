# 🌍 PyClimaExplorer — Next-Gen Spatial Climate Intelligence

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pyclimaexplorer-squirtlesquad.streamlit.app/)

**Live Demo URL:** [https://pyclimaexplorer-squirtlesquad.streamlit.app/](https://pyclimaexplorer-squirtlesquad.streamlit.app/)

PyClimaExplorer is a high-performance interactive visualizer designed to turn raw, multi-dimensional climate data into a compelling spatial story. Built within 24 hours for the **Technex '26 Hack-it-out Hackathon**, it bridges the gap between complex NetCDF (`.nc`) files and intuitive public outreach.

## 🚀 Key Features

* **Lightning-Fast Data Slicing:** Instantly process and filter climate variables like Surface Temperature and Precipitation using an optimized `xarray` pipeline.
* **3D Global Rendering:** Interactive 3D globe projection of climate anomalies using PyDeck for high-impact spatial visualization.
* **AI Story Mode:** Integrated Google Gemini API that auto-generates human-readable narratives and guided tours of climate shifts based on the raw telemetry data.
* **Comparison Mode:** Dual-view synchronized interface for decadal analysis (e.g., comparing 1990 vs. 2024 trends).
* **Spatial Computing Edge:** Optimized for WebXR and Meta Quest 3 in Passthrough Mode, allowing hands-free interaction with 3D data in a Mixed Reality environment.

## 🛠️ Tech Stack

* **Data Engine:** Python, Xarray, Pandas, NumPy
* **Frontend:** Streamlit (Glassmorphism UI)
* **Visualization:** PyDeck (3D Spatial) and Plotly (Temporal Line Plots)
* **AI:** Google Gemini 1.5 Pro

## 📦 Local Setup & Installation

To run PyClimaExplorer locally, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Prajjawal-Vaishya/PyClimaExplorer.git
   cd PyClimaExplorer
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables:**
   Create a `.env` file or export your Gemini API key:
   ```bash
   export GEMINI_API_KEY='your_gemini_api_key_here'
   ```

4. **Run the App:**
   ```bash
   streamlit run app.py
   ```

## 📂 Data Sources

The application is built to ingest standard NetCDF (`.nc`) climate datasets. For testing, you can use:
* **CESM** (Community Earth System Model) outputs.
* **ERA5** Reanalysis data.

## 👥 Team: Squirtle Squad
* **Prajjawal Vaishya**
