# Fundamental Exercises — Prompts + Solutions + Explanations (1–60)

This document is written **for students**.

## How to use this guide

For each exercise you will see:

- **Prompt** (what the function must do)
- **Solution** (one possible correct implementation)
- **Why it works** (short explanation)
- **Try these tests** (2–3 inputs you can run)

> Reminder: In assignments, **do not use **``** or **`` unless a prompt explicitly says so. Always **return** the result.

---

# Topic A — Types & Basic Expressions (1–10)

## 1) Add Two Integers

### Prompt

Write a function `add_two(a: int, b: int) -> int` that returns the sum.

### Solution

```python
def add_two(a: int, b: int) -> int:
    return a + b
```

### Why it works

- `+` adds integers in Python.

### Try these tests

- `add_two(3, 5)  # 8` → normal positive numbers
- `add_two(-2, 10)  # 8` → checks negative + positive
- `add_two(0, 0)  # 0` → checks the “do nothing” case

---

## 2) Minutes to Seconds

### Prompt

Write `minutes_to_seconds(minutes: int) -> int` that converts minutes to seconds.

### Solution

```python
def minutes_to_seconds(minutes: int) -> int:
    return minutes * 60
```

### Why it works

- 1 minute = 60 seconds, so multiply by 60.

### Try these tests

- `minutes_to_seconds(2)  # 120` → simple conversion
- `minutes_to_seconds(0)  # 0` → checks zero
- `minutes_to_seconds(15)  # 900` → a bigger normal value

---

## 3) Average of Two Floats

### Prompt

Write `average_two(a: float, b: float) -> float` that returns `(a + b) / 2`.

### Solution

```python
def average_two(a: float, b: float) -> float:
    return (a + b) / 2
```

### Why it works

- Average of two numbers is sum divided by 2.

### Try these tests

- `average_two(2.0, 4.0)  # 3.0` → clean numbers
- `average_two(1.5, 2.5)  # 2.0` → decimals
- `average_two(-2.0, 2.0)  # 0.0` → cancels out

---

## 4) Greeting Text

### Prompt

Write `greet(name: str) -> str` that returns exactly: `"Hello, <name>!"`.

### Solution

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

### Why it works

- f-strings let you insert variables into text.

### Try these tests

- `greet("Mina")  # "Hello, Mina!"` → normal name
- `greet("")  # "Hello, !"` → empty string edge case
- `greet("Dr. Lee")  # "Hello, Dr. Lee!"` → spaces and punctuation

---

## 5) String Length

### Prompt

Write `string_length(s: str) -> int` that returns the number of characters.

### Solution

```python
def string_length(s: str) -> int:
    return len(s)
```

### Why it works

- `len(...)` returns the number of characters in a string.

### Try these tests

- `string_length("abc")  # 3` → normal
- `string_length("")  # 0` → empty string
- `string_length("a b")  # 3` → spaces count too

---

## 6) Is Positive

### Prompt

Write `is_positive(n: int) -> bool` that returns True if `n > 0`.

### Solution

```python
def is_positive(n: int) -> bool:
    return n > 0
```

### Why it works

- Comparisons like `n > 0` produce a boolean (`True`/`False`).

### Try these tests

- `is_positive(5)  # True` → positive
- `is_positive(0)  # False` → boundary
- `is_positive(-1)  # False` → negative

---

## 7) Percent to Decimal

### Prompt

Write `percent_to_decimal(percent: float) -> float`. Example: 25 → 0.25.

### Solution

```python
def percent_to_decimal(percent: float) -> float:
    return percent / 100
```

### Why it works

- “Percent” means “per 100”. Divide by 100 to get decimal.

### Try these tests

- `percent_to_decimal(25.0)  # 0.25` → common
- `percent_to_decimal(5.0)  # 0.05` → small percent
- `percent_to_decimal(0.0)  # 0.0` → zero

---

## 8) Decimal to Percent

### Prompt

Write `decimal_to_percent(decimal: float) -> float`. Example: 0.25 → 25.

### Solution

```python
def decimal_to_percent(decimal: float) -> float:
    return decimal * 100
```

### Why it works

- Reverse of Exercise 7.

### Try these tests

- `decimal_to_percent(0.25)  # 25.0` → common
- `decimal_to_percent(0.05)  # 5.0` → small
- `decimal_to_percent(1.0)  # 100.0` → 100%

---

## 9) Quotient and Remainder

