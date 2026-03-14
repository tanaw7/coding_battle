import json
import os
import random
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox

# ----------------------------
# Configuration
# ----------------------------

STATE_FILE = "live_battle_state.json"
STAGE_FILENAME = "stage.py"
GRADER_SCRIPT = "grader.py"  # put this grader in the same folder as this UI

DEFAULT_TEAMS = [
    "Group 1: SMATCH",
    "Group 2: SOS",
    "Group 3: PyCharmers",
    "Group 4: Piethon",
    "Group 5: Fantastic 5",
]

MAX_STAGE_POINTS = 3
POINTS_BUG_FOUND = 1

# Put a greek battle image in the SAME folder as this script, e.g. greek_battle.png
# Or set this to an absolute path.
GREEK_IMAGE_CANDIDATES = [
    "img.png",
    "img.gif",
    "img.ppm",
]

# (num, topic, title, function, file)
EXERCISES = [
    (1, "A", "Add Two Integers", "add_two", "f01_add_two.py"),
    (2, "A", "Minutes to Seconds", "minutes_to_seconds", "f02_minutes_to_seconds.py"),
    (3, "A", "Average of Two Floats", "average_two", "f03_average_two.py"),
    (4, "A", "Greeting Text", "greet", "f04_greet.py"),
    (5, "A", "String Length", "string_length", "f05_string_length.py"),
    (6, "A", "Is Positive", "is_positive", "f06_is_positive.py"),
    (7, "A", "Percent to Decimal", "percent_to_decimal", "f07_percent_to_decimal.py"),
    (8, "A", "Decimal to Percent", "decimal_to_percent", "f08_decimal_to_percent.py"),
    (9, "A", "Quotient and Remainder", "divmod_pair", "f09_divmod_pair.py"),
    (10, "A", "Degrees to Radians", "degrees_to_radians", "f10_degrees_to_radians.py"),

    (11, "B", "Is Odd", "is_odd", "f11_is_odd.py"),
    (12, "B", "Compare Two Numbers", "compare_two", "f12_compare_two.py"),
    (13, "B", "Bigger of Two", "bigger", "f13_bigger.py"),
    (14, "B", "Letter Grade", "grade_letter", "f14_grade_letter.py"),
    (15, "B", "Between (Inclusive)", "between_inclusive", "f15_between_inclusive.py"),
    (16, "B", "Ticket Price", "ticket_price", "f16_ticket_price.py"),
    (17, "B", "Safe Division", "safe_divide", "f17_safe_divide.py"),
    (18, "B", "Is Vowel", "is_vowel", "f18_is_vowel.py"),
    (19, "B", "Median of Three Integers", "median_of_three", "f19_median_of_three.py"),
    (20, "B", "Sign of Number", "sign", "f20_sign.py"),

    (21, "C", "Sum of a List", "sum_list", "f21_sum_list.py"),
    (22, "C", "Count Greater Than", "count_greater_than", "f22_count_greater_than.py"),
    (23, "C", "First Divisible by k", "first_divisible", "f23_first_divisible.py"),
    (24, "C", "Count Consonants", "count_consonants", "f24_count_consonants.py"),
    (25, "C", "Squares from 1 to n", "squares_1_to_n", "f25_squares_1_to_n.py"),
    (26, "C", "Cumulative Maximum", "cumulative_max", "f26_cumulative_max.py"),
    (27, "C", "Keep Only Even Numbers", "keep_only_evens", "f27_keep_only_evens.py"),
    (28, "C", "Dash Join Words", "dash_join", "f28_dash_join.py"),
    (29, "C", "Count Occurrences", "count_occurrences", "f29_count_occurrences.py"),
    (30, "C", "Minimum in List", "min_in_list", "f30_min_in_list.py"),

    (31, "D", "Countdown List", "countdown_list", "f31_countdown_list.py"),
    (32, "D", "Sum Until Zero", "sum_until_zero", "f32_sum_until_zero.py"),
    (33, "D", "Count Digits", "count_digits", "f33_count_digits.py"),
    (34, "D", "Reverse Number", "reverse_number", "f34_reverse_number.py"),
    (35, "D", "Multiply by Repeated Addition", "multiply_repeat", "f35_multiply_repeat.py"),
    (36, "D", "Power by Repeated Multiplication", "power_loop", "f36_power_loop.py"),
    (37, "D", "Double Until Target", "double_until", "f37_double_until.py"),
    (38, "D", "Last Index", "last_index", "f38_last_index.py"),
    (39, "D", "Remove Leading Zeros", "remove_leading_zeros", "f39_remove_leading_zeros.py"),
    (40, "D", "Repeat Text", "repeat_text", "f40_repeat_text.py"),

    (41, "E", "Last Element", "last_element", "f41_last_element.py"),
    (42, "E", "First Two Elements (safe)", "first_two", "f42_first_two.py"),
    (43, "E", "Swap First and Last", "swap_first_last", "f43_swap_first_last.py"),
    (44, "E", "Count Above Average", "count_above_average", "f44_count_above_average.py"),
    (45, "E", "Remove All Occurrences", "remove_all", "f45_remove_all.py"),
    (46, "E", "Append (Return New)", "append_new", "f46_append_new.py"),
    (47, "E", "Flatten One Level", "flatten", "f47_flatten.py"),
    (48, "E", "Rotate Left by k", "rotate_left", "f48_rotate_left.py"),
    (49, "E", "Is Sorted (Ascending)", "is_sorted", "f49_is_sorted.py"),
    (50, "E", "Has Duplicates", "has_duplicates", "f50_has_duplicates.py"),

    (51, "F", "Frequency Dictionary (Numbers)", "frequency", "f51_frequency.py"),
    (52, "F", "Character Frequency (Ignore Spaces)", "char_frequency_no_spaces", "f52_char_frequency_no_spaces.py"),
    (53, "F", "Get With Default", "get_with_default", "f53_get_with_default.py"),
    (54, "F", "Sum of Dictionary Values", "sum_dict_values", "f54_sum_dict_values.py"),
    (55, "F", "Most Frequent Number", "most_frequent_number", "f55_most_frequent_number.py"),
    (56, "F", "Merge Counts", "merge_counts", "f56_merge_counts.py"),
    (57, "F", "Word Count", "word_count", "f57_word_count.py"),
    (58, "F", "Keys With Count At Least k", "keys_at_least", "f58_keys_at_least.py"),
    (59, "F", "Invert Dictionary (Unique Values)", "invert_unique", "f59_invert_unique.py"),
    (60, "F", "Histogram Bars", "histogram", "f60_histogram.py"),
]


