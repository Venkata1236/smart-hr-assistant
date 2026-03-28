from langchain.tools import tool
from datetime import datetime


@tool
def book_meeting_with_hr(details: str) -> str:
    """
    Book a meeting with the HR team.
    Use this when the user wants to schedule or book a meeting with HR.
    Input should include the purpose and preferred time if mentioned.
    Example: "book a meeting about salary discussion tomorrow at 3pm"
    """
    print(f"\n📅 Action Tool: Booking meeting — {details}")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""✅ Meeting Request Submitted!

📅 Meeting Details:
- Purpose: {details}
- Requested at: {timestamp}
- Status: Pending HR confirmation
- Meeting ID: HR-{datetime.now().strftime('%Y%m%d%H%M')}

📧 A confirmation email will be sent to your registered email within 2 hours.
HR team will confirm the meeting slot shortly."""


@tool
def submit_leave_request(details: str) -> str:
    """
    Submit a leave request on behalf of the employee.
    Use this when the user wants to apply for or submit a leave request.
    Input should include leave type, start date, end date, and reason.
    Example: "apply for annual leave from April 5 to April 7 for personal reasons"
    """
    print(f"\n📝 Action Tool: Submitting leave — {details}")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""✅ Leave Request Submitted!

📝 Leave Details:
- Request: {details}
- Submitted at: {timestamp}
- Status: Pending Manager Approval
- Request ID: LR-{datetime.now().strftime('%Y%m%d%H%M')}

📧 Your manager will be notified and approval will be sent to your email within 24 hours."""


@tool
def submit_expense_claim(details: str) -> str:
    """
    Submit an expense reimbursement claim.
    Use this when the user wants to claim or submit expenses for reimbursement.
    Input should include expense type, amount, and date.
    Example: "claim travel expense of 2500 rupees for client visit on March 20"
    """
    print(f"\n💰 Action Tool: Submitting expense — {details}")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""✅ Expense Claim Submitted!

💰 Expense Details:
- Claim: {details}
- Submitted at: {timestamp}
- Status: Under Finance Review
- Claim ID: EX-{datetime.now().strftime('%Y%m%d%H%M')}

📧 Finance team will process within 7 working days.
Amount will be credited to your bank account."""


@tool
def contact_hr_team(message: str) -> str:
    """
    Send a message or query directly to the HR team.
    Use this when the user wants to contact HR, raise a concern,
    or report an issue that needs human attention.
    Example: "contact HR about my payslip discrepancy"
    """
    print(f"\n📨 Action Tool: Contacting HR — {message}")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""✅ Message Sent to HR Team!

📨 Message Details:
- Message: {message}
- Sent at: {timestamp}
- Ticket ID: TK-{datetime.now().strftime('%Y%m%d%H%M')}

📧 HR team will respond within 24 hours.
You can track your ticket on the HR portal."""