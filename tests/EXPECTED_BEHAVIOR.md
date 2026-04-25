# Expected Behavior Matrix

| Input Story           | Planner Expected Outcome                                                                 | Director Expected Outcome                                                               | Evaluator Outcome               |
|-----------------------|-----------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|---------------------------------|
| Kids Fantasy          | Tone: Playful, adventurous.<br>Audience: Children.<br>Chars: Toaster, Vacuum, Boiler.  | Lighting: Bright, colorful neon night.<br>Location: Living room, stairs, dark basement.  | Approved: True, Score: 8-10.    |
| Action Thriller       | Tone: Fast-paced, tense.<br>Audience: Mature.<br>Chars: Ex-op, Mentor, AI.             | Location: Neo-Tokyo.<br>Lighting: High contrast, cinematic cyberpunk.<br>Shot: Tracking. | Approved: True, Score: 8-10.    |
| Ambiguous Mystery     | Tone: Eerie, melancholic.<br>Audience: Adults.<br>Chars: Detective.                     | Location: Seaside town, archives.<br>Lighting: Desaturated, foggy, low visibility.       | Approved: True, Score: 8-10.    |

## Edge Cases
- **Missing API Keys**: The system immediately catches `OPENAI_API_KEY` missing in `.env` and issues a frontend error via Streamlit.
- **DALL-E Refusal**: If an image prompt violates OpenAI's terms or hits a rate limit, the tool is bound by a try-catch block and returns an empty image string, skipping rendering rather than crashing the pipeline. The evaluator may or may not flag this explicitly depending on whether visual feasibility mentions it.
