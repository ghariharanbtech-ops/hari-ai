import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Hari AI", layout="centered")

st.title("🧠 Hari AI")
st.write("Your upgraded personal AI assistant")

# -------- CONFIG --------
GROQ_API_KEY = "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"

# -------- CHAT --------
st.subheader("💬 Chat")

q = st.text_area("Ask anything")

if st.button("Send"):
    if q:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": q}]
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()["choices"][0]["message"]["content"]
            st.success(result)
        except:
            st.error("AI error. Check API key.")

# -------- NOTES --------
st.subheader("🧾 Notes")

note = st.text_input("Write a note")

if st.button("Save Note"):
    st.session_state.setdefault("notes", []).append(note)
    st.success("Saved!")

if "notes" in st.session_state:
    for n in st.session_state.notes:
        st.write("•", n)

# -------- TASKS --------
st.subheader("📅 Daily Planner")

task = st.text_input("Add task")

if st.button("Add Task"):
    st.session_state.setdefault("tasks", []).append(task)
    st.success("Added!")

if "tasks" in st.session_state:
    for t in st.session_state.tasks:
        st.write("✔", t)

# -------- EXPORT --------
st.subheader("📊 Export Data")

if st.button("Export to CSV"):
    notes = st.session_state.get("notes", [])
    tasks = st.session_state.get("tasks", [])

    df = pd.DataFrame({
        "Notes": notes + [""]*(len(tasks)-len(notes)),
        "Tasks": tasks + [""]*(len(notes)-len(tasks))
    })

    csv = df.to_csv(index=False)
    st.download_button("Download", csv, "hari_ai_data.csv")
