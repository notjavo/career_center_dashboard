import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import subprocess
anonymous_app_counts = pd.read_csv('anonymous_app_counts.csv') # Read in app Count data

subtopic = st.selectbox("What Aspect of UVA First Generation Data do you Want to see?", ["Overview", "Internship Applications", "Job Applications",]) 

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
    st.write("")
    st.subheader("UVA Students With Handshake Application and First Gen Data From 2021-2024")
    total_counts = anonymous_app_counts['First Gen'].value_counts().rename('Number of UVA students')
    total_proportions = anonymous_app_counts['First Gen'].value_counts(normalize=True).rename('Percent of UVA Students')
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
    internship_counts = anonymous_app_counts[anonymous_app_counts.Internship >= threshold]['First Gen'].value_counts().rename('Percent(\\%)')
    int_porportions = (100 * (1 - round(internship_counts/total_counts, 2))).rename('Percent (%)')
    job_counts = anonymous_app_counts[anonymous_app_counts.Job >= threshold]['First Gen'].value_counts().rename('\\%')
    job_porportions =(100 * (1 - round(job_counts/total_counts, 2))).rename('Percent (%)')
    # Ouputting Int/Job Tables for Percet Under Threshold
    col3, col4 = st.columns(2)
    with col3:
        st.write(f"UVA Students < {threshold} internship app(s):\n", int_porportions)
    with col4:
        st.write(f"UVA Students < {threshold} job app(s):\n", job_porportions)


if subtopic == 'Internship Applications':
    # Look at percentiles from lower to upper threshold
    percentiles_lower = st.slider('Select lower threshold for percentiles chart', 0, 100, 0)
    percentiles_upper = st.slider('Select upper threshold for perentiles chart', 0, 100, 0 )
    percentiles = [x * .01 for x in range(percentiles_lower, percentiles_upper)]
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
    percentiles = [x * .01 for x in range(percentiles_lower, percentiles_upper)]
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