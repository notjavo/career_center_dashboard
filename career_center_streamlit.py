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
    ['Data by School/Groups', 'First Gen Data', 'Internship Impact','State Retention Data', 'Career Center Surveys'])


if topic == 'Data by School/Groups':
    data_by_groups.user_input()

elif topic == 'First Gen Data':
    first_gen.user_input()

elif topic == 'Career Center Survey Overviews':
    st.write("-3")
elif topic == 'State Retention Data':
    st.write(-2)
elif topic == 'Internship Impact':
    st.write(-1)