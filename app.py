import streamlit as st
from anthropic import Anthropic
from PIL import Image
import base64
import io
import os
import re
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="LandscapeAI Estimator",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

/* ── BASE ── */
html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif !important;
    background-color: #0d1f0f !important;
    color: #e8f0e9 !important;
}
.stApp {
    background: linear-gradient(135deg, #0d1f0f 0%, #122a14 50%, #0a1a0b 100%) !important;
}

/* ── HERO ── */
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
.tagline {
    font-size: 1rem;
    color: #a3c9a8;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.25rem;
}

/* ── SECTION CARDS ── */
.section-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(100,200,100,0.12);
    border-radius: 16px;
    padding: 1.75rem;
    margin-bottom: 1.5rem;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: #7ecf7e;
    margin-bottom: 1rem;
}

/* ── ALL WIDGET LABELS ── */
label, p, span,
div[data-testid="stWidgetLabel"] p,
div[data-testid="stWidgetLabel"] label,
.stSelectbox label, .stRadio label,
.stCheckbox label, .stNumberInput label,
.stTextArea label, .stFileUploader label,
.stSlider label {
    color: #f0fff0 !important;
    font-weight: 500 !important;
}

/* ── FILE UPLOADER: dark background ── */
div[data-testid="stFileUploader"] {
    background-color: #1a3320 !important;
    border: 1px dashed rgba(100,200,100,0.4) !important;
    border-radius: 12px !important;
    padding: 0.5rem !important;
}
div[data-testid="stFileUploader"] * {
    color: #c8f0c8 !important;
}
div[data-testid="stFileUploader"] button {
    background-color: #2d7a35 !important;
    color: #f0fff0 !important;
    border: none !important;
    border-radius: 8px !important;
}
section[data-testid="stFileUploaderDropzone"] {
    background-color: #1a3320 !important;
    border-color: rgba(100,200,100,0.4) !important;
}
section[data-testid="stFileUploaderDropzone"] * {
    color: #c8f0c8 !important;
    fill: #c8f0c8 !important;
}

/* ── SELECTBOX: dark background, visible text ── */
div[data-baseweb="select"] {
    background-color: #1a3320 !important;
}
div[data-baseweb="select"] > div {
    background-color: #1a3320 !important;
    border: 1px solid rgba(100,200,100,0.35) !important;
    border-radius: 10px !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] div,
div[data-baseweb="select"] input {
    color: #f0fff0 !important;
    background-color: transparent !important;
}
/* Dropdown menu */
ul[data-baseweb="menu"],
div[data-baseweb="popover"] {
    background-color: #1a3320 !important;
    border: 1px solid rgba(100,200,100,0.3) !important;
    border-radius: 10px !important;
}
ul[data-baseweb="menu"] li,
div[data-baseweb="popover"] li {
    background-color: #1a3320 !important;
    color: #f0fff0 !important;
}
ul[data-baseweb="menu"] li:hover,
div[data-baseweb="popover"] li:hover {
    background-color: #2d7a35 !important;
}

/* ── NUMBER INPUTS ── */
div[data-testid="stNumberInput"] input,
.stTextInput input,
.stTextArea textarea {
    background-color: #1a3320 !important;
    border: 1px solid rgba(100,200,100,0.35) !important;
    border-radius: 10px !important;
    color: #f0fff0 !important;
}
div[data-testid="stNumberInput"] button {
    background-color: #2d7a35 !important;
    color: #f0fff0 !important;
    border: none !important;
}

/* ── RADIO BUTTONS ── */
div[data-testid="stRadio"] label,
div[data-testid="stRadio"] span,
div[data-testid="stRadio"] p {
    color: #f0fff0 !important;
}

/* ── CHECKBOXES ── */
div[data-testid="stCheckbox"] label,
div[data-testid="stCheckbox"] span,
div[data-testid="stCheckbox"] p {
    color: #f0fff0 !important;
}

/* ── SLIDER ── */
div[data-testid="stSlider"] * {
    color: #f0fff0 !important;
}
div[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background-color: #4ade80 !important;
}
div[data-testid="stSlider"] [data-baseweb="slider"] div:first-child {
    background-color: rgba(255,255,255,0.1) !important;
}
div[data-testid="stSlider"] [data-baseweb="slider"] div:nth-child(2) {
    background-color: #4ade80 !important;
}