### Prompt

Write `divmod_pair(a: int, b: int) -> tuple[int, int]` returning `(a // b, a % b)`.

### Solution

```python
def divmod_pair(a: int, b: int) -> tuple[int, int]:
    return (a // b, a % b)
```

### Why it works

- `//` gives integer quotient; `%` gives remainder.

### Try these tests

- `divmod_pair(17, 5)  # (3, 2)` → remainder exists
- `divmod_pair(10, 2)  # (5, 0)` → exact division
- `divmod_pair(1, 3)  # (0, 1)` → quotient can be 0

---

## 10) Degrees to Radians (Use math.pi)

### Prompt

Write `degrees_to_radians(degrees: float) -> float` using `degrees * pi / 180`.

### Solution

```python
import math

def degrees_to_radians(degrees: float) -> float:
    return degrees * math.pi / 180
```

### Why it works

- Uses the standard conversion formula.
- `math.pi` is a good accurate value of π.

### Try these tests

- `degrees_to_radians(180.0)` → about `3.14159...` (half-turn)
- `degrees_to_radians(90.0)` → about `1.57079...` (quarter-turn)
- `degrees_to_radians(0.0)` → `0.0` (no rotation)

---

# Topic B — Conditions (11–20)

## 11) Is Odd

### Prompt

Write `is_odd(n: int) -> bool`.

### Solution

```python
def is_odd(n: int) -> bool:
    return n % 2 != 0
```

### Why it works

- Odd numbers do not divide evenly by 2.

### Try these tests

- `is_odd(7)  # True` → odd
- `is_odd(6)  # False` → even
- `is_odd(-3)  # True` → negatives can be odd too

---

## 12) Compare Two Numbers

### Prompt

Write `compare_two(a: float, b: float) -> str` returning `"greater"`, `"less"`, or `"equal"`.

### Solution

```python
def compare_two(a: float, b: float) -> str:
    if a > b:
        return "greater"
    elif a < b:
        return "less"
    else:
        return "equal"
```

### Why it works

- Exactly matches the three possible comparisons.

### Try these tests

- `compare_two(5, 2)  # "greater"` → a > b
- `compare_two(2, 5)  # "less"` → a < b
- `compare_two(3, 3)  # "equal"` → same number

---

## 13) Bigger of Two

### Prompt

Write `bigger(a: float, b: float) -> float`.

### Solution

```python
def bigger(a: float, b: float) -> float:
    if a >= b:
        return a
    return b
```

### Why it works

- If `a` is at least `b`, return `a`; otherwise return `b`.

### Try these tests

- `bigger(3, 10)  # 10` → second bigger
- `bigger(5, 5)  # 5` → equal case
- `bigger(-1, -5)  # -1` → negatives

---

## 14) Letter Grade

### Prompt

Write `grade_letter(score: int) -> str` with ranges A/B/C/D/F.

### Solution

```python
def grade_letter(score: int) -> str:
    if score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"
```

### Why it works

- We check from highest to lowest; the first match returns.

### Try these tests

- `grade_letter(83)  # "A"` → upper range
- `grade_letter(70)  # "B"` → boundary value
- `grade_letter(49)  # "F"` → below passing

---

## 15) Between (Inclusive)

### Prompt

Write `between_inclusive(x: float, low: float, high: float) -> bool`.

### Solution

```python
def between_inclusive(x: float, low: float, high: float) -> bool:
    return low <= x <= high
```

### Why it works

- Python supports chained comparisons.

### Try these tests

- `between_inclusive(5, 0, 10)  # True` → inside
- `between_inclusive(0, 0, 10)  # True` → boundary counts
- `between_inclusive(-1, 0, 10)  # False` → outside

---

## 16) Ticket Price

### Prompt

Write `ticket_price(age: int) -> int` with age rules.

### Solution

```python
def ticket_price(age: int) -> int:
    if age < 12:
        return 50
    elif age < 60:
        return 100
    else:
        return 70
```

### Why it works

- Ages 12–59 fall into the middle case (`age < 60`).

### Try these tests

- `ticket_price(10)  # 50` → child
- `ticket_price(12)  # 100` → boundary
- `ticket_price(60)  # 70` → senior boundary

---

## 17) Safe Division

### Prompt

Write `safe_divide(a: float, b: float) -> float | None`. Return None if b==0.

### Solution

