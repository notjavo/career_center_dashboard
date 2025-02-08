import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import first_gen, data_by_groups, internships_by_major

st.set_page_config(layout="wide")  # Enables wider layout but not forced full width

# Give Dashboard a title and give User options
st.sidebar.title('UVA Career Center Data')
topic = st.radio(
    'What UVA Career Center Data Do you Want to Explore? ',
    ['Trends by School at UVA', 'Internship Impact','Internships By Major', 
     'First Generation Students','State Retention Data', 'IPP Data'], horizontal=True)


# Call other scripts based on user input
if topic == 'Trends by School at UVA':
    data_by_groups.user_input() 
elif topic == 'First Generation Students':
    first_gen.user_input() 
elif topic == 'Internship Impact':
    exec(open('internship_impact_model.py').read())
elif topic == 'Internships By Major':
    internships_by_major.page_choice()
elif topic == 'State Retention Data':
    st.write(-2)
elif topic == 'IPP Data':
    exec(open('IPP_Data.py').read())
    st.write(-1)