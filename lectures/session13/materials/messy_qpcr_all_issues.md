# Answer key: messy_qpcr_exp14.xlsx (for instructors only)

## Structure
- Title in a merged cell (A1:I1); metadata (date, operator) in a free-text line (A2)
- Two-row header with merged cells (row 4 "Ct values" / "Lysate", row 5 actual names)
- Second table (summary of mean Ct) below the data on the same sheet, with hardcoded values
- Margin notes in column K carry real information (red = exclude, yellow = repeat, normalise to GAPDH)
- A hidden column J (run_id) that nobody told you about
- Cell comment on B4 ("Delta Ct or raw?"), so the data's meaning is unclear
- Sheet "plate layout" is a 96-well grid map, not tabular; sheet "Sheet3" holds a stray number (0.93, "R2 std curve?")

## Gene names and headers
- B5 and C5 were SEPT2 and MARCH1 but are stored as dates (2-Sep, 1-Mar)
- "ACTB " has a trailing space; header "conc." and "Vol" have no units; "measured" is a date, "comment" is free text

## Sample labels (treatment/dose/replicate all encoded in one string)
- Control: Ctrl_1 (trailing space), control_2, Control 3, ctrl-4
- Drug A 10 µM: DrugA_10uM_1, "Drug A 10 µM 2", DrugA_10um_3 (um instead of uM), "drugA 10uM rep4"
- Drug A 50 µM: DrugA_50uM_1/2, "Drug A 50µM 3", "DrugA 50uM_4"
- Drug B: DrugB_10uM_1/2, "Drug B_10uM_3"

## Ct values
- Decimal commas stored as text (e.g. "28,68") mixed with true numbers
- Annotations inside cells: "24.3 (?)"
- Non-numeric codes: "Undetermined", "n.d."
- One truly missing value (DrugB_10uM_2, GAPDH): missing vs. not detected is undocumented

## Lysate concentration and volume
- Units inside the cell: "5.2 mg/mL", "5.1mg/ml" (no space, different case)
- Mixed decimal comma/point: "4,8 mg/mL"
- Mixed units: "0.0049 g/mL" and "5400 µg/mL" in a column of mg/mL
- Volume: 20, "20 µL", "20ul", "0.02 mL" (same value, four notations)

## Dates
- Real date cells mixed with text: "12.03.2025", "3/12/2025" (ambiguous: US or EU?), "12.03.25", "12.3.2025", "March 13"

## Meaning carried by formatting only
- Red rows (excluded): "drugA 10uM rep4" and "DrugB_10uM_1". The only hint is the note in K5, and "contaminated?" in the comment column for one of them
- Yellow sample cells (repeat if time): DrugA_10uM_1 and DrugA_50uM_1; explained only in K7

## Summary table traps
- Hardcoded means, not formulas; they do not exactly match the data above
- "Drug A high" has n = "3 (4)", text in a numeric column, and it is unclear which sample was dropped
- Group names ("control", "Drug A low") do not match sample labels

## Suggested target (tidy) schema
sample_id | treatment | dose_uM | replicate | gene | ct | ct_flag | lysate_mg_per_ml | volume_ul | measured_date | excluded | exclusion_reason | run_id

(one row per sample x gene; flags such as "undetermined" go in ct_flag, not in the ct column)

## Decisions students should document
- How to treat "Undetermined", "n.d.", and "(?)" values
- Whether to exclude the red rows, and where the reason is recorded
- How the ambiguous date 3/12/2025 was interpreted
- What to do with the hidden run_id column
- Whether the summary table is rebuilt from the data or discarded
