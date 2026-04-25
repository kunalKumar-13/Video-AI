import urllib.parse

def generate_image(prompt: str) -> str:
    """Uses Pollinations API for unmetered free image generation since Gemini doesn't offer free API image tools directly."""
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        # We append a random seed text logic to ensure unique urls if multiple of the same prompt occur
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
        return url
    except Exception as e:
        print(f"Error generating image url: {e}")
        return ""
