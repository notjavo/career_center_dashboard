import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

barriers_data = pd.read_csv('Barriers_anonymous.csv')


demographic = st.sidebar.selectbox("Which Groups do you want to filter by", ['First Gen', 'College'])
barriers = st.sidebar.selectbox("Which Aspect of Barriers Survey do you want to compare", 
                                ['Most Common Barrier?', 'Reason to not persue Intership?'])

if demographic == 'First Gen':
    st.write(pd.crosstab(barriers_data['Q4'], barriers_data[barriers]))
elif demographic == 'College':
    st.write(pd.crosstab(barriers_data['Q4'], barriers_data['Q2_2']))
else:
    st.write(-1)