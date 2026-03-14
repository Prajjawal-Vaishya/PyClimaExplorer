"""
╔══════════════════════════════════════════════════════════════════════╗
║  PyClimaExplorer — app.py (Frontend Shell)                          ║
║  Tab-Based, Progressive-Disclosure UI for Climate Anomaly Viz       ║
║                                                                      ║
║  Architecture:                                                       ║
║    Tab 1 → 🌍 Main View    (3D Globe + Metric Cards)                ║
║    Tab 2 → 🔀 Compare      (Split-Screen Year Comparison)           ║
║    Tab 3 → 📖 Story Mode   (AI Narration + Temporal Chart)          ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
import plotly.graph_objects as go
import time
import backend  # ← PyClimaExplorer backend engine (3 pillars)

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="PyClimaExplorer",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# COMPLETE CSS — Glassmorphism + Dark Mode
# ==========================================
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

/* ── CSS Variables ── */
:root {
    --neon-cyan: #00f3ff;
    --neon-blue: #003cff;
    --neon-red: #ff3333;
    --neon-orange: #ffaa00;
    --neon-green: #00ff88;
    --dark-bg: #050914;
    --card-bg: rgba(10, 15, 30, 0.55);
    --glass-border: rgba(0, 243, 255, 0.15);
    --text-primary: #e8ecf1;
    --text-secondary: #8a99ad;
}

/* ── Global Defaults ── */
html, body, [class*="css"], p, span, div, label {
    font-family: 'Inter', 'Chakra Petch', sans-serif !important;
    color: var(--text-primary);
}

h1, h2, h3, h4 {
    font-family: 'Chakra Petch', sans-serif !important;
    letter-spacing: 1.5px;
}

/* ── Dark Background ── */
.stApp {
    background-color: var(--dark-bg) !important;
    background-image:
        radial-gradient(ellipse at 10% 40%, rgba(0, 60, 255, 0.06), transparent 50%),
        radial-gradient(ellipse at 90% 20%, rgba(0, 243, 255, 0.05), transparent 50%);
}

/* ── Hide Streamlit Chrome ── */
#MainMenu, header, footer { visibility: hidden; }

/* ── ANIMATIONS ── */
@keyframes neonPulse {
    0%   { filter: drop-shadow(0 0 4px rgba(0, 243, 255, 0.3)); }
    50%  { filter: drop-shadow(0 0 18px rgba(0, 243, 255, 0.7)) drop-shadow(0 0 30px rgba(0, 60, 255, 0.3)); }
    100% { filter: drop-shadow(0 0 4px rgba(0, 243, 255, 0.3)); }
}

@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes pulseGlow {
    0%   { box-shadow: 0 0 5px rgba(0, 243, 255, 0.2); }
    50%  { box-shadow: 0 0 20px rgba(0, 243, 255, 0.5), 0 0 40px rgba(0, 60, 255, 0.2); }
    100% { box-shadow: 0 0 5px rgba(0, 243, 255, 0.2); }
}

@keyframes scanline {
    0%   { background-position: 0 -100vh; }
    100% { background-position: 0 100vh; }
}

@keyframes loaderSlide {
    0%   { left: -60%; }
    100% { left: 100%; }
}

@keyframes breathe {
    0%, 100% { opacity: 0.6; }
    50%      { opacity: 1; }
}

/* ── Title ── */
.hero-title {
    text-align: center;
    font-family: 'Chakra Petch', sans-serif !important;
    font-weight: 800;
    font-size: 2.8rem;
    letter-spacing: 5px;
    text-transform: uppercase;
    background: linear-gradient(135deg, #ffffff 0%, var(--neon-cyan) 50%, var(--neon-blue) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding: 0.8rem 0 0.2rem 0;
    animation: neonPulse 3s ease-in-out infinite;
    margin-bottom: 0;
}

.hero-subtitle {
    text-align: center;
    font-family: 'Chakra Petch', sans-serif !important;
    color: var(--neon-cyan);
    font-size: 0.95rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    opacity: 0.7;
    margin-bottom: 1.8rem;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(5, 9, 20, 0.85) !important;
    backdrop-filter: blur(25px) !important;
    -webkit-backdrop-filter: blur(25px) !important;
    border-right: 1px solid var(--glass-border) !important;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stRadio label {
    color: var(--neon-cyan) !important;
    font-family: 'Chakra Petch', sans-serif !important;
    letter-spacing: 1.5px;
    font-size: 0.85rem;
    text-transform: uppercase;
    font-weight: 500;
}

.stSlider [role="slider"] {
    background-color: var(--neon-cyan) !important;
    box-shadow: 0 0 8px var(--neon-cyan) !important;
}

/* ── Metric Cards ── */
.metric-card {
    background: var(--card-bg);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 24px 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 0.8rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    animation: fadeSlideIn 0.6s ease-out both;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: -100%; width: 50%; height: 100%;
    background: linear-gradient(to right, transparent, rgba(0, 243, 255, 0.06), transparent);
    transform: skewX(-25deg);
    transition: all 0.6s ease;
}
.metric-card:hover {
    transform: translateY(-6px) scale(1.015);
    border-color: var(--neon-cyan);
    box-shadow: 0 12px 40px rgba(0, 243, 255, 0.25);
}
.metric-card:hover::before { left: 200%; }

.metric-label {
    font-family: 'Chakra Petch', sans-serif !important;
    font-size: 0.95rem;
    color: var(--text-secondary);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.metric-value {
    font-family: 'Chakra Petch', sans-serif !important;
    font-size: 2.4rem;
    font-weight: 700;
    color: var(--neon-cyan);
    text-shadow: 0 0 15px rgba(0, 243, 255, 0.4);
    line-height: 1;
    margin-bottom: 8px;
}
.metric-delta {
    font-size: 0.85rem;
    color: var(--text-secondary);
}

/* ── Section Headings ── */
.section-heading {
    font-family: 'Chakra Petch', sans-serif !important;
    font-size: 1.3rem;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--text-primary);
    margin: 1.2rem 0 0.8rem 0;
}
.section-heading .accent { color: var(--neon-cyan); }
.section-heading .accent-orange { color: var(--neon-orange); }

/* ── Color Legend ── */
.color-legend {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    margin-bottom: 12px;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.82rem;
    color: var(--text-secondary);
}
.legend-swatch {
    width: 14px; height: 14px;
    border-radius: 3px;
    border: 1px solid rgba(255,255,255,0.1);
}

/* ── Story Box ── */
.story-box {
    background: var(--card-bg);
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    padding: 24px;
    line-height: 1.75;
    font-size: 1rem;
    animation: fadeSlideIn 0.5s ease-out both;
}

/* ── Step Labels ── */
.step-label {
    font-family: 'Chakra Petch', sans-serif !important;
    color: var(--neon-cyan);
    font-size: 0.78rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 6px;
    opacity: 0.8;
}

/* ── Info Box ── */
.info-glass {
    background: var(--card-bg);
    border: 1px dashed var(--glass-border);
    border-radius: 12px;
    padding: 16px 20px;
    font-size: 0.92rem;
    color: var(--text-secondary);
    line-height: 1.6;
}
.info-glass strong { color: var(--neon-cyan); }

/* ── Status Pill ── */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.72rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-family: 'Chakra Petch', sans-serif !important;
    border: 1px solid;
}
.status-online {
    color: var(--neon-green);
    border-color: rgba(0, 255, 136, 0.3);
    background: rgba(0, 255, 136, 0.06);
    animation: breathe 2.5s infinite;
}
.status-uploaded {
    color: var(--neon-orange);
    border-color: rgba(255, 170, 0, 0.3);
    background: rgba(255, 170, 0, 0.06);
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Chakra Petch', sans-serif !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    font-size: 0.85rem;
    color: var(--text-secondary) !important;
    border-radius: 10px 10px 0 0;
    padding: 8px 20px;
    background: rgba(10, 15, 30, 0.3);
    border: 1px solid transparent;
}

.stTabs [aria-selected="true"] {
    color: var(--neon-cyan) !important;
    background: var(--card-bg) !important;
    border-color: var(--glass-border) !important;
    border-bottom: 2px solid var(--neon-cyan) !important;
}

/* ── Upload Zone ── */
.upload-zone {
    background: var(--card-bg);
    border: 2px dashed rgba(0, 243, 255, 0.25);
    border-radius: 16px;
    padding: 28px 20px;
    text-align: center;
    transition: all 0.3s ease;
}
.upload-zone:hover {
    border-color: var(--neon-cyan);
    box-shadow: 0 0 20px rgba(0, 243, 255, 0.1);
}

/* ── Comparison Badge ── */
.compare-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 6px;
    font-family: 'Chakra Petch', sans-serif !important;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.badge-a {
    background: rgba(255, 170, 0, 0.15);
    color: var(--neon-orange);
    border: 1px solid rgba(255, 170, 0, 0.3);
}
.badge-b {
    background: rgba(0, 243, 255, 0.15);
    color: var(--neon-cyan);
    border: 1px solid rgba(0, 243, 255, 0.3);
}

/* ── HUD Loader ── */
.hud-loader {
    text-align: center;
    padding: 26px 0;
    animation: fadeSlideIn 0.3s ease-out;
}
.hud-loader-text {
    font-family: 'Chakra Petch', sans-serif !important;
    color: var(--neon-cyan);
    font-size: 0.82rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    animation: breathe 1.2s infinite;
    margin-bottom: 12px;
}
.hud-loader-bar {
    width: 180px;
    height: 3px;
    background: rgba(0, 243, 255, 0.15);
    border-radius: 2px;
    margin: 0 auto;
    position: relative;
    overflow: hidden;
}
.hud-loader-bar::after {
    content: '';
    position: absolute;
    top: 0;
    width: 60%;
    height: 100%;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
    animation: loaderSlide 1s ease-in-out infinite;
}

/* ── Button Styling ── */
.stButton > button {
    font-family: 'Chakra Petch', sans-serif !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    font-size: 0.85rem;
    border: 1px solid var(--glass-border);
    border-radius: 10px;
    background: var(--card-bg) !important;
    color: var(--neon-cyan) !important;
    padding: 10px 24px;
    transition: all 0.3s ease;
}
.stButton > button:hover {
    border-color: var(--neon-cyan);
    box-shadow: 0 0 16px rgba(0, 243, 255, 0.3);
    transform: translateY(-2px);
}
.stButton > button:active {
    transform: translateY(0);
}

/* ── Compact file uploader ── */
[data-testid="stFileUploader"] section {
    border-radius: 12px;
    border: 1px dashed var(--glass-border);
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================
st.markdown("<div class='hero-title'>PYCLIMAEXPLORER</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Global Climate Telemetry Dashboard // System Online</div>", unsafe_allow_html=True)


# ==========================================
# SIDEBAR — THE CONTROL HUB
# ==========================================
with st.sidebar:
    st.markdown("""
    <h2 style='font-family: Chakra Petch, sans-serif; color: #00f3ff; text-align: center;
    font-size: 1.3rem; margin-bottom: 1.5rem;
    border-bottom: 1px solid rgba(0,243,255,0.2); padding-bottom: 1rem;'>
    CONTROL HUB</h2>
    """, unsafe_allow_html=True)

    # ── Step 1: Feed Data ──
    st.markdown("<div class='step-label'>Step 1 → Feed Data</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload a NetCDF (.nc) climate dataset",
        type=["nc"],
        help="Drop your .nc file here. We'll auto-detect variables like Temperature, Precipitation, or Wind."
    )

    # Process uploaded file
    use_uploaded = False
    if uploaded_file is not None:
        if "uploaded_nc_processed" not in st.session_state or st.session_state.get("uploaded_nc_name") != uploaded_file.name:
            with st.spinner("Parsing your dataset..."):
                success = backend.process_uploaded_nc(uploaded_file)
                if success:
                    st.session_state["uploaded_nc_processed"] = True
                    st.session_state["uploaded_nc_name"] = uploaded_file.name
                    st.success(f"[ OK ] Loaded: **{uploaded_file.name}**")
                else:
                    st.session_state["uploaded_nc_processed"] = False

    if st.session_state.get("uploaded_nc_processed"):
        st.markdown(f"""
        <div class='status-pill status-uploaded'>
            DATASET: {st.session_state.get('uploaded_nc_name', 'Dataset')}
        </div>
        """, unsafe_allow_html=True)
        use_uploaded = st.checkbox("Use uploaded dataset", value=True,
                                   help="Toggle to switch between your uploaded data and the built-in synthetic simulation.")

    st.markdown("---")

    # ── Step 2: Choose What to See ──
    st.markdown("<div class='step-label'>Step 2 → Choose What to See</div>", unsafe_allow_html=True)

    climate_var = st.selectbox(
        "Climate Variable",
        ("Temperature anomaly", "Precipitation levels", "Wind velocity patterns"),
        help="Pick the climate metric to visualize."
    )

    st.markdown("---")

    # ── Step 3: Pick a Year ──
    st.markdown("<div class='step-label'>Step 3 → Pick a Year</div>", unsafe_allow_html=True)

    selected_year = st.slider(
        "Year",
        min_value=1980,
        max_value=2050,
        value=2026,
        step=1,
        help="Slide to travel through time and see how the climate changes."
    )

    st.markdown("---")

    # ── Quick Info ──
    var_info = {
        "Temperature anomaly": "Deviation from the 1951–1980 global baseline average.",
        "Precipitation levels": "Rainfall volume anomalies across regions.",
        "Wind velocity patterns": "Surface wind speed deviations from norms."
    }
    st.markdown(f"""
    <div class='info-glass'>
        <strong>{climate_var}</strong><br>
        {var_info[climate_var]}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Status pill
    st.markdown("""
    <div style='text-align: center;'>
        <span class='status-pill status-online'>System Nominal</span>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# HUD LOADING STATE
# ==========================================
loader_placeholder = st.empty()
loader_placeholder.markdown(f"""
<div class="hud-loader">
    <div class="hud-loader-text">Initializing Telemetry: {climate_var}</div>
    <div class="hud-loader-bar"></div>
</div>
""", unsafe_allow_html=True)
time.sleep(0.45)
loader_placeholder.empty()


# ==========================================
# VARIABLE-AWARE COLOR ENGINE
# ==========================================
is_temp = climate_var == "Temperature anomaly"
is_precip = climate_var == "Precipitation levels"
is_wind = climate_var == "Wind velocity patterns"

if is_temp:
    map_colors = [
        [30, 80, 220, 200],   [100, 160, 255, 220],
        [220, 220, 230, 200], [255, 180, 50, 230],
        [255, 80, 0, 255],    [220, 0, 30, 255]
    ]
    chart_color, chart_fill, vline_color = "#ff3333", "rgba(255, 51, 51, 0.1)", "#ffaa00"
    legend_items = [("#1e50dc", "Cooling"), ("#c0c8d0", "Baseline"), ("#ffaa00", "Warm"), ("#ff3333", "Hot")]
elif is_precip:
    map_colors = [
        [180, 160, 100, 150], [100, 180, 160, 180],
        [50, 180, 200, 210],  [30, 140, 220, 230],
        [20, 80, 220, 255],   [10, 30, 180, 255]
    ]
    chart_color, chart_fill, vline_color = "#1e90ff", "rgba(30, 144, 255, 0.1)", "#1e90ff"
    legend_items = [("#b4a064", "Dry"), ("#32b4a0", "Moderate"), ("#1e90ff", "Heavy")]
else:
    map_colors = [
        [50, 180, 100, 150],  [80, 220, 180, 180],
        [0, 243, 255, 210],   [140, 100, 255, 230],
        [220, 50, 220, 255],  [255, 30, 120, 255]
    ]
    chart_color, chart_fill, vline_color = "#00f3ff", "rgba(0, 243, 255, 0.1)", "#8c64ff"
    legend_items = [("#32b464", "Calm"), ("#00f3ff", "Moderate"), ("#dc32dc", "Extreme")]

unit_map = {"Temperature anomaly": "°C", "Precipitation levels": "mm", "Wind velocity patterns": "m/s"}
unit = unit_map.get(climate_var, "")


# ==========================================
# REUSABLE COMPONENTS
# ==========================================

def metric_card(label, value, delta, color_override=None, delta_color=None):
    """Generate an HTML metric card."""
    val_style = f"style='color: {color_override}; text-shadow: 0 0 18px {color_override};'" if color_override else ""
    d_color = delta_color or "#8a99ad"
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value" {val_style}>{value}</div>
        <div class="metric-delta" style="color: {d_color};">{delta}</div>
    </div>
    """


def render_metric_cards(year_val):
    """Render top-row metric cards for a given year."""
    stats = backend.compute_summary_stats(climate_var, year_val, use_uploaded_data=use_uploaded)
    stats_prev = backend.compute_summary_stats(climate_var, max(year_val - 10, 1980), use_uploaded_data=use_uploaded)
    delta_max = round(stats["max_value"] - stats_prev["max_value"], 2)
    delta_sign = "▲" if delta_max >= 0 else "▼"

    c1, c2, c3 = st.columns(3)
    if is_temp:
        with c1:
            st.markdown(metric_card("Global Max Anomaly", f"{stats['max_value']:+.2f}{unit}",
                f"{delta_sign} {delta_max:+.2f} vs. decade ago", "#ff3333", "#ff6b6b"), unsafe_allow_html=True)
        with c2:
            st.markdown(metric_card("Anomaly Rate", f"{stats['anomaly_rate']:.1f}%",
                "▲ Critical" if stats['anomaly_rate'] > 30 else "Nominal", "#ffaa00", "#ffd060"), unsafe_allow_html=True)
        with c3:
            st.markdown(metric_card("Mean Anomaly", f"{stats['mean_value']:+.2f}{unit}",
                f"σ = {stats['std_value']:.2f}"), unsafe_allow_html=True)
    elif is_precip:
        with c1:
            st.markdown(metric_card("Max Precipitation", f"{stats['max_value']:.1f}{unit}",
                f"{delta_sign} {abs(delta_max):.1f}mm vs. decade ago", "#1e90ff", "#5eb3ff"), unsafe_allow_html=True)
        with c2:
            st.markdown(metric_card("Anomaly Rate", f"{stats['anomaly_rate']:.1f}%",
                "Watch zone" if stats['anomaly_rate'] > 20 else "Stable", "#ffaa00", "#ffd060"), unsafe_allow_html=True)
        with c3:
            st.markdown(metric_card("Mean Precip", f"{stats['mean_value']:.1f}{unit}",
                f"σ = {stats['std_value']:.1f}"), unsafe_allow_html=True)
    else:
        with c1:
            st.markdown(metric_card("Peak Wind Speed", f"{stats['max_value']:.1f} {unit}",
                f"{delta_sign} {abs(delta_max):.1f} vs. decade ago", "#dc32dc", "#e080e0"), unsafe_allow_html=True)
        with c2:
            st.markdown(metric_card("Avg Surface Wind", f"{stats['mean_value']:.1f} {unit}",
                f"{delta_sign} {abs(delta_max):.1f} vs. baseline", "#00f3ff", "#80f9ff"), unsafe_allow_html=True)
        with c3:
            st.markdown(metric_card("Anomaly Rate", f"{stats['anomaly_rate']:.1f}%",
                "▲ Rising" if stats['anomaly_rate'] > 25 else "Stable"), unsafe_allow_html=True)


def render_pydeck_map(year_val, map_height=500):
    """Render a PyDeck 3D globe for a given year."""
    # ── BACKEND HOOK: get_spatial_dataframe ──
    df_spatial = backend.get_spatial_dataframe(climate_var, year_val, use_uploaded_data=use_uploaded)

    layer = pdk.Layer(
        "HexagonLayer",
        data=df_spatial,
        get_position=["lon", "lat"],
        radius=120000,
        elevation_scale=1000,
        elevation_range=[0, 800],
        extruded=True,
        pickable=True,
        color_range=map_colors,
    )
    view_state = pdk.ViewState(
        latitude=20, longitude=0,
        zoom=1.2, pitch=45, bearing=-10,
        min_zoom=0.5, max_zoom=3.5
    )
    deck = pdk.Deck(
        map_provider="carto",
        map_style=pdk.map_styles.CARTO_DARK,
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": f"{climate_var} — Hex Bin Count: {{elevationValue}}"},
        parameters={"clearColor": [0, 0, 0, 0], "depthTest": True}
    )
    st.pydeck_chart(deck, use_container_width=True, height=map_height)


def render_legend():
    """Render the color legend bar."""
    legend_html = "<div class='color-legend'>"
    for color, label in legend_items:
        legend_html += f"<div class='legend-item'><div class='legend-swatch' style='background:{color};'></div>{label}</div>"
    legend_html += "</div>"
    st.markdown(legend_html, unsafe_allow_html=True)


def render_temporal_chart(highlight_year, chart_height=380):
    """Render the Plotly time-series chart."""
    years = np.arange(1980, 2051)
    # ── BACKEND HOOK: compute_summary_stats ──
    values = np.array([
        backend.compute_summary_stats(climate_var, int(yr), use_uploaded_data=use_uploaded)["mean_value"]
        for yr in years
    ])

    # Per-point marker colors (diverging for temperature)
    if is_temp:
        marker_colors = []
        for v in values:
            if v < -0.3:    marker_colors.append("#1e50dc")
            elif v < 0.3:   marker_colors.append("#c0c8d0")
            elif v < 0.8:   marker_colors.append("#ffaa00")
            else:           marker_colors.append("#ff3333")
    else:
        marker_colors = chart_color

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=values,
        mode='lines+markers',
        name=climate_var,
        line=dict(color=chart_color, width=3),
        marker=dict(size=6, color=marker_colors, line=dict(width=1, color='rgba(255,255,255,0.2)')),
        fill='tozeroy',
        fillcolor=chart_fill,
        hovertemplate="<b>Year %{x}</b><br>Δ Value: %{y:.3f}<extra></extra>"
    ))

    # Highlight selected year
    fig.add_vline(x=highlight_year, line_width=2, line_dash="dash", line_color=vline_color)
    fig.add_annotation(
        x=highlight_year, y=float(np.max(values)),
        text=f"▼ {highlight_year}", showarrow=False, yshift=16,
        font=dict(color=vline_color, family="Chakra Petch, sans-serif", size=15)
    )

    if is_temp:
        fig.add_hline(y=0, line_width=1, line_dash="dot", line_color="rgba(255,255,255,0.15)",
                      annotation_text="Baseline", annotation_font_color="rgba(255,255,255,0.3)")

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Chakra Petch, sans-serif", color="#e2e8f0", size=14),
        margin=dict(l=0, r=0, t=30, b=0),
        height=chart_height,
        xaxis=dict(
            showgrid=True, gridcolor='rgba(0, 243, 255, 0.05)',
            title=dict(text="Year", font=dict(size=16, family="Chakra Petch, sans-serif")),
            tickfont=dict(size=13)
        ),
        yaxis=dict(
            showgrid=True, gridcolor='rgba(0, 243, 255, 0.05)',
            title=dict(text=f"Anomaly ({unit})", font=dict(size=16, family="Chakra Petch, sans-serif")),
            tickfont=dict(size=13)
        ),
        hovermode="x unified",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right", x=1,
            bgcolor='rgba(0,0,0,0)'
        )
    )
    st.plotly_chart(fig, use_container_width=True)


