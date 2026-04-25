from typing import List
from pydantic import BaseModel, Field

class Character(BaseModel):
    name: str
    description: str
    role: str

class StoryBlueprint(BaseModel):
    genre: str
    tone: str
    audience: str
    characters: List[Character]
    five_step_arc: List[str] = Field(description="5-step story arc (e.g., Intro, Inciting Incident, Rising Action, Climax, Resolution)")

class Scene(BaseModel):
    scene_number: int
    location: str
    transition: str
    dialogues: List[str] = Field(description="Key dialogues or actions in the scene.")

class Script(BaseModel):
    scenes: List[Scene]

class SceneVisuals(BaseModel):
    scene_number: int
    location: str
    camera_shot: str
    lighting: str
    mood: str
    detailed_image_prompt: str

class ScenePlan(BaseModel):
    visuals: List[SceneVisuals]

class EvaluationReport(BaseModel):
    issues_found: List[str] = Field(description="List of issues in narrative coherence or visual feasibility.")
    coherence_score: int = Field(ge=0, le=10, description="Score from 0-10")
    approved: bool = Field(description="True if score >= 7 and no critical issues exist")
