from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from app.llms.models import get_model_from_env

_model = get_model_from_env()
_search = TavilySearchResults(max_results=5)
_tools = [_search]

agent = create_react_agent(_model, _tools)
