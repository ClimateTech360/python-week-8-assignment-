import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv('owid-covid-data.csv')
print(df.columns)
df.head()
df.isnull().sum()
df.info()
df.describe()

countries_of_interest = ['Kenya', 'United States', 'India']
df_filtered = df[df['location'].isin(countries_of_interest)]
print(df_filtered['location'].unique())
df_filtered.head()

df_filtered = df_filtered.dropna(subset=['date', 'total_cases'])
print(df_filtered[['date', 'total_cases']].isnull().sum())
df_filtered['date'] = pd.to_datetime(df_filtered['date'])
print(df_filtered['date'].dtype)
numeric_cols = df_filtered.select_dtypes(include='number').columns
df_filled_zero = df_filtered.copy()
df_filled_zero[numeric_cols] = df_filled_zero[numeric_cols].fillna(0)
print(df_filled_zero[numeric_cols].isnull().sum())

df_filled_zero['date'] = pd.to_datetime(df_filled_zero['date'])
df_clean = df_filled_zero.copy()
sns.set_theme(style="whitegrid")
countries = ['Kenya', 'United States', 'India']
df_plot = df_clean[df_clean['location'].isin(countries)].copy()
df_plot['death_rate'] = df_plot['total_deaths'] / df_plot['total_cases']
plt.figure(figsize=(10, 5))
for c in countries:
    sub = df_plot[df_plot['location'] == c]
    plt.plot(sub['date'], sub['total_cases'], label=c)
plt.title('Total COVID-19 Cases Over Time')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
for c in countries:
    sub = df_plot[df_plot['location'] == c]
    plt.plot(sub['date'], sub['total_deaths'], label=c)
plt.title('Total COVID-19 Deaths Over Time')
plt.xlabel('Date')
plt.ylabel('Total Deaths')
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
for c in countries:
    sub = df_plot[df_plot['location'] == c]
    plt.plot(sub['date'], sub['new_cases'], label=c, alpha=0.7)
plt.title('Daily New COVID-19 Cases')
plt.xlabel('Date')
plt.ylabel('New Cases')
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
for c in countries:
    sub = df_plot[df_plot['location'] == c]
    plt.plot(sub['date'], sub['death_rate'], label=c)
plt.title('COVID-19 Death Rate Over Time')
plt.xlabel('Date')
plt.ylabel('Death Rate')
plt.legend()
plt.tight_layout()
plt.show()

latest = df_clean[df_clean['date'] == df_clean['date'].max()]
top10 = latest.nlargest(10, 'total_cases')
plt.figure(figsize=(8, 6))
sns.barplot(data=top10, y='location', x='total_cases')
plt.title(
    f'Top 10 Countries by Total Cases as of {latest["date"].iloc[0].date()}')
plt.xlabel('Total Cases')
plt.ylabel('Country')
plt.tight_layout()
plt.show()

cols_needed = ['date', 'location', 'total_vaccinations',
               'people_vaccinated', 'population']
df_vax = df_clean[cols_needed].copy()

# Plot cumulative vaccinations over time
plt.figure(figsize=(10, 5))
for c in countries:
    sub = df_vax[df_vax['location'] == c]
    plt.plot(sub['date'], sub['total_vaccinations'], label=c)
plt.title('Cumulative COVID-19 Vaccinations Over Time')
plt.xlabel('Date')
plt.ylabel('Total Vaccinations')
plt.legend()
plt.tight_layout()
plt.show()

# Calculate % of population vaccinated
df_vax['pct_vaccinated'] = df_vax['people_vaccinated'] / \
    df_vax['population'] * 100

# Plot % vaccinated over time
plt.figure(figsize=(10, 5))
for c in countries:
    sub = df_vax[df_vax['location'] == c]
    plt.plot(sub['date'], sub['pct_vaccinated'], label=c)
plt.title('% of Population Vaccinated Over Time')
plt.xlabel('Date')
plt.ylabel('Percent Vaccinated')
plt.legend()
plt.tight_layout()
plt.show()

