import streamlit as st
from datetime import datetime, timezone
from google.cloud import firestore
                

st.set_page_config(
    page_title="US Population Dashboard",
    page_icon="🏂",
    layout="centered",
    initial_sidebar_state="expanded")

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("secret key.json")

st.title("CyberAttack Catcher")
st.text("A cybercatching software that helps non-tech savvy people understand cyber \nthreats to their server.")

st.divider()

with st.container(height=700):
    # Create a reference to the Google post.
    doc_ref = db.collection("Summaries")

    # Then get the data at that reference.
    
    docInfo = []
    
    for doc in doc_ref.stream():
        docElement = doc.to_dict()
        docInfo.append(docElement)
    
    docInfo = sorted(docInfo, key = lambda x: x['Date'], reverse=True)
    
    for i in docInfo:
        st.subheader(i['Date'].astimezone().strftime("%Y-%m-%d %H:%M:%S"))
        st.write("Summary:")
        st.write(i['Info'])
        st.divider()

