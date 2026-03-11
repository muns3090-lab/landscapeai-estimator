import streamlit as st
from anthropic import Anthropic
from PIL import Image
import base64
import io
import os
from dotenv import load_dotenv

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LandscapeAI Estimator",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d1f0f;
    color: #e8f0e9;
}

.stApp {
    background: linear-gradient(135deg, #0d1f0f 0%, #122a14 50%, #0a1a0b 100%);
}

/* Hero Header */
.hero-header {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    background: linear-gradient(180deg, rgba(34,85,40,0.4) 0%, transparent 100%);
    border-bottom: 1px solid rgba(100,200,100,0.15);
    margin-bottom: 2rem;
}
.logo-text {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    color: #7ecf7e;
    letter-spacing: -1px;
    text-shadow: 0 0 40px rgba(126,207,126,0.3);
}
.logo-leaf { color: #4ade80; }
.tagline {
    font-size: 1rem;
    color: #a3c9a8;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.25rem;
}

/* Section Cards */
.section-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(100,200,100,0.12);
    border-radius: 16px;
    padding: 1.75rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(6px);
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: #7ecf7e;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #2d7a35, #4ade80) !important;
    color: #0d1f0f !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2.5rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(74,222,128,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(74,222,128,0.4) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(100,200,100,0.2) !important;
    border-radius: 10px !important;
    color: #e8f0e9 !important;
}

/* Sliders */
.stSlider > div > div > div { background: #2d7a35 !important; }

/* Results box */
.result-box {
    background: linear-gradient(135deg, rgba(34,85,40,0.5), rgba(20,50,25,0.7));
    border: 1px solid rgba(74,222,128,0.3);
    border-radius: 16px;
    padding: 2rem;
    margin-top: 1.5rem;
}
.cost-highlight {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    color: #4ade80;
    text-align: center;
    text-shadow: 0 0 20px rgba(74,222,128,0.4);
}
.divider { border-color: rgba(100,200,100,0.15); margin: 1.5rem 0; }
.badge {
    display: inline-block;
    background: rgba(74,222,128,0.15);
    border: 1px solid rgba(74,222,128,0.3);
    border-radius: 20px;
    padding: 0.25rem 0.9rem;
    font-size: 0.82rem;
    color: #7ecf7e;
    margin: 0.2rem;
}
.step-num {
    background: #2d7a35;
    color: #4ade80;
    border-radius: 50%;
    width: 28px; height: 28px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.85rem;
    margin-right: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── Header / Logo ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="logo-text"><span class="logo-leaf">🌿</span> LandscapeAI</div>
    <div class="tagline">Smart Estimates for Beautiful Outdoor Spaces</div>
</div>
""", unsafe_allow_html=True)

# ── Helper: encode image ──────────────────────────────────────────────────────
def encode_image(uploaded_file):
    img = Image.open(uploaded_file)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    return base64.standard_b64encode(buffer.getvalue()).decode("utf-8")

# ── Helper: call Claude ───────────────────────────────────────────────────────
def get_estimate(form_data: dict, image_b64_list: list) -> str:
    api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    client = Anthropic(api_key=api_key)

    content = []
    for img in image_b64_list:
        content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": "image/jpeg", "data": img}
        })

    prompt = f"""
You are a professional Southern California landscaping estimator with 20+ years experience.
A homeowner has submitted photos of their yard (if provided) and the following project details:

YARD DIMENSIONS: {form_data['length']}ft x {form_data['width']}ft = {form_data['length']*form_data['width']} sq ft
BUDGET: ${form_data['budget']:,}
COLOR SCHEME PREFERENCE: {form_data['color_scheme']}
INCLUDE SWIMMING POOL: {form_data['pool']}
GROUND COVER: {form_data['ground_cover']}
PATIO COVER / PERGOLA: {form_data['patio_cover']}
PLANT MAINTENANCE LEVEL: {form_data['plant_maintenance']}
LIGHTING: {form_data['lighting']}
IRRIGATION SYSTEM: {form_data['irrigation']}
STYLE PREFERENCE: {form_data['style']}
SPECIAL REQUESTS: {form_data['special_requests'] or 'None'}

Based on Southern California average contractor prices and labor costs (2024-2025), provide:

1. **PROJECT FEASIBILITY** — Is the budget realistic? What's achievable?

2. **RECOMMENDED DESIGN CONCEPT** — A vivid 3-4 sentence description of exactly how the yard will look. Be specific about plants, materials, colors, and layout.

3. **DETAILED COST BREAKDOWN** — Line items with price ranges:
   - Site prep & demo
   - Ground cover (sod/turf/decomposed granite etc.)
   - Plants & trees
   - Hardscape (patio, walkways, edging)
   - Pool (if applicable)
   - Patio cover/pergola (if applicable)
   - Irrigation system (if applicable)
   - Lighting (if applicable)
   - Labor
   - Contingency (10%)
   - **TOTAL ESTIMATE RANGE**

4. **PROJECT TIMELINE** — Realistic week-by-week schedule

5. **TOP 3 DESIGN INSPIRATIONS** — Describe 3 specific visual styles with plant names and materials the homeowner can Google/Pinterest search

6. **MONEY-SAVING TIPS** — 3 specific tips to stay within budget

7. **RECOMMENDED NEXT STEPS** — What to do to get started

Use dollar signs, bullet points, and headers. Be specific with SoCal plant names (Bird of Paradise, Mexican Sage, Agave, etc.) and SoCal contractors typical rates.
"""
    content.append({"type": "text", "text": prompt})

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2500,
        messages=[{"role": "user", "content": content}]
    )
    return response.content[0].text

# ══════════════════════════════════════════════════════════════════════════════
# FORM LAYOUT
# ══════════════════════════════════════════════════════════════════════════════

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    # ── Section 1: Photos ─────────────────────────────────────────────────────
    st.markdown('<div class="section-card"><div class="section-title">📸 Step 1 — Upload Your Yard Photos</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Upload 1–4 photos of your front or backyard",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True
    )
    if uploaded_files:
        cols = st.columns(min(len(uploaded_files), 2))
        for i, f in enumerate(uploaded_files[:4]):
            with cols[i % 2]:
                st.image(f, use_container_width=True, caption=f"Photo {i+1}")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Section 2: Dimensions ─────────────────────────────────────────────────
    st.markdown('<div class="section-card"><div class="section-title">📐 Step 2 — Yard Dimensions</div>', unsafe_allow_html=True)
    dc1, dc2 = st.columns(2)
    with dc1:
        length = st.number_input("Length (feet)", min_value=5, max_value=500, value=50, step=5)
    with dc2:
        width = st.number_input("Width (feet)", min_value=5, max_value=500, value=40, step=5)
    sqft = length * width
    st.markdown(f'<div style="text-align:center;color:#7ecf7e;font-size:1.1rem;margin-top:0.5rem;">📏 Total Area: <strong>{sqft:,} sq ft</strong></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Section 3: Budget ─────────────────────────────────────────────────────
    st.markdown('<div class="section-card"><div class="section-title">💰 Step 3 — Your Budget <span style="color:#ef4444;font-size:0.8rem;">*required</span></div>', unsafe_allow_html=True)
    budget = st.select_slider(
        "Select your total budget",
        options=[5000, 10000, 15000, 20000, 30000, 40000, 50000, 75000, 100000, 150000, 200000],
        value=20000,
        format_func=lambda x: f"${x:,}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # ── Section 4: Design Preferences ────────────────────────────────────────
    st.markdown('<div class="section-card"><div class="section-title">🎨 Step 4 — Design Preferences</div>', unsafe_allow_html=True)

    style = st.selectbox("Overall Style", [
        "Modern/Contemporary", "Desert/Xeriscape", "Tropical/Lush",
        "Mediterranean", "Cottage/English Garden", "Japanese Zen",
        "Coastal/Beach Vibes", "Ranch/Rustic", "Minimalist/Clean Lines"
    ])
    color_scheme = st.selectbox("Color Scheme", [
        "Earthy Neutrals (tans, greens, browns)",
        "Bold & Vibrant (pinks, oranges, purples)",
        "Cool Blues & Whites",
        "Desert Tones (terracotta, sage, sand)",
        "Lush All-Green",
        "Black, White & Grey (modern)"
    ])
    ground_cover = st.selectbox("Ground Cover Preference", [
        "Natural Grass (sod)", "Artificial Turf", "Decomposed Granite",
        "Concrete/Pavers", "Mixed (grass + hardscape)", "Native Ground Cover Plants"
    ])
    plant_maintenance = st.radio("Plant Maintenance Level", ["Low (drought-tolerant, minimal)", "Medium", "High (lush, requires regular care)"], horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Section 5: Features ───────────────────────────────────────────────────
    st.markdown('<div class="section-card"><div class="section-title">✨ Step 5 — Features & Add-ons</div>', unsafe_allow_html=True)

    fc1, fc2 = st.columns(2)
    with fc1:
        pool = st.checkbox("🏊 Swimming Pool")
        patio_cover = st.checkbox("⛱️ Patio Cover / Pergola")
    with fc2:
        irrigation = st.checkbox("💧 Irrigation System")
        lighting = st.checkbox("💡 Outdoor Lighting")

    special_requests = st.text_area(
        "Any special requests or notes?",
        placeholder="e.g., I have dogs so need durable turf, want a fire pit, need privacy screening...",
        height=100
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ── Generate Button ───────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
bcol1, bcol2, bcol3 = st.columns([1, 2, 1])
with bcol2:
    generate = st.button("🌿 Generate My Free Estimate", use_container_width=True)

# ── Results ───────────────────────────────────────────────────────────────────
if generate:
    api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
if not api_key:
        st.error("⚠️ Anthropic API key not found. Please add it to your .env file.")
    else:
        with st.spinner("🌱 Our AI landscaping expert is designing your space..."):
            form_data = {
                "length": length, "width": width, "budget": budget,
                "color_scheme": color_scheme, "pool": "Yes" if pool else "No",
                "ground_cover": ground_cover, "patio_cover": "Yes" if patio_cover else "No",
                "plant_maintenance": plant_maintenance, "lighting": "Yes" if lighting else "No",
                "irrigation": "Yes" if irrigation else "No", "style": style,
                "special_requests": special_requests
            }
            image_b64_list = []
            if uploaded_files:
                for f in uploaded_files[:4]:
                    image_b64_list.append(encode_image(f))

            result = get_estimate(form_data, image_b64_list)

        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align:center;margin-bottom:1rem;">
            <div style="font-family:'DM Sans';color:#a3c9a8;font-size:0.9rem;text-transform:uppercase;letter-spacing:2px;">Your Custom Estimate</div>
            <div style="font-family:'Playfair Display',serif;font-size:1.5rem;color:#7ecf7e;">{sqft:,} sq ft · ${budget:,} Budget · {style}</div>
        </div>
        """, unsafe_allow_html=True)
        st.divider()
        st.markdown(result)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align:center;margin-top:2rem;padding:1rem;border:1px dashed rgba(100,200,100,0.2);border-radius:12px;color:#6b9e6b;font-size:0.85rem;">
            💼 <strong>Powered by LandscapeAI</strong> · Estimates based on Southern California 2024–2025 average pricing<br>
            Final quotes may vary · Always get 3 contractor bids before committing
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:4rem;padding:1rem;color:#3d6b45;font-size:0.78rem;border-top:1px solid rgba(100,200,100,0.08);">
    🌿 LandscapeAI Estimator · Built for Southern California homeowners · Not a binding quote
</div>
""", unsafe_allow_html=True)