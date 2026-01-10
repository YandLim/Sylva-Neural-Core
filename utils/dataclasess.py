from dataclasses import dataclass
from typing import Optional

@dataclass
class ModuleResults:
    sentence: str
    context: str
    status: Optional[bool] = None