# ==========================================
# TABS — The 3 Views
# ==========================================
tab_main, tab_compare, tab_story = st.tabs([
    "MAIN VIEW",
    "COMPARISON MODE",
    "STORY MODE"
])


# ──────────────────────────────────────────
# TAB 1: MAIN VIEW (3D Globe + Metrics)
# ──────────────────────────────────────────
with tab_main:
    # Metric Cards
    render_metric_cards(selected_year)

    st.markdown("<br>", unsafe_allow_html=True)

    # Section Heading
    st.markdown(f"""
    <div class='section-heading'>
        Spatial Telemetry: <span class='accent'>{climate_var}</span>
        <span style='float: right; font-size: 0.7em; color: #8a99ad;'>Year {selected_year}</span>
    </div>
    """, unsafe_allow_html=True)

    render_legend()
    render_pydeck_map(selected_year, map_height=520)

    # Spacer
    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

    # Temporal Chart
    st.markdown("<div class='section-heading'>Temporal Analysis</div>", unsafe_allow_html=True)
    render_temporal_chart(selected_year)


# ──────────────────────────────────────────
# TAB 2: COMPARISON MODE (Split Screen)
# ──────────────────────────────────────────
with tab_compare:
    st.markdown("""
    <div class='section-heading'>
        Side-by-Side <span class='accent'>Temporal Comparison</span>
    </div>
    <p style='color: #8a99ad; font-size: 0.9rem; margin-bottom: 1.2rem;'>
        Compare two different years to see how climate anomalies have shifted over time.
        Use the sliders below to pick any two points in history.
    </p>
    """, unsafe_allow_html=True)

    # Two year selectors
    sel_col1, sel_col2 = st.columns(2)
    with sel_col1:
        st.markdown("<span class='compare-badge badge-a'>A — Past</span>", unsafe_allow_html=True)
        year_a = st.slider("Year A", 1980, 2050, 1990, key="compare_year_a",
                           help="Select the first year for comparison.")
    with sel_col2:
        st.markdown("<span class='compare-badge badge-b'>B — Future</span>", unsafe_allow_html=True)
        year_b = st.slider("Year B", 1980, 2050, 2040, key="compare_year_b",
                           help="Select the second year for comparison.")

    st.markdown("---")

    # Split-screen maps
    map_a, map_b = st.columns(2)

    with map_a:
        st.markdown(f"""
        <div class='section-heading' style='font-size: 1rem;'>
            <span class='compare-badge badge-a'>A</span>
            <span class='accent-orange'> {climate_var}</span>
            <span style='color: #8a99ad;'>— Year {year_a}</span>
        </div>
        """, unsafe_allow_html=True)
        render_legend()
        render_pydeck_map(year_a, map_height=420)

        # Metrics for Year A
        stats_a = backend.compute_summary_stats(climate_var, year_a, use_uploaded_data=use_uploaded)
        st.markdown(f"""
        <div class='info-glass' style='margin-top: 0.8rem;'>
            <strong>Max:</strong> {stats_a['max_value']:+.2f}{unit} &nbsp;|&nbsp;
            <strong>Mean:</strong> {stats_a['mean_value']:+.2f}{unit} &nbsp;|&nbsp;
            <strong>Rate:</strong> {stats_a['anomaly_rate']:.1f}%
        </div>
        """, unsafe_allow_html=True)

    with map_b:
        st.markdown(f"""
        <div class='section-heading' style='font-size: 1rem;'>
            <span class='compare-badge badge-b'>B</span>
            <span class='accent'> {climate_var}</span>
            <span style='color: #8a99ad;'>— Year {year_b}</span>
        </div>
        """, unsafe_allow_html=True)
        render_legend()
        render_pydeck_map(year_b, map_height=420)

        # Metrics for Year B
        stats_b = backend.compute_summary_stats(climate_var, year_b, use_uploaded_data=use_uploaded)
        st.markdown(f"""
        <div class='info-glass' style='margin-top: 0.8rem;'>
            <strong>Max:</strong> {stats_b['max_value']:+.2f}{unit} &nbsp;|&nbsp;
            <strong>Mean:</strong> {stats_b['mean_value']:+.2f}{unit} &nbsp;|&nbsp;
            <strong>Rate:</strong> {stats_b['anomaly_rate']:.1f}%
        </div>
        """, unsafe_allow_html=True)

    # Delta Summary
    st.markdown("---")
    delta_mean = round(stats_b["mean_value"] - stats_a["mean_value"], 3)
    delta_max_cmp = round(stats_b["max_value"] - stats_a["max_value"], 3)
    delta_rate = round(stats_b["anomaly_rate"] - stats_a["anomaly_rate"], 1)

    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown(metric_card("Δ Mean Anomaly", f"{delta_mean:+.3f}{unit}",
            f"Year {year_a} → {year_b}", "#ffaa00" if delta_mean > 0 else "#1e90ff"), unsafe_allow_html=True)
    with d2:
        st.markdown(metric_card("Δ Peak Anomaly", f"{delta_max_cmp:+.3f}{unit}",
            f"Year {year_a} → {year_b}", "#ff3333" if delta_max_cmp > 0 else "#1e90ff"), unsafe_allow_html=True)
    with d3:
        st.markdown(metric_card("Δ Anomaly Rate", f"{delta_rate:+.1f}%",
            f"Year {year_a} → {year_b}", "#ff3333" if delta_rate > 0 else "#00ff88"), unsafe_allow_html=True)


