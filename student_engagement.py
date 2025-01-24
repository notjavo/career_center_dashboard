import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

handshake_data = pd.read_csv('handshake_data.csv') # Read in app Count data


# Function to take user defined input and display data based on this input
def user_input(subtopic_1, subtopic_2):
    if subtopic_2:
        for school in subtopic_2:
            visual = handshake_data[handshake_data['College_fds_2024'] == school].groupby([ 'College_fds_2024', 'Number of Internships',])[subtopic_1] \
                                                                    .agg(['mean', 'median', 'std', 'min', 'max','count']).round(2)
            st.write(f" {subtopic_1} for UVA {school} 2024 graduates by Number of Internships")
            st.write(visual)


# User input from Streamlit dashboard
metric = st.selectbox("Which Metric do you want to see?", ["Number of Fairs Attended", "Job Applications", "Internship Applications", "Alignment", "Career Readiness"])
school = st.multiselect("Which College Do you want to see data for ?", ["College and Graduate School of Arts & Sciences",                                                                            
                                                                                "School of Engineering & Applied Science",           
                                                                                "School of Architecture",                             
                                                                                "School of Education and Human Development",          
                                                                                "School of Data Science",                             
                                                                                "School of Nursing",                                  
                                                                                "School of Continuing and Professional Studies",      
                                                                                "School of Medicine",                                 
                                                                                "Darden Graduate School of Business Administration"])
user_input(metric, school)