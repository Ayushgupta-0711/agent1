# import streamlit as st
# import requests
# import pandas as pd
# from io import BytesIO
# import base64
# import matplotlib.pyplot as plt

# BACKEND_URL = st.secrets.get("backend_url", "http://backend:8000")

# st.set_page_config(page_title="Multi-Agent Data + Research Assistant", layout="wide")
# st.title("Multi-Agent Data + Research Assistant")

# # Sidebar: agent buttons
# st.sidebar.header("Agents")
# agent_choice = st.sidebar.radio("Choose an agent:", ("Orchestrator", "Data Intelligence", "Research Assistant"))

# # File upload area
# uploaded_file = st.file_uploader("Upload CSV/Excel or PDF (for research)", type=["csv","xlsx","xls","pdf"])
# query = st.text_input("Ask your question", key="query_input")

# col1, col2 = st.columns([1,3])
# with col1:
#     if st.button("Run"):  # Unified Run button
#         files = {}
#         data = {"query": query}
#         if uploaded_file is not None:
#             files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
#         try:
#             if agent_choice == "Orchestrator":
#                 resp = requests.post(f"{BACKEND_URL}/orchestrate", data=data, files=files, timeout=60)
#             elif agent_choice == "Data Intelligence":
#                 resp = requests.post(f"{BACKEND_URL}/data-agent/query", data=data, files=files, timeout=60)
#             else:
#                 resp = requests.post(f"{BACKEND_URL}/research-agent/query", data=data, files=files, timeout=60)
#             st.session_state["resp"] = resp.json()
#         except Exception as e:
#             st.error(f"Request failed: {e}")

# with col2:
#     if "resp" in st.session_state:
#         resp = st.session_state["resp"]
#         st.subheader("Response")
#         if resp.get("type") == "table":
#             df = pd.DataFrame(resp.get("data"))
#             st.dataframe(df)
#         elif resp.get("type") == "chart" and resp.get("chart_base64"):
#             chart_bytes = base64.b64decode(resp.get("chart_base64"))
#             st.image(chart_bytes)
#         else:
#             st.write(resp.get("text", "No output returned."))

# # Quick examples
# st.markdown("---")
# st.markdown("**Quick examples:**")
# if st.button("Show total sales in Q2 (example)"):
#     st.session_state["query_input"] = "What was the total sales in Q2?"

# if st.button("Plot revenue trends for top 5 products (example)"):
#     st.session_state["query_input"] = "Plot revenue trends for the top 5 products."


# if "query_input" not in st.session_state:
#         st.session_state.query_input = "Initial Value"

#         st.text_input("Enter query", key="query_input")

# st.markdown("---")
# st.info("Notes: Backend must be running. Default backend URL is 'http://backend:8000' when using docker-compose.")
import streamlit as st
import requests
import pandas as pd
import base64

# ✅ Backend URL (from secrets or fallback)
BACKEND_URL = st.secrets.get("backend_url", "http://127.0.0.1:8000")

# ✅ Page setup
st.set_page_config(page_title="Multi-Agent Data + Research Assistant", layout="wide")
st.title("Multi-Agent Data + Research Assistant")

# Sidebar: agent choice
st.sidebar.header("Agents")
agent_choice = st.sidebar.radio(
    "Choose an agent:",
    ("Orchestrator", "Data Intelligence", "Research Assistant")
)

# File upload + query box
uploaded_file = st.file_uploader(
    "Upload CSV/Excel or PDF (for research)",
    type=["csv", "xlsx", "xls", "pdf"]
)
query = st.text_input("Ask your question", key="query_input")

# Layout
col1, col2 = st.columns([1, 3])

with col1:
    if st.button("Run"):
        files = {}
        data = {"query": query}

        if uploaded_file is not None:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}

        try:
            if agent_choice == "Orchestrator":
                resp = requests.post(f"{BACKEND_URL}/orchestrate", data=data, files=files, timeout=60)
            elif agent_choice == "Data Intelligence":
                resp = requests.post(f"{BACKEND_URL}/data-agent/query", data=data, files=files, timeout=60)
            else:
                resp = requests.post(f"{BACKEND_URL}/research-agent/query", data=data, files=files, timeout=60)

            st.session_state["resp"] = resp.json()
        except Exception as e:
            st.error(f"Request failed: {e}")

with col2:
    if "resp" in st.session_state:
        resp = st.session_state["resp"]
        st.subheader("Response")

        if resp.get("type") == "table":
            df = pd.DataFrame(resp.get("data"))
            st.dataframe(df)
        elif resp.get("type") == "chart" and resp.get("chart_base64"):
            chart_bytes = base64.b64decode(resp.get("chart_base64"))
            st.image(chart_bytes)
        else:
            st.write(resp.get("text", "No output returned."))

# Quick examples
st.markdown("---")
st.markdown("**Quick examples:**")

if st.button("Show total sales in Q2 (example)"):
    st.session_state.query_input = "What was the total sales in Q2?"

if st.button("Plot revenue trends for top 5 products (example)"):
    st.session_state.query_input = "Plot revenue trends for the top 5 products."

st.markdown("---")
st.info("Notes: Backend must be running. Default backend URL is 'http://127.0.0.1:8000' when using docker-compose.")
