from typing import Literal, get_args

from pydantic import UUID4, BaseModel, Field

Trigger = Literal["trigger"]
TRIGGER: Trigger = get_args(Trigger)[0]


class TriggerReference(BaseModel):
    id: UUID4 = Field(
        ...,
        description="Trigger identifier",
        title="UUID",
    )
    type: Trigger = Field(default=TRIGGER)
