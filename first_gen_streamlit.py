import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import subprocess
import first_gen
# Use pipenv install to install packages 



# Give page a title and give Uer options
st.title('UVA Career Center Data')
topic = st.sidebar.selectbox(
    'What Do you want to look at? ',
    ['First Gen Data', 'Internship Impact','State Retention Data', 'Career Center Surveys'])

if topic == 'First Gen Data':
    subprocess.run(['python', 'first_gen.py'])

elif topic == 'Career Center Surveys':
    st.write(-3)
elif topic == 'State Retention Data':
    st.write(-2)
elif topic == 'Internship Impact':
    st.write(-1)