GridWatch — SCADA Substation Monitoring & Cybersecurity Platform

Project Overview
GridWatch is a Python-based SCADA-inspired substation monitoring platform designed to simulate electrical equipment, collect and analyze telemetry, detect abnormal operating conditions, manage alarms, and provide operators with a centralized view of substation health.
Future development will extend GridWatch into the cybersecurity side of industrial control systems (ICS/SCADA), including security-event monitoring, anomalous activity detection, and correlation between cybersecurity events and equipment conditions.

Features:
Equipment Simulation
Telemetry Monitoring
Equipment Health Analysis
Alarm Management
Operator Dashboard
Event History
Database



Installation:
Requirements
Python 3.x
Git
SQLite

Clone the Repository
git clone <repository-url>
cd Nisource_project
Create a Virtual Environment
For Windows:
python -m venv venv

Activate the environment:
venv\Scripts\activate

Install Dependencies

If the project has no external dependencies:

# No external packages currently required

If dependencies are added later, they should be installed with:

pip install -r requirements.txt

Usage
Start the monitoring system with:

python main.py

The system continuously runs monitoring cycles.

Each cycle:

Updates simulated equipment.
Collects equipment telemetry.
Stores telemetry in the database.
Analyzes equipment health.
Evaluates alarm conditions.
Records important events.
Updates the operator dashboard.
Waits before beginning the next monitoring cycle.

Example equipment output:

TX-101 | Mode: NORMAL | Cycles: 1
TX-102 | Mode: OVERLOAD | Cycles: 1
TX-103 | Mode: NORMAL | Cycles: 1

Example alarm lifecycle:

NEW ALARM: TX-102

TX-102 | CRITICAL | Temperature dangerously high

TX-102 entering RECOVERY mode

ALARM CLEARED: TX-102

TX-102 returning to NORMAL mode

Future Improvements:
Data & Monitoring(
Historical telemetry visualization
Long-term equipment trends
Rate-of-change analysis
More realistic electrical equipment models
External/live telemetry sources
Configurable monitoring intervals)

Predictive Maintenance(
Equipment degradation modeling
Failure prediction
Statistical anomaly detection
Predictive maintenance indicators
Machine-learning-based equipment health analysis)

Cybersecurity(
SCADA/ICS security monitoring
Authentication and access monitoring
Suspicious activity detection
Unauthorized configuration-change detection
Network/security event simulation
Security alert management
Operational and cybersecurity event correlation)


