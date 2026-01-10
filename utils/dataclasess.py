"""Use as output parameter for function to keep consistency"""

# Importing libraries
from dataclasses import dataclass
from typing import Optional

@dataclass
class ModuleResults:
    sentence: str
    context: str
    status: Optional[bool] = None
