import streamlit as st
import requests

st.set_page_config(page_title="AI Research Assistant", layout="centered")

st.markdown("""
<style>
.stApp { background-color: #0d1117; }
.block-container { background: #161b27; border-radius: 16px; padding: 2.5rem 2.5rem 3rem; max-width: 780px; margin-top: 3rem; }
h1 { color: #ffffff; font-size: 2.2rem; font-weight: 800; margin-bottom: 0.2rem; }
p  { color: #8b949e; font-size: 0.95rem; margin-bottom: 1.5rem; }
.stTextInput > div > div > input { background: #0d1117; border: 1px solid #30363d; border-radius: 10px; color: #fff; padding: 0.75rem 1rem; font-size: 1rem; }
.stTextInput > div > div > input::placeholder { color: #484f58; }
.stButton > button { background: #2f81f7 !important; color: #ffffff !important; border: none !important; border-radius: 10px !important; padding: 0.65rem 1.6rem !important; font-size: 1rem !important; font-weight: 700 !important; cursor: pointer !important; opacity: 1 !important; }
.stButton > button:hover { background: #1f6feb !important; color: #ffffff !important; }
.stButton > button p { color: #ffffff !important; font-weight: 700 !important; }
.stSidebar { background-color: #0d1117; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>AI Research Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p>Generate detailed AI-powered research reports instantly</p>", unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])
with col1:

    topic = st.text_input(
    "Research Topic",
    placeholder="Enter research topic...",
    label_visibility="collapsed"
)

    tavily_api_key = st.text_input(
        "Tavily API Key",
        type="password"
    )

    llm_api_key = st.text_input(
        "LLM API Key",
        type="password"
    )
with col2:
    go = st.button("Generate", use_container_width=True)

backend_url = st.sidebar.text_input("Backend URL", value="http://backend:8000")

if go:
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Researching... this may take a minute."):
            try:
                res = requests.post(

    f"{backend_url}/research",

    json={

        "topic": topic,

        "tavily_api_key": tavily_api_key,

        "llm_api_key": llm_api_key
    },

    timeout=600
)
                print(res.status_code)
                print(res.text)

                res.raise_for_status()

                data = res.json()

                st.divider()
                st.subheader("📄 Report")
                st.markdown(data["report"])

                st.divider()
                st.subheader("🧠 Critic Feedback")
                st.markdown(data["feedback"])

            except requests.exceptions.ConnectionError:
                st.error(f"Cannot connect to backend at `{backend_url}`. Is FastAPI running?")
            except Exception as e:
                st.error(f"Error: {e}")