```python
def safe_divide(a: float, b: float) -> float | None:
    if b == 0:
        return None
    return a / b
```

### Why it works

- Division by zero is not allowed, so we return `None` instead.

### Try these tests

- `safe_divide(10, 2)  # 5.0` → normal division
- `safe_divide(10, 0)  # None` → error case handled
- `safe_divide(-9, 3)  # -3.0` → negative result

---

## 18) Is Vowel

### Prompt

Write `is_vowel(ch: str) -> bool`, case-insensitive.

### Solution

```python
def is_vowel(ch: str) -> bool:
    return ch.lower() in "aeiou"
```

### Why it works

- Lowercasing makes it case-insensitive.
- `in` checks membership.

### Try these tests

- `is_vowel("A")  # True` → uppercase
- `is_vowel("b")  # False` → consonant
- `is_vowel("u")  # True` → vowel

---

## 19) Median of Three Integers

### Prompt

Write `median_of_three(a: int, b: int, c: int) -> int`.

### Solution

```python
def median_of_three(a: int, b: int, c: int) -> int:
    xs = [a, b, c]
    xs.sort()
    return xs[1]
```

### Why it works

- Sorting puts values in order, so the middle is index 1.

### Try these tests

- `median_of_three(1, 9, 3)  # 3` → mixed order
- `median_of_three(5, 5, 1)  # 5` → duplicates
- `median_of_three(-1, -5, -3)  # -3` → negatives

---

## 20) Sign of Number

### Prompt

Write `sign(n: int) -> str` returning "positive"/"negative"/"zero".

### Solution

```python
def sign(n: int) -> str:
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    else:
        return "zero"
```

### Why it works

- Exactly matches the three cases.

### Try these tests

- `sign(5)  # "positive"` → positive
- `sign(-2)  # "negative"` → negative
- `sign(0)  # "zero"` → boundary

---

# Topic C — For Loops (21–30)

## 21) Sum of a List

### Prompt

Write `sum_list(nums: list[int]) -> int`. Return 0 for an empty list.

### Solution

```python
def sum_list(nums: list[int]) -> int:
    total = 0
    for x in nums:
        total += x
    return total
```

### Why it works

- We start at 0 and add each number.

### Try these tests

- `sum_list([1, 3, 2, 5])  # 11` → normal list
- `sum_list([])  # 0` → empty list
- `sum_list([-1, 1, -2, 2])  # 0` → positives and negatives cancel

---

## 22) Count Greater Than

### Prompt

Write `count_greater_than(nums: list[int], threshold: int) -> int`.

### Solution

```python
def count_greater_than(nums: list[int], threshold: int) -> int:
    count = 0
    for x in nums:
        if x > threshold:
            count += 1
    return count
```

### Why it works

- We count items that satisfy the condition `x > threshold`.

### Try these tests

- `count_greater_than([1, 5, 7, 2, 7], 4)  # 3` → some pass, some fail
- `count_greater_than([], 10)  # 0` → empty list
- `count_greater_than([5, 5, 5], 5)  # 0` → strict “greater than”

---

## 23) First Divisible by k

### Prompt

Write `first_divisible(nums: list[int], k: int) -> int | None`.

### Solution

```python
def first_divisible(nums: list[int], k: int) -> int | None:
    for x in nums:
        if x % k == 0:
            return x
    return None
```

### Why it works

- Return immediately when you find the first matching item.
- If none match, return `None`.

### Try these tests

- `first_divisible([5, 7, 9, 10], 3)  # 9` → match in the middle
- `first_divisible([5, 7], 2)  # None` → no match
- `first_divisible([6, 9, 12], 3)  # 6` → first item matches

---

## 24) Count Consonants

### Prompt

Write `count_consonants(s: str) -> int` (letters only), case-insensitive. Ignore spaces/non-letters.

### Solution

```python
def count_consonants(s: str) -> int:
    vowels = "aeiou"
    count = 0
    for ch in s.lower():
        if ch.isalpha() and ch not in vowels:
            count += 1
    return count
```

### Why it works

- `lower()` makes checking simpler.
- `isalpha()` ensures we only count letters.
- We count letters that are not vowels.

### Try these tests

- `count_consonants("Hello World")  # 7` → typical phrase
- `count_consonants("AEIOU")  # 0` → only vowels
- `count_consonants("Hi!!")  # 1` → punctuation ignored

---

## 25) Squares from 1 to n

### Prompt

