# bind/ — atomic files

- `find-canonical-name.md` — discover real table/field names from the model (no live conn)
- `bind-field.md` — add a field to a visual role
- `column-vs-measure.md` — set the correct field kind (most common binding bug)
- `swap-field.md` — replace a bound field with a different one
- `clear-binding.md` — remove a field from a role
- `inspect-bindings.md` — show what fields are bound where

## Golden rule

Never guess a field name. Run `find-canonical-name.md` first. A typo silently produces a binding error only Power BI Desktop catches.
