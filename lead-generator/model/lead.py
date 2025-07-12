from dataclasses import dataclass

@dataclass
class Lead:
    def __init__(self, name, title, company, location, profile_url, email=None, score=0):
        self.name = name
        self.title = title
        self.company = company
        self.location = location
        self.profile_url = profile_url
        self.email = email or ""
        self.score = score

    def calculate_score(self):
        score = 0
        if any(role in self.title.lower() for role in ['cto', 'ceo', 'founder']):
            score += 50
        if any(city in self.location.lower() for city in ['san francisco', 'new york', 'london']):
            score += 25
        if self.company and len(self.company) > 2:
            score += 10
        return score

