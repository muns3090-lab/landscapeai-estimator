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

/* ── RESULT BOX WRAPPER ── */
.result-outer {
    background: #0a1c0b;
    border: 1px solid rgba(74,222,128,0.25);
    border-radius: 16px;
    padding: 2rem 2.25rem;
    margin-top: 1rem;
}

/* Force ALL text inside result box to be bright — targets Streamlit's markdown divs */
.result-outer *,
.result-outer p,
.result-outer li,
.result-outer span,
.result-outer div,
.result-outer ul,
.result-outer ol,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] ul li,
[data-testid="stMarkdownContainer"] ol li,
[data-testid="stMarkdownContainer"] td,
[data-testid="stMarkdownContainer"] th {
    color: #dff5df !important;
    line-height: 1.8 !important;
}
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4 {
    color: #7ecf7e !important;
    font-family: 'Playfair Display', serif !important;
}
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] b {
    color: #a8e6a8 !important;
    font-weight: 600 !important;
}
/* Table styling in results */
[data-testid="stMarkdownContainer"] table {
    width: 100%;
    border-collapse: collapse;
}
[data-testid="stMarkdownContainer"] th {
    background: rgba(74,222,128,0.15) !important;
    color: #7ecf7e !important;
    padding: 0.5rem 0.75rem !important;
    border: 1px solid rgba(100,200,100,0.25) !important;
}
[data-testid="stMarkdownContainer"] td {
    padding: 0.45rem 0.75rem !important;
    border: 1px solid rgba(100,200,100,0.15) !important;
    color: #dff5df !important;
}
[data-testid="stMarkdownContainer"] tr:nth-child(even) td {
    background: rgba(255,255,255,0.03) !important;
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


def clean_result_text(result_text):
    lines = result_text.strip().split("\n")
    return "\n".join(l for l in lines if not l.startswith("IMAGE_SEARCHES:"))


def generate_yard_svgs(form_data):
    """
    Ask Claude to generate 3 SVG yard illustrations based on user inputs.
    Returns list of (svg_string, label) tuples rendered inline — no external network needed.
    """
    api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    client = Anthropic(api_key=api_key)

    # Pick colors based on scheme
    color_map = {
        "Earthy Neutrals": {"ground": "#c8a96e", "plant1": "#4a7c3f", "plant2": "#6b9e50", "accent": "#8b6914", "hard": "#b8956a"},
        "Bold and Vibrant": {"ground": "#7ab648", "plant1": "#e8445a", "plant2": "#ff9800", "accent": "#9c27b0", "hard": "#e0c080"},
        "Cool Blues and Whites": {"ground": "#a8d5a2", "plant1": "#4a90d9", "plant2": "#7ec8e3", "accent": "#ffffff", "hard": "#c8d8e8"},
        "Desert Tones": {"ground": "#d4a574", "plant1": "#8b9d5a", "plant2": "#c4963c", "accent": "#e07840", "hard": "#c8a878"},
        "Lush All-Green": {"ground": "#5a9e3c", "plant1": "#2d6e1a", "plant2": "#7ecf5a", "accent": "#a8d878", "hard": "#8cb878"},
        "Black, White and Grey": {"ground": "#9e9e9e", "plant1": "#333333", "plant2": "#666666", "accent": "#ffffff", "hard": "#757575"},
    }
    scheme_key = next((k for k in color_map if k in form_data["color_scheme"]), "Earthy Neutrals")
    c = color_map[scheme_key]

    has_pool = form_data["pool"] == "Yes"
    has_patio = form_data["patio_cover"] == "Yes"
    has_lights = form_data["lighting"] == "Yes"
    style = form_data["style"]
    ground = form_data["ground_cover"]

    pool_svg = """
        <ellipse cx="520" cy="200" rx="80" ry="50" fill="#4fc3f7" opacity="0.85"/>
        <ellipse cx="520" cy="200" rx="80" ry="50" fill="none" stroke="#0288d1" stroke-width="2"/>
        <text x="520" y="205" text-anchor="middle" font-size="11" fill="#0288d1" font-family="sans-serif">Pool</text>
    """ if has_pool else ""

    patio_svg = """
        <rect x="60" y="60" width="160" height="100" rx="4" fill="#c8a878" opacity="0.7"/>
        <line x1="60" y1="60" x2="60" y2="40" stroke="#8b6914" stroke-width="3"/>
        <line x1="140" y1="60" x2="140" y2="35" stroke="#8b6914" stroke-width="3"/>
        <line x1="220" y1="60" x2="220" y2="40" stroke="#8b6914" stroke-width="3"/>
        <line x1="55" y1="40" x2="225" y2="35" stroke="#8b6914" stroke-width="2.5"/>
        <text x="140" y="115" text-anchor="middle" font-size="11" fill="#4a2e00" font-family="sans-serif">Patio</text>
    """ if has_patio else ""

    lights_svg = """
        <circle cx="100" cy="58" r="5" fill="#fff9c4" opacity="0.9"/>
        <circle cx="160" cy="52" r="5" fill="#fff9c4" opacity="0.9"/>
        <circle cx="220" cy="55" r="5" fill="#fff9c4" opacity="0.9"/>
    """ if has_lights else ""

    # Ground cover fill
    if "Turf" in ground or "Grass" in ground:
        ground_fill = c["ground"]
        ground_pattern = f'<rect x="30" y="150" width="580" height="220" fill="{ground_fill}" rx="4" opacity="0.9"/>'
    elif "Granite" in ground or "Decomposed" in ground:
        ground_fill = "#c4a882"
        ground_pattern = f'<rect x="30" y="150" width="580" height="220" fill="{ground_fill}" rx="4" opacity="0.85"/>'
    elif "Concrete" in ground or "Pavers" in ground:
        ground_fill = "#b0b0b0"
        ground_pattern = f'<rect x="30" y="150" width="580" height="220" fill="{ground_fill}" rx="4" opacity="0.8"/><line x1="30" y1="200" x2="610" y2="200" stroke="#999" stroke-width="1" opacity="0.5"/><line x1="30" y1="250" x2="610" y2="250" stroke="#999" stroke-width="1" opacity="0.5"/><line x1="150" y1="150" x2="150" y2="370" stroke="#999" stroke-width="1" opacity="0.5"/><line x1="300" y1="150" x2="300" y2="370" stroke="#999" stroke-width="1" opacity="0.5"/><line x1="450" y1="150" x2="450" y2="370" stroke="#999" stroke-width="1" opacity="0.5"/>'
    else:
        ground_fill = c["ground"]
        ground_pattern = f'<rect x="30" y="150" width="580" height="220" fill="{ground_fill}" rx="4" opacity="0.85"/>'

    # Style-specific plant shapes
    if "Japanese" in style or "Zen" in style:
        plants = f"""
        <circle cx="120" cy="148" r="28" fill="{c['plant1']}" opacity="0.9"/>
        <rect x="115" y="155" width="10" height="30" fill="#5c3d1a"/>
        <circle cx="240" cy="142" r="20" fill="{c['plant2']}" opacity="0.85"/>
        <circle cx="380" cy="145" r="32" fill="{c['plant1']}" opacity="0.9"/>
        <rect x="374" y="155" width="12" height="32" fill="#5c3d1a"/>
        <ellipse cx="500" cy="150" rx="18" ry="40" fill="{c['plant2']}" opacity="0.8"/>
        <rect x="80" y="310" width="4" height="40" fill="#8b6914"/>
        <ellipse cx="82" cy="305" rx="12" ry="8" fill="{c['accent']}" opacity="0.7"/>
        """
    elif "Desert" in style or "Xeriscape" in style:
        plants = f"""
        <ellipse cx="110" cy="150" rx="15" ry="40" fill="{c['plant1']}" opacity="0.9"/>
        <ellipse cx="130" cy="145" rx="12" ry="35" fill="{c['plant2']}" opacity="0.85"/>
        <ellipse cx="280" cy="148" rx="20" ry="45" fill="{c['plant1']}" opacity="0.9"/>
        <circle cx="400" cy="152" r="22" fill="{c['accent']}" opacity="0.8"/>
        <ellipse cx="500" cy="146" rx="16" ry="38" fill="{c['plant2']}" opacity="0.9"/>
        <circle cx="160" cy="300" r="18" fill="{c['plant1']}" opacity="0.7"/>
        <circle cx="450" cy="320" r="14" fill="{c['plant2']}" opacity="0.7"/>
        """
    elif "Tropical" in style:
        plants = f"""
        <ellipse cx="100" cy="135" rx="25" ry="50" fill="{c['plant1']}" opacity="0.9"/>
        <ellipse cx="140" cy="128" rx="20" ry="42" fill="{c['plant2']}" opacity="0.85"/>
        <circle cx="300" cy="138" r="35" fill="{c['plant1']}" opacity="0.9"/>
        <ellipse cx="420" cy="132" rx="22" ry="48" fill="{c['plant2']}" opacity="0.9"/>
        <circle cx="530" cy="140" r="28" fill="{c['accent']}" opacity="0.8"/>
        <ellipse cx="200" cy="290" rx="30" ry="20" fill="{c['plant2']}" opacity="0.6"/>
        """
    else:
        plants = f"""
        <circle cx="115" cy="148" r="25" fill="{c['plant1']}" opacity="0.9"/>
        <rect x="110" y="158" width="10" height="28" fill="#5c3d1a"/>
        <circle cx="260" cy="144" r="30" fill="{c['plant2']}" opacity="0.85"/>
        <rect x="254" y="158" width="12" height="28" fill="#5c3d1a"/>
        <circle cx="400" cy="146" r="27" fill="{c['plant1']}" opacity="0.9"/>
        <rect x="394" y="158" width="12" height="28" fill="#5c3d1a"/>
        <circle cx="530" cy="150" r="22" fill="{c['plant2']}" opacity="0.85"/>
        <ellipse cx="180" cy="300" rx="15" ry="25" fill="{c['accent']}" opacity="0.7"/>
        """

    # Sky gradient based on style
    sky_color = "#87ceeb" if "Coastal" in style else "#b8d4f0" if "Japanese" in style or "Zen" in style else "#a8c8e8"

    views = [
        ("🏡 Wide Overview", f"""
        <!-- Sky -->
        <defs>
            <linearGradient id="sky1" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="{sky_color}"/>
                <stop offset="100%" stop-color="#e8f4f8"/>
            </linearGradient>
            <linearGradient id="wall1" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#e8dcc8"/>
                <stop offset="100%" stop-color="#d4c4a8"/>
            </linearGradient>
        </defs>
        <rect width="640" height="400" fill="url(#sky1)"/>
        <!-- House wall -->
        <rect x="0" y="80" width="640" height="120" fill="url(#wall1)" opacity="0.6"/>
        <!-- Ground -->
        {ground_pattern}
        <!-- Plants along back wall -->
        {plants}
        <!-- Patio cover -->
        {patio_svg}
        <!-- Pool -->
        {pool_svg}
        <!-- Lights -->
        {lights_svg}
        <!-- Walkway -->
        <polygon points="280,370 360,370 340,200 300,200" fill="{c['hard']}" opacity="0.7"/>
        <!-- Sun -->
        <circle cx="580" cy="40" r="28" fill="#fff176" opacity="0.9"/>
        <line x1="580" y1="5" x2="580" y2="15" stroke="#fff176" stroke-width="2"/>
        <line x1="615" y1="40" x2="625" y2="40" stroke="#fff176" stroke-width="2"/>
        <line x1="604" y1="16" x2="610" y2="10" stroke="#fff176" stroke-width="2"/>
        <!-- Label -->
        <rect x="10" y="370" width="130" height="22" rx="4" fill="rgba(0,0,0,0.5)"/>
        <text x="75" y="385" text-anchor="middle" font-size="12" fill="white" font-family="sans-serif">{style} · {ground.split('(')[0]}</text>
        """),
        ("🌅 Eye-Level View", f"""
        <defs>
            <linearGradient id="sky2" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#f4a261"/>
                <stop offset="40%" stop-color="{sky_color}"/>
                <stop offset="100%" stop-color="#e8f4f8"/>
            </linearGradient>
        </defs>
        <rect width="640" height="400" fill="url(#sky2)"/>
        <!-- Ground perspective -->
        {ground_pattern}
        <!-- Large foreground plants -->
        <ellipse cx="80" cy="200" rx="30" ry="70" fill="{c['plant1']}" opacity="0.95"/>
        <ellipse cx="560" cy="195" rx="28" ry="65" fill="{c['plant2']}" opacity="0.95"/>
        <circle cx="160" cy="170" r="40" fill="{c['plant2']}" opacity="0.85"/>
        <rect x="155" y="185" width="10" height="50" fill="#5c3d1a"/>
        <circle cx="480" cy="165" r="38" fill="{c['plant1']}" opacity="0.85"/>
        <rect x="475" y="180" width="10" height="50" fill="#5c3d1a"/>
        <!-- Patio if selected -->
        {patio_svg}
        <!-- Hardscape path -->
        <rect x="250" y="300" width="140" height="70" fill="{c['hard']}" opacity="0.7" rx="3"/>
        <line x1="250" y1="335" x2="390" y2="335" stroke="#999" stroke-width="1" opacity="0.5"/>
        <line x1="320" y1="300" x2="320" y2="370" stroke="#999" stroke-width="1" opacity="0.5"/>
        <!-- Lights -->
        {lights_svg}
        <!-- Accent plants foreground -->
        <ellipse cx="310" cy="340" rx="12" ry="28" fill="{c['accent']}" opacity="0.8"/>
        <!-- Label -->
        <rect x="10" y="370" width="160" height="22" rx="4" fill="rgba(0,0,0,0.5)"/>
        <text x="90" y="385" text-anchor="middle" font-size="12" fill="white" font-family="sans-serif">Golden Hour · {form_data['color_scheme'].split('(')[0].strip()}</text>
        """),
        ("🌿 Garden Detail", f"""
        <defs>
            <linearGradient id="soil" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#8b6914"/>
                <stop offset="100%" stop-color="#5c3d0a"/>
            </linearGradient>
        </defs>
        <!-- Background -->
        <rect width="640" height="400" fill="{sky_color}" opacity="0.3"/>
        <rect x="0" y="250" width="640" height="150" fill="url(#soil)" opacity="0.6"/>
        <!-- Close-up plants -->
        <ellipse cx="120" cy="200" rx="40" ry="100" fill="{c['plant1']}" opacity="0.95"/>
        <ellipse cx="160" cy="185" rx="30" ry="80" fill="{c['plant2']}" opacity="0.9"/>
        <circle cx="320" cy="170" r="55" fill="{c['plant2']}" opacity="0.9"/>
        <rect x="314" y="200" width="12" height="80" fill="#5c3d1a"/>
        <ellipse cx="480" cy="190" rx="35" ry="90" fill="{c['plant1']}" opacity="0.95"/>
        <ellipse cx="530" cy="195" rx="28" ry="75" fill="{c['accent']}" opacity="0.85"/>
        <!-- Ground cover close up -->
        <rect x="0" y="300" width="640" height="100" fill="{c['ground']}" opacity="0.7"/>
        <!-- Rocks/decorative -->
        <ellipse cx="200" cy="310" rx="20" ry="12" fill="#a0a0a0" opacity="0.8"/>
        <ellipse cx="420" cy="315" rx="16" ry="10" fill="#909090" opacity="0.8"/>
        <ellipse cx="300" cy="320" rx="12" ry="8" fill="#b0b0b0" opacity="0.8"/>
        <!-- Flowers accent -->
        <circle cx="250" cy="248" r="8" fill="{c['accent']}" opacity="0.9"/>
        <circle cx="390" cy="244" r="7" fill="{c['accent']}" opacity="0.9"/>
        <circle cx="180" cy="260" r="6" fill="{c['accent']}" opacity="0.85"/>
        <!-- Label -->
        <rect x="10" y="370" width="180" height="22" rx="4" fill="rgba(0,0,0,0.5)"/>
        <text x="100" y="385" text-anchor="middle" font-size="12" fill="white" font-family="sans-serif">Plant Detail · {form_data['plant_maintenance'].split('(')[0].strip()} Maintenance</text>
        """),
    ]

    svgs = []
    for label, content_svg in views:
        full_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 400" width="100%" style="border-radius:10px;display:block;">
        {content_svg}
        </svg>"""
        svgs.append((full_svg, label))

    return svgs


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

Provide your estimate using ONLY the format below. Do not use markdown tables anywhere — use only bullet points and ## headers.

## 1. Project Feasibility
Write 2-3 sentences on whether the budget is realistic and what is achievable.

## 2. Recommended Design Concept
Write 3-4 vivid sentences describing exactly how the yard will look: plants, materials, colors, layout.

## 3. Detailed Cost Breakdown
Use this exact bullet format for every line item — no tables, no pipes:
- **Site Prep & Demolition:** $X,XXX – $X,XXX
- **Ground Cover ({form_data['ground_cover']}):** $X,XXX – $X,XXX
- **Plants & Trees:** $X,XXX – $X,XXX
- **Hardscape (patio, walkways, edging):** $X,XXX – $X,XXX
- **Pool:** $X,XXX – $X,XXX (only if selected)
- **Patio Cover / Pergola:** $X,XXX – $X,XXX (only if selected)
- **Irrigation System:** $X,XXX – $X,XXX (only if selected)
- **Outdoor Lighting:** $X,XXX – $X,XXX (only if selected)
- **Labor (SoCal rates):** $X,XXX – $X,XXX
- **Contingency (10%):** $X,XXX
- **TOTAL ESTIMATE: $XX,XXX – $XX,XXX**

## 4. Project Timeline
Use this exact bullet format:
- **Week 1–2:** Activity description
- **Week 3–4:** Activity description
(and so on until project complete)

## 5. Top 3 Design Inspirations
- **[Style Name]:** Description with specific SoCal plant names and materials
- **[Style Name]:** Description with specific SoCal plant names and materials
- **[Style Name]:** Description with specific SoCal plant names and materials

## 6. Money-Saving Tips
- **Tip 1:** Specific actionable advice
- **Tip 2:** Specific actionable advice
- **Tip 3:** Specific actionable advice

## 7. Recommended Next Steps
- Step 1
- Step 2
- Step 3

Use SoCal plant names (Bird of Paradise, Agave, Mexican Sage, Kangaroo Paw, etc.) and current SoCal contractor rates. Do not use pipe characters or markdown tables anywhere.
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

        # ── AI-Generated Design Visuals ──
        st.markdown("""
        <div style="font-family:'Playfair Display',serif;font-size:1.25rem;color:#7ecf7e;margin-bottom:0.4rem;">
            🖼️ AI-Generated Design Visuals
        </div>
        <div style="color:#a3c9a8;font-size:0.84rem;margin-bottom:1rem;">
            Three views of your yard based on your exact inputs — style, ground cover, features &amp; color scheme.
        </div>
        """, unsafe_allow_html=True)

        svg_data = generate_yard_svgs(form_data)
        ic1, ic2, ic3 = st.columns(3)
        for col, (svg_str, label) in zip([ic1, ic2, ic3], svg_data):
            with col:
                st.markdown(
                    f'<div style="background:#1a3320;border:1px solid rgba(100,200,100,0.25);'
                    f'border-radius:12px;overflow:hidden;padding:0;">'
                    f'{svg_str}'
                    f'<div style="color:#a3c9a8;font-size:0.8rem;text-align:center;padding:0.4rem 0;'
                    f'background:rgba(0,0,0,0.3);">{label}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Estimate text — back to st.markdown for clean table/bullet formatting ──
        st.markdown('<div class="result-outer">', unsafe_allow_html=True)
        st.markdown(display_result)
        st.markdown('</div>', unsafe_allow_html=True)

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