# COVID-19 Global Data Tracker

This is a Jupyter Notebook project that analyzes and visualizes global COVID-19 trends, including cases, deaths, recoveries, and vaccinations across countries.

## Objectives

Import and clean COVID-19 global data from Our World in Data.
Explore time series trends of cases, deaths, and vaccinations for selected countries (Kenya, USA, India).
Compare key metrics across countries and calculate derived indicators such as death rate and percentage vaccinated.
Visualize data with line charts, bar charts, heatmaps, and an interactive choropleth map.
Communicate insights through narrative explanations and visualizations in a Jupyter Notebook.

## Tools & Libraries

- pandas – data loading, cleaning, and manipulation
- matplotlib & seaborn– static visualizations (line plots, bar charts, heatmaps)
- plotly.express – interactive choropleth maps

## How to Run / View

1. Clone this repository:
   ```bash
   git clone <repo-url>
   ```
2. Navigate to the project folder and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Open the Jupyter Notebook:
   ```bash
   jupyter notebook COVID19_Global_Tracker.ipynb
   ```
4. Run all cells in order to reproduce the analysis and visualizations.

Key Insights & Reflections

1. India experienced the steepest rise in total cases early on (April–June 2021), whereas Kenya’s curve remained relatively flat in comparison.
2. In as much as the USA had a high case count, its death rate plateaued below 2%, compared to over 2.5% in India at several peaks.
3. The USA achieved over 50% population vaccination by mid-2021, outpacing India (35%) and Kenya (20%) by the same date.
   Several countries show sudden drops to zero in new case counts—indicating reporting lags or corrections rather than true declines.
5.  Interactive choropleth maps vividly highlight regional hotspots in South America and Europe, as well as lower vaccination rates in parts of Africa.
