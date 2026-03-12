# 🌿 LandscapeAI Estimator

**AI-powered backyard design and cost estimation for Southern California homeowners.**

Built with Claude AI + Stability AI + Streamlit. Upload photos of your yard, set your budget and style preferences, and get photorealistic design previews, a detailed cost breakdown, a week-by-week project timeline, and a downloadable PDF estimate — all in under 60 seconds.

🔗 **Live App:** [landscapeai-estimator.streamlit.app](https://landscapeai-estimator.streamlit.app)

---

## ✨ Features

- 📸 **Photo Upload** — Upload up to 4 photos of your current yard for AI analysis
- 🎨 **Design Preferences** — Choose style, color scheme, ground cover, maintenance level, and add-ons (pool, pergola, irrigation, lighting)
- 🖼️ **Photorealistic Previews** — 3 AI-generated views of your finished yard (wide overview, eye-level, garden detail) powered by Stability AI
- 💰 **Detailed Cost Breakdown** — Itemized estimates using current SoCal contractor rates
- 📅 **Project Timeline** — Week-by-week schedule from site prep to final planting
- 💡 **Design Inspirations & Savings Tips** — AI-curated recommendations tailored to your inputs
- 📄 **PDF Export** — Download a branded, full-color estimate report with images and all sections
- 🔒 **Rate Limited** — 3 estimates per session / 5 per day to prevent abuse

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend & App | [Streamlit](https://streamlit.io) |
| AI Text & Estimates | [Anthropic Claude API](https://www.anthropic.com) (`claude-opus-4-5`) |
| AI Image Generation | [Stability AI](https://stability.ai) (Stable Image Core) |
| Image Processing | Pillow (PIL) |
| PDF Generation | ReportLab |
| Environment | Python 3.10+ |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/landscapeai-estimator.git
cd landscapeai-estimator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up API keys

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
STABILITY_API_KEY=sk-your-stability-key-here
```

**Get your keys:**
- Anthropic: [console.anthropic.com](https://console.anthropic.com)
- Stability AI (free tier — 25 images/month): [platform.stability.ai/account/keys](https://platform.stability.ai/account/keys)

### 4. Run locally

```powershell
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## ☁️ Deploy to Streamlit Cloud

### Step 1 — Push to GitHub
Follow the GitHub upload steps in the section below.

### Step 2 — Connect to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
2. Click **New app**
3. Select your repository, branch (`main`), and set the main file to `app.py`
4. Click **Deploy**

### Step 3 — Add secrets
In your deployed app: **Settings → Secrets**, add:

```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
STABILITY_API_KEY = "sk-your-stability-key-here"
```

> ⚠️ Never commit your `.env` file or paste API keys directly into your code.

---

## 📁 Project Structure

```
landscapeai-estimator/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env                # Local API keys (never commit this)
├── .gitignore          # Excludes .env and cache files
└── README.md           # This file
```

---

## 🔑 How the API Key Flow Works

The app uses a layered key resolution strategy:

1. **User-supplied key** (entered in the app UI) — used first, charges the user's own Stability AI credits
2. **Streamlit secrets** — fallback for the app owner when testing
3. **Environment variable** — fallback for local development

This means the app is fully public but users bring their own Stability AI key for image generation. The Anthropic key (for text estimates) stays private in Streamlit secrets.

---

## 💡 Usage Notes

- Estimates are based on **Southern California 2024–2025 average contractor rates**
- This tool provides **AI-generated estimates only** — not binding quotes
- Always obtain at least **3 contractor bids** before committing to a project
- Image generation takes ~20–30 seconds (3 images generated sequentially)

---

## 👤 Author

**Sunil Srinivas Sukumar**
Technical Program Manager & AI Product Builder

- 🔗 [LinkedIn](https://www.linkedin.com/in/sss90)
- 💻 [GitHub](https://github.com/muns3090-lab)
- 🌿 [Live App](https://landscapeai-estimator.streamlit.app)
- 🎫 [ServiceNow Ticket Intelligence](https://servicenow-ticket-intelligence.streamlit.app)

---

## 📄 License

MIT License — free to use, modify, and distribute with attribution.
