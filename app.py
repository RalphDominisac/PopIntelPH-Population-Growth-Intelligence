import streamlit as st
import pandas as pd
import ollama
import random


# ─────────────────────────────────────────────
# Global CSS
# ─────────────────────────────────────────────
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PopIntelPH: Population Growth Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Load CSS
load_css("styles/main.css")


# ─────────────────────────────────────────────
# Load Data
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/clean_population_growth.csv")
    return df

df = load_data()


# ─────────────────────────────────────────────
# Page Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <h1>📊 PopIntelPH: Population Growth Intelligence</h1>
    <div class="source-tag">📌 Philippine Statistics Authority · 2026 CBPP</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# National Overview
# ─────────────────────────────────────────────
avg_national = df["avg_growth"].mean()
high_growth_count = df[df["growth_category"] == "High Growth"].shape[0]

st.markdown(f"""
<div class="section">
    <div class="section-title">🌍 National Overview</div>
    <div class="metric-row">
        <div class="metric-card">
            <div class="label">Avg Growth · All Regions</div>
            <div class="value accent-green">{avg_national:.2f}%</div>
        </div>
        <div class="metric-card">
            <div class="label">High Growth Regions</div>
            <div class="value accent-blue">{high_growth_count}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Top Growing Regions
# ─────────────────────────────────────────────
top_regions = df.sort_values(by="avg_growth", ascending=False).head(5)

st.markdown("""
<div class="section">
    <div class="section-title">🏆 Top Growing Regions</div>
""", unsafe_allow_html=True)

st.dataframe(
    top_regions[["Region", "avg_growth", "growth_category"]].rename(columns={
        "avg_growth": "Avg Growth (%)",
        "growth_category": "Category"
    }),
    hide_index=True,
    use_container_width=True,
)

st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Region Selector
# ─────────────────────────────────────────────
st.markdown("""
<div class="section">
    <div class="section-title">🔍 Region Selection</div>
""", unsafe_allow_html=True)

regions = sorted(df["Region"].unique())
region = st.selectbox(
    "Choose a region to analyze population trends",
    regions,
    label_visibility="visible",
)

st.markdown("</div>", unsafe_allow_html=True)

selected = df[df["Region"] == region]


# ─────────────────────────────────────────────
# Growth Rates Table
# ─────────────────────────────────────────────
st.markdown("""
<div class="section">
    <div class="section-title">📋 Growth Rates</div>
""", unsafe_allow_html=True)

st.dataframe(selected, hide_index=True, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Analysis
# ─────────────────────────────────────────────
avg_growth = selected["avg_growth"].values[0]
category   = selected["growth_category"].values[0]

trend_values = [
    selected["2020-2025"].values[0],
    selected["2025-2030"].values[0],
    selected["2030-2035"].values[0],
]

def get_trend_direction(values):
    if values[2] > values[0]:   return "Increasing"
    elif values[2] < values[0]: return "Decreasing"
    else:                        return "Stable"

trend_direction = get_trend_direction(trend_values)

# Badge color mapping
category_class = {
    "High Growth":   "high",
    "Medium Growth": "medium",
    "Low Growth":    "low",
}.get(category, "low")

trend_class = trend_direction.lower()
trend_icon  = {"Increasing": "↑", "Decreasing": "↓", "Stable": "→"}.get(trend_direction, "")

st.markdown(f"""
<div class="section">
    <div class="section-title">📈 Analysis</div>
    <div class="metric-row">
        <div class="metric-card">
            <div class="label">Average Growth Rate</div>
            <div class="value accent-green">{avg_growth:.2f}%</div>
        </div>
        <div class="metric-card">
            <div class="label">Growth Category</div>
            <div class="value" style="font-size:1.1rem; padding-top:8px;">
                <span class="badge {category_class}">{category}</span>
            </div>
        </div>
    </div>
    <div style="margin-top: 1rem;">
        <span class="trend-pill {trend_class}">{trend_icon} Trend: {trend_direction}</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Growth Trend Chart
# ─────────────────────────────────────────────
trend_df = pd.DataFrame({
    "Period":      ["2020–2025", "2025–2030", "2030–2035"],
    "Growth Rate": trend_values,
})

st.markdown("""
<div class="section">
    <div class="section-title">📉 Growth Trend</div>
""", unsafe_allow_html=True)

st.line_chart(trend_df.set_index("Period"), use_container_width=True, height=420)

st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# AI Insight
# ─────────────────────────────────────────────
def generate_ai_insight(region, avg_growth, category, trend_direction):
    pressure = (
        "high population pressure"   if avg_growth > 1.0 else
        "moderate population pressure" if avg_growth > 0.7 else
        "low population pressure"
    )
    focus_area = random.choice([
        "urban infrastructure",
        "healthcare systems",
        "housing demand",
        "employment opportunities",
        "transportation networks",
    ])

    prompt = f"""
You are a senior government data analyst in the Philippines.

Analyze the population growth of {region}.

DATA:
- Growth Rate: {avg_growth}
- Category: {category}
- Trend: {trend_direction}
- Population Pressure: {pressure}

CONTEXT:
Focus on {focus_area}.

INSTRUCTIONS:
- Be specific to the region
- Avoid generic advice
- Sound like a real policy analyst
- Keep it concise but insightful

Return your response STRICTLY in this format:

Insight:
<short paragraph>

Risk:
<short paragraph>

Recommendation:
- Point 1 (start with action verb)
- Point 2 (specific to region)
- Point 3 (short and clear)
"""
    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]


def parse_ai_output(text):
    sections = {"Insight": "", "Risk": "", "Recommendation": ""}
    current = None
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("Insight"):        current = "Insight";        continue
        elif line.startswith("Risk"):         current = "Risk";           continue
        elif line.startswith("Recommendation"): current = "Recommendation"; continue
        if current:
            sections[current] += line + "\n"
    return sections


def format_text(text):
    lines = text.split("\n")
    paragraphs, bullets = [], []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("-") or line.startswith("•"):
            bullets.append(line.lstrip("-• ").strip())
        else:
            paragraphs.append(line)
    html = "".join(f"<p>{p}</p>" for p in paragraphs)
    if bullets:
        html += "<ul>" + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>"
    return html


def render_ai_section():
    st.markdown("""
    <div class="section">
        <div class="section-title">🤖 AI Insight</div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="region-heading">
        📍 {region}
        <span>· AI-generated policy analysis</span>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Generating insight via Llama 3…"):
        insight_text = generate_ai_insight(region, avg_growth, category, trend_direction)

    sections = parse_ai_output(insight_text)

    st.markdown(f"""
    <div class="ai-card insight">
        <div class="card-title">📊 Insight</div>
        {format_text(sections["Insight"])}
    </div>

    <div class="ai-card risk">
        <div class="card-title">⚠️ Risk</div>
        {format_text(sections["Risk"])}
    </div>

    <div class="ai-card reco">
        <div class="card-title">💡 Recommendation</div>
        {format_text(sections["Recommendation"])}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


render_ai_section()