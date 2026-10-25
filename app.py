import streamlit as st
from agent import investigate

st.set_page_config(page_title="NightWatch", page_icon="🌙", layout="wide")

st.title("🌙 NightWatch")
st.caption("Autonomous Local AI Incident Investigator • NVIDIA GB10 • NemoClaw + OpenClaw")

st.markdown("### Incident Command Center")

incident = st.text_input(
    "Describe the incident",
    value="Checkout is failing. Investigate."
)

if st.button("🚨 Investigate Incident", type="primary"):
    with st.spinner("NightWatch is autonomously investigating locally..."):
        trace, diagnosis = investigate(incident)

    st.success("Investigation complete")

    st.markdown("### 🧠 Agent Investigation Trace")

    for i, (tool, result) in enumerate(trace, 1):
        with st.expander(f"Step {i} — 🔧 {tool}", expanded=True):
            st.code(result)

    st.markdown("### 🎯 NightWatch Diagnosis")
    st.write(diagnosis)

    st.warning(
        "🛡️ Human approval required before any production-changing action."
    )

st.divider()
st.caption(
    "🔒 LOCAL-FIRST • Qwen 3.5 9B inference runs on-device • "
    "Incident data never leaves the GB10"
)
