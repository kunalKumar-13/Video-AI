from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from agents.schemas import StoryBlueprint
import os

def plan_story(narrative: str, language: str = "English") -> StoryBlueprint:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3, api_key=os.getenv("GROQ_API_KEY"))
    structured_llm = llm.with_structured_output(StoryBlueprint)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert AI Story Planner. Process the user's messy narrative and output a structured story blueprint in {language}."),
        ("user", "{narrative}")
    ])
    
    chain = prompt | structured_llm
    return chain.invoke({"narrative": narrative, "language": language})