def exercise_one_line(ex):
    n, topic, title, _fn, _file = ex
    return f"{n:02d} (Topic {topic}) — {title}"


def default_state():
    return {
        "teams": DEFAULT_TEAMS[:],
        "scores": {t: 0 for t in DEFAULT_TEAMS},
        "used_exercises": [],
        "current_exercise": None,
        "round_log": [],      # one row per round
        "undo_stack": [],     # undo records for "Undo Last Round"
        "stage_index": 0,     # auto-rotating stage team index
    }


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Live Coding Battle — Scoreboard")
        self.geometry("1260x780")
        self.minsize(1120, 680)

        self.state_data = self.load_state()
        self.exercise_map = {ex[0]: ex for ex in EXERCISES}

        if not self.state_data.get("teams"):
            self.state_data["teams"] = DEFAULT_TEAMS[:]
        self.state_data["stage_index"] = int(self.state_data.get("stage_index", 0)) % len(self.state_data["teams"])

        self.greeks_photo = None  # keep reference
        self.create_ui()

        if self.state_data.get("current_exercise") is None:
            self.pick_random_no_repeat_or_end()

        self.set_stage_team_from_index()
        self.refresh_all()

    def load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if not isinstance(data, dict) or "teams" not in data or "scores" not in data:
                    return default_state()
                if not data["teams"]:
                    data["teams"] = DEFAULT_TEAMS[:]
                for t in data["teams"]:
                    data["scores"].setdefault(t, 0)
                data.setdefault("used_exercises", [])
                data.setdefault("current_exercise", None)
                data.setdefault("round_log", [])
                data.setdefault("undo_stack", [])
                data.setdefault("stage_index", 0)
                return data
            except Exception:
                return default_state()
        return default_state()

    def save_state(self):
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state_data, f, indent=2, ensure_ascii=False)

    def set_exercise_box_text(self, lines):
        self.ex_text.configure(state="normal")
        self.ex_text.delete("1.0", tk.END)
        self.ex_text.insert(tk.END, "\n".join(lines))
        self.ex_text.configure(state="disabled")

    def refresh_unused_count(self):
        used = set(self.state_data["used_exercises"])
        unused = [ex[0] for ex in EXERCISES if ex[0] not in used]
        self.unused_var.set(f"Unused: {len(unused)} / 60")

    def refresh_exercise_info(self):
        ex_num = self.state_data.get("current_exercise")
        if ex_num is None:
            self.set_exercise_box_text(["(no more exercises)", "", ""])
            return
        ex = self.exercise_map.get(ex_num)
        if not ex:
            self.set_exercise_box_text(["(invalid exercise)", "", ""])
            return
        self.set_exercise_box_text([exercise_one_line(ex), "", ""])

    def refresh_scoreboard(self):
        for item in self.score_tree.get_children():
            self.score_tree.delete(item)
        items = sorted(self.state_data["scores"].items(), key=lambda kv: (-kv[1], kv[0]))
        for team, score in items:
            self.score_tree.insert("", "end", values=(team, score))

    def refresh_round_log(self):
        for item in self.log_tree.get_children():
            self.log_tree.delete(item)
        for i, row in enumerate(self.state_data["round_log"], start=1):
            self.log_tree.insert(
                "", "end",
                values=(
                    i,
                    row.get("exercise", ""),
                    row.get("stage_team", ""),
                    row.get("stage_points", 0),
                    row.get("bug_teams", ""),
                    row.get("note", ""),
                ),
            )

    def refresh_all(self):
        self.refresh_unused_count()
        self.refresh_exercise_info()
        self.refresh_scoreboard()
        self.refresh_round_log()

    def clear_bug_selection(self):
        self.bug_list.selection_clear(0, tk.END)

    def set_stage_team_from_index(self):
        teams = self.state_data["teams"]
        idx = int(self.state_data.get("stage_index", 0)) % len(teams)
        self.stage_team_var.set(teams[idx])

    def advance_stage_team(self):
        teams = self.state_data["teams"]
        self.state_data["stage_index"] = (int(self.state_data.get("stage_index", 0)) + 1) % len(teams)
        self.set_stage_team_from_index()

    def get_unused_numbers(self):
        used = set(self.state_data["used_exercises"])
        return [ex[0] for ex in EXERCISES if ex[0] not in used]

    def pick_random_no_repeat_or_end(self):
        unused = self.get_unused_numbers()
        if not unused:
            self.state_data["current_exercise"] = None
            self.save_state()
            self.refresh_all()
            messagebox.showinfo("Done", "All 60 exercises have been used.")
            return
        self.state_data["current_exercise"] = random.choice(unused)
        self.save_state()
        self.refresh_all()

    def _show_output_window(self, title: str, text: str) -> None:
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry("920x620")

        txt = tk.Text(win, wrap="word")
        txt.insert("1.0", text)
        txt.configure(state="disabled")
        txt.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(win, orient="vertical", command=txt.yview)
        txt.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def run_stage_grader(self) -> None:
        app_dir = os.path.dirname(os.path.abspath(__file__))
        grader_path = os.path.join(app_dir, GRADER_SCRIPT)

        if not os.path.exists(grader_path):
            messagebox.showerror(
                "Grader not found",
                f"Could not find grader script:\n{grader_path}\n\n"
                f"Put {GRADER_SCRIPT} in the same folder as this UI."
            )
            return

        stage_path = os.path.join(app_dir, STAGE_FILENAME)
        if not os.path.exists(stage_path):
            messagebox.showwarning(
                "stage.py not found",
                f"Could not find:\n{stage_path}\n\n"
                "Make sure the student code is saved as stage.py in the same folder."
            )

        try:
            result = subprocess.run(
                [sys.executable, grader_path, app_dir],
                capture_output=True,
                text=True
            )
        except Exception as e:
            messagebox.showerror("Failed to run grader", str(e))
            return

        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += "\n\n--- STDERR ---\n" + result.stderr

        if not output.strip():
            output = "(No output from grader.)"

        self._show_output_window("Stage Grader Output", output)

    def current_exercise_short_text(self):
        ex_num = self.state_data.get("current_exercise")
        if ex_num is None:
            return "(none)"
        ex = self.exercise_map.get(ex_num)
        return exercise_one_line(ex) if ex else str(ex_num)

    def finalize_round_and_next(self):
        ex_num = self.state_data.get("current_exercise")
        if ex_num is None:
            messagebox.showwarning("No exercise", "No exercise available. Reset used list or start a new session.")
            return

        teams = self.state_data["teams"]

        stage_team = self.stage_team_var.get().strip()
        if stage_team not in self.state_data["scores"]:
            messagebox.showerror("Invalid stage team", "Please select a valid stage team.")
            return

        prev_stage_index = int(self.state_data.get("stage_index", 0))
        try:
            self.state_data["stage_index"] = teams.index(stage_team)
        except ValueError:
            self.state_data["stage_index"] = prev_stage_index

        try:
            stage_points = int(self.stage_points_var.get().strip())
        except ValueError:
            messagebox.showerror("Invalid stage points", "Stage points must be 0, 1, 2, or 3.")
            self.state_data["stage_index"] = prev_stage_index
            return
        if stage_points < 0 or stage_points > MAX_STAGE_POINTS:
            messagebox.showerror("Invalid stage points", "Stage points must be 0, 1, 2, or 3.")
            self.state_data["stage_index"] = prev_stage_index
            return

        selected_idxs = list(self.bug_list.curselection())
        bug_teams = []
        for idx in selected_idxs:
            t = self.bug_list.get(idx)
            if t != stage_team:
                bug_teams.append(t)

        note = self.note_var.get().strip()

        undo_record = {
            "exercise_num": ex_num,
            "awards": [],
            "prev_stage_index": prev_stage_index,
        }

        if stage_points != 0:
            self.state_data["scores"][stage_team] += stage_points
            undo_record["awards"].append((stage_team, stage_points))

        for t in bug_teams:
            if t in self.state_data["scores"]:
                self.state_data["scores"][t] += POINTS_BUG_FOUND
                undo_record["awards"].append((t, POINTS_BUG_FOUND))

        self.state_data["round_log"].append({
            "exercise": self.current_exercise_short_text(),
            "stage_team": stage_team,
            "stage_points": stage_points,
            "bug_teams": ", ".join(bug_teams) if bug_teams else "",
            "note": note,
        })

        if ex_num not in self.state_data["used_exercises"]:
            self.state_data["used_exercises"].append(ex_num)

        self.state_data["undo_stack"].append(undo_record)
        if len(self.state_data["undo_stack"]) > 50:
            self.state_data["undo_stack"] = self.state_data["undo_stack"][-50:]

        self.note_var.set("")
        self.stage_points_var.set("3")
        self.clear_bug_selection()

        self.advance_stage_team()

        unused = self.get_unused_numbers()
        self.state_data["current_exercise"] = random.choice(unused) if unused else None

        self.save_state()
        self.refresh_all()

    def undo_last_round(self):
        if not self.state_data["undo_stack"]:
            messagebox.showinfo("Nothing to undo", "No rounds to undo.")
            return

        undo_record = self.state_data["undo_stack"].pop()

        for team, pts in undo_record.get("awards", []):
            if team in self.state_data["scores"]:
                self.state_data["scores"][team] -= pts

        if self.state_data["round_log"]:
            self.state_data["round_log"].pop()

        ex_num = undo_record.get("exercise_num")
        if ex_num in self.state_data["used_exercises"]:
            self.state_data["used_exercises"].remove(ex_num)

        self.state_data["current_exercise"] = ex_num
        self.state_data["stage_index"] = int(undo_record.get("prev_stage_index", 0))
        self.set_stage_team_from_index()

        self.save_state()
        self.refresh_all()

    def reset_used(self):
        if not messagebox.askyesno("Reset used list", "Reset used exercises (allow repeats again)?"):
            return
        self.state_data["used_exercises"] = []
        self.state_data["current_exercise"] = None
        self.state_data["undo_stack"] = []
        self.save_state()
        self.pick_random_no_repeat_or_end()
        self.set_stage_team_from_index()

    def new_session(self):
        if not messagebox.askyesno(
            "New session",
            "This will reset scores to 0 and clear the round log.\n"
            "It will NOT reset the used exercise list unless you click 'Reset used list'.\n\nContinue?"
        ):
            return
        for t in self.state_data["scores"]:
            self.state_data["scores"][t] = 0
        self.state_data["round_log"] = []
        self.state_data["undo_stack"] = []
        if self.state_data.get("current_exercise") is None:
            self.pick_random_no_repeat_or_end()
        self.set_stage_team_from_index()
        self.save_state()
        self.refresh_all()

    def show_state_location(self):
        abs_path = os.path.abspath(STATE_FILE)
        messagebox.showinfo("State file", f"State is saved at:\n{abs_path}")

    def finalize_session(self):
        items = sorted(self.state_data["scores"].items(), key=lambda kv: (-kv[1], kv[0]))
        lines = [f"{i}. {team}: {score}" for i, (team, score) in enumerate(items, start=1)]
        winner = items[0][0] if items else "(none)"
        msg = (
            "Final Scores:\n\n" + "\n".join(lines) +
            f"\n\nWinner: {winner}\n\n"
            "Scoring reminder:\n"
            "- Stage points = 0..3 (you choose)\n"
            f"- Bug-finder teams = +{POINTS_BUG_FOUND} each\n"
            "- Stage team auto-rotates each round\n"
        )
        messagebox.showinfo("Finalized", msg)

    def create_ui(self):
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)

        left = ttk.Frame(self, padding=12)
        right = ttk.Frame(self, padding=12)
        left.grid(row=0, column=0, sticky="nsew")
        right.grid(row=0, column=1, sticky="nsew")

        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)

        ex_box = ttk.LabelFrame(left, text="Current Exercise (auto-random, no repeat)", padding=10)
        ex_box.grid(row=0, column=0, sticky="ew")
        ex_box.columnconfigure(0, weight=1)

        self.ex_text = tk.Text(
            ex_box,
            height=3,
            wrap="word",
            borderwidth=0,
            highlightthickness=0,
        )
        self.ex_text.grid(row=0, column=0, sticky="ew")
        self.ex_text.configure(state="disabled")

        pick_box = ttk.LabelFrame(left, text="Controls", padding=10)
        pick_box.grid(row=1, column=0, sticky="ew", pady=(12, 0))
        pick_box.columnconfigure(0, weight=1)
        pick_box.columnconfigure(1, weight=1)
        pick_box.columnconfigure(2, weight=1)

        self.unused_var = tk.StringVar(value="Unused: ? / 60")
        ttk.Label(pick_box, textvariable=self.unused_var).grid(row=0, column=0, sticky="w")
        ttk.Button(pick_box, text="Pick Next Random", command=self.pick_random_no_repeat_or_end).grid(row=0, column=1, sticky="ew", padx=6)
        ttk.Button(pick_box, text="Reset used list", command=self.reset_used).grid(row=0, column=2, sticky="ew", padx=6)

        round_box = ttk.LabelFrame(left, text="Round Setup (Finalize Round & Next)", padding=10)
        round_box.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        round_box.columnconfigure(1, weight=1)

        ttk.Label(round_box, text="Stage Team (auto-rotates):").grid(row=0, column=0, sticky="w")
        self.stage_team_var = tk.StringVar(value=self.state_data["teams"][0])
        self.stage_team_combo = ttk.Combobox(round_box, textvariable=self.stage_team_var, values=self.state_data["teams"], state="readonly")
        self.stage_team_combo.grid(row=0, column=1, sticky="ew", padx=8)

        ttk.Label(round_box, text="Stage points (0–3):").grid(row=1, column=0, sticky="w", pady=(10, 0))
        self.stage_points_var = tk.StringVar(value="3")
        self.stage_points_combo = ttk.Combobox(
            round_box,
            textvariable=self.stage_points_var,
            values=[str(i) for i in range(0, MAX_STAGE_POINTS + 1)],
            state="readonly",
            width=6,
        )
        self.stage_points_combo.grid(row=1, column=1, sticky="w", padx=8, pady=(10, 0))

        ttk.Label(round_box, text="Bug-finder team(s) (+1 each):").grid(row=2, column=0, sticky="nw", pady=(10, 0))
        self.bug_list = tk.Listbox(round_box, selectmode="multiple", height=6, exportselection=False)
        for t in self.state_data["teams"]:
            self.bug_list.insert("end", t)
        self.bug_list.grid(row=2, column=1, sticky="ew", padx=8, pady=(10, 0))

        ttk.Label(round_box, text="Note (optional):").grid(row=3, column=0, sticky="w", pady=(10, 0))
        self.note_var = tk.StringVar(value="")
        ttk.Entry(round_box, textvariable=self.note_var).grid(row=3, column=1, sticky="ew", padx=8, pady=(10, 0))

        btns = ttk.Frame(left)
        btns.grid(row=3, column=0, sticky="ew", pady=(12, 0))
        btns.columnconfigure(0, weight=2)
        btns.columnconfigure(1, weight=1)
        btns.columnconfigure(2, weight=1)
        btns.columnconfigure(3, weight=1)

        ttk.Button(btns, text="Finalize Round & Next", command=self.finalize_round_and_next).grid(row=0, column=0, sticky="ew", padx=4)
        ttk.Button(btns, text="Run Grader", command=self.run_stage_grader).grid(row=0, column=1, sticky="ew", padx=4)
        ttk.Button(btns, text="Undo Last Round", command=self.undo_last_round).grid(row=0, column=2, sticky="ew", padx=4)
        ttk.Button(btns, text="Finalize Session", command=self.finalize_session).grid(row=0, column=3, sticky="ew", padx=4)

        session_box = ttk.LabelFrame(left, text="Session", padding=10)
        session_box.grid(row=4, column=0, sticky="ew", pady=(12, 0))
        session_box.columnconfigure(0, weight=1)
        session_box.columnconfigure(1, weight=1)

        ttk.Button(session_box, text="New Session (reset scores & log)", command=self.new_session).grid(row=0, column=0, sticky="ew", padx=4)
        ttk.Button(session_box, text="Show state file path", command=self.show_state_location).grid(row=0, column=1, sticky="ew", padx=4)

        img_box = ttk.LabelFrame(left, text="Battle Spirit", padding=6)
        img_box.grid(row=5, column=0, sticky="ew", pady=(12, 0))
        img_box.columnconfigure(0, weight=1)

        self.img_label = ttk.Label(img_box)
        self.img_label.grid(row=0, column=0, sticky="ew")
        self.load_and_set_image()

        score_box = ttk.LabelFrame(right, text="Scoreboard (live)", padding=10)
        score_box.grid(row=0, column=0, sticky="ew")
        score_box.columnconfigure(0, weight=1)

        self.score_tree = ttk.Treeview(score_box, columns=("team", "score"), show="headings", height=8)
        self.score_tree.heading("team", text="Team")
        self.score_tree.heading("score", text="Score")
        self.score_tree.column("team", width=240, anchor="w", stretch=False)
        self.score_tree.column("score", width=90, anchor="center", stretch=False)
        self.score_tree.grid(row=0, column=0, sticky="ew")

        log_box = ttk.LabelFrame(right, text="Round Log (one row per round)", padding=10)
        log_box.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        log_box.rowconfigure(0, weight=1)
        log_box.columnconfigure(0, weight=1)

        self.log_tree = ttk.Treeview(
            log_box,
            columns=("idx", "exercise", "stage", "stage_pts", "bug_teams", "note"),
            show="headings",
        )
        for col, title, w, stretch in [
            ("idx", "#", 50, False),
            ("exercise", "Exercise", 260, False),
            ("stage", "Stage Team", 170, False),
            ("stage_pts", "Stage Pts", 80, False),
            ("bug_teams", "Bug Finder Teams (+1 each)", 340, True),
            ("note", "Note", 220, True),
        ]:
            self.log_tree.heading(col, text=title)
            self.log_tree.column(col, width=w, anchor="w" if col in ("exercise", "stage", "bug_teams", "note") else "center", stretch=stretch)

        self.log_tree.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(log_box, orient="vertical", command=self.log_tree.yview)
        self.log_tree.configure(yscrollcommand=scroll.set)
        scroll.grid(row=0, column=1, sticky="ns")

    def load_and_set_image(self):
        app_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = None

        for c in GREEK_IMAGE_CANDIDATES:
            candidate = os.path.join(app_dir, c) if not os.path.isabs(c) else c
            if os.path.exists(candidate):
                img_path = candidate
                break

        if img_path is None:
            self.img_label.configure(text="(put greek_battle.png in this folder to show image)")
            return

        try:
            img = tk.PhotoImage(file=img_path)
            img = img.subsample(3, 3)
            self.greeks_photo = img
            self.img_label.configure(image=self.greeks_photo)
        except Exception:
            self.img_label.configure(text="(could not load image; try .gif or .ppm if PNG fails)")


def main():
    app = App()
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")
    except Exception:
        pass
    app.mainloop()


if __name__ == "__main__":
    main()