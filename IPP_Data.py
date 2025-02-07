import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

data = pd.read_csv('streamlit_data_anonymous.csv')

# Display the resulting DataFrame
data['time of IPP'] = data['time of IPP'].apply(lambda x: x[0] if isinstance(x, list) else x)
df = pd.DataFrame({'time of IPP': [data['time of IPP'].dropna().tolist()]})
df['time of IPP'] = df['time of IPP'].astype('category')

# Optionally, reorder categories if needed
df['time of IPP'] = df['time of IPP'].cat.set_categories([
    ['AY 19-20'], ['AY 20-21'], ['AY 21-22'], ['Fall 22'], ['Fall 23'], 
     ['Spring 2020'], ['Spring 2021'], ['Spring 22'], ['Spring 23'], ['Spring 24'], 
     ['Summer 2020'], ['Summer 2021'], ['Summer 22'], ['Summer 23']],
     ordered=True
)



st.write(df)

# Set up Plotting Data
mybars = df['time of IPP'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
# Create a color list with the desired repetitions
colors = ['Navy']*3 + ['red']*2 + ['green']*5 + ['orange']*4  # Adjust the numbers as needed

# Ensure the number of colors matches the number of bars
if len(colors) != len(mybars):
    st.error("Number of colors must match the number of bars!")
else:
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    # Create bar plot with specified colors
    bars = ax.bar(mybars.index, mybars.values, color=colors)
    # Add height labels above the bars
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval, 2), 
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    # Labels and title
    ax.set_ylabel('Students in IPP Program')
    ax.set_xlabel('School Year and Term')
    ax.set_title('UVA IPP Program Participation')
    ax.set_xticklabels(mybars.index, rotation=45)
    # Display in Streamlit
    st.pyplot(fig)

# Output other IPP data to streamlit 
st.write(data[data['time of IPP'].notnull()]['College_fds_2024'].value_counts(normalize=False))

st.write(data)
st.write(data[data['time of IPP'].notnull()])
