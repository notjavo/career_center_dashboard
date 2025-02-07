import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


def user_input():
    majors_data = pd.read_csv('streamlit_data_anonymous.csv', low_memory=False)
    majors_data.majors_data.groupby('Primary Major')['Number of Internships_fds_2023'].value_counts().unstack(fill_value=0)

    # Combine the number of internship and major columns together 
    majors_data['Major'] = pd.concat([majors_data['Primary Major'], majors_data['Recipient Primary Majors_fds_2021'], majors_data['Recipient Primary Major_fds_2022'], majors_data['Q5.4_fds_2024']], ignore_index=True)
    majors_data['num_internships'] = pd.concat([majors_data['Number of Internships_fds_2023'], majors_data['Number of Internships'], majors_data['How many internships (summer and/or academic year) did you have while attending the University of Virginia?_fds_2021'], 
                                                majors_data['If you participated in internships, how many internships did you have while attending the University of Virginia?_fds_2022']], ignore_index=True)

    # Get by major Counts
    counts= majors_data.groupby('Major')['num_internships'].size().unstack(fill_value=0)
    counts1 = majors_data.groupby('Recipient Primary Majors_fds_2021')['How many internships (summer and/or academic year) did you have while attending the University of Virginia?_fds_2021'].size().unstack(fill_value=0)
    counts2 = majors_data.groupby('Recipient Primary Major_fds_2022')['If you participated in internships, how many internships did you have while attending the University of Virginia?_fds_2022'].size().unstack(fill_value=0)
    counts3 = majors_data.groupby('Primary Major')['Number of Internships_fds_2023'].size().unstack(fill_value=0)
    counts4 = majors_data.groupby('Q5.4_fds_2024')['Number of Internships'].value_counts().unstack(fill_value=0)
    st.write(counts1, counts2, counts3, counts4)

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
    # Streamlit user input
    analysis = st.sidebar.selectbox('How do you want to see By Major Internship Data?', ['By specific Major', 'Sorted by Best/Worst'],
                            key='user_input')

    if analysis == 'By specific Major':
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
            'Echols Scholar - Interdisciplinary', 'Economics',
            'Education - Administration & Supervision',
            'Education - Athletic Training',
            'Education - Clinical & School Psychology',
            'Education - Counselor Education',
            'Education - Curriculum & Instruction',
            'Education - Early Childhood Development',
            'Education - Educational Policy (Policy Studies)',
            'Education - Educational Psychology',
            'Education - Elementary Education', 'Education - English Education',
            'Education - Higher Education', 'Education - Kinesiology',
            'Education - Reading Education',
            'Education - Research Statistics & Evaluation',
            'Education - Science Education', 'Education - Social Studies Education',
            'Education - Special Education',
            'Education - Speech Communication Disorders',
            'Education - Youth & Social Innovation',
            'Engineering - Aerospace Engineering',
            'Engineering - Biomedical Engineering',
            'Engineering - Chemical Engineering', 'Engineering - Civil Engineering',
            'Engineering - Computer Engineering', 'Engineering - Computer Science',
            'Engineering - Electrical Engineering',
            'Engineering - Engineering Science',
            'Engineering - Materials Science & Engineering',
            'Engineering - Materials Science and Engineering',
            'Engineering - Mechanical & Aerospace Engineering',
            'Engineering - Mechanical Engineering',
            'Engineering - Systems Engineering', 'English',
            'Environmental Sciences',
            'Environmental Thought & Practice - Interdisciplinary',
            'European Studies', 'Foreign Affairs', 'French',
            'Global Studies - Interdisciplinary', 'Government',
            'Health Sciences Management (SCPS)', 'History',
            'Human Biology - Interdisciplinary', 'Interdisciplinary (SCPS-BIS)',
            'Japanese Language & Literature - Interdisciplinary',
            'Latin American Studies', 'Linguistics', 'Mathematics', 'Media Studies',
            'Media Studies - Interdisciplinary', 'Microbiology',
            'Middle Eastern and South Asian Languages and Cultures', 'Music',
            'Neuroscience', 'Neuroscience - Interdisciplinary', 'Nursing',
            'Pharmacology', 'Philosophy', 'Physics',
            'Political & Social Thought - Interdisciplinary',
            'Political Philosophy Policy & Law - Interdisciplinary', 'Psychology',
            'Public Health', 'Public Policy', 'Public Safety',
            'Quantative Analytics in Education & Social Science',
            'Religious Studies', 'Slavic Languages and Literatures', 'Sociology',
            'Spanish', 'Statistics', 'Urban Development',
            'Women Gender & Sexuality - Interdisciplinary'
            ],
            [ 'Engineering - Aerospace Engineering',
            'Engineering - Biomedical Engineering',
            'Data Science'])
        # Sort filtered columns
        sorting_column = '0 (%)' # column to filter by 
        result = result[(result['Total Students']>=4) & result.index.isin(majors)].sort_values(by=sorting_column, ascending=False) # Show Highest First
        result.round(1)


        # Save counts and percent df's
        result_percent=result.iloc[:, 5:]
        result = result.iloc[:, 1:5]

        # heatmap code
        plt.figure(figsize=(8,6))
        sns.heatmap(result_percent, annot=True, cmap="Blues", linewidths=0.5)

        plt.title("Internship Distribution Heatmap")
        plt.ylabel("Major")
        plt.xlabel("Num Internships")

        # Display the plot in Streamlit
        st.pyplot(plt)
        st.write(result)

    elif analysis == 'Sorted by Best/Worst':
        sorting = st.sidebar.selectbox('How do you want to sort', ['0 (%)', '3+ (%)'],
                               key='sorting')
        min_students = st.sidebar.slider("How many Students does Major need to have to show", 0, 100, 60)
        result = result[result['Total Students']>=min_students].sort_values(by=sorting, ascending=False) # Show Highest First
        result.round(1)


        # Save counts and percent df's
        result_percent=result.iloc[:, 5:]
        result = result.iloc[:, 1:5]

        # heatmap code
        plt.figure(figsize=(8,6))
        sns.heatmap(result_percent, annot=True, cmap="Blues", linewidths=0.5)

        plt.title("Internship Distribution Heatmap")
        plt.ylabel("Major")
        plt.xlabel("Num Internships")

        # Display the plot in Streamlit
        st.pyplot(plt)
        st.write(result)