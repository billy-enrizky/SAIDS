# SAIDS - Smart Alert Intrusion Detection System

## Inspiration
Traditional incident reports often require significant time to analyze, leaving room for critical malicious activities to go unnoticed in real-time. Users without technical expertise are especially vulnerable, as they may not understand complex attack terminology or recognize security threats. We sought to solve these challenges by creating an enhanced Intrusion Detection System (IDS) that leverages advanced AI to provide clearer, more actionable insights.

## What It Does
SAIDS is an enhanced Intrusion Detection System (IDS) that monitors network traffic in real-time, recognizes malicious traffic, and alerts users about potential threats through an intuitive web interface. The alerts are analyzed by a Large Language Model (LLM), providing users with detailed insights and an overall understanding of the incident.

### Key Features:
- **Real-Time Alerts**: Users are notified immediately about malicious activities, allowing them to take swift action to mitigate potential risks.
- **Attack History Dashboard**: All alerts are stored in a dashboard, enabling users to review previous incidents and track patterns or trends over time.
- **Enhanced Incident Response**: Unlike traditional IDS, SAIDS utilizes AI to detect anomalies and generate helpful summaries for security analysts, streamlining the incident response process.
- **User-Friendly Experience**: Non-technical users can easily understand and respond to threats through a clean and intuitive interface.

## How We Built It
- **Front-End**: Developed using TypeScript and React to ensure a smooth and user-friendly experience.
- **Back-End**: Powered by Flask and integrated with the Gemini Large Language Model (LLM) for real-time threat analysis.
- **Intrusion Detection**: Snort was used as the IDS to monitor network traffic. We utilized pre-made .PCAP files to simulate network traffic during a Denial-of-Service (DOS) attack.
- **Web Sockets**: Implemented using `socket.io` for real-time communication between the IDS and the web interface.
- **Hosting**: Firebase was used for cloud hosting and managing real-time data updates.

## Built With
- **Firebase**: For cloud hosting and real-time database.
- **Flask**: Backend framework for handling API requests.
- **Gemini LLM**: To process alerts and provide in-depth analysis.
- **React**: For building the user interface.
- **Snort**: For real-time network traffic monitoring and intrusion detection.
- **Socket.io**: For real-time communication between the front-end and back-end.
- **TypeScript**: For building scalable and maintainable front-end code.

## Benefits
- **Real-Time Alerts**: Instant notifications about potential threats, ensuring timely actions.
- **Attack History Dashboard**: Easy access to historical data for better incident tracking and analysis.
- **Improved Response Process**: AI-driven insights assist security analysts in interpreting and responding to threats faster.
- **Non-Technical User-Friendly**: Simplified threat descriptions make it easy for anyone to understand and act on alerts.

