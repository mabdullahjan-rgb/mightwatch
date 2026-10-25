import json
import urllib.request
from tools import TOOLS

MODEL = "qwen3.5:9b"
URL = "http://127.0.0.1:11434/api/chat"

SYSTEM = """You are NightWatch, an autonomous SRE incident investigator running locally.

You can use these tools:
- read_logs: inspect current checkout-service logs
- check_deployments: inspect recent deployments
- search_incidents: search historical incidents
- read_runbook: inspect the incident-response runbook

Investigate incidents by choosing tools yourself.

Respond ONLY with JSON in one of these forms:
{"tool":"read_logs"}
{"tool":"check_deployments"}
{"tool":"search_incidents"}
{"tool":"read_runbook"}
{"final":"your concise diagnosis and recommended action"}

Do not invent evidence. Use tools before diagnosing.
Never execute production-changing actions. Recommend them for engineer approval.
"""

def ask_model(messages):
    body = json.dumps({
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "format": "json"
    }).encode()

    req = urllib.request.Request(
        URL, data=body,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req, timeout=120) as r:
        result = json.loads(r.read())
    return result["message"]["content"]

def investigate(problem):
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": problem}
    ]

    trace = []

    for _ in range(8):
        raw = ask_model(messages)

        try:
            action = json.loads(raw)
        except json.JSONDecodeError:
            messages.append({
                "role": "user",
                "content": "Return valid JSON only."
            })
            continue

        if "final" in action:
            return trace, action["final"]

        tool_name = action.get("tool")

        if tool_name not in TOOLS:
            messages.append({
                "role": "user",
                "content": "Choose one of the available tools."
            })
            continue

        result = TOOLS[tool_name]()
        trace.append((tool_name, result))

        messages.append({"role": "assistant", "content": raw})
        messages.append({
            "role": "user",
            "content": f"TOOL RESULT ({tool_name}):\n{result}"
        })

    return trace, "Investigation stopped after maximum tool calls."

if __name__ == "__main__":
    trace, answer = investigate("Checkout is failing. Investigate.")

    print("\n=== NIGHTWATCH TOOL TRACE ===")
    for name, result in trace:
        print(f"\n[{name}]\n{result}")

    print("\n=== NIGHTWATCH DIAGNOSIS ===")
    print(answer)
