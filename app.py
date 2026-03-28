import os
import sys
from dotenv import load_dotenv
from core.agent import run_hr_agent
from core.vector_store import build_vector_store

load_dotenv()


def print_separator():
    print("\n" + "=" * 60 + "\n")


def print_welcome():
    print_separator()
    print("🤝  SMART HR ASSISTANT — CLI MODE")
    print("    Powered by LangChain + FAISS + ReAct Agent")
    print_separator()
    print("I can help you with:")
    print("  📋 Policy questions — leave, salary, WFH, benefits")
    print("  📅 Book meetings with HR")
    print("  📝 Submit leave requests")
    print("  💰 Expense claims")
    print("  📨 Contact HR team")
    print_separator()
    print("Type 'quit' to exit | 'rebuild' to rebuild FAISS index\n")


def run_cli():
    print_welcome()

    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in .env")
        sys.exit(1)

    while True:
        try:
            user_input = input("You: ").strip()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("👋 Thank you for using Smart HR Assistant!")
            break

        if user_input.lower() == "rebuild":
            build_vector_store()
            continue

        print("\n🤔 Agent is thinking...\n")

        result = run_hr_agent(user_input)

        print(f"\n🤝 HR Assistant:\n{result['output']}\n")

        if result["steps"]:
            print("📊 Tools Used:")
            for step in result["steps"]:
                action = step[0]
                print(f"  → {action.tool}: {action.tool_input[:80]}...")
            print()


if __name__ == "__main__":
    run_cli()