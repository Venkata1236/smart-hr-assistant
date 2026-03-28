"""
🔍 RAG Tool - FAISS Semantic Search for HR Policies (v1.0 2026)
==============================================================
Wraps FAISS retriever as a LangChain @tool.
Uses .invoke() for LangChain 0.2+ compatibility.
Returns top-4 policy chunks for agent context.
Author: Venkata Reddy (@Venkata1236)
"""



from langchain.tools import tool
from core.vector_store import load_vector_store

def create_rag_tool():
    """
    Creates a RAG tool that searches HR policies in FAISS.
    Agent uses this for policy-related questions.
    """
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 4}
    )

    @tool
    def search_hr_policies(query: str) -> str:
        """
        Search the HR policy documents for information about:
        leave policies, work from home, salary, onboarding,
        resignation, performance review, travel expenses,
        health benefits, harassment policy, training budget.
        Use this tool when the user asks about any HR policy or rule.
        """
        print(f"\n🔍 RAG Tool: Searching for '{query}'")
        docs = retriever.invoke(query)  # ← FIXED (was get_relevant_documents)

        if not docs:
            return "No relevant HR policy information found."

        results = []
        for i, doc in enumerate(docs, 1):
            results.append(f"[Result {i}]: {doc.page_content}")

        return "\n\n".join(results)

    return search_hr_policies