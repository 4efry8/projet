class DifficultySettings:
    def __init__(self, level):
        if level == "easy":
            self.time_limit = 30
            self.score_multiplier = 1
        elif level == "medium":
            self.time_limit = 20
            self.score_multiplier = 2
        elif level == "hard":
            self.time_limit = 10
            self.score_multiplier = 3