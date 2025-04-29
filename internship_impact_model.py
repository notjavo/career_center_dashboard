import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
import pickle
from sklearn.inspection import permutation_importance
from sklearn.metrics import accuracy_score

def main():
    st.title("Internship Impact Modeling")
    st.write("""
    ### Predict Student Outcomes Based on Career Center Data
    This tool allows career counselors to predict various student outcomes based on internship 
    and career fair participation, helping to identify which factors most influence student success.
    """)
    
    # Load the dataset
    try:
        df = pd.read_csv('final_modeling_data.csv')
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return
    
    # Sidebar for prediction type selection
    prediction_type = st.sidebar.radio(
        "What would you like to predict?",
        ["Student Employment Status", "Continuing Education", "Still Looking Status"]
    )
    
    # Main content based on prediction type
    if prediction_type == "Student Employment Status":
        employment_prediction(df)
    elif prediction_type == "Continuing Education":
        education_prediction(df)
    else:
        still_looking_prediction(df)

def train_models(df):
    """Train all three models and return them as a dictionary"""
    models = {}
    
    # Model 1: Working Status
    X = df[['avg_unemployment', 'primary_major', 'fairs_above_avg', 'Internship_binary', 'apps_above_avg', 'ipp_flag', 'total_apps']]
    Y = df['Outcome_binary']
    X_encoded = pd.get_dummies(X, columns=['primary_major'])
    
    # No need to split as we're training on the full dataset for deployment
    rf_model_working = RandomForestClassifier(n_estimators=1000, random_state=42, class_weight='balanced')
    rf_model_working.fit(X_encoded, Y)
    models['working'] = rf_model_working
    
    # Model 2: Continuing Education
    X2 = df[['avg_unemployment', 'primary_major', 'fairs_above_avg', 'Internship_binary', 'apps_above_avg', 'ipp_flag']]
    Y2 = df['binary_cont_education']
    X_encoded2 = pd.get_dummies(X2, columns=['primary_major'])
    
    rf_model_education = RandomForestClassifier(n_estimators=1000, random_state=42, class_weight='balanced')
    rf_model_education.fit(X_encoded2, Y2)
    models['education'] = rf_model_education
    
    # Model 3: Still Looking
    X3 = df[['avg_unemployment', 'fairs_above_avg', 'Internship_binary', 'apps_above_avg', 'ipp_flag', 'primary_major']]
    Y3 = df['binary_still_looking']
    X_encoded3 = pd.get_dummies(X3, columns=['primary_major'])
    
    rf_model_still_looking = RandomForestClassifier(n_estimators=1000, random_state=42)
    rf_model_still_looking.fit(X_encoded3, Y3)
    models['still_looking'] = rf_model_still_looking
    
    return models, X_encoded, X_encoded2, X_encoded3

