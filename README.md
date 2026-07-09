ResearchMind 🔬
ResearchMind is an automated, multi-agent AI research pipeline that conducts web searches, scrapes deep page content, synthesizes findings into structured reports, and evaluates its own output with rigorous editorial critique.

Powered entirely by the ultra-fast Groq Ecosystem and orchestrated via LangChain, the application provides a 100% UI-driven environment that requires no persistent configuration or local environmental keys.

🚀 Key Features
Dynamic UI-Driven Credentials: Enter your Groq and Tavily API keys directly into the frontend interface. Your credentials are held securely in temporary memory and are never saved to disk.

Dual-Agent Collaboration: * Search Agent: Queries the web via Tavily and extracts high-impact summaries.

Reader Agent: Deep-scrapes target text and strips out noisy elements (navbars, ads, scripts).

Sequential Synthesis Pipeline: A dedicated Writer Chain compiles the scraped insights into a cohesive markdown report while a Critic Chain scores and checks the final draft.

Groq API Optimized: Tailored chunking limits ensure your runs stay completely clear of standard free-tier Token-Per-Minute (TPM) limits.

🛠️ System Architecture
The workflow flows sequentially across three custom files:

┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   tools.py  │ ───>  │  agents.py  │ ───>  │   app.py    │
└─────────────┘       └─────────────┘       └─────────────┘
 Raw Extraction        Agent Wrappers        Streamlit UI
  (BS4/Tavily)         & Chain Logics       & Context Flow




📦 Prerequisites & Installation
Make sure your virtual environment (my_env) is activated, then install the required dependencies:

PowerShell
pip install streamlit langchain langchain-groq langchain-core tavily-python beautifulsoup4 requests lxml python-dotenv
Required Packages List
streamlit (Frontend rendering engine)

langchain & langchain-core (Agent frameworks)

langchain-groq (Groq API bindings)

tavily-python (Web exploration API)

beautifulsoup4 (DOM cleaning and scraping)

💻 Project Structure
Your project directory should look exactly like this:

Plaintext
multi_agent_ai_model/
│
├── app.py          # Streamlit layout, Sidebar panel, and step execution
├── agents.py       # LLM factory and agent executors wrapping the tools
└── tools.py        # Raw functional definitions for Tavily search and Scraper
⚡ How to Run
Open your terminal inside your project folder and activate your virtual environment.

Launch the Streamlit server using Python's module runner:

PowerShell
python -m streamlit run app.py
Open the browser window (usually http://localhost:8501).

Expand the Sidebar Panel, enter your Groq API Key (gsk_...) and Tavily API Key (tvly_...).

Enter a research topic and trigger the execution pipeline!

📝 Advanced Configuration (Token Mitigation)
To respect Groq's standard limit of 6,000 Tokens per Minute (TPM) for the llama-3.1-8b-instant model, text extraction has been hard-capped:

Web Search: Max results are constrained to 3 items with a max summary layout of 180 characters.

Web Scraper: Clean page reads are bounded to the top 1,000 characters of readable text.

📄 License
This project is built for professional research workflows and educational applications. Feel free to modify the internal agent prompts inside agents.py to match alternative analytical structures!
