"""
🤖 HR Agent - LangGraph ReAct Agent Factory (v1.0 2026)
======================================================
LLM: GPT-4o-mini | Framework: LangGraph prebuilt.
Tools: RAG + 4 action tools. Input via HumanMessage.
Secrets: Streamlit/CLI unified key resolution.
Author: Venkata Reddy (@Venkata1236)
"""



import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from core.rag_tool import create_rag_tool
from core.action_tools import (
    book_meeting_with_hr,
    submit_leave_request,
    submit_expense_claim,
    contact_hr_team
)
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    try:
        import streamlit as st
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return os.getenv("OPENAI_API_KEY")

def get_llm():
    return ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.3,
        openai_api_key=get_api_key()
    )

def create_hr_agent():
    llm = get_llm()
    rag_tool = create_rag_tool()
    tools = [
        rag_tool,
        book_meeting_with_hr,
        submit_leave_request,
        submit_expense_claim,
        contact_hr_team
    ]
    agent = create_react_agent(llm, tools)
    return agent

def run_hr_agent(query: str, chat_history: list = None) -> dict:
    agent = create_hr_agent()
    try:
        result = agent.invoke({
            "messages": [HumanMessage(content=query)]
        })
        output = result["messages"][-1].content
        return {
            "output": output,
            "steps": [],
            "error": None
        }
    except Exception as e:
        return {
            "output": f"I encountered an error: {str(e)}. Please try again.",
            "steps": [],
            "error": str(e)
        }