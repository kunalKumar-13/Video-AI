from langgraph.graph import StateGraph, START, END
from workflows.state import WorkflowState
from agents.planner import plan_story
from agents.writer import write_script
from agents.director import direct_scenes
from agents.evaluator import evaluate_pipeline
from tools.image_generator import generate_image
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("workflow")

from agents.schemas import StoryBlueprint, Character, Script, Scene, ScenePlan, SceneVisuals, EvaluationReport

def planner_node(state: WorkflowState):
    logger.info("Executing Planner Node")
    if state.get("mock_mode"):
        blueprint = StoryBlueprint(
            genre="Cyberpunk Action", tone="Dark & Gritty", audience="Mature",
            characters=[Character(name="Kael", description="Rogue Hacker", role="Protagonist")],
            five_step_arc=["Intro", "Hack", "Chased", "Showdown", "Escape"]
        )
        return {"blueprint": blueprint}
    blueprint = plan_story(state["narrative"], state.get("language", "English"))
    return {"blueprint": blueprint}

def script_node(state: WorkflowState):
    logger.info("Executing Script Node")
    if state.get("mock_mode"):
        script = Script(scenes=[Scene(scene_number=1, location="NEON ALLEY", transition="FADE IN", dialogues=["KAEL: They're onto us!"])])
        return {"script": script}
    script = write_script(state["blueprint"], state.get("language", "English"))
    return {"script": script}

def director_node(state: WorkflowState):
    logger.info("Executing Director Node")
    if state.get("mock_mode"):
        scene_plan = ScenePlan(visuals=[SceneVisuals(scene_number=1, location="Neon Alley", camera_shot="Wide Shot", lighting="Neon Pink & Blue", mood="Tense", detailed_image_prompt="Cyberpunk neon alleyway at night, rainy, glowing pink and blue lights, cinematic")])
        return {"scene_plan": scene_plan}
    scene_plan = direct_scenes(state["script"], state.get("language", "English"))
    return {"scene_plan": scene_plan}

def image_node(state: WorkflowState):
    logger.info("Executing Image Generator Node")
    images = []
    for visual in state["scene_plan"].visuals:
        url = generate_image(visual.detailed_image_prompt)
        images.append(url)
    return {"images": images}

def evaluator_node(state: WorkflowState):
    logger.info("Executing Evaluator Node")
    if state.get("mock_mode"):
        eval_report = EvaluationReport(issues_found=[], coherence_score=10, approved=True)
        return {"evaluation": eval_report}
    eval_report = evaluate_pipeline(
        state["narrative"],
        state["blueprint"],
        state["script"],
        state["scene_plan"]
    )
    return {"evaluation": eval_report}

def create_workflow():
    workflow = StateGraph(WorkflowState)
    
    workflow.add_node("Planner", planner_node)
    workflow.add_node("ScriptWriter", script_node)
    workflow.add_node("Director", director_node)
    workflow.add_node("ImageTool", image_node)
    workflow.add_node("Evaluator", evaluator_node)
    
    workflow.add_edge(START, "Planner")
    workflow.add_edge("Planner", "ScriptWriter")
    workflow.add_edge("ScriptWriter", "Director")
    workflow.add_edge("Director", "ImageTool")
    workflow.add_edge("ImageTool", "Evaluator")
    workflow.add_edge("Evaluator", END)
    
    return workflow.compile()
