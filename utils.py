
import os
from dotenv import load_dotenv
import pandas as pd
import requests
import plotly.express as px
import streamlit as st
load_dotenv()

API_KEY = os.getenv("API_KEY") or st.secrets("API_KEY") 
WML_URL = os.getenv("WML_URL") or st.secrets("WML_URL")
PROJECT_ID = os.getenv("PROJECT_ID") or st.secrets("PROJECT_ID")

def call_granite(prompt):
    token_url = "https://iam.cloud.ibm.com/identity/token"
    print("🔐 Getting access token...")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "apikey": API_KEY,
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
    }

    token_response = requests.post(token_url, headers=headers, data=data)
    if token_response.status_code != 200:
        return "⚠️ Error fetching access token."

    access_token = token_response.json().get("access_token")
    print("✅ Access token received")
    print("🚀 Sending prompt to Granite model...")

    model_id = "ibm/granite-13b-instruct-v2"
    inference_url = f"{WML_URL}/ml/v1/text/generation?version=2024-05-01"

    payload = {
        "model_id": model_id,
        "input": prompt,
       
        "parameters": {
            "decoding_method": "greedy",   
            "temperature": 0.7,              
            "top_k": 50,                     
            "top_p": 0.95,              
            "max_new_tokens": 500         
        },
        "project_id": PROJECT_ID  
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(inference_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['results'][0]['generated_text']
    else:
        return f"❌ API Error: {response.status_code} - {response.text}"

def get_chat_response(user_query):
    """Generate empathetic medical response."""
    prompt = f"""
    You are HealthAI, an empathetic healthcare assistant. Provide a clear, kind response to the user's question. Suggest consulting a doctor if needed.

    User: {user_query}
    Response:
    """
    return call_granite(prompt)

def predict_disease(symptoms):
    """Predict conditions from symptoms."""
    prompt = f"""
    You are HealthAI, a diagnostic assistant. Based on symptoms, list possible conditions with likelihood and next steps. Suggest consulting a doctor.

    Symptoms: {symptoms}
    Output format:
    - Condition: [Name] | Likelihood: [Percentage]% | Next Steps: [Actions]
    """
    return call_granite(prompt)

def generate_treatment_plan(condition):
    """Generate a treatment plan."""
    prompt = f"""
    Suggest a treatment plan for the disease: {condition}
    """
    return call_granite(prompt)

def load_sample_data():
    uploaded_file = st.file_uploader("Upload your health data (CSV or Excel)", type=['csv', 'xlsx'])

    if uploaded_file is not None:
       try:
          if uploaded_file.name.endswith('.csv'): 
            df = pd.read_csv(uploaded_file)
          else:
            df = pd.read_excel(uploaded_file)

          st.success("File uploaded successfully!")

       
          st.subheader("📊 Raw Data")
          st.dataframe(df)

  
          st.subheader("📈 Data Summary")
          st.write(df.describe())

       except Exception as e:
        st.error(f"Error reading file: {e}")
    return df

def create_health_plots(data):
  
    
    
   
    if "Date" not in data.columns:
        data = data.copy()
        data["Date"] = pd.date_range(start="2024-01-01", periods=len(data), freq='D')

    fig1 = px.line(data, x="Date", y="HeartRate", title="Heart Rate Trend")
    fig2 = px.line(data, x="Date", y=["SystolicBP", "DiastolicBP"], title="Blood Pressure Trend")
    fig3 = px.line(data, x="Date", y="BloodGlucose", title="Blood Glucose Trend")

 
    fig4=px.pie(data, names="Symptom", title="Symptom Frequency")
    if fig4 is not None:
     fig4=px.pie(data, names="Symptom", title="Symptom Frequency")
    else:
     st.info("🟡 'Symptom' column not found. Pie chart not displayed.")


    return fig1, fig2, fig3, fig4


def generate_health_insights(data):
    """Generate AI insights from health trends."""
    summary = data.describe().to_string()
    prompt = f"""
    You are HealthAI, a health analyst. Analyze the patient’s health metrics (summary below) and provide insights on trends and recommendations.

    Data Summary:
    {summary}
    Insights:
    """
    return call_granite(prompt)
