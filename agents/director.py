from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from agents.schemas import Script, ScenePlan
import os

def direct_scenes(script: Script, language: str = "English") -> ScenePlan:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3, api_key=os.getenv("GROQ_API_KEY"))
    structured_llm = llm.with_structured_output(ScenePlan)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a visionary Scene Director. Translate the following script into a visual scene plan. Create compelling visual details for each scene. Ensure that the detailed_image_prompt is a descriptive English prompt suitable for an AI image generator (like DALL-E) to recreate the perfect shot, regardless of the script's language."),
        ("user", "Script Scenes: {scenes}")
    ])
    
    chain = prompt | structured_llm
    return chain.invoke({"scenes": [s.model_dump() for s in script.scenes]})
