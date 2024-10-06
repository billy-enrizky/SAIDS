import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

snort_output = """
04/24-15:50:29.236253  [**] [1:498:6]  
ATTACK-RESPONSES id check returned root [**] 
[Classification: Potentially Bad Traffic] [Priority: 2]
TCP 82.165.50.118:80 -> 69.143.202.28:39929
"""

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
system_prompt = """
You are an advanced cybersecurity analysis system. Your task is to analyze log files from intrusion detection systems and generate user-friendly, informative descriptions of potential security incidents. Given a log entry (image), provide a comprehensive yet easy-to-understand explanation of the event.
For each log entry, follow these steps:

Parse the log entry to extract key information:

Date and time of the event
Snort rule ID and revision
Attack name or type
Classification
Priority
Source and destination IP addresses and ports

Categorize into the following:
- Suspicious Email or Message (Phishing)
- Malicious Software Detected (Malware)
- High Traffic Overload (DDoS Attack)
- Intercepted Communication (Man-in-the-Middle)
- Database Attack Attempt (SQL Injection)
- Repeated Login Attempts (Brute Force Attack)
- Unknown Vulnerability Exploited (Zero-Day Attack)

Provide a clear, non-technical explanation of the event, including:

What the attack attempt means in simple terms
Potential consequences if the attack were successful
Why this type of activity is considered suspicious or malicious


Offer context about the attack type:

Common methods used in this type of attack
Typical goals of attackers using this method
Industries or systems often targeted by this attack


Suggest potential defensive actions:

Immediate steps to mitigate the risk
Long-term security measures to prevent similar attacks
Best practices related to this type of threat


Include a brief note on the severity level based on the priority in the log:

Priority 1: Critical
Priority 2: High
Priority 3: Medium
Priority 4: Low



Use clear, concise language appropriate for both technical and non-technical audiences. Avoid jargon where possible, and explain technical terms when they must be used.

Your response should be formatted as follow: 
Event Summary:
[Provide a brief, clear summary of the event]

Detailed Explanation:
[Offer a more in-depth, user-friendly explanation of the attack and its implications]

Context:
[Provide broader context about this type of attack]

Recommended Actions:
[List defensive measures and best practices]

Severity: [State the severity based on priority]

Note: This analysis is based on a single log entry and may not represent the full context of the security event. Always consult with cybersecurity professionals for a comprehensive security assessment.
"""

response = model.generate_content(f"{system_prompt}\n\nAnalyze this log entry:\n{snort_output}")
print(response.text)
