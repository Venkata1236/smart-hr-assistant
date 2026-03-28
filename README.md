# 🤝 Smart HR Assistant

> RAG + Agent Hybrid — retrieves HR policies OR takes actions based on intent

![Python](https://img.shields.io/badge/Python-3.11-blue)
![LangChain](https://img.shields.io/badge/LangChain-Latest-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange)
![FAISS](https://img.shields.io/badge/FAISS-Vector_DB-purple)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)

---

## 📌 What Is This?

A Smart HR Assistant combining RAG retrieval with ReAct agent decision-making. The agent decides whether to search HR policies (RAG tool → FAISS) or take an action (book meeting, submit leave, claim expense). Built with LangChain, FAISS, and custom tools.

---

## 🗺️ Simple Flow
```
User asks question
        ↓
Agent THINKS — policy question or action needed?
        ↓
Policy question → RAG Tool → FAISS search → answer
Action needed  → Action Tool → book / submit / contact
        ↓
Final answer returned
```

---

## 📁 Project Structure
```
smart_hr_assistant/
├── app.py
├── streamlit_app.py
├── data/
│   └── hr_policies.txt
├── core/
│   ├── __init__.py
│   ├── vector_store.py
│   ├── rag_tool.py
│   ├── action_tools.py
│   └── agent.py
├── .env
├── requirements.txt
└── README.md
```

---

## 🧠 Key Concepts

| Concept | What It Does |
|---|---|
| **RAG + Agent Hybrid** | Agent decides when to retrieve vs when to act |
| **Custom Tools** | @tool decorator wraps functions for agent use |
| **ReAct Agent** | Thought → Action → Observation loop |
| **FAISS** | Vector store for HR policy search |
| **Tool Descriptions** | Agent reads descriptions to pick the right tool |

---

## ⚙️ Local Setup
```bash
git clone https://github.com/venkata1236/smart-hr-assistant.git
cd smart_hr_assistant
pip install -r requirements.txt
```

Add `.env`:
```
OPENAI_API_KEY=your_key_here
```

Add `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "your_key_here"
```

Run:
```bash
python -m streamlit run streamlit_app.py
python app.py
```

---

## 💬 Try These Queries
```
Policy:  "What is the annual leave policy?"
Policy:  "How many WFH days are allowed per week?"
Action:  "Book a meeting with HR about my salary"
Action:  "Apply for 2 days sick leave from tomorrow"
Action:  "Claim travel expense of 2500 rupees"
Mixed:   "What is the leave policy and apply for 3 days leave"
```

---

## 📦 Tech Stack

- **LangChain** — ReAct agent, custom tools, FAISS retriever
- **FAISS** — Vector store for HR policy search
- **OpenAI** — GPT-4o-mini + text-embedding-ada-002
- **Streamlit** — Chat UI with tool usage display

---

## 👤 Author

**Venkata Reddy Bommavaram**
- 📧 bommavaramvenkat2003@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/venkatareddy1203)
- 🐙 [GitHub](https://github.com/venkata1236)