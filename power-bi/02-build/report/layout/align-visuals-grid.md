# Equal-gap grid

Same as `align-visuals-row.md` but in both axes. Column edges in row 2 must match row 1.

## Critical rule

Vertical column edges must align across rows. The gap position in row 2 must be the same x-coordinate as row 1.

```
RIGHT (aligned):
+------ 608 ------+--16--+------ 608 ------+   Row 1
+------ 608 ------+--16--+------ 608 ------+   Row 2
                  ^
                  Same column edge

WRONG (misaligned):
+------ 648 ------+--16--+---- 568 ----+        Row 1
+--- 500 ---+--16--+------- 716 ------+        Row 2
```

## Formula

Compute `visual_width` once per column, reuse the same x positions across every row.

## Worked example

2 charts side-by-side, then a full-width table below. Page 1280 × 720, margin 24, gap 16:

```
Row 1: 2 visuals → visual_width = (1232 - 16) / 2 = 608. x = 24, 648.
Row 2: 1 full-width visual → x = 24, width = 1232.
```

Commands as in `align-visuals-row.md` but with the row 2 visual spanning both column positions.

## After

`../validate/validate.md`.
