# Charlie Gibbs
# 15/05/2026
# Main application architecture file
#
# This file acts as the main control system for the application.
# This design follows a modular architecture approach which improves maintainability and scalability
# by separating the engine from the function controls.

import tkinter as tk
from src.quiz import QuizGUI
from src.exam import ExamGUI


def clear(root):

    # Removes all the existing UI elements from the window.
    # This ensures a clean transition between scenes.
    for widget in root.winfo_children():
        widget.destroy()


def show_menu(root):

    # Clears the current screen before loading the menu to prevent UI overlapping.
    clear(root)

    # Main title label for the application.
    tk.Label(root, text="Year 10 Numeracy App", font=("Arial", 18)).pack(pady=20)

    # Button to launch the quiz mode.
    tk.Button(root, text="Quiz Mode", width=20,
              command=lambda: start_quiz(root)).pack(pady=10)

     # Button to launch the exam mode
    tk.Button(root, text="Exam Mode", width=20,
              command=lambda: start_exam(root)).pack(pady=10)

    # Button to open the help menu.
    tk.Button(root, text="Help", width=20,
              command=lambda: show_help(root)).pack(pady=10)


def start_quiz(root):

    # Clears the menu before launching the quiz interface.
    clear(root)

    # Initializes quiz module.
    # Passing show_menu as a callback allows the users to return without tight coupling.
    QuizGUI(root, show_menu)


def start_exam(root):

    # Clears menu before launching the exam interface.
    clear(root)

    # Initializes exam GUI module.
    ExamGUI(root, show_menu)

def show_help(root):

    # Clears screen before showing the help menu.
    clear(root)

    # Loads the help instructions from the help.txt file
    # This improves future proofing because there are no changes needed to the main structure of the code.
    try:
        with open("data/help.txt", "r") as file:
            text = file.read()
    except FileNotFoundError:

        # Ensures program doesn't crash if the file is missing.
        text = "Help file not found."

    # Displays help menu in a readable format.
    tk.Label(root, text=text, justify="left", wraplength=350).pack(pady=20)

    # Returns user to the main menu.
    tk.Button(root, text="Back",
              command=lambda: show_menu(root)).pack(pady=10)

def run():

    # Creates the main application window
    root = tk.Tk()
    root.title("Numeracy App")

    # Fixed window size for a consistent layout across devices.
    root.geometry("400x350")

    # Loads menu on start up
    show_menu(root)

    # Starts Tkinter event loop
    root.mainloop()

# Ensures the program runs when only when executed directly.
# This prevents unintended execution when it is imported as a module.
if __name__ == "__main__":
    run()