Write `squares_1_to_n(n: int) -> list[int]` for n ≥ 1.

### Solution

```python
def squares_1_to_n(n: int) -> list[int]:
    out: list[int] = []
    for i in range(1, n + 1):
        out.append(i * i)
    return out
```

### Why it works

- `range(1, n+1)` includes n.
- Square is `i*i`.

### Try these tests

- `squares_1_to_n(5)  # [1,4,9,16,25]` → normal
- `squares_1_to_n(1)  # [1]` → smallest valid
- `squares_1_to_n(3)  # [1,4,9]` → short list

---

## 26) Cumulative Maximum

### Prompt

Write `cumulative_max(nums: list[int]) -> list[int]`.

### Solution

```python
def cumulative_max(nums: list[int]) -> list[int]:
    if not nums:
        return []

    out: list[int] = []
    current = nums[0]
    for x in nums:
        if x > current:
            current = x
        out.append(current)
    return out
```

### Why it works

- `current` remembers the biggest value seen so far.
- Each output position stores that current maximum.

### Try these tests

- `cumulative_max([2, 1, 3, 0, 5])  # [2,2,3,3,5]` → rises over time
- `cumulative_max([5, 4, 3])  # [5,5,5]` → never increases
- `cumulative_max([])  # []` → empty list case

---

## 27) Keep Only Even Numbers

### Prompt

Write `keep_only_evens(nums: list[int]) -> list[int]`.

### Solution

```python
def keep_only_evens(nums: list[int]) -> list[int]:
    out: list[int] = []
    for x in nums:
        if x % 2 == 0:
            out.append(x)
    return out
```

### Why it works

- Even numbers have `x % 2 == 0`.

### Try these tests

- `keep_only_evens([3, 4, 0, 7, 8, 9])  # [4,0,8]` → mix
- `keep_only_evens([1, 3, 5])  # []` → none even
- `keep_only_evens([])  # []` → empty list

---

## 28) Dash Join Words

### Prompt

Write `dash_join(words: list[str]) -> str` using `-` between words.

### Solution

```python
def dash_join(words: list[str]) -> str:
    return "-".join(words)
```

### Why it works

- `join` connects list items with the given separator.

### Try these tests

- `dash_join(["coding", "for", "all"])  # "coding-for-all"` → normal
- `dash_join([])  # ""` → empty list becomes empty string
- `dash_join(["a"])  # "a"` → single item has no dashes

---

## 29) Count Occurrences

### Prompt

Write `count_occurrences(nums: list[int], target: int) -> int`.

### Solution

```python
def count_occurrences(nums: list[int], target: int) -> int:
    count = 0
    for x in nums:
        if x == target:
            count += 1
    return count
```

### Why it works

- We count matches where `x == target`.

### Try these tests

- `count_occurrences([1, 2, 1, 1, 3], 1)  # 3` → multiple hits
- `count_occurrences([], 7)  # 0` → empty list
- `count_occurrences([5, 5, 5], 4)  # 0` → no matches

---

## 30) Minimum in List (non-empty)

### Prompt

Write `min_in_list(nums: list[int]) -> int` (assume non-empty).

### Solution

```python
def min_in_list(nums: list[int]) -> int:
    m = nums[0]
    for x in nums[1:]:
        if x < m:
            m = x
    return m
```

### Why it works

- Start from the first value and keep the smallest seen.

### Try these tests

- `min_in_list([5, 2, 9, -1, 3])  # -1` → minimum is negative
- `min_in_list([7])  # 7` → single element
- `min_in_list([2, 2, 2])  # 2` → duplicates

---

# Topic D — While Loops (31–40)

## 31) Countdown List

### Prompt

Write `countdown_list(n: int) -> list[int]` returning `[n, n-1, ..., 0]`.

### Solution

```python
def countdown_list(n: int) -> list[int]:
    out: list[int] = []
    while n >= 0:
        out.append(n)
        n -= 1
    return out
```

### Why it works

- The loop runs until n becomes -1.

### Try these tests

- `countdown_list(5)  # [5,4,3,2,1,0]` → normal
- `countdown_list(0)  # [0]` → smallest
- `countdown_list(1)  # [1,0]` → quick check

---

## 32) Sum Until Zero

### Prompt

Write `sum_until_zero(nums: list[int]) -> int`. Stop when you see 0.

### Solution

