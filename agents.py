import os
from langchain_groq import ChatGroq 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_agent
from tools import web_search, web_scraper
from langchain_core.tools import Tool

# ── Dynamic Tool Helpers to fix the missing function error ──
def create_search_tool(tavily_key: str):
    return Tool(
        name="web_search",
        func=lambda query: web_search(query, tavily_key),
        description="Search the web for recent and relevant information on the topic."
    )

def create_scraper_tool():
    return Tool(
        name="web_scraper",
        func=web_scraper,
        description="Scrape and return clean text content from a given URL."
    )

# ── 1. Create the LLM Instance ──
def get_llm(groq_api_key):
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.5,
        groq_api_key=groq_api_key
    )

# ── 2. Build the Search Agent (Kept exactly how you wanted it) ──
def build_search_agent(llm, tavily_key: str):
    search_tool = create_search_tool(tavily_key)
    return create_agent(
        model=llm,
        tools=[search_tool]
    )

# ── 3. Build the Reader Agent (Kept exactly how you wanted it) ──
def build_reader_agent(llm):
    scraper_tool = create_scraper_tool()
    return create_agent(
        model=llm,
        tools=[scraper_tool]
    )

# ── 4. Build the Writer Chain ──
def get_writer_chain(llm):
    writer_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
        ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (CRITICAL: List all sources used. Every source MUST be a clickable Markdown link using the exact format: [Source Name or Title](URL))

Be detailed, factual and professional."""),
    ])
    return writer_prompt | llm | StrOutputParser()

# ── 5. Build the Critic Chain ──
def get_critic_chain(llm):
    critic_prompt = ChatPromptTemplate.from_messages([
         ("system", "You are a sharp and constructive research critic. Be honest and specific."),
         ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
    ])
    return critic_prompt | llm | StrOutputParser()