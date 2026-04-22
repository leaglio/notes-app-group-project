# Scrum Project Documentation - K3 PPE Monitoring

## 1. Team Roles
- **Product Owner**: Jafar (Responsible for defining features and business value)
- **Scrum Master**: Antigravity AI (Responsible for technical guidance and process)
- **Developers**: Jafar & Antigravity (Responsible for building the frontend, backend, and AI integration)

## 2. Product Backlogs
| ID | Title | Description | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| PB01 | Real-time Webcam Feed | Implement live camera stream in the dashboard | Feature | High | Done |
| PB02 | Roboflow AI Integration | Connect backend to YOLOv11 model for PPE detection | Feature | High | Done |
| PB03 | SQLite Database Setup | Create persistent storage for safety violation logs | Feature | High | Done |
| PB04 | Real-time Toast Alerts | Show popup notifications when violations are detected | Feature | Medium | Done |
| PB05 | Multi-class Detection | Support detection for Helmet, Vest, and Mask | Feature | High | Done |
| PB06 | Export Compliance Reports | Ability to download violation history as PDF/Excel | Feature | Medium | Backlog |
| PB07 | User Authentication | Secure login for safety officers to access dashboard | Security | Low | Backlog |
| PB08 | Multi-Camera Dashboard | Support monitoring from multiple CCTV sources | Feature | Low | Backlog |
| PB09 | Fix Blob Startup Bug | Resolve TypeError when camera is starting up | Bug | High | Done |

## 3. Priority Decisions
- **High Priority**: Core AI detection and real-time monitoring functionality. Without these, the system has no value.
- **Medium Priority**: User experience enhancements like Toast alerts and basic reporting.
- **Low Priority**: Security and advanced scaling (multi-camera), which are "nice-to-have" for the initial MVP.

## 4. Daily Sprint (Log)
- **Day 1**: Initial project setup, Backend FastAPI initialization.
- **Day 2**: Frontend UI Design (Glassmorphism) and Roboflow API integration.
- **Day 3**: Bug fixing (Webcam Blob error) and implementing real-time Alerts.

## 5. Weekly Sprint
- **Week 1 Focus**: Completing the functional MVP with live AI detection and local database logging. (Status: COMPLETED)
