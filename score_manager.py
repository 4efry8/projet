import json
import os

class ScoreManager:
    def __init__(self):
        self.score_file = "data/scores.json"
        if not os.path.exists(self.score_file):
            with open(self.score_file, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def save_score(self, name, difficulty, score, elapsed_time):
        with open(self.score_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if difficulty not in data:
            data[difficulty] = []

        data[difficulty].append({"name": name, "score": score, "time": elapsed_time})

        with open(self.score_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def get_top_scores(self, difficulty):
        with open(self.score_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return sorted(data.get(difficulty, []), key=lambda x: (-x['score'], x['time']))[:5]