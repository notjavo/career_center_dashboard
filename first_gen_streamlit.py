import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import first_gen




# Give page a title and give Uer options
st.title('UVA Career Center Data')
topic = st.sidebar.selectbox(
    'What Do you want to look at? ',
    ['First Gen Data', 'Internship Impact','State Retention Data', 'Career Center Surveys'])


if topic == 'First Gen Data':
    first_gen.user_input()

elif topic == 'Career Center Survey Overviews':
    st.write("-3")
elif topic == 'State Retention Data':
    st.write(-2)
elif topic == 'Internship Impact':
    st.write(-1)