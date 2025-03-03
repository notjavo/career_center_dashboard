import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

handshake_data = pd.read_csv('streamlit_data_anonymous.csv', low_memory=False) # Read in app Count data

# Function to take user defined input and display data based on this input
def main():
    visual = st.sidebar.selectbox("Which Visual do you want to see?", ["Overview", "Bar Chart", "Percentiles", "Table"], key='visual')
    point_of_interest = st.sidebar.selectbox("Which Metric do you want to see?", ["Job Applications", "Internship Applications",
                                                                          "num_events_checked_in", "num_events_signed_up", "num_appointments", "num_fairs", 
                                                                            "Alignment", "Career Readiness"])
    def schools():
        schools = st.sidebar.multiselect("Which College Do you want to see data for ?", 
                                         ["All",
                                         "College and Graduate School of Arts & Sciences",                                                                            
                                         "School of Engineering & Applied Science",           
                                         "School of Architecture",                             
                                         "School of Education and Human Development",          
                                         "School of Data Science",                             
                                         "School of Nursing",                                  
                                         "School of Continuing and Professional Studies",      
                                         "School of Medicine",                                 
                                         "Darden Graduate School of Business Administration"],
                                        ["College and Graduate School of Arts & Sciences", "School of Engineering & Applied Science" ] ) # Set initial Schools
        return schools


    if visual == "Overview":
        # Make unified num_internships column
        handshake_data['num_internships'] = pd.concat([handshake_data['Number of Internships'],  # 2024 
                                                       handshake_data['num_internships_from_plans'], # plans only
                                                handshake_data['Number of Internships_fds_2023'], 
                                                 handshake_data['If you participated in internships, how many internships did you have while attending the University of Virginia?_fds_2022'],
                                                handshake_data['How many internships (summer and/or academic year) did you have while attending the University of Virginia?_fds_2021']],
                                                ignore_index=True)
        # Compute counts and percentages
        counts = handshake_data['num_internships'].value_counts()
        percentages = handshake_data['num_internships'].value_counts(normalize=True) * 100
        data = handshake_data[handshake_data['num_internships'].notnull()] # Only look at data with Internship Counts
        
        # Plot the bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(percentages.index, percentages.values, width=0.8)
        # Add labels on top of bars (percentages)
        ax.bar_label(bars, labels=[f"{v:.2f}%" for v in percentages.values], padding=3)
        ax.set_xlabel('Number of Internships by UVA Student')
        ax.set_ylabel(f'Percent of Students')
        ax.set_title(f'UVA Class of 2021-2024 Percent of Students with 0, 1, 2, 3+ internships')
        ax.legend(title=f"Among {len(data)} UVA Graduates 2021-2024" , bbox_to_anchor=(1, 1), framealpha=.5) 
        ax.grid(True)
        st.pyplot(fig)

        # Demographics of Students in Visual
        st.subheader('Demographics of Students in Visual')
        data['Athlete_fds_2024'] = data['Athlete_fds_2024'].replace({'Yes': True, 'TRUE': True , 'FALSE': False, 'No': False})
        data['Gender_fds_2024'] = data['Gender_fds_2024'].replace({'Male': True, 'Female': False})

        summary_stats = data.groupby('num_internships')[['First Gen', 'Alignment', 'Career Readiness',
                                                         'Job Applications', 'Internship Applications', 'num_fairs', 'num_events_signed_up',
                                                         'Athlete_fds_2024' ,'Gender_fds_2024', #'Education Level_fds_2024'
                                                        ]].mean()
        summary_stats['First Gen (%)'] = (summary_stats.pop('First Gen') * 100).round(2) # Change column name and porportion -> Percentage
        summary_stats['Athlete (%)'] = (summary_stats.pop('Athlete_fds_2024') * 100).round(2)
        summary_stats['Male (%)'] = (summary_stats.pop('Gender_fds_2024') * 100).round(2)
        summary_stats = summary_stats.applymap(lambda x: f"{x:.2f}").T
        st.table(summary_stats)

        # Download the Data
        st.subheader('Download Subset of Student Data in Visual')
        st.download_button(
            label="🔥 Download this Data!🔥",
            data=data.to_csv(index=False).encode('utf-8'), # Convert to CSV
            file_name=f'{visual}.csv', # filename based on userinput
            mime="text/csv", # tells browser it's a csv
            help="Click to download data of students in this plot as CSV!")
        st.write('Rows:',data.shape[0], "Columns", data.shape[1], data.head(3))
    
        
        st.subheader('Feed New Data To Dashboard')
        # Upload New Data
        uploaded_file = st.file_uploader("Add Data to Dashboard", type="csv")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write("Preview of uploaded file:")
            st.dataframe(df)


    elif visual == "Bar Chart":
        schools = schools()
        avg_stat = st.sidebar.selectbox("Which Stat do you want to see?", ["mean", "median"])
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
        schools = schools()
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
        schools = schools()
        for school in schools:
            visual = handshake_data[handshake_data['College_fds_2024'] == school].groupby([ 'College_fds_2024', 'Number of Internships',])[point_of_interest] \
                                                                    .agg(['mean', 'median', 'std', 'min', 'max','count']).round(2)
            st.write(f"{point_of_interest} for {school} 2024 graduates by Number of Internships")
            st.write(visual)
    else:
        print('error')