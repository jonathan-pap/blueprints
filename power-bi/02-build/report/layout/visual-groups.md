# Group visuals (move/scale together)

> A visual group binds several visuals so they reposition and resize as one unit — header
> strips, KPI rows, chart+caption pairs. The group is itself a special visual on the page;
> members are normal visuals tagged with the group as parent.

## Inspect

```bash
pbir visuals group "<project>.Report/Overview.Page" --list
```

Lists every group on the page with member counts and mode.

## Create

```bash
pbir visuals group "<project>.Report/Overview.Page" --create "KPI Group"
pbir visuals group "<project>.Report/Overview.Page" --create "Header" --mode ScaleMode
```

Creates an empty group at the page origin (default mode `ScaleMode`). Reposition with
`../layout/position-visual.md`.

## Add / remove members

```bash
pbir visuals group "<...>/Overview.Page/KPI Group.Visual" --add "Card_Revenue.Visual"
pbir visuals group "<...>/Overview.Page/KPI Group.Visual" --add "Card_Margin.Visual" --add "Card_Units.Visual"
pbir visuals group "<...>/Overview.Page/KPI Group.Visual" --remove "Card_Units.Visual"
```

`--add` / `--remove` are repeatable. The path is the **group** visual; values are member names
on the same page.

## Ungroup

```bash
# one member leaves, stays on page:
pbir visuals group "<...>/Overview.Page/Card_Revenue.Visual" --ungroup
# whole group dissolved, members stay:
pbir visuals group "<...>/Overview.Page/KPI Group.Visual" --ungroup
```

Behavior depends on whether the path points at a member or the group container.

## Hand-authoring equivalent

In `visual.json`, a member carries `parentGroupName: "<group visual name>"`; the group is a
visual with `visualType: "group"`. When generating pages with a build script, set
`parentGroupName` on each member (and drop it when relaying a harvested visual into a new
ungrouped page — see `projects/test/_build-native-gallery.py`, which `pop`s it).

## When to use / not

- **Use:** header bands (logo+title+nav), KPI rows that should scale uniformly, chart+caption pairs.
- **Don't:** independent positioning across pages (use page templates); visual *hierarchy* —
  that's alignment (`align-visuals-row.md` / `align-visuals-grid.md`), not grouping.

## After

`pbir validate "<project>.Report"` checks group parent links (a group referencing a missing
member fails). Run after every group mutation → `../validate/validate.md`.
