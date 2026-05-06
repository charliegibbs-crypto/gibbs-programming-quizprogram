import tkinter as tk
import random
import time
from src.questions import load_questions


class ExamGUI:
    def __init__(self, root, back):
        self.root = root
        self.back = back

        data = load_questions()
        self.questions = random.sample(data["exam"], min(10, len(data["exam"])))

        self.index = 0
        self.score = 0

        self.time_limit = 300
        self.start_time = time.time()

        self.timer = tk.Label(root, text="")
        self.timer.pack()

        self.label = tk.Label(root, text="", font=("Arial", 14), wraplength=300)
        self.label.pack(pady=20)

        # VALIDATION ADDED
        vcmd = (root.register(self.validate_input), "%P")
        self.entry = tk.Entry(root, validate="key", validatecommand=vcmd)
        self.entry.pack(pady=10)

        self.entry.bind("<Return>", self.handle_enter)

        self.submit_btn = tk.Button(root, text="Submit", command=self.check)
        self.submit_btn.pack(pady=10)
        tk.Button(root, text="Back", command=self.exit).pack()

        self.update_timer()
        self.load()

    # INPUT VALIDATION
    def validate_input(self, new_text):
        if len(new_text) > 20:
            return False

        allowed_chars = "0123456789./-%:$yn"

        # allow empty input
        if new_text == "":
            return True

        # check every character is allowed
        for char in new_text:
            if char not in allowed_chars:
                return False

        return True

    def update_timer(self):
        remaining = int(self.time_limit - (time.time() - self.start_time))

        if remaining <= 0:
            self.timer.config(text="Time's up!")
            self.timer.pack_forget()
            self.finish()
            return

        mins = remaining // 60
        secs = remaining % 60

        self.timer.config(text=f"Time Left: {mins}:{secs:02}")
        self.root.after(1000, self.update_timer)

    def load(self):
        if self.index >= len(self.questions):
            self.finish()
            return

        q = self.questions[self.index]
        self.label.config(text=f"Q{self.index + 1}: {q['question']}")
        self.entry.delete(0, tk.END)
        self.entry.focus()

    def check(self):
        if self.index >= len(self.questions):
            return

        user = self.entry.get().strip()

        if user == "":
            return

        user = user.lower()
        correct = self.questions[self.index]["answer"].lower()

        if user == correct:
            self.score += 1

        self.index += 1

        if self.index >= len(self.questions):
            self.finish()
        else:
            self.load()

    def handle_enter(self, event):
        self.check()

    def finish(self):
        self.label.config(
            text=f"Exam Finished!\nScore: {self.score}/{len(self.questions)}"
        )
        self.entry.pack_forget()
        self.submit_btn.config(state="disabled")

    def exit(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.back(self.root)
