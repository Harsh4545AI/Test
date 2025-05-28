from pydantic_ai import Agent
from app.models.image import ImageAgentResponse
from app.prompts.image_analysis import IMAGE_ANALYSIS_PROMPT

image_agent = Agent(
    model="openai:gpt-4o",
    output_type=ImageAgentResponse,
    system_prompt=IMAGE_ANALYSIS_PROMPT
)
