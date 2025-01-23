import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import first_gen
import seaborn

# Clear cache
st.cache_data.clear()

handshake_data = pd.read_csv('handshake_data.csv')


# Give page a title and give Uer options
st.title('UVA Career Center Data')
topic = st.sidebar.selectbox(
    'What Do you want to look at? ',
    ['Career Center Student Engagement', 'First Gen Data', 'Internship Impact','State Retention Data', 'Career Center Surveys'])

# Add a checkbox to toggle the display of the data table
show_data = st.sidebar.checkbox('Show raw data')

if show_data:
    st.write(handshake_data)

if topic == 'Career Center Student Engagement':
    subtopic_1= st.selectbox("Which Metric do you want to see?", ["Number of Fairs Attended", "Job Applications", "Internship Applications", "Alignment", "Career Readiness"])
    subtopic_2 = st.multiselect("Which College Do you want to see data for ?", ["College and Graduate School of Arts & Sciences",                                                                            
                                                                                "School of Engineering & Applied Science",           
                                                                                "School of Architecture",                             
                                                                                "School of Education and Human Development",          
                                                                                "School of Data Science",                             
                                                                                "School of Nursing",                                  
                                                                                "School of Continuing and Professional Studies",      
                                                                                "School of Medicine",                                 
                                                                                "Darden Graduate School of Business Administration"])
    if subtopic_2:
        visual = handshake_data[handshake_data['College_fds_2024'] == (subtopic_2[0])].groupby([ 'College_fds_2024', 'Number of Internships',])[subtopic_1] \
                                                                    .agg(['mean', 'median', 'std', 'min', 'max','count'])
        visual = handshake_data[handshake_data['College_fds_2024']== (subtopic_2[1])].groupby([ 'College_fds_2024', 'Number of Internships',])[subtopic_1] \
                                                            .agg(['mean', 'median', 'std', 'min', 'max','count'])
        st.write(f" {subtopic_1} for UVA {subtopic_2} 2024 graduates by Number of Internships")
        st.write(visual)


elif topic == 'First Gen Data':
    first_gen.user_input()

elif topic == 'Career Center Survey Overviews':
    st.write("-3")
elif topic == 'State Retention Data':
    st.write(-2)
elif topic == 'Internship Impact':
    st.write(-1)