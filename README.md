# ICCS102 Coding Battle - README

A lightweight classroom mini-game for **live coding battles** with **live scoring** and a **one-click stage grader**.

This project supports a fun, competitive activity where:

* one team codes live as the **Stage Team**
* other teams act as **Snipers** (identify *major* issues)
* scores are tracked across many rounds
* the **grader** can be run instantly from the UI

---

## Project Folder Structure (current)

Keep these files in the **same folder** (project root):

* `grader.py` — the stage grader (grades `stage.py`)
* `img.png` — optional image shown in the UI
* `live_battle.py` — the scoreboard UI (includes the Run Grader button)
* `live_battle_state.json` — (auto-created) persistent scores + round log
* `stage.py` — the student’s live-coded solution for the current round

The grader also creates:

* `stage_grading_report.json` — latest grading report (JSON)

---

## Quick Start

### 1) Run the Live Battle UI

```bash
python live_battle.py
```

### 2) During each round

1. The UI shows a **random exercise** (no repeats)
2. Stage Team codes the solution in `stage.py`
3. Instructor assigns:

   * Stage Team points (0–3)
   * Up to 2 sniping teams (+1 each, different issues)
4. Click **Finalize Round & Next**

### 3) One-click grading

Click **Run Grader** in the UI to run:

```bash
python grader.py
```

* `grader.py` always grades **`stage.py` in the same folder**.
* Output is shown in a popup.

---

## Activity Rules

### Round Timing (~7 minutes)

* **5 min** Stage coding time
* **1 min** sniping window (teams call out issues)
* **~1 min** instructor confirmation + scoring + transition/buffer

Planned use:

* **2 sessions**, about **1.5 hours** each
* Typically **~12–13 rounds per session**

### Exercise Selection

* Random selection
* **No repeats** until the pool is exhausted

### Stage Team Participation

* Each round: **2 students** from Stage Team come up and code together
* Each student may appear on stage **max 2 times per session**

  * “Valid” means present + not already twice
  * If a team has too few available members, repeats are allowed

---

## Scoring

### Stage Team: 0–3 points (instructor awarded)

* **3** = correct + acceptable clarity
* **2** = correct but has a minor issue / messy / edge-case concern
* **1** = partially correct / very close
* **0** = incorrect / fails clearly

> **No style sniping.** Instructor may *rarely* deduct 1 point for truly unreadable/unconventional code.

### Sniping Teams: +1 point each (max 2 teams per round)

* Snipes must be **major issues** only:

  * wrong output, exception, wrong function name, wrong parameters, missing return, etc.
* A sniping point is awarded only if:

  * the issue is real, and
  * the instructor confirms it (often via the grader)
* **Max 2 sniping teams** can score per round
* Must be **different issues**
* **First come first served** by instructor judgment

---

## UI Features

* Live **Scoreboard**
* Persistent **Round Log**
* **Undo Last Round**
* Auto-rotating **Stage Team**
* Random **exercise picker** (no repeats)
* Optional image under Session box (uses `img.png`)

---

## Reset / New Session

* **New Session**: resets scores and round log (keeps used exercises unless you reset)
* **Reset used list**: allows exercises to appear again from the beginning
* State persists in `live_battle_state.json`

---

## Troubleshooting

### “Run Grader” says **grader not found**

* Ensure `grader.py` is in the same folder as `live_battle.py`

### “Run Grader” says **stage.py not found**

* Ensure the student’s code is saved as `stage.py` in the same folder

### Image doesn’t show

* Ensure `img.png` exists in the same folder

---

## Version

**v1.0**
