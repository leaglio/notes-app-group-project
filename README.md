# K3 Guardian - PPE Compliance Monitoring System

Sistem monitoring Keselamatan dan Kesehatan Kerja (K3) berbasis AI untuk mendeteksi penggunaan alat pelindung diri (APD) secara real-time.

---

## 🛡️ Scrum Project Management

### 1. Team Roles
*   **Product Owner**: Jafar Sodik
*   **Scrum Master**: Antigravity AI
*   **Developer Team**: Jafar Sodik & AI Assistant

### 2. Product Backlogs
| ID | User Story / Task | Goal | Priority | Status |
|----|-------------------|------|----------|--------|
| PB01 | Real-time Webcam Integration | Membuka akses kamera via browser | High | ✅ Done |
| PB02 | Roboflow AI Core Integration | Menghubungkan API AI ke backend | High | ✅ Done |
| PB03 | SQLite Database System | Menyimpan log pelanggaran secara lokal | High | ✅ Done |
| PB04 | Real-time Toast Notifications | Memberi alert popup saat ada pelanggaran | Medium | ✅ Done |
| PB05 | Multi-class Detection (Helm, Mask, Vest) | Deteksi 3 jenis APD sekaligus | High | 🏃 In Progress |
| PB06 | Export Report to Excel/PDF | Download riwayat pelanggaran harian | Medium | 📋 Backlog |
| PB07 | User Authentication System | Login khusus petugas safety | Low | 📋 Backlog |
| PB08 | Dashboard Analytics Visualization | Grafik tren kepatuhan APD per minggu | Medium | 📋 Backlog |

### 3. Backlog Priority Decisions
*   **Prioritas Utama (High)**: Fokus pada fungsionalitas inti yaitu deteksi AI dan konektivitas kamera. Tanpa ini, sistem tidak bisa mendeteksi pelanggaran.
*   **Prioritas Menengah (Medium)**: Fokus pada UX dan pelaporan data (Notifikasi & Export).
*   **Prioritas Rendah (Low)**: Fitur tambahan seperti keamanan login dan skalabilitas multi-kamera.

### 4. Daily Sprint (Weekly Progress)
*   **Senin**: Research model AI di Roboflow & Setup environment Python.
*   **Selasa**: Pembuatan Backend FastAPI & Integrasi Database SQLite.
*   **Rabu**: Pengembangan Frontend Dashboard & Perbaikan bug kamera (Blob error).
*   **Kamis**: Implementasi sistem Alert real-time.

### 5. Weekly Sprint Session
*   **Sprint 1**: Fokus pada "Zero to MVP" (Minimum Viable Product). Menghasilkan dashboard yang bisa mendeteksi helm via webcam. (STATUS: Selesai)
*   **Sprint 2**: Fokus pada "Feature Expansion". Menambahkan deteksi masker, rompi, dan fitur export data. (STATUS: On-going)

---

## 🚀 How to Run
1. `pip install -r backend/requirements.txt`
2. `python backend/seed_db.py` (untuk data awal)
3. `python backend/app.py`
4. Buka `frontend/index.html` di browser.
