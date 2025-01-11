from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.website import WebsiteTools
from phi.tools.googlesearch import GoogleSearch
import openai
from dotenv import load_dotenv
import os
load_dotenv()

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

multi_ai_agent.print_response("What is the latest news in the context of this web page url: 'https://www.datascienceoutlook.com/2023/12/apple-deals-with-news-publishers-to.html'",markdown=True)

