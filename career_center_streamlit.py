import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set page and Sidebar layout
st.set_page_config(layout="centered")  # Enables wider layout but not forced full width
st.html( """ <style> [data-testid="stSidebarContent"] { color: #232D4B; background-color: #E57200; } </style> """ )

# Give Dashboard a title and give user options
st.sidebar.title('UVA Career Center Data')
st.sidebar.image('uva.png', width=200, )  # Adjust the width as needed
topic = st.radio(
    'What UVA Career Center Data Do you Want to Explore? ',
    ['Trends by School at UVA', 'Internships By Major', 'First Generation Students', 'Internship Impact', 
     'State Retention Data', 'IPP Data'], horizontal=True)



# Call other scripts based on user input
if topic == 'Trends by School at UVA':
    import data_by_groups
    data_by_groups.main()

elif topic == 'First Generation Students':
    import first_gen
    first_gen.user_input()

elif topic == 'Internships By Major':
    import internships_by_major
    internships_by_major.page_choice()

elif topic == 'Internship Impact':
    # exec(open('internship_impact_model.py').read())
    st.write(-1)

elif topic == 'State Retention Data':
    st.write(-2)

elif topic == 'IPP Data':
    exec(open('IPP_Data.py').read())
    st.write(-1)
