from dataclasses import dataclass

@dataclass
class Lead:
    name: str
    title: str
    company: str
    location: str
    profile_url: str
    email: str
