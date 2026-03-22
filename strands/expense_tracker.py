from strands import Agent, tool
from strands.models import BedrockModel

model = BedrockModel(
    model_id = "us.anthropic.claude-opus-4-5-20251101-v1:0",
    region_name = "us-east-1",
    temperature = 0.7,
    max_tokens = 1024,
)

#In-memory store
_expenses: list[dict] = [] 

@tool
def add_expense(amount: float, category: str, description: str) -> str:
    """Add a new expense entry to the tracker.

    Args:
        amount: Expense amount in INR
        category: Spending category (e.g., Food, Tech, Travel)
        description: Brief description of the expense

    Returns:
        Confirmation message
    """
    _expenses.append({"amount": amount, "category": category, "description": description})
    return f"Added: ₹{amount:.2f} for {category} ({description})"


@tool
def get_spending_summary() -> str:
    """Get a summary of all expenses grouped by category with totals.

    Returns:
        Formatted spending summary with category totals and grand total
    """
    if not _expenses:
        return "No expenses recorded yet"
    
    totals: dict[str, float] = {}

    for exp in _expenses:
        totals[exp["category"]] = totals.get(exp["category"], 0) + exp["amount"]

    lines = ["Spending summary:", "-"*30]

    for cat, total in sorted(totals.items(), key=lambda x: -x[1]):
        lines.append(f" Total:  ₹{sum(totals.values()):.2f}")
    
    return "\n".join(lines)


@tool
def get_largest_expense() -> str:
    """Find the single largest expense entry.

    Returns:
        Details of the largest expense
    """
    if not _expenses:
        return "No expenses recorded yet."
    largest = max(_expenses, key=lambda x: x["amount"])
    return f"Largest: ₹{largest['amount']:.2f} on {largest['category']} ({largest['description']})"


agent = Agent(
    model=model,
    tools=[add_expense, get_spending_summary, get_largest_expense])

if __name__ == "__main__":
    agent("""
I had the following expenses this week:
- ₹500 on groceries
- ₹150 on coffee at Starbucks
- ₹800 on my AWS bill
- ₹300 on Ola to the airport
- ₹4500 on a flight ticket

Please add all of these, then show me a spending summary
and tell me my largest single expense.
""")