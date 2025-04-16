import streamlit as st
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf


fds_outcomes = pd.read_csv('fds_model_outcome_data.csv')

impact_model = smf.glm(formula='Outcome_binary ~ Internship_binary',
data = fds_outcomes, family=sm.families.Binomial()).fit()

st.write(impact_model.summary())

st.write(np.exp(impact_model.params))

st.header('Odds Ratio')
st.write("This coef is stating that, if a University of Virginia student has one or more internships throughout their time at UVA, at the time of them taking the final destination survey, they are 32% more likely to indicate that they have a full time position compared to a student who completed zero internships throughout their time at UVA. ")

