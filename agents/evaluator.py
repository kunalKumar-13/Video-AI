from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from agents.schemas import StoryBlueprint, Script, ScenePlan, EvaluationReport
import os

def evaluate_pipeline(narrative: str, blueprint: StoryBlueprint, script: Script, scene_plan: ScenePlan) -> EvaluationReport:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3, api_key=os.getenv("GROQ_API_KEY"))
    structured_llm = llm.with_structured_output(EvaluationReport)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an impartial AI Evaluator. Review the original narrative, Blueprint, Script, and Scene Plan. Assess coherence, logical flow, and visual feasibility. Identify any issues, assign a score out of 10, and approve if score >= 7 and no critical issues exist."),
        ("user", "Narrative: {narrative}\n\nBlueprint: {blueprint}\n\nScript: {script}\n\nScene Plan: {scene_plan}")
    ])
    
    chain = prompt | structured_llm
    return chain.invoke({
        "narrative": narrative,
        "blueprint": blueprint.model_dump(),
        "script": script.model_dump(),
        "scene_plan": scene_plan.model_dump()
    })
