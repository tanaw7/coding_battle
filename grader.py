"""
ICCS102 Stage Grader (single file: stage.py)

Usage:
    python iccs102_stage_grader.py
    # (Optional) you may pass one argument, but it is ignored:
    # python iccs102_stage_grader.py anything_here

Behavior:
- Reads stage.py in the SAME folder as this grader file
- Detects which exercise is present by matching function name against the known 60 function names
- Grades ONLY the detected exercise
- Produces detailed reasons when incorrect
- Saves JSON report to stage_grading_report.json in the SAME folder as this grader file

Notes:
- stage.py must contain EXACTLY ONE of the expected function names (otherwise AMBIGUOUS).
- This version REMOVES input()/print() rule checks (as requested).
- This version INCLUDES:
  (2) Signature checking (clear "expected N args" message)
  (3) Stronger tests for all 60 exercises
- Import rules:
  - By default: NO imports allowed
  - EX10 allows importing math (and only math)
"""

from __future__ import annotations

import ast
import importlib.util
import inspect
import json
import math
import os
import sys
import traceback
from dataclasses import dataclass, asdict
from typing import Any, Callable, Dict, List, Optional, Tuple

# --- Color helpers (ANSI) ---
RESET = "\x1b[0m"
BOLD = "\x1b[1m"
GREEN = "\x1b[32m"
RED = "\x1b[31m"
YELLOW = "\x1b[33m"


def _enable_vt_mode_windows() -> None:
    """Enable ANSI escape codes on Windows terminal (best effort)."""
    if os.name != "nt":
        return
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE = -11
        mode = ctypes.c_uint()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
    except Exception:
        pass


def _supports_color() -> bool:
    # NO_COLOR standard: https://no-color.org/
    if os.environ.get("NO_COLOR"):
        return False
    return sys.stdout.isatty()


def _c(text: str, color: str) -> str:
    if not _supports_color():
        return text
    return f"{color}{text}{RESET}"


STAGE_FILENAME = "stage.py"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


@dataclass(frozen=True)
class ExerciseSpec:
    ex_num: int
    topic: str
    title: str
    func: str
    expected_args: int
    allowed_imports: Tuple[str, ...] = ()


