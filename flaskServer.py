from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS  # Import CORS
from datetime import datetime, timezone
import google.generativeai as genai
from dotenv import load_dotenv
import os
from google.cloud import firestore

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*") 

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("secret key.json")

@app.route("/")
def index():
    return "SocketIO server is running."

#generate summary given a report
#store this report in db and send to front end
@app.route('/CyberAttack', methods=['POST'])
def CyberAttack(snort_output):
    snort_output = """
    04/24-15:50:29.236253  [**] [1:498:6]  
    ATTACK-RESPONSES id check returned root [**] 
    [Classification: Potentially Bad Traffic] [Priority: 2]
    TCP 82.165.50.118:80 -> 69.143.202.28:39929
    """

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    system_prompt = """
    You are an advanced cybersecurity analysis system. Your task is to analyze log files from intrusion detection systems and generate user-friendly, informative descriptions of potential security incidents. Given a log entry, provide a comprehensive yet easy-to-understand explanation of the event.
    For each log entry, follow these steps:

    Parse the log entry to extract key information:

    Date and time of the event
    Snort rule ID and revision
    Attack name or type
    Classification
    Priority
    Source and destination IP addresses and ports


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
    Example input:
    04/24-15:50:29.236253  [**] [1:498:6] ATTACK-RESPONSES id check returned root [**] [Classification: Potentially Bad Traffic] [Priority: 2] TCP 82.165.50.118:80 -> 69.143.202.28:39929

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

    response = model.generate_content(
        contents=f"{system_prompt}\n\nAnalyze this log entry:\n{snort_output}"
    )
    # print(response.text)
    tim = datetime.now().astimezone(timezone.utc)
    
    msg = {'Info': response.text, 'Date': str(tim)[:-6]+'Z'}
    
    doc_ref = db.collection("Summaries").document()

    doc_ref.set(msg)
    
    socketio.emit('server_message', msg)

@app.route('/get_data', methods=['GET'])#get past summaries
def RetrievePastMessages():
    doc_ref = db.collection("Summaries")
    docInfo = []
    
    for doc in doc_ref.stream():
        docElement = doc.to_dict()
        docInfo.append(docElement)
    
    docInfo = sorted(docInfo, key = lambda x: x['Date'], reverse=True)
    return jsonify(docInfo)

@socketio.on('connect')
def handle_connect():
    # socketio.emit('send_message')
    print("Called")
    # CyberAttack("")

if __name__ == "__main__":
    socketio.run(app, host='localhost', port=5001)
    
