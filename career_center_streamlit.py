import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import first_gen, data_by_groups, majors



st.set_page_config(layout="wide")  # Enables wider layout but not forced full width
st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 20%;  /* Adjust this percentage to control width */
        margin: auto;  /* Centers the content */
    }
    </style>
    """,
    unsafe_allow_html=True,
)




# Give Dashboard a title and give User options
st.sidebar.title('UVA Career Center Data')
topic = st.sidebar.selectbox(
    'What Data Do you want to look at? ',
    ['Data by School/Groups', 'First Gen Data', 'Internship Impact', 'State Retention Data', 'IPP Data', 'Internships By Major'],
    key='main')


# Call other scripts based on user input
if topic == 'Data by School/Groups':
    data_by_groups.user_input() 
elif topic == 'First Gen Data':
    first_gen.user_input() 
elif topic == 'Internship Impact':
    #exec(open('internship_impact_model.py').read())
    st.write(-1)
elif topic == 'State Retention Data':
    st.write(-2)
elif topic == 'IPP Data':
    #exec(open('IPP_Data.py').read())
    st.write(-1)
elif topic == 'Internships By Major':
    majors.user_input()