EXERCISES: List[ExerciseSpec] = [
    ExerciseSpec(1, "A", "Add Two Integers", "add_two", 2),
    ExerciseSpec(2, "A", "Minutes to Seconds", "minutes_to_seconds", 1),
    ExerciseSpec(3, "A", "Average of Two Floats", "average_two", 2),
    ExerciseSpec(4, "A", "Greeting Text", "greet", 1),
    ExerciseSpec(5, "A", "String Length", "string_length", 1),
    ExerciseSpec(6, "A", "Is Positive", "is_positive", 1),
    ExerciseSpec(7, "A", "Percent to Decimal", "percent_to_decimal", 1),
    ExerciseSpec(8, "A", "Decimal to Percent", "decimal_to_percent", 1),
    ExerciseSpec(9, "A", "Quotient and Remainder", "divmod_pair", 2),
    ExerciseSpec(10, "A", "Degrees to Radians", "degrees_to_radians", 1, allowed_imports=("math",)),

    ExerciseSpec(11, "B", "Is Odd", "is_odd", 1),
    ExerciseSpec(12, "B", "Compare Two Numbers", "compare_two", 2),
    ExerciseSpec(13, "B", "Bigger of Two", "bigger", 2),
    ExerciseSpec(14, "B", "Letter Grade", "grade_letter", 1),
    ExerciseSpec(15, "B", "Between (Inclusive)", "between_inclusive", 3),
    ExerciseSpec(16, "B", "Ticket Price", "ticket_price", 1),
    ExerciseSpec(17, "B", "Safe Division", "safe_divide", 2),
    ExerciseSpec(18, "B", "Is Vowel", "is_vowel", 1),
    ExerciseSpec(19, "B", "Median of Three Integers", "median_of_three", 3),
    ExerciseSpec(20, "B", "Sign of Number", "sign", 1),

    ExerciseSpec(21, "C", "Sum of a List", "sum_list", 1),
    ExerciseSpec(22, "C", "Count Greater Than", "count_greater_than", 2),
    ExerciseSpec(23, "C", "First Divisible by k", "first_divisible", 2),
    ExerciseSpec(24, "C", "Count Consonants", "count_consonants", 1),
    ExerciseSpec(25, "C", "Squares from 1 to n", "squares_1_to_n", 1),
    ExerciseSpec(26, "C", "Cumulative Maximum", "cumulative_max", 1),
    ExerciseSpec(27, "C", "Keep Only Even Numbers", "keep_only_evens", 1),
    ExerciseSpec(28, "C", "Dash Join Words", "dash_join", 1),
    ExerciseSpec(29, "C", "Count Occurrences", "count_occurrences", 2),
    ExerciseSpec(30, "C", "Minimum in List", "min_in_list", 1),

    ExerciseSpec(31, "D", "Countdown List", "countdown_list", 1),
    ExerciseSpec(32, "D", "Sum Until Zero", "sum_until_zero", 1),
    ExerciseSpec(33, "D", "Count Digits", "count_digits", 1),
    ExerciseSpec(34, "D", "Reverse Number", "reverse_number", 1),
    ExerciseSpec(35, "D", "Multiply by Repeated Addition", "multiply_repeat", 2),
    ExerciseSpec(36, "D", "Power by Repeated Multiplication", "power_loop", 2),
    ExerciseSpec(37, "D", "Double Until Target", "double_until", 1),
    ExerciseSpec(38, "D", "Last Index", "last_index", 2),
    ExerciseSpec(39, "D", "Remove Leading Zeros", "remove_leading_zeros", 1),
    ExerciseSpec(40, "D", "Repeat Text", "repeat_text", 2),

    ExerciseSpec(41, "E", "Last Element", "last_element", 1),
    ExerciseSpec(42, "E", "First Two Elements (safe)", "first_two", 1),
    ExerciseSpec(43, "E", "Swap First and Last", "swap_first_last", 1),
    ExerciseSpec(44, "E", "Count Above Average", "count_above_average", 1),
    ExerciseSpec(45, "E", "Remove All Occurrences", "remove_all", 2),
    ExerciseSpec(46, "E", "Append (Return New)", "append_new", 2),
    ExerciseSpec(47, "E", "Flatten One Level", "flatten", 1),
    ExerciseSpec(48, "E", "Rotate Left by k", "rotate_left", 2),
    ExerciseSpec(49, "E", "Is Sorted (Ascending)", "is_sorted", 1),
    ExerciseSpec(50, "E", "Has Duplicates", "has_duplicates", 1),

    ExerciseSpec(51, "F", "Frequency Dictionary (Numbers)", "frequency", 1),
    ExerciseSpec(52, "F", "Character Frequency (Ignore Spaces)", "char_frequency_no_spaces", 1),
    ExerciseSpec(53, "F", "Get With Default", "get_with_default", 3),
    ExerciseSpec(54, "F", "Sum of Dictionary Values", "sum_dict_values", 1),
    ExerciseSpec(55, "F", "Most Frequent Number", "most_frequent_number", 1),
    ExerciseSpec(56, "F", "Merge Counts", "merge_counts", 2),
    ExerciseSpec(57, "F", "Word Count", "word_count", 1),
    ExerciseSpec(58, "F", "Keys With Count At Least k", "keys_at_least", 2),
    ExerciseSpec(59, "F", "Invert Dictionary (Unique Values)", "invert_unique", 1),
    ExerciseSpec(60, "F", "Histogram Bars", "histogram", 1),
]

FUNC_TO_SPEC: Dict[str, ExerciseSpec] = {e.func: e for e in EXERCISES}


@dataclass
class GradeReport:
    detected_function: Optional[str]
    detected_exercise: Optional[int]
    status: str            # PASS/FAIL/MISSING/AMBIGUOUS
    points: int            # 1 if PASS else 0
    file_used: str
    reasons: List[str]
    warnings: List[str]


# ----------------------------
# Helpers
# ----------------------------

def _safe_repr(x: Any, max_len: int = 200) -> str:
    try:
        s = repr(x)
    except Exception:
        s = f"<unreprable {type(x).__name__}>"
    if len(s) > max_len:
        s = s[: max_len - 3] + "..."
    return s


def _float_close(a: float, b: float, tol: float = 1e-9) -> bool:
    return abs(a - b) <= tol


