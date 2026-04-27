# This file is the main engine of my program. It will work with all of my other files depending on which mode is selected (exam or quiz) 
# Charlie Gibbs
# Dated 27/04/2026

import tkinter as tk
from src.quiz import QuizGUI
from src.exam import ExamGUI


def clear(root):
    for widget in root.winfo_children():
        widget.destroy()


def show_menu(root):
    clear(root)

    tk.Label(root, text="Year 10 Numeracy App", font=("Arial", 18)).pack(pady=20)

    tk.Button(root, text="Quiz Mode", width=20,
              command=lambda: start_quiz(root)).pack(pady=10)

    tk.Button(root, text="Exam Mode", width=20,
              command=lambda: start_exam(root)).pack(pady=10)


def start_quiz(root):
    clear(root)
    QuizGUI(root, show_menu)


def start_exam(root):
    clear(root)
    ExamGUI(root, show_menu)


def run():
    root = tk.Tk()
    root.title("Numeracy App")
    root.geometry("400x350")

    show_menu(root)

    root.mainloop()


if __name__ == "__main__":
    run()
