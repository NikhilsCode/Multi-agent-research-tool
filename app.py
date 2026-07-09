import streamlit as st
import time
import os
from agents import get_llm, build_reader_agent, build_search_agent, get_writer_chain, get_critic_chain

st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded", # Opened sidebar by default for configuration
)

# Keep your custom CSS styling block here
st.markdown("""<style>...your existing CSS styles...</style>""", unsafe_allow_html=True)

# ── Sidebar API Configuration ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ API Configuration")
    
    # Read initial defaults from your local .env file if they exist
    default_groq = ""
    default_tavily = ""
    
    user_groq_key = st.text_input("Groq API Key", value=default_groq, type="password", help="Enter your gsk_... key")
    user_tavily_key = st.text_input("Tavily API Key", value=default_tavily, type="password", help="Enter your tvly_... key")
    
    st.markdown("---")
    st.markdown("### 🤖 Model Profile")
    st.info("⚡ **Engine:** `Groq Ecosystem`  \n🔬 **Model:** `llama-3.1-8b-instant`  \n🌡️ **Temp:** `0.5`")

# Initialize session state cleanly
if "results" not in st.session_state:
    st.session_state.results = {}

# ── Pipeline Execution Function ──────────────────────────────────────────────
def run_pipeline(topic_val, groq_key, tavily_key):
    st.session_state.results = {}
    status_placeholder = st.empty()
    
    try:
        llm = get_llm(groq_key)
        writer_chain = get_writer_chain(llm)
        critic_chain = get_critic_chain(llm)
        
        # --- STEP 1: SEARCH ---
        status_placeholder.info("🔍 Step 1: Search Agent is gathering web data...")
        search_agent = build_search_agent(llm, tavily_key)
        sr = search_agent.invoke({"messages": f"Find information about: {topic_val}"})
        search_out = sr.get("output", str(sr)) if isinstance(sr, dict) else str(sr)
        st.session_state.results["search"] = search_out
        time.sleep(1)

        # --- STEP 2: READER ---
        status_placeholder.info("📄 Step 2: Reader Agent is scraping deep resources...")
        reader_agent = build_reader_agent(llm)
        # REDUCED: Drastically cut what we feed into the scraper window from 1000 characters down to 400
        rr = reader_agent.invoke({"messages": f"Scrape key data from these references:\n{search_out[:400]}"})
        reader_out = rr.get("output", str(rr)) if isinstance(rr, dict) else str(rr)
        st.session_state.results["reader"] = reader_out
        time.sleep(1)

        # --- STEP 3: WRITER ---
        status_placeholder.info("✍️ Step 3: Writer is drafting the report...")
        # OPTIMIZED: Truncate the combined text variables to protect the token window budget
        research_combined = f"Search Results:\n{search_out[:1000]}\n\nScraped Content:\n{reader_out[:1000]}"
        writer_out = writer_chain.invoke({"topic": topic_val, "research": research_combined})
        st.session_state.results["writer"] = writer_out
        time.sleep(1)

        # --- STEP 4: CRITIC ---
        status_placeholder.info("🧐 Step 4: Critic is reviewing the report...")
        critic_out = critic_chain.invoke({"report": writer_out})
        st.session_state.results["critic"] = critic_out

        status_placeholder.success("🎉 Pipeline complete!")
        
    except Exception as e:
        st.error(f"An error occurred during pipeline execution: {str(e)}")
    finally:
        # Clean runtime API environments variable paths
        os.environ.pop("GROQ_API_KEY", None)
        os.environ.pop("TAVILY_API_KEY", None)


# ── UI Layout ────────────────────────────────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    with st.form("research_form", clear_on_submit=False):
        topic = st.text_input("Research Topic", placeholder="e.g. Quantum computing breakthroughs")
        submit_button = st.form_submit_button("⚡ Run Research Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

if submit_button:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    elif not user_groq_key.strip() or not user_tavily_key.strip():
        st.error("Missing credentials! Please insert both your Groq and Tavily API keys in the sidebar panel.")
    else:
        run_pipeline(topic, user_groq_key, user_tavily_key)

# ── Display Panel Results ─────────────────────────────────────────────────────
r = st.session_state.results
if r:
    st.markdown('---')
    if "writer" in r:
        st.markdown('### 📝 Final Research Report')
        st.markdown(r["writer"])
    if "critic" in r:
        st.markdown('### 🧐 Critic Feedback')
        st.markdown(r["critic"])