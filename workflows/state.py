from typing import TypedDict, Optional, List
from agents.schemas import StoryBlueprint, Script, ScenePlan, EvaluationReport

class WorkflowState(TypedDict):
    """The state of the narrative conversion workflow."""
    narrative: str
    language: str
    
    blueprint: Optional[StoryBlueprint]
    script: Optional[Script]
    scene_plan: Optional[ScenePlan]
    images: List[str]
    evaluation: Optional[EvaluationReport]
    
    mock_mode: bool
    errors: List[str]
