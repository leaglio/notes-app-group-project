import streamlit as st
import cv2
import tempfile
import time
from src.compliance import simulate_ppe_detection, evaluate_compliance
from src.logger import log_event
from src.detector import RealTimeDetector

st.set_page_config(
    page_title="PPE Guard AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# SAFE MODERN CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(circle at 50% 0%, #1a1a2e 0%, #050505 60%, #000000 100%);
    color: #e5e7eb;
}

section[data-testid="stSidebar"] {
    background: rgba(5, 5, 5, 0.85) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

.block-container {
    padding-top: 3rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

.main-title {
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
    letter-spacing: -0.04em;
}

.sub-title {
    color: #a1a1aa;
    font-size: 1.05rem;
    font-weight: 400;
    margin-bottom: 2rem;
    line-height: 1.6;
}

.tag {
    display: inline-block;
    padding: 6px 14px;
    margin-right: 10px;
    margin-bottom: 12px;
    border-radius: 6px;
    background: rgba(0, 242, 254, 0.08);
    border: 1px solid rgba(0, 242, 254, 0.2);
    color: #00f2fe;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.metric {
    background: rgba(15, 15, 20, 0.6);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.metric:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(0, 242, 254, 0.05);
}

.metric-label {
    color: #71717a;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}

.metric-value {
    color: #ffffff;
    font-size: 1.4rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}

.panel {
    background: rgba(12, 12, 16, 0.7);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.03);
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}

.panel-title {
    color: #ffffff;
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
    letter-spacing: -0.01em;
}

.panel-sub {
    color: #71717a;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}

.result-box {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 16px;
}

.status-ok {
    color: #10b981;
    text-shadow: 0 0 15px rgba(16, 185, 129, 0.4);
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}

.status-bad {
    color: #ef4444;
    text-shadow: 0 0 15px rgba(239, 68, 68, 0.4);
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}

.ppe-item {
    background: rgba(0, 0, 0, 0.2);
    border-left: 2px solid rgba(255,255,255,0.1);
    padding: 12px 16px;
    margin-bottom: 8px;
    font-size: 0.9rem;
    display: flex;
    justify-content: space-between;
}

.good-box {
    background: linear-gradient(90deg, rgba(16,185,129,0.1) 0%, rgba(16,185,129,0.02) 100%);
    border-left: 3px solid #10b981;
    color: #a7f3d0;
    padding: 16px;
    border-radius: 4px;
    font-weight: 500;
    font-size: 0.95rem;
}

.bad-box {
    background: linear-gradient(90deg, rgba(239,68,68,0.1) 0%, rgba(239,68,68,0.02) 100%);
    border-left: 3px solid #ef4444;
    color: #fca5a5;
    padding: 16px;
    border-radius: 4px;
    font-weight: 500;
    font-size: 0.95rem;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    padding: 1rem 1rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    border: none;
    background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
    color: #000 !important;
    box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 242, 254, 0.5);
    color: #000 !important;
    border: none;
}

.stDownloadButton > button {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    color: white !important;
    box-shadow: none;
}
.stDownloadButton > button:hover {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    color: white !important;
}
</style>

""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## Control Center")

    source = st.selectbox(
        "Choose Input Source",
        ["CCTV (IP Camera)", "Webcam Laptop", "Upload Video", "Simulation"]
    )

    ip_url = ""
    uploaded_video = None

    if source == "CCTV (IP Camera)":
        ip_url = st.text_input(
            "Enter IP Camera URL",
            value="http://10.5.227.140:8081/video"
        )
        st.caption("Gunakan URL stream yang sama seperti yang berhasil dibuka di browser.")

    if source == "Upload Video":
        uploaded_video = st.file_uploader(
            "Upload CCTV Footage",
            type=["mp4", "avi", "mov"]
        )

# =========================
# HEADER
# =========================
st.markdown('<div class="main-title">PPE Guard AI Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Modern workplace safety monitoring interface for PPE compliance validation using camera input and intelligent evaluation logic.</div>',
    unsafe_allow_html=True
)

st.markdown("""
<span class="tag">Computer Vision</span>
<span class="tag">CCTV Integration</span>
<span class="tag">Monitoring Dashboard</span>
<span class="tag">Safety Compliance</span>
<span class="tag">Competition MVP</span>
""", unsafe_allow_html=True)

# =========================
# HELPERS
# =========================
def process_detection():
    ppe = simulate_ppe_detection()
    compliance = evaluate_compliance(ppe)
    confidence = round((sum(ppe.values()) / len(ppe)) * 100, 1)
    status = "COMPLIANT" if compliance["is_compliant"] else "VIOLATION"

    log_event(status, compliance["missing_items"], confidence)

    return {
        "ppe": ppe,
        "compliance": compliance,
        "confidence": confidence,
        "status": status
    }

def capture_from_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return None
    return frame

def capture_from_video_file(uploaded_file):
    if uploaded_file is None:
        return None

    temp_video = tempfile.NamedTemporaryFile(delete=False)
    temp_video.write(uploaded_file.read())
    temp_video.flush()

    cap = cv2.VideoCapture(temp_video.name)
    if not cap.isOpened():
        return None

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return None
    return frame

def capture_from_ip_camera(url):
    if not url.strip():
        return None

    cap = cv2.VideoCapture(url)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not cap.isOpened():
        cap.release()
        return None

    frame = None

    # warm up beberapa frame biar lebih stabil
    for _ in range(5):
        ret, temp = cap.read()
        if ret and temp is not None:
            frame = temp
        time.sleep(0.05)

    cap.release()
    return frame

# =========================
# METRICS
# =========================
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown("""
    <div class="metric">
        <div class="metric-label">System Mode</div>
        <div class="metric-value">LIVE</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric">
        <div class="metric-label">Input Source</div>
        <div class="metric-value" style="font-size:1rem;">{source}</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="metric">
        <div class="metric-label">Detection Engine</div>
        <div class="metric-value">AI CV</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown("""
    <div class="metric">
        <div class="metric-label">Alert Status</div>
        <div class="metric-value" style="color:#f87171;">ARMED</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# =========================
# BUTTONS
# =========================
col_btn1, col_btn2 = st.columns(2)
start_stream = col_btn1.button("Start AI Monitoring")
report_clicked = col_btn2.button("Prepare Report")

st.write("")

# =========================
# MAIN LOGIC
# =========================
if start_stream:
    st.info("Starting real-time AI Monitoring in a separate window. Press 'q' in the window to stop.")
    
    detector = RealTimeDetector("yolov8n.pt")
    
    cap = None
    if source == "Simulation" or source == "Webcam Laptop":
        cap = cv2.VideoCapture(0)
    elif source == "CCTV (IP Camera)":
        cap = cv2.VideoCapture(ip_url)
    elif source == "Upload Video" and uploaded_video is not None:
        temp_video = tempfile.NamedTemporaryFile(delete=False)
        temp_video.write(uploaded_video.read())
        temp_video.flush()
        cap = cv2.VideoCapture(temp_video.name)
        
    if cap is None or not cap.isOpened():
        st.error("Failed to open video source.")
        st.stop()
        
    window_name = "PPE Guard AI - Live Monitor"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    latest_result = None
    last_frame = None
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            processed_frame, results = detector.process_frame(frame)
            
            if results:
                latest_result = results[0]
                
            last_frame = processed_frame
            
            cv2.imshow(window_name, processed_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        
    if last_frame is not None:
        st.session_state["latest_frame"] = last_frame
        
    if latest_result is not None:
        st.session_state["latest_result"] = latest_result
        st.rerun()

# =========================
# PANELS
# =========================
left_col, right_col = st.columns([1.25, 1])

with left_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Monitoring Feed</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-sub">Current captured frame from the selected monitoring source.</div>', unsafe_allow_html=True)

    if "latest_frame" in st.session_state:
        frame_rgb = cv2.cvtColor(st.session_state["latest_frame"], cv2.COLOR_BGR2RGB)
        st.image(frame_rgb, caption="Captured Frame", use_container_width=True)
    else:
        st.info("No frame captured yet. Click 'Analyze Current Frame' to start.")

    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Detection Result</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-sub">Current PPE evaluation output from the monitoring system.</div>', unsafe_allow_html=True)

    if "latest_result" in st.session_state:
        latest = st.session_state["latest_result"]

        status_class = "status-ok" if latest["status"] == "COMPLIANT" else "status-bad"

        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("**Current Evaluation**")
        st.markdown(f'<div class="{status_class}">{latest["status"]}</div>', unsafe_allow_html=True)
        st.markdown(f"**Confidence Score:** {latest['confidence']}%")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("**PPE Items**")
        for item, status in latest["ppe"].items():
            label = "Detected" if status else "Missing"
            color = "#4ade80" if status else "#f87171"
            st.markdown(
                f'<div class="ppe-item"><span style="font-weight:700; color:{color};">{label}</span> — {item.replace("_", " ").title()}</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

        if latest["compliance"]["is_compliant"]:
            st.markdown(
                '<div class="good-box">Worker is compliant with PPE requirements.</div>',
                unsafe_allow_html=True
            )
        else:
            missing = ", ".join(latest["compliance"]["missing_items"])
            st.markdown(
                f'<div class="bad-box">Violation detected. Missing PPE: {missing}</div>',
                unsafe_allow_html=True
            )
    else:
        st.info("No analysis result yet. Click 'Analyze Current Frame' to generate output.")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# REPORT
# =========================
if report_clicked and "latest_result" in st.session_state:
    latest = st.session_state["latest_result"]
    report_text = f"""
PPE GUARD AI REPORT
===================
Status: {latest["status"]}
Confidence: {latest["confidence"]}%
PPE Status: {latest["ppe"]}
Compliance: {latest["compliance"]}
"""
    st.download_button(
        label="Download Compliance Report",
        data=report_text,
        file_name="ppe_compliance_report.txt",
        mime="text/plain"
    )