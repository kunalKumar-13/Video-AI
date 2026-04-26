from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

from workflows.graph import create_workflow
from workflows.state import WorkflowState

app = FastAPI(title="Forge AI API", description="Narrative to Visual Story Agent", version="1.0")

class StoryRequest(BaseModel):
    narrative: str
    language: str = "English"

workflow = create_workflow()

@app.post("/generate")
def generate_story(req: StoryRequest):
    try:
        initial_state = {
            "narrative": req.narrative,
            "language": req.language,
            "blueprint": None,
            "script": None,
            "scene_plan": None,
            "images": [],
            "evaluation": None,
            "errors": []
        }
        
        result = workflow.invoke(initial_state)
        
        return {
            "status": "success",
            "eval_report": result.get("evaluation"),
            "script": result.get("script"),
            "scene_plan": result.get("scene_plan"),
            "images": result.get("images")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}