def _assert_equal(actual: Any, expected: Any, label: str, reasons: List[str]) -> None:
    if actual != expected:
        reasons.append(f"{label}: expected {_safe_repr(expected)} but got {_safe_repr(actual)}")


def _assert_float(actual: Any, expected: float, label: str, reasons: List[str], tol: float = 1e-6) -> None:
    if not isinstance(actual, (int, float)):
        reasons.append(f"{label}: expected a number (int/float) but got {type(actual).__name__}")
        return
    if not _float_close(float(actual), float(expected), tol=tol):
        reasons.append(f"{label}: expected approximately {expected} but got {actual} (tol={tol})")


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _ast_import_checks(source: str, spec: ExerciseSpec) -> List[str]:
    """
    Returns fatal reasons if imports violate allowed_imports.
    (No print/input checks in this version.)
    """
    fatal: List[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        fatal.append(f"SyntaxError: {e.msg} at line {e.lineno}, column {e.offset}")
        return fatal

    allowed = set(spec.allowed_imports)
    imported: List[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.append(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported.append(node.module.split(".")[0])

    imported = list(dict.fromkeys(imported))

    if allowed:
        for m in imported:
            if m not in allowed:
                fatal.append(f"Rule violation: unexpected import '{m}'. Allowed: {sorted(allowed)}")
    else:
        if imported:
            fatal.append(f"Rule violation: imports are not allowed here, but found: {imported}")

    return fatal


def _load_module_from_path(path: str) -> Tuple[Optional[Any], Optional[str]]:
    try:
        module_name = "stage_" + str(abs(hash(path))).replace("-", "_")
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            return None, "Could not load module spec."
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore[attr-defined]
        return mod, None
    except Exception:
        return None, traceback.format_exc(limit=5)


def detect_function_in_stage(source: str) -> Tuple[Optional[str], List[str]]:
    """
    Returns (detected_func, all_detected_funcs_that_match_exercises).
    If exactly 1 match, detected_func is that match.
    If 0 or >1 matches, detected_func is None.
    """
    try:
        tree = ast.parse(source)
    except Exception:
        return None, []

    found: List[str] = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in FUNC_TO_SPEC:
            found.append(node.name)

    found = list(dict.fromkeys(found))
    if len(found) == 1:
        return found[0], found
    return None, found


def check_signature(fn: Callable[..., Any], expected_args: int, func_name: str) -> Optional[str]:
    """
    Returns an error string if signature clearly does not support expected_args positional args.
    Otherwise returns None.
    """
    try:
        sig = inspect.signature(fn)
    except Exception:
        return None

    params = list(sig.parameters.values())
    empty = inspect.Parameter.empty

    kwonly_required = [
        p.name for p in params
        if p.kind == inspect.Parameter.KEYWORD_ONLY and p.default is empty
    ]
    if kwonly_required:
        return (
            f"Function signature issue: '{func_name}' has required keyword-only parameter(s) "
            f"{kwonly_required}. Expected {expected_args} normal positional parameter(s)."
        )

    positional = [
        p for p in params
        if p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    ]
    has_varargs = any(p.kind == inspect.Parameter.VAR_POSITIONAL for p in params)

    required_positional = sum(1 for p in positional if p.default is empty)
    max_positional = float("inf") if has_varargs else len(positional)

    if expected_args < required_positional or expected_args > max_positional:
        max_text = "infinite (*args)" if max_positional == float("inf") else str(int(max_positional))
        return (
            f"Function signature issue: expected {expected_args} parameter(s), "
            f"but your function requires at least {required_positional} and allows at most {max_text} positional args."
        )

    return None


# ----------------------------
# Strong tests for all 60
# ----------------------------

def run_tests(spec: ExerciseSpec, func: Callable[..., Any], reasons: List[str]) -> None:
    f = func
    n = spec.ex_num

    try:
        # A
        if n == 1:
            _assert_equal(f(3, 5), 8, "add_two(3,5)", reasons)
            _assert_equal(f(-2, 10), 8, "add_two(-2,10)", reasons)
            _assert_equal(f(0, 0), 0, "add_two(0,0)", reasons)

        elif n == 2:
            _assert_equal(f(2), 120, "minutes_to_seconds(2)", reasons)
            _assert_equal(f(0), 0, "minutes_to_seconds(0)", reasons)
            _assert_equal(f(1), 60, "minutes_to_seconds(1)", reasons)

        elif n == 3:
            _assert_float(f(2.0, 4.0), 3.0, "average_two(2.0,4.0)", reasons)
            _assert_float(f(1.5, 2.5), 2.0, "average_two(1.5,2.5)", reasons)
            _assert_float(f(-1.0, 1.0), 0.0, "average_two(-1.0,1.0)", reasons)

        elif n == 4:
            _assert_equal(f("Mina"), "Hello, Mina!", 'greet("Mina")', reasons)
            _assert_equal(f(""), "Hello, !", 'greet("")', reasons)
            _assert_equal(f("A"), "Hello, A!", 'greet("A")', reasons)

        elif n == 5:
            _assert_equal(f("abc"), 3, 'string_length("abc")', reasons)
            _assert_equal(f(""), 0, 'string_length("")', reasons)
            _assert_equal(f("a b"), 3, 'string_length("a b")', reasons)

        elif n == 6:
            _assert_equal(f(5), True, "is_positive(5)", reasons)
            _assert_equal(f(0), False, "is_positive(0)", reasons)
            _assert_equal(f(-1), False, "is_positive(-1)", reasons)

        elif n == 7:
            _assert_float(f(25.0), 0.25, "percent_to_decimal(25.0)", reasons)
            _assert_float(f(5.0), 0.05, "percent_to_decimal(5.0)", reasons)
            _assert_float(f(0.0), 0.0, "percent_to_decimal(0.0)", reasons)

        elif n == 8:
            _assert_float(f(0.25), 25.0, "decimal_to_percent(0.25)", reasons)
            _assert_float(f(0.05), 5.0, "decimal_to_percent(0.05)", reasons)
            _assert_float(f(0.0), 0.0, "decimal_to_percent(0.0)", reasons)

        elif n == 9:
            _assert_equal(f(17, 5), (3, 2), "divmod_pair(17,5)", reasons)
            _assert_equal(f(10, 2), (5, 0), "divmod_pair(10,2)", reasons)
            _assert_equal(f(0, 3), (0, 0), "divmod_pair(0,3)", reasons)

        elif n == 10:
            _assert_float(f(180.0), math.pi, "degrees_to_radians(180.0)", reasons, tol=1e-6)
            _assert_float(f(90.0), math.pi / 2, "degrees_to_radians(90.0)", reasons, tol=1e-6)
            _assert_float(f(0.0), 0.0, "degrees_to_radians(0.0)", reasons, tol=1e-9)

        # B
        elif n == 11:
            _assert_equal(f(7), True, "is_odd(7)", reasons)
            _assert_equal(f(6), False, "is_odd(6)", reasons)
            _assert_equal(f(-3), True, "is_odd(-3)", reasons)

        elif n == 12:
            _assert_equal(f(5, 2), "greater", "compare_two(5,2)", reasons)
            _assert_equal(f(3, 3), "equal", "compare_two(3,3)", reasons)
            _assert_equal(f(-1, 2), "less", "compare_two(-1,2)", reasons)

        elif n == 13:
            _assert_equal(f(3, 10), 10, "bigger(3,10)", reasons)
            _assert_equal(f(5, 5), 5, "bigger(5,5)", reasons)
            _assert_equal(f(-1, -2), -1, "bigger(-1,-2)", reasons)

        elif n == 14:
            _assert_equal(f(83), "A", "grade_letter(83)", reasons)
            _assert_equal(f(49), "F", "grade_letter(49)", reasons)
            _assert_equal(f(79), "B", "grade_letter(79)", reasons)
            _assert_equal(f(80), "A", "grade_letter(80)", reasons)
            _assert_equal(f(50), "D", "grade_letter(50)", reasons)

        elif n == 15:
            _assert_equal(f(5, 0, 10), True, "between_inclusive(5,0,10)", reasons)
            _assert_equal(f(-1, 0, 10), False, "between_inclusive(-1,0,10)", reasons)
            _assert_equal(f(0, 0, 10), True, "between_inclusive(0,0,10)", reasons)
            _assert_equal(f(10, 0, 10), True, "between_inclusive(10,0,10)", reasons)

        elif n == 16:
            _assert_equal(f(10), 50, "ticket_price(10)", reasons)
            _assert_equal(f(12), 100, "ticket_price(12)", reasons)
            _assert_equal(f(59), 100, "ticket_price(59)", reasons)
            _assert_equal(f(60), 70, "ticket_price(60)", reasons)

        elif n == 17:
            _assert_equal(f(10, 2), 5.0, "safe_divide(10,2)", reasons)
            _assert_equal(f(10, 0), None, "safe_divide(10,0)", reasons)
            _assert_equal(f(0, 5), 0.0, "safe_divide(0,5)", reasons)

        elif n == 18:
            _assert_equal(f("A"), True, 'is_vowel("A")', reasons)
            _assert_equal(f("b"), False, 'is_vowel("b")', reasons)
            _assert_equal(f("u"), True, 'is_vowel("u")', reasons)

        elif n == 19:
            _assert_equal(f(1, 9, 3), 3, "median_of_three(1,9,3)", reasons)
            _assert_equal(f(5, 5, 1), 5, "median_of_three(5,5,1)", reasons)
            _assert_equal(f(2, 3, 1), 2, "median_of_three(2,3,1)", reasons)

        elif n == 20:
            _assert_equal(f(5), "positive", "sign(5)", reasons)
            _assert_equal(f(0), "zero", "sign(0)", reasons)
            _assert_equal(f(-2), "negative", "sign(-2)", reasons)

        # C
        elif n == 21:
            _assert_equal(f([1, 3, 2, 5]), 11, "sum_list([1,3,2,5])", reasons)
            _assert_equal(f([]), 0, "sum_list([])", reasons)
            _assert_equal(f([0, 0]), 0, "sum_list([0,0])", reasons)

        elif n == 22:
            _assert_equal(f([1, 5, 7, 2, 7], 4), 3, "count_greater_than([..],4)", reasons)
            _assert_equal(f([], 10), 0, "count_greater_than([],10)", reasons)
            _assert_equal(f([4, 5, 6], 6), 0, "count_greater_than([4,5,6],6)", reasons)

        elif n == 23:
            _assert_equal(f([5, 7, 9, 10], 3), 9, "first_divisible([..],3)", reasons)
            _assert_equal(f([5, 7], 2), None, "first_divisible([5,7],2)", reasons)
            _assert_equal(f([2, 4, 6], 2), 2, "first_divisible([2,4,6],2)", reasons)

        elif n == 24:
            _assert_equal(f("Hello World"), 7, 'count_consonants("Hello World")', reasons)
            _assert_equal(f("AEIOU"), 0, 'count_consonants("AEIOU")', reasons)
            _assert_equal(f("123!!"), 0, 'count_consonants("123!!")', reasons)
            _assert_equal(f("bcd XYZ"), 6, 'count_consonants("bcd XYZ")', reasons)

        elif n == 25:
            _assert_equal(f(5), [1, 4, 9, 16, 25], "squares_1_to_n(5)", reasons)
            _assert_equal(f(1), [1], "squares_1_to_n(1)", reasons)

        elif n == 26:
            _assert_equal(f([2, 1, 3, 0, 5]), [2, 2, 3, 3, 5], "cumulative_max([..])", reasons)
            _assert_equal(f([]), [], "cumulative_max([])", reasons)

        elif n == 27:
            _assert_equal(f([3, 4, 0, 7, 8, 9]), [4, 0, 8], "keep_only_evens([..])", reasons)
            _assert_equal(f([]), [], "keep_only_evens([])", reasons)
            _assert_equal(f([1, 3, 5]), [], "keep_only_evens([1,3,5])", reasons)

        elif n == 28:
            _assert_equal(f(["coding", "for", "all"]), "coding-for-all", "dash_join([...])", reasons)
            _assert_equal(f([]), "", "dash_join([])", reasons)
            _assert_equal(f(["a"]), "a", 'dash_join(["a"])', reasons)

        elif n == 29:
            _assert_equal(f([1, 2, 1, 1, 3], 1), 3, "count_occurrences([..],1)", reasons)
            _assert_equal(f([], 7), 0, "count_occurrences([],7)", reasons)
            _assert_equal(f([2, 2, 2], 1), 0, "count_occurrences([2,2,2],1)", reasons)

        elif n == 30:
            _assert_equal(f([5, 2, 9, -1, 3]), -1, "min_in_list([..])", reasons)

        # D
        elif n == 31:
            _assert_equal(f(5), [5, 4, 3, 2, 1, 0], "countdown_list(5)", reasons)
            _assert_equal(f(0), [0], "countdown_list(0)", reasons)

        elif n == 32:
            _assert_equal(f([3, 4, 2, 0, 100]), 9, "sum_until_zero([3,4,2,0,100])", reasons)
            _assert_equal(f([0, 5]), 0, "sum_until_zero([0,5])", reasons)
            _assert_equal(f([1, 2, 3]), 6, "sum_until_zero([1,2,3]) (no zero)", reasons)

        elif n == 33:
            _assert_equal(f(0), 1, "count_digits(0)", reasons)
            _assert_equal(f(12345), 5, "count_digits(12345)", reasons)
            _assert_equal(f(7), 1, "count_digits(7)", reasons)

        elif n == 34:
            _assert_equal(f(120), 21, "reverse_number(120)", reasons)
            _assert_equal(f(7), 7, "reverse_number(7)", reasons)
            _assert_equal(f(1000), 1, "reverse_number(1000)", reasons)

        elif n == 35:
            _assert_equal(f(3, 4), 12, "multiply_repeat(3,4)", reasons)
            _assert_equal(f(5, 0), 0, "multiply_repeat(5,0)", reasons)
            _assert_equal(f(-2, 3), -6, "multiply_repeat(-2,3)", reasons)

        elif n == 36:
            _assert_equal(f(2, 5), 32, "power_loop(2,5)", reasons)
            _assert_equal(f(3, 0), 1, "power_loop(3,0)", reasons)
            _assert_equal(f(5, 1), 5, "power_loop(5,1)", reasons)

        elif n == 37:
            _assert_equal(f(9), 16, "double_until(9)", reasons)
            _assert_equal(f(1), 1, "double_until(1)", reasons)
            _assert_equal(f(16), 16, "double_until(16)", reasons)

        elif n == 38:
            _assert_equal(f([5, 3, 5, 2, 5], 5), 4, "last_index([..],5)", reasons)
            _assert_equal(f([5, 3, 5, 2, 5], 9), -1, "last_index([..],9)", reasons)
            _assert_equal(f([], 1), -1, "last_index([],1)", reasons)

        elif n == 39:
            _assert_equal(f("000123"), "123", "remove_leading_zeros('000123')", reasons)
            _assert_equal(f("0000"), "0", "remove_leading_zeros('0000')", reasons)
            _assert_equal(f("5"), "5", "remove_leading_zeros('5')", reasons)

        elif n == 40:
            _assert_equal(f("ha", 3), "hahaha", "repeat_text('ha',3)", reasons)
            _assert_equal(f("x", 0), "", "repeat_text('x',0)", reasons)
            _assert_equal(f("", 5), "", "repeat_text('',5)", reasons)

        # E
        elif n == 41:
            _assert_equal(f([3, 1, 9]), 9, "last_element([3,1,9])", reasons)
            _assert_equal(f([7]), 7, "last_element([7])", reasons)

        elif n == 42:
            _assert_equal(f([1, 2, 3, 4]), [1, 2], "first_two([1,2,3,4])", reasons)
            _assert_equal(f([9]), [9], "first_two([9])", reasons)
            _assert_equal(f([]), [], "first_two([])", reasons)

        elif n == 43:
            _assert_equal(f([1, 2, 3, 4]), [4, 2, 3, 1], "swap_first_last([..])", reasons)
            _assert_equal(f([9, 8]), [8, 9], "swap_first_last([9,8])", reasons)

        elif n == 44:
            _assert_equal(f([1, 2, 3, 4, 10]), 1, "count_above_average([..])", reasons)
            _assert_equal(f([5, 5, 5]), 0, "count_above_average([5,5,5])", reasons)

        elif n == 45:
            _assert_equal(f([1, 2, 1, 3, 1], 1), [2, 3], "remove_all([..],1)", reasons)
            _assert_equal(f([1, 2, 3], 9), [1, 2, 3], "remove_all([1,2,3],9)", reasons)

        elif n == 46:
            nums = [1, 2]
            out = f(nums, 9)
            _assert_equal(out, [1, 2, 9], "append_new([1,2],9)", reasons)
            if nums != [1, 2]:
                reasons.append("append_new: should NOT mutate the original list, but it changed.")

        elif n == 47:
            _assert_equal(f([[1, 2], [3], [4, 5]]), [1, 2, 3, 4, 5], "flatten([[..]])", reasons)
            _assert_equal(f([[], [1], []]), [1], "flatten([[],[1],[]])", reasons)

        elif n == 48:
            _assert_equal(f([1, 2, 3, 4, 5], 2), [3, 4, 5, 1, 2], "rotate_left([1..5],2)", reasons)
            _assert_equal(f([1, 2, 3], 5), [3, 1, 2], "rotate_left([1,2,3],5)", reasons)
            _assert_equal(f([], 3), [], "rotate_left([],3)", reasons)

        elif n == 49:
            _assert_equal(f([1, 2, 2, 5]), True, "is_sorted([1,2,2,5])", reasons)
            _assert_equal(f([3, 2, 1]), False, "is_sorted([3,2,1])", reasons)
            _assert_equal(f([]), True, "is_sorted([]) (empty is sorted)", reasons)

        elif n == 50:
            _assert_equal(f([1, 2, 3, 2]), True, "has_duplicates([..])", reasons)
            _assert_equal(f([1, 2, 3]), False, "has_duplicates([1,2,3])", reasons)
            _assert_equal(f([]), False, "has_duplicates([])", reasons)

        # F
        elif n == 51:
            _assert_equal(f([2, 2, 5, 2, 5]), {2: 3, 5: 2}, "frequency([..])", reasons)
            _assert_equal(f([]), {}, "frequency([])", reasons)

        elif n == 52:
            _assert_equal(f("a b a c"), {"a": 2, "b": 1, "c": 1}, "char_frequency_no_spaces('a b a c')", reasons)
            _assert_equal(f("   "), {}, "char_frequency_no_spaces('   ')", reasons)

        elif n == 53:
            _assert_equal(f({"a": 3}, "a", 0), 3, "get_with_default({'a':3},'a',0)", reasons)
            _assert_equal(f({"a": 3}, "b", 0), 0, "get_with_default({'a':3},'b',0)", reasons)

        elif n == 54:
            _assert_equal(f({"a": 2, "b": 5}), 7, "sum_dict_values({'a':2,'b':5})", reasons)
            _assert_equal(f({}), 0, "sum_dict_values({})", reasons)

        elif n == 55:
            _assert_equal(f([2, 2, 3, 3, 3, 1, 1]), 3, "most_frequent_number([...])", reasons)
            _assert_equal(f([4, 4, 5, 5]), 4, "most_frequent_number([4,4,5,5]) tie->smaller", reasons)
            _assert_equal(f([9]), 9, "most_frequent_number([9])", reasons)

        elif n == 56:
            _assert_equal(f({"a": 2}, {"a": 1, "b": 3}), {"a": 3, "b": 3}, "merge_counts({...})", reasons)
            _assert_equal(f({}, {"x": 1}), {"x": 1}, "merge_counts({}, {'x':1})", reasons)

        elif n == 57:
            _assert_equal(f("hi hi bye"), {"hi": 2, "bye": 1}, "word_count('hi hi bye')", reasons)
            _assert_equal(f("  a   a "), {"a": 2}, "word_count('  a   a ')", reasons)

        elif n == 58:
            _assert_equal(f({"a": 2, "b": 5, "c": 1}, 2), ["a", "b"], "keys_at_least({...},2)", reasons)
            _assert_equal(f({"b": 1}, 2), [], "keys_at_least({'b':1},2)", reasons)

        elif n == 59:
            _assert_equal(f({"a": 1, "b": 2}), {1: "a", 2: "b"}, "invert_unique({'a':1,'b':2})", reasons)
            _assert_equal(f({}), {}, "invert_unique({})", reasons)

        elif n == 60:
            _assert_equal(f([2, 2, 5, 5, 5]), {2: "**", 5: "***"}, "histogram([..])", reasons)
            _assert_equal(f([]), {}, "histogram([])", reasons)

    except Exception:
        reasons.append("Exception while running tests:\n" + traceback.format_exc(limit=3))


# ----------------------------
# Main grading
# ----------------------------

def grade_stage_file() -> GradeReport:
    file_path = os.path.join(SCRIPT_DIR, STAGE_FILENAME)
    reasons: List[str] = []
    warnings: List[str] = []

    if not os.path.isfile(file_path):
        return GradeReport(
            detected_function=None,
            detected_exercise=None,
            status="MISSING",
            points=0,
            file_used=file_path,
            reasons=[f"Missing file: expected '{STAGE_FILENAME}' next to the grader (same folder)."],
            warnings=[],
        )

    source = _read_text(file_path)
    detected_func, matches = detect_function_in_stage(source)

    if matches and detected_func is None:
        return GradeReport(
            detected_function=None,
            detected_exercise=None,
            status="AMBIGUOUS",
            points=0,
            file_used=file_path,
            reasons=[
                "More than one known exercise function was found in stage.py.",
                f"Found: {matches}",
                "stage.py must contain exactly ONE of the expected function names."
            ],
            warnings=[]
        )

    if not matches:
        return GradeReport(
            detected_function=None,
            detected_exercise=None,
            status="MISSING",
            points=0,
            file_used=file_path,
            reasons=[
                "No known exercise function name was found in stage.py.",
                "Make sure stage.py defines exactly one of the required functions (e.g., add_two, safe_divide, etc.)."
            ],
            warnings=[]
        )

    spec = FUNC_TO_SPEC[detected_func]

    # Import checks only (no print/input checks)
    reasons.extend(_ast_import_checks(source, spec))

    # Import stage.py
    mod, err = _load_module_from_path(file_path)
    if err is not None or mod is None:
        reasons.append("Could not import stage.py (runtime error on import).")
        reasons.append(err if err else "(unknown import error)")
        return GradeReport(
            detected_function=detected_func,
            detected_exercise=spec.ex_num,
            status="FAIL",
            points=0,
            file_used=file_path,
            reasons=reasons,
            warnings=warnings,
        )

    fn_obj = getattr(mod, detected_func, None)
    if fn_obj is None or not callable(fn_obj):
        reasons.append(f"Function '{detected_func}' not found or not callable after import.")
        return GradeReport(
            detected_function=detected_func,
            detected_exercise=spec.ex_num,
            status="FAIL",
            points=0,
            file_used=file_path,
            reasons=reasons,
            warnings=warnings,
        )

    sig_issue = check_signature(fn_obj, spec.expected_args, detected_func)
    if sig_issue:
        reasons.append(sig_issue)

    run_tests(spec, fn_obj, reasons)

    status = "PASS" if not reasons else "FAIL"
    points = 1 if status == "PASS" else 0

    return GradeReport(
        detected_function=detected_func,
        detected_exercise=spec.ex_num,
        status=status,
        points=points,
        file_used=file_path,
        reasons=reasons,
        warnings=warnings,
    )


def print_report(r: GradeReport) -> None:
    _enable_vt_mode_windows()

    print("=" * 72)
    print(_c("ICCS102 Stage Grader (stage.py)", BOLD))
    print("=" * 72)
    print(f"File: {r.file_used}")
    print(f"Detected: {r.detected_function} (Exercise {r.detected_exercise})")

    status_line = f"{r.status} [{r.points}/1]"
    if r.status == "PASS":
        status_line = _c(status_line, BOLD + GREEN)
    else:
        status_line = _c(status_line, BOLD + RED)

    print(f"Result: {status_line}")
    print()

    if r.warnings:
        print(_c("Warnings:", BOLD + YELLOW))
        for w in r.warnings:
            print(_c(f"  - {w}", YELLOW))
        print()

    if r.reasons:
        print(_c("Issues:", BOLD + RED))
        for reason in r.reasons:
            lines = str(reason).splitlines()
            print(_c(f"  - {lines[0]}", RED))
            for extra in lines[1:]:
                print(_c(f"    {extra}", RED))
    else:
        print(_c("No issues found.", GREEN))


def main() -> int:
    # We allow 0 or 1 argument for compatibility with tools that call it with a folder.
    if len(sys.argv) > 2:
        print("Usage: python iccs102_stage_grader.py")
        return 2

    report = grade_stage_file()
    print_report(report)

    out_json = os.path.join(SCRIPT_DIR, "stage_grading_report.json")
    try:
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(asdict(report), f, indent=2, ensure_ascii=False)
        print(f"\nSaved JSON report to: {out_json}")
    except Exception as e:
        print(f"\nCould not save JSON report: {e}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