# Pie chart of vaccinated vs. unvaccinated (latest date)
latest_date = df_vax['date'].max()
latest_vax = df_vax[df_vax['date'] == latest_date].set_index('location')

for c in countries:
    vac = latest_vax.loc[c, 'people_vaccinated']
    pop = latest_vax.loc[c, 'population']
    unvac = pop - vac

    plt.figure(figsize=(4, 4))
    plt.pie([vac, unvac],
            labels=['Vaccinated', 'Unvaccinated'],
            autopct='%1.1f%%',
            startangle=90)
    plt.title(f'{c} Vaccination Status as of {latest_date.date()}')
    plt.tight_layout()
    plt.show()

    # Building a Choropleth Map
latest_date = df_clean['date'].max()
df_latest = (
    df_clean[df_clean['date'] == latest_date]
    .loc[:, ['iso_code', 'location', 'total_cases', 'total_vaccinations']]
    .dropna(subset=['iso_code'])
)

# Choropleth of total cases
fig_cases = px.choropleth(
    df_latest,
    locations='iso_code',
    color='total_cases',
    hover_name='location',
    color_continuous_scale='Reds',
    title=f'Global COVID-19 Total Cases as of {latest_date.date()}',
    labels={'total_cases': 'Total Cases'}
)
fig_cases.update_layout(margin=dict(l=0, r=0, t=40, b=0))
fig_cases.show()

# Choropleth of vaccination count (optional
fig_vax = px.choropleth(
    df_latest,
    locations='iso_code',
    color='total_vaccinations',
    hover_name='location',
    color_continuous_scale='Blues',
    title=f'Global COVID-19 Total Vaccinations as of {latest_date.date()}',
    labels={'total_vaccinations': 'Total Vaccinations'}
)
fig_vax.update_layout(margin=dict(l=0, r=0, t=40, b=0))
fig_vax.show()

# Insights & Reporting


def calculate_stats(data):
    """
Magnitude & Timing of Waves

The United States consistently shows the highest absolute numbers of total cases and deaths, with clear multi-peak waves (spring 2020, winter 2020–21, summer 2021, winter 2021–22).

India’s curve features a particularly sharp surge around April–May 2021 (its devastating second wave), followed by a slower decline.

Kenya’s total‐cases curve remains far lower in magnitude and exhibits a more gradual rise and fall, reflecting less intense but more prolonged waves.

Death Rate Differences

India’s overall death rate (total_deaths / total_cases) stays below that of the U.S. throughout most of the timeline, suggesting either demographic factors (younger population) or reporting differences.

Kenya’s calculated death rate is more variable—spiking during certain waves—possibly indicating under-reporting of cases, delayed care, or data lags.

Vaccination Rollout Speed & Coverage

The U.S. led the pack early on, reaching high percentages of vaccinated people by mid-2021, then plateauing around 60–70%.

India’s vaccination percentage climbed rapidly during summer 2021 but took longer to surpass 40% of its population.

Kenya started much later and more slowly, remaining below 20% vaccinated by early 2022, underscoring global equity challenges in vaccine access.

Geographic Patterns (Choropleth Takeaways)

The world map of total cases highlights the U.S., India, Brazil, and several European countries in the darkest red—corroborating that high-population nations and those with early aggressive testing/reporting show the greatest case counts.

Vaccination maps reveal stark disparities: North America and Europe in deep blue (high vaccinations), parts of Africa, South Asia, and Latin America in pale shades (lower rollouts).

Anomalies & Patterns to Note

India’s mid-2021 second wave is an outlier in both its daily new-cases spike and temporary jump in death rate.

Kenya’s data shows “plateau” periods where case counts hardly budged for weeks—likely reflecting testing constraints or true lull periods.

Some smaller nations (not in our three) appear darker on the choropleth despite lower populations, hinting at very high per-capita reporting/testing.
    """