def employment_prediction(df):
    st.header("Predict Student Employment Status")
    
    models, X_encoded, _, _ = train_models(df)
    model = models['working']
    
    # Form for user input
    st.write("### Enter Student Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        unemployment_rate = st.slider("Average Unemployment Rate (%)", 
                                    min_value=float(df['avg_unemployment'].min()), 
                                    max_value=float(df['avg_unemployment'].max()), 
                                    value=float(df['avg_unemployment'].mean()))
        
        primary_major = st.selectbox("Primary Major", 
                                    options=sorted(df['primary_major'].unique()))
        
        internship = st.radio("Completed an Internship?", 
                            options=["Yes", "No"], 
                            index=0)
        internship_binary = 1 if internship == "Yes" else 0
    
    with col2:
        fairs_above_avg = st.radio("Career Fair Attendance Above Average?", 
                                  options=["Yes", "No"], 
                                  index=0)
        fairs_above_avg_binary = 1 if fairs_above_avg == "Yes" else 0
        
        apps_above_avg = st.radio("Applications Submitted Above Average?", 
                                 options=["Yes", "No"], 
                                 index=0)
        apps_above_avg_binary = 1 if apps_above_avg == "Yes" else 0
        
        ipp_flag = st.radio("Participated in IPP Program?", 
                           options=["Yes", "No"], 
                           index=0)
        ipp_flag_binary = 1 if ipp_flag == "Yes" else 0
        
        total_apps = st.number_input("Total Applications Submitted", 
                                   min_value=0, 
                                   max_value=200, 
                                   value=int(df['total_apps'].mean()))
    
    # Create feature array for prediction
    features = pd.DataFrame({
        'avg_unemployment': [unemployment_rate],
        'fairs_above_avg': [fairs_above_avg_binary],
        'Internship_binary': [internship_binary],
        'apps_above_avg': [apps_above_avg_binary],
        'ipp_flag': [ipp_flag_binary],
        'primary_major': [primary_major],
        'total_apps': [total_apps]
    })
    
    # One-hot encode the features
    feature_cols = X_encoded.columns
    features_encoded = pd.get_dummies(features, columns=['primary_major'])
    
    # Align the columns with the training data
    for col in feature_cols:
        if col not in features_encoded.columns:
            features_encoded[col] = 0
    
    features_aligned = features_encoded[feature_cols]
    
    # Make prediction
    if st.button("Predict Employment Status"):
        prediction = model.predict(features_aligned)[0]
        probability = model.predict_proba(features_aligned)[0][1]
        
        st.write("### Prediction Results")
        if prediction == 1:
            st.success(f"This student is likely to be EMPLOYED after graduation (Probability: {probability:.2f})")
        else:
            st.error(f"This student is likely to be UNEMPLOYED after graduation (Probability: {1-probability:.2f})")
        
        # Feature importance
        plot_feature_importance(model, feature_cols)

def education_prediction(df):
    st.header("Predict Continuing Education")
    
    models, _, X_encoded2, _ = train_models(df)
    model = models['education']
    
    # Form for user input
    st.write("### Enter Student Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        unemployment_rate = st.slider("Average Unemployment Rate (%)", 
                                    min_value=float(df['avg_unemployment'].min()), 
                                    max_value=float(df['avg_unemployment'].max()), 
                                    value=float(df['avg_unemployment'].mean()))
        
        primary_major = st.selectbox("Primary Major", 
                                    options=sorted(df['primary_major'].unique()))
        
        internship = st.radio("Completed an Internship?", 
                            options=["Yes", "No"], 
                            index=0)
        internship_binary = 1 if internship == "Yes" else 0
    
    with col2:
        fairs_above_avg = st.radio("Career Fair Attendance Above Average?", 
                                  options=["Yes", "No"], 
                                  index=0)
        fairs_above_avg_binary = 1 if fairs_above_avg == "Yes" else 0
        
        apps_above_avg = st.radio("Applications Submitted Above Average?", 
                                 options=["Yes", "No"], 
                                 index=0)
        apps_above_avg_binary = 1 if apps_above_avg == "Yes" else 0
        
        ipp_flag = st.radio("Participated in IPP Program?", 
                           options=["Yes", "No"], 
                           index=0)
        ipp_flag_binary = 1 if ipp_flag == "Yes" else 0
    
    # Create feature array for prediction
    features = pd.DataFrame({
        'avg_unemployment': [unemployment_rate],
        'fairs_above_avg': [fairs_above_avg_binary],
        'Internship_binary': [internship_binary],
        'apps_above_avg': [apps_above_avg_binary],
        'ipp_flag': [ipp_flag_binary],
        'primary_major': [primary_major]
    })
    
    # One-hot encode the features
    feature_cols = X_encoded2.columns
    features_encoded = pd.get_dummies(features, columns=['primary_major'])
    
    # Align the columns with the training data
    for col in feature_cols:
        if col not in features_encoded.columns:
            features_encoded[col] = 0
    
    features_aligned = features_encoded[feature_cols]
    
    # Make prediction
    if st.button("Predict Continuing Education"):
        prediction = model.predict(features_aligned)[0]
        probability = model.predict_proba(features_aligned)[0][1]
        
        st.write("### Prediction Results")
        if prediction == 1:
            st.success(f"This student is likely to CONTINUE EDUCATION (Probability: {probability:.2f})")
        else:
            st.error(f"This student is likely to NOT CONTINUE EDUCATION (Probability: {1-probability:.2f})")
        
        # Feature importance
        plot_feature_importance(model, feature_cols)

