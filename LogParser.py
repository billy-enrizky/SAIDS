import time
import requests
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

#program that checks for updates in the log file of a snort application
#stores all reports into db and generates summaries for every new report by calling backend api
#clears log file after processing every report
if __name__ == "__main__":
    db = firestore.Client.from_service_account_json("secret key.json")
    logFileName = ""
    doc_ref = db.collection("Reports")
    while(True): #check for new reports every minute
        file = open(logFileName, 'r')
        line = file.readline()
        while line!="":
            if(len(doc_ref.where(filter=FieldFilter("value", "==", line)).stream())==0):#check if report exists in db
                db.collection("Reports").document().set({'value': line})#if not exist store in db and get summary
                requests.post(url = 'http://localhost:5001/CyberAttack', params={'attackString': line})
            line = file.readline()
            
        open('file.txt', 'w').close() #delete all reports in the log file
        time.sleep(60)
    