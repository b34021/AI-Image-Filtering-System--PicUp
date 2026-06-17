from dataclasses import dataclass
from typing import List

@dataclass
class SelectedPeopleDTO:
    image_paths: List[str]
    cust_id: int
    event_id: int