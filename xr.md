# PyClimaExplorer: Mixed Reality Deployment Guide

This document outlines the exact technical execution and judging pitch for deploying PyClimaExplorer as a Spatial Computing Dashboard using the Meta Quest 3, completely bypassing the instability of native VR while maximizing the immersion of the user.

## The Core Concept: The Spatial Command Center
We are bypassing the instability of native VR to create a Mixed Reality Spatial Dashboard. Instead of attempting to render a glitchy 3D world that users must stand inside, we are turning the real world into an analyst's command center. The user remains fully grounded in the physical hackathon hall but interacts with a massive, floating, interactive data interface.

---

## 1. The Visual Experience (What the Judge Sees)

When the judge puts on the Meta Quest 3, they will experience the following sequence:

*   **Physical Grounding:** They will see the actual room around them through the headset's Passthrough Mode. This immediately eliminates the claustrophobia and motion sickness associated with standard VR.
*   **The Floating Interface:** Hovering in the center of the room is a curved, IMAX-scale web browser window.
*   **The Transparency Hack:** Because we injected pitch-black CSS (`#050914`) into the Streamlit app, the background of the browser blends into the room. The UI elements—the sliders, the AI text, and the map—appear as glowing, borderless neon holograms floating in mid-air.
*   **The 3D Extrusion:** In the center of this floating dashboard is the PyDeck globe. Because we set the camera `pitch=60` and enabled 3D extrusion with aggressively scaled math, the climate anomalies do not look like flat colors. They look like physical, 3D architectural bars jutting out toward the judge.

## 2. The Interaction Model (How it feels)

This entirely fulfills the promise of "native hands-free 3D interaction".

*   **No Controllers Required:** The judge uses the Quest 3's native hand-tracking.
*   **Laser Pointing & Pinching:** To change the year from 1990 to 2024, the judge physically raises their hand, points at the Streamlit timeline slider, and pinches their fingers to drag it.
*   **Tactile AI Generation:** They can reach out and "press" the button to trigger the Gemini AI "Story Mode", watching the terrifying climate analysis type out character-by-character on a 10-foot floating screen.
*   **Map Manipulation:** They can grab the 3D PyDeck map, rotate the globe, and lean their physical body forward to inspect the anomaly spikes over specific continents.

## 3. The Technical Execution (How it is Built)

To achieve this at hackathon speed without breaking the data pipeline, we combine three specific techniques already built into our codebase:

1.  **The WebXR Browser Loophole:** We use the native Oculus Browser. This browser automatically translates standard web clicks (like Streamlit widgets) into hand-tracking pinches. We get spatial interaction for free, without writing a single line of WebXR JavaScript or breaking Streamlit's iframe security constraints.
2.  **PyDeck Depth Rendering:** We force the Z-axis in Python using `extruded=True`, `pitch=60`, and a severely multiplied `elevation_scale=100000` inside the PyDeck layer. This ensures the WebGL canvas renders true 3D geometry inside the 2D browser window.
3.  **The "Anti-Nausea" Caching Protocol:** Because rendering 3D maps and parsing multi-dimensional NetCDF datasets is heavy, we aggressively use Streamlit's `@st.cache_data` in our `backend.py`. This ensures that when the judge drags the slider in Mixed Reality, the 3D map updates instantly without stuttering, preserving the immersive illusion and preventing simulator sickness.

---

## 4. The Pitch: Why This Wins

If a judge asks, *"Why is it in a browser window instead of sitting on the table?"*, this is your exact response:

> "True spatial data visualization often fails because rendering heavy multi-dimensional NetCDF data natively in WebXR causes severe frame drops and motion sickness. 
>
> We engineered PyClimaExplorer for real-world analysts. By isolating the environment via the Oculus Browser in Passthrough mode, we guarantee a stable, zero-latency Spatial Computing environment. The user gets hands-free 3D interaction with terabytes of data, wrapped in a UI that actually works without making them sick."

---

## Technical Deployment Checklist (10 Minutes Prior to Judging)

1.  **Network Sync:** Ensure the laptop running the Streamlit app and the Meta Quest 3 are on the **exact same Wi-Fi network**.
2.  **Get Local IP:** On the laptop, open a terminal and run `ipconfig` (Windows) or `ifconfig` (Mac/Linux). Note the IPv4 address (e.g., `192.168.1.55`).
3.  **Launch Server:** Ensure Streamlit is running binding to the network.
    *   `streamlit run app.py` (Streamlit defaults to binding 0.0.0.0 anyway)
4.  **Launch Headset:** Put on the Quest 3.
5.  **Enable Passthrough:** Ensure the headset is in Mixed Reality Passthrough mode (double-tap the side of the headset).
6.  **Open Browser:** Launch the native Meta Quest Browser.
7.  **Navigate to App:** Type the laptop's IP address and the Streamlit port into the URL bar: `http://<YOUR_IPV4_ADDRESS>:8501`.
8.  **Enter "God Mode":** 
    *   Grab the bottom edge of the browser window.
    *   Pull it toward you until it fills your entire field of view.
    *   Look for the "Curve / Wrap" toggle button in the bottom-right UI tray of the browser and toggle it ON so the screen wraps panoramically around the user.
9.  **Hand Off:** Hand the headset to the judge as they approach your table.
