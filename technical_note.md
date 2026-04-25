# Technical Note

## Architecture Decisions
The architecture heavily relies on LangGraph. Rather than relying on rigid sequential LangChain wrappers or a single zero-shot LLM pass, LangGraph provides granular deterministic states. State dictionaries are strictly typed using Pydantic, enforcing JSON schema outputs for each distinct agent (e.g., Eventual output structs for Blueprint, Script, Evaluate).

## Why Multi-Agent?
The translation from raw concept to visual storyboard requires vastly different expertise.
1. **Story Planner**: Needs broad strokes, creative constraint matching (5-point arc).
2. **Script Writer**: Requires rigorous formatting logic and dialogue structuring.
3. **Director**: Needs visual prompt engineering suitable for a Latent Diffusion/DALL-E system.
4. **Evaluator**: Needs to step back neutrally and compute a holistic score.
Using a single model pass causes "attention decay" and prompt overload. Breaking logic into specialized agents drastically increases reliability.

## Tradeoffs & Cost Considerations
- **Latencies**: Multi-agent pipelines execute in consecutive blocks (barring async optimizations on parallelizable states). For real-time UX, latency is high (often 20+ seconds).
- **Cost**: Generative image models (like DALL-E-3) are significantly expensive per run ($0.04 per image). A 10-scene script equates to $0.40 purely on storyboard rendering. 
- **Mitigation**: We enforce maximum scene counts via system prompts, employ deterministic temperature strategies (0.3), and could incorporate caching embeddings (FAISS) or local JSON for deterministic caching to avoid redundant reruns in standard scenarios.

## Reliability Strategies
- **Temperature control**: A standard 0.3 enforces less hallucinatory variability in screenplay schema structures.
- **Pydantic Validation**: Using `.with_structured_output(...)` across models guarantees the evaluator model receives reliably structured inputs rather than chaotic free-text parsing.
