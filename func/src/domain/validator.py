# Third part
from pydantic import BaseModel


class Snapshots(BaseModel):
    pid: dict
    onboarding: list
    wallet: list
    vai_na_cola: list
    blocked_assets: list
    user_blocks: dict
    warranty_assets: list
    warranty: dict

