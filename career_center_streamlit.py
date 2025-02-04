import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import first_gen, data_by_groups


handshake_data = pd.read_csv('streamlit_data_anonymous.csv') # Importing Handshake Data



# Give Dashboard a title and give User options
st.sidebar.title('UVA Career Center Data')
topic = st.sidebar.selectbox(
    'What Data Do you want to look at? ',
    ['Data by School/Groups', 'First Gen Data', 'Internship Impact', 'State Retention Data', 'Career Center Surveys', 'IPP Data'])


# Call other scripts based on user input
if topic == 'Data by School/Groups':
    data_by_groups.user_input() 
elif topic == 'First Gen Data':
    first_gen.user_input() 
elif topic == 'Internship Impact':
    exec(open('internship_impact_model.py').read())
elif topic == 'Career Center Survey Overviews':
    st.write("-3")
elif topic == 'State Retention Data':
    st.write(-2)
elif topic == 'IPP Data':
    exec(open('IPP_Data.py').read())