```python
def sum_until_zero(nums: list[int]) -> int:
    total = 0
    i = 0
    while i < len(nums) and nums[i] != 0:
        total += nums[i]
        i += 1
    return total
```

### Why it works

- We move index `i` forward until we reach 0 or the end.

### Try these tests

- `sum_until_zero([3, 4, 2, 0, 100])  # 9` → stops at 0
- `sum_until_zero([0, 5])  # 0` → stops immediately
- `sum_until_zero([1, 2, 3])  # 6` → no zero, sums all

---

## 33) Count Digits

### Prompt

Write `count_digits(n: int) -> int` for n ≥ 0. Note: 0 has 1 digit.

### Solution

```python
def count_digits(n: int) -> int:
    if n == 0:
        return 1
    count = 0
    while n > 0:
        count += 1
        n //= 10
    return count
```

### Why it works

- Each `// 10` removes the last digit.

### Try these tests

- `count_digits(0)  # 1` → special case
- `count_digits(12345)  # 5` → normal multi-digit
- `count_digits(9)  # 1` → single digit

---

## 34) Reverse Number

### Prompt

Write `reverse_number(n: int) -> int` for n ≥ 0. Example: 120 → 21.

### Solution

```python
def reverse_number(n: int) -> int:
    rev = 0
    while n > 0:
        digit = n % 10
        rev = rev * 10 + digit
        n //= 10
    return rev
```

### Why it works

- `% 10` takes the last digit.
- `rev * 10 + digit` appends that digit to the end of `rev`.

### Try these tests

- `reverse_number(120)  # 21` → leading zeros disappear
- `reverse_number(7)  # 7` → single digit
- `reverse_number(1000)  # 1` → many trailing zeros

---

## 35) Multiply by Repeated Addition

### Prompt

Write `multiply_repeat(a: int, b: int) -> int` using repeated addition (assume b ≥ 0).

### Solution

```python
def multiply_repeat(a: int, b: int) -> int:
    total = 0
    i = 0
    while i < b:
        total += a
        i += 1
    return total
```

### Why it works

- Adding `a` exactly `b` times equals `a * b`.

### Try these tests

- `multiply_repeat(3, 4)  # 12` → basic
- `multiply_repeat(5, 0)  # 0` → b=0 means add nothing
- `multiply_repeat(-2, 3)  # -6` → negative a

---

## 36) Power by Repeated Multiplication

### Prompt

Write `power_loop(base: int, exp: int) -> int` (assume exp ≥ 0).

### Solution

```python
def power_loop(base: int, exp: int) -> int:
    result = 1
    i = 0
    while i < exp:
        result *= base
        i += 1
    return result
```

### Why it works

- Multiplying base by itself exp times equals base^exp.

### Try these tests

- `power_loop(2, 5)  # 32` → normal
- `power_loop(3, 0)  # 1` → any number power 0 is 1
- `power_loop(-2, 3)  # -8` → odd exponent keeps negative

---

## 37) Double Until Target

### Prompt

Write `double_until(target: int) -> int` starting from 1 and doubling until >= target.

### Solution

```python
def double_until(target: int) -> int:
    value = 1
    while value < target:
        value *= 2
    return value
```

### Why it works

- `value` grows 1, 2, 4, 8, ... until it reaches the target.

### Try these tests

- `double_until(9)  # 16` → passes target
- `double_until(1)  # 1` → already enough
- `double_until(16)  # 16` → exact power of two

---

## 38) Last Index

### Prompt

Write `last_index(nums: list[int], target: int) -> int` returning last index or -1.

### Solution

```python
def last_index(nums: list[int], target: int) -> int:
    i = len(nums) - 1
    while i >= 0:
        if nums[i] == target:
            return i
        i -= 1
    return -1
```

### Why it works

- We search from the end, so the first match is the last index.

### Try these tests

- `last_index([5, 3, 5, 2, 5], 5)  # 4` → multiple matches
- `last_index([1, 2, 3], 9)  # -1` → not found
- `last_index([], 1)  # -1` → empty list

---

## 39) Remove Leading Zeros

### Prompt

Write `remove_leading_zeros(s: str) -> str`. If result is empty, return "0".

### Solution

```python
def remove_leading_zeros(s: str) -> str:
    i = 0
    while i < len(s) and s[i] == "0":
        i += 1
    out = s[i:]
    return out if out != "" else "0"
```

### Why it works

- We move i forward while we see leading '0'.
- Slice from i to the end.

### Try these tests

