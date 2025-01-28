import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


## Links for below statistics
#https://nces.ed.gov/programs/coe/pdf/2022/cce_508.pdf 
#https://uvamagazine.org/articles/the_class_of_2026_by_the_numbers 
#https://news.virginia.edu/content/final-exercises-2022#:~:text=Looking%20Backlookingbacklooking-,University%20News,Play%20Video 
#https://news.virginia.edu/content/diversity-rise 

### UVA First Generation rate by class
# * Class of 2028: 18.8%
# * Class of 2027: 17.5%
# * Class of 2026: 15.7%
# * Class of 2025: 12%    (admitted students not matriculated for 2025)
# * Class of 2024: 13.6%
# * Class of 2023: 12.8%
# * Class of 2022: 7.7%

# ### Overview of First Generation rate in US
# * 58% of US children under age 18 have one or more parent with a college degree 

# Reading in Handshake Data
handshake_data = pd.read_csv('streamlit_data_anonymous.csv') # Read in app Count data

def user_input():
    """ Function to take user defined input and display data based on this input
    """ 
    subtopic_1 = 'Overview'
    subtopic_1 = st.selectbox("What Aspect of UVA First Generation Data do you Want to see?", ["Overview", "Internship Applications", "Job Applications",])

    if subtopic_1 == "Overview":
        # First Gen Data
        df = pd.DataFrame({'year': [2022, 2023, 2024, 2025, 2026, 2027, 2028],
                    'first_gen': [7.7, 12.8, 13.6, 12, 15.7, 17.5, 18.8]})

        # Plotting UVA's First Generation Data 
        fig, ax = plt.subplots()
        df.plot.bar(x='year', y='first_gen', rot=45, color='orange', ax=ax)
        ax.set_ylim(0, 25)
        ax.set_title('Percentage of Students First Generation by UVA Class', fontsize=14, fontweight='bold')
        ax.set_xlabel('Graduating Class', fontsize=10)
        ax.set_ylabel('Percentage (%)', fontsize=10)
        plt.tight_layout()
        # Adding text annotations
        for i, v in enumerate(df['first_gen']):
            ax.text(i, v + 1, f'{v:.1f}', ha='center')
        # Displaying the plot in Streamlit
        st.pyplot(fig)

        # Looking at Counts and Proportions of First gen or Not
        st.write("")
        st.subheader("UVA Students With Handshake Application and First Gen Data From 2021-2024")
        total_counts = handshake_data['First Gen'].value_counts().rename('Number of UVA students')
        total_proportions = handshake_data['First Gen'].value_counts(normalize=True).rename('Percent of UVA Students')
        col1, col2 = st.columns(2)
        with col1:
            st.write(total_counts)
        with col2:
            st.write(round(total_proportions * 100, 2))

        # Visualizing percent with less than given number of apps by group
        threshold = 0 # Initialize threshold using a placeholder
        st.subheader("Percent of UVA Students With Less Than Given Number of Applications")
        threshold = st.slider("Cutoff Number of Ints/Job Applications", 0, 100, 0)
        # Percent of Each Group
        internship_counts = handshake_data[handshake_data['Internship Applications']>= threshold]['First Gen'].value_counts().rename('Percent(\\%)')
        int_porportions = (100 * (1 - round(internship_counts/total_counts, 2))).rename('Percent (%)')
        job_counts = handshake_data[handshake_data['Job Applications'] >= threshold]['First Gen'].value_counts().rename('\\%')
        job_porportions =(100 * (1 - round(job_counts/total_counts, 2))).rename('Percent (%)')
        # Ouputting Int/Job Tables for Percet Under Threshold
        col3, col4 = st.columns(2)
        with col3:
            st.write(f"UVA Students < {threshold} internship app(s):\n", int_porportions)
        with col4:
            st.write(f"UVA Students < {threshold} job app(s):\n", job_porportions)


    elif subtopic_1 == 'Internship Applications':
        # Look at percentiles from lower to upper threshold
        percentiles_lower = st.slider('Select lower threshold for percentiles chart', 0, 100, 0)
        percentiles_upper = st.slider('Select upper threshold for perentiles chart', 0, 100, 0 )
        percentiles = [x * .01 for x in range(percentiles_lower, percentiles_upper)]
        # Group by First Gen and calculate percentiles
        int_app_percentiles = handshake_data.groupby('First Gen')['Internship Applications'].quantile(percentiles).unstack(level=1)

        # Plotting Percentiles plot for Internships
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        # colors = {'False': 'darkorange', 'True': 'blue'}
        for i, first_gen in enumerate(int_app_percentiles.index):
            ax1.plot(int_app_percentiles.columns, int_app_percentiles.values[i], marker='x', label=first_gen)
        # Add labels, title, and legend
        ax1.set_xlabel('Percentiles')
        ax1.set_ylabel('Internship Applications')
        ax1.set_title('Internship Applications by percentile First Gen Students')
        ax1.legend(title='First Generation student')
        ax1.grid(True)
        # Displaying the plot in Streamlit
        st.pyplot(fig1)


    elif subtopic_1 == 'Job Applications':
        percentiles_lower = st.slider('Select lower threshold for percentiles chart', 0, 100, 0)
        percentiles_upper = st.slider('Select upper threshold for perentiles chart', 0, 100, 51)
        percentiles = [x * .01 for x in range(percentiles_lower, percentiles_upper)]
        job_app_percentiles = handshake_data.groupby('First Gen')['Job Applications'].quantile(percentiles).unstack(level=1)

        # Job percentile plot
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        for i, first_gen in enumerate(job_app_percentiles.index):
            ax1.plot(job_app_percentiles.columns, job_app_percentiles.values[i], marker='x', label=first_gen)
        # Add labels, title, and legend
        ax1.set_xlabel('Percentiles')
        ax1.set_ylabel('Job Applications')
        ax1.set_title('Job Applications by percentile First Gen Students')
        ax1.legend(title='First Generation student')
        ax1.grid(True)
        # Displaying the plot in Streamlit
        st.pyplot(fig1)



 # # Make A choropleth of applications by students destination

# fips_groundwater = pd.merge(va_counties, fds_2024_app_counts, left_on='CTYNAME', right_on='Jurisdiction', how='inner')
# geojson_url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
# # Create choropleth map
# fig = px.choropleth(
#     fds_2024_app_counts,
#     geojson=geojson_url,
#     locations='FIPS',
#     color='mean_county_depth',
#     color_continuous_scale=px.colors.sequential.PuBu[::-1],
#     scope='usa',  # Limits map to the United States
#     labels={'values': 'mean water depth across stations by county'}
# )
# fig.update_geos(fitbounds="locations", visible=False)
# fig.update_layout(
#     title_text=f"{state} Mean Water Table Depth by County",
#     title_x=0
# )