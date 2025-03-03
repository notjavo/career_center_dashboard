import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


def page_choice():
    # Read in the Data
    majors_data = pd.read_csv('streamlit_data_anonymous.csv', low_memory=False)

    # Combine the number of internship and major columns together 
    majors_data['Major'] = pd.concat([majors_data['Primary Major'], majors_data['Recipient Primary Majors_fds_2021'], majors_data['Recipient Primary Major_fds_2022'], majors_data['Q5.4_fds_2024']], ignore_index=True)
    majors_data['num_internships'] = pd.concat([majors_data['Number of Internships_fds_2023'], majors_data['Number of Internships'], majors_data['How many internships (summer and/or academic year) did you have while attending the University of Virginia?_fds_2021'], 
                                                majors_data['If you participated in internships, how many internships did you have while attending the University of Virginia?_fds_2022']], ignore_index=True)

    # Get number of students by major and number of internships
    aggregated_majors = majors_data.groupby('Major')['num_internships'].value_counts().unstack(fill_value=0)
    
    # # Incorrect way
    # st.subheader(f"Getting count by major using: 'majors_data.groupby('Major')['num_internships'].size()'")
    # st.write('If a person has `Major` filled out but `num_internships` as NaN, they are still counted.')
    # st.write(majors_data.groupby('Major')['num_internships'].size())

    # # Correct way
    # st.subheader(f"Getting internship count by major using: majors_data.groupby('Major')['num_internships'].value_counts()'")
    # st.write(majors_data.groupby('Major')['num_internships'].value_counts())
    ## Proving counts of major/internship respondents by year
    # counts1 = majors_data.groupby('Recipient Primary Majors_fds_2021')['How many internships (summer and/or academic year) did you have while attending the University of Virginia?_fds_2021'].value_counts()
    # counts2 = majors_data.groupby('Recipient Primary Majors_fds_2021')['How many internships (summer and/or academic year) did you have while attending the University of Virginia?_fds_2021'].size()
    # countess = majors_data.groupby('Recipient Primary Major_fds_2022')['If you participated in internships, how many internships did you have while attending the University of Virginia?_fds_2022'].value_counts()
    # counts3 = majors_data.groupby('Primary Major')['Number of Internships_fds_2023'].value_counts()
    # counts4 = majors_data.groupby('Q5.4_fds_2024')['Number of Internships'].value_counts()
    # st.write(counts1, counts2, counts3, counts4)
    
    # Compute row-wise percentages
    row_percents = (aggregated_majors.div(aggregated_majors.sum(axis=1), axis=0)) * 100
    
    # Append ' Percent (%)' to column names
    row_percents.columns = [f"{col} (%)" for col in row_percents.columns]

    # Combine aggregated_majors and percentages
    agg_stats = pd.concat([aggregated_majors, row_percents], axis=1)

    # Add total Students Column
    agg_stats['Total Students'] = agg_stats.iloc[:, 0:4].sum(axis=1)
    
    # Streamlit user input
    user_choice = st.sidebar.selectbox('How do you want to see By Major Internship Data?', ['Sorted by Best/Worst', 'By specific Major', ])


    def get_parameters(agg_stats):
        # User Input / Sorting
        sort_option = st.sidebar.selectbox("Sort By ___ Internship Group", agg_stats.columns[0:4])  
        sort_order = st.sidebar.radio("Sort order:", ["Descending", "Ascending"]) 
        ascending = sort_order == "Descending"  # Convert to Boolean for sorting
        chart_option = st.sidebar.radio("Show Counts or Percent of Students?", ["Counts", "Percent"])
    
        return sort_option, ascending, chart_option


    def plot_chart(plot_df, result, chart_option):
         # heatmap code
        plt.figure(figsize=(8,6))
        sns.heatmap(plot_df, annot=True, cmap="Blues", linewidths=0.5,  
                    cbar_kws={'label': "Percent of UVA 2021-2024 Grads by Major", 'orientation': 'horizontal'})
        plt.title(f"{chart_option} of Students by Major")  # Set title separately
        plt.xlabel("Number of Internships")
        plt.ylabel("Major")
        plt.show()
        # Display the plot in Streamlit
        st.subheader("Plot of Internships By Major")
        st.pyplot(plt)
        st.write(result)


    if user_choice == 'Sorted by Best/Worst':
        # Call function to get user-parameters
        sort_option, ascending, chart_option = get_parameters(agg_stats)
        min_students = st.sidebar.slider("Show Majors with at least ____ Respondents 2021-2024", 0, 100, 60)
        
        # Filtered Data Frame
        result = agg_stats[agg_stats['Total Students']>=min_students].sort_values(by=sort_option, ascending=ascending) # Show Highest First

        # Save by count and percent df's
        if chart_option == 'Counts':
            plot_df = result.iloc[:, 0:4]
        else:
            plot_df = result.iloc[:, 4:-1] # Percents

        plot_chart(plot_df, result, chart_option)

    elif user_choice  == 'By specific Major':
        # Call function to get user-parameter
        majors = st.multiselect('Which Majors do you want to see majors_data for?', ['African-American & African Studies',
            'American Studies - Interdisciplinary', 'Anthropology',
            'Applied Statistics', 'Archaeology - Interdisciplinary', 'Architecture',
            'Architecture - Architectural History',
            'Architecture - Constructed Environment',
            'Architecture - Landscape Architecture',
            'Architecture - Urban & Environmental Planning', 'Art - Art History',
            'Art - History of Art & Architecture', 'Art - Studio Art', 'Astronomy',
            'Astronomy-Physics', 'Biochemistry & Molecular Genetics', 'Biology',
            'Biophysics', 'Business Administration', 'Chemistry', 'Classics',
            'Cognitive Science - Interdisciplinary', 'Computer Science',
            'Computer Science - Interdisciplinary', 'Creative Writing',
            'Data Science', 'Drama', 'East Asian Studies - Interdisciplinary',
            'Echols Scholar - Interdisciplinary', 'Economics', 'Education - Administration & Supervision',
            'Education - Athletic Training', 'Education - Clinical & School Psychology',
            'Education - Counselor Education',
            'Education - Curriculum & Instruction','Education - Early Childhood Development',
            'Education - Educational Policy (Policy Studies)', 'Education - Educational Psychology',
            'Education - Elementary Education', 'Education - English Education',
            'Education - Higher Education', 'Education - Kinesiology',
            'Education - Reading Education', 'Education - Research Statistics & Evaluation',
            'Education - Science Education', 'Education - Social Studies Education',
            'Education - Special Education',
            'Education - Speech Communication Disorders','Education - Youth & Social Innovation',
            'Engineering - Aerospace Engineering','Engineering - Biomedical Engineering',
            'Engineering - Chemical Engineering', 'Engineering - Civil Engineering',
            'Engineering - Computer Engineering', 'Engineering - Computer Science',
            'Engineering - Electrical Engineering','Engineering - Engineering Science',
            'Engineering - Materials Science & Engineering',
            'Engineering - Materials Science and Engineering',
            'Engineering - Mechanical & Aerospace Engineering',
            'Engineering - Mechanical Engineering',
            'Engineering - Systems Engineering', 'English', 'Environmental Sciences',
            'Environmental Thought & Practice - Interdisciplinary',
            'European Studies', 'Foreign Affairs', 'French',
            'Global Studies - Interdisciplinary', 'Government','Health Sciences Management (SCPS)', 
            'History','Human Biology - Interdisciplinary', 'Interdisciplinary (SCPS-BIS)',
            'Japanese Language & Literature - Interdisciplinary',
            'Latin American Studies', 'Linguistics', 'Mathematics', 'Media Studies',
            'Media Studies - Interdisciplinary', 'Microbiology',
            'Middle Eastern and South Asian Languages and Cultures', 'Music',
            'Neuroscience', 'Neuroscience - Interdisciplinary', 'Nursing',
            'Pharmacology', 'Philosophy', 'Physics','Political & Social Thought - Interdisciplinary',
            'Political Philosophy Policy & Law - Interdisciplinary', 'Psychology',
            'Public Health', 'Public Policy', 'Public Safety', 'Quantative Analytics in Education & Social Science',
            'Religious Studies', 'Slavic Languages and Literatures', 'Sociology',
            'Spanish', 'Statistics', 'Urban Development',
            'Women Gender & Sexuality - Interdisciplinary'
            ],
            [ 'Engineering - Aerospace Engineering',
            'Engineering - Biomedical Engineering',
            'Data Science'])
        sort_option, ascending, chart_option = get_parameters(agg_stats)

        #Filtered Data Frame
        result = agg_stats[(agg_stats['Total Students']>=0) & agg_stats.index.isin(majors)].sort_values(by=sort_option, ascending=ascending) # Show Highest First

        # Save by count and percent df's
        if chart_option == 'Counts':
            plot_df = result.iloc[:, 0:4]
        else:
            plot_df = result.iloc[:, 4:-1] # Percents

        plot_chart(plot_df, result, chart_option)