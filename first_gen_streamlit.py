import numpy as np
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


anonymous_app_counts = pd.read_csv('anonymous_app_counts.csv') # Read in app Count data


# Give page a title and give Uer options
st.title('UVA Career Center Data')
topic = st.sidebar.selectbox(
    'What Do you want to look at? ',
    ['Internship Data', 'First Gen Data', 'In-State / Out of State Data'])


if topic == 'First Gen Data':
    subtopic = st.selectbox("What Aspect of UVA 2024 First Data do you Want to see?", ["Overview", "Internship Applications", "Job Applications",]) 

    if subtopic == "Overview":
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
        st.write("UVA Students With Handshake Applications Data From 2021-2024")
        total_counts = anonymous_app_counts['First Gen'].value_counts().rename('Number of UVA students')
        total_proportions = anonymous_app_counts['First Gen'].value_counts(normalize=True).rename('Percent of UVA Students')
        col1, col2 = st.columns(2)
        with col1:
            st.write(total_counts)
        with col2:
            st.write(round(total_proportions * 100, 2))

        # Threshold apps
        threshold = st.slider('Threshold', 0, 10, 0) # Number of ints/jobs higher or less than
        internship_counts = anonymous_app_counts[anonymous_app_counts.Internship >= threshold]['First Gen'].value_counts().rename('%')
        int_porportions = 100 * (1 - round(internship_counts/total_counts, 2))
        
        col3, col4 = st.columns(2)
        with col3:
            st.write(f"Percent (%) less than {threshold} internship application(s):\n", int_porportions, "\n\n")

        # anonymous_app_counts.Job.sort_values(ascending=True)[-20:]
        job_counts = anonymous_app_counts[anonymous_app_counts.Job >= threshold]['First Gen'].value_counts().rename('%')
        job_porportions = 100 * (1 - round(job_counts/total_counts, 2))
        with col4:
            st.write(f"Percent less than {threshold} job application(s):\n", job_porportions)


    if subtopic == 'Internship Applications':
        # Look at percentiles from lower to upper threshold
        percentiles_lower = st.slider('Select lower threshold for percentiles chart', 0, 100, 0)
        percentiles_upper = st.slider('Select upper threshold for perentiles chart', 0, 100, 51)
        percentiles = [x * 0.01 for x in range(percentiles_lower, percentiles_upper)]
        # Group by First Gen and calculate percentiles
        int_app_percentiles = anonymous_app_counts.groupby('First Gen')['Internship'].quantile(percentiles).unstack(level=1)
        


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

    elif subtopic == 'Job Applications':
        percentiles_lower = st.slider('Select lower threshold for percentiles chart', 0, 100, 0)
        percentiles_upper = st.slider('Select upper threshold for perentiles chart', 0, 100, 51)
        percentiles = [x * 0.01 for x in range(percentiles_lower, percentiles_upper)]
        job_app_percentiles = anonymous_app_counts.groupby('First Gen')['Job'].quantile(percentiles).unstack(level=1)

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