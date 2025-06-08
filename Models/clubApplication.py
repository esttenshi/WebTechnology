from dataclasses import dataclass

@dataclass
class ClubApplication:

    id: int = None
    title: str = None
    head: str = None
    description: str = None
    path_to_img: str = None