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
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# COMPLETE CSS — Sci-Fi HUD + All Components
# ==========================================
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600;1,700&display=swap');

/* ── CSS Variables ── */
:root {
    --neon-cyan: #00f3ff;
    --neon-blue: #003cff;
    --neon-red: #ff3333;
    --neon-orange: #ffaa00;
    --dark-bg: #050914;
    --glass-bg: rgba(10, 15, 30, 0.6);
    --glass-border: rgba(0, 243, 255, 0.2);
}

/* ── Global text defaults ── */
html, body, [class*="css"], p, span, div {
    font-family: 'Chakra Petch', sans-serif !important;
    color: #e0e0e0;
}

/* ── Orbitron for headings ── */
h1, h2, h3, .stMetric [data-testid="stMetricValue"] {
    font-family: 'Chakra Petch', sans-serif !important;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* ── Dark App Background ── */
.stApp {
    background-color: var(--dark-bg) !important;
    background-image:
        radial-gradient(circle at 15% 50%, rgba(0, 60, 255, 0.08), transparent 25%),
        radial-gradient(circle at 85% 30%, rgba(0, 243, 255, 0.08), transparent 25%);
}

/* ── Hide streamlit defaults ── */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* =========================================
   ANIMATIONS
   ========================================= */

/* Title breathing neon pulse */
@keyframes neonPulse {
    0%   { filter: drop-shadow(0 0 4px rgba(0, 243, 255, 0.3)); }
    50%  { filter: drop-shadow(0 0 16px rgba(0, 243, 255, 0.8)) drop-shadow(0 0 30px rgba(0, 60, 255, 0.4)); }
    100% { filter: drop-shadow(0 0 4px rgba(0, 243, 255, 0.3)); }
}

/* Fade-in for main content */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Button pulsing glow */
@keyframes pulseGlow {
    0%   { box-shadow: 0 0 5px rgba(0, 243, 255, 0.2), inset 0 0 5px rgba(0, 243, 255, 0.1); }
    50%  { box-shadow: 0 0 20px rgba(0, 243, 255, 0.6), 0 0 35px rgba(0, 60, 255, 0.3), inset 0 0 10px rgba(0, 243, 255, 0.3); }
    100% { box-shadow: 0 0 5px rgba(0, 243, 255, 0.2), inset 0 0 5px rgba(0, 243, 255, 0.1); }
}

/* HUD Loader scanline */
@keyframes scanline {
    0%   { background-position: 0 -100vh; }
    100% { background-position: 0 100vh; }
}

@keyframes blinkText {
    0%, 100% { opacity: 1; }
    50%      { opacity: 0.3; }
}

@keyframes loaderSlide {
    0%   { left: -60%; }
    100% { left: 100%; }
}

/* =========================================
   MAIN TITLE
   ========================================= */
h1 {
    text-align: center !important;
    font-weight: 900 !important;
    letter-spacing: 4px !important;
    background: linear-gradient(90deg, #ffffff, var(--neon-cyan), var(--neon-blue));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-top: 1rem !important;
    margin-bottom: 0.2rem !important;
    animation: neonPulse 3s ease-in-out infinite;
}

/* Subtitle */
.subtitle-container {
    text-align: center;
    margin-bottom: 2.5rem;
}
.subtitle {
    font-family: 'Chakra Petch', sans-serif !important;
    color: var(--neon-cyan);
    font-size: 1.2rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    text-shadow: 0 0 10px rgba(0, 243, 255, 0.4);
    opacity: 0.85;
}

/* =========================================
   SIDEBAR — Glassmorphism
   ========================================= */
[data-testid="stSidebar"] {
    background: rgba(5, 9, 20, 0.8) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-right: 1px solid var(--glass-border) !important;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label {
    color: var(--neon-cyan) !important;
    font-family: 'Chakra Petch', sans-serif !important;
    letter-spacing: 2px;
    font-size: 0.95rem;
    text-transform: uppercase;
    font-weight: 500;
}

.stSlider [data-testid="stTickBar"] { background: #1a202c !important; }
.stSlider [role="slider"] {
    background-color: var(--neon-cyan) !important;
    box-shadow: 0 0 10px var(--neon-cyan) !important;
}

/* =========================================
   METRIC CARDS (custom HTML)
   ========================================= */
.metric-card {
    background: var(--glass-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    padding: 28px 20px;
    text-align: center;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    margin-bottom: 1rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

/* Sweep light on hover */
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: -100%; width: 50%; height: 100%;
    background: linear-gradient(to right, transparent, rgba(0, 243, 255, 0.08), transparent);
    transform: skewX(-25deg);
    transition: all 0.7s ease;
}

.metric-card:hover {
    transform: translateY(-8px) scale(1.02);
    border-color: var(--neon-cyan);
    box-shadow: 0 12px 35px rgba(0, 243, 255, 0.35), inset 0 0 15px rgba(0, 60, 255, 0.15);
}

.metric-card:hover::before { left: 200%; }

.metric-label {
    font-family: 'Chakra Petch', sans-serif !important;
    font-size: 1.2rem;
    color: #90a4b8;
    text-transform: uppercase;
    letter-spacing: 3px;
    font-weight: 600;
}

.metric-value {
    font-family: 'Chakra Petch', sans-serif !important;
    font-size: 2.8rem;
    font-weight: 700;
    color: var(--neon-cyan);
    text-shadow: 0 0 15px rgba(0, 243, 255, 0.5);
    margin: 10px 0;
    line-height: 1.2;
}

.metric-delta {
    font-family: 'Chakra Petch', sans-serif !important;
    font-size: 0.95rem;
    margin-top: 6px;
    letter-spacing: 1.5px;
    opacity: 0.75;
}

/* =========================================
   SECTION HEADINGS
   ========================================= */
.section-heading {
    font-family: 'Chakra Petch', sans-serif !important;
    color: #b0bec5;
    letter-spacing: 3px;
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 1rem;
    text-transform: uppercase;
}
.section-heading .accent { color: var(--neon-cyan); }

/* =========================================
   BUTTONS — Pulsing Glow
   ========================================= */
.stButton > button {
    background: rgba(5, 10, 25, 0.85) !important;
    color: var(--neon-cyan) !important;
    border: 2px solid var(--neon-cyan) !important;
    border-radius: 8px !important;
    font-family: 'Chakra Petch', sans-serif !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    padding: 12px 24px !important;
    width: 100%;
    transition: all 0.3s ease !important;
    animation: pulseGlow 2s infinite !important;
}

.stButton > button:hover {
    background: var(--neon-cyan) !important;
    color: #000 !important;
    box-shadow: 0 0 25px var(--neon-cyan), 0 0 50px var(--neon-cyan) !important;
    transform: scale(1.03);
    animation: none !important;
}

/* =========================================
   STORY BOX (AI Narrative)
   ========================================= */
.story-box {
    background: rgba(10, 15, 30, 0.55);
    border-left: 4px solid var(--neon-cyan);
    padding: 20px;
    border-radius: 0 12px 12px 0;
    font-family: 'Chakra Petch', sans-serif !important;
    font-size: 1.15rem;
    color: #e2e8f0;
    line-height: 1.7;
    margin-top: 12px;
    box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5), 0 5px 15px rgba(0,0,0,0.3);
    position: relative;
    backdrop-filter: blur(10px);
}

/* Grid overlay on story box */
.story-box::after {
    content: '';
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(rgba(0,243,255,0.04) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0,243,255,0.04) 1px, transparent 1px);
    background-size: 20px 20px;
    pointer-events: none;
    opacity: 0.3;
}

.highlight {
    color: var(--neon-cyan);
    font-weight: 600;
}

/* =========================================
   HUD LOADER
   ========================================= */
.hud-loader {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    text-align: center;
    position: relative;
}

.hud-loader::after {
    content: '';
    position: absolute;
    width: 100%; height: 100%;
    background: repeating-linear-gradient(0deg,
        rgba(0, 243, 255, 0.03) 0px, rgba(0, 243, 255, 0.03) 1px,
        transparent 1px, transparent 4px);
    animation: scanline 4s linear infinite;
    pointer-events: none;
}

.hud-loader-text {
    font-family: 'Chakra Petch', sans-serif !important;
    font-size: 1rem;
    color: var(--neon-cyan);
    letter-spacing: 4px;
    text-transform: uppercase;
    animation: blinkText 1.5s ease-in-out infinite;
    text-shadow: 0 0 10px rgba(0, 243, 255, 0.6);
}

.hud-loader-bar {
    width: 200px; height: 3px;
    background: rgba(0, 243, 255, 0.15);
    border-radius: 3px;
    margin-top: 12px;
    overflow: hidden;
    position: relative;
}

.hud-loader-bar::after {
    content: '';
    position: absolute;
    width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
    animation: loaderSlide 1.2s ease-in-out infinite;
}

/* =========================================
   FADE-IN WRAPPER
   ========================================= */
.main-content-wrapper {
    animation: fadeIn 1.2s ease-out forwards;
}

/* =========================================
   COLOR LEGEND
   ========================================= */
.color-legend {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    margin: 8px 0 4px 0;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.85rem;
    color: #90a4b8;
    letter-spacing: 1px;
}

.legend-swatch {
    width: 14px; height: 14px;
    border-radius: 3px;
    border: 1px solid rgba(255,255,255,0.15);
}

/* =========================================
   STREAMLIT NATIVE METRIC STYLING
   ========================================= */
[data-testid="stMetric"] {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border);
    padding: 15px;
    border-radius: 10px;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease-in-out;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    border: 1px solid rgba(0, 255, 255, 0.8);
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# APPLICATION HEADER
# ==========================================
st.markdown("<h1>🌍 PyClimaExplorer</h1>", unsafe_allow_html=True)
st.markdown("""
<div class='subtitle-container'>
    <span class='subtitle'>Global Climate Telemetry Dashboard // System Online</span>
</div>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR: THE CONTROL HUB
# ==========================================
with st.sidebar:
    st.markdown("""
    <h2 style='font-family: 'Chakra Petch', sans-serif; color: #00f3ff; text-align: center;
    font-size: 1.4rem; margin-bottom: 1.5rem;
    border-bottom: 1px solid rgba(0,243,255,0.3); padding-bottom: 1rem;'>
    ⚙ Control Hub</h2>
    """, unsafe_allow_html=True)

    climate_var = st.selectbox(
        "Climate Variable",
        ("Temperature anomaly", "Precipitation levels", "Wind velocity patterns"),
        help="Select the climate metric to visualize on the 3D map and timeline."
    )

    selected_year = st.slider(
        "Temporal Selection (Year)",
        min_value=1980,
        max_value=2050,
        value=2026,
        step=1,
        help="Drag to select the focus year. The timeline chart will highlight this year."
    )

    st.markdown("---")

    # Quick info about the selected variable
    var_info = {
        "Temperature anomaly": "🌡️ Tracks deviation from the 1951–1980 global baseline average.",
        "Precipitation levels": "🌧️ Measures rainfall volume anomalies across regions.",
        "Wind velocity patterns": "💨 Maps surface wind speed deviations from climatological norms."
    }
    st.markdown(f"""
    <div style='padding: 12px; border: 1px dashed rgba(0, 243, 255, 0.25);
    border-radius: 8px; font-size: 0.95rem; color: #a0aec0; line-height: 1.6;'>
    <strong style='color: #00f3ff;'>{climate_var}</strong><br>
    {var_info[climate_var]}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='padding: 10px; border: 1px dashed rgba(0, 243, 255, 0.3);
    border-radius: 8px; text-align: center;'>
    <span style='color: #00f3ff; font-family: 'Chakra Petch', sans-serif; font-size: 0.75rem;
    letter-spacing: 2px;'>SYSTEM STATUS:
    <span style='color: #00ff00; text-shadow: 0 0 5px #00ff00;'>NOMINAL</span></span>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# HUD LOADING STATE
# ==========================================
loader_placeholder = st.empty()
loader_placeholder.markdown(f"""
<div class="hud-loader">
    <div class="hud-loader-text">Calculating Telemetry: {climate_var}</div>
    <div class="hud-loader-bar"></div>
</div>
""", unsafe_allow_html=True)
time.sleep(0.6)
loader_placeholder.empty()


# ==========================================
# MAIN CONTENT (fade-in wrapper)
# ==========================================
st.markdown("<div class='main-content-wrapper'>", unsafe_allow_html=True)


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


# ==========================================
# TOP ROW: METRIC CARDS
# ==========================================
col1, col2, col3 = st.columns(3)

def metric_card(label, value, delta, color_override=None, delta_color=None):
    val_style = f"style='color: {color_override}; text-shadow: 0 0 18px {color_override};'" if color_override else ""
    d_color = delta_color or "#a0aec0"
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value" {val_style}>{value}</div>
        <div class="metric-delta" style="color: {d_color};">{delta}</div>
    </div>
    """

# Dynamic metric values driven by backend.compute_summary_stats()
stats = backend.compute_summary_stats(climate_var, selected_year)
stats_prev = backend.compute_summary_stats(climate_var, max(selected_year - 10, 1980))  # decade comparison
delta_max = round(stats["max_value"] - stats_prev["max_value"], 2)
delta_sign = "▲" if delta_max >= 0 else "▼"

unit_map = {"Temperature anomaly": "°C", "Precipitation levels": "mm", "Wind velocity patterns": "m/s"}
unit = unit_map.get(climate_var, "")

if is_temp:
    with col1:
        st.markdown(metric_card("Global Max Anomaly", f"{stats['max_value']:+.2f}{unit}",
            f"{delta_sign} {delta_max:+.2f} vs. decade ago", "#ff3333", "#ff6b6b"), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("Anomaly Rate", f"{stats['anomaly_rate']:.1f}%",
            "▲ Critical" if stats['anomaly_rate'] > 30 else "Nominal", "#ffaa00", "#ffd060"), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card("Mean Anomaly", f"{stats['mean_value']:+.2f}{unit}",
            f"σ = {stats['std_value']:.2f}"), unsafe_allow_html=True)
elif is_precip:
    with col1:
        st.markdown(metric_card("Max Precipitation", f"{stats['max_value']:.1f}{unit}",
            f"{delta_sign} {abs(delta_max):.1f}mm vs. decade ago", "#1e90ff", "#5eb3ff"), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("Anomaly Rate", f"{stats['anomaly_rate']:.1f}%",
            "Moderate — watch zone" if stats['anomaly_rate'] > 20 else "Stable", "#ffaa00", "#ffd060"), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card("Mean Precip", f"{stats['mean_value']:.1f}{unit}",
            f"σ = {stats['std_value']:.1f}"), unsafe_allow_html=True)
else:
    with col1:
        st.markdown(metric_card("Peak Wind Speed", f"{stats['max_value']:.1f} {unit}",
            f"{delta_sign} {abs(delta_max):.1f} vs. decade ago", "#dc32dc", "#e080e0"), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("Avg Surface Wind", f"{stats['mean_value']:.1f} {unit}",
            f"{delta_sign} {abs(delta_max):.1f} vs. baseline", "#00f3ff", "#80f9ff"), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card("Anomaly Rate", f"{stats['anomaly_rate']:.1f}%",
            "▲ Rising trend" if stats['anomaly_rate'] > 25 else "Stable"), unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)


# ==========================================
# MIDDLE ROW: SPATIAL VIEW (PyDeck 3D Map)
# ==========================================
st.markdown(f"<div class='section-heading'>Spatial Telemetry: <span class='accent'>{climate_var}</span></div>", unsafe_allow_html=True)

# Color Legend
legend_html = "<div class='color-legend'>"
for color, label in legend_items:
    legend_html += f"<div class='legend-item'><div class='legend-swatch' style='background:{color};'></div>{label}</div>"
legend_html += "</div>"
st.markdown(legend_html, unsafe_allow_html=True)

# ⚙️  Pillar 1+2: Smart Math pipeline → cached spatial DataFrame
df_spatial = backend.get_spatial_dataframe(climate_var, selected_year)

layer = pdk.Layer(
    "HexagonLayer",
    data=df_spatial,
    get_position=["lon", "lat"],
    radius=120000,
    elevation_scale=1000,         # ← was 50000 — subtle raised bumps, not skyscrapers
    elevation_range=[0, 800],     # ← was [0, 3000] — keep pillars compact
    extruded=True,
    pickable=True,
    color_range=map_colors,
)

view_state = pdk.ViewState(
    latitude=20, longitude=0,
    zoom=1.2, pitch=45, bearing=-10,
    # Lock the viewport to prevent weird scrolling artifacts
    min_zoom=0.5, max_zoom=3.5 
)

r = pdk.Deck(
    map_provider="carto",
    map_style=pdk.map_styles.CARTO_DARK,
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": f"{climate_var} — Hex Bin Count: {{elevationValue}}"},
    parameters={"clearColor": [0, 0, 0, 0], "depthTest": True}
)

st.pydeck_chart(r, use_container_width=True, height=480)  # lock map height

# CSS spacer — breathing room between map and bottom row
st.markdown("<div style='margin-bottom: 2.5rem;'></div>", unsafe_allow_html=True)


# ==========================================
# BOTTOM ROW: TEMPORAL CHART + AI NARRATION
# ==========================================
with st.container():
    bottom_col1, bottom_col2 = st.columns([7, 3])

# --- Column 1: Plotly Temporal Time-Series ---
with bottom_col1:
    st.markdown("<div class='section-heading'>Temporal Analysis</div>", unsafe_allow_html=True)

    # Build temporal series from the backend (mean anomaly per year)
    years = np.arange(1980, 2051)
    values = np.array([
        backend.compute_summary_stats(climate_var, int(yr))["mean_value"]
        for yr in years
    ])

    # Per-point diverging marker colors (Temperature mode)
    if is_temp:
        marker_colors = []
        for v in values:
            if v < -0.3:
                marker_colors.append("#1e50dc")
            elif v < 0.3:
                marker_colors.append("#c0c8d0")
            elif v < 0.8:
                marker_colors.append("#ffaa00")
            else:
                marker_colors.append("#ff3333")
    else:
        marker_colors = chart_color

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=years, y=values,
        mode='lines+markers',
        name=climate_var,
        line=dict(color=chart_color, width=3),
        marker=dict(size=7, color=marker_colors, line=dict(width=1, color='rgba(255,255,255,0.3)')),
        fill='tozeroy',
        fillcolor=chart_fill,
        hovertemplate="<b>Year %{x}</b><br>Δ Value: %{y:.3f}<extra></extra>"
    ))

    # Highlight selected year
    fig.add_vline(x=selected_year, line_width=2, line_dash="dash", line_color=vline_color)
    yr_idx = int(np.clip(selected_year - 1980, 0, len(values) - 1))
    fig.add_annotation(
        x=selected_year, y=float(np.max(values)),
        text=f"▼ {selected_year}", showarrow=False, yshift=18,
        font=dict(color=vline_color, family="Chakra Petch, sans-serif", size=16)
    )

    # Add a baseline zero-line for temperature
    if is_temp:
        fig.add_hline(y=0, line_width=1, line_dash="dot", line_color="rgba(255,255,255,0.2)",
                      annotation_text="Baseline", annotation_font_color="rgba(255,255,255,0.4)")

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Chakra Petch, sans-serif", color="#e2e8f0", size=15),
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(
            showgrid=True, gridcolor='rgba(0, 243, 255, 0.06)',
            title=dict(text="Year", font=dict(size=18, family="Chakra Petch, sans-serif")),
            tickfont=dict(size=14)
        ),
        yaxis=dict(
            showgrid=True, gridcolor='rgba(0, 243, 255, 0.06)',
            title=dict(text=f"Anomaly ({unit})", font=dict(size=18, family="Chakra Petch, sans-serif")),
            tickfont=dict(size=14)
        ),
        hovermode="x unified",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(0,0,0,0)'
        )
    )

    st.plotly_chart(fig, use_container_width=True)


# --- Column 2: AI Story Mode ---
with bottom_col2:
    st.markdown("<div class='section-heading' style='text-align: center;'>AI Narration</div>", unsafe_allow_html=True)

    if st.button("⚡ Generate AI Climate Report"):
        # 🧠 Pillar 3: Gemini LLM streaming (falls back gracefully)
        ai_stats = backend.compute_summary_stats(climate_var, selected_year)
        max_anom = ai_stats["max_value"]
        anomaly_rate = ai_stats["anomaly_rate"]

        severity = "critical" if anomaly_rate > 40 else "moderate" if anomaly_rate > 20 else "stable"
        severity_color = "#ff3333" if severity == "critical" else "#ffaa00" if severity == "moderate" else "#00ff00"

        # Severity header (HTML styled)
        st.markdown(f"""
        <div class='story-box'>
            <strong style='color: {severity_color};'>⬤ THREAT LEVEL: {severity.upper()}</strong><br><br>
        </div>
        """, unsafe_allow_html=True)

        # Stream the AI warning character-by-character (typing effect)
        st.write_stream(
            backend.stream_climate_warning(
                target_year=selected_year,
                max_anomaly=float(max_anom),
                region_name="Global Equatorial Zone",
            )
        )
    else:
        st.markdown("""
        <div class='story-box' style='text-align: center; opacity: 0.7;'>
            <div style='margin-bottom: 15px; color: #00f3ff; font-family: 'Chakra Petch', sans-serif; font-size: 0.9rem;
            letter-spacing: 2px;'>[ AWAITING COMMAND ]</div>
            <div style='font-size: 1rem; color: #90a4b8;'>
            Click the button above to generate an AI-powered climate intelligence report
            for the current variable and year selection.
            </div>
        </div>
        """, unsafe_allow_html=True)


st.markdown("</div>", unsafe_allow_html=True)
