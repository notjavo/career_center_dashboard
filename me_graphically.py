import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import requests

# Load geojson data
url = 'https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json'
r = requests.get(url)
geojson_counties = json.loads(r.text)

# Read county data
counties = pd.read_csv('vacounties.csv')

# Assigning Number of Friends/Family

counties['Number of Friends/Family'] = 0  # Initialize column with 0
counties.loc[counties['Jurisdiction'] == 'Fairfax County', 'Number of Friends/Family'] = 12
counties.loc[counties['Jurisdiction'] == 'Albemarle County', 'Number of Friends/Family'] = 1
counties.loc[counties['Jurisdiction'] == 'Suffolk city', 'Number of Friends/Family'] = 3
counties.loc[counties['Jurisdiction'] == 'Richmond city', 'Number of Friends/Family'] = 3
counties.loc[counties['Jurisdiction'] == 'Arlington County', 'Number of Friends/Family'] = 8
counties.loc[counties['Jurisdiction'] == 'Loudon County', 'Number of Friends/Family'] = 7
counties.loc[counties['Jurisdiction'] == 'Rockingham County', 'Number of Friends/Family'] = 4
counties.loc[counties['Jurisdiction'] == 'Isle of Wight County', 'Number of Friends/Family'] = 8
counties.loc[counties['Jurisdiction'] == 'Chesapeake city', 'Number of Friends/Family'] = 6
counties.loc[counties['Jurisdiction'] == 'Virginia Beach city', 'Number of Friends/Family'] = 9  
counties.loc[counties['Jurisdiction'] == 'Hanover County', 'Number of Friends/Family'] = 8
counties.loc[counties['Jurisdiction'] == 'Goochland County', 'Number of Friends/Family'] = 2
counties.loc[counties['Jurisdiction'] == 'Henrico County', 'Number of Friends/Family'] = 2


# Years lived in each location (used for marker size)
years_lived = {
    "Fairfax County": 18,
    "Albemarle County": 9,
    "Rockingham County": 12,
    "Virginia Beach": 9
}

# Latitude & Longitude for Highlighted Counties
highlight_locations = pd.DataFrame({
    'Jurisdiction': ['Fairfax County', 'Albemarle County', 'Rockingham County', 'Virginia Beach'],
    'lat': [38.8462, 38.0293, 38.4021, 36.8529],
    'lon': [-77.3064, -78.4767, -78.8704, -75.9779],
    'years_lived': [years_lived[j] for j in years_lived],  # Map years lived to size
    'color': ['green', 'red', 'green', 'green']
})

# Create the choropleth
fig = px.choropleth(counties,
                    geojson=geojson_counties,
                    locations='FIPS',
                    color='Number of Friends/Family',
                    scope='usa',
                    hover_name='Jurisdiction',
                    hover_data=['Number of Friends/Family', 'Total Population'],
                    color_continuous_scale=px.colors.sequential.Blues,
                    title='Friends/Family I have By County they Live in Virginia')

fig.update_geos(fitbounds='locations')

years = [16, 1, 4, 1]

# Add scatter points (stars) based on years lived
for i, row in highlight_locations.iterrows():
    location_name = row['Jurisdiction']
    # Update legend entry for Albemarle County (Red Star) to indicate "Currently Here"
    if location_name == "Albemarle County":
        location_name += " (Currently Here)"
    fig.add_trace(go.Scattergeo(
        lon=[row['lon']],
        lat=[row['lat']],
        mode='markers',
        marker=dict(symbol='star', size=row['years_lived'], color=row['color']),
        name=f"{location_name} ({years[i]} years)"
    ))

# Update legend position and title
fig.update_layout(
    legend=dict(x=0, title="Places I've Lived by number of years"),
    margin=dict(l=0, r=0, t=40, b=0)
)

fig.show()








