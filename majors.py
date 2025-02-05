import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
data = pd.read_csv('streamlit_data_anonymous.csv', low_memory=False)


# Combine the number of internship and major columns together 
data['Major'] = pd.concat([data['Primary Major'], data['Recipient Primary Majors_fds_2021'], data['Recipient Primary Major_fds_2022'], data['Q5.4_fds_2024']], ignore_index=True)
data['num_internships'] = pd.concat([data['Number of Internships'], data['Q10.1_fds_2024'], data['How many internships (summer and/or academic year) did you have while attending the University of Virginia?_fds_2021'], data['If you participated in internships, how many internships did you have while attending the University of Virginia?_fds_2022']], ignore_index=True)


counts= data.groupby('Major')['num_internships'].value_counts().unstack(fill_value=0)

# Compute row-wise percentages
row_percents = (counts.div(counts.sum(axis=1), axis=0) * 100)
total_students = counts.sum(axis=1).rename('Total Students')


# Append '_percent' to column names
row_percents.columns = [f"{col} (%)" for col in row_percents.columns]

# Combine counts and percentages
result = pd.concat([total_students, counts], axis=1)
result = pd.concat([result, row_percents], axis=1)
result.columns.name = 'Num Internships'
result.index.name = 'Major'


# User Specified Filters on the Data
Threshold = st.slider() # minimum number of students in major to show
sorting_column = '0 (%)' # column to filter by 
result = result[result['Total Students']>=Threshold].sort_values(by=sorting_column, ascending=False) # Show Highest First
result.round(1)


# Save counts and percent df's
result_percent=result.iloc[:, 5:]
result = result.iloc[:, 1:5]

plt.figure(figsize=(8,6))
sns.heatmap(result_percent, annot=True, cmap="Blues")

plt.title("Internship Distribution Heatmap")
plt.ylabel("Major")
plt.xlabel("Num Internships")
plt.show()