import streamlit as st
from src.compliance import simulate_ppe_detection, evaluate_compliance

st.set_page_config(page_title="PPE Guard AI", layout="wide")

st.title("PPE Guard AI Dashboard")
st.caption("AI-based workplace safety monitoring system")

st.markdown("## Monitoring Panel")

def process_frame():
    ppe = simulate_ppe_detection()
    compliance = evaluate_compliance(ppe)
    return {
        "ppe": ppe,
        "compliance": compliance
    }

col1, col2 = st.columns(2)

with col1:
    st.info("Click the button below to simulate PPE compliance checking.")

    if st.button("Run PPE Check"):
        result = process_frame()
        st.session_state["result"] = result

with col2:
    st.markdown("### System Status")
    st.write("Input Source: Simulated Frame")
    st.write("Detection Mode: PPE Compliance Check")

if "result" in st.session_state:
    result = st.session_state["result"]

    st.markdown("## PPE Detection Result")

    for item, status in result["ppe"].items():
        if status:
            st.success(f"{item}: Detected")
        else:
            st.error(f"{item}: Not Detected")

    st.markdown("## Compliance Status")
    if result["compliance"]["is_compliant"]:
        st.success("Worker is compliant")
    else:
        st.error(f"Violation detected. Missing: {result['compliance']['missing_items']}")