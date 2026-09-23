from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    """Schema for JSON-based comic generation requests (/generate-comic/json)."""
    story_prompt: str = Field(..., description="Main idea for the comic")
    character_name: str = Field(..., description="Hero of the comic")
    setting: str = Field(..., description="Location, e.g. forest, school, city, space")
    tone: str = Field(..., description="Mood of the story, e.g. dramatic, funny")
    art_style: str = Field(..., description="Visual style, e.g. anime, realistic")
