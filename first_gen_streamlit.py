import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import subprocess
# Use pipenv install to install packages 


anonymous_app_counts = pd.read_csv('anonymous_app_counts.csv') # Read in app Count data


# Give page a title and give Uer options
st.title('UVA Career Center Data')
topic = st.sidebar.selectbox(
    'What Do you want to look at? ',
    ['First Gen Data', 'Internship Impact','State Retention Data', 'Career Center Surveys'])


if topic == 'First Gen Data':
    subprocess.run(['python', 'first_gen.py'])

elif topic == 'Career Center Surveys':
    print(2)
elif topic == 'State Retention Data':
    print(3)
elif topic == 'Internship Impact':
    print(7)