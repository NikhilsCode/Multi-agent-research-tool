import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient

def web_search(query: str, tavily_key: str) -> str:
    """Internal search function using the UI provided key."""
    if not tavily_key:
        return "Error: Tavily API key is missing from the sidebar configuration."
        
    try:
        tavily = TavilyClient(api_key=tavily_key)
        # REDUCED: Max results from 5 down to 3
        results = tavily.search(query=query, max_results=2) 
        out = []
        for r in results['results']:
            out.append(
                # REDUCED: Content snippet from 300 characters down to 180
                f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:180]}\n"
            )
        return "\n----\n".join(out)
    except Exception as e:
        return f"Tavily Search Error: {str(e)}"

def web_scraper(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        # REDUCED: Drastically cut raw text body extraction from 3000 down to 1000 characters
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"