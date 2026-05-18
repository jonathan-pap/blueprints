# Selection signals — Power BI cross-filter integration

Deneb exposes Power BI's selection state as a Vega signal called `pbiSelection`. Wire it to make charts respond to cross-filter and emit selections back.

## Read selection (highlight selected marks)

```json
{
  "mark": { "type": "bar" },
  "encoding": {
    "opacity": {
      "condition": { "test": "datum.__selected__ === 'on'", "value": 1.0 },
      "value": 0.3
    }
  }
}
```

`__selected__` is a per-row field added by Deneb based on `pbiSelection`. Values: `'on'`, `'off'`, `'neutral'`.

## Emit selection (clicking a mark filters other visuals)

```json
{
  "mark": "bar",
  "params": [{
    "name":   "highlight",
    "select": { "type": "point" }
  }],
  "encoding": {
    "opacity": { "condition": { "param": "highlight", "value": 1 }, "value": 0.3 }
  }
}
```

The selected datum is sent back to Power BI via Deneb's selection bridge. Other visuals on the page cross-filter accordingly.

## Tooltip

```json
"tooltip": [
  { "field": "Category", "type": "nominal" },
  { "field": "Y",        "type": "quantitative", "format": ",d" }
]
```

Tooltips render natively via Power BI's tooltip system, not Vega's.

## Limitation

Some Power BI features (drillthrough, "Show as table") don't work on Deneb visuals. Document if your dashboard relies on them.
