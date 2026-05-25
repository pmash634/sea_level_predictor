#  Sea Level Rise Predictor

An interactive data analysis dashboard that visualizes global sea level rise from 1880 to 2014, with linear regression forecasts to 2050 (and beyond).

Built with Python · Pandas · Plotly · Streamlit · SciPy.

---

## What it does

- Loads CSIRO adjusted sea level records (1880–2014)
- Computes two linear regressions:
  - **Full-period** (1880–2014): baseline historical trend
  - **Recent period** (2000–present): captures the modern acceleration
- Projects sea levels to any year up to 2100
- Displays key metrics: slope, R², and projected values
- Interactive controls: toggle layers, adjust forecast year, change the "recent" cutoff

## 🔍 Key finding

The post-2000 rate of sea level rise is approximately **60% faster** than the historical average — a signal of accelerating climate impact captured clearly in the regression slopes.

---

##  Getting started

### 1. Clone the repo
```bash
git clone https://github.com/pmash634/sea-level-predictor.git
cd sea-level-predictor
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the dashboard
```bash
streamlit run dashboard/app.py
```

The app will open at `http://localhost:8501`.

### 4. Or run the static script
```bash
python src/sea_level_analysis.py
# Saves plot to output/sea_level_plot.png
```

---

##  Project structure

```
sea-level-predictor/

README.md
requirements.txt
data/
epa-sea-level.csv        # CSIRO adjusted sea level dataset
src/
 sea_level_analysis.py    # Core analysis: load, regress, plot
dashboard/
 app.py                   # Streamlit interactive dashboard
 output/
 sea_level_plot.png       # Static chart output
notebooks/
 exploration.ipynb        # EDA and methodology notes
## Data source

- **Dataset**: [EPA Global Mean Sea Level](https://www.epa.gov/climate-indicators/climate-change-indicators-sea-level)
- **Measurement**: CSIRO adjusted sea level (inches relative to 1990 baseline)
- **Coverage**: 1880–2014

---

## 🛠 Tech stack

| Tool | Purpose |
pandas` | Data loading and manipulation |
scipy.stats.linregress` | Linear regression |
| `plotly` | Interactive charts in dashboard |
| `matplotlib` | Static chart export |
| `streamlit` | Dashboard framework |

---

## Deploy to Streamlit Cloud 

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set main file path to `dashboard/app.py`
5. Click Deploy— your app gets a public URL!

---

## Author

Purity wanjiku macharia · Applied Statistics with Programming · Murang'a University  


