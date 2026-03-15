from duckduckgo_search import DDGS # type: ignore
from ai_brain import generate_response # brain link

def deep_research(q): # rag node
    try:
        res = [r['body'] for r in DDGS().text(q, max_results=3)] # web pull
        if not res: return "Sir, the search yielded no significant data." # zero res
        
        p = f"Using this context, give a concise answer (natural, no markdown, end with 'Sir'):\n\nCONTEXT:\n{chr(10).join(res)}\n\nQUESTION: {q}"
        return generate_response(p) # neuro process
    except: return "Research node timed out, Sir." # time out
