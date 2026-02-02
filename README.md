# Mini DMN Compiler & Clinical Interpreter

This project implements a **deterministic clinical decision engine** for Community Health Workers (CHWs).  
It digitizes paper-based clinical manuals by converting plain-language medical guidelines into **executable Decision Model and Notation (DMN) rulesets**, visualizes decision logic using **Mermaid flowcharts**, and provides a **traceable execution engine** for patient data.

---

## Project Structure

- **`compiler.py`**  
  Rule Extraction component. Parses clinical manual text into structured JSON and maps each rule to a `chunk_id` for traceability.

- **`interpreter.py`**  
  Execution engine. Handles boolean expression parsing (`AND`, `OR`, `NOT`, parentheses) and implements DMN-style *fall-through semantics* where the first matching rule wins. Also includes **Lint Mode** logic to highlight potential unreachable rules.

- **`mermaid.py`**  
  Translates the ruleset into a `flowchart TD` Mermaid diagram for visual validation.

- **`main.py`**  
  Runs the end-to-end pipeline in the following order: rule extraction from manual excerpt, visualization with mermaid diagram, linting, and patient evaluation.

- **`test_interpreter.py`**  
  Automated test suite verifying logic correctness and safety-focused error handling.

---

## Setup & Requirements

- **Python 3.6+** (any version 3.6 or later should work, I used Python 3.8.10)
- **Dependencies:**  
  Uses only Python standard libraries (`json`, `re`, `unittest`) for zero-dependency portability

---

## How to Run

Run the complete pipeline and generate all deliverables:

```bash
python3 main.py
```

### Generated Deliverables

- **`reconstructed_ruleset.json`**  
  Structured ruleset extracted from the manual text, including evidence fields.

- **`ruleset_flowchart.mmd`**  
  Mermaid source code representing the decision graph.

- **`interpreter_output.json`**  
  Detailed results for 10 patients, including decision paths and evidence.

---

## Automated Testing

To run the logic verification tests:

```bash
python3 test_interpreter.py
```

This test suite verifies:
- Correct clinical outcomes
- Proper default fallbacks
- Robust error handling for missing or invalid data

---

## Optional Bonus: Clinical Lint Mode

The project includes a **Lint Mode** designed to detect logical inconsistencies in clinical manuals *before* deployment. It identifies:

- **Unreachable Rules**  
  Rules placed after a catch-all (`true`) condition.

- **Redundant Logic**  
  Duplicate conditions that can never trigger.

- **Subset Shadowing**  
  Specific rules (e.g., `A AND B`) placed after broader rules (e.g., `A`).

---

### Testing the Linter

To test linting behavior, point `MANUAL_PATH` in `main.py` to `test_lint.jsonl`.  
This sample intentionally includes logical errors:

- `R3` duplicates `R2`
- `R5` and `R6` are unreachable due to the catch-all rule in `R4`
- `R6` is shadowed by the broader condition in `R1`

---

## Requirement Fulfillment

DMN Semantics: Top-to-bottom evaluation; first match wins 
Expression Language: AND, OR, NOT, parentheses, bare variables 
Evidence Mapping: Every rule and outcome links to `chunk_id` 
Mermaid Output: Flowchart TD decision visualization 
Error Handling: Clear failures for missing data, unknown variables, invalid syntax 
Patient Output: `patient_id`, outcome, matched_rule, path, justification, evidence 