- `remove_leading_zeros("000123")  # "123"` → normal
- `remove_leading_zeros("0000")  # "0"` → becomes empty
- `remove_leading_zeros("100")  # "100"` → no leading zeros

---

## 40) Repeat Text

### Prompt

Write `repeat_text(text: str, n: int) -> str`.

### Solution

```python
def repeat_text(text: str, n: int) -> str:
    result = ""
    i = 0
    while i < n:
        result += text
        i += 1
    return result
```

### Why it works

- Concatenates the same text n times.

### Try these tests

- `repeat_text("ha", 3)  # "hahaha"` → normal
- `repeat_text("x", 0)  # ""` → repeats zero times
- `repeat_text("", 5)  # ""` → empty stays empty

---

# Topic E — Lists (41–50)

## 41) Last Element (non-empty)

### Prompt

Write `last_element(nums: list[int]) -> int` (assume non-empty).

### Solution

```python
def last_element(nums: list[int]) -> int:
    return nums[-1]
```

### Why it works

- `nums[-1]` means “last item” in Python.

### Try these tests

- `last_element([3, 1, 9])  # 9` → normal
- `last_element([7])  # 7` → single item
- `last_element([1, 2])  # 2` → small list

---

## 42) First Two Elements (safe)

### Prompt

Write `first_two(nums: list[int]) -> list[int]` returning first two items (or fewer).

### Solution

```python
def first_two(nums: list[int]) -> list[int]:
    return nums[:2]
```

### Why it works

- Slicing handles short lists safely.

### Try these tests

- `first_two([1, 2, 3, 4])  # [1,2]` → normal
- `first_two([9])  # [9]` → shorter than 2
- `first_two([])  # []` → empty list

---

## 43) Swap First and Last

### Prompt

Write `swap_first_last(nums: list[int]) -> list[int]` (assume length ≥ 2).

### Solution

```python
def swap_first_last(nums: list[int]) -> list[int]:
    out = nums[:]  # copy
    out[0], out[-1] = out[-1], out[0]
    return out
```

### Why it works

- We copy first so we don’t change the original.
- Tuple swap swaps the two positions.

### Try these tests

- `swap_first_last([1,2,3,4])  # [4,2,3,1]` → normal
- `swap_first_last([9,8])  # [8,9]` → smallest valid
- `swap_first_last([-1, 0, 5])  # [5,0,-1]` → includes negatives

---

## 44) Count Above Average

### Prompt

Write `count_above_average(nums: list[int]) -> int` (assume non-empty).

### Solution

```python
def count_above_average(nums: list[int]) -> int:
    avg = sum(nums) / len(nums)
    count = 0
    for x in nums:
        if x > avg:
            count += 1
    return count
```

### Why it works

- First compute average.
- Then count values strictly greater than that average.

### Try these tests

- `count_above_average([1,2,3,4,10])  # 1` → only 10 is above
- `count_above_average([5,5,5])  # 0` → none strictly above
- `count_above_average([0, 10])  # 1` → average is 5

---

## 45) Remove All Occurrences

### Prompt

Write `remove_all(nums: list[int], target: int) -> list[int]`.

### Solution

```python
def remove_all(nums: list[int], target: int) -> list[int]:
    return [x for x in nums if x != target]
```

### Why it works

- We build a new list excluding the target.

### Try these tests

- `remove_all([1,2,1,3,1], 1)  # [2,3]` → removes many
- `remove_all([4,5], 9)  # [4,5]` → target not present
- `remove_all([], 1)  # []` → empty list

---

## 46) Append (Return New)

### Prompt

Write `append_new(nums: list[int], value: int) -> list[int]` without mutating nums.

### Solution

```python
def append_new(nums: list[int], value: int) -> list[int]:
    return nums + [value]
```

### Why it works

- `nums + [value]` creates a new list.

### Try these tests

- `append_new([1,2], 9)  # [1,2,9]` → normal
- `append_new([], 5)  # [5]` → empty list
- `append_new([0], 0)  # [0,0]` → duplicates allowed

---

## 47) Flatten One Level

### Prompt

Write `flatten(items: list[list[int]]) -> list[int]`.

### Solution

```python
def flatten(items: list[list[int]]) -> list[int]:
    out: list[int] = []
    for row in items:
        for x in row:
            out.append(x)
    return out
```

### Why it works

- Two loops: one over sublists, one over elements.

### Try these tests