# ──────────────────────────────────────────
# TAB 3: STORY MODE (AI + Timeline)
# ──────────────────────────────────────────
with tab_story:
    story_col1, story_col2 = st.columns([6, 4])

    with story_col1:
        st.markdown("<div class='section-heading'>Temporal Analysis</div>", unsafe_allow_html=True)
        render_temporal_chart(selected_year, chart_height=400)

    with story_col2:
        st.markdown("""
        <div class='section-heading' style='text-align: center;'>
            AI <span class='accent'>Climate Intelligence</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("GENERATE AI CLIMATE REPORT", use_container_width=True):
            # ── BACKEND HOOK: compute_summary_stats + stream_climate_warning ──
            ai_stats = backend.compute_summary_stats(climate_var, selected_year, use_uploaded_data=use_uploaded)
            max_anom = ai_stats["max_value"]
            anomaly_rate = ai_stats["anomaly_rate"]

            severity = "critical" if anomaly_rate > 40 else "moderate" if anomaly_rate > 20 else "stable"
            severity_color = "#ff3333" if severity == "critical" else "#ffaa00" if severity == "moderate" else "#00ff88"

            st.markdown(f"""
            <div class='story-box'>
                <strong style='color: {severity_color};'>⬤ THREAT LEVEL: {severity.upper()}</strong><br><br>
            </div>
            """, unsafe_allow_html=True)

            # Stream the AI narration character-by-character
            st.write_stream(
                backend.stream_climate_warning(
                    target_year=selected_year,
                    max_anomaly=float(max_anom),
                    region_name="Global Equatorial Zone",
                )
            )
        else:
            st.markdown(f"""
            <div class='story-box' style='text-align: center; padding: 40px 24px;'>
                <div style='color: #00f3ff; font-family: Chakra Petch, sans-serif; font-size: 1.2rem;
                letter-spacing: 4px; margin-bottom: 12px; text-transform: uppercase;'>[ NEURAL LINK ACTIVE ]</div>
                <div style='color: #00f3ff; font-family: Chakra Petch, sans-serif; font-size: 0.82rem;
                letter-spacing: 2.5px; margin-bottom: 12px; text-transform: uppercase;'>[ Awaiting Command ]</div>
                <div style='font-size: 0.92rem; color: #8a99ad; line-height: 1.6;'>
                Press the button above to generate an AI-powered climate intelligence report
                for <strong style='color: #00f3ff;'>{climate_var}</strong> in <strong style='color: #ffaa00;'>Year {selected_year}</strong>.
                </div>
            </div>
            """, unsafe_allow_html=True)


    # Guided Tour Section (below the main story content)
    st.markdown("---")
    st.markdown("""
    <div class='section-heading'>
        🎯 Quick <span class='accent'>Climate Snapshots</span>
    </div>
    """, unsafe_allow_html=True)

    snap_cols = st.columns(4)
    climate_events = [
        ("Pinatubo", 1991, "Volcanic cooling dip"),
        ("El Niño", 1998, "Record spike year"),
        ("Acceleration", 2016, "Hottest year recorded"),
        ("Projection", 2045, "Near +1.5°C threshold"),
    ]
    for i, (label, event_year, desc) in enumerate(climate_events):
        with snap_cols[i]:
            if st.button(f"{label}", key=f"snap_{event_year}", use_container_width=True):
                snap_stats = backend.compute_summary_stats(climate_var, event_year, use_uploaded_data=use_uploaded)
                st.markdown(f"""
                <div class='info-glass' style='margin-top: 8px; text-align: center;'>
                    <strong style='color: #ffaa00;'>Year {event_year}</strong><br>
                    <span style='font-size: 0.85rem;'>{desc}</span><br><br>
                    <strong>Max:</strong> {snap_stats['max_value']:+.2f}{unit}<br>
                    <strong>Mean:</strong> {snap_stats['mean_value']:+.2f}{unit}<br>
                    <strong>Rate:</strong> {snap_stats['anomaly_rate']:.1f}%
                </div>
                """, unsafe_allow_html=True)
            else:
                st.caption(desc)
