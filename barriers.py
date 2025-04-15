import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

barriers_data = pd.read_csv('Barriers_anonymous.csv')

barriers_data['First Gen'] = barriers_data['Q4']
barriers_data['intership_status'] = barriers_data['Q6']
barriers_data['undergrad_research'] = barriers_data['Q2_2']
barriers_data['clinical_experience'] = barriers_data['Q2_3']
barriers_data['intership_location'] = barriers_data['Q11']
barriers_data['reason_to_not_pursue_internship'] = barriers_data['Q20']
#barriers_data['intership_barriers'] = barriers_data['Q13']

demographic = st.sidebar.selectbox("Which Groups do you want to filter by", ['First Gen', 'College'])
barriers_col = st.sidebar.selectbox("Which Aspect of Barriers Survey do you want to compare", 
                                ['intership_status', 'undergrad_research', 'clinical_experience',
                                 'intership_location', 'reason_to_not_pursue_internship'])
method = st.sidebar.selectbox("How do you want to see this data", ['Counts', 'Percentages'])


st.write("Table 1:", barriers_data[barriers_col][0], divider=True)
if method == 'Counts':
    ct = pd.crosstab(barriers_data[demographic], barriers_data[barriers_col]).reset_index()
    ct = ct.fillna(' ')
    ct = ct.iloc[1:-1, :-2]
    st.table(ct)
elif method == 'Percentages':
    ct = pd.crosstab(barriers_data[demographic], barriers_data[barriers_col])
    ct = ct.iloc[1:-1, :-2] # Get rid of junk in data
    ct.iloc[0, :] = ct.iloc[0, :]/2734 # Other students Row
    ct.iloc[1, :] = ct.iloc[1, :]/653 # Row First Gen
    ct = ct.applymap(lambda x: f"{x * 100:.2f}") # Multiply and limit decimals
    ct = round(ct.reset_index(), 2)
    st.table(ct)
else:
    st.write(-1)\

