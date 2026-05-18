# reviewers/ — review checklists

> Pre-flight checks to run on generated content before showing it to the user. One file per artifact type.

- `pbip-validator-checklist.md` — full PBIP project diagnostic flow (validate_pbip.py + pbir validate + manual TMDL pass)
- `deneb-review.md` — Deneb Vega / Vega-Lite spec validation
- `svg-review.md` — SVG DAX measure validation
- `python-review.md` — Python visual script validation
- `r-review.md` — R visual script validation

## When to use

After generating any of the above artifact types, run the matching checklist before declaring the work done. Each returns PASS / FAIL per check, up to 3 design suggestions, and a verdict (READY / NEEDS CHANGES).

## Output

Don't write the checklist results to a file by default — they're inline review notes. If the verdict is NEEDS CHANGES and the user asks to track them, dump the review to `../../outputs/YYYY-MM-DD-<project>-<type>-review.md`.
