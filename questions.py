# Charlie Gibbs
# 15/05/2026
# Question loader system
#
# This module is responsible for loading quiz questions and exam questions from the external JSON file.
# It acts as the data access layer between the stored data and the program.
# Separating data loading from the main program improves decomposition, readability,
# and future maintainability.

import json

def load_questions():
    try:

        # Opens the external questions JSON file containing the quiz and exam questions.
        # Using an external file will improve the future proofing because questions can be modified
        # without changing the core program logic.
        with open("data/questions.json", "r") as file:
            return json.load(file)

    except FileNotFoundError:

        # This handles the case where the questions file is missing which prevents the program from crashing
        # and provides a safe callback structure.
        print("Error: questions.json not found.")
        return {"quiz": [], "exam": []}

    except json.JSONDecodeError:

        # This handles the invalid or corrupted JSON file. This improves the robustness by ensuring
        # it fails safely rather than crashing unexpectedly.
        print("Error: JSON file is corrupted.")
        return {"quiz": [], "exam": []}
