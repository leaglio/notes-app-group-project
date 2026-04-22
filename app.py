import streamlit as st
from src.compliance import simulate_ppe_detection, evaluate_compliance

st.set_page_config(page_title="PPE Guard AI", layout="wide")

st.title("PPE Guard AI Dashboard")
st.write("AI-based PPE compliance monitoring system")

def process_frame():
    ppe = simulate_ppe_detection()
    compliance = evaluate_compliance(ppe)
    return {
        "ppe": ppe,
        "compliance": compliance
    }

if st.button("Run PPE Check"):
    result = process_frame()

    st.subheader("PPE Status")
    st.write(result["ppe"])

    if result["compliance"]["is_compliant"]:
        st.success("Worker is compliant")
    else:
        st.error(f"Violation detected. Missing: {result['compliance']['missing_items']}")