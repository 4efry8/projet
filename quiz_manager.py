import json
import random

class QuizManager:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.questions = self.load_questions()
        self.current_question = None

    def load_questions(self):
        with open(f"data/questions/{self.difficulty}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["questions"]

    def get_random_question(self):
        if not self.questions:
            return None
        self.current_question = random.choice(self.questions)
        self.questions.remove(self.current_question)
        return self.current_question

    def verify_answer(self, answer_index):
        return answer_index == self.current_question["correct_answer"]