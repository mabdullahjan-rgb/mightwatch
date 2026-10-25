# 🌙 NightWatch

**A local AI incident investigator for engineering teams, powered by NVIDIA GB10.**

NightWatch autonomously investigates software incidents by examining application logs, recent deployments, historical incidents, and engineering runbooks. It identifies the likely root cause and recommends the safest next action while keeping sensitive operational data and AI inference local.

## The Problem

During production outages, engineers lose critical time jumping between logs, deployment history, previous incidents, and runbooks. Sending this information to cloud AI systems can also expose sensitive infrastructure and operational data.

NightWatch brings the investigation to the data instead.

## How It Works

An engineer can simply report:

> "Checkout is failing. Investigate."

NightWatch's local agent investigates the incident using available tools:

- `read_logs` — examines current application logs
- `check_deployments` — checks recent software deployments
- `search_incidents` — searches historical incidents
- `read_runbook` — consults engineering response procedures

The agent uses the evidence to produce a root-cause diagnosis and recommended response.

## Demo Incident

In the included checkout incident, NightWatch discovers:

1. Checkout failures began shortly after deployment `v2.8.1`.
2. Logs show database connection timeouts and connection-pool exhaustion.
3. A historical incident contains the same failure pattern.
4. The engineering runbook recommends rollback for a matching deployment regression.
5. NightWatch recommends rollback to the previous stable version.

NightWatch does **not** execute production-changing actions automatically. Human approval is required.

## Local-First Architecture

NightWatch runs AI inference locally on the NVIDIA GB10 using the hackathon's NemoClaw/OpenClaw stack and local Qwen model serving.

Incident evidence remains on-device rather than being sent to a cloud AI API.

## Stack

- NVIDIA GB10
- NemoClaw / OpenClaw
- Local Qwen inference
- Python
- Streamlit
- Git

## Safety

NightWatch separates investigation from execution. It can diagnose incidents and recommend actions, but production-changing actions require explicit engineer approval.

## Why NightWatch

NightWatch turns scattered operational evidence into a single autonomous investigation while preserving the privacy of sensitive engineering data.
