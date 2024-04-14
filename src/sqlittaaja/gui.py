from tkinter import Tk, ttk
from tkinter.filedialog import askopenfilename
import tomllib
from sqlittaaja.checker import check_exercises
from sqlittaaja.extractor import extract
from sqlittaaja.diff_check import compute_similarity


def load_config_file():
    """Loads config file."""
    global config_file_path

    config_file_path = askopenfilename(filetypes=[("Toml files", "*.toml")])
    if config_file_path:
        load_config_btn.configure(text="Done!")


def print_gui_score():
    """Checks exercises and prints score to GUI."""

    try:
        with open(config_file_path, "rb") as file:
            config = tomllib.load(file)

            init_script = config["answer"].get("initialize", "")
            answer = config["answer"]["exercise"]
            exercises = extract(config["exercise"]["path"])

            student_scores = check_exercises(init_script, answer, exercises)
            answer_similarities = compute_similarity(exercises)

            for widget in student_score_frame.winfo_children():
                widget.destroy()

            ttk.Label(
                student_score_frame,
                text="Student Name",
                font=("Arial", 15),
            ).grid(row=0, column=0)

            ttk.Label(
                student_score_frame,
                text="Score",
                font=("Arial", 15),
            ).grid(row=0, column=1)

            if answer_similarities:
                ttk.Label(
                    student_score_frame,
                    text="Similarity",
                    font=("Arial", 15),
                ).grid(row=0, column=2)

            ttk.Separator(student_score_frame, orient="horizontal").grid(
                row=1, column=0, columnspan=3, sticky="ew"
            )

            row = 2

            for student_name, score in student_scores.items():

                ttk.Label(
                    student_score_frame,
                    text=student_name,
                    font=("Arial", 15),
                ).grid(row=row, column=0, sticky="w")

                ttk.Label(
                    student_score_frame,
                    text=score,
                    font=("Arial", 15),
                ).grid(row=row, column=1, padx=10, sticky="e")

                if student_name in answer_similarities:
                    for name, similarity in answer_similarities[student_name]:
                        ttk.Label(
                            student_score_frame,
                            text=f"{name} ({str(round(similarity * 100, 2))}%)",
                            font=("Arial", 15),
                            foreground="red",
                        ).grid(row=row, column=2, padx=10, sticky="w")
                        row += 1
                row += 1
                ttk.Separator(student_score_frame, orient="horizontal").grid(
                    row=row, column=0, columnspan=3, sticky="ew"
                )
                row += 1

            window.update_idletasks()
            window_width = (
                student_score_frame.winfo_width()
                if student_score_frame.winfo_width() > frame.winfo_width()
                else frame.winfo_width()
            )
            window.geometry(
                f"{window_width}x{frame.winfo_height() + student_score_frame.winfo_height() + 30}"
            )
            load_config_btn.configure(text="Select file")

    except Exception as e:
        print("Error printing gui score:", e)


def start_gui():
    """Starts tkinter gui"""
    global window, frame, student_score_frame, load_config_btn, config_file_path

    window = Tk()
    window.title("SQLite exercise checker")

    frame = ttk.Frame(window, padding=20)
    frame.grid()

    ttk.Label(frame, text="Config file", padding=10).grid(row=0, column=0)
    load_config_btn = ttk.Button(frame, text="Select file", command=load_config_file)
    load_config_btn.grid(row=0, column=1)

    ttk.Button(frame, text="Check exercises", command=print_gui_score, padding=10).grid(
        row=1, column=0, columnspan=2, sticky="ew"
    )

    student_score_frame = ttk.LabelFrame(window, padding=5)
    student_score_frame.grid(column=0)

    window.update_idletasks()
    window.geometry(f"{frame.winfo_width()}x{frame.winfo_height()}")
    window.mainloop()
