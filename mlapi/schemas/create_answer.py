from pydantic import BaseModel



class Content(BaseModel):
    """
    Content to be processed by `create_answer`
    """

    fname: str  # Full path to the video file
    rename: str  # Filename to be used for audio file

