from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv
import os

load_dotenv()

#modelsetup

#llm=ChatOpenAI(model="gpt-4o-mini", temperature=0) while using openai

llm= ChatOpenAI(model="gemini-2.5-flash",
                api_key=os.getenv("GEMINI_API_KEY"),
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                temperature=0
                ) 

#1stagent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )

#2ndagent (reader agent)
def build_reader_agent():
     return create_agent(
          model=llm,
          tools=[scrape_url]
    )

#writer chain using runnable
writer_prompt=ChatPromptTemplate.from_messages([
    ("system", " You are an expert research writer . write clear, structured and insightful reports."),
    ("human","""write a detailed research report on the topic below.
      
Topic: {topic}

Research Gathered:{research}
      
Structure the report as:
-Introduction      
-Key Findings (minimun 3 well explained points)
-Conclusion
-Sources(list all URLs found in the research)      
      
Be detailed, factual and professional. """)
])

writer_chain= writer_prompt | llm | StrOutputParser()

#critic_chain
critic_prompt=ChatPromptTemplate([
    ("system","You ae a sharp and constructive research critic . Be honest and specific."),
    ("human","""Review the research report below and evaluate it strictly.

Report:{report}

Respond in this exact format:

Score: X/10          

Strengths:
- ...     
- ...
     
Area to Improve:
- ...     
- ...

One line verdict:
- ... """)
])

critic_chain = critic_prompt | llm | StrOutputParser()

