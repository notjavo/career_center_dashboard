import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

handshake_data = pd.read_csv('streamlit_data_anonymous.csv', low_memory=False) # Read in app Count data

# Function to take user defined input and display data based on this input
def user_input():
    schools = st.multiselect("Which College Do you want to see data for ?", [   "All",
                                                                                "College and Graduate School of Arts & Sciences",                                                                            
                                                                                "School of Engineering & Applied Science",           
                                                                                "School of Architecture",                             
                                                                                "School of Education and Human Development",          
                                                                                "School of Data Science",                             
                                                                                "School of Nursing",                                  
                                                                                "School of Continuing and Professional Studies",      
                                                                                "School of Medicine",                                 
                                                                                "Darden Graduate School of Business Administration"],
                                                                                ["College and Graduate School of Arts & Sciences",                                                                            
                                                                                "School of Engineering & Applied Science" ] )
    point_of_interest = st.selectbox("Which Metric do you want to see?", ["Job Applications", 
                                                                          "Internship Applications",
                                                                          "num_events_checked_in",
                                                                          "num_events_signed_up",
                                                                          "num_appointments",
                                                                            "num_fairs", 
                                                                            "Alignment",
                                                                              "Career Readiness"], key='point_of_interest')
    visual = st.selectbox("Which Visual do you want to see?", ["Bar Chart", "Percentiles", "Table"], key='visual')
    
    if visual == "Bar Chart":
        avg_stat = st.selectbox("Which Stat do you want to see?", ["mean", "median"])
        def bar_chart(poi_stats, counts):
            # Plotting Bar Chart for point_of interest
            fig, ax = plt.subplots(figsize=(10, 6))
            poi_stats.plot(kind='bar', ax=ax, width=0.8)
            # Add labels, title, and legend
            ax.set_xlabel('Number of Internships')
            ax.set_ylabel(f'{point_of_interest} {avg_stat}')
            ax.set_title(f'{point_of_interest} by Group')
            ax.grid(True)
             # Add values on the bars
            for container in ax.containers:
                ax.bar_label(container, fmt='%.1f', padding=3)

            # Modify legend labels to include counts
            if isinstance(counts, (pd.Series, dict)):  # If counts has multiple values (can use len())
                legend_labels = [f"{avg_stat} {point_of_interest}\n{group} ({counts[group]} Hoos)" for group in counts.index]
                ax.legend(legend_labels, title='UVA Schools (2024 Graduating Class)', bbox_to_anchor=(1.05, 1), framealpha=.3) # ,bbox_to_anchor=(1.05, 1)
            else:  # If counts is a single number (no len())
                legend_labels = [f"{avg_stat} {point_of_interest}\nUVA 2024 ({counts} students)"]
                ax.legend(legend_labels, title='All UVA Schools (2024 Graduating Class)', bbox_to_anchor=(1.05, 1), framealpha=.3)
            st.pyplot(fig)


        # Group by school
        if schools ==  ['All']:
            poi_stats = handshake_data.groupby('Number of Internships')[point_of_interest].agg(avg_stat).round(2)
            counts = handshake_data['College_fds_2024'].notnull().sum()
            bar_chart(poi_stats, counts)
        else:
            grouped = handshake_data[handshake_data['College_fds_2024'].isin(schools)]
            poi_stats = grouped.groupby(['College_fds_2024', 'Number of Internships'])[point_of_interest].agg(avg_stat).round(2).unstack(level=0)
            counts = grouped.groupby('College_fds_2024')['Number of Internships'].count()
            bar_chart(poi_stats, counts)


    elif visual == "Percentiles":
        handshake_data[point_of_interest] = handshake_data[point_of_interest].fillna(0)

        def generate_percentiles():
             # Look at percentiles from lower to upper Threshold
            percentiles_lower = st.slider('Select lower Threshold for percentiles chart', 0, 100, 0)
            percentiles_upper = st.slider('Select upper Threshold for perentiles chart', 0, 100, 50)
            percentiles = [(x * .01)+.01 for x in range(percentiles_lower, percentiles_upper)]
            return percentiles
        
        def chart_percentiles(poi_percentiles):
            # Plotting Percentiles plot for point_of interest
            fig1, ax1 = plt.subplots(figsize=(8, 6))
            # colors = {'False': 'darkorange', 'True': 'blue'}
            for i, group in enumerate(poi_percentiles.index):
                ax1.plot(100*poi_percentiles.columns, poi_percentiles.values[i], marker='x', label=group)
            # Add labels, title, and legend
            ax1.set_xlabel('Percentile')
            ax1.set_ylabel(f'{point_of_interest}')
            ax1.set_title(f'{point_of_interest} by percentile')
    
            legend_labels = [f"{point_of_interest} UVA 2024 \n {group} ({len(handshake_data[handshake_data['College_fds_2024'] == group])} students)" for group in poi_percentiles.index]
            ax1.legend(legend_labels, title='Groups')
            ax1.grid(True)
            # Displaying the plot in Streamlit
            st.pyplot(fig1)


        if schools == ['All']:
            percentiles = generate_percentiles() # User generated percentiles
            poi_percentiles = handshake_data[point_of_interest].quantile(percentiles).to_frame().T
            chart_percentiles(poi_percentiles) # chart percentiles for All students

        else:
            percentiles = generate_percentiles() # User generated percentiles
            poi_percentiles = handshake_data[handshake_data['College_fds_2024'].isin(schools)].groupby('College_fds_2024')[point_of_interest].quantile(percentiles).unstack(level=1)
            chart_percentiles(poi_percentiles) # chart percentiles by School All students


    elif visual == "Table":
        for school in schools:
            visual = handshake_data[handshake_data['College_fds_2024'] == school].groupby([ 'College_fds_2024', 'Number of Internships',])[point_of_interest] \
                                                                    .agg(['mean', 'median', 'std', 'min', 'max','count']).round(2)
            st.write(f"{point_of_interest} for {school} 2024 graduates by Number of Internships")
            st.write(visual)