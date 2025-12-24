class Memory:
    def __init__(self):
        self.short_term = []
        self.profile = {
            "name": None, "age": None, "gender": None, "location": "Gujarat",
            "district": None, "income_monthly": None, "occupation": None,
            "household_size": None, "disability": None, "caste_category": None,
            "farmer": None, "student": None
        }
        self.chosen_scheme = None
        self.application = None

    def update_profile(self, key, value):
        self.profile[key] = value

    def remember_turn(self, user_text=None, agent_text=None, corrections=None):
        self.short_term.append({"user_text": user_text, "agent_text": agent_text, "corrections": corrections})

    def get_missing_fields(self, fields):
        return [f for f in fields if not self.profile.get(f)]
