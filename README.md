
# Enhanced Netflix BI Dashboard

## 📦 Stack used:
1. Language: Python 3.13.5
2. Framework: Streamlit - for creating the web dashboard
3. Visualization: Plotly - for rich, interactive charts and maps
4. Data Handling: Pandas - for data transformation, aggregation, and filtering

## 📦Required Packages (installed via requirements.txt):
- streamlit
- pandas
- plotly

To install:
- pip install -r requirements.txt **OR** py -m pip install -r requirements.txt

To run:
- streamlit run app.py

## 📂 Dataset
- BI&A - Case Study Dataset.csv (10,000 rows of Netflix user viewing data)

## 📊 Features
- KPI Metrics: Avg Duration, Avg Rating, Binge Viewers %
- Interactive Filters: Location, Watching Method, Subscription Type
- Visuals:
  - Top Watched Shows (colored by Avg Duration)
  - Subscription Type & Watching Method combo
  - Device Usage (Pie Chart)
  - Age Group vs Gender Line Analysis
  - Map of Avg Duration by Country
  - Monthly Viewership Trend

## 📈 Enhancements Made
- Netflix-styled UI with dark theme and branding
- Added dropdown filters for month, location, and device
- New views: interactive map, Age Group vs Gender Line Analysis , line chart trend
- Tables showing top watched shows and device usage

## 🤖 AI Contribution
ChatGPT helped design layout and optimized insights creating better insights.

## 📊 Value Added
The original dashboard was static and minimal. This version offers:
- **Interactivity**
- **Deeper user behavior segmentation**
- **Better storytelling via maps, heatmaps & timelines**

## ▶️ Run Instructions
```bash
pip install -r requirements.txt
streamlit run app.py
```

