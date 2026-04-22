const API_BASE = 'http://localhost:8000';
const video = document.getElementById('webcam');
const canvas = document.getElementById('detection-canvas');
const ctx = canvas.getContext('2d');
const startBtn = document.getElementById('start-btn');
const toastContainer = document.getElementById('toast-container');

let isRunning = false;

// 1. Start Webcam
async function initCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        
        // Wait for video metadata to load
        video.onloadedmetadata = () => {
            isRunning = true;
            startBtn.innerHTML = '<i class="fas fa-stop"></i> STOP MONITORING';
            startBtn.style.background = 'var(--accent-red)';
            processFrame();
        };
    } catch (err) {
        console.error("Error accessing webcam: ", err);
        alert("Cannot access camera. Please check permissions.");
    }
}

// 2. Main Detection Loop
async function processFrame() {
    if (!isRunning || video.videoWidth === 0) {
        if (isRunning) setTimeout(processFrame, 500);
        return;
    }

    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = video.videoWidth;
    tempCanvas.height = video.videoHeight;
    const tempCtx = tempCanvas.getContext('2d');
    tempCtx.drawImage(video, 0, 0);

    tempCanvas.toBlob(async (blob) => {
        if (!blob) {
            if (isRunning) setTimeout(processFrame, 1000);
            return;
        }

        const formData = new FormData();
        formData.append('file', blob, 'frame.jpg');

        try {
            const response = await fetch(`${API_BASE}/detect`, {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            
            if (result.status === 'success') {
                drawDetections(result.detections);
                
                if (result.violations && result.violations.length > 0) {
                    result.violations.forEach(v => showToast(v));
                }
                updateStats();
            }
        } catch (err) {
            console.error("Detection error:", err);
        }

        if (isRunning) setTimeout(processFrame, 1500);
    }, 'image/jpeg');
}

// 3. Draw Bounding Boxes
function drawDetections(detections) {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (!detections || detections.length === 0) return;

    detections.forEach(det => {
        const x = det.x - det.width / 2;
        const y = det.y - det.height / 2;
        const w = det.width;
        const h = det.height;

        ctx.strokeStyle = '#22c55e';
        ctx.lineWidth = 4;
        ctx.strokeRect(x, y, w, h);

        ctx.fillStyle = '#22c55e';
        ctx.font = 'bold 20px Outfit';
        ctx.fillText(`${det.class} (${Math.round(det.confidence * 100)}%)`, x, y > 30 ? y - 10 : y + 30);
    });
}

function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<i class="fas fa-exclamation-circle"></i> ALERT: ${message}`;
    toastContainer.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

async function updateStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();
        document.getElementById('active-workers').innerText = data.active_workers;
        document.getElementById('compliance-rate').innerText = `${data.compliance_rate}%`;
        document.getElementById('violation-count').innerText = data.total_violations;
        renderLogs(data.recent_logs);
    } catch (err) {}
}

function renderLogs(logs) {
    const logContainer = document.getElementById('violation-logs');
    if (!logs) return;
    logContainer.innerHTML = ''; 
    logs.forEach(log => {
        const logItem = document.createElement('div');
        logItem.className = `log-item ${log.status === 'Missing' ? 'warning' : 'info'}`;
        logItem.innerHTML = `
            <div class="log-time">${log.timestamp}</div>
            <div class="log-details">
                <p class="log-msg"><strong>${log.ppe_type} ${log.status}</strong></p>
                <p class="log-loc">Zone A - AI Active</p>
            </div>
        `;
        logContainer.appendChild(logItem);
    });
}

startBtn.addEventListener('click', () => {
    if (!isRunning) {
        initCamera();
    } else {
        isRunning = false;
        if (video.srcObject) {
            video.srcObject.getTracks().forEach(track => track.stop());
        }
        startBtn.innerHTML = '<i class="fas fa-play"></i> START MONITORING';
        startBtn.style.background = 'var(--accent-blue)';
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
});

document.addEventListener('DOMContentLoaded', updateStats);
