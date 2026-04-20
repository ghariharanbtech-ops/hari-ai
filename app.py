import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Hari AI", layout="centered")

st.title("🧠 Hari AI")
st.write("Your personal AI assistant")

q = st.text_area("Ask anything")

if st.button("Send"):
    if q:
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
        headers = {"Authorization": "Bearer YOUR_REAL_TOKEN"}
        response = requests.post(API_URL, headers=headers, json={"inputs": q})
        try:
            st.write(response.json()[0]["generated_text"])
        except:
            st.write("AI busy, try again")

note = st.text_input("Write note")
if st.button("Save Note"):
    st.session_state.setdefault("notes", []).append(note)

task = st.text_input("Add task")
if st.button("Add Task"):
    st.session_state.setdefault("tasks", []).append(task)

if st.button("Export"):
    df = pd.DataFrame({
        "Notes": st.session_state.get("notes", []),
        "Tasks": st.session_state.get("tasks", [])
    })
    st.download_button("Download CSV", df.to_csv(), "hari_ai.csv")
