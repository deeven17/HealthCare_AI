import streamlit as st
import utils
from datetime import datetime


st.set_page_config(page_title="HealthAI", layout="wide")


st.sidebar.title("HealthAI Menu")
page = st.sidebar.selectbox("Select Feature", ["Patient Chat", "Disease Prediction", "Treatment Plans", "Health Analytics"])


st.sidebar.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M IST')}")


if page == "Patient Chat":
    st.title("HealthAI: Patient Chat")
    st.write("Ask any health-related question for personalized guidance!")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for msg in st.session_state.chat_history:
        with st.chat_message("user" if "user" in msg else "assistant"):
            st.write(msg["user"] if "user" in msg else msg["response"])
    user_input = st.chat_input("Type your question here...")
    if user_input:
        with st.chat_message("user"): st.write(user_input)
        with st.spinner("Generating response..."):
            try:
                response = utils.get_chat_response(user_input)
                with st.chat_message("assistant"): st.write(response)
            except Exception as e:
                st.error(f"Error: Could not get response. Please try again. ({str(e)})")
        st.session_state.chat_history.append({"user": user_input, "response": response if 'response' in locals() else "No response"})


elif page == "Disease Prediction":
    st.title("HealthAI: Disease Prediction")
    st.write("Enter your symptoms to receive a predictive analysis.")
    with st.form("symptoms_form"):
        symptoms = st.text_area("Symptoms (e.g., headache, fever):")
        submitted = st.form_submit_button("Predict")
        if submitted and symptoms:
            with st.spinner("Analyzing symptoms..."):
                try:
                    result = utils.predict_disease(symptoms)
                    st.write("### Possible Conditions")
                    st.write(result)
                except Exception as e:
                    st.error(f"Error: Could not predict. Please try again. ({str(e)})")
        elif submitted and not symptoms:
            st.warning("Please enter symptoms before predicting.")


elif page == "Treatment Plans":
    st.title("HealthAI: Treatment Plans")
    st.write("Enter a diagnosed condition to get a personalized plan.")
    with st.form("treatment_form"):
        condition = st.text_input("Condition (e.g., Hypertension):")
        submitted = st.form_submit_button("Generate Plan")
        if submitted and condition:
            with st.spinner("Generating plan..."):
                try:
                    plan = utils.generate_treatment_plan(condition)
                   
                    st.write(plan)
                except Exception as e:
                    st.error(f"Error: Could not generate plan. Please try again. ({str(e)})")
        elif submitted and not condition:
            st.warning("Please enter a condition before generating a plan.")

elif page == "Health Analytics":
    st.title("HealthAI: Health Analytics Dashboard")
    st.write("Visualize and analyze your health data trends.")
    with st.spinner("Loading data and charts..."):
        try:
            data = utils.load_sample_data()
            fig1, fig2, fig3, fig4 = utils.create_health_plots(data)
            st.plotly_chart(fig1, use_container_width=True)
            st.plotly_chart(fig2, use_container_width=True)
            st.plotly_chart(fig3, use_container_width=True)
            st.plotly_chart(fig4, use_container_width=True)
            summary = data.describe()
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Avg. Heart Rate", f"{summary['HeartRate']['mean']:.1f} bpm", f"±{summary['HeartRate']['std']:.1f}")
            col2.metric("Avg. Blood Pressure", f"{summary['SystolicBP']['mean']:.1f}/{summary['DiastolicBP']['mean']:.1f}", "+0.0")
            col3.metric("Avg. Blood Glucose", f"{summary['BloodGlucose']['mean']:.1f} mg/dL", f"±{summary['BloodGlucose']['std']:.1f}")
           
            col4.metric("Avg. Sleep", "6.8 hours", "↓0.5")
            insights = utils.generate_health_insights(data)
            st.write("### AI-Generated Health Insights")
            st.write(insights)
        except Exception as e:
            st.error(f"Error: Could not load analytics. Check data file. ({str(e)})")