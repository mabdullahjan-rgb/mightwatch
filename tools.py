from pathlib import Path

BASE = Path(__file__).parent / "data"

def read_logs():
    """Read current checkout-service logs."""
    return (BASE / "logs" / "checkout.log").read_text()

def check_deployments():
    """Check recent software deployments."""
    return (BASE / "deployments.txt").read_text()

def search_incidents():
    """Search historical incidents for similar failures."""
    results = []
    for file in (BASE / "incidents").glob("*.txt"):
        results.append(file.read_text())
    return "\n\n".join(results)

def read_runbook():
    """Read the engineering incident-response runbook."""
    return (BASE / "runbook.txt").read_text()

TOOLS = {
    "read_logs": read_logs,
    "check_deployments": check_deployments,
    "search_incidents": search_incidents,
    "read_runbook": read_runbook,
}

if __name__ == "__main__":
    for name, tool in TOOLS.items():
        print(f"\n===== {name} =====")
        print(tool())
