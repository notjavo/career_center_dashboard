import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Reading in Handshake Data
handshake_data = pd.read_csv('streamlit_data_anonymous.csv') # Read in app Count data

def user_input():
    """ Function to take user defined input and display data based on this input
    """ 
    subtopic_1 = 'Overview'
    subtopic_1 = st.selectbox("What Aspect of UVA First Generation Data do you Want to see?", ["Overview", "Percentiles", "Bar Chart"])

    if subtopic_1 == "Overview":
        # First Gen Data
        df = pd.DataFrame({'year': [2022, 2023, 2024, 2025, 2026, 2027, 2028],
                    'first_gen': [11.07, 12.81, 13.60, 11.96, 15.62, 17.37, 18.83]})

        # Plotting UVA's First Generation Data 
        fig, ax = plt.subplots()
        df.plot.bar(x='year', y='first_gen', rot=45, color='darkorange', ax=ax)
        ax.set_ylim(0, 25)
        ax.set_title('Percentage First Generation Student by UVA Class', fontsize=14, fontweight='bold')
        ax.set_xlabel('Graduating Class', fontsize=10)
        ax.set_ylabel('Percentage of Students who are First Generation(%)', fontsize=10)
        plt.tight_layout()
        # Adding text annotations
        for i, v in enumerate(df['first_gen']):
            ax.text(i, v + 1, f'{v:.1f}%', ha='center')
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



    elif subtopic_1 == "Percentiles":
        point_of_interest = st.selectbox("Which Metric do you want to see?", ["Job Applications", 
                                                                          "Internship Applications",
                                                                            "num_fairs", 
                                                                            "Alignment",
                                                                              "Career Readiness"])
        def generate_percentiles():
             # Look at percentiles from lower to upper threshold
            percentiles_lower = st.slider('Select lower threshold for percentiles chart', 0, 100, 0)
            percentiles_upper = st.slider('Select upper threshold for perentiles chart', 0, 100, 50)
            percentiles = [x * .01 for x in range(percentiles_lower, percentiles_upper)]
            return percentiles
        
        def chart_percentiles(poi_percentiles):
            # Plotting Percentiles plot for point_of interest
            fig1, ax1 = plt.subplots(figsize=(8, 6))
            # colors = {'False': 'darkorange', 'True': 'blue'}
            for i, first_gen in enumerate(poi_percentiles.index):
                ax1.plot(100*poi_percentiles.columns, poi_percentiles.values[i], marker='x', label=first_gen)
            # Add labels, title, and legend
            ax1.set_xlabel('Percentile')
            ax1.set_ylabel(f'{point_of_interest}')
            ax1.set_title(f'{point_of_interest} by percentile')
            ax1.legend(title='First Generation Student (True/False)')
            ax1.grid(True)
            # Displaying the plot in Streamlit
            st.pyplot(fig1)

        percentiles = generate_percentiles() # User generated percentiles
        poi_percentiles = handshake_data[handshake_data['College_fds_2024'].notnull()].groupby('First Gen')[point_of_interest].quantile(percentiles).unstack(level=1)
        chart_percentiles(poi_percentiles) # chart percentiles by School All students


    if subtopic_1 == "Bar Chart":
        point_of_interest = st.selectbox("Which Metric do you want to see?", ["Job Applications", 
                                                                          "Internship Applications",
                                                                          "num_events_checked_in",
                                                                          "num_events_signed_up",
                                                                          "num_appointments",
                                                                            "num_fairs", 
                                                                            "Alignment",
                                                                              "Career Readiness"])
        avg_stat = st.selectbox("Which Stat do you want to see?", ["mean", "median"])

        def bar_chart(poi_stats, counts, point_of_interest):
            # Define custom colors
            colors = ['#1f77b4', '#ff7f0e']  # Blue and Orange (customizable)

            # Plotting Bar Chart for point_of_interest
            fig, ax = plt.subplots(figsize=(10, 6))
            poi_stats.plot(kind='bar', ax=ax, width=0.8, color=colors)

            # Add labels, title, and legend
            ax.set_xlabel('First Generation Student (True/False)')
            ax.set_ylabel(f'{point_of_interest} ({avg_stat})')
            ax.set_title(f'{point_of_interest} by Group')
            ax.grid(True)

            # Add values on the bars
            for container in ax.containers:
                ax.bar_label(container, fmt='%.1f', padding=3)

            # Legend
            legend_labels = [f"{avg_stat} {point_of_interest}\nUVA 2024 ({counts} students)"]
            ax.legend(legend_labels, title='All UVA Schools (2024 Graduating Class)', bbox_to_anchor=(1.05, 1), framealpha=.3)

            # Display in Streamlit
            st.pyplot(fig)

        # Aggregate statistics
        poi_stats = handshake_data.groupby('First Gen')[point_of_interest].agg(avg_stat).round(2)
        counts = handshake_data['College_fds_2024'].notnull().sum()

        # Call the function
        bar_chart(poi_stats, counts, point_of_interest)



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