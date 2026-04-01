# 📊 PopIntelPH: Population Growth Intelligence

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![AI](<https://img.shields.io/badge/AI-Llama3%20(Ollama)-green>)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## 🎬 Demo

> Replace this with your demo GIF

![Demo GIF](./assets/demo.gif)

---

## 📸 Screenshots

> Add your screenshots below

### Dashboard Overview

![Screenshot 1](./assets/screenshot1.png)

### Regional Analysis

![Screenshot 2](./assets/screenshot2.png)

### AI Insight Panel

![Screenshot 3](./assets/screenshot3.png)

---

## 🧠 Architecture

> Replace with your architecture diagram image

![Architecture](./assets/architecture.png)

### Flow:

1. Load PSA dataset
2. Clean + transform data
3. Compute metrics
4. Visualize via Streamlit
5. Send structured prompt to Llama 3 (Ollama)
6. Parse + render AI insights

---

## 🚀 Overview

PopIntelPH is a data analytics dashboard that analyzes regional population growth trends in the Philippines using official data from the Philippine Statistics Authority (PSA).

It combines data visualization, statistical analysis, and features an AI-powered analysis using a local AI model (Llama 3 via Ollama) to generate actionable policy insights for each region.

Inside this repo may also contain extra miscellanous data for more information about the origins of the dataset that was utilized in this project.

---

## 🚀 Features

- 📈 Interactive dashboard
- 🏆 Top growth detection
- 📊 Statistical insights
- 📉 Trend visualization
- 🤖 AI-generated insights (local LLM)

---

## 🧠 AI Integration

- Ollama (local runtime)
- Llama 3 model
- No external API
- Fully offline capable

---

## 📂 Project Structure

```
popintelph/
│
├── app.py             # Main Streamlit app
├── inspect_data.py    # Data cleaning script
│
├── data/
│ ├── clean_population_growth.csv                          # normalized data
│ └── Statistical Tables (2020 CBPP Subnational).xlsx      # raw data (utilized Table 2)
│ └── Press Release (2020 CBPP Subnational).pdf            # extra miscellaneous data
│ └── Technical Notes (2020 CBPP Subnational).pdf          # extra miscellaneous data
│
├── styles/
│ └── main.css         # UI styling
│
├── requirements.txt
└── README.md
```

---

## 🛠️ Installation

```bash
git clone https://github.com/YOUR_USERNAME/popintelph.git
cd popintelph
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

---

## 🤖 Setup Ollama

```bash
ollama pull llama3
ollama run llama3
```

---

## ▶️ Run

```bash
streamlit run app.py
```

---

## ⚠️ Limitations

- Requires local Ollama
- Not cloud-deployable (without server setup)

---

## 👨‍💻 Author

Ralph Henry L. Dominisac
