from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from agents.schemas import StoryBlueprint, Script
import os

def write_script(blueprint: StoryBlueprint, language: str = "English") -> Script:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3, api_key=os.getenv("GROQ_API_KEY"))
    structured_llm = llm.with_structured_output(Script)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Screenwriter. Convert the following story blueprint into a detailed screenplay format in {language}. Provide scene numbers, locations, transitions, and key dialogues/actions."),
        ("user", "Blueprint details:\n\nGenre: {genre}\nTone: {tone}\nAudience: {audience}\nCharacters: {characters}\nArc: {arc}")
    ])
    
    chain = prompt | structured_llm
    return chain.invoke({
        "genre": blueprint.genre,
        "tone": blueprint.tone,
        "audience": blueprint.audience,
        "characters": [c.model_dump() for c in blueprint.characters],
        "arc": blueprint.five_step_arc,
        "language": language
    })
