# app.py
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load dataset
df = pd.read_csv('data/total-number-of-emigrants.csv')

color_min = df['Total number of emigrants'].min()
color_max = min(df['Total number of emigrants'].max(), 10500000)

fig = px.choropleth(
    df,
    locations="Entity",
    locationmode="country names",
    color="Total number of emigrants",
    animation_frame="Year",
    title="Global Emigration Trends (1990-2020)",
    color_continuous_scale="Plasma",
    range_color=[color_min, color_max],
    hover_name="Entity",
    hover_data=["Total number of emigrants"]
)

fig.update_layout(
    title={
        'text': "Global Emigration Trends (1990-2020)",
        'font': {
            'family': "Times",
            'size': 20,
        }
    }
)


fig2 = px.line(
    df.groupby("Year")["Total number of emigrants"].sum().reset_index(),
    x="Year",
    y="Total number of emigrants",
    title="Global Emigration Over Time",
    markers=True,
    template="plotly_white"
)

fig2.update_layout(
    title={
        'text': "Total Emigration Over Time",
        'font': {
            'family': "Times",
            'size': 20,
        }
    }
)

continents = ["Europe", "Asia", "Africa", "Austrailia and New Zealand", "Northern America", "South America"]
areas = df[df['Entity'].isin(continents)]

top_countries = areas[areas['Year'] == 2020].nlargest(10, 'Total number of emigrants')
fig3 = px.bar(
    top_countries,
    x="Entity",
    y="Total number of emigrants",
    title="Top Continents by Emigration in 2020",
    template="plotly_white"
)

fig3.update_layout(
    title={
        'text': "Top Continents by Emigration in 2020",
        'font': {
            'family': "Times",
            'size': 20,
        }
    }
)

italy = df[df['Entity'] == 'Italy']

fig4 = px.line(
    italy.groupby("Year")["Total number of emigrants"].sum().reset_index(),
    x="Year",
    y="Total number of emigrants",
    title="Italian Emigration Over Time",
    markers=True,
    template="plotly_white"
)

fig4.update_layout(
    title={
        'text': "Total Emigration in Italy Over Time",
        'font': {
            'family': "Times",
            'size': 20,
        }
    }
)

# Dash App Layout
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Global Migration Trends"),
    html.Div(className="container", children=[
        html.P("Emigration is defined as the act of leaving one's own country to settle permanently in another; moving abroad. This phenomenon has been a central part of human history, driven by factors such as economic opportunities, political instability, environmental changes, and the search for better living conditions. Over time, migration patterns have shaped cultures, economies, and demographics worldwide, creating complex narratives of growth, challenge, and transformation. This dashboard provides a data-driven exploration of global emigration trends, shedding light on where people are moving and the forces that influence these migrations."),
    ]),
    html.Div(className="graph-container", children=[
        dcc.Graph(figure=fig),
        html.P("The choropleth map illustrates the total number of emigrants per country from 1990 to 2020, with colors representing the number of emigrants. Darker shades indicate countries with higher emigration, while lighter shades show those with lower emigration levels. The map is animated by year, allowing you to explore how global emigration patterns evolved over the past three decades. It offers a visual understanding of where most people have been moving from, reflecting the geopolitical and socio-economic factors influencing these trends."),
    ]),
    html.Div(className="graph-container", children=[
        dcc.Graph(figure=fig3),
        html.P("The bar chart ranks continents based on the number of emigrants in 2020. It provides a snapshot of which continents experienced the most emigration during that year. This visualization offers a comparative view of migration across continents, making it easier to identify regions where emigration was particularly high. The chart sheds light on the global distribution of emigrants and helps contextualize the broader migration trends of the year."),
    ]),
    html.Div(className="graph-container", children=[
        dcc.Graph(figure=fig2),
        html.P("This line chart displays the total number of emigrants worldwide each year. The chart aggregates data across countries to show how global emigration has fluctuated over time. It highlights key trends, such as periods of sharp increase or decline in migration, which may correlate with global events like economic crises or political upheavals. This chart helps contextualize the overall movement of people across borders, offering a clear view of global migration patterns."),
    ]),
    html.Div(className="graph-container", children=[
        dcc.Graph(figure=fig4),
        html.P("This line chart tracks the number of emigrants from Italy over time, highlighting how migration trends have shifted for this particular country. By focusing on Italy, the chart allows for an in-depth look at the country’s emigration history and the specific events or factors influencing these changes. You can observe periods of higher or lower emigration and consider the social, economic, and political forces at play within Italy during these times."),
    ]),
])

if __name__ == "__main__":
    app.run_server(debug=False)