/* ── GENERATE BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #2d7a35, #4ade80) !important;
    color: #0d1f0f !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2.5rem !important;
    box-shadow: 0 4px 20px rgba(74,222,128,0.3) !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(74,222,128,0.5) !important;
}

/* ── SPINNER ── */
div[data-testid="stSpinner"] p { color: #7ecf7e !important; }

/* ── DIVIDER ── */
hr { border-color: rgba(100,200,100,0.2) !important; }

/* ── RESULT HTML STYLES ── */
.result-outer {
    background: #0a1c0b;
    border: 1px solid rgba(74,222,128,0.25);
    border-radius: 16px;
    padding: 2rem 2.25rem;
    margin-top: 1rem;
    color: #dff5df;
}
.result-outer h2 {
    font-family: 'Playfair Display', serif;
    color: #7ecf7e;
    font-size: 1.25rem;
    margin: 1.5rem 0 0.6rem;
    border-bottom: 1px solid rgba(100,200,100,0.15);
    padding-bottom: 0.4rem;
}
.result-outer p {
    color: #dff5df;
    line-height: 1.8;
    margin: 0.4rem 0;
}
.result-outer ul, .result-outer ol {
    color: #dff5df;
    padding-left: 1.4rem;
    margin: 0.4rem 0 0.8rem;
}
.result-outer li {
    color: #dff5df;
    line-height: 1.8;
    margin-bottom: 0.2rem;
}
.result-outer strong {
    color: #a8e6a8;
    font-weight: 600;
}
.result-outer .total-line {
    background: rgba(74,222,128,0.1);
    border: 1px solid rgba(74,222,128,0.3);
    border-radius: 8px;
    padding: 0.6rem 1rem;
    color: #4ade80;
    font-weight: 700;
    font-size: 1.05rem;
    margin-top: 0.75rem;
}

/* ── INSPIRATION CARDS ── */
.inspiration-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 1rem 0 1.5rem;
}
.inspiration-card {
    background: #1a3320;
    border: 1px solid rgba(100,200,100,0.2);
    border-radius: 12px;
    overflow: hidden;
}
.inspiration-card img {
    width: 100%;
    height: 180px;
    object-fit: cover;
    display: block;
}
.inspiration-label {
    color: #a3c9a8;
    font-size: 0.78rem;
    font-weight: 500;
    padding: 0.5rem 0.75rem;
    background: rgba(0,0,0,0.3);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="logo-text">🌿 LandscapeAI</div>
    <div class="tagline">Smart Estimates for Beautiful Outdoor Spaces</div>
</div>
""", unsafe_allow_html=True)


# ── HELPERS ───────────────────────────────────────────────────────────────────
def encode_image(uploaded_file):
    img = Image.open(uploaded_file)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    return base64.standard_b64encode(buffer.getvalue()).decode("utf-8")


def parse_image_searches(result_text):
    lines = result_text.strip().split("\n")
    for line in reversed(lines):
        if line.startswith("IMAGE_SEARCHES:"):
            raw = line.replace("IMAGE_SEARCHES:", "").strip()
            terms = [t.strip() for t in raw.split("|") if t.strip()]
            return terms[:3]
    return []


def clean_result_text(result_text):
    lines = result_text.strip().split("\n")
    return "\n".join(l for l in lines if not l.startswith("IMAGE_SEARCHES:"))


def markdown_to_html(text):
    """Convert Claude markdown output to styled HTML."""
    lines = text.split("\n")
    html_lines = []
    in_ul = False
    in_ol = False
    ol_counter = 0

    for line in lines:
        stripped = line.strip()

        # Close lists if needed
        if in_ul and not stripped.startswith("- ") and not stripped.startswith("* "):
            html_lines.append("</ul>")
            in_ul = False
        if in_ol and not re.match(r"^\d+\.", stripped):
            html_lines.append("</ol>")
            in_ol = False
            ol_counter = 0

        if not stripped:
            html_lines.append("<br>")
            continue

        # Headings
        if stripped.startswith("#### "):
            content = format_inline(stripped[5:])
            html_lines.append(f"<h2>{content}</h2>")
        elif stripped.startswith("### "):
            content = format_inline(stripped[4:])
            html_lines.append(f"<h2>{content}</h2>")
        elif stripped.startswith("## "):
            content = format_inline(stripped[3:])
            html_lines.append(f"<h2>{content}</h2>")
        elif stripped.startswith("# "):
            content = format_inline(stripped[2:])
            html_lines.append(f"<h2>{content}</h2>")

        # Numbered list
        elif re.match(r"^\d+\.", stripped):
            if not in_ol:
                html_lines.append("<ol>")
                in_ol = True
            content = format_inline(re.sub(r"^\d+\.\s*", "", stripped))
            html_lines.append(f"<li>{content}</li>")

        # Bullet list
        elif stripped.startswith("- ") or stripped.startswith("* "):
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            content = format_inline(stripped[2:])
            # Highlight total line
            if "TOTAL" in content.upper() or "total estimate" in content.lower():
                html_lines.append(f'<li class="total-line">{content}</li>')
            else:
                html_lines.append(f"<li>{content}</li>")

        # Normal paragraph
        else:
            content = format_inline(stripped)
            html_lines.append(f"<p>{content}</p>")

    if in_ul:
        html_lines.append("</ul>")
    if in_ol:
        html_lines.append("</ol>")

    return "\n".join(html_lines)


def format_inline(text):
    """Handle bold and italic inline markdown."""
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


def get_pexels_images(queries):
    """Get working landscape images from Pexels using their curated endpoint (no key needed for embed)."""
    pexels_map = {
        "modern": "https://images.pexels.com/photos/1643389/pexels-photo-1643389.jpeg?auto=compress&cs=tinysrgb&w=700",
        "desert": "https://images.pexels.com/photos/158251/forest-the-sun-morning-158251.jpeg?auto=compress&cs=tinysrgb&w=700",
        "tropical": "https://images.pexels.com/photos/1072824/pexels-photo-1072824.jpeg?auto=compress&cs=tinysrgb&w=700",
        "mediterranean": "https://images.pexels.com/photos/1029599/pexels-photo-1029599.jpeg?auto=compress&cs=tinysrgb&w=700",
        "japanese": "https://images.pexels.com/photos/1108701/pexels-photo-1108701.jpeg?auto=compress&cs=tinysrgb&w=700",
        "coastal": "https://images.pexels.com/photos/1005417/pexels-photo-1005417.jpeg?auto=compress&cs=tinysrgb&w=700",
        "backyard": "https://images.pexels.com/photos/2988861/pexels-photo-2988861.jpeg?auto=compress&cs=tinysrgb&w=700",
        "garden": "https://images.pexels.com/photos/1458694/pexels-photo-1458694.jpeg?auto=compress&cs=tinysrgb&w=700",
        "patio": "https://images.pexels.com/photos/1643384/pexels-photo-1643384.jpeg?auto=compress&cs=tinysrgb&w=700",
        "pool": "https://images.pexels.com/photos/261327/pexels-photo-261327.jpeg?auto=compress&cs=tinysrgb&w=700",
        "lawn": "https://images.pexels.com/photos/589840/pexels-photo-589840.jpeg?auto=compress&cs=tinysrgb&w=700",
        "minimalist": "https://images.pexels.com/photos/2736388/pexels-photo-2736388.jpeg?auto=compress&cs=tinysrgb&w=700",
        "xeriscape": "https://images.pexels.com/photos/5503376/pexels-photo-5503376.jpeg?auto=compress&cs=tinysrgb&w=700",
        "cottage": "https://images.pexels.com/photos/931177/pexels-photo-931177.jpeg?auto=compress&cs=tinysrgb&w=700",
    }

    fallbacks = [
        "https://images.pexels.com/photos/2988861/pexels-photo-2988861.jpeg?auto=compress&cs=tinysrgb&w=700",
        "https://images.pexels.com/photos/1643389/pexels-photo-1643389.jpeg?auto=compress&cs=tinysrgb&w=700",
        "https://images.pexels.com/photos/1072824/pexels-photo-1072824.jpeg?auto=compress&cs=tinysrgb&w=700",
    ]

    result_urls = []
    for i, q in enumerate(queries[:3]):
        q_lower = q.lower()
        matched = False
        for keyword, url in pexels_map.items():
            if keyword in q_lower:
                result_urls.append((url, q))
                matched = True
                break
        if not matched:
            result_urls.append((fallbacks[i % len(fallbacks)], q))

    return result_urls


def get_estimate(form_data, image_b64_list):
    api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    client = Anthropic(api_key=api_key)

    content = []
    for img in image_b64_list:
        content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": "image/jpeg", "data": img}
        })

    prompt = f"""
You are a professional Southern California landscaping estimator with 20+ years of experience.
A homeowner submitted the following project details:

YARD DIMENSIONS: {form_data['length']}ft x {form_data['width']}ft = {form_data['length'] * form_data['width']} sq ft
BUDGET: ${form_data['budget']:,}
COLOR SCHEME: {form_data['color_scheme']}
SWIMMING POOL: {form_data['pool']}
GROUND COVER: {form_data['ground_cover']}
PATIO COVER / PERGOLA: {form_data['patio_cover']}
PLANT MAINTENANCE: {form_data['plant_maintenance']}
LIGHTING: {form_data['lighting']}
IRRIGATION: {form_data['irrigation']}
STYLE: {form_data['style']}
SPECIAL REQUESTS: {form_data['special_requests'] or 'None'}

Provide a detailed estimate with these exact sections using markdown headers (##):

## 1. Project Feasibility
Is the budget realistic for this project? What is achievable?

## 2. Recommended Design Concept
A vivid 3-4 sentence description of how the yard will look. Be specific about plants, materials, colors, layout.

## 3. Detailed Cost Breakdown
List every line item as a bullet with a dollar range:
- Site prep & demolition: $X,XXX - $X,XXX
- Ground cover: $X,XXX - $X,XXX
- Plants & trees: $X,XXX - $X,XXX
- Hardscape (patio, walkways, edging): $X,XXX - $X,XXX
- Pool (if applicable): $X,XXX - $X,XXX
- Patio cover/pergola (if applicable): $X,XXX - $X,XXX
- Irrigation system (if applicable): $X,XXX - $X,XXX
- Lighting (if applicable): $X,XXX - $X,XXX
- Labor: $X,XXX - $X,XXX
- Contingency (10%): $X,XXX
- **TOTAL ESTIMATE RANGE: $XX,XXX - $XX,XXX**

## 4. Project Timeline
Week-by-week schedule as bullet points.

## 5. Top 3 Design Inspirations
Three named styles with SoCal plant names and materials.

## 6. Money-Saving Tips
Three specific actionable tips.

## 7. Recommended Next Steps
Clear action items to get started.

Use SoCal plant names (Bird of Paradise, Agave, Mexican Sage, etc.) and current SoCal contractor rates.

On the very last line, output:
IMAGE_SEARCHES: {form_data['style']} backyard | {form_data['ground_cover']} landscape | {form_data['style']} garden patio
"""

    content.append({"type": "text", "text": prompt})

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2800,
        messages=[{"role": "user", "content": content}]
    )
    return response.content[0].text


# ── FORM ──────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="section-card"><div class="section-title">📸 Step 1 — Upload Your Yard Photos</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Upload 1–4 photos of your front or backyard",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True
    )
    if uploaded_files:
        img_cols = st.columns(min(len(uploaded_files), 2))
        for i, f in enumerate(uploaded_files[:4]):
            with img_cols[i % 2]:
                st.image(f, use_container_width=True, caption=f"Photo {i+1}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card"><div class="section-title">📐 Step 2 — Yard Dimensions</div>', unsafe_allow_html=True)
    dc1, dc2 = st.columns(2)
    with dc1:
        length = st.number_input("Length (feet)", min_value=5, max_value=1000, value=50, step=5)
    with dc2:
        width = st.number_input("Width (feet)", min_value=5, max_value=1000, value=40, step=5)
    sqft = length * width
    st.markdown(f'<div style="text-align:center;color:#7ecf7e;font-size:1.1rem;margin-top:0.5rem;">Total Area: <strong>{sqft:,} sq ft</strong></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card"><div class="section-title">💰 Step 3 — Your Budget</div>', unsafe_allow_html=True)
    budget = st.select_slider(
        "Select your total budget",
        options=[5000, 10000, 15000, 20000, 30000, 40000, 50000, 75000, 100000,
                 150000, 200000, 250000, 300000, 400000, 500000],
        value=20000,
        format_func=lambda x: f"${x:,}"
    )
    st.markdown(f'<div style="text-align:center;color:#4ade80;font-size:1.2rem;font-weight:700;margin-top:0.4rem;">${budget:,}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-card"><div class="section-title">🎨 Step 4 — Design Preferences</div>', unsafe_allow_html=True)
    style = st.selectbox("Overall Style", [
        "Modern/Contemporary", "Desert/Xeriscape", "Tropical/Lush",
        "Mediterranean", "Cottage/English Garden", "Japanese Zen",
        "Coastal/Beach Vibes", "Ranch/Rustic", "Minimalist/Clean Lines"
    ])
    color_scheme = st.selectbox("Color Scheme", [
        "Earthy Neutrals (tans, greens, browns)",
        "Bold and Vibrant (pinks, oranges, purples)",
        "Cool Blues and Whites",
        "Desert Tones (terracotta, sage, sand)",
        "Lush All-Green",
        "Black, White and Grey (modern)"
    ])
    ground_cover = st.selectbox("Ground Cover Preference", [
        "Natural Grass (sod)", "Artificial Turf", "Decomposed Granite",
        "Concrete/Pavers", "Mixed (grass + hardscape)", "Native Ground Cover Plants"
    ])
    plant_maintenance = st.radio(
        "Plant Maintenance Level",
        ["Low (drought-tolerant, minimal)", "Medium", "High (lush, requires regular care)"],
        horizontal=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

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
        placeholder="e.g., dogs need durable turf, want a fire pit, need privacy screening...",
        height=100
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ── GENERATE BUTTON ───────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
b1, b2, b3 = st.columns([1, 2, 1])
with b2:
    generate = st.button("🌿 Generate My Free Estimate", use_container_width=True)

# ── RESULTS ───────────────────────────────────────────────────────────────────
if generate:
    api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("API key not found. Add ANTHROPIC_API_KEY to Streamlit secrets.")
    else:
        with st.spinner("🌱 Our AI landscaping expert is designing your space..."):
            form_data = {
                "length": length, "width": width, "budget": budget,
                "color_scheme": color_scheme,
                "pool": "Yes" if pool else "No",
                "ground_cover": ground_cover,
                "patio_cover": "Yes" if patio_cover else "No",
                "plant_maintenance": plant_maintenance,
                "lighting": "Yes" if lighting else "No",
                "irrigation": "Yes" if irrigation else "No",
                "style": style,
                "special_requests": special_requests
            }
            image_b64_list = [encode_image(f) for f in (uploaded_files or [])[:4]]
            result = get_estimate(form_data, image_b64_list)

        image_search_terms = parse_image_searches(result)
        display_result = clean_result_text(result)

        # ── Summary header ──
        st.markdown(f"""
        <div style="text-align:center;margin:2rem 0 1.5rem;">
            <div style="color:#a3c9a8;font-size:0.85rem;text-transform:uppercase;letter-spacing:2px;margin-bottom:0.4rem;">Your Custom Estimate</div>
            <div style="font-family:'Playfair Display',serif;font-size:1.5rem;color:#7ecf7e;">
                {sqft:,} sq ft &nbsp;·&nbsp; ${budget:,} Budget &nbsp;·&nbsp; {style}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Inspiration images ──
        st.markdown("""
        <div style="font-family:'Playfair Display',serif;font-size:1.25rem;color:#7ecf7e;margin-bottom:0.4rem;">
            🖼️ Design Inspiration Visuals
        </div>
        <div style="color:#a3c9a8;font-size:0.84rem;margin-bottom:1rem;">
            Visual references matching your style — share these with your contractor.
        </div>
        """, unsafe_allow_html=True)

        if image_search_terms and len(image_search_terms) >= 3:
            queries = image_search_terms
        else:
            queries = [
                f"{style} backyard",
                f"{ground_cover} landscape",
                f"{style} patio garden"
            ]

        image_data = get_pexels_images(queries)

        ic1, ic2, ic3 = st.columns(3)
        for col, (img_url, label) in zip([ic1, ic2, ic3], image_data):
            with col:
                st.markdown(f"""
                <div class="inspiration-card">
                    <img src="{img_url}" alt="{label}" />
                    <div class="inspiration-label">🔍 {label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Estimate text rendered as HTML ──
        result_html = markdown_to_html(display_result)
        st.markdown(f'<div class="result-outer">{result_html}</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align:center;margin-top:2rem;padding:1rem;
             border:1px dashed rgba(100,200,100,0.2);border-radius:12px;
             color:#a3c9a8;font-size:0.84rem;">
            💼 <strong style="color:#7ecf7e;">Powered by LandscapeAI</strong>
            &nbsp;·&nbsp; Based on Southern California 2024–2025 average pricing<br>
            Final quotes may vary &nbsp;·&nbsp; Always get 3 contractor bids before committing
        </div>
        """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:4rem;padding:1rem;
     color:#3d6b45;font-size:0.78rem;
     border-top:1px solid rgba(100,200,100,0.08);">
    🌿 LandscapeAI Estimator · Built for Southern California homeowners · Not a binding quote
</div>
""", unsafe_allow_html=True)