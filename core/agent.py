import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent 
from langchain_core.prompts import PromptTemplate  
from langchain.agents import AgentExecutor         
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


AGENT_PROMPT = """You are a Smart HR Assistant for a company.
You help employees with HR-related queries and actions.

You have access to these tools:
{tools}

Use the following format STRICTLY:

Question: the input question you must answer
Thought: think about what to do — is this a policy question or an action request?
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Guidelines:
- For questions about policies, rules, entitlements → use search_hr_policies
- For booking meetings → use book_meeting_with_hr
- For leave applications → use submit_leave_request
- For expense claims → use submit_expense_claim
- For contacting HR → use contact_hr_team
- Always be helpful, professional, and empathetic
- If you cannot find the information, suggest contacting HR directly

Begin!

Question: {input}
Thought: {agent_scratchpad}"""


def create_hr_agent():
    """
    Creates a ReAct agent with RAG + action tools.
    """
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.3,
        openai_api_key=get_api_key()
    )

    # Load all tools
    rag_tool = create_rag_tool()
    tools = [
        rag_tool,
        book_meeting_with_hr,
        submit_leave_request,
        submit_expense_claim,
        contact_hr_team
    ]

    # Create prompt
    prompt = PromptTemplate(
        template=AGENT_PROMPT,
        input_variables=["input", "agent_scratchpad", "tools", "tool_names"]
    )

    # Create ReAct agent
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    # Wrap in executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True,
        return_intermediate_steps=True
    )

    return agent_executor


def run_hr_agent(query: str, chat_history: list = None) -> dict:
    """
    Runs the HR agent for a given query.
    Returns response and intermediate steps.
    """
    agent = create_hr_agent()

    try:
        result = agent.invoke({"input": query})
        return {
            "output": result.get("output", ""),
            "steps": result.get("intermediate_steps", []),
            "error": None
        }
    except Exception as e:
        return {
            "output": f"I encountered an error: {str(e)}. Please try again.",
            "steps": [],
            "error": str(e)
        }