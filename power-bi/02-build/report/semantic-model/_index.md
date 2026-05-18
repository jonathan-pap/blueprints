# semantic-model/ — atomic files

> Read TMDL from the report side. **No live model connection** — these all read files on disk in `<project>.SemanticModel/`. For live values or DAX validation, go to `../../../03-bind/`.

- `find-field-from-tmdl.md` — locate a field's canonical name from TMDL
- `read-measure-definition.md` — get the DAX for an existing measure
- `infer-dax-from-visual.md` — derive the DAX a visual is generating
- `rebind-to-different-field.md` — swap a visual's binding from old field to new
