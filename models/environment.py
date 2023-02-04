import uuid
from pydantic import BaseModel, Field

# A response body is the data your API sends to the client

# Models the request body of the "Environment"-entity (meaning sent by/from client to this API)
class Environment(BaseModel):
    env_id: str = Field(default_factory=uuid.uuid4, alias="run_id")
    max_reward: float
    min_reward: float