def still_looking_prediction(df):
    st.header("Predict If Student Is Still Looking")
    
    models, _, _, X_encoded3 = train_models(df)
    model = models['still_looking']
    
    # Form for user input
    st.write("### Enter Student Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        unemployment_rate = st.slider("Average Unemployment Rate (%)", 
                                    min_value=float(df['avg_unemployment'].min()), 
                                    max_value=float(df['avg_unemployment'].max()), 
                                    value=float(df['avg_unemployment'].mean()))
        
        primary_major = st.selectbox("Primary Major", 
                                    options=sorted(df['primary_major'].unique()))
        
        internship = st.radio("Completed an Internship?", 
                            options=["Yes", "No"], 
                            index=0)
        internship_binary = 1 if internship == "Yes" else 0
    
    with col2:
        fairs_above_avg = st.radio("Career Fair Attendance Above Average?", 
                                  options=["Yes", "No"], 
                                  index=0)
        fairs_above_avg_binary = 1 if fairs_above_avg == "Yes" else 0
        
        apps_above_avg = st.radio("Applications Submitted Above Average?", 
                                 options=["Yes", "No"], 
                                 index=0)
        apps_above_avg_binary = 1 if apps_above_avg == "Yes" else 0
        
        ipp_flag = st.radio("Participated in IPP Program?", 
                           options=["Yes", "No"], 
                           index=0)
        ipp_flag_binary = 1 if ipp_flag == "Yes" else 0
    
    # Create feature array for prediction
    features = pd.DataFrame({
        'avg_unemployment': [unemployment_rate],
        'fairs_above_avg': [fairs_above_avg_binary],
        'Internship_binary': [internship_binary],
        'apps_above_avg': [apps_above_avg_binary],
        'ipp_flag': [ipp_flag_binary],
        'primary_major': [primary_major]
    })
    
    # One-hot encode the features
    feature_cols = X_encoded3.columns
    features_encoded = pd.get_dummies(features, columns=['primary_major'])
    
    # Align the columns with the training data
    for col in feature_cols:
        if col not in features_encoded.columns:
            features_encoded[col] = 0
    
    features_aligned = features_encoded[feature_cols]
    
    # Make prediction
    if st.button("Predict Still Looking Status"):
        prediction = model.predict(features_aligned)[0]
        probability = model.predict_proba(features_aligned)[0][1]
        
        st.write("### Prediction Results")
        if prediction == 1:
            st.error(f"This student is likely to be STILL LOOKING for opportunities (Probability: {probability:.2f})")
        else:
            st.success(f"This student is likely to be SETTLED with their current status (Probability: {1-probability:.2f})")
        
        # Feature importance
        plot_feature_importance(model, feature_cols)

def plot_feature_importance(model, feature_names):
    """Plot feature importance for the model"""
    st.write("### Feature Importance")
    
    # Get feature importances
    importances = model.feature_importances_
    
    # Sort importances
    indices = np.argsort(importances)[-10:]  # Top 10 features
    
    # Simplify feature names for better display
    feature_names = [name.replace('primary_major_', '') for name in feature_names]
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(range(len(indices)), importances[indices], align='center')
    ax.set_yticks(range(len(indices)))
    ax.set_yticklabels([feature_names[i] for i in indices])
    ax.set_xlabel('Feature Importance')
    ax.set_title('Top 10 Important Features')
    
    st.pyplot(fig)
    
    st.write("""
    ### Interpretation Guide
    - **Higher feature importance** indicates that the feature has more influence on the prediction
    - For binary features like internship completion or program participation, a high importance means these factors significantly affect outcomes
    - For majors, importance indicates how strongly a specific major influences the predicted outcome
    """)

if __name__ == "__main__":
    main()

