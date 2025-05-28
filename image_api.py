from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.image_agent import image_agent
from app.models.image import ImageAgentResponse

router = APIRouter()

class ImageRequest(BaseModel):
    session_id: str
    image_url: str

@router.post("/image", response_model=ImageAgentResponse)
async def analyze_image(request: ImageRequest):
    result = await image_agent.run(request.image_url)
    return result.output
