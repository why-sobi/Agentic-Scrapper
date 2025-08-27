from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.tools import Tool
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType

from langchain.tools import StructuredTool

from pydantic import BaseModel
import ast # For structured output (Convert string representation of list to Python list)

# from langchain.prompts import PromptTemplate
# from langchain.chains.llm import LLMChain
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.chains import ConversationalRetrievalChain # this allows query with memory

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY_1")


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=api_key,
    temperature=0.1)



from utility.outputFormat import FinalResult # this is a custom schema for saving product listings
from utility.save import SaveResult


# - ```IMPORT CUSTOM TOOLS HERE AS FUNCTIONS```


from scrappers.olx_scrapper import OlxScrapper
from scrappers.daraz import DarazScrapper


# - ```Setup of the Scrapper Agent```


systemPrompt = """You are a helpful agent that scrapes listings from various platforms based on user queries. 
You will use the tools provided to gather information and return it in a structured format without any additional text.

User Query: {query}"""

generic_scraping_description = """A tool to scrape {name} for listings based on a query. 
It returns a list of dictionary with keys 'name', 'URL', 'price', 'rating', 'description'."""

save_scraping_description = """Saves the scraped listings to a local CSV file. Expects a list of dictionaries along with a file name."""


# - `Scrapper Tools`



OlxScrapperTool = Tool(
    name="olx_scrapper",
    func=OlxScrapper,
    description=generic_scraping_description.format(name="OLX"),
)

DarazScrapperTool = Tool(
    name="daraz_scrapper",
    func=DarazScrapper,
    description=generic_scraping_description.format(name="Daraz")
)


# - `Utility Tools`


# SaveScrapingTool = StructuredTool.from_function(
#     name="save_scraping",
#     func=SaveResult,
#     description=save_scraping_description,
#     # args_schema=SaveResultParams
# )


tools = load_tools(["llm-math"], llm=llm)

tools.extend([OlxScrapperTool, DarazScrapperTool]) # as we add more scrappers, we can extend this list
# tools.extend([SaveScrapingTool]) # as we add more utility tools, we can extend this list


# - ```Function and Usage of Scrapper Agent```


def ScrapeListings(query: str) -> FinalResult:
    """
    Scrape listings from various platforms based on the query.
    
    Args:
        query (str): The search query to use for scraping.
        
    Returns:
        list: A list of dictionaries containing the scraped data.
    """
    
    query = systemPrompt.format(query=query)
    
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    # print(type(agent.agent))
    
    response = agent.invoke(query)
    return ast.literal_eval(response['output']) # Convert the string representation of the list back to a Python list


# ## NOTE  
# - Right now search is only done based on the product, it does not support any sort of filters whatsoever 


SaveResult(ScrapeListings("Get listing for nvidia graphic cards from olx"), filename="graphic_cards.csv")





