import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

handshake_data = pd.read_csv('streamlit_data_anonymous.csv') # Read in app Count data



# Function to take user defined input and display data based on this input
def user_input():
    point_of_interest = st.selectbox("Which Metric do you want to see?", ["Internship Applications", "Job Applications", "Number of Fairs Attended", "Alignment", "Career Readiness"])
    schools = st.multiselect("Which College Do you want to see data for ?", ["College and Graduate School of Arts & Sciences",                                                                            
                                                                                "School of Engineering & Applied Science",           
                                                                                "School of Architecture",                             
                                                                                "School of Education and Human Development",          
                                                                                "School of Data Science",                             
                                                                                "School of Nursing",                                  
                                                                                "School of Continuing and Professional Studies",      
                                                                                "School of Medicine",                                 
                                                                                "Darden Graduate School of Business Administration"])
    for school in schools:
        visual = handshake_data[handshake_data['College_fds_2024'] == school].groupby([ 'College_fds_2024', 'Number of Internships',])[point_of_interest] \
                                                                .agg(['mean', 'median', 'std', 'min', 'max','count']).round(2)
        st.write(f"{point_of_interest} for {school} 2024 graduates by Number of Internships")
        st.write(visual)

    # Make a side by side boxplot of the data
    fig, ax = plt.subplots()
    handshake_data.boxplot(column=point_of_interest, by='Number of Internships', ax=ax)
    plt.title(f"{point_of_interest} by Number of Internships")
