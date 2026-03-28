import streamlit as st
import os
from dotenv import load_dotenv
from core.agent import run_hr_agent
from core.vector_store import load_vector_store, build_vector_store

load_dotenv()

st.set_page_config(
    page_title="Smart HR Assistant",
    page_icon="🤝",
    layout="centered"
)

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vector_store_ready" not in st.session_state:
    st.session_state.vector_store_ready = False


# ─────────────────────────────────────────
# LOAD VECTOR STORE ONCE
# ─────────────────────────────────────────
if not st.session_state.vector_store_ready:
    with st.spinner("📚 Loading HR knowledge base..."):
        try:
            load_vector_store()
            st.session_state.vector_store_ready = True
        except Exception as e:
            st.error(f"❌ Failed to load knowledge base: {str(e)}")


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.title("🤝 Smart HR Assistant")
    st.markdown("---")

    st.markdown("### 🛠️ Tools Available")
    st.markdown("🔍 **RAG Tool** — Search HR Policies")
    st.markdown("📅 **Book Meeting** — Schedule with HR")
    st.markdown("📝 **Leave Request** — Apply for leave")
    st.markdown("💰 **Expense Claim** — Submit expenses")
    st.markdown("📨 **Contact HR** — Send message to HR")

    st.markdown("---")
    st.markdown("### 💡 Try Asking")
    st.caption("What is the leave policy?")
    st.caption("Book a meeting with HR about salary")
    st.caption("Apply for 3 days leave next week")
    st.caption("How many WFH days are allowed?")
    st.caption("Claim travel expense of 2500 rupees")

    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    if st.button("🔄 Rebuild Knowledge Base", use_container_width=True):
        with st.spinner("Rebuilding FAISS index..."):
            build_vector_store()
        st.success("✅ Knowledge base rebuilt!")

    st.markdown("---")
    st.caption(
        "RAG + Agent Hybrid. Agent decides whether "
        "to retrieve policy info or take an action."
    )


# ─────────────────────────────────────────
# MAIN — HEADER
# ─────────────────────────────────────────
st.title("🤝 Smart HR Assistant")
st.caption(
    "Ask me about HR policies or request actions like "
    "booking meetings, submitting leaves, or claiming expenses."
)
st.markdown("---")


# ─────────────────────────────────────────
# EXAMPLE BUTTONS
# ─────────────────────────────────────────
if not st.session_state.chat_history:
    st.markdown("### 💡 Try these:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 What is the leave policy?", use_container_width=True):
            st.session_state.starter = "What is the annual leave policy?"
            st.rerun()
        if st.button("🏠 WFH policy?", use_container_width=True):
            st.session_state.starter = "What is the work from home policy?"
            st.rerun()
        if st.button("💰 Salary credit date?", use_container_width=True):
            st.session_state.starter = "When is the salary credited every month?"
            st.rerun()
    with col2:
        if st.button("📅 Book HR meeting", use_container_width=True):
            st.session_state.starter = "Book a meeting with HR about my appraisal"
            st.rerun()
        if st.button("📝 Apply for leave", use_container_width=True):
            st.session_state.starter = "Apply for 2 days sick leave from tomorrow"
            st.rerun()
        if st.button("💸 Claim expense", use_container_width=True):
            st.session_state.starter = "Claim travel expense of 1500 rupees for client visit"
            st.rerun()
    st.markdown("---")


# ─────────────────────────────────────────
# DISPLAY CHAT HISTORY
# ─────────────────────────────────────────
for message in st.session_state.chat_history:
    if message["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="🤝"):
            st.markdown(message["content"])
            if message.get("tools_used"):
                with st.expander("🔍 Tools used"):
                    for tool in message["tools_used"]:
                        st.caption(f"→ {tool}")


# ─────────────────────────────────────────
# HANDLE STARTER BUTTONS
# ─────────────────────────────────────────
if "starter" in st.session_state:
    query = st.session_state.pop("starter")

    with st.chat_message("user", avatar="👤"):
        st.markdown(query)

    with st.chat_message("assistant", avatar="🤝"):
        with st.spinner("🤔 Agent is thinking..."):
            result = run_hr_agent(query)

        st.markdown(result["output"])

        tools_used = []
        if result["steps"]:
            for step in result["steps"]:
                action = step[0]
                tools_used.append(f"{action.tool}: {str(action.tool_input)[:60]}...")
            with st.expander("🔍 Tools used"):
                for t in tools_used:
                    st.caption(f"→ {t}")

    st.session_state.chat_history.append({"role": "user", "content": query})
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": result["output"],
        "tools_used": tools_used
    })
    st.rerun()


# ─────────────────────────────────────────
# CHAT INPUT
# ─────────────────────────────────────────
user_input = st.chat_input("Ask about HR policies or request an action...")

if user_input:
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🤝"):
        with st.spinner("🤔 Agent is thinking..."):
            result = run_hr_agent(user_input)

        st.markdown(result["output"])

        tools_used = []
        if result["steps"]:
            for step in result["steps"]:
                action = step[0]
                tools_used.append(f"{action.tool}: {str(action.tool_input)[:60]}...")
            with st.expander("🔍 Tools used"):
                for t in tools_used:
                    st.caption(f"→ {t}")

    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": result["output"],
        "tools_used": tools_used
    })
    st.rerun()