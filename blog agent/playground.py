from phi.agent import Agent
import phi.api
from phi.model.groq import Groq
from phi.tools.website import WebsiteTools
from phi.tools.googlesearch import GoogleSearch
import openai
from dotenv import load_dotenv
import os
import phi
from phi.playground import Playground, serve_playground_app
load_dotenv()

phi.api = os.getenv('PHI_API_KEY')

openai.api_key = os.getenv("OPENAI_API_KEY")

# web search agent
websearch_agent = Agent(
    name = "web search agent",
    role = "Search the web for the information",
    model = Groq(id="llama-3.2-3b-preview"),
    tools = [GoogleSearch()],
    instructions= ["Always include sources"],
    show_tool_calls=True,
    markdown=True
)

# Website agent
website_agent = Agent(
    name = "website blog agent",
    model = Groq(id="llama-3.2-3b-preview"),
    tools = [WebsiteTools()],
    instructions= ["Get information from the given website url"],
    show_tool_calls=True,
    markdown= True,
)

multi_ai_agent = Agent(
    team= [websearch_agent, websearch_agent],
    instructions= ["Always include sources","Get information from the given website url"],
    show_tool_calls= True,
    markdown= True
)

app = Playground(agents=[websearch_agent,website_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app",reload=True)
    