- `flatten([[1,2],[3],[4,5]])  # [1,2,3,4,5]` → normal
- `flatten([[] , [1]])  # [1]` → empty inner list
- `flatten([])  # []` → empty outer list

---

## 48) Rotate Left by k

### Prompt

Write `rotate_left(items: list[int], k: int) -> list[int]`. Wrap around. If empty, return [].

### Solution

```python
def rotate_left(items: list[int], k: int) -> list[int]:
    if not items:
        return []
    k = k % len(items)
    return items[k:] + items[:k]
```

### Why it works

- `k % len(items)` handles large k.
- Slicing and concatenation performs the rotation.

### Try these tests

- `rotate_left([1,2,3,4,5], 2)  # [3,4,5,1,2]` → typical
- `rotate_left([1,2,3], 5)  # [3,1,2]` → k larger than length
- `rotate_left([], 3)  # []` → empty list

---

## 49) Is Sorted (Ascending)

### Prompt

Write `is_sorted(nums: list[int]) -> bool` for non-decreasing order.

### Solution

```python
def is_sorted(nums: list[int]) -> bool:
    for i in range(1, len(nums)):
        if nums[i] < nums[i - 1]:
            return False
    return True
```

### Why it works

- If any item is smaller than the one before it, order is broken.

### Try these tests

- `is_sorted([1,2,2,5])  # True` → duplicates allowed
- `is_sorted([3,2,1])  # False` → decreasing
- `is_sorted([])  # True` → empty list is “sorted” by convention

---

## 50) Has Duplicates

### Prompt

Write `has_duplicates(nums: list[int]) -> bool`.

### Solution

```python
def has_duplicates(nums: list[int]) -> bool:
    seen: set[int] = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False
```

### Why it works

- Sets store unique values.
- If we see the same value again, it’s a duplicate.

### Try these tests

- `has_duplicates([1,2,3,2])  # True` → repeats
- `has_duplicates([1,2,3])  # False` → all unique
- `has_duplicates([])  # False` → empty has no duplicates

---

# Topic F — Dictionaries (51–60)

## 51) Frequency Dictionary (Numbers)

### Prompt

Write `frequency(nums: list[int]) -> dict[int, int]` counting occurrences.

### Solution

```python
def frequency(nums: list[int]) -> dict[int, int]:
    counts: dict[int, int] = {}
    for x in nums:
        counts[x] = counts.get(x, 0) + 1
    return counts
```

### Why it works

- `get(x, 0)` returns 0 if the key doesn’t exist yet.
- Then we add 1 each time we see x.

### Try these tests

- `frequency([2,2,5,2,5])  # {2:3, 5:2}` → multiple keys
- `frequency([])  # {}` → empty input
- `frequency([1,1,1])  # {1:3}` → single key repeated

---

## 52) Character Frequency (Ignore Spaces)

### Prompt

Write `char_frequency_no_spaces(s: str) -> dict[str, int]` ignoring spaces.

### Solution

```python
def char_frequency_no_spaces(s: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for ch in s:
        if ch == " ":
            continue
        counts[ch] = counts.get(ch, 0) + 1
    return counts
```

### Why it works

- We skip `' '`.
- Count the rest using the same counting pattern.

### Try these tests

- `char_frequency_no_spaces("a b a c")` → checks skipping spaces
- `char_frequency_no_spaces("   ")  # {}` → only spaces
- `char_frequency_no_spaces("!!a!!")` → punctuation counts too (not spaces)

---

## 53) Get With Default

### Prompt

Write `get_with_default(d: dict[str, int], key: str, default: int) -> int`.

### Solution

```python
def get_with_default(d: dict[str, int], key: str, default: int) -> int:
    return d.get(key, default)
```

### Why it works

- `.get` gives a safe lookup without crashing if key is missing.

### Try these tests

- `get_with_default({"a": 3}, "a", 0)  # 3` → key exists
- `get_with_default({"a": 3}, "b", 0)  # 0` → key missing
- `get_with_default({}, "x", 9)  # 9` → empty dictionary

---

## 54) Sum of Dictionary Values

### Prompt

Write `sum_dict_values(d: dict[str, int]) -> int`.

### Solution

```python
def sum_dict_values(d: dict[str, int]) -> int:
    total = 0
    for v in d.values():
        total += v
    return total
```

### Why it works

- `d.values()` gives all the values.
- Add them up like a normal sum.

