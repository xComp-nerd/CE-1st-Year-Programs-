''' Source code authored by Eljay Calanday and Jayson Nolasco'''

import tkinter as tk
from tkinter import messagebox
import random
import json
import os

DB_PATH = "QuizDB.json"

class QuestionManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.questions = self._load_all_questions()

    def _load_all_questions(self):
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database file not found: {self.db_path}")
        with open(self.db_path, 'r') as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("QuizDB.json must contain a list of question dicts")
        return data.copy()

    def get_random_question(self):
        if not self.questions:
            return None
        choice = random.choice(self.questions)
        self.questions.remove(choice)
        return choice['Question']

class QuizGameUI:
    def __init__(self, root, num_questions=10, time_limit=10):
        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("600x400")

        self.manager = QuestionManager()
        self.num_questions = min(num_questions, len(self.manager.questions))
        self.time_limit = time_limit

        self.score = 0
        self.unanswered = 0
        self.current_qnum = 0
        self.time_left = self.time_limit
        self.timer_running = False
        self.timer_job = None

        self._build_ui()
        self._show_welcome()

    def _build_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True, fill='both')

        self.info_label = tk.Label(self.frame, text="", font=("Arial", 14))
        self.info_label.pack(pady=10)

        self.question_label = tk.Label(self.frame, text="", wraplength=500, font=("Arial", 16))
        self.question_label.pack(pady=20)

        self.answer_buttons = []
        for idx in range(4):
            btn = tk.Button(self.frame, text="", font=("Arial", 14), width=40,
                            command=lambda i=idx: self._on_answer(i))
            btn.pack(pady=5)
            self.answer_buttons.append(btn)

        self.timer_label = tk.Label(self.frame, text="", font=("Arial", 12))
        self.timer_label.pack(pady=10)

    def _clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.pack_forget()
        self.frame.pack(expand=True, fill='both')

    def _show_welcome(self):
        self._clear_frame()
        self.question_label.config(text=(
            f"Welcome to the Quiz Game!\nYou will answer {self.num_questions} questions,"
            f" each within {self.time_limit} seconds.\nClick Start to begin."
        ))
        start_btn = tk.Button(self.frame, text="Start Quiz", font=("Arial", 14), command=self._start_quiz)
        start_btn.pack(pady=20)

    def _start_quiz(self):
        self.score = 0
        self.unanswered = 0
        self.current_qnum = 0
        self.manager.questions = self.manager._load_all_questions()
        self._next_question()

    def _next_question(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        if self.current_qnum >= self.num_questions:
            return self._show_results()

        qdata = self.manager.get_random_question()
        if qdata is None:
            return self._show_results()

        self.current_qnum += 1
        self.current_question = qdata
        self._update_ui()
        self._start_timer()

    def _update_ui(self):
        self._clear_frame()
        self.info_label.config(text=(
            f"Question {self.current_qnum}/{self.num_questions}"
            f" | Score: {self.score} | Unanswered: {self.unanswered}"
        ))
        self.info_label.pack(pady=10)

        self.question_label.config(text=self.current_question[0])
        self.question_label.pack(pady=20)

        for idx, btn in enumerate(self.answer_buttons):
            text = f"{chr(65+idx)}. {self.current_question[2+idx]}"
            btn.config(text=text, state='normal')
            btn.pack(pady=5)

        self.timer_label.config(text=f"Time left: {self.time_limit} sec")
        self.timer_label.pack(pady=10)

    def _start_timer(self):
        self.time_left = self.time_limit
        self.timer_running = True
        self._countdown()

    def _countdown(self):
        if not self.timer_running:
            return
        if self.time_left > 0:
            self.timer_label.config(text=f"Time left: {self.time_left} sec")
            self.time_left -= 1
            self.timer_job = self.root.after(1000, self._countdown)
        else:
            self.timer_running = False
            self.unanswered += 1
            messagebox.showinfo("Time's up!", "You ran out of time!")
            self._next_question()

    def _on_answer(self, idx):
        if not self.timer_running:
            return
        self.timer_running = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        correct_answer = self.current_question[1]
        chosen = self.current_question[2 + idx]
        if chosen == correct_answer:
            self.score += 1
        self.root.after(300, self._next_question)

    def _show_results(self):
        self._clear_frame()
        self.question_label.config(
            text=f"Quiz Over!\nYour Score: {self.score}/{self.num_questions}\nUnanswered: {self.unanswered}"
        )
        self.question_label.pack(pady=20)
        exit_btn = tk.Button(self.frame, text="Exit", font=("Arial", 14), command=self.root.quit)
        exit_btn.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizGameUI(root)
    root.mainloop()
