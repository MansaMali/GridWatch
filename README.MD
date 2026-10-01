GridWatch — SCADA Substation Monitoring & Cybersecurity Platform
Overview

GridWatch is a Python-based SCADA-inspired monitoring platform designed to simulate electrical substation operations and equipment monitoring. The project models critical substation assets, collects telemetry, analyzes equipment health, manages alarms, and provides operators with a centralized view of system conditions.

The project was developed to combine software engineering, industrial control systems (ICS/SCADA), and cybersecurity concepts while providing hands-on experience with technologies used in critical infrastructure environments.


Key Features
Equipment Simulation

Simulates electrical substation equipment, including:

Power Transformers
Circuit Breakers
Capacitor Banks
Telemetry Collection

Collects and processes operational data such as:

Voltage
Current
Temperature
Equipment Load
Equipment Status
Reactive Power
Equipment Health Analysis

Evaluates equipment conditions using:

Operating thresholds
Trend analysis
Status classification
Abnormal-condition detection
Alarm Management

Provides automated alarm functionality:

New alarm generation
Active alarm tracking
Alarm-clearing notifications
Equipment recovery monitoring
Operator Dashboard

Provides a centralized operational view of:

Equipment conditions
Health status
Active alarms
System-wide monitoring information
Data Storage

Uses SQLite to store:

Telemetry records
Equipment events
Historical operating data
Technologies Used
Python
SQLite
Git
GitLab
Visual Studio Code
System Workflow

GridWatch continuously performs monitoring cycles:

Update simulated equipment conditions
Collect equipment telemetry
Store telemetry in the database
Analyze equipment health
Evaluate alarm conditions
Record significant events
Update the operator dashboard
Begin the next monitoring cycle
Example Alarm Lifecycle
NEW ALARM: TX-102

TX-102 | CRITICAL | Temperature dangerously high

TX-102 entering RECOVERY mode

ALARM CLEARED: TX-102

TX-102 returning to NORMAL mode
Installation
Requirements
Python 3.x
Git
SQLite
Clone Repository
git clone <repository-url>
cd Nisource_project
Create Virtual Environment

Windows:

python -m venv venv
venv\Scripts\activate
Install Dependencies

Currently, no external packages are required.

If future dependencies are added:

pip install -r requirements.txt
Running GridWatch

Start the monitoring platform:

python main.py

GridWatch will begin executing continuous monitoring cycles, collecting telemetry, evaluating equipment health, managing alarms, and updating the operator dashboard.

Future Development
Advanced Monitoring & Analytics
Historical telemetry visualization
Long-term equipment trending
Rate-of-change analysis
More realistic equipment models
External/live telemetry integration
Configurable monitoring intervals
Predictive Maintenance
Equipment degradation modeling
Failure prediction
Statistical anomaly detection
Predictive maintenance indicators
Machine-learning-assisted health analysis
Cybersecurity & ICS Security Monitoring
Authentication and access control
Security event monitoring
Suspicious activity detection
Unauthorized configuration-change detection
Security alert management
Cybersecurity event correlation
Operational and security-event visibility
Project Goals

GridWatch is intended to demonstrate the intersection of:

Software Engineering
SCADA & Industrial Control Systems
Cybersecurity
Critical Infrastructure Technology
Data Analysis & Monitoring

The long-term vision is to evolve GridWatch into a platform capable of simulating both operational technology (OT) monitoring and cybersecurity monitoring within a modern utility environment.