### Try these tests

- `sum_dict_values({"a": 2, "b": 5})  # 7` → normal
- `sum_dict_values({})  # 0` → empty dict
- `sum_dict_values({"x": -1, "y": 1})  # 0` → negatives possible

---

## 55) Most Frequent Number

### Prompt

Write `most_frequent_number(nums: list[int]) -> int`. Tie: return the smaller number.

### Solution

```python
def most_frequent_number(nums: list[int]) -> int:
    counts: dict[int, int] = {}
    for x in nums:
        counts[x] = counts.get(x, 0) + 1

    best_num = nums[0]
    best_count = counts[best_num]

    for x, c in counts.items():
        if c > best_count or (c == best_count and x < best_num):
            best_num = x
            best_count = c

    return best_num
```

### Why it works

- Build counts first.
- Track best by (1) higher count, (2) smaller number when tied.

### Try these tests

- `most_frequent_number([2,2,3,3,3,1,1])  # 3` → clear winner
- `most_frequent_number([4,4,5,5])  # 4` → tie, choose smaller
- `most_frequent_number([9])  # 9` → single element

---

## 56) Merge Counts

### Prompt

Write `merge_counts(a: dict[str, int], b: dict[str, int]) -> dict[str, int]` (add counts).

### Solution

```python
def merge_counts(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    out: dict[str, int] = {}

    for k, v in a.items():
        out[k] = v

    for k, v in b.items():
        out[k] = out.get(k, 0) + v

    return out
```

### Why it works

- Copy a into out.
- Add b’s counts using `get`.

### Try these tests

- `merge_counts({"a": 2}, {"a": 1, "b": 3})` → overlapping key
- `merge_counts({}, {"x": 1})` → empty a
- `merge_counts({"x": 5}, {})` → empty b

---

## 57) Word Count

### Prompt

Write `word_count(s: str) -> dict[str, int]` using spaces to separate words.

### Solution

```python
def word_count(s: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for w in s.split():
        counts[w] = counts.get(w, 0) + 1
    return counts
```

### Why it works

- `split()` breaks into words (and automatically collapses multiple spaces).
- Count each word.

### Try these tests

- `word_count("hi hi bye")` → repeated word
- `word_count("   a   b  a ")` → multiple spaces handled
- `word_count("")  # {}` → empty string gives empty list of words

---

## 58) Keys With Count At Least k

### Prompt

Write `keys_at_least(d: dict[str, int], k: int) -> list[str]` sorted.

### Solution

```python
def keys_at_least(d: dict[str, int], k: int) -> list[str]:
    out: list[str] = []
    for key, val in d.items():
        if val >= k:
            out.append(key)
    out.sort()
    return out
```

### Why it works

- Filter keys by the condition, then sort the result.

### Try these tests

- `keys_at_least({"a": 2, "b": 5, "c": 1}, 2)  # ["a","b"]` → normal
- `keys_at_least({"x": 1}, 2)  # []` → none meet k
- `keys_at_least({}, 1)  # []` → empty dict

---

## 59) Invert Dictionary (Unique Values)

### Prompt

Write `invert_unique(d: dict[str, int]) -> dict[int, str]` (values are unique).

### Solution

```python
def invert_unique(d: dict[str, int]) -> dict[int, str]:
    out: dict[int, str] = {}
    for key, val in d.items():
        out[val] = key
    return out
```

### Why it works

- If values are unique, each value becomes a key safely.

### Try these tests

- `invert_unique({"a": 1, "b": 2})  # {1:"a", 2:"b"}` → normal
- `invert_unique({})  # {}` → empty
- `invert_unique({"x": 99})  # {99:"x"}` → single item

---

## 60) Histogram Bars

### Prompt

Write `histogram(nums: list[int]) -> dict[int, str]` mapping number → `"*" * count`.

### Solution

```python
def histogram(nums: list[int]) -> dict[int, str]:
    counts: dict[int, int] = {}
    for x in nums:
        counts[x] = counts.get(x, 0) + 1

    out: dict[int, str] = {}
    for x, c in counts.items():
        out[x] = "*" * c

    return out
```

### Why it works

- First count how many times each number appears.
- Then build star strings using `"*" * c`.

### Try these tests

- `histogram([2,2,5,5,5])  # {2:"**", 5:"***"}` → two keys
- `histogram([])  # {}` → empty
- `histogram([7])  # {7:"*"}` → single number

