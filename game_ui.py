import tkinter as tk
from tkinter import messagebox
from quiz_manager import QuizManager
from score_manager import ScoreManager
from difficulty import DifficultySettings
import time

class QuizGameUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quiz Game")
        self.root.geometry("600x400")
        self.root.configure(bg="#1313d0")
        self.username = ""
        self.score = 0
        self.start_time = None

    def run(self):
        self.show_home()
        self.root.mainloop()

    def show_home(self):
        self.clear_window()
        tk.Label(self.root, text="Welcome to BIT Quiz Game!", font=("Algerian", 20, "bold") ,fg="white", bg="#1313d0",).pack(pady=40)
        tk.Label(self.root, text="Enter your name",font=("Imprint MT Shadow",14,"bold") ,fg="white", bg="#1313d0",).pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=15)

        tk.Label(self.root, text="Choose Difficulty",font=("Arial",14,"bold"),fg="white", bg="#1313d0",).pack(pady=10)
        tk.Button(self.root, text="Easy",font=("Arial",14,"bold"),fg="white", bg="green", command=lambda: self.start_game("easy")).pack(pady=5)
        tk.Button(self.root, text="Medium",font=("Arial",14,"bold") ,fg="white", bg="orange", command=lambda: self.start_game("medium")).pack(pady=5)
        tk.Button(self.root, text="Hard",font=("Arial",14,"bold"),fg="white", bg="red", command=lambda: self.start_game("hard")).pack(pady=5)

    def start_game(self, difficulty):
        self.username = self.name_entry.get()
        if not self.username:
            messagebox.showwarning("Input Error", "Please enter your name.")
            return
        self.difficulty = difficulty
        self.quiz_manager = QuizManager(difficulty)
        self.difficulty_settings = DifficultySettings(difficulty)
        self.score_manager = ScoreManager()
        self.score = 0
        self.start_time = time.time()
        self.show_question()

    def show_question(self):
        question_data = self.quiz_manager.get_random_question()
        if question_data is None:
            self.end_game()
            return

        self.clear_window()
        tk.Label(self.root, text=question_data["question"], wraplength=500, font=("Arial", 16)).pack(pady=20)

        for idx, option in enumerate(question_data["options"]):
            tk.Button(self.root, text=option, width=50,
                      command=lambda i=idx: self.check_answer(i)).pack(pady=5)

        self.root.after(self.difficulty_settings.time_limit * 1000, self.time_up)

    def check_answer(self, selected_index):
        if self.quiz_manager.verify_answer(selected_index):
            self.score += 10 * self.difficulty_settings.score_multiplier
            messagebox.showinfo("Correct!", "Good job!")
        else:
            explanation = self.quiz_manager.current_question.get("explanation", "")
            messagebox.showinfo("Wrong", f"Wrong answer. {explanation}")
        self.show_question()

    def time_up(self):
        if self.quiz_manager.current_question:
            messagebox.showinfo("Time's up!", "You took too long!")
            self.show_question()

    def end_game(self):
        elapsed_time = int(time.time() - self.start_time)
        self.score_manager.save_score(self.username, self.difficulty, self.score, elapsed_time)

        self.clear_window()
        tk.Label(self.root, text="Game Over!", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.root, text=f"Your Score: {self.score}").pack(pady=5)

        tk.Button(self.root, text="View Leaderboard", command=self.show_leaderboard).pack(pady=5)
        tk.Button(self.root, text="Play Again", command=self.show_home).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.destroy).pack(pady=5)

    def show_leaderboard(self):
        self.clear_window()
        tk.Label(self.root, text="Leaderboard", font=("Arial", 20)).pack(pady=20)

        scores = self.score_manager.get_top_scores(self.difficulty)
        for idx, entry in enumerate(scores, start=1):
            tk.Label(self.root, text=f"{idx}. {entry['name']} - {entry['score']} pts ({entry['time']} sec)").pack()

        tk.Button(self.root, text="Back", command=self.show_home).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()